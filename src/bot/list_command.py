from telegram import Update

from db.cards_dynamodb_repository import CardsDynamoDbRepository

async def list_command(update: Update, _):
  '''
  Usage: 
    /list - List all decks of cards
    /list <name> - List a deck of cards
  '''

  if not update.message:
    return
  
  text = update.message.text

  if not text:
    return
  
  commands = text.split(' ')

  if len(commands) == 1:
    await update.message.reply_text(list_all_decks())
  else :
    await update.message.reply_text(list_deck(commands[1]))

def list_all_decks():
  repository = CardsDynamoDbRepository()
  decks = repository.list_decks()

  if not decks:
    return 'No decks found!'

  decks_list = '\n'.join(decks)

  return decks_list

def list_deck(name: str):
  repository = CardsDynamoDbRepository()

  if not repository.has_deck(name):
    return 'Deck not found!'

  cards = repository.list_cards_in_deck(name)

  if not cards:
    return 'No cards found!'

  cards_list = '\n'.join([f'{card.question} - {card.answer}' for card in cards])

  return cards_list