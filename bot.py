import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

TOKEN = os.environ.get("BOT_TOKEN")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Je suis en ligne 🔥 Ton Boruto Bot marche !")

def run_flask():
    flask_app.run(host='0.0.0.0', port=10000)

def main():
    if not TOKEN:
        print("ERREUR: BOT_TOKEN manquant")
        return
    print("Demarrage du bot Telegram...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    main()
