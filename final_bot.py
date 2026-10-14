import os, requests, nest_asyncio
nest_asyncio.apply()
from collections import deque
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8910612419:AAGITX-LWrPIqwVKtvFvCvxOENnn1cAohy8")
prices = deque(maxlen=50)

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT", timeout=5)
        return float(r.json()['price'])
    except:
        return 1.08

for i in range(20):
    prices.append(get_price())

def get_ma(d,p):
    if len(d)<p: return None
    return sum(list(d)[-p:])/p

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb=[[InlineKeyboardButton("30 SEC",callback_data="30s"),InlineKeyboardButton("1 MIN",callback_data="1m")],[InlineKeyboardButton("2 MIN",callback_data="2m"),InlineKeyboardButton("5 MIN",callback_data="5m")]]
    await update.message.reply_text("Pocket Signal LIVE - Choose timer:",reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); p=get_price(); prices.append(p)
    fast=get_ma(prices,5); slow=get_ma(prices,20)
    sig="WAIT" if fast is None else "BUY UP - UP" if fast>slow else "SELL DOWN - DOWN"
    label={"30s":"30 Sec","1m":"1 Min","2m":"2 Min","5m":"5 Min"}[q.data]
    await q.edit_message_text(f"{sig}\nTimer: {label}\nPrice: {round(p,5)}\nGo Pocket Option NOW - {label}")

def main():
    print("Bot starting..."); app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start)); app.add_handler(CallbackQueryHandler(btn))
    app.run_polling()

main()
