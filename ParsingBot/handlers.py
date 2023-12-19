from telegram import Update
from telegram.ext import CallbackContext
from googletrans import Translator
from typing import Literal
from utils import save_to_csv

# Define a function to translate text using googletrans
def translate_text(text: str, dest=Literal['en', 'uk']) -> str:
    try:
        translator = Translator()
        return translator.translate(text, dest=dest).text
    except:
        return text

# Define a function to handle the messages that the bot receives
def message_handler(update: Update, context: CallbackContext) -> None:
    # Get the message from the update
    message = update.message

    # Get the chat id
    chat_id = message.chat.id

    # Get the sender and the send time
    sender = message.from_user.username
    send_time = message.date

    # Check if the message is a reply to another message
    reply_to = ""
    if message.reply_to_message:
        reply_to = message.reply_to_message.from_user.username

    # Save the message, sender, send time, and reply_to to a CSV file named after the chat id
    data = [[message.text, sender, send_time, reply_to]]
    save_to_csv(data, f'{chat_id}.csv')

def chats(update: Update, context: CallbackContext) -> None:
    # Get the user id of the user who sent the private message
    user_id = update.effective_user.id

    # Initialize an empty list to store the chat ids
    chat_ids = []

    # Iterate over all chats that the bot is in
    for chat in context.bot.get_chats():
        # Check if the user is in the chat
        if context.bot.get_chat_member(chat.id, user_id).status != 'left':
            # If the user is in the chat, add the chat id to the list
            chat_ids.append(chat.id)

    # Send the list of chat ids to the user
    context.bot.send_message(chat_id=user_id, text=f"You are in these chats: {chat_ids}")