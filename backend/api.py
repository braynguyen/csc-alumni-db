from database import get_db_connection, create_table
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
import sqlite3

# creating global reqs
app = FastAPI()
create_table()

class Member(BaseModel):
    pitt_id: str
    fname: str
    lname: str
    grad_year: int

@app.get("/members")
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.post("/members")
def create_member(member: Member):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO members (pittId, fname, lname, gradYear) VALUES (?, ?, ?, ?)", 
        (member.pitt_id, member.fname, member.lname, member.grad_year)
    )
    conn.commit()
    conn.close()

    return {
        "pittId": member.pitt_id,
        "fname": member.fname,
        "lname": member.lname,
        "gradYear": member.grad_year
    }

# if __name__ == "__main__":
#     if not check_tables(curr):
#         create_tables(conn, curr)
    
#     insert_dummy_data(conn, curr, "btn16", "Brayden", "Nguyen", 2025)

#     print(
#         curr.execute("""
#             SELECT * FROM members;
#         """).fetchall()
#     )
    
#     clear_tables(conn, curr)
#     conn.close()