import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schema import ItemSchema, UserSchema

from fastapi import FastAPI, Depends

model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/user")
def get_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return {"users": users}


@app.get("/user/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter_by(id=id).first()
    return {"data": user}


@app.post("/create/user")
def create_user(db: Session = Depends(get_db), user: UserSchema = None):
    if user is None:
        return {"message": "Please give user data"}
    user_found = model.User(email=user.email)
    db.add(user_found)
    db.commit()
    return {"id": user_found.id}


@app.put("/update/user/{id}")
def update_user(id: int, db: Session = Depends(get_db), user: UserSchema = None):
    user_found = db.get(model.User, id)
    if user_found is None:
        return {"message": "User not found!"}
    if user is None:
        return {"message": "Please give user data"}
    user_found.email = user.email
    db.commit()
    return {"data": {
        "id": user_found.id,
        "email": user.email
    }}


@app.delete("/delete/user/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.get(model.User, id)
    if user is None:
        return {"message": "User not found!"}
    db.delete(user)
    db.commit()
    return {"data": "Deleted User"}


@app.delete("/delete/user")
def delete_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    for user in users:
        db.delete(user)
        db.commit()
    return {"msg": "All users deleted"}
