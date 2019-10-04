# postgres-import-wizard
Responsible for importing a raw data set into a table in a Postgres database

# Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Basic](#basic)

## About <a name="about"></a>

## Installation <a name="installation"></a>

## Usage <a name="usage"></a>

```
usage: postgres-import-wizard [-h] [--clean] [--delimiter {,,|,	}] --file FILE
                              [--postgres_connection POSTGRES_CONNECTION]
                              [--schema SCHEMA] --table TABLE

Responsible for importing a raw data set into a table in a Postgres database

optional arguments:
  -h, --help            show this help message and exit
  --clean               Delete any table that already exists at
                        "SCHEMA"."TABLE" (default: False)
  --delimiter {,,|,	}   Delimiter separating fields in FILE (default: ,)
  --file FILE           Path to data file to import (default: None)
  --postgres_connection POSTGRES_CONNECTION
                        Postgres connection string for raw database (default:
                        postgresql://postgres@localhost:5433/raw)
  --schema SCHEMA       Name of schema in which to create table (default:
                        public)
  --table TABLE         Name of table to create (default: None)
```

## Examples <a name="examples"></a>

In this section we provide a few examples illustrating usage of the `wizard`.

### Basic <a name="basic"></a>

Importing the example csv data set provided under `examples` can be done by
executing

```sh
$ python main.py --file examples/data.csv --table "example1"
```

Issuing that will load the comma-separated data set into a table named
`example1` within the default `public` schema of the database.
