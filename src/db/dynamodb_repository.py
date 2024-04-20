from db.connection import get_db

class DynamoDbRepository():
  def __init__(self):
    self.dynamodb = get_db()