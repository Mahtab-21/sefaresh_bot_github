from telegram.ext import Updater, CommandHandler
from config import TOKEN

def start(update, context):
    update.message.reply_text("ربات فعاله ✅")

def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN not set!")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("Bot is starting...")
    updater.start_polling()
    updater.idle()
