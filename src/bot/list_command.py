from telegram import Update

from db.models import Deck, Card
from db.session import session
from db.unique_deck_name import unique_deck_name

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
  decks = session.query(Deck).all()

  if not decks:
    return 'No decks found!'

  decks_list = '\n'.join([str(deck.name) for deck in decks])

  return decks_list

def list_deck(name: str):
  deck = session.query(Deck).filter(Deck.name == name).first()

  if not deck:
    return 'Deck not found!'

  cards = session.query(Card).filter(Card.deck_id == deck.id).all()

  if not cards:
    return 'No cards found!'

  cards_list = '\n'.join([f'{card.question} - {card.answer}' for card in cards])

  return cards_list