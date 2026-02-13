# main.py
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os

TOKEN = os.environ.get("TOKEN")  # تو Render Token رو در Environment Variables ست کن

def start(update, context):
    update.message.reply_text("سلام!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
