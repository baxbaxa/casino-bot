from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8510572957:AAHFOGt4-7Lxw87SvVE_ydIpyWqGOqUd-n4"
CASINO_REF_LINK = "https://track.magicclick.partners/click?o=2088&a=26227"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    text = (
        "<b>Want to Beat the Casino? 🚀</b>\n\n"
        "✨ Forget random luck—pro gamblers use a proven mathematical system, and now you can too.\n\n"
        "💡 Inside our exclusive community, we reveal the <b>Top 5 Pro Methods</b> that consistently beat the house, starting with a minimum budget of just <b>$30</b>.\n\n"
        "🔒 <b>How to Get Instant Access:</b>\n"
        "<i>⚠️ These secrets only work on our verified partner platform where our winning algorithms are optimized.</i>\n\n"
        "💵 • Deposit your starting bank (minimum $30).\n"
        "📸 • Send a screenshot of your registration to unlock the full 5-Method Guide instantly!\n\n"
        "🔥 <b>Spots are strictly limited!</b> Register now, fund your $30, and start winning today. 🏆"
    )

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚀 Register Now", url=CASINO_REF_LINK))
    
    await message.answer(
        text, 
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
