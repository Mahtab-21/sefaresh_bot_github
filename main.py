from telegram.ext import Updater, CommandHandler
from config import TOKEN
import os


def start(update, context):
    update.message.reply_text("ربات فعاله ✅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
