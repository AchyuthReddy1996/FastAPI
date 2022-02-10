from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database import get_db
from .. import utilities, outh2, models


router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    #print(user_credentials.username,user_credentials.password)
    user = db.query(models.User).filter(user_credentials.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"{user_credentials.username} not found")
    if not utilities.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Credentials not valid")
    access_token = outh2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}



