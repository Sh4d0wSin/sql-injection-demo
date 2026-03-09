from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("demo.db")

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT)
     """)
    

    cursor.execute("""DELETE FROM users""")


    cursor.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        [
            ("admin", "admin123", "admin"),
            ("user1", "password1", "user"),
            ("user2", "password2", "user"),
        ]
    )


    conn.commit()
    conn.close()



init_db()


@app.post("/login/vulnerable")
def vulnerable_login(request: LoginRequest):
    conn = sqlite3.connect("demo.db")

    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + request.username + "' AND password = '" + request.password + "'"

    cursor.execute(query)

    results = cursor.fetchall()

    conn.close()

    return {"query": query, "results": results}

@app.post("/login/secure")
def secure_login(request: LoginRequest):
    conn = sqlite3.connect("demo.db")

    cursor = conn.cursor()

    param_query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    cursor.execute(param_query, (request.username, request.password))

    results = cursor.fetchall()

    conn.close()

    return {"param_query": param_query, "results": results}

@app.post("/reset")
def restart():

    init_db()
    
    return {"message": "Database reset"}


