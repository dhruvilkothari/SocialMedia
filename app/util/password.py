from pwdlib import PasswordHash

# Initialize the hasher with Argon2
password_hasher = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    """Hashes a plain-text password."""
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a stored hash."""
    return password_hasher.verify(plain_password, hashed_password)