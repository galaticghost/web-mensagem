from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///teste.db", echo=True)

SessionLocal = sessionmaker(bind=engine)
def get_session():
    with SessionLocal() as session:
        yield session
