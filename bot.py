import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
print(f"DEBUG TOKEN exists: {bool(TOKEN)}")
if not TOKEN:
    print("ERREUR: BOT_TOKEN est vide sur Render !")
else:
    print(f"DEBUG TOKEN starts with: {TOKEN[:10]}...")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "OK - Bot is running"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Je marche enfin 🔥")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

def main():
    if not TOKEN:
        print("STOP: Pas de token, polling impossible")
        return
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Lancement du polling avec drop_pending_updates=True...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    main()
