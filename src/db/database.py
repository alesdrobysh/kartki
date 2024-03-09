from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config

engine = create_engine(
  url=config.db_url_psycopg,
  echo=True
)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

