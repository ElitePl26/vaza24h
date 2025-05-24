import os
import mercadopago
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# === TOKENS VIA VARIÁVEIS DE AMBIENTE ===
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
MP_TOKEN = os.getenv('MP_TOKEN')

# === CONFIG MERCADOPAGO ===
sdk = mercadopago.SDK(MP_TOKEN)

def start(update: Update, context: CallbackContext):
    texto = """
🔥🌶️ *GARANTA AGORA SEU ACESSO AO GRUPO VIP MAIS INSANO DO BRASIL!* 🔥

📦 Receba conteúdos exclusivos e atualizados 24H.
💥 Seja um membro VIP e aproveite as promoções enquanto durarem!

Clique abaixo para escolher seu plano e se deliciar com conteúdo 🔥🌶️
"""
    keyboard = [
        [InlineKeyboardButton("VIP 1 ANO ( + Vendido ) – R$ 69,99", callback_data='vip_1ano')],
        [InlineKeyboardButton("VIP 3 MESES 40%OFF – R$ 34,99", callback_data='vip_3meses')],
        [InlineKeyboardButton("VIP MENSAL 30%OFF – R$ 22,99", callback_data='vip_mensal')],
        [InlineKeyboardButton("VIP SEMANAL 25%OFF – R$ 12,99", callback_data='vip_semanal')],
        [InlineKeyboardButton("VIP VITALÍCIO ( PROMOÇÃO ) ⭕ – R$ 99,99", callback_data='vip_vitalicio')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(texto, parse_mode='Markdown', reply_markup=reply_markup)

def gerar_pagamento(valor, descricao):
    preference_data = {
        "items": [
            {
                "title": descricao,
                "quantity": 1,
                "unit_price": float(valor)
            }
        ]
    }
    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]["init_point"]

def liberar_acesso_falso(chat_id, context):
    context.bot.send_message(
        chat_id=chat_id,
        text="""
✅ *Pagamento confirmado!*

Sua assinatura foi validada com sucesso.

🔥 Clique no botão abaixo para acessar seu conteúdo VIP:
👉 [ENTRAR AGORA](https://t.me/teugrupovip)

📞 Suporte: @teucontatofake
""",
        parse_mode='Markdown'
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    planos = {
        'vip_1ano': (69.99, "Plano VIP 1 Ano"),
        'vip_3meses': (34.99, "Plano VIP 3 Meses"),
        'vip_mensal': (22.99, "Plano VIP Mensal"),
        'vip_semanal': (12.99, "Plano VIP Semanal"),
        'vip_vitalicio': (99.99, "Plano VIP Vitalício"),
    }

    if query.data in planos:
        valor, descricao = planos[query.data]
        link = gerar_pagamento(valor, descricao)

        query.edit_message_text(
            text=f"""
✅ Clique no link abaixo para efetuar o pagamento do *{descricao}*:

👉 [Pagar com MercadoPago]({link})

⚠️ Após o pagamento, aguarde até 10 minutos para liberação automática.

📤 Ou envie seu comprovante aqui no chat para agilizar.
""", parse_mode='Markdown'
        )

        # Liberação fake real após 10 minutos
        chat_id = query.message.chat.id
        threading.Timer(600, liberar_acesso_falso, args=(chat_id, context)).start()

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    print("BOT MEGA VAZA + ONLINE NO RENDER ✅")
    updater.idle()

if __name__ == '__main__':
    main()
