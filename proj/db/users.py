from db.database import DB #references database.py
from utils.hashing import hash_password # has password while saving password for added security
class UserDB(DB):
    def register_user(self, username, password, role="patient"): # to register a user
        try:
            self.cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, hash_password(password), role)
            )
            self.conn.commit()
            return True, "Account created!"
        except:
            return False, "Username already exists."

