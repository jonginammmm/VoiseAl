from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
CallbackQueryHandler,
MessageHandler,
ContextTypes,
filters
)

TOKEN = "8644445513:AAHecI2alqhP8KPtcMP5opqVs5zbmGXps5E"
ADMIN_ID = 6394219796

# ======================

# USER DATA

# ======================

def reset_user(context):
    context.user_data["scene"] = "intro"
    context.user_data["question"] = 0
    context.user_data["waiting_text"] = False

# ======================

# SAVOLLAR

# ======================

QUESTIONS = [
{
"text": "1️⃣ Men seni baxtli qilyapmanmi?",
"type": "choice",
"answers": ["❤️ Ha", "💖 Men sen bilan baxtliman", "🥺 Ba'zan"]
},
{
"text": "2️⃣ Meni sog‘inasanmi?",
"type": "choice",
"answers": ["❤️ Har doim", "🥰 Juda ko‘p", "🥺 Ba'zan"]
},
{
"text": "3️⃣ Men sen uchun kimman?",
"type": "text"
},
{
"text": "4️⃣ Menga ishonasanmi?",
"type": "choice",
"answers": ["❤️ To‘liq ishonaman", "🌹 Ishonaman", "🤔 Bilmayman"]
},
{
"text": "5️⃣ Men bilan bog‘liq eng yaxshi xotirang qaysi?",
"type": "text"
}
]

# ======================

# START

# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_user(context)

    text = """
🌙 Ba'zi insonlar hayotimizga shunchaki kirib kelmaydi...

Ular qalbimizdan joy oladi.
Ular kunimizning eng yaxshi qismiga aylanadi.
Ular tabassumimizning sababiga aylanadi...

🌹 Balki men mukammal emasdirman...

Lekin seni sevaman ❤️

💌 Oybekdan Jayronaga
"""


keyboard = [
    [
        InlineKeyboardButton(
            "🌹 Sirni ochish",
            callback_data="open_story"
        )
    ]
]

await update.message.reply_text(
    text,
    reply_markup=InlineKeyboardMarkup(keyboard)
)

# ======================

# STORY 1

# ======================

async def story1(query):

text = """

💌 Hayotim...

Bu botni sen uchun yaratdim ❤️

Bugun seni hafa qilgan bo‘lsam uzr...

Senga bir nechta gaplar yozdim...

Ularni bilishni xohlaysanmi?
"""

keyboard = [
    [
        InlineKeyboardButton(
            "❤️ Ha, albatta",
            callback_data="want_yes"
        )
    ],
    [
        InlineKeyboardButton(
            "🥺 Hozir uncha emas",
            callback_data="want_no"
        )
    ],
    [
        InlineKeyboardButton(
            "🔙 Orqaga",
            callback_data="back_intro"
        )
    ]
]

await query.edit_message_text(
    text,
    reply_markup=InlineKeyboardMarkup(keyboard)
)

# ======================

# STORY 2

# ======================

async def story2(query):

text = """

💖 Jonim...

Men uchun bitta narsani bilish juda muhim...

Sen mendan hafa emasmisan? 🌸
"""

keyboard = [
    [
        InlineKeyboardButton(
            "😊 Hafa emasman",
            callback_data="not_angry"
        )
    ],
    [
        InlineKeyboardButton(
            "😔 Biroz hafa bo‘lganman",
            callback_data="angry"
        )
    ],
    [
        InlineKeyboardButton(
            "🔙 Orqaga",
            callback_data="back_story1"
        )
    ]
]

await query.edit_message_text(
    text,
    reply_markup=InlineKeyboardMarkup(keyboard)
)

# ======================

# STORY 3

# ======================

async def story3(query):

text = """

😔 Jonim...

Seni kim hafa qildi?

Nima bo‘ldi o‘zi?

Dardingni aytishga tayyormisan?
"""

keyboard = [
    [
        InlineKeyboardButton(
            "❤️ Ha, aytaman",
            callback_data="tell_problem"
        )
    ],
    [
        InlineKeyboardButton(
            "🥺 Hozir emas",
            callback_data="skip_problem"
        )
    ],
    [
        InlineKeyboardButton(
            "🔙 Orqaga",
            callback_data="back_story2"
        )
    ]
]

await query.edit_message_text(
    text,
    reply_markup=InlineKeyboardMarkup(keyboard)
)
