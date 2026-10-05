
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "Boruto Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo ! Je suis Boruto Bot")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Tu as dit: {text}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    token = os.environ.get("BOT_TOKEN")
    if not token:
        return
    app_bot = ApplicationBuilder().token(token).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

if __name__ == "__main__":
    main()
