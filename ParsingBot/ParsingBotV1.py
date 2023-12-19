'''
TODO:
make chats function working mama

'''

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from handlers import message_handler, chats

def main():
    # Create the Updater and pass it the bot's token
    updater = Updater("6444292840:AAEXDFLWdrk7Cha3yQ0yjPG6TpT4mJu13OQ", use_context=True)

    # Get the dispatcher from the updater
    dp = updater.dispatcher

    # Add a message handler for text messages
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # Add a command handler for the /chat command
    chats_handler = CommandHandler('chats', chats)
    dp.add_handler(chats_handler)

    # Start the bot
    updater.start_polling()

if __name__ == "__main__":
    main()

