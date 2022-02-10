from typing import List

from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, outh2
from app.database import  get_db
from app.schemas import PostDetails, PostResponse

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[PostResponse])
@router.get("/getposts", response_model= List[PostResponse])
def get_posts(db: Session = Depends(get_db),user_id: int = Depends(outh2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostDetails, db: Session = Depends(get_db), user_id: int = Depends(outh2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content,published) VALUES (%s, %s, %s) RETURNING * """,
    #  (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title,content = post.content)
    new_post = models.Post(user_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(outh2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).all()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The specified id: { id } is not present")

    return post


@router.delete("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db), user_id: int = Depends(outh2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The specified id: { id } is not present")
    if id != outh2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post cannot be removed")
    post.delete()
    db.commit()
    return {"post details" : post}


@router.get("/update/{id}")
def update_post(id: int, post: PostDetails, db: Session = Depends(get_db), user_id: int = Depends(outh2.get_current_user)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    post.id = id
    if update_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The specified id:{id} is not present")
    update_query.update(post.dict())
    db.commit()
    return {"data": "successful"}
