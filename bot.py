import logging
import sqlite3
import requests
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================= CONFIG =================
API_TOKEN = "8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw"
ELEVEN_API_KEY = "sk_59b3a1586fb9ca5ea49721713f40dd6f0da599a37b6076d3"
ADMIN_ID = 6394219796  # o'zingni ID
FREE_LIMIT = 7

CHANNEL_LINK = "https://t.me/C0META_Uc"
ADMIN_LINK = "@oybekortiqboyevv"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= DATABASE =================
conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT,
    created_at TEXT,
    requests INTEGER DEFAULT 0,
    is_premium INTEGER DEFAULT 0,
    last_request TEXT,
    voice TEXT,
    style TEXT
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
    UPDATE users SET requests = requests + 1, last_request=?
    WHERE telegram_id=?
    """, (datetime.now().isoformat(), user_id))
    conn.commit()

# ================= MENUS =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎙 Voice yaratish", callback_data="create"),
        InlineKeyboardButton("📊 Profil", callback_data="profile"),
    )
    kb.add(
        InlineKeyboardButton("🚀 Kanal", url=CHANNEL_LINK),
        InlineKeyboardButton("👨‍💻 Admin", url=ADMIN_LINK),
    )
    return kb

def voice_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👨 Erkak", callback_data="male"),
        InlineKeyboardButton("👩 Ayol", callback_data="female"),
    )
    kb.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back"))
    return kb

def style_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎙 Podcast", callback_data="podcast"),
        InlineKeyboardButton("😂 Meme", callback_data="meme"),
    )
    kb.add(
        InlineKeyboardButton("🎮 Gamer", callback_data="gamer"),
        InlineKeyboardButton("❤️ Romantic", callback_data="romantic"),
    )
    kb.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back"))
    return kb

# ================= START =================
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    register_user(msg.from_user)

    text = f"""
🚀 <b>PRO VOICE AI BOT</b>

🎧 Matndan real ovoz yarating
🔥 Eng sifatli AI ovozlar

📌 Limit: {FREE_LIMIT} ta / kun
"""

    await msg.answer(text, parse_mode="HTML", reply_markup=main_menu())

# ================= CALLBACK =================
@dp.callback_query_handler()
async def callbacks(call: types.CallbackQuery):
    uid = call.from_user.id

    if call.data == "create":
        await call.message.edit_text("🎙 KeraklI Ovozni tanlang:", reply_markup=voice_menu())

    elif call.data == "male":
        user_state[uid] = {"voice": "male"}
        await call.message.edit_text("🎨 Stilni tanlang:", reply_markup=style_menu())

    elif call.data == "female":
        user_state[uid] = {"voice": "female"}
        await call.message.edit_text("🎨 Stilni tanglang:", reply_markup=style_menu())

    elif call.data in ["podcast","meme","gamer","romantic"]:
        user_state[uid]["style"] = call.data
        await call.message.edit_text("✍️ Marhamat Matn yuboring...")

    elif call.data == "profile":
        cursor.execute("SELECT requests, is_premium FROM users WHERE telegram_id=?", (uid,))
        r = cursor.fetchone()

        await call.message.edit_text(
            f"📊 Ishlatilgan: {r[0]}\n💎 Premium: {r[1]}",
            reply_markup=main_menu()
        )

    elif call.data == "back":
        await call.message.edit_text("Menu", reply_markup=main_menu())

# ================= GENERATE =================
@dp.message_handler()
async def generate(msg: types.Message):
    uid = msg.from_user.id

    if uid not in user_state:
        await msg.answer("❗ Avval /start bosing")
        return

    if not check_limit(uid):
        await msg.answer("❌ Limitiz tugadi")
        return

    text = msg.text
    voice = user_state[uid]["voice"]

    await msg.answer("🎧 Ovoz tayyorlanmoqda biroz kuting...")

    voice_id = "21m00Tcm4TlvDq8ikWAM" if voice == "male" else "EXAVITQu4vr4xnSDxMaL"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    try:
        r = requests.post(url, json=payload, headers=headers)

        if r.status_code == 200:
            file = f"{uid}.mp3"

            with open(file, "wb") as f:
                f.write(r.content)

            with open(file, "rb") as f:
                await bot.send_audio(msg.chat.id, f)

            os.remove(file)
            increment_usage(uid)

        else:
            await msg.answer("❌ API Token xato")

    except Exception as e:
        await msg.answer("❌ Server xato")

# ================= ADMIN =================
@dp.message_handler(commands=['stat'])
async def stat(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    await msg.answer(f"👥 Users: {users}")

# ================= RUN =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
