import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional


class UserPostRequest(BaseModel):

    id: int
    username: str
    email: str
    first_name: str


class UserPostResponse(BaseModel):
    id: int
    username: str
    email: str


def exception_422_null_body():
    raise HTTPException(
        status_code=422,
        detail="You forgot to add request body"
    )

def exception_404_not_found():
    raise HTTPException(
        status_code=404,
        detail="There is no user with this ID"
    )


app = FastAPI()


##########################################################
# How to create DABABASE using sqlalchemy?               #
##########################################################
# TODO
# Refer -
# https://docs.sqlalchemy.org/en/20/core/metadata.html#creating-and-dropping-database-tables

models.Base.metadata.create_all(bind=engine)


def create_sample_user():
    user_model = models.Users()
    user_model.id = 1
    user_model.username = "prashant"
    user_model.email = "prashant@gmail.com"
    user_model.first_name = "prash"
    db = get_db()
    session = Session()
    session.add(user_model)
    session.commit()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# create_sample_user()


@app.get("/")
def read_all(db: Session = Depends(get_db)):
    """
    from models.films import Film
    Film.objects.all()

    Args:
        db:

    Returns:

    """
    return db.query(models.Users).all()


@app.post("/", status_code=201, response_model=UserPostResponse)
def create_user(user_data: Optional[UserPostRequest] = None, db: Session = Depends(get_db)):

    if user_data is None:
        exception_422_null_body()

    user_model = models.Users()
    user_model.id = user_data.id
    user_model.username = user_data.username
    user_model.email = user_data.email
    user_model.first_name = user_data.first_name
    db.add(user_model)
    db.commit()
    response = UserPostResponse(
        id=user_model.id,
        username=user_model.username,
        email=user_model.email)

    return response


@app.put("/{user_id}")
def update_user(
        user_id: int,
        user_data: Optional[UserPostRequest] = None,
        db: Session = Depends(get_db)
):
    if user_data is None:
        exception_422_null_body()

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        exception_404_not_found()

    user.username = user_data.username
    user.email = user_data.email
    user.first_name = user_data.first_name

    db.add(user)
    db.commit()
    response = UserPostResponse(
        id=user_data.id,
        username=user_data.username,
        email=user_data.email
    )

    return response


@app.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        exception_404_not_found()

    db.query(models.Users).filter(models.Users.id == user_id).delete()

    db.commit()

    return {
        "message": f"user - {user.id} deleted successfully"
    }
