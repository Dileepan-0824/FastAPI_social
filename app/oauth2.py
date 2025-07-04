import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, models, utils
from .database import get_db
from typing import Optional
from .config import settings
#secret key
#algorithm used
#expiration time


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #oauth2_scheme is the scheme for the oauth2 authentication and url is the url of the login endpoint

SECRET_KEY = settings.secret_key #secret key for the jwt token
ALGORITHM = settings.algorithm #algorithm used for the jwt token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes #expiration time for the jwt token

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,  # pass datetime object
        "iat": now      # pass datetime object
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(encoded_jwt, bytes):
        encoded_jwt = encoded_jwt.decode('utf-8')
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        from datetime import datetime
        print("[DEBUG] SECRET_KEY:", SECRET_KEY)
        print("[DEBUG] ALGORITHM:", ALGORITHM)
        print("[DEBUG] Current UTC timestamp:", int(datetime.utcnow().timestamp()))
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded JWT payload:", payload)  # Debug print
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except ExpiredSignatureError as e:
        print("ExpiredSignatureError:", e)
        raise credentials_exception
    except InvalidTokenError as e:
        print("InvalidTokenError:", e)
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    print("Querying user with id:", token_data.id)  # Debug print
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        print("No user found with id:", token_data.id)  # Debug print
        raise credentials_exception
    return user
