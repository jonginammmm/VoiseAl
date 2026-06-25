from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [
        [InlineKeyboardButton("💖 BOSHLASH", callback_data="story")]
    ]

    await update.message.reply_text(
        "🌸 Xush kelibsan gulim...\nBu senga maxsus dunyo ❤️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= STORY =================
async def story(update, context):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton("❤️ Ha davom etamiz", callback_data="quiz_start")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="home")]
    ]

    await q.edit_message_text(
        "💌 Men seni juda qadrlayman...\n10 ta savol boshlaymizmi?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= HOME =================
async def home(q):
    await q.edit_message_text(
        "🏠 MENU",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💖 Hikoya", callback_data="story")]
        ])
    )

# ================= 10 SAVOL + MOS JAVOB =================
questions = [
    ("💖 Men seni baxtli qilyapmanmi?", "❤️ Ha, juda baxtliman sen bilan"),
    ("🌸 Meni kechira olasanmi?", "💔 Albatta, hammasini unutaman"),
    ("💌 Men haqimda fikring?", "😍 Sen juda qadrli odamsan"),
    ("💖 Meni sog‘inasanmi?", "🥺 Ha, har doim sog‘inaman"),
    ("🌸 Men sen uchun kimman?", "❤️ Eng muhim insonimsan"),
    ("💌 Menga ishonasanmi?", "🤍 To‘liq ishonaman"),
    ("💖 Meni tushunasanmi?", "🌸 Ha, har doim tushunishga harakat qilaman"),
    ("🌸 Meni yo‘qotishni xohlaysanmi?", "😔 Yo‘q, hech qachon"),
    ("💌 Eng yaxshi xotira?", "💖 Sen bilan bo‘lgan hamma lahza"),
    ("💖 Meni sevishing rostmi?", "❤️ Ha, juda chin dildan sevaman")
]

# ================= QUIZ START =================
async def quiz_start(update, context):
    q = update.callback_query
    await q.answer()

    context.user_data["q"] = 0
    await show_question(q, context)

# ================= SHOW QUESTION =================
async def show_question(q, context):
    i = context.user_data["q"]

    if i >= len(questions):
        await q.edit_message_text(
            "💖 10 ta savol tugadi...\nSen men uchun juda muhimsan ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 MENU", callback_data="home")]
            ])
        )
        return

    question, _ = questions[i]

    keyboard = [
        [InlineKeyboardButton("💌 Javobni ko‘rish", callback_data="answer")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="story")]
    ]

    await q.edit_message_text(question, reply_markup=InlineKeyboardMarkup(keyboard))

# ================= ANSWER =================
async def show_answer(update, context):
    q = update.callback_query
    await q.answer()

    i = context.user_data["q"]
    _, answer = questions[i]

    context.user_data["q"] += 1

    keyboard = [
        [InlineKeyboardButton("➡️ Keyingi savol", callback_data="next")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="story")]
    ]

    await q.edit_message_text(answer, reply_markup=InlineKeyboardMarkup(keyboard))

# ================= NEXT =================
async def next_q(update, context):
    q = update.callback_query
    await q.answer()
    await show_question(q, context)

# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data

    if data == "story":
        await story(update, context)

    elif data == "quiz_start":
        await quiz_start(update, context)

    elif data == "answer":
        await show_answer(update, context)

    elif data == "next":
        await next_q(update, context)

    elif data == "home":
        await home(q)

# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
app.run_polling()
