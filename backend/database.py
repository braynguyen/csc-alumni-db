import sqlite3

DATABASE = "alumni.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            name TEXT PRIMARY KEY
        )
    """)

    # graduated attribute can be inferred from grad year
    # dates are stored in 'YYYY-MM-DD' format
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            pittId TEXT PRIMARY KEY,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            gradDate INTEGER NOT NULL,
            location TEXT,
            company TEXT,
            FOREIGN KEY (company) references companies(name)
        )
    """)

    # dates are stored in 'YYYY-MM-DD' format
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            company TEXT NOT NULL,
            pittId TEXT NOT NULL,
            date INTEGER NOT NULL,
            role TEXT NOT NULL,
            PRIMARY KEY (company, pittId, date),
            FOREIGN KEY (pittId) REFERENCES members (pittId),
            FOREIGN KEY (company) REFERENCES companies (name)
        )
    """)
    conn.commit()
    conn.close()
