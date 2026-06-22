import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_message(text):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "☕️ Donate Ủng Hộ",
                url="https://t.me/DonateXosoAI"
            )
        ]
    ])

    bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
