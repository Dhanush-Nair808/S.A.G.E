import bcrypt


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    
    # Correctly truncate by bytes if it exceeds 72 bytes
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        
    salt = bcrypt.gensalt(rounds=12)
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode('utf-8')
    
    # Correctly truncate by bytes if it exceeds 72 bytes
    if len(plain_bytes) > 72:
        plain_bytes = plain_bytes[:72]
        
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)