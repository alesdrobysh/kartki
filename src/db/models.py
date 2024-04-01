from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Deck(Base):
  __tablename__ = 'decks'

  id = Column(Integer, primary_key=True)
  name = Column(String)

  def __repr__(self):
    return f'<Deck(id={self.id}, name={self.name})>'
  
class Card(Base):
  __tablename__ = 'cards'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  deck_id = Column(Integer, ForeignKey('decks.id'))

  def __repr__(self):
    return f'<Card(id={self.id}, question={self.question}, answer={self.answer}, deck_id={self.deck_id})>'
