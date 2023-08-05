
# Table of Contents

1.  [Salient: A simple SQLAlchemy Linter](#org6332640)
    1.  [What is it?](#orgd4c6bef)
    2.  [Why?](#org962193d)
    3.  [Simple and Naive](#org0461335)
        1.  [The Benefits of Naivete](#orgc8fde2a)
        2.  [Trade-Offs](#org6abd652)
    4.  [The Name](#org8b43816)
    5.  [Usage](#orgc7de55c)
    6.  [Current State](#org1f4a428)
    7.  [Requirements](#org26d16f8)
    8.  [Contributing](#org1da3846)


<a id="org6332640"></a>

# Salient: A simple SQLAlchemy Linter


<a id="orgd4c6bef"></a>

## What is it?

Salient is a rather simple, naive, even simplistic, linter for SQLAlchemy class based models.


<a id="org962193d"></a>

## Why?

I wrote this after discovering that a SA model in a project I work on had a table column that was defined once and then redefined with a different definition later in the model. I have also found that unnecessary `nullable=True` and `index=False` can be found all over the place.  I wrote this after discovering that a SA model in a project I work on had a table column that was defined once and then redefined with a different definition later in the model. I have also found that unnecessary `nullable=True` and `index=False` can be found all over the place. 


<a id="org0461335"></a>

## Simple and Naive

Salient takes few options and parses SA models in a naive manner. Salient does not currently use an AST or a finite state machine to parse source code. Rather it parses like you might with grep.


<a id="orgc8fde2a"></a>

### The Benefits of Naivete

Salient should be simple to understand and to maintain.


<a id="org6abd652"></a>

### Trade-Offs

Salient assumes a Python module contains one SA class based model, so if you have a module with multiple classes and they have column names in common you would need to separate them or not check for redefined columns. This also means that if you have `nullable=True` in a module being linted outside of a column definition the linter is going to be most unhappy with you.


<a id="org8b43816"></a>

## The Name

Salient comes from my abbreviating SQLAlchemy as SA and it being a linter, SAli[e]nt.


<a id="orgc7de55c"></a>

## Usage

The idea, and hope, is that your SA models live in their own directory separate from other source code. Salient probably won't break if it sees other source, but it was really intended to mostly look at SA models.

`poetry run python salient.py -rni src/app/models/*.py`

    1 file(s) with errors were found.
    
    examples/all_problems.py
      Redefined Columns - unoriginal_column_name:
        16: Column(Integer)
        19: Column(Boolean)
      Unnecessary nullable=True:
        17:     col_1 = Column(nullable=True)
      Unnecessary index=False:
        18:     col_2 = Column(index=False)

You can run with the `-h` or `--help` parameter for more options.

    usage: salient.py [-h] [-n] [-i] [-r] [--config CONFIG] [-R RECURSIVE] [-1 STOP_AFTER_FIRST_ERROR] files [files ...]
    
    positional arguments:
      files                 files to lint
    
    optional arguments:
      -h, --help            show this help message and exit
      -n, --nullable-true   Check for unnecessary nullable=True
      -i, --index-false     Check for unnecessary index=False
      -r, --redefined-column
                            Check for columns that are redefined.
      --config CONFIG       Load options from CONFIG FILE.
      -R, --recursive       If FILES includes directories scan those as well
      -1 STOP_AFTER_FIRST_ERROR, --stop-after-first-error STOP_AFTER_FIRST_ERROR
                            stop after first error


<a id="org1f4a428"></a>

## Current State

Alpha / MVP

-   Believed to do what it says on the tin, but YMMV
-   Not all command line options are implemented. (help, and the three linting rules work, that is all)
-   Doesn't recurse subdirectories
-   Doesn't currently use a config file, and no environment variables have been implemented.
-   Still has TODOs in the code. :)
-   Mostly untested, but the most complex of the linters is tested.
-   PRs welcome!


<a id="org26d16f8"></a>

## Requirements

-   Python 3.8 or above.
    -   I've set the Poetry config to require Python 3.8 or above. I don't believe anything is preventing use with 3.7, but I am not opposed to throwing in a walrus here and there if it is the best way to do something.
-   Poetry, any modern version.


<a id="org1da3846"></a>

## Contributing

-   Code is formatted with the latest version of Black.
-   MyPy isn't configured yet, but please use typehints. (Not everything is typehinted, but the project is a day old at the time of this writing!)
-   New code should be tested.

