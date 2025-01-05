from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False)


def get_session():
    with Session() as session:
        yield session
