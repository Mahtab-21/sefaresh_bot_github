import os
from flask import Flask, request
from payment import verify_payment
from database import set_paid, get_order

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Server Running"

@app.route("/verify/<int:order_id>")
def verify(order_id):

    authority = request.args.get("Authority")
    status = request.args.get("Status")

    if status != "OK":
        return "Payment Cancelled ❌"

    order = get_order(order_id)

    if not order:
        return "Order Not Found ❌"

    amount = order[8]

    success = verify_payment(order_id, authority, amount)

    if success:
        set_paid(order_id)
        return "Payment Success ✅"

    return "Verification Failed ❌"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
