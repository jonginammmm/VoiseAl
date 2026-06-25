romantic_bot.py

from telegram import (
Update,
InlineKeyboardButton,
InlineKeyboardMarkup
)

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

# ======================
# USER DATA
# ======================

def reset_user(context):
context.user_data["scene"] = "intro"
context.user_data["question"] = 0
context.user_data["waiting_text"] = False

======================

SAVOLLAR

======================

QUESTIONS = [

{
"text":"1️⃣ Men seni baxtli qilyapmanmi?",
"type":"choice",
"answers":[
"❤️ Ha",
"💖 Men sen bilan baxtliman",
"🥺 Ba'zan"
]
},

{
"text":"2️⃣ Meni sog‘inasanmi?",
"type":"choice",
"answers":[
"❤️ Har doim",
"🥰 Juda ko‘p",
"🥺 Ba'zan"
]
},

{
"text":"3️⃣ Men sen uchun kimman?",
"type":"text"
},

{
"text":"4️⃣ Menga ishonasanmi?",
"type":"choice",
"answers":[
"❤️ To‘liq ishonaman",
"🌹 Ishonaman",
"🤔 Bilmayman"
]
},

{
"text":"5️⃣ Men bilan bog‘liq eng yaxshi xotirang qaysi?",
"type":"text"
},

{
"text":"6️⃣ Agar hozir yoningda bo‘lsam nima qilarding?",
"type":"choice",
"answers":[
"🤗 Quchoqlardim",
"❤️ Yonimda qol derdim",
"🥰 Gaplashardim"
]
},

{
"text":"7️⃣ Meni bir so‘z bilan tarifla ❤️",
"type":"text"
},

{
"text":"8️⃣ Meni tanlaganingdan afsusdasanmi?",
"type":"choice",
"answers":[
"❤️ Hech qachon",
"🥺 Ba'zan afsuslantirasan",
"💔 Ha"
]
},

{
"text":"9️⃣ Meni rostan sevasanmi?",
"type":"choice",
"answers":[
"❤️ Juda ham sevaman",
"💖 Seni yaxshi ko‘raman",
"🥰 So‘z bilan aytib bo‘lmaydi"
]
},

{
"text":"🔟 Menga aytolmagan bir gaping bormi?",
"type":"text"
}

]

======================

START

======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

reset_user(context)

text = """

🌙 Ba'zi insonlar hayotimizga shunchaki kirib kelmaydi...

Ular qalbimizdan joy oladi.
Ular kunimizning eng yaxshi qismiga aylanadi.
Ular tabassumimizning sababiga aylanadi...

🌹 Balki men mukammal emasdirman...

Lekin seni qadrlayman ❤️

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

======================

STORY 1

======================

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

======================

STORY 2

======================

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

======================

STORY 3

======================

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
)======================

SHOW QUESTION

======================

async def show_question(query, context):

index = context.user_data["question"]

if index >= len(QUESTIONS):
    await final_scene(query, context)
    return

q = QUESTIONS[index]

# TEXT SAVOL
if q["type"] == "text":

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
        f"{q['text']}\n\n✍️ Javobni yozib yuboring...",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# INLINE SAVOL
else:

    buttons = []

    for answer in q["answers"]:
        buttons.append(
            [
                InlineKeyboardButton(
                    answer,
                    callback_data=f"answer_{index}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "🔙 Orqaga",
                callback_data="back_question"
            )
        ]
    )

    await query.edit_message_text(
        q["text"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

======================

NEXT QUESTION

======================

async def next_question(query, context):

context.user_data["question"] += 1

await show_question(
    query,
    context
)

======================

INLINE JAVOB

======================

async def answer_question(query, context):

user = query.from_user

index = context.user_data["question"]

await context.bot.send_message(
    ADMIN_ID,
    f"""

❤️ INLINE JAVOB

👤 {user.first_name}
🆔 {user.id}

📌 Savol:
{QUESTIONS[index]["text"]}

✅ Javob:
{query.data}
"""
)

await query.edit_message_text(
    """

💌 Men javobingni qabul qildim...

Rahmat ❤️
"""
)

context.user_data["question"] += 1

await show_question(
    query,
    context
)

======================

TEXT JAVOB

======================

async def handle_text(update, context):

if not context.user_data.get("waiting_text"):
    return

user = update.effective_user

text = update.message.text

q_index = context.user_data["question"]

await context.bot.send_message(
    ADMIN_ID,
    f"""

💌 TEXT JAVOB

👤 {user.first_name}
🆔 {user.id}

📌 Savol:
{QUESTIONS[q_index]["text"]}

✍️ Javob:
{text}
"""
)

await update.message.reply_text(
    """

❤️ Men javobingni qabul qildim...

Rahmat gulim 🌹
"""
)

context.user_data["waiting_text"] = False

context.user_data["question"] += 1

# Keyingi savol

q = QUESTIONS[context.user_data["question"]]

if q["type"] == "choice":

    buttons = []

    for answer in q["answers"]:

        buttons.append(
            [
                InlineKeyboardButton(
                    answer,
                    callback_data=f"answer_{context.user_data['question']}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "🔙 Orqaga",
                callback_data="back_question"
            )
        ]
    )

    await update.message.reply_text(
        q["text"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

else:

    await update.message.reply_text(
        f"""

{q["text"]}

✍️ Javobni yozib yuboring...
"""
)

    context.user_data["waiting_text"] = True

======================

FINAL SCENE

======================

async def final_scene(query, context):

text = """

🏆 Tabriklayman...

Sen bu kichik sayohatning oxiriga yetding ❤️

🌹 Agar shu yerga qadar yetib kelgan bo‘lsang...

Demak menga biroz vaqtingni ajratding.

Buning uchun rahmat ❤️

💌 Endi esa ichingda menga aytolmagan gaplaring bo‘lsa...

Bemalol yozib qoldir.

Bu xabar faqat Oybekga yetkaziladi ❤️
"""

keyboard = [
    [
        InlineKeyboardButton(
            "💌 Maxfiy xabar qoldirish",
            callback_data="secret_message"
        )
    ]
]

await query.edit_message_text(
    text,
    reply_markup=InlineKeyboardMarkup(keyboard)
)
