import os
import mercadopago
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MP_TOKEN = os.getenv("MP_TOKEN")

# SDK MercadoPago
sdk = mercadopago.SDK(MP_TOKEN)

user_payment_pending = {}

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("💳 Gerar QR Code para PIX", callback_data="pagar_pix")]]
    update.message.reply_text("🔐 *Bem-vindo ao sistema de acesso VIP!*")

"Clique abaixo para gerar o QR Code de pagamento PIX.", 
 "/opt/render/project/src/main.py"
                              parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

def gerar_preferencia(valor, user_id):
    preference_data = {
        "items": [
            {
                "title": "Acesso VIP Mega Vaza +",
                "quantity": 1,
                "unit_price": float(valor)
            }
        ]
        "notification_url": f"https://seuapp.onrender.com/webhook?user_id={user_id}"
    }
    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]

def pagar_pix(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    preference = gerar_preferencia(14.90, user_id)

    qr_img_base64 = preference["point_of_interaction"]["transaction_data"]["qr_code_base64"]
    qr_data = preference["point_of_interaction"]["transaction_data"]["qr_code"]

    user_payment_pending[str(user_id)] = True

    context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=qr_img_base64,
        caption=f"💳 *Chave PIX gerada com sucesso!*

Escaneie o QR ou copie e cole no seu app:

`{qr_data}`

📤 Após o pagamento, aguarde liberação automática.",
        parse_mode='Markdown'
    )

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(pagar_pix, pattern="pagar_pix"))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
