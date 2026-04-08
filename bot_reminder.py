import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

akun = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Reminder Aktif\n\n"
        "/add namaakun YYYY-MM-DD\n"
        "/list"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nama = context.args[0]
    tanggal = context.args[1]

    akun.append((nama, tanggal))

    await update.message.reply_text("Akun ditambahkan")

async def listakun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "List akun:\n"

    for nama, tanggal in akun:
        text += f"{nama} - {tanggal}\n"

    await update.message.reply_text(text)

async def cek_expired(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()

    for nama, tanggal in akun:
        exp = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
        if exp - today == datetime.timedelta(days=1):
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"Besok akun {nama} expired!"
            )

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    context.job_queue.run_repeating(
        cek_expired,
        interval=3600,
        first=10,
        chat_id=chat_id
    )

    await update.message.reply_text("Reminder otomatis aktif")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", listakun))
app.add_handler(CommandHandler("reminder", reminder))

app.run_polling()
