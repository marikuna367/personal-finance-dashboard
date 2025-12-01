# small script to create a test user and optionally link a mock account
from .db import init_db, engine
from .models import User
from .core import hash_password
from sqlmodel import Session, text

if __name__ == '__main__':
    init_db()
    with Session(engine) as session:
        # using raw SQL for compatibility across SQLModel versions in some environments
        result = session.exec(text("SELECT * FROM user WHERE email='demo@example.com'")).first()
        if not result:
            user = User(email='demo@example.com', hashed_password=hash_password('password'))
            session.add(user)
            session.commit()
            print('Created demo user: demo@example.com / password')
        else:
            print('Demo user already exists')
