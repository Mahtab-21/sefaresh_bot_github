from telegram import *
from telegram.ext import *
from products import products
from extractor import extract_data
from database import save_order
from payment import create_payment
import uuid

PRODUCT, COLOR, QTY, NAME, PHONE, ADDRESS, POSTAL, CONFIRM = range(8)


async def start(update, context):
    await update.message.reply_text("کد محصول را بفرست:")
    return PRODUCT


async def get_product(update, context):

    code, color = extract_data(update.message.text, products)

    if not code:
        await update.message.reply_text("کد اشتباه است ❌")
        return PRODUCT

    p = products[code]

    context.user_data["product"] = p["name"]
    context.user_data["price"] = int(p["price"].replace(" تومان", ""))

    if color:
        context.user_data["color"] = color
        await update.message.reply_text("تعداد:")
        return QTY

    kb = [[InlineKeyboardButton(c, callback_data=c)]
          for c in p["colors"]]

    await update.message.reply_text(
        "رنگ را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

    return COLOR


async def get_color(update, context):
    q = update.callback_query
    await q.answer()
    context.user_data["color"] = q.data
    await q.edit_message_text("تعداد:")
    return QTY


async def get_qty(update, context):

    if not update.message.text.isdigit():
        await update.message.reply_text("عدد وارد کن")
        return QTY

    context.user_data["qty"] = int(update.message.text)
    await update.message.reply_text("نام:")
    return NAME


async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("تلفن:")
    return PHONE


async def get_phone(update, context):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("آدرس:")
    return ADDRESS


async def get_address(update, context):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("کد پستی:")
    return POSTAL


async def get_postal(update, context):

    context.user_data["postal"] = update.message.text
    d = context.user_data

    total = d["price"] * d["qty"]

    msg = f"""
🛒 سفارش شما:

{d['product']}
رنگ: {d['color']}
تعداد: {d['qty']}
💰 مبلغ: {total} تومان
"""

    kb = [[
        InlineKeyboardButton("پرداخت 💳", callback_data="pay"),
        InlineKeyboardButton("لغو ❌", callback_data="no")
    ]]

    await update.message.reply_text(
        msg,
        reply_markup=InlineKeyboardMarkup(kb)
    )

    return CONFIRM


async def confirm(update, context):

    q = update.callback_query
    await q.answer()

    if q.data == "no":
        await q.edit_message_text("سفارش لغو شد ❌")
        return ConversationHandler.END

    d = context.user_data

    order_id = int(str(uuid.uuid4().int)[:8])
    total = d["price"] * d["qty"]

    save_order({
        "id": order_id,
        "product": d["product"],
        "color": d["color"],
        "qty": d["qty"],
        "name": d["name"],
        "phone": d["phone"],
        "address": d["address"],
        "postal": d["postal"],
        "price": total
    })

    link = create_payment(total, order_id)

    if not link:
        await q.edit_message_text("خطا در ایجاد پرداخت ❌")
        return ConversationHandler.END

    await q.edit_message_text(f"برای پرداخت روی لینک زیر بزن:\n{link}")

    return ConversationHandler.END
