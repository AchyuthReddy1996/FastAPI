from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, utilities
from ..database import get_db
from ..schemas import UserCreate, UserResponse

router = APIRouter(
    tags=["users"]
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = utilities.hashing(user.password)
    user.password = hashed_password
    print(user.password)
    print(user.email)
    print("________________________________")
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Email:{user.email} already exists")
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}")
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} not found")
    return user