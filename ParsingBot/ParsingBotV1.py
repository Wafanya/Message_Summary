'''
TODO:
make chats function working mama
add translation logic
add summarization
        
'''


import csv
import pandas as pd
import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContextr

from langdetect import detect
from googletrans import Translator

# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def translate_text(text, dest='en'):
    try:
        lang = detect(text)
        if lang == 'en':
            return text
        else:
            translator = Translator()
            return translator.translate(text, dest=dest).text
    except:
        return text

# Function to save data to a CSV file
def save_to_csv(data, filename):
    # Load the existing data
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df.loc[len(df)] = data[0]  # Add the new row at the end
    else:
        df = pd.DataFrame(data, columns=['message', 'sender', 'time', 'reply_to'])

    # If there are more than 1000 rows, remove the oldest ones
    if len(df) > 1000:
        df = df.tail(1000)  # Keep only the last 1000 rows

    # Save the data back to the CSV file
    df.to_csv(filename, index=False)

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

def preprocess_csv(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Check if there is reply to message
    df['is_reply_to'] = df['reply_to'].str.strip().str.len() == 0
    
    # Concatenate text by row
    df['ConcatText'] = df.apply(lambda row: row['sender'] + ": " + row['message'] + (" Replied to: " + row['reply_to'] if row['is_reply_to'] else ""), axis=1)
    # Concatenate all text from the column
    concatenated_text = df['ConcatText'].str.cat(sep=' ')
    
    return concatenated_text

def summarize_text(text):
    tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")
    model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")
    summary = pipeline('summarization', model=model, tokenizer=tokenizer)

    return summary(text, max_length=250, min_length=30, do_sample=False)



# Create the Updater and pass it the bot's token
updater = Updater("6444292840:AAEXDFLWdrk7Cha3yQ0yjPG6TpT4mJu13OQ", use_context=True)

dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text, message_handler))

# Add a command handler for the /chat command
chats_handler = CommandHandler('chats', chats)
dp.add_handler(chats_handler)

# Start the bot
updater.start_polling()
