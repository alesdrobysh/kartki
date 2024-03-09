from  db.models import Card, Deck
from db.database import session
from bot.main import init as bot_init

if __name__ == '__main__':
  deck = Deck(name='Default')
  session.add(deck)

  card = Card(question='What is the capital of Poland?', answer='Warsaw', deck_id=deck.id)
  session.add(card)

  session.commit()
