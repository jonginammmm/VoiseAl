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
ADMIN_ID = 6394219796
FREE_LIMIT = 7

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= DB =================
conn = sqlite3.connect("probot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
requests INTEGER DEFAULT 0,
last TEXT,
voice TEXT,
style TEXT,
history TEXT
)
""")
conn.commit()

# ================= HELPERS =================
def add_user(u):
    cursor.execute("SELECT * FROM users WHERE id=?", (u.id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (id, username) VALUES (?,?)", (u.id, u.username))
        conn.commit()

def check_limit(uid):
    cursor.execute("SELECT requests,last FROM users WHERE id=?", (uid,))
    r = cursor.fetchone()
    if not r: return True

    req,last = r
    if last:
        if datetime.now() - datetime.fromisoformat(last) > timedelta(days=1):
            cursor.execute("UPDATE users SET requests=0 WHERE id=?", (uid,))
            conn.commit()
            return True

    return req < FREE_LIMIT

def update_req(uid):
    cursor.execute("UPDATE users SET requests=requests+1,last=? WHERE id=?",
                   (datetime.now().isoformat(), uid))
    conn.commit()

def save(uid, voice=None, style=None, text=None):
    if voice:
        cursor.execute("UPDATE users SET voice=? WHERE id=?", (voice, uid))
    if style:
        cursor.execute("UPDATE users SET style=? WHERE id=?", (style, uid))
    if text:
        cursor.execute("UPDATE users SET history=? WHERE id=?", (text[:100], uid))
    conn.commit()

# ================= SMART TEXT FIX =================
def smart_fix(text):
    fixes = {
        "salomlar": "Salom",
        "nma gap": "Nima gap",
        "qalesan": "Qalaysan"
    }
    for k,v in fixes.items():
        text = text.replace(k,v)
    return text

# ================= UI =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎙 Ovoz yaratish", callback_data="create"),
        InlineKeyboardButton("📊 Profil", callback_data="profile")
    )
    kb.add(
        InlineKeyboardButton("🧠 Tarix", callback_data="history"),
        InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings")
    )
    kb.add(
        InlineKeyboardButton("👨‍💻 Admin", url="https://t.me/oybekortiqboyevv")
    )
    return kb

def voice_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👨‍🎤 Erkak", callback_data="male"),
        InlineKeyboardButton("👩‍🎤 Ayol", callback_data="female")
    )
    kb.add(
        InlineKeyboardButton("🤖 Robot", callback_data="robot"),
        InlineKeyboardButton("🎙 Studio", callback_data="studio")
    )
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    return kb

def style_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎙 Podcast", callback_data="podcast"),
        InlineKeyboardButton("😂 Meme", callback_data="meme")
    )
    kb.add(
        InlineKeyboardButton("🎮 Gamer", callback_data="gamer"),
        InlineKeyboardButton("❤️ Romantik", callback_data="romantic")
    )
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    return kb

# ================= START =================
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    add_user(msg.from_user)

    await msg.answer(
        " <b>Voice AI Pro</b>\n\n"
        "Minimal. Fast. Powerful.\n\n"
        f"Limit: {FREE_LIMIT}/day",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ================= CALLBACK =================
@dp.callback_query_handler()
async def cb(call: types.CallbackQuery):
    uid = call.from_user.id

    if call.data == "create":
        await call.message.edit_text("🎙 KeraklI ovozni tanlang", reply_markup=voice_menu())

    elif call.data in ["male","female","robot","studio"]:
        save(uid, voice=call.data)
        await call.message.edit_text("🎨 KeraklI tugmani tanlang", reply_markup=style_menu())

    elif call.data in ["podcast","meme","gamer","romantic"]:
        save(uid, style=call.data)
        await call.message.edit_text("✍️ Marhamat matnizni jonating")

    elif call.data == "profile":
        cursor.execute("SELECT requests FROM users WHERE id=?", (uid,))
        r = cursor.fetchone()
        await call.message.edit_text(f"📊 Used: {r[0]}", reply_markup=main_menu())

    elif call.data == "history":
        cursor.execute("SELECT history FROM users WHERE id=?", (uid,))
        h = cursor.fetchone()
        await call.message.edit_text(f"🧠 Last:\n{h[0]}", reply_markup=main_menu())

    elif call.data == "back":
        await call.message.edit_text("Menu", reply_markup=main_menu())

# ================= GENERATE =================
@dp.message_handler()
async def gen(msg: types.Message):
    uid = msg.from_user.id

    if not check_limit(uid):
        await msg.answer("❌ Sizga berilgan limit tugadi ertagacha☺️")
        return

    text = smart_fix(msg.text)

    cursor.execute("SELECT voice,style FROM users WHERE id=?", (uid,))
    data = cursor.fetchone()

    if not data or not data[0]:
        await msg.answer("❗ Select voice first")
        return

    voice,style = data

    await msg.answer("⏳ Ovoz tayyorlanmoqda biroz kuting...")

    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    payload = {
        "text": f"{style}: {text}",
        "model_id": "eleven_multilingual_v2"
    }

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json=payload, headers=headers)

        if r.status_code == 200:
            file = f"{uid}.mp3"
            open(file,"wb").write(r.content)

            await bot.send_audio(msg.chat.id, open(file,"rb"))

            os.remove(file)
            update_req(uid)
            save(uid, text=text)

        else:
            await msg.answer("❌ API Token Xato")

    except:
        await msg.answer("❌ Serverda xatolik bor")

# ================= ADMIN =================
@dp.message_handler(commands=['users'])
async def users(msg: types.Message):
    if msg.from_user.id != ADMIN_ID: return
    cursor.execute("SELECT COUNT(*) FROM users")
    await msg.answer(f"Users: {cursor.fetchone()[0]}")

@dp.message_handler(commands=['find'])
async def find(msg: types.Message):
    if msg.from_user.id != ADMIN_ID: return
    uid = int(msg.get_args())
    cursor.execute("SELECT username FROM users WHERE id=?", (uid,))
    u = cursor.fetchone()
    await msg.answer(f"User: {u}")

@dp.message_handler(commands=['send'])
async def send(msg: types.Message):
    if msg.from_user.id != ADMIN_ID: return
    text = msg.get_args()

    cursor.execute("SELECT id FROM users")
    for u in cursor.fetchall():
        try:
            await bot.send_message(u[0], text)
        except:
            pass

    await msg.answer("Sent")

# ================= RUN =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
