import logging
import sqlite3
import requests
import os
import time
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================= CONFIG =================
API_TOKEN = os.environ.get("8644445513:AAFp6lAsKvpTGGpw6KY01QhQyGp729aWYIw")
ELEVEN_API_KEY = os.environ.get("sk_59b3a1586fb9ca5ea49721713f40dd6f0da599a37b6076d3")
ADMIN_ID = int(os.environ.get("6394219796", "0"))

FREE_LIMIT = 7

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= DATABASE =================
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    username TEXT,
    created_at TEXT,
    requests INTEGER DEFAULT 0,
    last_request TEXT,
    voice TEXT,
    is_blocked INTEGER DEFAULT 0
)
""")
conn.commit()

# ================= STATE =================
user_state = {}

# ================= USER SYSTEM =================
def register_user(user):
    cursor.execute("SELECT telegram_id FROM users WHERE telegram_id=?", (user.id,))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (telegram_id, username, created_at)
        VALUES (?, ?, ?)
        """, (user.id, user.username, datetime.now().isoformat()))
        conn.commit()

def get_user_id(uid):
    cursor.execute("SELECT id FROM users WHERE telegram_id=?", (uid,))
    r = cursor.fetchone()
    return r[0] if r else None

# ================= LIMIT SYSTEM =================
def check_limit(uid):
    cursor.execute("SELECT requests, last_request FROM users WHERE telegram_id=?", (uid,))
    row = cursor.fetchone()

    if not row:
        return True

    req, last = row

    if last:
        last_time = datetime.fromisoformat(last)
        if datetime.now() - last_time > timedelta(days=1):
            cursor.execute("UPDATE users SET requests=0 WHERE telegram_id=?", (uid,))
            conn.commit()
            return True

    return req < FREE_LIMIT

def add_request(uid):
    cursor.execute("""
    UPDATE users
    SET requests = requests + 1,
        last_request = ?
    WHERE telegram_id = ?
    """, (datetime.now().isoformat(), uid))
    conn.commit()

# ================= KEYBOARDS =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎙 Ovoz", callback_data="voice"),
        InlineKeyboardButton("👤 Profil", callback_data="profile"),
    )
    kb.add(
        InlineKeyboardButton("⚙ Admin", callback_data="admin"),
    )
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    return kb

def voice_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👨 Erkak", callback_data="male"),
        InlineKeyboardButton("👩 Ayol", callback_data="female"),
    )
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    return kb

def admin_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📊 Statistika", callback_data="stats"),
        InlineKeyboardButton("👥 Foydalanuvchi", callback_data="users"),
    )
    kb.add(
        InlineKeyboardButton("📢 Broadcast", callback_data="broadcast"),
        InlineKeyboardButton("🚫 Ban list", callback_data="banlist"),
    )
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    return kb

# ================= START =================
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    register_user(msg.from_user)

    uid = get_user_id(msg.from_user.id)

    await msg.answer(
        f"🚀 VOICE AI BOTga xushkebsz\n\n👤 User ID: {uid}\n🎧 Matndan ovoz yaratish boti☺️",
        reply_markup=main_menu()
    )

# ================= CALLBACK ROUTER =================
@dp.callback_query_handler(lambda c: True)
async def cb(call: types.CallbackQuery):
    uid = call.from_user.id

    # MAIN
    if call.data == "voice":
        await call.message.edit_text("🎙 Ovozni tanlang", reply_markup=voice_menu())

    elif call.data == "profile":
        cursor.execute("SELECT requests FROM users WHERE telegram_id=?", (uid,))
        r = cursor.fetchone()
        await call.message.edit_text(
            f"👤 Profil\n\n📊 Requests: {r[0] if r else 0}",
            reply_markup=main_menu()
        )

    # VOICE
    elif call.data in ["male", "female"]:
        user_state[uid] = {"voice": call.data}
        await call.message.edit_text("✍️ Marhamat matn yuboring", reply_markup=back_btn())

    # ADMIN
    elif call.data == "admin":
        if uid != ADMIN_ID:
            await call.answer("No access", show_alert=True)
            return
        await call.message.edit_text("⚙ Admin Panel", reply_markup=admin_menu())

    elif call.data == "stats":
        cursor.execute("SELECT COUNT(*) FROM users")
        users = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(requests) FROM users")
        req = cursor.fetchone()[0] or 0

        await call.message.edit_text(
            f"📊 STATS\n\n👥 Users: {users}\n🔁 Requests: {req}",
            reply_markup=admin_menu()
        )

    elif call.data == "back":
        await call.message.edit_text("🏠 Menu", reply_markup=main_menu())

# ================= GENERATE VOICE =================
@dp.message_handler()
async def generate(msg: types.Message):
    uid = msg.from_user.id

    if uid not in user_state:
        await msg.answer("❗ Avval Ovozni tanlang")
        return

    if not check_limit(uid):
        await msg.answer("❌ Limit tugagan")
        return

    voice = user_state[uid]["voice"]

    await msg.answer("🎧 ..")

    voice_id = "21m00Tcm4TlvDq8ikWAM" if voice == "male" else "EXAVITQu4vr4xnSDxMaL"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": msg.text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)

        if r.status_code == 200:
            file = f"{uid}_{int(time.time())}.mp3"

            with open(file, "wb") as f:
                f.write(r.content)

            with open(file, "rb") as f:
                await bot.send_audio(msg.chat.id, f)

            os.remove(file)

            add_request(uid)

        else:
            await msg.answer("❌ API Xato")

    except Exception:
        await msg.answer("❌ Serverda xatolik")

# ================= RUN =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
