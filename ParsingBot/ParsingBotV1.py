'''
TODO:
Add additional processing of sender and send time
Change save file to .csv type with clolumns = ['message', 'sender', 'time']

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['message', 'sender', 'time'])
        writer.writerows(data)
        
'''


import csv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContextr

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['message', 'sender', 'time'])
        writer.writerows(data)

# Define a function to handle the messages that the bot receives
def message_handler(update: Update, context: CallbackContext) -> None:
    # Get the message from the update
    message = update.message
    # Get the chat id
    chat_id = message.chat.id
    # Get the sender and the send time
    sender = message.from_user.username
    send_time = message.date
    # Save the message, sender, and send time to a CSV file named after the chat id
    data = [[message.text, sender, send_time]]
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



# Create the Updater and pass it the bot's token
updater = Updater("6444292840:AAEXDFLWdrk7Cha3yQ0yjPG6TpT4mJu13OQ", use_context=True)

dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text, message_handler))

# Add a command handler for the /chat command
chats_handler = CommandHandler('chats', chats)
dp.add_handler(chats_handler)

# Start the bot
updater.start_polling()
