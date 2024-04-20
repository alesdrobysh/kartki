from telegram import Update

from db.cards_dynamodb_repository import CardsDynamoDbRepository

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

  repository = CardsDynamoDbRepository()

  new_name = repository.get_unique_deck_name(new_name)
  repository.rename_deck(old_name, new_name)

  await update.message.reply_text(f'Renamed deck from {old_name} to {new_name}')
