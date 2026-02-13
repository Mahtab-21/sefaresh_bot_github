import requests
from config import MERCHANT_ID, BASE_URL
from database import set_authority

# 🌱 SANDBOX URLS
ZP_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"


def create_payment(amount, order_id):

    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "description": f"Order #{order_id}",
        "callback_url": f"{BASE_URL}/verify/{order_id}"
    }

    try:
        response = requests.post(ZP_REQUEST, json=data).json()

        if response["data"]["code"] == 100:
            authority = response["data"]["authority"]

            # ذخیره authority در دیتابیس
            set_authority(order_id, authority)

            return f"{ZP_STARTPAY}{authority}"

        else:
            print("Zarinpal Error:", response)

    except Exception as e:
        print("Payment Exception:", e)

    return None


def verify_payment(order_id, authority, amount):

    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "authority": authority
    }

    try:
        response = requests.post(ZP_VERIFY, json=data).json()

        print("Verify Response:", response)

        return response["data"]["code"] == 100

    except Exception as e:
        print("Verify Exception:", e)
        return False
