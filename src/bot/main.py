from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler


async def start_command(update: Update, _):
  await update.message.reply_text('Hello! This is the Kartki Bot!')

async def help_command(update: Update, _):
  await update.message.reply_text('Hello! This is the Kartki Bot!')


if __name__ == '__main__':
  load_dotenv()
  TOKEN = os.getenv('TOKEN')

  print('Starting...')
  app = Application.builder().token(TOKEN).build()

  app.add_handler(CommandHandler('start', start_command))
  app.add_handler(CommandHandler('help', help_command))

  print('Polling...')
  app.run_polling(poll_interval = 3)
