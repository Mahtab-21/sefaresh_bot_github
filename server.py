from flask import Flask
import threading
from main import main
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

def start_bot():
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()

# اجرای بات در Thread جدا
start_bot()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)
