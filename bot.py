import os
import telebot
import random
import time
import json
import requests

# =========================================
# ТОКЕНЫ
# =========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# =========================================
# ПАМЯТЬ
# =========================================

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

# =========================================
# НАСТРОЕНИЕ
# =========================================

moods = ["good", "lazy", "playful", "sassy"]
bot_mood = random.choice(moods)

def change_mood():
    global bot_mood

    if random.random() < 0.15:
        bot_mood = random.choice(moods)

# =========================================
# "ЖИВОСТЬ"
# =========================================

def think():
    time.sleep(random.uniform(1.0, 3.5))

def human_unknown():
    phrases = [
        "хз если честно 😏",
        "не шарю в этом",
        "сложный вопрос конечно",
        "я бы сейчас соврал, но не хочу",
        "понятия не имею",
        "интересно звучит кстати",
        "мне лень думать 😎"
    ]

    return random.choice(phrases)

# =========================================
# OPENROUTER AI
# =========================================

def ask_ai(user_id, user_message):

    url = "https://openrouter.ai/api/v1/chat/completions"

    name = memory[user_id].get("name")

    system_prompt = f"""
Ты — Ками.

Ты НЕ должен говорить как ChatGPT или ассистент.

Ты:
- живой
- дерзкий
- иногда ленивый
- иногда смешной
- общаешься как человек
- используешь разговорную речь
- можешь подкалывать
- НЕ отвечаешь слишком официально
- не пишешь огромные сообщения
- иногда говоришь "хз", "ну", "мм"

Информация о пользователе:
Имя: {name}

Настроение:
{bot_mood}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",

        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except:
        return human_unknown()

# =========================================
# START
# =========================================

@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.chat.id)

    if user_id not in memory:
        memory[user_id] = {
            "name": None,
            "messages": 0
        }

    save_memory(memory)

    bot.send_chat_action(message.chat.id, 'typing')
    think()

    start_phrases = [
        "йо 😏 я Ками",
        "ну привет 😎",
        "живой вроде"
    ]

    bot.send_message(
        message.chat.id,
        random.choice(start_phrases)
    )

# =========================================
# ЧАТ
# =========================================

@bot.message_handler(func=lambda m: True)
def chat(message):

    global memory

    user_id = str(message.chat.id)
    text = message.text.lower()

    if user_id not in memory:
        memory[user_id] = {
            "name": None,
            "messages": 0
        }

    memory[user_id]["messages"] += 1

    save_memory(memory)

    change_mood()

    # иногда игнорит 😏
    if random.random() < 0.03:
        return

    # иногда пишет "..."
    if random.random() < 0.05:
        bot.send_message(message.chat.id, "...")

    # typing
    bot.send_chat_action(message.chat.id, 'typing')
    think()

    # память имени
    if "меня зовут" in text:

        name = text.replace("меня зовут", "").strip()

        memory[user_id]["name"] = name

        save_memory(memory)

        bot.send_message(
            message.chat.id,
            f"окей, {name}. запомнил 😏"
        )

        return

    # локальные реакции
    if "как тебя зовут" in text:
        answers = [
            "я Ками 😏",
            "Ками. а что?",
            "можешь звать меня Ками"
        ]

        bot.send_message(message.chat.id, random.choice(answers))
        return

    if "кто я" in text:

        name = memory[user_id]["name"]

        if name:
            bot.send_message(
                message.chat.id,
                f"ты {name}, я помню 😎"
            )
        else:
            bot.send_message(
                message.chat.id,
                "пока не знаю как тебя зовут 😏"
            )

        return

    # ИИ ОТВЕТ
    ai_answer = ask_ai(user_id, text)

    if len(ai_answer) > 400:
        ai_answer = ai_answer[:400]

    bot.send_message(message.chat.id, ai_answer)

print("KAMI STARTED 😏")

bot.infinity_polling()
