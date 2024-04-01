from telegram import Update

from db.models import Deck
from db.session import session
from db.unique_deck_name import unique_deck_name

async def rename_command(update: Update, _):
  '''Usage: /rename <old_name> <new_name> - Rename a deck'''

  if not update.message:
    return
  
  text = update.message.text

  if not text:
    return
  
  commands = text.split(' ')

  if len(commands) != 3:
    await update.message.reply_text('Usage: /rename <old_name> <new_name>')
    return
  
  old_name = commands[1]
  new_name = commands[2]

  if not old_name:
    await update.message.reply_text('Please provide the old name of the deck!')

  if not new_name:
    await update.message.reply_text('Please provide the new name for the deck!')

  session.query(
    Deck
  ).filter(
    Deck.name == old_name
  ).update(
    {'name': unique_deck_name(new_name)}
  )

  session.commit()

  await update.message.reply_text(f'Renamed deck from {old_name} to {new_name}')
