from db.models import Deck
from db.session import session

def unique_deck_name(name: str, counter: int = 0) -> str:
    check_deck = session.query(Deck).filter(Deck.name == name).first()

    if check_deck:
      counter += 1
      new_name = f'{name}_{counter}'
      return unique_deck_name(new_name, counter)
    
    return name