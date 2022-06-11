from multiprocessing import synchronize
from fastapi import Depends, HTTPException, Response, status, APIRouter

from app import models, schemas, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    valid_post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post_exist = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id)
    user = db.query(models.Vote).filter(models.Vote.user_id == current_user.id)
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    find_vote = vote_query.first()
    # Check if post to vote is valid(ie: in the post table).
    if valid_post.first():
        print("got here 1")
        # Check if it exists in the vote table
        if post_exist.first():
            print("got here 2")
            # Check if the like belongs to the current_user
            if user.first():
                print("got here 3")
                # Check if the vote id is 1
                if find_vote:
                    if vote.vote_dir == 1:
                        print("got here 4")
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Already Voted",
                        )
                    else:
                        print("got here 5")
                        vote_query.delete(synchronize_session=False)
                        db.commit()
                        return "Deleted"
            if vote.vote_dir == 0:
                print("got here 6")
                return "You haven't voted"

        # Check if the vote id is 1
        if vote.vote_dir == 1:
            print("got here 7")
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return new_vote
        else:
            print("got here 8")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"You haven't voted"
            )
    print("got here 9")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post you want to vote doesn't exist",
    )
    # if find_vote:
    #     print("got here 1")
    #     if vote.vote_dir == 1:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN, detail="Already Voted"
    #         )

    #     vote_query.delete(synchronize_session=False)
    #     db.commit()
    #     return "Deleted"
    # print("got here")
    # if vote.vote_dir == 1:
    #     print("got here 2")
    #     new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
    #     db.add(new_vote)
    #     db.commit()
    #     db.refresh(new_vote)
    #     return new_vote
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN, detail=f"You haven't voted"
    # )
