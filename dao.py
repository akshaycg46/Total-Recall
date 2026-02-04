import psycopg2
from psycopg2 import sql

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Akshay117',
    'host': 'localhost',
    'port': '5432'
}

def insert_data(text_data, vector_data):
    """
    Insert text and vector data into the PostgreSQL database.

    :param text_data: The text data to insert.
    :param vector_data: The vector data to insert (list of floats).
    :param db_params: Dictionary with database connection parameters (dbname, user, password, host, port).
    """
    # Convert vector to string format expected by pgvector
    vector_str = '{' + ','.join(map(str, vector_data)) + '}'

    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_params['dbname'],
            user=db_params['user'],
            password=db_params['password'],
            host=db_params['host'],
            port=db_params['port']
        )
        cur = conn.cursor()

        # Insert data into the table
        insert_query = """
        INSERT INTO spot (texts, vectors)
        VALUES (%s, %s)
        """
        cur.execute(insert_query, (text_data, vector_str))

        # Commit the transaction
        conn.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

def fetch_data():
    """
    Fetch all rows from the example_table.

    :param db_params: Dictionary with database connection parameters (dbname, user, password, host, port).
    :return: List of tuples containing rows from the example_table.
    """
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_params['dbname'],
            user=db_params['user'],
            password=db_params['password'],
            host=db_params['host'],
            port=db_params['port']
        )
        cur = conn.cursor()

        # Retrieve data
        cur.execute("SELECT * FROM spot;")
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
