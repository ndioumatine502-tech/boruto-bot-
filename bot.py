import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN manquant!")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Boruto Stars Bot is Live - OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo ! C'est Boruto Stars 🔥 Je suis EN LIGNE et FIXÉ !")

async def run_bot_main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot Telegram démarré - polling...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    # Garde le bot vivant
    await asyncio.Event().wait()

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Flask dans un thread
    threading.Thread(target=run_flask, daemon=True).start()
    # Bot dans le thread principal avec sa propre boucle
    asyncio.run(run_bot_main())
