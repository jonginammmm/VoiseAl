from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===================================
# СОЗЛАМАЛАР
# ===================================

TOKEN = "8644445513:AAHM19rmhUwTZgK4T8vKhpWbrqnebasT2Vc"
ADMIN_ID = 6394219796

# ===================================
# USER DATA
# ===================================

def reset_user(context):
    context.user_data.clear()

    context.user_data["story"] = 1
    context.user_data["question"] = 0
    context.user_data["waiting_text"] = False
    context.user_data["secret"] = False


# ===================================
# /START
# ===================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reset_user(context)

    text = """
🌙━━━━━━━━━━━━━━━━━━━━━━🌙

        ❤️ Ассалому алайкум ❤️

Балким ҳозир сен:

«Оддий Telegram бот экан...»

деб ўйлагандирсан...

Лекин...

Бу ерда ҳаммаси бошқача...

Бу ерда оддий тугмалар эмас...

Оддий ёзувлар эмас...

Оддий гаплар ҳам эмас...

Бу ерда...

Юракдан чиққан сатрлар яширинган...

Ҳар бир ҳарф...

Ҳар бир сўз...

Ҳар бир нуқта...

Бир инсон ҳақида ўйлаб ёзилган...

Ҳеч ким мажбур қилмади...

Ҳеч ким айтмади...

Шунчаки...

Қалбим шуни истади...

Чунки...

Ҳаётда баъзи инсонлар
оддий инсон бўлиб қолмайди...

Улар инсоннинг энг гўзал
хотираларига айланади...

Мен учун ҳам
шундай инсон бор...

🌹

Бу саёҳат давомида
мен сенга...

Кўп нарсаларни айтаман...

Балким куларсан...

Балким ҳайрон қоларсан...

Балким жимгина ўқирсан...

Лекин...

Ҳар бир саҳифани
охиригача ўқишингни истайман...

Чунки...

Энг муҳим гаплар
охирида бўлади... ❤️

🌙━━━━━━━━━━━━━━━━━━━━━━🌙
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🌹 Давом этиш",
                callback_data="story1",
            )
        ]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ===================================
# STORY 1
# ===================================

async def story1(query):

    text = """
🌸

Биласанми...

Инсон ҳаётида минглаб одамлар
учрар экан...

Кимдир бир кунга...

Кимдир бир ойга...

Кимдир бир йилга...

Лекин...

Шундай инсонлар ҳам бўлар эканки...

Улар келгач...

Оддий кунлар ҳам
байрамдек туюлар экан...

Оддий табассум ҳам
бутун кайфиятни ўзгартирар экан...

Оддий хабар ҳам
соатлаб кутилар экан...

Мен буни...

Сени учратганимдан кейин тушундим... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Кейингиси",
                callback_data="story2",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    # ===================================
# STORY 2
# ===================================

async def story2(query):

    text = """
🌙

Баъзан...

Инсоннинг бахти
катта нарсаларда эмас экан...

Оддийгина...

"Қалайсан?" деган хабарда...

"Эҳтиёт бўл..." деган сўзда...

"Яхши ухла..." деган тилакда...

"Кулгин..." деган илтимосда...

Мен учун эса...

Сен билан бўлган
ҳар бир суҳбат...

Ҳар бир лаҳза...

Ҳар бир кулги...

Энг қиммат хотирага айланиб қолган...

Шунинг учун ҳам...

Бугун сенга
оддий хабар эмас...

Юрагимни кўрсатмоқчиман... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🌹 Давом этиш",
                callback_data="story3",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story1",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ===================================
# STORY 3
# ===================================

async def story3(query):

    text = """
🌸

Ҳар куни...

Одамлар минглаб
инсонларни кўришади...

Лекин...

Ҳамма ҳам
қалбда из қолдирмайди...

Сен эса...

Ҳеч нарса қилмасанг ҳам...

Оддийгина кулиб қўйсанг ҳам...

Кайфиятимни ўзгартириб юборасан...

Балким...

Бу сен учун оддийдир...

Аммо...

Мен учун эмас...

Чунки...

Сенинг табассуминг...

Мен кўрган
энг чиройли манзаралардан бири... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Давоми",
                callback_data="story4",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story2",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ===================================
# STORY 4
# ===================================

async def story4(query):

    text = """
🥹

Мен мукаммал эмасман...

Балким...

Кўп хатолар қилгандирман...

Баъзан хафа ҳам қилгандирман...

Лекин...

Битта нарсани
ҳеч қачон унутмагин...

Менинг ниятим
сени хафа қилиш бўлмаган...

Аксинча...

Сени кулишингни...

Бахтли бўлишингни...

Орзуларинг ушалишини...

Ҳар доим хоҳлаганман...

Ва ҳозир ҳам...

Шу нарсани хоҳлайман... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🌹 Кейингиси",
                callback_data="story5",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story3",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    # ===================================
# STORY 5
# ===================================

async def story5(query):

    text = """
🌙

Ҳозир сен шу ёзувларни ўқияпсан...

Балким...

«Буларнинг ҳаммасини
ўзи ёздими?»

деб ўйлагандирсан...

Жавоби...

Ҳа...

Чунки сен учун
тайёр сўзлар етарли эмасди...

Сен учун
юракдан чиққан сўзлар керак эди...

Шунинг учун...

Ҳар бир жумлани
шошмасдан ёздим...

Ҳар бир нуқтани ҳам
ўйлаб қўйдим...

Чунки...

Сен бунга арзийсан... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🌹 Давом этиш",
                callback_data="story6",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story4",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ===================================
# STORY 6
# ===================================

async def story6(query):

    text = """
🌸

Мен ҳаётимда
кўплаб инсонларни учратдим...

Лекин...

Ҳеч ким менга
сенчалик таъсир қилмаган...

Сенинг биргина
«яхшиман»

деган хабаринг ҳам
кайфиятимни кўтариб юборади...

Сен эса...

Бу ҳақда
балким билмайсан ҳам...

Шунинг учун...

Бугун сенга
шу гапларни айтишни истадим... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Кейингиси",
                callback_data="story7",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story5",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ===================================
# STORY 7
# ===================================

async def story7(query):

    text = """
🥹

Энди мен сендан
битта савол сўрамоқчиман...

Ростини айт...

Мендан хафа эмасмисан?

Чунки...

Сенинг хафалигинг...

Мени ҳам хафа қилади...

Агар
бирор марта
беихтиёр
сени ранжитган бўлсам...

Бугун...

Юрагимдан туриб...

Кечирим сўрайман... ❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "😊 Ҳафа эмасман",
                callback_data="questions",
            )
        ],
        [
            InlineKeyboardButton(
                "🥺 Бироз ҳафа бўлганман",
                callback_data="sorry",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story6",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ===================================
# UZR SO'RASH
# ===================================

async def sorry_scene(query):

    text = """
🥺

Ростдан ҳам...

Сени хафа қилган бўлсам...

Мени кечир...

Бу ҳеч қачон
атайлаб бўлмаган...

Чунки...

Мен учун сенинг
табассуминг...

Ҳар қандай баҳсдан ҳам
қиммат...

Ҳар қандай ғурурдан ҳам
устун...

Иложи бўлса...

Яна бир марта
кулиб қўйгин... 🌹❤️
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "❤️ Кечирдим",
                callback_data="questions",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Орқага",
                callback_data="story7",
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
