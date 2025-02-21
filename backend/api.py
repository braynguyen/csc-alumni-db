from database import get_db_connection, initialize_tables
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
import sqlite3

# creating global reqs
app = FastAPI()
initialize_tables()


@app.get("/restart")
def clean_up():
    conn = get_db_connection()
    cursor = conn.cursor()
    tables = cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
    
    conn.commit()
    conn.close()

    initialize_tables()

# class Company(BaseModel):
#     name: str

@app.get("/companies/{company_name}")
def get_company(company_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM companies WHERE name = ?",
        (company_name,)
    )
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.get("/companies")
def get_companies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.post("/companies")
def create_company(company: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # values should sanitize input
    cursor.execute(
        "INSERT INTO companies (name) VALUES (?)", 
        (company,)
    )
    conn.commit()
    conn.close()

    return {
        "name": company
    }

class Member(BaseModel):
    pitt_id: str
    fname: str
    lname: str
    grad_date: str
    location: str
    company: str

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

    # values should sanitize input
    cursor.execute(
        "INSERT INTO members (pittId, fname, lname, gradDate, location, company) VALUES (?, ?, ?, ?, ?, ?)", 
        (member.pitt_id, member.fname, member.lname, member.grad_date, member.location, member.company)
    )
    conn.commit()
    conn.close()


    # create company if it does not exist in the database
    if not get_company(member.company):
        create_company(member.company)

    return {
        "pittId": member.pitt_id,
        "fname": member.fname,
        "lname": member.lname,
        "gradDate": member.grad_date,
        "location": member.location,
        "company": member.company
    }