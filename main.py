from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from config import TOKEN
from handlers import *
import threading
import server

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PRODUCT: [MessageHandler(Filters.text & ~Filters.command, get_product)],
            COLOR: [CallbackQueryHandler(get_color)],
            QTY: [MessageHandler(Filters.text & ~Filters.command, get_qty)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, get_phone)],
            ADDRESS: [MessageHandler(Filters.text & ~Filters.command, get_address)],
            POSTAL: [MessageHandler(Filters.text & ~Filters.command, get_postal)],
            CONFIRM: [CallbackQueryHandler(confirm)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv)

    # Run Flask server in a separate thread
    t = threading.Thread(target=server.run)
    t.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
