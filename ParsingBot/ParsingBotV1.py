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


from telegram.ext import Updater, MessageHandler, Filters

# Define a function to handle the messages that the bot receives
def message_handler(update, context):
    # Get the message from the update
    message = update.message
    # Get the chat id
    chat_id = message.chat.id
    # Save the message to a text file named after the chat id
    with open(f'{chat_id}.txt', 'a') as f:
        f.write(message.text + '\n')

# Create the Updater and pass it the bot's token
updater = Updater("6444292840:AAEXDFLWdrk7Cha3yQ0yjPG6TpT4mJu13OQ", use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Add a message handler that will be called for any message
dp.add_handler(MessageHandler(Filters.text, message_handler))

# Start the bot
updater.start_polling()
