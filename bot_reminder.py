from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8780196053:AAHNfoh8ftmcgyrFb8-5xOupL6gs7Qa0tZk"

akun = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Reminder Akun\n\n"
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

    for a in akun:
        text += f"{a[0]} - {a[1]}\n"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", listakun))

app.run_polling()
