from psycopg2 import connect


def create_connection(username="postgres", password="coderslab"):
    cnx = connect(
        user=username,
        password=password,
        host="localhost",
        database="active_db"
    )

    cursor = cnx.cursor()
    cnx.autocommit = True

    return cnx, cursor


def close_connection(cnx, cursor):
    cursor.close()
    cnx.close()
