import logging
import telebot
import sqlite3
import requests
import os
from datetime import datetime, timedelta

# ================= CONFIG =================
API_TOKEN = "8644445513:AAHMYm0GkhFCx2jCGWKwiLhNAwmUaailT1U"
ELEVEN_API_KEY = "sk_39b547e65c3b5b48ee6f0485e8daeb486ee7e5906f7aaf6b"
ADMIN_ID = 6394219796
FREE_LIMIT = 7


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# ================= DATABASE =================
conn = sqlite3.connect("voisalbot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    username TEXT,
    created_at TEXT,
    requests INTEGER DEFAULT 0,
    is_premium INTEGER DEFAULT 0,
    last_request TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    created_at TEXT
)
""")

conn.commit()


# ================= STATE =================
user_state = {}


# ================= HELPERS =================
def register_user(user):
    cursor.execute("SELECT * FROM users WHERE telegram_id=?", (user.id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (telegram_id, username, created_at) VALUES (?, ?, ?)",
            (user.id, user.username, datetime.now().isoformat())
        )
        conn.commit()


def check_limit(user_id):
    cursor.execute("SELECT requests, last_request, is_premium FROM users WHERE telegram_id=?", (user_id,))
    row = cursor.fetchone()

    if not row:
        return True

    requests_count, last_request, premium = row

    if premium:
        return True

    if last_request:
        last = datetime.fromisoformat(last_request)
        if datetime.now() - last > timedelta(days=1):
            cursor.execute("UPDATE users SET requests=0 WHERE telegram_id=?", (user_id,))
            conn.commit()
            return True

    return requests_count < FREE_LIMIT


def increment_usage(user_id):
    cursor.execute("""
        UPDATE users
        SET requests = requests + 1,
            last_request=?
        WHERE telegram_id=?
    """, (datetime.now().isoformat(), user_id))
    conn.commit()


def log_request(user_id, text):
    cursor.execute(
        "INSERT INTO logs (user_id, text, created_at) VALUES (?, ?, ?)",
        (user_id, text, datetime.now().isoformat())
    )
    conn.commit()


# ================= KEYBOARDS =================
def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎧 Create Voice", callback_data="create"))
    kb.add(InlineKeyboardButton("📊 Profile", callback_data="profile"))
    kb.add(InlineKeyboardButton("💎 Premium", callback_data="premium"))
    return kb


def voice_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👨 Male", callback_data="male"))
    kb.add(InlineKeyboardButton("👩 Female", callback_data="female"))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back_main"))
    return kb


def style_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎙 Podcast", callback_data="podcast"))
    kb.add(InlineKeyboardButton("😂 Meme", callback_data="meme"))
    kb.add(InlineKeyboardButton("🎮 Gamer", callback_data="gamer"))
    kb.add(InlineKeyboardButton("❤️ Romantic", callback_data="romantic"))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back_voice"))
    return kb


# ================= START =================
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    register_user(msg.from_user)
    await msg.answer("🚀 VoisAlBot ishga tushdi!", reply_markup=main_menu())


# ================= CALLBACK =================
@dp.callback_query_handler()
async def callbacks(call: types.CallbackQuery):
    uid = call.from_user.id

    if call.data == "create":
        await call.message.edit_text("Matn yuboring", reply_markup=voice_menu())

    elif call.data == "profile":
        cursor.execute("SELECT requests, is_premium FROM users WHERE telegram_id=?", (uid,))
        r = cursor.fetchone()

        if r:
            await call.message.edit_text(
                f"📊 Requests: {r[0]}\n💎 Premium: {r[1]}",
                reply_markup=main_menu()
            )

    elif call.data == "premium":
        await call.message.edit_text(
            "💎 Premium olish uchun admin bilan bog‘laning",
            reply_markup=main_menu()
        )

    elif call.data in ["male", "female"]:
        user_state[uid] = {"voice": call.data}
        await call.message.edit_text("Style tanlang", reply_markup=style_menu())

    elif call.data in ["podcast", "meme", "gamer", "romantic"]:
        if uid not in user_state:
            user_state[uid] = {}

        user_state[uid]["style"] = call.data
        await call.message.edit_text("Endi matn yuboring...")

    elif call.data == "back_main":
        await call.message.edit_text("Menu", reply_markup=main_menu())

    elif call.data == "back_voice":
        await call.message.edit_text("Ovoz tanlang", reply_markup=voice_menu())


# ================= TEXT TO VOICE =================
@dp.message_handler()
async def generate(msg: types.Message):
    uid = msg.from_user.id

    if uid not in user_state:
        await msg.answer("Avval /start dan boshlang")
        return

    if not check_limit(uid):
        await msg.answer("❌ Limit tugadi. Premium oling")
        return

    text = msg.text
    voice = user_state[uid].get("voice", "male")

    await msg.answer("⏳ Generatsiya...")

    voice_id = "EXAVITQu4vr4xnSDxMaL" if voice == "male" else "MF3mGyEYCl7XYWbV9V6O"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == 200:
        file_path = f"voice_{uid}.mp3"

        with open(file_path, "wb") as f:
            f.write(r.content)

        with open(file_path, "rb") as f:
            await bot.send_audio(msg.chat.id, f, caption="🎧 Done")

        increment_usage(uid)
        log_request(uid, text)

        os.remove(file_path)

    else:
        await msg.answer("❌ Xatolik ElevenLabs API")


# ================= RUN =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
