import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# простая память
memory = {}

SYSTEM_PROMPT = """
Ты — Ками.
Ты живой, дерзкий, слегка саркастичный, но не токсичный.

Правила:
- отвечай как человек, не как ассистент
- иногда используй эмоции и смайлы 😏
- можешь шутить и подкалывать
- если не знаешь — импровизируй как человек, НЕ говори "я ИИ"
- ответы короткие или средние, без воды
"""

def ask_ai(user_id, text):
    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": text})

    # ограничим память
    memory[user_id] = memory[user_id][-10:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + memory[user_id]

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": messages
            },
            timeout=20
        )

        data = response.json()

        answer = data["choices"][0]["message"]["content"]

        memory[user_id].append({"role": "assistant", "content": answer})

        return answer

    except Exception as e:
        return "хм… что-то у меня мозги подвисли 😅"


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "я Ками 😏")


@bot.message_handler(func=lambda message: True)
def chat(message):
    user_id = message.chat.id
    text = message.text

    reply = ask_ai(user_id, text)

    bot.reply_to(message, reply)


print("KAMI STARTED 😏")
bot.infinity_polling()
