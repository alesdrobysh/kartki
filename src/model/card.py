from pydantic import BaseModel

class Card(BaseModel):
  deck_name: str # partition key
  question: str # sort key
  answer: str