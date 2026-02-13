from flask import Flask
import threading
import os
from main import main

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

def run_bot():
    main()

# اجرای بات در یک Thread جدا
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

