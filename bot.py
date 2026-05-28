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


def history(uid):
    return memory.get(str(uid), [])


def add(uid, role, text):
    uid = str(uid)
    if uid not in memory:
        memory[uid] = []

    memory[uid].append({"role": role, "text": text})
    memory[uid] = memory[uid][-20:]

    save_memory(memory)


# ---------------- AI ---------------- #

def ask_ai(uid, text):
    msgs = [
        {
            "role": "system",
            "content": (
                "Ты Ками. Живой, дерзкий, немного саркастичный, "
                "но умный. Отвечай как человек, иногда подкалывай."
            )
        }
    ]

    for m in history(uid):
        msgs.append({
            "role": "user" if m["role"] == "user" else "assistant",
            "content": m["text"]
        })

    msgs.append({"role": "user", "content": text})

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": msgs
        }
    )

    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Я завис 😏"


# ---------------- NORMAL CHAT ---------------- #

@bot.message_handler(content_types=['text'])
def normal(message):
    uid = message.from_user.id
    text = message.text

    add(uid, "user", text)
    reply = ask_ai(uid, text)
    add(uid, "bot", reply)

    bot.send_message(message.chat.id, reply)


# ---------------- BUSINESS SUPPORT ---------------- #

@bot.business_message_handler(content_types=['text'])
def business(message):
    uid = message.from_user.id
    text = message.text

    add(uid, "user", text)
    reply = ask_ai(uid, text)
    add(uid, "bot", reply)

    bot.send_message(message.chat.id, reply)


@bot.business_connection_handler()
def connected(message):
    print("BUSINESS CONNECTED:", message)


print("KAMI STARTED 😏")
bot.polling(none_stop=True)
