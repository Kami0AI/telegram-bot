import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.lower()

    if "привет" in text:
        bot.send_message(message.chat.id, "Привет 😏")
    elif "кто ты" in text:
        bot.send_message(message.chat.id, "Я бот, который наконец-то работает 😎")
    else:
        bot.send_message(message.chat.id, f"Я понял: {message.text}")

print("BOT STARTED 😏")
bot.infinity_polling()
