import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Boruto Bot est en ligne 🔥")

def main():
    if not TOKEN:
        print("ERREUR: BOT_TOKEN non trouvé!")
        return
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    # Pour Render - lance Flask en arrière plan
    from threading import Thread
    Thread(target=lambda: app_flask.run(host='0.0.0.0', port=10000)).start()
    main()
