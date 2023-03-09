import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends


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


create_sample_user()


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

