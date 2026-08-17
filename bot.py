import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- აქ ჩასვით თქვენი მონაცემები ---
TOKEN = "8227638682:AAEYe7LRCWds6WCubXCxbSvk1FDDB01YpDU"
CHANNEL_ID = -1004408814436  # თქვენი დახურული არხის/ჯგუფის ID (მინუსებით)
CASINO_REF_LINK = "https://track.magicclick.partners/click?o=2088&a=26227" # თქვენი კაზინოს რეფერალური ლინკი
# ---------------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

# მონაცემთა ბაზა (იმახსოვრებს ვინც დააჭირა)
def init_db():
    conn = sqlite3.connect("casino_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registered_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    text = (
        "Want to Beat the Casino? 🚀\n\n"
        "Forget random luck—pro gamblers use a proven mathematical system, and now you can too.\n\n"
        "Inside our exclusive community, we reveal the Top 5 Pro Methods that consistently beat the house, starting with a minimum budget of just $30.\n\n"
        "🔒 **How to Get Instant Access:**\n"
        "• Register on our verified partner platform.\n"
        "• Deposit your starting bank (minimum $30).\n\n"
        "აჭირეთ ქვემოთ მოცემულ ღილაკს რეგისტრაციისთვის და მიიღეთ წვდომა ჯგუფზე! 👇"
    )

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🚀 Register Now (Casino Link)",
        callback_data="clicked_register"
    ))

    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "clicked_register")
async def process_register_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or "No username"

    # ვინახავთ ბაზაში (ტრეკინგი)
    conn = sqlite3.connect("casino_users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO registered_users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
    except Exception as e:
        print(f"ბაზის შეცდომა: {e}")
    finally:
        conn.close()

    print(f"[ტრეკინგი] მომხმარებელმა @{username} (ID: {user_id}) დააჭირა რეგისტრაციის ღილაკს!")

    try:
        # ვუქმნით ერთჯერად პერსონალურ მიწვევიან ლინკს ჯგუფში შესასვლელად
        invite_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1
        )

        text_response = (
            f"მადლობა რომ დაინტერესდით! 🎉\n\n"
            f"1️⃣ ჯერ გაიარეთ რეგისტრაცია და დეპოზიტი აქ:\n👉 {CASINO_REF_LINK}\n\n"
            f"2️⃣ რეგისტრაციის შემდეგ, ესეც თქვენი პირადი ერთჯერადი მოსაწვევი ბმული ჩვენს დახურულ ჯგუფში:\n👉 {invite_link.invite_link}"
        )

        await callback.message.answer(text_response)

    except Exception as e:
        print(f"შეცდომა ლინკის გენერაციისას: {e}")
        await callback.message.answer(f"გთხოვთ გადახვიდეთ რეგისტრაციისთვის:\n👉 {CASINO_REF_LINK}")

    await callback.answer()

if __name__ == "__main__":
    import asyncio
    print("ბოტი გააქტიურებულია...")
    asyncio.run(dp.start_polling(bot))
