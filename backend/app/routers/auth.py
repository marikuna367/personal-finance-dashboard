from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from .. import models, schemas, db, core

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=schemas.UserRead)
def signup(user_in: schemas.UserCreate):
    with Session(db.engine) as session:
        statement = select(models.User).where(models.User.email == user_in.email)
        result = session.exec(statement).first()
        if result:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = models.User(email=user_in.email, hashed_password=core.hash_password(user_in.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate):
    with Session(db.engine) as session:
        statement = select(models.User).where(models.User.email == form_data.email)
        user = session.exec(statement).first()
        if not user or not core.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = core.create_access_token(user.email)
        return {"access_token": token, "token_type": "bearer"}
