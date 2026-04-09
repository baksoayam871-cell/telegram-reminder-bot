import os
import json
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "accounts.json"

def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Panel Akun Premium\n\n"
        "/add layanan email YYYY-MM-DD\n"
        "/list\n"
        "/expired\n"
        "/besok\n"
        "/stats\n"
        "/remove\n"
        "/reminder"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    layanan=context.args[0]
    email=context.args[1]
    tanggal=context.args[2]

    data=load_data()
    data.append({"layanan":layanan,"email":email,"tanggal":tanggal})
    save_data(data)

    await update.message.reply_text("Akun ditambahkan")

async def listakun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data=load_data()

    text="List akun:\n"
    for d in data:
        text+=f"{d['layanan']} | {d['email']} | {d['tanggal']}\n"

    await update.message.reply_text(text)

async def expired(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today=datetime.date.today()
    data=load_data()

    text="Expired hari ini:\n"

    for d in data:
        exp=datetime.datetime.strptime(d["tanggal"],"%Y-%m-%d").date()
        if exp==today:
            text+=f"{d['layanan']} {d['email']}\n"

    await update.message.reply_text(text)

async def besok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today=datetime.date.today()
    data=load_data()

    text="Expired besok:\n"

    for d in data:
        exp=datetime.datetime.strptime(d["tanggal"],"%Y-%m-%d").date()
        if exp-today==datetime.timedelta(days=1):
            text+=f"{d['layanan']} {d['email']}\n"

    await update.message.reply_text(text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data=load_data()

    counts={}
    for d in data:
        layanan=d["layanan"]
        counts[layanan]=counts.get(layanan,0)+1

    text="Statistik akun:\n"
    for k,v in counts.items():
        text+=f"{k}: {v}\n"

    await update.message.reply_text(text)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email=context.args[0]
    data=load_data()

    data=[d for d in data if d["email"]!=email]

    save_data(data)

    await update.message.reply_text("Akun dihapus")

async def reminder(context: ContextTypes.DEFAULT_TYPE):
    today=datetime.date.today()
    data=load_data()

    text="Reminder besok expired:\n"

    for d in data:
        exp=datetime.datetime.strptime(d["tanggal"],"%Y-%m-%d").date()
        if exp-today==datetime.timedelta(days=1):
            text+=f"{d['layanan']} {d['email']}\n"

    if text!="Reminder besok expired:\n":
        await context.bot.send_message(chat_id=context.job.chat_id,text=text)

async def start_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id=update.effective_chat.id

    context.job_queue.run_repeating(
        reminder,
        interval=3600,
        first=10,
        chat_id=chat_id
    )

    await update.message.reply_text("Reminder otomatis aktif")

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("add",add))
app.add_handler(CommandHandler("list",listakun))
app.add_handler(CommandHandler("expired",expired))
app.add_handler(CommandHandler("besok",besok))
app.add_handler(CommandHandler("stats",stats))
app.add_handler(CommandHandler("remove",remove))
app.add_handler(CommandHandler("reminder",start_reminder))

app.run_polling()
