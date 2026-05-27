import os
import telebot
import random
import time
import json

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# -------------------------
# "ПАМЯТЬ" (простая)
# -------------------------
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

memory = load_memory()

# -------------------------
# ХАРАКТЕР БОТА
# -------------------------
moods = ["good", "neutral", "lazy", "sassy"]
bot_mood = random.choice(moods)

def change_mood():
    global bot_mood
    if random.random() < 0.2:
        bot_mood = random.choice(moods)

# -------------------------
# ФРАЗЫ
# -------------------------
greet = ["йо 😏", "привет", "хай", "ну здарова", "че надо"]
sass = ["хмм... сомнительно", "ты серьёзно?", "ладно, допустим", "не уверен что ты прав 😏"]
lazy = ["лень отвечать", "ммм", "ок", "..."]

def think():
    time.sleep(random.uniform(1.2, 3.5))

# -------------------------
# СТАРТ
# -------------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)

    if user_id not in memory:
        memory[user_id] = {"name": None, "messages": 0}

    bot.send_chat_action(message.chat.id, 'typing')
    think()

    bot.send_message(message.chat.id, "йо 😏 я тут. давай общаться")

# -------------------------
# ОСНОВНОЙ ЧАТ
# -------------------------
@bot.message_handler(func=lambda m: True)
def chat(message):
    global memory

    user_id = str(message.chat.id)
    text = message.text.lower()

    if user_id not in memory:
        memory[user_id] = {"name": None, "messages": 0}

    memory[user_id]["messages"] += 1
    save_memory(memory)

    change_mood()

    bot.send_chat_action(message.chat.id, 'typing')
    think()

    # -------------------------
    # ЗАПОМИНАНИЕ ИМЕНИ
    # -------------------------
    if "меня зовут" in text:
        name = text.replace("меня зовут", "").strip()
        memory[user_id]["name"] = name
        save_memory(memory)
        bot.send_message(message.chat.id, f"окей, запомнил: {name} 😏")
        return

    name = memory[user_id]["name"]

    # -------------------------
    # РЕАКЦИИ
    # -------------------------
    if "привет" in text:
        bot.send_message(message.chat.id, random.choice(greet))

    elif "как дела" in text:
        if bot_mood == "good":
            bot.send_message(message.chat.id, "норм, настроение топ 😎")
        elif bot_mood == "lazy":
            bot.send_message(message.chat.id, "ну такое...")
        else:
            bot.send_message(message.chat.id, "живу, как обычно")

    elif "кто я" in text:
        if name:
            bot.send_message(message.chat.id, f"ты {name}, я тебя помню 😏")
        else:
            bot.send_message(message.chat.id, "я пока не знаю тебя")

    elif "что делаешь" in text:
        bot.send_message(message.chat.id, "с тобой общаюсь, очевидно 😏")

    elif "сколько сообщений" in text:
        bot.send_message(message.chat.id, f"ты написал мне {memory[user_id]['messages']} сообщений")

    elif "любишь" in text:
        bot.send_message(message.chat.id, "люблю норм разговоры, не тупые 😏")

    else:
        if bot_mood == "sassy":
            bot.send_message(message.chat.id, random.choice(sass))
        elif bot_mood == "lazy":
            bot.send_message(message.chat.id, random.choice(lazy))
        else:
            bot.send_message(message.chat.id, "я тебя понял 😏")

print("BOT STARTED 😏")

bot.infinity_polling()
