from jose import jwt
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
from config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(identity) -> str:
    to_encode = identity.copy()
    expire = datetime.now(UTC) + timedelta(minutes=300)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.encode_algorithm)
    return encoded_jwt

def get_hashed_password(password):
    return password_context.hash(password)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

