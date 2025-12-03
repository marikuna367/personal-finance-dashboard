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
    statement = select(User).where(User.email == "demo@example.com")
    existing_user = session.exec(statement).first()

    if existing_user:
        # Update password to demo123 for consistency
        existing_user.hashed_password = get_password_hash("demo123")
        session.add(existing_user)
        session.commit()
        print("Demo user password updated to 'demo123'.")
    else:
        demo = User(
            email="demo@example.com", hashed_password=get_password_hash("demo123")
        )
        session.add(demo)
        session.commit()
        print("Demo user added successfully.")
