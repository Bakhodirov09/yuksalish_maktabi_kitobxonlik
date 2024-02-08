from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

channels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Obuna Bo'lish", url="https://t.me/Muhammadali_Eshonqulov")
        ],
        [
            InlineKeyboardButton(text="➕ Obuna Bo'lish", url="https://t.me/yuksalish_maktablari")
        ],
        [
            InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")
        ]
    ]
)

pagination = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="left"),
            InlineKeyboardButton(text="➡️", callback_data="right")
        ]
    ]
)
