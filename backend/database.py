import sqlite3

DATABASE = "alumni.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            pittId TEXT PRIMARY KEY,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            gradYear INTEGER
        )
    """)
    conn.commit()
    conn.close()

create_table()

def check_tables(conn: sqlite3.Connection, curr: sqlite3.Cursor) -> bool:
    return bool(curr.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='members';
    """).fetchall())

def create_tables(conn: sqlite3.Connection, curr: sqlite3.Cursor):
    curr.execute("CREATE TABLE members(pitt_id, fname, lname, grad_date)")
    print("Table created.")
    conn.commit()


def insert_dummy_data(conn, curr, pitt_id, fname, lname, year):
    statement = """
        INSERT INTO members
                 (pitt_id, fname, lname, grad_date)
                 values (?, ?, ?, ?);
    """
    curr.execute(statement, (pitt_id, fname, lname, year))
    conn.commit()


def clear_tables(conn, curr, ):
    tables = curr.execute("""
                SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()

    for table in tables:
        curr.execute(f"DROP TABLE IF EXISTS {table[0]}")
    
    conn.commit()