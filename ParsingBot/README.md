# Telegram Message Saver

This script saves incoming messages from a Telegram bot to a text file.

## Description

The script uses the `python-telegram-bot` library to interact with the Telegram API. It defines a message handler function that gets called whenever the bot receives a message. The message, along with its sender and timestamp, is then saved to a text file.

## Installation

You need to install the `python-telegram-bot` library. You can install it with pip:

```bash
pip install python-telegram-bot
```

## Usage

Replace the token in the `Updater` function with your bot's token. Run the script, and it will start listening for incoming messages.
Our current bot is [@multikitestparsing_bot](https://t.me/multikitestparsing_bot)  

## TODO

- Add additional processing of sender and send time.
- Change save file to .csv type with columns = ['message', 'sender', 'time'].
