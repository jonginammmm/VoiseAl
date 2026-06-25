from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"

# ---------- START SCREEN ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌸 Xush kelibsan, gulim...\n\n"
        "Bu mendan senga kichik sovg‘a ❤️"
    )

    keyboard = [
        [InlineKeyboardButton("💖 START", callback_data="start_story")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------- STORY 1 ----------
async def story1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "💌 Hayotim, borligim, mehribonim...\n\n"
        "Bu botni sen uchun yaratdim ❤️\n"
        "Bugun seni hafa qilganimni bilaman...\n"
        "Nafaqat bugun, oldin ham...\n\n"
        "Shuning uchun senga 1-2 narsa yozdim...\n"
        "Buni bilishni xohlaysanmi?"
    )

    keyboard = [
        [InlineKeyboardButton("❤️ Ha, albatta xohlayman", callback_data="yes")],
        [InlineKeyboardButton("💔 Uncha xohlamayapman", callback_data="no")]
    ]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------- YES PATH ----------
async def yes_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "💖 Jonim...\n\n"
        "Sen mendan hafa emasmisan?"
    )

    keyboard = [
        [InlineKeyboardButton("😊 Ha, hafa emasman", callback_data="happy")],
        [InlineKeyboardButton("😔 Yo‘q", callback_data="sad")]
    ]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def happy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🌸 Rahmat...\n\n"
        "Sen meni kechirding ❤️\n"
        "Men seni juda qadrlayman..."
    )


async def sad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "💔 Kechirasan...\n\n"
        "Men seni xafa qilgan bo‘lsam, uzr...\n"
        "Yana hammasini tuzataman ❤️"
    )


# ---------- NO PATH ----------
async def no_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🌸 Nima bo‘ldi gulim?\n"
        "Kimdir hafa qildimi yoki nimadir yoqmadimi?"
    )

    keyboard = [
        [InlineKeyboardButton("😔 Ha, hafa qildi", callback_data="hurt")],
        [InlineKeyboardButton("🙂 Yo‘q, hammasi joyida", callback_data="ok")]
    ]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def hurt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "💌 Menga yoz:\n@oybekortiqvoyevv\n\n"
        "Shu yerga yozsang, hamma darding yengillashadi ❤️"
    )


async def ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🌸 Unda yaxshi...\n"
        "Demak kayfiyating yaxshi ❤️\n\n"
        "Davom etamizmi?"
    )

    keyboard = [
        [InlineKeyboardButton("💖 Ha, albatta davom etamiz", callback_data="continue")]
    ]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------- CONTINUE (10 SAVOL FLOW) ----------
async def continue_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["q"] = 1

    await query.edit_message_text(
        "💖 Boshladik...\n\n1-savol:\nMen sen uchin kimman🫣?"
    )


# ---------- ROUTER ----------
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "start_story":
        await story1(update, context)

    elif data == "yes":
        await yes_path(update, context)

    elif data == "no":
        await no_path(update, context)

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


# ---------- RUN ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))

app.run_polling()
