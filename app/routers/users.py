from typing import List

from app import models, schemas, utils
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email == user.email)
    if user_exist.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User already exist"
        )
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get a user
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )

    return user


# Get all users
@router.get("", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
