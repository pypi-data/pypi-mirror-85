# dockingFormatter

Simple formatter for docking of the compound logs. That takes docking log and returns interesting findings in format of xlsx file.

## Installation

You can install the **dockingFormatter** from [PyPI](https://pypi.org/project/dockingFormatter/):

```
pip install dockingFormatter
```

or

```
pip3 install dockingFormatter
```

The formatter is supported on Python3 and should be working fine on Python2.

## What it does

The dockingFormatter is a simple command line application, it takes docking log and then finds lowest affinity for the given compound. Afterwards returns the inforamtion in form of xmls file looking like that:

![Formatter output sample](images/xmls-formatter.png)

## How to use

```

$ dockingFormatter [DOCKING LOG FILE NAME] 

```

or with custom output file name

```

$ dockingFormatter [DOCKING LOG FILE NAME] --outputfile [CUSTOM NAME with or without xmls extension on the end]

```

to see all options and description you can use 

```

$ dockingFormatter --help

```

## Developing dockingFormatter

To install dockingFormatter, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```
