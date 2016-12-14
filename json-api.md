# Generic events submitted to the logger from the profiled machine

 - categoryname: Must be a valid category, so offcputime for now.
 - columnX: A column name for that category

```
{
  "hostname": "destiny",
  "time": "2016-10-24 17:12:43.288693",
  "categoryname":
    [
      {
        "column1": "value",
        "column2": "value",
      },
      {
        "column1": "value",
        "column1": value",
      }
    ],
}
```

# Offcputimecategory

elapsed is in nanoseconds

```
{
  "hostname": "destiny",
  "time": "2016-10-24 17:12:43.288693",
  "offcputime":
    [
      {
        "process": "dd",
        "pid": 1234,
        "stack": "sys_write;btrfs_file_write;some_enospc_function_that_sucks",
        "elapsed": 123456,
      }
    ]
}
```

# Queries format, submitted to the query service by the visualizer

categoryname - Must be a valid category, so offcputime for now.
 - limit: The number of items to fetch, if not present it returns all of them
 - elementN: Valid column names for the category
 - expr: Must be "=", "<", "<=", ">", ">=", "!=", "contains"
 - oper: Must be "and" or "or"
 - format: Must be "list" or "flamegraph".  If not specified we assume "list".

```
{
  "categoryname":
    {
      "elements": ["element1", "element2", "element3"],
      "format": "list"
      "limit": 5
      "constraints":
        [
          {
            "oper": "and",
            "conditions": [
              {
                "element1": "value",
                "expr": "="
              },
              {
                "element2": "value",
                "expr": "contains"
              },
            ]
          }
        ]
      }
}
```

The results will be in the following format for "format": "list"

```
{
  "categoryname": [
    {
      "element1": "value",
      "element2": "value",
      "element3": "value",
    },
  ]
}
```

The results will be in the following format for "format": "flamegraph"

```
{
  "name": "sys_write",
  "value": 123456,
  "children": [
    {
      "name": "btrfs_file_write",
      "value": 123456,
      "children": [
        {
          "name": "some_enospce_function_that_sucks",
          "value": 123450,
        },
        {
          "name": "prepare_pages",
          "value": 6,
        }
      ]
    }
  ]
}
```

This is meant to be used in conjunction with one of the d3 javascript such as

https://github.com/cimi/d3-flame-graphs

If "flamegraph" is specificed then "elements" must contain the field that
contains the collapsed stacktrace.  If no other field is specified then the
flamegraph is built based on frequency of the stack.  If a time field is also
specified it will be used as the time weight. Specifying more than 2 fields
will probably return something weird or error out.  Also you must only specify
one category, otherwise you will only get one categories flamegraph back and
it'll be random which one python finds first.

# Get categories

This is just a basic URL API, just open http://kernelscope/api/getcategories and
you will get a json response in the following format

column_type can currently be one of the following
 - string: Just a normal string
 - timestamp: A timestamp
 - int: An integer
 - stack: A stacktrace in the standard stacktrace format
 - elapsed: A time in usecs, usually for the given stacktrace

```
{
  "categoryname": [
    {
      "name": "database column name",
      "type": "column_type",
      "prettyname": "A pretty name for the column",
    }
  ]
}
```
