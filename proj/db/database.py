import sqlite3
import pandas as pd
from utils.hashing import hash_password
class DB:
    def __init__(self, path="hospital_db.sqlite"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()
    def create_tables(self): # create tables on loss of database
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'patient'
            )
        """)
        self.conn.commit()
    def register_user(self, username, password):
        try:
            self.cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password))
            )
            self.conn.commit()
            return True, "Account created!"
        except sqlite3.IntegrityError:
            return False, "Username already exists."
    def authenticate(self, username, password):
        pwd_hash = hash_password(password) # as it is not passobile to dehash a password, we check if the hash match
        self.cur.execute(
            "SELECT username, role FROM users WHERE username=? AND password_hash=?",
            (username, pwd_hash)
        )
        return self.cur.fetchone()
    def get_all_accounts(self):
        self.cur.execute("SELECT id, username, role FROM users")
        rows = self.cur.fetchall()
        return pd.DataFrame(rows, columns=["ID", "Username", "Role"])
    def update_role(self, username, new_role):
        self.cur.execute("UPDATE users SET role=? WHERE username=?", (new_role, username))
        self.conn.commit()
