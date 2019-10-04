import argparse
import re
import sys

from psycopg2 import connect, sql, errors as pgerrors

from log import create_logger

def parse_args():
    parser = argparse.ArgumentParser(
        prog='postgres-import-wizard',
        description='Responsible for importing a raw data set into a table in a Postgres database',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Delete any table that already exists at "SCHEMA"."TABLE"'
    )
    parser.add_argument(
        '--delimiter',
        type=str,
        help='Delimiter separating fields in FILE',
        default=',',
        choices=[',', '|', '\t']
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to data file to import',
        required=True
    )
    parser.add_argument(
        '--postgres_connection',
        type=str,
        help='Postgres connection string for raw database',
        default='postgresql://postgres@localhost:5433/raw'
    )
    parser.add_argument(
        '--schema',
        type=str,
        help='Name of schema in which to create table',
        default='public'
    )
    parser.add_argument(
        '--table',
        type=str,
        help='Name of table to create',
        required=True
    )
    return parser.parse_args()

def main(logger, cur, clean, filename, delimiter, schema, table, fields):
    if clean:
        logger.info('Attempting to drop current data table')
        # Drop the table that already exists at "schema"."table"
        # If no such table exists, we will allow that exception to pass
        # We use savepoints to implement a rollback if the drop throws an error
        # Since we don't really want to rollback the overall transaction of which
        # this is only one component
        try:
            cur.execute('SAVEPOINT savedrop;')
            drop_table(
                cur=cur,
                schema=schema,
                table=table
            )
            cur.execute('RELEASE SAVEPOINT savedrop;')
            logger.info('Table dropped')
        except pgerrors.UndefinedTable:
            logger.info('No table currently exists there, proceeding to create it')
            cur.execute('ROLLBACK TO SAVEPOINT savedrop;')
            pass

    logger.info('Creating data table')
    create_table(
        cur=cur,
        schema=schema,
        table=table,
        fields=fields
    )
    logger.info('Table created')

    # Use stdin to stream file data into Postgres's COPY command
    # We use this (through copy_expert) instead of psycopg2's copy_from because
    # it allows for more flexibility
    # We use the encoding 'utf-8-sig' to allow for byte order marks that
    # tend to occur in government data sets that were prepared with Excel
    logger.info('Copying data file into the table')
    stmt = sql.SQL("""
        COPY {}.{} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER {});
    """).format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.Literal(delimiter)
    )
    with open(filename, 'r', encoding='utf-8-sig') as sys.stdin:
        cur.copy_expert(stmt, sys.stdin)

    logger.info('{} rows successfully copied into {}.{}'.format(cur.rowcount, schema, table))

def drop_table(cur, schema, table):
    stmt = sql.SQL("""
        DROP TABLE {}.{};
    """).format(
        sql.Identifier(schema),
        sql.Identifier(table)
    )
    cur.execute(stmt)

def create_table(cur, schema, table, fields):
    stmt = sql.SQL("""
        CREATE TABLE {}.{} (
            {} TEXT
        );
    """).format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(' TEXT,').join(map(sql.Identifier, fields))
    )
    cur.execute(stmt)

if __name__ == '__main__':
    args = parse_args()

    logger = create_logger()
    logger.info('Starting the wizard')

    try:
        logger.info('Connecting to db')
        conn = connect(args.postgres_connection)
        cur = conn.cursor()

        logger.info('Getting header line from file')
        with open(args.file, 'r', encoding='utf-8-sig') as f:
            header = f.readline().strip()

        # Extract fields using ',' as a delimiter
        # and clean any non-word character from field names
        # i.e., remove anything that isn't [a-zA-Z0-9_]
        fields = []
        pattern = re.compile('(\W)+')
        for field in header.split(args.delimiter):
            fields.append(pattern.sub('', field))

        logger.info('Beginning Postgres import...')
        main(
            logger=logger,
            cur=cur,
            clean=args.clean,
            filename=args.file,
            delimiter=args.delimiter,
            schema=args.schema,
            table=args.table,
            fields=fields
        )

        conn.commit()
    except Exception as err:
        logger.fatal('Exception occurred while loading raw data: ' + str(err))
    finally:
        conn.rollback()
        cur.close()
        conn.close()
        logger.info('Exiting the wizard. Goodbye.')
