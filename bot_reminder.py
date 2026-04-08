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
        exp = datetime.datetime.strptime(tanggal, "%
