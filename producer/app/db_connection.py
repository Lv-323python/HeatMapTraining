import psycopg2
from postgres_helpers.postgres_config import HOST, POSTGRES_PASSWORD, PORT, HEAT_MAP_DB, POSTGRES_USER


def create_database():
    """ create PostgreSQL database"""
    db_check_command = """
        SELECT datname from pg_database
    """
    db_create_command = """
        CREATE DATABASE heat_map_db
    """
    conn = None
    try:
        # read the connection parameters
        params = {
            'database': 'postgres',
            'user': POSTGRES_USER,
            'password': POSTGRES_PASSWORD,
            'host': HOST,
            'port': PORT
        }
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(0)
        cur = conn.cursor()

        cur.execute(db_check_command)
        dbs = cur.fetchall()
        print(dbs)

        if (HEAT_MAP_DB,) not in dbs:
            print('here')
            cur.execute(db_create_command)

        cur.close()
        conn.commit()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()