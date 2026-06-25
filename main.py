from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"
# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    text = (
        "✨ SYSTEM LOADING...\n"
        "💖 Maxfiy dunyo ochilmoqda...\n\n"
        "🌸 Xush kelibsan gulim ❤️"
    )

    keyboard = [
        [InlineKeyboardButton("💖 Kirish", callback_data="start_story")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= STORY =================
async def story(update, context):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton("❤️ Ha boshlaymiz", callback_data="start_quiz")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="home")]
    ]

    await q.edit_message_text(
        "💌 Men seni juda qadrlayman...\n10 ta savolga o‘tamizmi?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================= QUESTIONS =================
questions = [
    ("1️⃣ Men seni baxtli qilyapmanmi?",
     [("❤️ Ha", "a"), ("💔 Yo‘q", "a"), ("💖 Men baxtliman", "a")]),

    ("2️⃣ Meni sog‘inasanmi?",
     [("❤️ Ha", "a"), ("💔 Yo‘q", "a")]),

    ("3️⃣ Men sen uchun kimman?",
     None),

    ("4️⃣ Menga ishonasanmi?",
     [("❤️ Ha", "a"), ("💔 Yo‘q", "a")]),

    ("5️⃣ Eng yaxshi xotiramiz nima?",
     None),

    ("6️⃣ Meni tushunasanmi?",
     None),

    ("7️⃣ Meni yo‘qotishni xohlaysanmi?",
     [("💔 Ha", "a"), ("❤️ Yo‘q", "a")]),

    ("8️⃣ Meni tanlaganingdan afsusdasanmi?",
     [("💔 Ha", "a"), ("❤️ Yo‘q", "a")]),

    ("9️⃣ Meni rostan sevasanmi?",
     [("❤️ Juda sevaman", "a"), ("💖 Yaxshi ko‘raman", "a")]),

    ("🔟 Men kimman sen uchun?",
     None),
]

# ================= SHOW QUESTION =================
async def show_question(q, context):
    i = context.user_data["step"]

    if i >= len(questions):
        await final_screen(q)
        return

    question, answers = questions[i]

    keyboard = []

    if answers:
        for text, cb in answers:
            keyboard.append([InlineKeyboardButton(text, callback_data=cb)])
    else:
        keyboard.append([InlineKeyboardButton("✍ Javob yozaman", callback_data="write")])

    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])

    await q.edit_message_text(question, reply_markup=InlineKeyboardMarkup(keyboard))


# ================= CALLBACK ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "start_story":
        await story(update, context)

    elif data == "start_quiz":
        context.user_data["step"] = 0
        await show_question(q, context)

    elif data == "back":
        if context.user_data["step"] > 0:
            context.user_data["step"] -= 1
        await show_question(q, context)

    elif data == "a":
        await accept_and_next(q, context)

    elif data == "write":
        await q.edit_message_text("✍ Javobingizni yozing...")

    elif data == "home":
        await start(q.message, context)


# ================= ACCEPT + NEXT (ENG MUHIM FIX) =================
async def accept_and_next(q, context):
    await q.edit_message_text("❤️ Men javobingni qabul qildim...")

    # 👇 MUHIM: pause yo‘q, darhol next
    context.user_data["step"] += 1

    await show_question(q, context)


# ================= TEXT ANSWER =================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step", 0)

    if step >= len(questions):
        return

    question, answers = questions[step]

    if answers is None:
        update.message.text

        await update.message.reply_text("❤️ Men javobingni qabul qildim...")

        context.user_data["step"] += 1

        # ⚡ MUHIM FIX: next question
        await update.message.reply_text("⏳ Keyingi savol yuklanmoqda...")

        # fake callback style
        await show_question(update.message, context)


# ================= FINAL =================
async def final_screen(q):
    await q.edit_message_text(
        "💖 HURMATLI JAYRONA ❤️\n\n"
        "Oybek bu botni sizni xursand qilish uchun yaratdi.\n\n"
        "Agar ichingizda gaplaringiz bo‘lsa yozing...\n"
        "Men uni unga yetkazaman 💌"
    )


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

app.run_polling()
