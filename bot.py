import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from parser_yakaboo import get_discounts

<<<<<<< HEAD
# 🔧 Заміни токен і chat_id на свої
TOKEN = "7859780731:AAFKQfcB_rs4aoYsTY0F3l7zWjuTzNCFgLY"
CHAT_ID = "33268705"
=======
# 📥 Завантаження змінних з .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
>>>>>>> f6f1fe1 (🛡️ add .env to .gitignore and load secrets via dotenv)

# 🔧 Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📤 Надсилання повідомлень
async def send_discounts(context: ContextTypes.DEFAULT_TYPE):
    books = get_discounts()

    if not books:
        await context.bot.send_message(chat_id=CHAT_ID, text="📭 Нових знижок не знайдено.")
        return

    # Дробимо повідомлення по 10 книжок
    chunk_size = 10
    for i in range(0, len(books), chunk_size):
        chunk = books[i:i + chunk_size]
        text = ""
        for book in chunk:
            text += (
                f"📘 <b>{book['title']}</b>\n"
                f"💰 <b>{book['price']}</b>\n"
                f"🔗 <a href=\"{book['link']}\">Перейти</a>\n\n"
            )
        await context.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")

# 🟢 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Вітаю! Надсилаю сьогоднішні знижки...")
    await send_discounts(context)

# 🕑 Планувальник
def daily_discount_job(application):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: application.create_task(send_discounts(application.bot)), 'cron', hour=9)
    scheduler.start()
    logger.info("Щоденна розсилка знижок запланована на 09:00.")

# 🚀 Запуск бота
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    daily_discount_job(application)
    logger.info("Бот запущено...")
    application.run_polling()
