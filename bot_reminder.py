import os
import json
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8109114402

DATA_FILE = "accounts.json"
USERS_FILE = "users.json"


def is_admin(user_id):
    return user_id == ADMIN_ID


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)


def log_user(user):

    users = load_users()

    data = {
        "id": user.id,
        "username": user.username,
        "name": user.first_name
    }

    if data not in users:
        users.append(data)
        save_users(users)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    log_user(update.effective_user)

    await update.message.reply_text(
"""Panel Akun Premium

/add layanan email YYYY-MM-DD nomor
/list
/expired
/besok
/stats
/remove email
/reminder
/stop
/users
"""
)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    layanan = context.args[0]
    email = context.args[1]
    tanggal = context.args[2]
    nomor = context.args[3]

    data = load_data()

    data.append({
        "layanan": layanan,
        "email": email,
        "tanggal": tanggal,
        "nomor": nomor
    })

    save_data(data)

    await update.message.reply_text("Akun + customer ditambahkan")


async def listakun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    data = load_data()

    text = "List akun:\n"

    for d in data:
        text += f"{d['layanan']} | {d['email']} | {d['tanggal']} | {d['nomor']}\n"

    await update.message.reply_text(text)


async def expired(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    today = datetime.date.today()
    data = load_data()

    text = "Expired hari ini:\n"

    for d in data:
        exp = datetime.datetime.strptime(d["tanggal"], "%Y-%m-%d").date()

        if exp == today:
            text += f"{d['layanan']} {d['email']} | https://wa.me/{d['nomor']}\n"

    await update.message.reply_text(text)


async def besok(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    today = datetime.date.today()
    data = load_data()

    text = "Expired besok:\n"

    for d in data:
        exp = datetime.datetime.strptime(d["tanggal"], "%Y-%m-%d").date()

        if exp - today == datetime.timedelta(days=1):
            text += f"{d['layanan']} {d['email']} | https://wa.me/{d['nomor']}\n"

    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    data = load_data()

    counts = {}

    for d in data:
        layanan = d["layanan"]
        counts[layanan] = counts.get(layanan, 0) + 1

    text = "Statistik akun:\n"

    for k, v in counts.items():
        text += f"{k}: {v}\n"

    await update.message.reply_text(text)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    email = context.args[0]

    data = load_data()

    data = [d for d in data if d["email"] != email]

    save_data(data)

    await update.message.reply_text("Akun dihapus")


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    users = load_users()

    text = "User yang pernah pakai bot:\n\n"

    for u in users:
        text += f"{u['name']} | @{u['username']} | {u['id']}\n"

    await update.message.reply_text(text)


async def reminder_job(context: ContextTypes.DEFAULT_TYPE):

    today = datetime.date.today()
    data = load_data()

    text = "Reminder besok expired:\n"

    for d in data:
        exp = datetime.datetime.strptime(d["tanggal"], "%Y-%m-%d").date()

        if exp - today == datetime.timedelta(days=1):
            text += f"{d['layanan']} {d['email']} | https://wa.me/{d['nomor']}\n"

    if text != "Reminder besok expired:\n":
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=text
        )


async def start_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    chat_id = update.effective_chat.id

    context.job_queue.run_repeating(
        reminder_job,
        interval=18000,
        first=10,
        chat_id=chat_id,
        name=str(chat_id)
    )

    await update.message.reply_text("Reminder aktif (cek setiap 5 jam)")


async def stop_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Kamu bukan admin")
        return

    jobs = context.job_queue.get_jobs_by_name(str(update.effective_chat.id))

    for job in jobs:
        job.schedule_removal()

    await update.message.reply_text("Reminder dimatikan")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", listakun))
app.add_handler(CommandHandler("expired", expired))
app.add_handler(CommandHandler("besok", besok))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("reminder", start_reminder))
app.add_handler(CommandHandler("stop", stop_reminder))

app.run_polling()
