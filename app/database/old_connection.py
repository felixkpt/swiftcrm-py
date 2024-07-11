# app/database/old_connection.py
import mysql.connector
from mysql.connector import errorcode
from decouple import Config, RepositoryEnv

# Database connection configuration

DOTENV_FILE = '.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

DB_HOST = env_config.get('DB_HOST')
DB_USER = env_config.get('DB_USER')
DB_PASS = env_config.get('DB_PASS')
DB_NAME = env_config.get('DB_NAME')
config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASS,
    'database': DB_NAME,
    'raise_on_warnings': True
}

def get_connection():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def execute_query(query, params=None, fetch_method='all'):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute(query, params)
        cnx.commit()
        if cursor.with_rows:
            if fetch_method == 'all':
                return cursor.fetchall()
            elif fetch_method == 'first':
                return cursor.fetchone()
            else:
                raise ValueError("Invalid fetch method. Use 'all' or 'first'.")
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        cnx.close()

def execute_insert(query, params=None):
    cnx = get_connection()
    cursor = cnx.cursor()
    try:
        cursor.execute(query, params)
        cnx.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        cnx.close()

def start_transaction():
    cnx = get_connection()
    cnx.start_transaction()
    return cnx

def commit_transaction(cnx):
    try:
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error committing transaction: {err}")
    finally:
        cnx.close()

def rollback_transaction(cnx):
    try:
        cnx.rollback()
    except mysql.connector.Error as err:
        print(f"Error rolling back transaction: {err}")
    finally:
        cnx.close()

def execute_schema(schema_file):
    cnx = get_connection()
    cursor = cnx.cursor()
    try:
        with open(schema_file, 'r') as f:
            schema = f.read()
        for statement in schema.split(';'):
            if statement.strip():
                cursor.execute(statement)
        cnx.commit()
        print("Schema applied successfully.")
    except mysql.connector.Error as err:
        print(f"Error executing schema: {err}")
    except FileNotFoundError:
        print(f"Schema file {schema_file} not found.")
    finally:
        cursor.close()
        cnx.close()
