from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import key


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=key.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key.SECRET_KEY, algorithm=key.ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, key.SECRET_KEY, algorithms=key.ALGORITHM)
        return decoded_token.get("username")
    except JWTError:
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_jwt_token(token)
    if username:
        return username
    else:
        return None