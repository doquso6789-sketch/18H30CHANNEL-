import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)


async def send_message(text):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "☕️ Donate Ủng Hộ",
                url="https://t.me/DonateXosoAI"
            )
        ]
    ])

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
