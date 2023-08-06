import os
from io import open

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md"), encoding="utf-8").read()


version = "0.0.8"

install_requires = [
    "prettytable<1",
    "ipython>=1.0",
    "ipython-genutils>=0.1.0",
]


setup(
    name="ipython-kusto",
    version=version,
    description="Microsoft Kusto access via IPython",
    long_description=README + "\n",
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Programming Language :: Python :: 3",
    ],
    keywords="database ipython kusto",
    author="Graham Wheeler",
    author_email="graham@grahamwheeler.com",
    url="https://github.com/gramster/ipython-kusto",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
