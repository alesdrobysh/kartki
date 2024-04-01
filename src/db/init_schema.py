from db.models import Base
from db.engine import engine

def init_schema():
  Base.metadata.create_all(bind=engine)
  print('Schema initialized')
