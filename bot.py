import os
import telebot
import random
import time

# токен берём из переменных окружения (GitHub/Render норм вариант)
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# "живые" ответы
greetings = [
    "йо 😏",
    "привет",
    "хай",
    "че как",
    "ну здарова"
]

how_are_you = [
    "нормально, но могло быть интереснее",
    "живу, как обычно 😎",
    "всё ок, а ты как?",
    "да норм, не жалуюсь"
]

unknown = [
    "хз что ты имеешь в виду 😏",
    "не понял, но звучит интересно",
    "переформулируй",
    "я завис на этом моменте 🤔"
]

# имитация "печати"
def think():
    time.sleep(random.uniform(1.2, 3.0))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    think()
    bot.send_message(message.chat.id, "йо 😏 я тут, пиши что хочешь")

@bot.message_handler(func=lambda message: True)
def chat(message):
    text = message.text.lower()

    bot.send_chat_action(message.chat.id, 'typing')
    think()

    # реакции
    if "привет" in text:
        bot.send_message(message.chat.id, random.choice(greetings))

    elif "как дела" in text:
        bot.send_message(message.chat.id, random.choice(how_are_you))

    elif "что делаешь" in text:
        bot.send_message(message.chat.id, "с тобой общаюсь вообще-то 😏")

    elif "кто ты" in text:
        bot.send_message(message.chat.id, "я твой чат-бот, но не простой 😎")

    elif "любишь" in text:
        bot.send_message(message.chat.id, "я люблю стабильные ответы и твои сообщения 😏")

    else:
        bot.send_message(message.chat.id, random.choice(unknown))

print("bot started...")

bot.infinity_polling()
