# Python Commons
[![PyPI version](https://badge.fury.io/py/drizm-commons.svg)](https://badge.fury.io/py/drizm-commons)  

This package includes shared code used by
the Drizm organizations development team.  

It is not intended for public usage but you
may still download, redistribute or 
modify it to your liking.

## Usage

Basic Install (utils only):  
>pip install drizm-commons


Full install (SQLAlchemy features available):  
>pip install drizm-commons[sqla]

Import like so:  
*import drizm_commons*

## Documentation

### Utilities

**Convinience Functions:**  
````python
from drizm_commons.utils import *


# Check whether function name is dunder
is_dunder("__name__")  # True

# Check if a given string is a valid UUIDv4
uuid4_is_valid("myvalue")  # False

# Check if a URL is valid and the contents URL-Safe
url_is_http("https://myapp.com/")  # True

# Get the current applications root path
Path(get_application_root())
````

**Path with extra features:**
````python
from drizm_commons.utils import Path

# Recursively delete a folder
path = Path(__file__).parent
path.rmdir(recursive=True)
````

**Cache last passed parameter:**
````python
from drizm_commons.utils import memoize


@memoize
def foo(a):
    return a


foo(3)  # 3
foo()  # 3
````

### Introspection

````python
from drizm_commons.inspect import SQLAIntrospector


table = SQLAIntrospector(my_table_instance)

""" Attributes """
table.tablename  # get the name of the table
table.classname  # get the classname of the declarative instance
table.columns  # get all SQLA fields of the class
table.column_attrs  # get all SQLA fields + property and hybrid_property of the class
````

## Changelog

### 0.1.1

- Added SQLAlchemy JSON Encoder
- Fixed bugs related to the Introspection
API
- Added table registry
- Added additional utilities

### 0.1.2

- Added get_root_path and recursive delete
Path utilities
- Fixed various bugs

### 0.2.0

- Added full test suite
- Added testing tools
- Revamped introspection API
- Provided additional overrides for the
SQL connection adapter

### 0.2.1

- Added support for datetime JSON
encoding

### 0.2.2

- Improved in-code documentation
- Integrated additional utils from
drizm-django-commons

### 0.3.0

- Added introspection capabilities 
for property and SQLAlchemy's
hybrid_property
- SQLAEncoder now respects property
and hybrid_property on SQLA declarative
instances
- Additional customizability hooks
for custom fields or data handling
- Support for JSON-Encoding table
instances
- Added SQLA as optional dependency
- Added additional testing utilities

### 0.3.1

- Improved code documentation
- Added docs
- Added memoize function decorator
to cache last previously passed
function parameter

### 0.3.2

- Fixed issue with introspection API
picking up validation methods

### 0.3.3

- Added additional tests and bugfixes
