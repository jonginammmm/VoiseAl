from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = 0

    text = (
        "✨ SYSTEM LOADING...\n"
        "💖 Maxfiy dunyo ochilmoqda...\n\n"
        "🌸 Xush kelibsan gulim ❤️"
    )

    keyboard = [[InlineKeyboardButton("💖 Kirish", callback_data="intro")]]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= INTRO STORY =================
async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "💌 Hayotim...\n\n"
        "Bu botni sen uchun yaratdim ❤️\n"
        "Seni hafa qilgan bo‘lsam uzr...\n\n"
        "Buni bilishni xohlaysanmi?"
    )

    keyboard = [
        [InlineKeyboardButton("❤️ Ha", callback_data="start_yes")],
        [InlineKeyboardButton("💔 Yo‘q", callback_data="start_no")]
    ]

    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= YES / NO =================
async def yes(update, context):
    q = update.callback_query
    await q.answer()

    await q.edit_message_text(
        "💖 Jonim...\nSen mendan hafa emasmisan?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("😊 Yo‘q hafa emasman", callback_data="start_quiz")],
            [InlineKeyboardButton("😔 Ha hafa qilding", callback_data="hurt")]
        ])
    )


async def no(update, context):
    q = update.callback_query
    await q.answer()

    await q.edit_message_text(
        "🌸 Nima bo‘ldi?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("😔 Ha", callback_data="hurt")],
            [InlineKeyboardButton("🙂 Hammasi joyida", callback_data="ok")]
        ])
    )


async def hurt(update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("💌 Agar xafa bo‘lgan bo‘lsang yozib yubor ❤️")


async def ok(update, context):
    q = update.callback_query
    await q.answer()

    await q.edit_message_text(
        "💖 Zo‘r...\nEndi davom etamizmi?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❤️ Ha", callback_data="start_quiz")]
        ])
    )


# ================= 10 SAVOL =================
qa = [
    ("1️⃣ Men seni baxtli qilyapmanmi?", ["❤️ Ha", "💔 Yo‘q", "💖 Baxtliman"]),
    ("2️⃣ Meni sog‘inasanmi?", ["❤️ Ha", "💔 Yo‘q"]),
    ("3️⃣ Men sen uchun kimman?", ["💖 Eng muhim", "❤️ Sevgan"]),
    ("4️⃣ Menga ishonasanmi?", ["❤️ Ha", "💔 Yo‘q"]),
    ("5️⃣ Eng yaxshi xotira?", ["💖 Uchrashuv", "🌸 Har kuni"]),
    ("6️⃣ Meni tushunasanmi?", ["❤️ Ha", "💔 Yo‘q"]),
    ("7️⃣ Meni yo‘qotishni xohlaysanmi?", ["💔 Ha", "❤️ Yo‘q"]),
    ("8️⃣ Afsusdasanmi?", ["💔 Ha", "❤️ Yo‘q"]),
    ("9️⃣ Meni sevasanmi?", ["❤️ Juda", "💖 Yaxshi ko‘raman"]),
    ("🔟 Men kimman sen uchun?", ["💖 Hammasi", "❤️ Hayotim"])
]


# ================= SHOW =================
async def show(q, context):
    i = context.user_data["step"]

    if i >= len(qa):
        await q.edit_message_text(
            "💖 MAXFIY XABAR ❤️\n\n"
            "Oybek bu botni siz uchun yaratdi...\n\n"
            "Agar gaplaringiz bo‘lsa yozing 💌"
        )
        return

    question, answers = qa[i]

    keyboard = [[InlineKeyboardButton(a, callback_data="ans")] for a in answers]
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])

    await q.edit_message_text(question, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "intro":
        await intro(update, context)

    elif data == "start_yes":
        await yes(update, context)

    elif data == "start_no":
        await no(update, context)

    elif data == "start_quiz":
        context.user_data["step"] = 0
        await show(q, context)

    elif data == "ans":
        await accept(q, context)

    elif data == "back":
        if context.user_data["step"] > 0:
            context.user_data["step"] -= 1
        await show(q, context)


# ================= ACCEPT =================
async def accept(q, context):
    await q.edit_message_text("❤️ Men javobingni qabul qildim...")

    context.user_data["step"] += 1

    await show(q, context)


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))

app.run_polling()
