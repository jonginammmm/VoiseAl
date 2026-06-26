from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8644445513:AAGMhCkbVh9o0YJH0rg6-gVDkW3M84zr8rc"
ADMIN_ID = 6394219796

# ==========================
# USER DATA
# ==========================

def reset_user(context):
    context.user_data["scene"] = "intro"
    context.user_data["question"] = 0
    context.user_data["waiting_text"] = False


# ==========================
# SAVOLLAR
# ==========================

QUESTIONS = [
    {
        "text": "1️⃣ Men seni baxtli qilyapmanmi?",
        "type": "choice",
        "answers": ["❤️ Ha", "💖 Men sen bilan baxtliman", "🥺 Ba'zan"],
    },
    {
        "text": "2️⃣ Meni sog'inasanmi?",
        "type": "choice",
        "answers": ["❤️ Har doim", "🥰 Juda ko'p", "🥺 Ba'zan"],
    },
    {
        "text": "3️⃣ Men sen uchun kimman? ❤️",
        "type": "text",
    },
    {
        "text": "4️⃣ Menga ishonasanmi?",
        "type": "choice",
        "answers": ["❤️ To'liq ishonaman", "🌹 Ishonaman", "🤔 Bilmayman"],
    },
    {
        "text": "5️⃣ Men bilan bog'liq eng yaxshi xotirang qaysi?",
        "type": "text",
    },
    {
        "text": "6️⃣ Agar hozir yoningda bo'lsam nima qilarding?",
        "type": "choice",
        "answers": ["🤗 Quchoqlardim", "❤️ Yonimda qol derdim", "🥰 Gaplashardim"],
    },
    {
        "text": "7️⃣ Meni bir so'z bilan tarifla ❤️",
        "type": "text",
    },
    {
        "text": "8️⃣ Meni tanlaganingdan afsusdasanmi?",
        "type": "choice",
        "answers": ["❤️ Hech qachon", "🥺 Ba'zan", "💔 Ha"],
    },
    {
        "text": "9️⃣ Meni rostan sevasanmi?",
        "type": "choice",
        "answers": [
            "❤️ Juda ham sevaman",
            "💖 Seni yaxshi ko'raman",
            "🥰 So'z bilan aytib bo'lmaydi",
        ],
    },
    {
        "text": "🔟 Menga aytolmagan bir gaping bormi?",
        "type": "text",
    },
]

# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_user(context)

    text = """
🌙

Ba'zi insonlar hayotimizga shunchaki kirib kelmaydi...

Ular qalbimizdan joy oladi...
Ular tabassumimiz sababiga aylanadi...
Ular har bir kunimizni chiroyli qiladi...

❤️

"Seni uchratgan kunim,
hayotimning eng go'zal sahifasi boshlandi..."

🌹

Mukammal bo'lmasligim mumkin...

Lekin seni chin yurakdan qadrlayman...

Bugun seni kichkina sayohatga taklif qilaman...

Bu oddiy bot emas...

Bu yuragimdagi ayta olmagan gaplar... ❤️

💌 Oybekdan Jayronaga
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🌹 Sayohatni boshlash",
                callback_data="story1",
            )
        ]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    # ==========================
# STORY 1
# ==========================

async def story1(query):
    text = """
💌 Hayotim...

Bugun seni shu yerga bekorga chaqirmadim...

Ichimda uzoq vaqtdan beri ayta olmagan gaplarim bor...

Har safar seni o'ylaganimda yuzimda tabassum paydo bo'ladi...

Sen buni bilarmiding? ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Davomini o'qish",
                callback_data="story2",
            )
        ],
        [
            InlineKeyboardButton(
                "🌙 Keyinroq",
                callback_data="close",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ==========================
# STORY 2
# ==========================

async def story2(query):
    text = """
🌹

Har kuni Xudodan bitta narsa so'rayman...

Tabassuming hech qachon yo'qolmasin...

Ko'zlaringda doim baxt porlasin...

Chunki sen kulsang...

Men ham baxtli bo'laman... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🥺 Davomi",
                callback_data="story3",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Orqaga",
                callback_data="story1",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ==========================
# STORY 3
# ==========================

async def story3(query):
    text = """
🥺

Lekin bitta narsani bilishni juda xohlayman...

Sen mendan hafa emasmisan?

Chunki sening xafalig'ing...

Meni ham xafa qiladi...
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "😊 Hafa emasman",
                callback_data="questions",
            )
        ],
        [
            InlineKeyboardButton(
                "😔 Biroz hafa bo'lganman",
                callback_data="sad",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Orqaga",
                callback_data="story2",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ==========================
# SAD STORY
# ==========================

async def sad_story(query):
    text = """
😔

Agar seni xafa qilgan bo'lsam...

Meni kechir...

Bu hech qachon ataylab bo'lmagan...

Sening tabassuming men uchun hamma narsadan qimmat... ❤️

Iltimos...

Yana kulgin...
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Seni kechirdim",
                callback_data="questions",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Orqaga",
                callback_data="story3",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    # ==========================
# SHOW QUESTION
# ==========================

async def show_question(query, context):
    index = context.user_data["question"]

    if index >= len(QUESTIONS):
        await final_scene(query, context)
        return

    question = QUESTIONS[index]

    # Matnli savol
    if question["type"] == "text":
        context.user_data["waiting_text"] = True

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 Orqaga",
                    callback_data="back_question"
                )
            ]
        ]

        await query.edit_message_text(
            f"{question['text']}\n\n✍️ Javobni yozib yuboring...",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Tugmali savol
    else:
        keyboard = []

        for answer in question["answers"]:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        answer,
                        callback_data=f"answer_{answer}"
                    )
                ]
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "🔙 Orqaga",
                    callback_data="back_question"
                )
            ]
        )

        await query.edit_message_text(
            question["text"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# ==========================
# NEXT QUESTION
# ==========================

async def next_question(query, context):
    context.user_data["question"] += 1
    await show_question(query, context)


# ==========================
# INLINE JAVOB
# ==========================

async def answer_question(query, context):
    user = query.from_user

    answer = query.data.replace("answer_", "")

    index = context.user_data["question"]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
❤️ Yangi javob

👤 {user.first_name}
🆔 {user.id}

📌 Savol:
{QUESTIONS[index]["text"]}

✅ Javob:
{answer}
""",
    )

    await next_question(query, context)
    # ==========================
# HANDLE TEXT
# ==========================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_text"):
        return

    user = update.effective_user
    answer = update.message.text

    index = context.user_data["question"]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
💌 TEXT JAVOB

👤 {user.first_name}
🆔 {user.id}

📌 Savol:
{QUESTIONS[index]["text"]}

✍️ Javob:
{answer}
"""
    )

    context.user_data["waiting_text"] = False
    context.user_data["question"] += 1

    if context.user_data["question"] >= len(QUESTIONS):
        await update.message.reply_text(
            """
🎉 Rahmat...

Barcha savollarga javob berding. ❤️

Yana bitta kichkina sovg'am bor...
"""
        )
        await final_message(update, context)
        return

    q = QUESTIONS[context.user_data["question"]]

    if q["type"] == "choice":
        keyboard = []

        for ans in q["answers"]:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        ans,
                        callback_data=f"answer_{ans}"
                    )
                ]
            )

        await update.message.reply_text(
            q["text"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:
        context.user_data["waiting_text"] = True

        await update.message.reply_text(
            f"{q['text']}\n\n✍️ Javobni yozing..."
        )


# ==========================
# FINAL MESSAGE
# ==========================

async def final_message(update, context):
    keyboard = [
        [
            InlineKeyboardButton(
                "💌 Maxfiy xabar qoldirish",
                callback_data="secret"
            )
        ]
    ]

    text = """
❤️

Shu yerga qadar kelganing uchun rahmat...

Balki bu oddiy botdir...

Lekin undagi har bir so'z yuragimdan yozildi...

Seni qadrlayman...

Seni hurmat qilaman...

Va eng muhimi...

❤️ Seni yaxshi ko'raman...

🌹 Oybek
"""

    if hasattr(update, "message") and update.message:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ==========================
# CALLBACK HANDLER
# ==========================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "story1":
        await story1(query)

    elif data == "story2":
        await story2(query)

    elif data == "story3":
        await story3(query)

    elif data == "sad":
        await sad_story(query)

    elif data == "questions":
        context.user_data["question"] = 0
        await show_question(query, context)

    elif data.startswith("answer_"):
        await answer_question(query, context)

    elif data == "secret":
        context.user_data["waiting_text"] = True

        await query.edit_message_text(
            """
💌

Menga aytolmagan barcha gaplaringni yoz...

Bu xabar faqat Oybekga yuboriladi. ❤️
"""
        )
        # ==========================
# MAIN
# ==========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Buyruqlar
    app.add_handler(CommandHandler("start", start))

    # Tugmalar
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Matnli javoblar
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    print("❤️ Romantic Bot ishga tushdi...")

    app.run_polling()


# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    main()
