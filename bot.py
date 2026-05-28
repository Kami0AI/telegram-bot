import os
import json
import requests
import telebot

TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TOKEN)

MEMORY_FILE = "memory.json"


# ---------------- MEMORY ---------------- #

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


memory = load_memory()


def get_history(user_id):
    return memory.get(str(user_id), [])


def add_to_history(user_id, role, text):
    uid = str(user_id)

    if uid not in memory:
        memory[uid] = []

    memory[uid].append({"role": role, "text": text})

    # ограничим память
    memory[uid] = memory[uid][-20:]

    save_memory(memory)


# ---------------- AI ---------------- #

def ask_ai(user_id, user_text):
    history = get_history(user_id)

    messages = [
        {
            "role": "system",
            "content": (
                "Ты — Ками. Живой, дерзкий, немного саркастичный, "
                "но умный и полезный собеседник. "
                "Отвечай как человек, не как ассистент. "
                "Иногда подкалывай пользователя, но не будь токсичным."
            )
        }
    ]

    for msg in history:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})

    messages.append({"role": "user", "content": user_text})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": messages
        }
    )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Я завис, не понял вопрос 😏"


# ---------------- HANDLERS ---------------- #

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Я Ками 😏\nГотов общаться. Только не задавай скучные вопросы."
    )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    text = message.text

    add_to_history(user_id, "user", text)

    reply = ask_ai(user_id, text)

    add_to_history(user_id, "assistant", reply)

    bot.send_message(message.chat.id, reply)


# ---------------- BUSINESS SUPPORT (если Telegram даст апдейты) ---------------- #

@bot.business_message_handler(content_types=['text'])
def handle_business(message):
    user_id = message.from_user.id
    text = message.text

    add_to_history(user_id, "user", text)

    reply = ask_ai(user_id, text)

    add_to_history(user_id, "assistant", reply)

    bot.send_message(message.chat.id, reply)


print("KAMI STARTED 😏")
bot.polling(none_stop=True)
