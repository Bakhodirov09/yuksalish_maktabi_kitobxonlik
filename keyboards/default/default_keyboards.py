from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Telefon raqam jonatish", request_contact=True)
        ]
    ], resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Test ishlash")
        ]
    ], resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor qilish")
        ]
    ], resize_keyboard=True
)


admins_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"📕➕ Kitob qoshish"),
            KeyboardButton(text="➕📝 Savol qoshish")
        ],
        [
            KeyboardButton(text="👤📊 Ota onalar natijalari"),
            KeyboardButton(text="⭐️ Ballarni ozgartirish")
        ],
        [
            KeyboardButton(text=f"🏛➕ Sinf qoshish"),
            KeyboardButton(text=f"🏛➕ Gurux qoshish")
        ],
        [
            KeyboardButton(text="➕👤 O'quvchi qoshish")
        ],
        [
            KeyboardButton(text=f"👤➕ Admin qoshish"),
            KeyboardButton(text="🚫👤 Admin olib tashlash")
        ],
        [
            KeyboardButton(text="📕 Kitob olib tashlash")
        ],
    ], resize_keyboard=True
)

sccores = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"❌ Bekor qilish")
        ],
        [
            KeyboardButton(text="✅ Togri javob uchun achkoni o'zgartirish")
        ],
        [
            KeyboardButton(text="❌ Notogri javob uchun achkoni o'zgartirish")
        ],
        [
            KeyboardButton(text="📝 Savollar miqdorini o'zgartirish")
        ]
    ], resize_keyboard=True
)

options = ReplyKeyboardMarkup(
    keyboard=[
        [
          KeyboardButton(text="❌ Bekor qilish")
        ],
        [
            KeyboardButton(text="A")
        ],
        [
            KeyboardButton(text="B")
        ],
        [
            KeyboardButton(text="D")
        ],
    ], resize_keyboard=True
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Xa"),
            KeyboardButton(text="❌ Yo'q")
        ]
    ], resize_keyboard=True
)

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🪪 Ro'yxatdan o'tish")
        ]
    ], resize_keyboard=True
)

dad_mom = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍🦰 Farzandimning otasiman"),
            KeyboardButton(text="🧕 Farzandimning onasiman")
        ]
    ], resize_keyboard=True
)
