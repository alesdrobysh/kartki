from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config import config
from bot.import_command import import_command
from bot.list_command import list_command
from bot.rename_command import rename_command
from bot.match_command import match_command

def init_bot():
  print('Starting...')

  if not config.TOKEN:
    raise ValueError('No token provided')

  app = Application.builder().token(config.TOKEN).build()

  app.add_handler(CommandHandler('import', import_command))
  app.add_handler(CommandHandler('list', list_command))
  app.add_handler(CommandHandler('rename', rename_command))
  app.add_handler(CommandHandler('match', match_command))

  print('Polling...')
  app.run_polling(poll_interval = 3)
