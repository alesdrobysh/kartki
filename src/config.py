import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  TOKEN = os.getenv('TOKEN')

  AWS_REGION = os.getenv('AWS_REGION')
  AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

  CARDS_TABLE_NAME = os.getenv('CARDS_TABLE_NAME')

config = Config()
