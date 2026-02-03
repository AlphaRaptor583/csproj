import hashlib
def hash_password(password: str) -> str: # SHA256 hash of password is created and stored in database for better security
    return hashlib.sha256(password.encode()).hexdigest()
