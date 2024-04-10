import psycopg2
from decouple import config
from psycopg2 import sql
from psycopg2.errors import DuplicateDatabase

DB_DSN = config("QD_BACKEND_DB_URL")
DSN_WITHOUT_DB, DB_NAME = DB_DSN.rsplit("/", maxsplit=1)
POSTGRES_DB_DSN = f"{DSN_WITHOUT_DB}/postgres"

connection = psycopg2.connect(POSTGRES_DB_DSN)
connection.autocommit = True
with connection.cursor() as cursor:
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DB_NAME)))
    except DuplicateDatabase:
        pass
    else:
        print(f"Banco de dados criado: {DB_NAME}")

connection.close()
