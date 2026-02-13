import os

# توجه: اسم این متغیر محیطی باید دقیقا همون باشه که تو Render گذاشتی
TOKEN = os.getenv("BOT_TOKEN")  
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
MERCHANT_ID = os.getenv("MERCHANT_ID", "")
BASE_URL = os.getenv("BASE_URL", "")
