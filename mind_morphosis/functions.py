from . import bcrypt

def HashPassword(pwd: str) -> str:
    hashed_pwd = bcrypt.generate_password_hash(pwd).decode(encoding="utf-8")
    return hashed_pwd

def CheckHashPassword(hash_pwd: bytes, pwd: str) -> bool:
    return bcrypt.check_password_hash(hash_pwd, bytes(pwd, "utf-8"))