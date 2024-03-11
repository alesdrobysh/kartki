import re
import csv
import requests
from telegram import Update

from db.models import Deck, Card
from db.database import session
from db.unique_deck_name import unique_deck_name

async def import_command(update: Update, _):
  '''Usage: /import <link> <name> - Import a Google Sheet into the database'''

  if not update.message:
    return
  
  text = update.message.text

  if not text:
    return
  
  commands = text.split(' ')

  if len(commands) != 3:
    await update.message.reply_text('Usage: /import <link> <name>')
    return
  
  link = commands[1]
  name = commands[2]

  if not link:
    await update.message.reply_text('Please provide a link to a Google Sheet!')

  if not name:
    await update.message.reply_text('Please provide a name for the deck!')

  rows = get_sheet(link)

  update_db(rows, name)

  await update.message.reply_text(f'Imported {len(rows)} cards from the Google Sheet!')

def convert_google_sheet_url(url):
    return re.sub(r'\/edit#gid=\d+', '/export?format=csv', url)

def get_sheet(link):
    csv_link = convert_google_sheet_url(link)
    response = requests.get(csv_link)
    iterator = response.iter_lines()
    reader = csv.reader([b.decode('utf-8') for b in iterator], delimiter=',')

    return list(reader)

def update_db(rows: list[list[str]], name: str):
    deck = Deck(name=unique_deck_name(name))
    session.add(deck)
    session.flush()

    for row in rows:
      card = Card(question=row[0], answer=row[1], deck_id=deck.id)
      session.add(card)

    session.commit()
