from bot.main import init_bot
from db.init_schema import init_schema

if __name__ == '__main__':
  init_schema()
  init_bot()
