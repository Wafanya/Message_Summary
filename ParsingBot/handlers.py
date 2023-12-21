from telegram import Update
from telegram.ext import CallbackContext
from utils import save_to_csv
import csv
from preprocessor import preprocess_csv
from summarizer import summarize_text


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
    chat_id = update.effective_chat.id

    # Also add the chat id to the CSV file
    with open('BotIsIn.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        if str(chat_id) not in [row[0] for row in reader]:
            # If the chat id is not in the file, add it
            with open('BotIsIn.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([chat_id])

def chats(update: Update, context: CallbackContext) -> None:
    # Get the user id of the user who sent the private message
    user_id = update.effective_user.id

    # Initialize an empty list to store the chat names
    user_chats = []

    # Initialize an empty set to store the chat ids
    chat_ids = set()

    # Load chat ids from the CSV file
    with open('BotIsIn.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            chat_ids.add(int(row[0]))

    # Iterate over all chats that the bot has seen
    for chat_id in chat_ids:
        # Check if the user is in the chat
        chat_member = context.bot.get_chat_member(chat_id, user_id)
        if chat_member.status != 'left':
            # If the user is in the chat, add the chat title and id to the list
            chat = context.bot.get_chat(chat_id)
            if chat.title is not None:  # Only add the chat if the title is not None
                user_chats.append(f"{chat.title} - /summarize {chat_id}")

    # Format the list of chats into a string
    user_chats_str = "\n".join(user_chats)

    # Send the list of chat names and ids to the user
    context.bot.send_message(chat_id=user_id, text=f"Available chats:\n{user_chats_str}")

def summarize(update: Update, context: CallbackContext) -> None:
    # Get the chat id from the command arguments
    chat_id = int(context.args[0])

    # Construct the path to the CSV file
    csv_path = f"/{chat_id}.csv"

    # Preprocess the CSV file
    text = preprocess_csv(csv_path)

    # Summarize the text
    summary = summarize_text(text)

    # Send the summary to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=summary)
