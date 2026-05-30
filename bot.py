from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8647681598:AAGOHneNveSUdvWsc5wII_ymbtYBlBVFYPw"

notes = {}

keyboard = ReplyKeyboardMarkup(
    [["📝 Додати нотатку", "📋 Показати нотатки"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я твій бот-помічник.",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    if user_id not in notes:
        notes[user_id] = []

    if text == "📝 Додати нотатку":
        await update.message.reply_text("Напиши свою нотатку:")
        context.user_data["adding_note"] = True

    elif text == "📋 Показати нотатки":
        user_notes = notes.get(user_id, [])
        if not user_notes:
            await update.message.reply_text("Нотаток немає")
        else:
            await update.message.reply_text("\n".join(user_notes))

    elif context.user_data.get("adding_note"):
        notes[user_id].append(text)
        context.user_data["adding_note"] = False
        await update.message.reply_text("Збережено!")

    else:
        await update.message.reply_text("Використовуй кнопки")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()