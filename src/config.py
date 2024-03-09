import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  TOKEN = os.getenv('TOKEN')

  DB_HOST = os.getenv('DB_HOST')
  DB_PORT = os.getenv('DB_PORT')
  DB_USER = os.getenv('DB_USER')
  DB_PASS = os.getenv('DB_PASS')
  DB_NAME = os.getenv('DB_NAME')

  @property
  def db_url_psycopg(self):
    return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


config = Config()
