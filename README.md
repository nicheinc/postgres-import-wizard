# postgres-import-wizard
Responsible for importing a raw data set into a table in a Postgres database

# Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [CSV, Public Schema](#csvpublic)
  - [CSV, Non-Public Schema](#csvnotpublic)
  - [Tab-Delimited](#tab)

## About <a name="about"></a>

We often have data in a file on our filesystem and we want to import it into a
table in a Postgres database. Other database management systems like Microsoft
SQL Server offer a graphical import wizard, but Postgres does not. The
`postgres-import-wizard` (henceforth known as the `wizard`) fills this gap.

The `wizard` is used to copy a flat-data file such as a CSV or tab-delimited
text file into a Postgres table. Although Postgres provides a built-in
[`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command, it
requires the table to already exist; otherwise there's nothing to copy the data
into. To circumvent this issue, the `wizard` reads the header of the file you
want to load and uses those fields to define a table with `text` columns in
a database you specify.

## Installation <a name="installation"></a>

No installation is required. The `wizard` is meant to be run directly from
source using Python 3.

That said, it's recommended to run this in a [Python virtual
environment](https://docs.python.org/3/library/venv.html) and install what's in
`requirements.txt` (which is really just
[`psycopg`](http://initd.org/psycopg/)).

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
All examples are run using the default Postgres connection string provided by
the utility, so be sure that if you run them verbatim you have a local Postgres
instance running on your machine, available at port 5433, with a database named
`raw`. Be sure to use a [Postgres password
file](https://www.postgresql.org/docs/current/libpq-pgpass.html) to specify
credentials for your database's user.

The example data sets provided under the `examples` folder are subsets of the
[Private School Universe Survey](https://nces.ed.gov/surveys/pss/) (PSS) for
the 2017-18 school year provided by the National Center for Education
Statistics. This data set provides a biennial census of private schools in the
United States of America.

### CSV, Public Schema <a name="csvpublic"></a>

Importing the example csv data set provided under `examples` can be done by
executing

```sh
$ python main.py --file examples/data.csv --table "example1"
```

Issuing that will load the comma-separated data set into a table named
`example1` within the default `public` schema of the database.

We can reimport the data:

```sh
$ python main.py --clean --file examples/data.csv --table "example1"
```

If we had omitted the `--clean` flag the `wizard` would have thrown an error
like

```sh
CRITICAL [2019-10-04 08:56:20] Exception occurred while loading raw data: relation "example1" already exists
```

### CSV, Non-Public Schema <a name="csvnotpublic"></a>

This example functions much the same as [CSV, Public Schema](#csvpublic) above
except we try to load the data into a non-public schema:

```sh
$ python main.py --file examples/data.csv --schema "sonic" --table "example1"
INFO [2019-10-04 09:12:27] Starting the wizard
...
CRITICAL [2019-10-04 09:12:27] Exception occurred while loading raw data: schema "sonic" does not exist
LINE 2:         CREATE TABLE "sonic"."example1" (
                             ^

INFO [2019-10-04 09:12:27] Exiting the wizard. Goodbye.
```

Oh no! We need to create the schema before we can create tables in it. After
creating a schema called `sonic` we can rerun the command above and everything
should complete fine.

### Tab-Delimited <a name="tab"></a>

The only tricky thing with importing a tab-delimited data file is that we need
to specify a literal `\t`. This can be accomplished by escaping it in our
argument list with `$'\t'`, like the following

```sh
$ python main.py --delimiter $'\t' --file examples/data.txt --table "example2"
```
