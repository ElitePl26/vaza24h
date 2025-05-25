import os
from flask import Flask, request
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MP_TOKEN = os.getenv("MP_TOKEN")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and "data" in data and "id" in data["data"]:
        payment_id = data["data"]["id"]

        headers = {
            "Authorization": f"Bearer {MP_TOKEN}"
        }
        r = requests.get(f"https://api.mercadopago.com/v1/payments/{payment_id}", headers=headers)

        if r.status_code == 200:
            payment_info = r.json()
            if payment_info.get("status") == "approved":
                user_id = request.args.get("user_id")
                if user_id:
                    message = "✅ *Pagamento confirmado!*

Clique abaixo para solicitar seu acesso VIP:
👉 @teucontatofake"
                    requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                        json={
                            "chat_id": user_id,
                            "text": message,
                            "parse_mode": "Markdown"
                        }
                    )
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
