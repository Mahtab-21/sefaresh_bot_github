from telegram.ext import *
from config import TOKEN
from handlers import *
import threading
import server


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_product)],
            COLOR: [CallbackQueryHandler(get_color)],
            QTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_qty)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            POSTAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_postal)],
            CONFIRM: [CallbackQueryHandler(confirm)]
        },
        fallbacks=[]
    )

    app.add_handler(conv)

    t = threading.Thread(target=server.run)
    t.start()

    app.run_polling()


if __name__ == "__main__":
    main()
