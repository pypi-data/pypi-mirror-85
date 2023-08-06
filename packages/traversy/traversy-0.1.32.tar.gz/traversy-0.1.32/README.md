# traversy

Fast data traversal & manipulation tools for Python. Check out the
[documentation](https://tensortom.github.io/traversy/).

[![Actively Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://gitHub.com/TensorTom/traversy/graphs/commit-activity)
[![MIT License](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/traversy/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/traversy/)

## Quick-Start

```python
from traversy import traverse
import json


jo = json.loads("""{
  "2019": {
    "uat": {
      "pkey": true,
      "user": "testval",
      "testkey": true,
      "mylist": [
      {
        "foo": "bar",
        "foo2": "bar2"
      },
      {
        "baz": "milk",
        "bar": "foo"
      }
      ]
    },
    "dev": {
      "pkey": true,
      "testval": "testval",
      "testval2": true
    },
    "test1": [1, 2, "testval"],
    "test2": [{"one": "foo", "two": "bar", "three": "testval"}]
  }
}""")

def is_eq(key, val, opath, query):  # Use of a filter func is optional.
    return val == query


for node in traverse(jo, is_eq, query="milk"):
    print("Found", node.key, ':', node.value)  # baz : milk
    print("Full path access:", jo[node.path_str])  # "2019.uat.mylist.1.baz"
```

For each iteration, traverse() returns a dict or data object of...

```
{'key', 'value', 'node_path', 'path_str', 'filter_func',
'filter_args': (data, kwargs), 'parent_node', 'output_formatter'}
```

For more information on these non-built-in data structure (Which are optional
to use), check out [mo-dots](https://pypi.org/project/mo-dots/) and
[dotty_dict](https://pypi.org/project/dotty-dict/).


### Changelog

- **11/15/2020 - 0.1.32** : Fix for pypi.

- **11/15/2020 - 0.1.3** : Refactored & added more utility methods. Added docs.

- **11/13/2020 - 0.1.2** : Doc correction.

- **11/13/2020 - 0.1.1** : Deprecated `set_output_format()` and made package compatible with both Python 2 and Python 3.