import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN manquant!")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Live - OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Message reçu de {update.effective_user.id}")
    await update.message.reply_text("Yo ! Je suis en ligne 🔥 Ça marche enfin !")

def run_bot():
    print("Démarrage du bot Telegram...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    # Lance le bot en arrière-plan
    threading.Thread(target=run_bot, daemon=True).start()
    # Lance Flask en principal pour Render
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)
