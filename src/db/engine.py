from sqlalchemy import create_engine

from db.models import Base
from config import config

engine = create_engine(
  url=config.db_url_psycopg,
  echo=True
)
