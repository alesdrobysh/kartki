from typing import List
from boto3.dynamodb.conditions import Key

from db.dynamodb_repository import DynamoDbRepository
from model.card import Card
from config import config

class CardsDynamoDbRepository(DynamoDbRepository):
  def __init__(self):
    super().__init__()
    self.table = self.dynamodb.Table(config.CARDS_TABLE_NAME)

  def insert_card(self, card: Card):
    self.table.put_item(Item=card.model_dump())

  def insert_cards(self, cards: List[Card]):
    with self.table.batch_writer() as batch:
      for card in cards:
        batch.put_item(Item=card.model_dump())
  
  def replace_card(self, card: Card, newCard: Card):
    self.delete_card(card)
    self.insert_card(newCard)

  def delete_card(self, card: Card):
    self.table.delete_item(Key={
      "deck_name": card.deck_name,
      "question": card.question
    })

  def has_deck(self, deck_name):
    return self.list_decks().count(deck_name) > 0
  
  def list_decks(self) -> List[str]:
    response = self.table.scan()
    return list(set([card["deck_name"] for card in response["Items"]]))
  
  def list_cards_in_deck(self, deck_name):
    response = self.table.query(
      KeyConditionExpression=Key("deck_name").eq(deck_name)
    )
    
    return [Card(**card) for card in response["Items"]]

  def rename_deck(self, old_name, new_name):
    cards = self.list_cards_in_deck(old_name)
    for card in cards:
      newCard = Card(deck_name=new_name, question=card.question, answer=card.answer)
      self.replace_card(card, newCard)

  def delete_deck(self, deck_name):
    cards = self.list_cards_in_deck(deck_name)
    for card in cards:
      self.delete_card(card)

  def get_unique_deck_name(self, deck_name, counter=0) -> str:
    if self.has_deck(deck_name):
      counter += 1
      return self.get_unique_deck_name(f"{deck_name} ({counter})", counter)
    
    return deck_name
