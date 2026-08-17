from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8510572957:AAHFOGt4-7Lxw87SvVE_ydIpyWqGOqUd-n4"
ADMIN_ID = 1649615322  # თქვენი პირადი Telegram ID
CASINO_REF_LINK = "https://track.magicclick.partners/click?o=2088&a=26227"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. /start ბრძანება - მისასალმებელი ტექსტი და ღილაკი
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    text = (
        "<b>Want to Beat the Casino? 🚀</b>\n\n"
        "✨ Forget random luck—pro gamblers use a proven mathematical system, and now you can too.\n\n"
        "💡 Inside our exclusive community, we reveal the <b>Top 5 Pro Methods</b> that consistently beat the house, starting with a minimum budget of just <b>$30</b>.\n\n"
        "🔒 <b>How to Get Instant Access:</b>\n"
        "<i>⚠️ These secrets only work on our verified partner platform where our winning algorithms are optimized.</i>\n\n"
        "💵 • Deposit your starting bank (minimum $30).\n"
        "📸 • <b>Send a screenshot of your registration here to unlock the full 5-Method Guide instantly!</b>\n\n"
        "🔥 <b>Spots are strictly limited!</b> Register now, fund your $30, and start winning today. 🏆"
    )

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚀 Register Now", url=CASINO_REF_LINK))
    
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# 2. სკრინის მიღება და ადმინისტრატორთან გაგზავნა
@dp.message(F.photo)
async def handle_screenshot(message: types.Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "No username"
    
    caption = (
        "📥 <b>New Registration Screenshot!</b>\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: <code>{user.id}</code>"
    )

    try:
        # სკრინს უგზავნის პირდაპირ თქვენს Telegram-ში
        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=caption,
            parse_mode="HTML"
        )
        
        # მომხმარებელს უბრუნებს ინგლისურ დასტურს
        await message.answer("✅ Screenshot received successfully! The administrator will verify it and send you the 5-Method Guide shortly.")
    
    except Exception as e:
        print(f"Error sending screenshot: {e}")
        await message.answer("❌ An error occurred while sending your screenshot. Please try again.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
