from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌸 Xush kelibsan, gulim...\n\n"
        "Bu mendan senga kichik sovg‘a ❤️"
    )

    keyboard = [
        [InlineKeyboardButton("💖 START", callback_data="start_story")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= STORY =================
async def story1(update, context):
    q = update.callback_query
    await q.answer()

    text = (
        "💌 Hayotim...\n\n"
        "Bu botni sen uchun yaratdim ❤️\n"
        "Buni bilishni hohlisanmi🙃\n"
    )

    keyboard = [
        [InlineKeyboardButton("❤️ Ha", callback_data="yes")],
        [InlineKeyboardButton("💔 Yo‘q", callback_data="no")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="home")]
    ]

    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= YES =================
async def yes(update, context):
    q = update.callback_query
    await q.answer()

    text = "💖 Jonim... sen mendan hafa emasmisan?"

    keyboard = [
        [InlineKeyboardButton("😊 Ha yoq hafa emasman", callback_data="happy")],
        [InlineKeyboardButton("😔 Xa Xafaman", callback_data="sad")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="start_story")]
    ]

    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= NO =================
async def no(update, context):
    q = update.callback_query
    await q.answer()

    text = (
        "🌸 Nimadur bo‘ldi gulim?\n"
        "Kimdir hafa qildimi?"
    )

    keyboard = [
        [InlineKeyboardButton("😔 Ha hafa qilishdi", callback_data="hurt")],
        [InlineKeyboardButton("🙂 Yo‘q hammasi joyida", callback_data="ok")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="start_story")]
    ]

    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= CONTINUE =================
async def continue_flow(update, context):
    q = update.callback_query
    await q.answer()

    context.user_data["q"] = 0
    await show_question(q, context)


# ================= 10 SAVOL =================
questions = [
    "1️⃣ Men seni baxtli qilyapmanmi?",
    "2️⃣ Meni kechira olasanmi?",
    "3️⃣ Men haqimda fikring qanday?",
    "4️⃣ Meni sog‘inasanmi?",
    "5️⃣ Men sen uchun kimman?",
    "6️⃣ Eng yoqimli xotiramiz qaysi?",
    "7️⃣ Menga ishonasanmi?",
    "8️⃣ Men seni tushunamanmi?",
    "9️⃣ Meni yo‘qotishni xohlaysanmi?",
    "🔟 Oxirgi savol: meni sevishing rostmi?"
]


# ================= SHOW QUESTION =================
async def show_question(q, context):
    i = context.user_data["q"]

    if i >= len(questions):
        await q.edit_message_text(
            "💖 Rahmat Jonim...\n\nSeni juda qadrlayman ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Home", callback_data="home")]
            ])
        )
        return

    keyboard = [
        [InlineKeyboardButton("❤️ Javob beraman", callback_data="next_q")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="ok")]
    ]

    await q.edit_message_text(
        questions[i],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================= NEXT QUESTION =================
async def next_question(update, context):
    q = update.callback_query
    await q.answer()

    context.user_data["q"] += 1
    await show_question(q, context)


# ================= OTHER =================
async def happy(update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("🌸 Rahmat ❤️ Men seni qadrlayman...")

async def sad(update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("💔 Uzr... seni xafa qilmoqchi emasdim...")

async def hurt(update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("💌 Menga yoz: @oybekortiqvoyevv ❤️")

async def ok(update, context):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton("💖 Boshlash", callback_data="continue")]
    ]

    await q.edit_message_text(
        "🌸 Unda yaxshi ❤️ Davom etamizmi?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data

    if data == "start_story":
        await story1(update, context)

    elif data == "yes":
        await yes(update, context)

    elif data == "no":
        await no(update, context)

    elif data == "happy":
        await happy(update, context)

    elif data == "sad":
        await sad(update, context)

    elif data == "hurt":
        await hurt(update, context)

    elif data == "ok":
        await ok(update, context)

    elif data == "continue":
        await continue_flow(update, context)

    elif data == "next_q":
        await next_question(update, context)

    elif data == "home":
        await start(update.callback_query.message, context)


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))

app.run_polling()
