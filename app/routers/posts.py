import shutil
from typing import List, Optional
from fastapi import (
    Depends,
    Form,
    HTTPException,
    Response,
    status,
    APIRouter,
    File,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db


router = APIRouter(prefix="/post", tags=["Post"])

# Get all post
@router.get("", response_model=List[schemas.PostVoteRespone])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )

    if len(post) == 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return post


# Create Post
@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRespone
)
def create_post(
    contents: schemas.Post = Depends(),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    imgUrl = ""
    if image is not None:
        with open(f"media/{image.filename}", "wb") as media:
            shutil.copyfileobj(image.file, media)
        print(image.filename)
        imgUrl += f"{image.filename}"

    print(contents.title)
    new_post = models.Post(
        user_id=current_user.id, image=imgUrl.strip(), **contents.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.post("/upload")
def upload_image(image: UploadFile = File(...)):
    with open(f"media/{image.filename}", "wb") as media:
        shutil.copyfileobj(image.file, media)
    print(image.filename)


@router.get("/uploads/{filename}")
def upload_image(
    filename: str,
    db: Session = Depends(get_db),
):
    # with open(f"media/{image.filename}", "wb") as media:
    #     shutil.copyfileobj(image.file, media)
    # print(image.filename)
    # print(name.content)
    pic = db.query(models.Post).filter(models.Post.image == filename).first()

    if not pic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    # return {"v": name.dict(), "image": image.filename}
    return FileResponse(f"media/{pic.image}")


# Get post by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostRespone)
def get_post_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    get_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not get_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return get_post


# Update post
@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostRespone
)
def update_post_by_id(
    id: str,
    updated_post: schemas.Post,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    if str(post.first().user_id) == str(current_user.id):

        post.update(updated_post.dict(), synchronize_session=False)
        db.commit()
        return post.first()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail=f"You can't touch this"
    )


# Delete Post by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    del_post = db.query(models.Post).filter(models.Post.id == id)

    if not del_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    pid = del_post.first().user_id
    if str(pid) == str(current_user.id):

        del_post.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail=f"You can't touch this"
    )
