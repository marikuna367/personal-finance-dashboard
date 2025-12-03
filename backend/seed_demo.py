# 

from sqlmodel import Session, select
from app.db import engine, SQLModel
from app.models import User
from passlib.context import CryptContext

# Create tables if they don't exist
SQLModel.metadata.create_all(engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Open session
with Session(engine) as session:
    # Check if demo user exists using SQLModel query
    statement = select(User).where(User.email == "demo@gmail.com")
    existing_user = session.exec(statement).first()

    if existing_user:
        print("Demo user already exists.")
    else:
        demo = User(
            email="demo@gmail.com",
            hashed_password=get_password_hash("password")
        )
        session.add(demo)
        session.commit()
        print("Demo user added successfully.")
