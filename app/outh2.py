from datetime import datetime
#from typing import Optional
from jose import JWTError, jwt
from pydantic.datetime_parse import timedelta
from . import schemas
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from . import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = config.Settings.secret_key
ALGORITHM = config.Settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.Settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms= [ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id =id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail=f"not valid")
    return verify_access_token(token,credentials_exception)

