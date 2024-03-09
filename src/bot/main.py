from telegram import Update
from telegram.ext import Application, CommandHandler

from config import config

async def start_command(update: Update, _):
  await update.message.reply_text('Hello! This is the Kartki Bot!')

async def help_command(update: Update, _):
  await update.message.reply_text('Hello! This is the Kartki Bot!')


def init():
  print('Starting...')
  app = Application.builder().token(config.TOKEN).build()

  app.add_handler(CommandHandler('start', start_command))
  app.add_handler(CommandHandler('help', help_command))

  print('Polling...')
  app.run_polling(poll_interval = 3)
