import random
from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CallbackQueryHandler, CommandHandler

from db.cards_dynamodb_repository import CardsDynamoDbRepository
from model.card import Card

async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  '''
  Usage: 
    /match <name> - Launches a match game with the deck. 
                    User will be prompted with a random card front and will need to match it with the correct back.
                    If the user gets it right, they will be prompted with another card and so on until the deck is exhausted.
                    If the user gets it wrong, they will get the correct answer and will be prompted with another card.
  '''

  if not update.message or not context.args:
    return
  
  if len(context.args) != 1:
    await update.message.reply_text('Usage: /match <deck_name>')
    return
  
  repository = CardsDynamoDbRepository()
  
  deck_name = context.args[0]
  # deck = session.query(Deck).filter(Deck.name == deck_name).first()
  if not repository.has_deck(deck_name):
    await update.message.reply_text('Deck not found!')
    return
  
  cards = repository.list_cards_in_deck(deck_name)
  if not cards:
    await update.message.reply_text('Deck is empty!')
    return
  
  match_game = MatchGame(context.application, update.message.chat_id, cards)
  await match_game.start()
  
class MatchGame:
  def __init__(self, application: Application, chat_id: int, cards: List[Card]):
    self.cards = cards
    self.application = application
    self.current_card_index = 0
    self.chat_id = chat_id

    self.button_handler = CallbackQueryHandler(self.button)
    self.cancel_handler = CommandHandler('cancel', self.stop)

    random.shuffle(self.cards)
    

  async def start(self):
    self.application.add_handler(self.button_handler)
    self.application.add_handler(self.cancel_handler)
    
    await self.loop()

  async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    self.application.remove_handler(self.button_handler)
    self.application.remove_handler(self.cancel_handler)

    if update.message:
      await update.message.reply_text('Game stopped!')
      
  async def loop(self):
    card = self.cards[self.current_card_index]
    other_cards = [ c for c in self.cards if c != card ]

    keyboard = [
      InlineKeyboardButton(f'{card.answer}', callback_data=f'{card.answer}'),
      InlineKeyboardButton(f'{other_cards[0].answer}', callback_data=f'{other_cards[0].answer}'),
      InlineKeyboardButton(f'{other_cards[1].answer}', callback_data=f'{other_cards[1].answer}'),
      InlineKeyboardButton(f'{other_cards[2].answer}', callback_data=f'{other_cards[2].answer}')
    ]

    random.shuffle(keyboard)

    reply_markup = InlineKeyboardMarkup([keyboard])

    await self.application.bot.send_message(chat_id=self.chat_id, text=f'{card.question}')
    await self.application.bot.send_message(chat_id=self.chat_id, text='Select the answer:', reply_markup=reply_markup)

  async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    if not query:
      return
    
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    current_card = self.cards[self.current_card_index]

    if query.data != current_card.answer:
      await query.edit_message_text(text=f"Selected option: {query.data}. Correct answer: {current_card.answer}")
    else:
      await query.edit_message_text(text=f"Selected option: {query.data}. Correct!")

    self.current_card_index = self.current_card_index + 1

    if self.current_card_index < len(self.cards):
      await self.loop()
    else:
      await self.application.bot.send_message(chat_id=self.chat_id, text='Game over!')
      self.application.remove_handler(self.button_handler)
      self.application.remove_handler(self.cancel_handler)
