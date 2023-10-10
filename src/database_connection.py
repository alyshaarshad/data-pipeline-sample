import mysql
from mysql.connector import errorcode


def connect_to_db(host, port, user, password, database_name):
    try:
        cnx = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database_name
        )
        print(f"Connected to database '{database_name}'")
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{database_name}' does not exist. Creating a new one...")
            cnx = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
            cursor = cnx.cursor()
            cursor.execute(f"CREATE DATABASE {database_name}")
            cnx.database = database_name
            print(f"Database '{database_name}' created")
            return cnx
        else:
            print(err)

            
def create_tables(cursor,table_name):
    # Check if table exists
    table_exists = False
    try:
        cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
        table_exists = True
        print("Table exists")
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_NO_SUCH_TABLE:
            pass
        else:
            raise e

    # Create table if it doesn't exist
    if not table_exists:
        print("Creating table")
        cursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), user VARCHAR(255), repository_name VARCHAR(255), repository_owner VARCHAR(255), created_at DATETIME, merged_at DATETIME, tags VARCHAR(255), state VARCHAR(255), body TEXT)")
