from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = 0

    keyboard = [
        [InlineKeyboardButton("💖 Boshlash", callback_data="q1")]
    ]

    await update.message.reply_text(
        "🌸 Xush kelibsan...\nBu bizning maxfiy dunyomiz ❤️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= QUESTIONS DATA =================
questions = [
    ("1️⃣ Men seni baxtli qila olyapmanmi?",
     [("❤️ Ha", "a1"), ("💔 Yo‘q", "a1"), ("💖 Men sen bilan baxtliman", "a1")]),

    ("2️⃣ Meni sog‘inasanmi?",
     [("❤️ Ha", "a2"), ("💔 Yo‘q", "a2")]),

    ("3️⃣ Men sen uchun kimman? (yozib yubor)",
     None),

    ("4️⃣ Men sen uchun kimman?",
     None),

    ("5️⃣ Menga ishonasanmi?",
     [("❤️ Ha ishonaman", "a5"), ("💔 Yo‘q", "a5"), ("🤔 Bilmayman", "a5")]),

    ("6️⃣ Eng yaxshi xotiramiz nima?",
     None),

    ("7️⃣ Men sen uchun kimman?",
     None),

    ("8️⃣ Meni tanlaganingdan afsusdasanmi?",
     [("💔 Ha afsusdaman", "a8"), ("❤️ Yo‘q hech qachon", "a8")]),

    ("9️⃣ Meni rostan sevasanmi?",
     [("❤️ Juda ham sevaman", "a9"), ("💖 Yaxshi ko‘raman", "a9")]),

    ("🔟 Oxirgi savol: Men kimman sen uchun?",
     None),
]

# ================= SHOW QUESTION =================
async def show_question(q, context):
    i = context.user_data["step"]

    if i >= len(questions):
        await final_screen(q)
        return

    question, answers = questions[i]

    if answers:
        keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in answers]
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])

        await q.edit_message_text(question, reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await q.edit_message_text(
            question + "\n\n✍ Javob yozib yuboring...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Orqaga", callback_data="back")]
            ])
        )

# ================= CALLBACK ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # START QUIZ
    if data == "q1":
        context.user_data["step"] = 0
        await show_question(q, context)

    # BACK
    elif data == "back":
        if context.user_data["step"] > 0:
            context.user_data["step"] -= 1
        await show_question(q, context)

    # INLINE ANSWER FLOW
    elif data.startswith("a"):
        await accepted(q, context)

# ================= ACCEPT ANSWER =================
async def accepted(q, context):
    await q.edit_message_text("❤️ Men javobingni qabul qildim...")

    context.user_data["step"] += 1

    # next question
    await show_question(q, context)

# ================= TEXT ANSWER HANDLER =================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step", 0)

    if step >= len(questions):
        return

    question, answers = questions[step]

    # faqat text kerak bo‘ladigan savollar
    if answers is None:
        text = update.message.text

        context.user_data[f"ans_{step}"] = text

        await update.message.reply_text("❤️ Men javobingni qabul qildim...")

        context.user_data["step"] += 1

        # next question trigger
        fake_update = update
        await show_question(fake_update, context)

# ================= FINAL SCREEN =================
async def final_screen(q):
    await q.edit_message_text(
        "💖 HURMATLI JAYRONA ❤️\n\n"
        "Oybek bu botni sizni xursand qilish uchun yaratdi.\n\n"
        "Agar aytmoqchi bo‘lgan gaplaringiz bo‘lsa, shu yerga yozing...\n"
        "Men uni Oybekka yetkazaman 💌"
    )

# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

app.run_polling()
