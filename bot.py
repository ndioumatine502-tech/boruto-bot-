import os
import logging
from flask import Flask
from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters
import threading

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - Boruto Bot Running 🔥"

# Packs : (nom, quantité, prix en Stars)
PACKS = {
    "pack10": {"title": "Pack 10 Boruto", "amount": 10, "price": 25},
    "pack50": {"title": "Pack 50 Boruto", "amount": 50, "price": 100},
    "packvip": {"title": "Pack VIP", "amount": 250, "price": 250},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🔥 Bienvenue chez Boruto Stars Bot 🔥\nChoisis ton pack :"
    # Tu avais des boutons custom, on utilise /buy pour l'instant
    await update.message.reply_text(text + "\n\nEnvoie /buy pour voir les packs.")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton("⭐ Pack 10 Boruto - 25 ⭐", callback_data="pack10")],
        [InlineKeyboardButton("⭐ Pack 50 Boruto - 100 ⭐", callback_data="pack50")],
        [InlineKeyboardButton("⭐ Pack VIP - 250 ⭐", callback_data="packvip")],
    ]
    # On gère aussi via CallbackQuery
    await update.message.reply_text("Stars Boruto\nAchat de stars", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pack = PACKS.get(query.data)
    if not pack:
        return
    # Créer la facture Stars
    prices = [LabeledPrice(pack["title"], pack["price"])]
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=pack["title"],
        description=f"Achat de {pack['amount']} stars Boruto",
        payload=query.data,
        provider_token="",  # Vide pour Telegram Stars
        currency="XTR",
        prices=prices,
    )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload = update.message.successful_payment.invoice_payload
    pack = PACKS.get(payload)
    await update.message.reply_text(f"✅ Paiement reçu ! Tu as reçu {pack['amount']} Boruto Stars ! Merci 🔥")

# Supprime le webhook automatiquement pour éviter Conflict
async def post_init(application):
    await application.bot.delete_webhook(drop_pending_updates=True)
    print("WEBHOOK SUPPRIME - Bot démarré sans conflit")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("Lancement polling...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    main()
