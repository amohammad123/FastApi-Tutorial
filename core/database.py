from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    age = Column(Integer)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# alembic revision --autogenerate -m "added age to person table"
# alembic upgrade head
# alembic upgrade <revision>
# alembic downgrade <revision>
