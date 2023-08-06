import datetime
import json
import re
from string import Formatter
from IPython.core.display import display

from azure.kusto.data.exceptions import KustoError, KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

from IPython.core.magic import (
    Magics,
    cell_magic,
    line_magic,
    magics_class,
    needs_local_scope,
)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display_javascript, HTML
try:
    from traitlets.config.configurable import Configurable
    from traitlets import Bool, Int, Unicode
except ImportError:
    from IPython.config.configurable import Configurable
    from IPython.utils.traitlets import Bool, Int, Unicode
from IPython.utils.io import capture_output
from IPython import get_ipython


def run_cell(cmd):
    with capture_output() as io:
        res = get_ipython().run_cell(cmd)
        if res.success:
            return io.stdout
    return None

def has_token_expired():
    res = run_cell('!az account get-access-token --query "expiresOn" --output tsv')
    if res is None:
        return None
    try:
        # Subtract a few minutes for buffer
        exp = datetime.datetime.fromisoformat(res[:19]) - datetime.timedelta(minutes=5)
        now = datetime.datetime.now()
        return exp < now
    except:
        # Something went wrong; do a login
        return True

def ensure_logged_in():
    exp = has_token_expired()
    if exp is None:
        return "Can't sign in to Azure. Do you have the Azure CLI tools installed?"
    elif exp:
        res =  run_cell('!az login')
        if res is None:
            return "Can't sign in to Azure. Please sign in from a terminal."
        elif res.find('You have logged in') >= 0:
            return None
        else:
            return "Sign in to Azure failed. Please sign in from a terminal."
    else:
        return None  # have existing token

def run_query(cluster, db, query):
    if cluster.find('://') < 0:
        cluster = f'https://{cluster}.kusto.windows.net'
    client = KustoClient(KustoConnectionStringBuilder.with_az_cli_authentication(cluster))
    response = client.execute(db, query)
    return dataframe_from_result_table(response.primary_results[0])


@magics_class
class KustoMagic(Magics, Configurable):
    """Runs KQL statement on a database.
    Provides the %%kql magic."""

    cluster = Unicode(
        None,
        config=True,
        allow_none=True,
        help="Default Kusto cluster to query",
    )
    database = Unicode(
        None,
        config=True,
        allow_none=True,
        help="Default Kusto database to query",
    )
    
    def __init__(self, shell):
        self.cluster = None
        self.database = None
        Configurable.__init__(self, config=shell.config)
        Magics.__init__(self, shell=shell)
        # Add ourself to the list of module configurable via %config
        self.shell.configurables.append(self)

    @needs_local_scope
    @line_magic("kqlset")
    @magic_arguments()
    @argument("-c", "--cluster", type=str, help="specify default cluster")
    @argument("-d", "--database", type=str, help="specify default database")
    def configure(self, line="", local_ns={}):
        """ Set the default Kusto cluster and/or database. This overrides
        what is in the extension configuration, but can in turn be overriden
        per query by the %kql magic.
        """
        args = parse_argstring(self.configure, line) 
        self.cluster = args.cluster
        self.database = args.database

    @needs_local_scope
    @line_magic("kql")
    @cell_magic("kql")
    @magic_arguments()
    @argument("line", default="", nargs="*", type=str, help="kql query")
    @argument("-c", "--cluster", type=str, help="specify cluster")
    @argument("-d", "--database", type=str, help="specify database")
    @argument("-f", "--file", type=str, help="Run KQL from file at this path")
    @argument("-s", "--set", type=str, help="name of Python variable to assign result to")
    @argument("-n", "--noexpand", action="store_true", help="Don't do variable expansion of {id}s")
    @argument("-q", "--quiet", action="store_true", help="Don't display dataframe")
    @argument("-e", "--error", action="store_true", help="Display raw Kusto error")
    def execute(self, line="", cell="", local_ns={}):
        """Runs KQL statement against a database in a cluster.
        If necessary, an attempt will be made to log in to Azure first.
        The result is returned as a Pandas DataFrame and assigned to a 
        Python variable (by default named kqlresult, unless overridden by --set).
        """
        # Parse variables (words wrapped in {}) for %%kql magic
        cell_variables = [
            fn for _, fn, _, _ in Formatter().parse(cell) if fn is not None
        ]
        cell_params = {}
        missing = None
        for variable in cell_variables:
            if variable in local_ns:
                cell_params[variable] = local_ns[variable]
            else:
                missing = variable

        # Strip any comments from the line
        #line = sql.parse.without_sql_comment(parser=self.execute.parser, line=line)

        # Get the arguments
        args = parse_argstring(self.execute, line)
        
        if not args.noexpand:
            if missing:
                raise NameError(missing)
            cell = cell.format(**cell_params)

        # save globals and locals so they can be referenced in bind vars
        user_ns = self.shell.user_ns.copy()
        user_ns.update(local_ns)

        command_text = " ".join(args.line) + "\n" + cell

        if args.file:
            with open(args.file, "r") as infile:
                command_text = infile.read() + "\n" + command_text

        #parsed = sql.parse.parse(command_text, self)
        parsed = command_text.strip()

        if not parsed:
            return

        # Make sure we are logged in
        err = ensure_logged_in()
        if err is not None:
            return err

        try:
            c = args.cluster or self.cluster
            if c is None:
                return "No cluster specified"
            d = args.database or self.database
            if d is None:
                return "No database specified"
            v = args.set or 'kqlresult'
            df = run_query(c, d, parsed)
            self.shell.user_ns.update({v: df})
            if not args.quiet:
                return df
        except KustoError as e:
            if args.error:
                raise e
            try:
                # This is all kinda kludgy          
                msg = e.args[0][0]['error']['@message']
                x = msg.find('line:position=')
                if x >= 0:
                    try:
                        x += 14
                        l, p = msg[x:x + msg[x:].find(']')].split(':')
                        l = int(l) - 1
                        p = int(p) - 1
                        lines = parsed.split('\n')
                        result = "<div style=\"fontfamily='monospace'\">"
                        for i, line in enumerate(lines):
                            result += line
                            result += "<br>"
                            if i == l:
                                result += "<div style=\"color: red\" >" + ('&nbsp;' * p) + '^ ' + msg + '</div><br>'
                        result += '</div>'
                        return HTML(result)
                    except Exception:
                        pass
                return msg
            except Exception:
                raise e
        except Exception as e:
            raise

  
def load_ipython_extension(ip):
    """Load the extension in IPython."""

    # this fails in both Firefox and Chrome for OS X.
    # I get the error: TypeError: IPython.CodeCell.config_defaults is undefined

    # js = "IPython.CodeCell.config_defaults.highlight_modes['magic_sql'] = {'reg':[/^%%sql/]};"
    # display_javascript(js, raw=True)
    ip.register_magics(KustoMagic)

