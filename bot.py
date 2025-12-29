import telebot
import requests
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# این قسمت برای زنده نگه داشتن ربات است
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# دستورات ربات
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "سلام! ربات فعال است ✅\n\nIP یا دامنه بفرست\nیا /user username")

@bot.message_handler(commands=['user'])
def user(m):
    try:
        u = m.text.split()[1]
        r = f"👤 {u}:\n"
        r += f"📸 instagram.com/{u}\n"
        r += f"💻 github.com/{u}\n"
        r += f"✈️ t.me/{u}"
        bot.reply_to(m, r)
    except:
        bot.reply_to(m, "مثال: /user ali")

@bot.message_handler(func=lambda m: True)
def ip(m):
    try:
        d = requests.get(f"http://ip-api.com/json/{m.text}").json()
        if d['status'] == 'success':
            bot.reply_to(m, f"🌍 {d['country']} - {d['city']}\n🏢 {d['isp']}")
        else:
            bot.reply_to(m, "❌ نامعتبر")
    except:
        pass

print("✅ Bot Started!")
bot.infinity_polling()
