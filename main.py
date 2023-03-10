import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from pydantic import BaseModel


class UserPostRequest(BaseModel):

    id: int
    username: str
    email: str
    first_name: str


class UserPostResponse(BaseModel):
    id: int
    username: str
    email: str


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
    breakpoint()
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


@app.post("/", response_model=UserPostResponse)
def create_user(user_data: UserPostRequest, db: Session = Depends(get_db)):
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
