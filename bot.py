import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# ===== обычные сообщения =====
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if "привет" in text:
        bot.send_message(message.chat.id, "Привет 😏")
    elif "кто ты" in text:
        bot.send_message(message.chat.id, "Я твой бот-компаньон 😎")
    else:
        bot.send_message(message.chat.id, f"Ты написал: {message.text}")


# ===== webhook endpoint =====
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


# ===== старт сервера =====
@app.route("/")
def home():
    return "Bot is alive 😎"


if __name__ == "__main__":
    bot.remove_webhook()

    url = os.getenv("WEBHOOK_URL")  # например https://xxx.onrender.com
    bot.set_webhook(url=f"{url}/webhook")

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
