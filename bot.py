from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        send_message(chat_id, f"Ками: {text} 😏")

    if "business_message" in data:
        chat_id = data["business_message"]["chat"]["id"]
        text = data["business_message"].get("text", "")

        send_message(chat_id, f"Бизнес-Ками: {text} 🔥")

    return "ok"
