from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
CallbackQueryHandler,
MessageHandler,
ContextTypes,
filters
)

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"
ADMIN_ID = 6394219796

======================

USER DATA

======================

def reset_user(context):
context.user_data["question"] = 0
context.user_data["waiting_text"] = False

======================

SAVOLLAR

======================

QUESTIONS = [
{
"text": "1️⃣ Men seni baxtli qilyapmanmi?",
"type": "choice",
"answers": [
"❤️ Ha",
"💖 Men sen bilan baxtliman",
"🥺 Ba'zan"
]
},

{
    "text": "2️⃣ Meni sog‘inasanmi?",
    "type": "choice",
    "answers": [
        "❤️ Har doim",
        "🥰 Juda ko‘p",
        "🥺 Ba'zan"
    ]
},

{
    "text": "3️⃣ Men sen uchun kimman?",
    "type": "text"
},

{
    "text": "4️⃣ Menga ishonasanmi?",
    "type": "choice",
    "answers": [
        "❤️ To‘liq ishonaman",
        "🌹 Ishonaman",
        "🤔 Bilmayman"
    ]
},

{
    "text": "5️⃣ Men bilan bog‘liq eng yaxshi xotirang qaysi?",
    "type": "text"
},

{
    "text": "6️⃣ Agar hozir yoningda bo‘lsam nima qilarding?",
    "type": "choice",
    "answers": [
        "🤗 Quchoqlardim",
        "❤️ Yonimda qol derdim",
        "🥰 Gaplashardim"
    ]
},

{
    "text": "7️⃣ Meni bir so‘z bilan tarifla ❤️",
    "type": "text"
},

{
    "text": "8️⃣ Meni tanlaganingdan afsusdasanmi?",
    "type": "choice",
    "answers": [
        "❤️ Hech qachon",
        "🥺 Ba'zan afsuslantirasan",
        "💔 Ha"
    ]
},

{
    "text": "9️⃣ Meni rostan sevasanmi?",
    "type": "choice",
    "answers": [
        "❤️ Juda ham sevaman",
        "💖 Seni yaxshi ko‘raman",
        "🥰 So‘z bilan aytib bo‘lmaydi"
    ]
},

{
    "text": "🔟 Menga aytolmagan bir gaping bormi?",
    "type": "text"
}

]
