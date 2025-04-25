import os
import time
import random
import threading
import logging
import schedule
from datetime import datetime
import pytz
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

# تنظیمات
TOKEN = os.getenv("TELEGRAM_TOKEN") or "7873616946:AAHfvkE9t2YKDG214JwHFSN00dDmeFBtn40"
USER_IDS = [7485583903, 5371611029]  # اضافه کردن آیدی جدید به لیست
TEHRAN = pytz.timezone("Asia/Tehran")

# پیام‌ها
morning_messages = [
    "☀️ صبحت بخیر عشقم! امروزت پر از موفقیت باشه 💪❤️",
    "🌟 یه روز فوق‌العاده در انتظارتِ — بدرخشی قشنگم! ✨😘",
    "🌞 صبح یعنی دوباره با فکر تو بیدار شم 💭💖",
    "📈 آرزوی موفقیت برات دارم، می‌دونم عالی‌ای! 😍🔥",
    "🌼 صبحت بخیر ملکه قلبم 👑❤️، روزت پُر از اتفاقای خوب باشه!",
    "💖 بلند شو بدرخشی، دنیا منتظر لبخند قشنگته 😍🌞",
    "🍯 صبحت مثل عسل شیرین باشه عشقم 😘🍀"
]

noon_messages = [
    "🕑 حواسم بهته همیشه، حتی وسط روز! 💘",
    "💌 دوستت دارم، مراقب خودت باش 😇",
    "🌞 وسط روز هم به یادت بودم، مثل همیشه 😍",
    "😊 یه لبخند بزن قشنگم، جات تو قلبمه! ❤️",
    "🍽 اگه الان ناهار خوردی، امیدوارم مزه‌ش مثل عشقم برات شیرین بوده باشه 😋💖",
    "⏳ وقت استراحته، یه دل سیر فکر منم بکن 😌❤️",
    "📸 حتی تو شلوغی روز، یه فکرت لبخند میاره رو لبم 😁💭"
]

night_messages = [
    "🌜 شب بخیر عشقم، قشنگ بخواب 😴❤️",
    "🛌 آروم بخواب، فردا روز قشنگیه بازم برای ما 💑",
    "💤 خوابای خوب ببینی خوشگل من 😘",
    "✨ تا فردا که دوباره عاشقت شم، شبت خوش 💖",
    "🌌 امشبم با فکر تو می‌خوابم، توی رویاها هم با همیم 😍🌠",
    "🌙 شب آرومی داشته باشی فرشته‌ی من 😇💤",
    "📖 قصه‌ی عاشقانه‌مون هر شب تو ذهنم ادامه داره، شبت قشنگ عشقم 🥰📚"
]


bot = Bot(token=TOKEN)

def send_message(text):
    try:
        bot.send_message(chat_id=USER_IDS[0], text=text)  # پیام به آیدی اول ارسال می‌شود
        logging.info(f"✅ پیام فرستاده شد: {text}")
    except Exception as e:
        logging.error(f"❌ خطا در ارسال پیام: {e}")

def check_schedule():
    now = datetime.now(TEHRAN).strftime("%H:%M")
    if now == "09:00":
        send_message(random.choice(morning_messages))
    elif now == "16:00":
        send_message(random.choice(noon_messages))
    elif now == "4:04":
        send_message(random.choice(night_messages))

def run_schedule():
    while True:
        check_schedule()
        time.sleep(60)  # هر یک دقیقه چک می‌کنه

# هندلر start
def start(update: Update, context):
    if update.effective_user.id in USER_IDS:
        context.bot.send_message(chat_id=update.effective_user.id, text=" سلام قشنگم! ربات فعاله و برات پیام می‌فرسته ❤️ و ساخته شده با عشق برای عشقم 😍")
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text="این ربات خصوصی‌ه عزیز! 🔐")

def main():
    logging.basicConfig(level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    threading.Thread(target=run_schedule, daemon=True).start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
