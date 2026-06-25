from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"

# ================= CINEMATIC START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    text = (
        "✨ SYSTEM LOADING...\n"
        "❤️ romantic module ochilmoqda...\n"
        "🌸 xotiralar yuklanmoqda...\n\n"
        "💌 Xush kelibsan, gulim...\n"
        "Bu oddiy bot emas...\n"
        "Bu — sen uchun yozilgan kichik dunyo ❤️"
    )

    keyboard = [
        [InlineKeyboardButton("💖 KIRISH", callback_data="home")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ================= HOME DASHBOARD =================
def home_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 Hikoya", callback_data="story"),
         InlineKeyboardButton("🎯 Test", callback_data="test")],

        [InlineKeyboardButton("💬 Xabarlar", callback_data="msg"),
         InlineKeyboardButton("🌸 Kayfiyat", callback_data="mood")],

        [InlineKeyboardButton("💖 Final", callback_data="final"),
         InlineKeyboardButton("💔 Kechirim", callback_data="sorry")]
    ])

# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # HOME
    if data == "home":
        await q.edit_message_text(
            "🏠 MAIN MENU\nTanla 👇",
            reply_markup=home_menu()
        )

    # STORY
    elif data == "story":
        context.user_data["chapter"] = 0
        await story(q, context)

    # TEST
    elif data == "test":
        context.user_data["q"] = 0
        await test(q, context)

    # MSG
    elif data == "msg":
        await q.edit_message_text(
            "💬 Sen mening eng chiroyli tasodifimsan ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yana", callback_data="msg")],
                [InlineKeyboardButton("🏠 Menu", callback_data="home")]
            ])
        )

    # MOOD
    elif data == "mood":
        await q.edit_message_text(
            "🌸 Kayfiyat tanla:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("😊 Baxtli", callback_data="home")],
                [InlineKeyboardButton("😔 Hafa", callback_data="sorry")],
                [InlineKeyboardButton("💖 Sevgi", callback_data="home")]
            ])
        )

    # FINAL
    elif data == "final":
        await q.edit_message_text(
            "💖 SEN MENING BAHTIMSAN ❤️\n\n"
            "Men seni har doim qadrlayman...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Menu", callback_data="home")]
            ])
        )

    # SORRY
    elif data == "sorry":
        await q.edit_message_text(
            "💔 Agar seni xafa qilgan bo‘lsam uzr...\n"
            "Men seni juda qadrlayman ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Menu", callback_data="home")]
            ])
        )

# ================= STORY SYSTEM =================
story_pages = [
    "💌 Chapter 1:\nMen seni ko‘rgan kunim hammasi o‘zgardi...",
    "🌸 Chapter 2:\nHar kuni seni o‘ylayman...",
    "💖 Chapter 3:\nSen mening eng katta hissiyotimsan..."
]

async def story(q, context):
    i = context.user_data["chapter"]

    if i >= len(story_pages):
        await q.edit_message_text(
            "💖 Hikoya tugadi...\nEndi davom etamizmi?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 Test", callback_data="test")],
                [InlineKeyboardButton("🏠 Menu", callback_data="home")]
            ])
        )
        return

    keyboard = [
        [InlineKeyboardButton("➡️ Keyingi", callback_data="next_story")],
        [InlineKeyboardButton("🏠 Menu", callback_data="home")]
    ]

    await q.edit_message_text(story_pages[i], reply_markup=InlineKeyboardMarkup(keyboard))

    context.user_data["chapter"] += 1

# ================= STORY NEXT =================
async def router_extra(update, context):
    q = update.callback_query
    data = q.data

    if data == "next_story":
        await story(q, context)

# ================= TEST SYSTEM =================
questions = [
    "💖 Men seni baxtli qilyapmanmi?",
    "🌸 Meni kechira olasanmi?",
    "💌 Men haqimda fikring?",
    "💖 Meni sog‘inasanmi?",
    "🌸 Men sen uchun kimman?",
    "💌 Menga ishonasanmi?",
    "💖 Meni tushunasanmi?",
    "🌸 Meni yo‘qotishni xohlaysanmi?",
    "💌 Eng yaxshi xotira?",
    "💖 Meni sevishing rostmi?"
]

async def test(q, context):
    i = context.user_data["q"]

    if i >= len(questions):
        await q.edit_message_text(
            "💖 TEST TUGADI ❤️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Menu", callback_data="home")]
            ])
        )
        return

    await q.edit_message_text(
        questions[i],
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❤️ Javob beraman", callback_data="next_test")],
            [InlineKeyboardButton("🏠 Menu", callback_data="home")]
        ])
    )

async def router_test(update, context):
    q = update.callback_query
    data = q.data

    if data == "next_test":
        context.user_data["q"] += 1
        await test(q, context)

# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
app.add_handler(CallbackQueryHandler(router_extra))
app.add_handler(CallbackQueryHandler(router_test))

app.run_polling()
