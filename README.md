# postgres-import-wizard
Responsible for importing a raw data set into a table in a Postgres database

# Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)

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
  --schema SCHEMA       Name of schema in which to create table (default: raw)
  --table TABLE         Name of table to create (default: None)
```
