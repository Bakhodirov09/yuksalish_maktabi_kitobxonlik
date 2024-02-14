import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.default_keyboards import *
from keyboards.inline.inline_keyboards import pagination
from loader import dp
from states.states import *
from utils.db_api.database_functions import *


@dp.message_handler(commands="start")
async def bot_start(message: types.Message, state: FSMContext):
    # await insert_admin(chat_id=5596277119)
    # await update_all()
    # await delete()
    # await delete_books()
    # await delete_admin(chat_id=message.chat.id)
    # await insert_chegara()
    if await is_admin(chat_id=message.chat.id):
        userga = f"Xush Kelibsiz"
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        if await get_user(chat_id=message.chat.id):
            userga = f"😊 Botga Xush Kelibsiz"
            await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)
        else:
            userga = f"😊 Assalomu alaykum xurmatli ota-ona.Yuksalish maktabining kitobxonlik botiga xush kelibsiz!\nBotdan foydalanish uchun avvalo ro'yxatdan oting!"
            await message.answer(text=userga.capitalize(), reply_markup=register)
            await state.set_state("register")

@dp.message_handler(state="register", text="🪪 Ro'yxatdan o'tish")
async def register_handler(message: types.Message, state: FSMContext):
    userga = f"✍️ Royxatdan Otish Uchun Ismingizni Kiriting."
    await message.answer(text=userga.capitalize(), reply_markup=ReplyKeyboardRemove())
    await RegisterStates.name.set()

@dp.message_handler(state="*", text="❌ Bekor qilish")
async def cancelling_handler(message: types.Message, state: FSMContext):
    userga = f"❌ Bekor qilindi"
    if await is_admin(chat_id=message.chat.id):
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)
    await state.finish()

@dp.message_handler(state=RegisterStates.name)
async def get_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "name": message.text
    })
    userga = f"✍️ Endi Familyangizni Kiriting"
    await message.answer(text=userga.capitalize())
    await RegisterStates.surname.set()

@dp.message_handler(state=RegisterStates.surname)
async def get_surname_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "surname": message.text
    })
    userga = f"😊 Iltimos: {message.from_user.full_name} Telefon Raqamingizni Tugma Orqali Yuboring."
    await message.answer(text=userga.capitalize(), reply_markup=send_phone_number)
    await RegisterStates.phone_number.set()

@dp.message_handler(state="*", text="❌ Yo'q")
async def cancel_handler(message: types.Message, state: FSMContext):
    userga = f"✅ Bekor Qilindi"
    await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)
    await state.finish()

@dp.message_handler(state=RegisterStates.phone_number, content_types=types.ContentType.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "phone_number": message.contact.phone_number
    })
    userga = f"😊 Farzandingiz Nechinchi Sinfda Oqiydi?"
    sinflar1 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❌ Bekor qilish")
            ]
        ], resize_keyboard=True, row_width=1
    )
    sinflar = await get_all_classes()
    for sinf in sinflar:
        sinflar1.insert(KeyboardButton(text=f"{sinf['class_number']}"))
    await message.answer(text=userga.capitalize(), reply_markup=sinflar1)
    await state.set_state("parent_class")

@dp.message_handler(state="parent_class")
async def parent_class_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "classi": message.text
    })
    userga = f"{message.text}ning Qaysi Guruxida?"
    bolimla = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    groups = await get_all_groups(classi=message.text)
    for inn in groups:
        bolimla.insert(KeyboardButton(text=inn["group"]))
    await message.answer(text=userga.capitalize(), reply_markup=bolimla)
    await state.set_state("parent_class_bolim")

@dp.message_handler(state="parent_class_bolim")
async def parent_class_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "bolim": message.text
    })
    userga = f"😊 Siz Farzandingizni Otasimisiz Yoki Farzandingizi Onasi?"
    await message.answer(text=userga.capitalize(), reply_markup=dad_mom)
    await state.set_state("parent_who")

@dp.message_handler(state="parent_who", content_types=types.ContentType.TEXT)
async def parent_class_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    who = ""
    if message.text == "👨‍🦰 Farzandimning otasiman":
        who = "ota"
    else:
        who = "ona"
    await state.update_data({
        "who": who,
        "bolim": data["bolim"],
        "classi": data["classi"],
        "name": data["name"],
        "surname": data["surname"],
        "phone_number": data["phone_number"]
    })
    userga = f"😊 O'quvchilar Bolimidan Ozingizni Farzandingizni Tanlang."
    oquvchilar = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    studentlar = await get_all_students(sinf=data["classi"], gurux=data["bolim"])
    for oquvchi in studentlar:
        oquvchilar.insert(KeyboardButton(text=oquvchi["full_name"]))
    await message.answer(text=userga.capitalize(), reply_markup=oquvchilar)
    await state.set_state("select_guy")

@dp.message_handler(state="select_guy")
async def select_student_handler(message: types.Message, state: FSMContext):
    student_name = await get_student(student_name=message.text)
    if student_name:
        if message.from_user.username:
            await state.update_data({
                "student_name": student_name["full_name"],
                "username": message.from_user.username,
                "chat_id": message.chat.id
            })
        else:
            await state.update_data({
                "student_name": student_name["full_name"],
                "username": "Mavjud Emas",
                "chat_id": message.chat.id
            })
        data = await state.get_data()
        userga = ""
        try:
            await write_user_table(data=data)
            userga = f"😊 Marhamat Botdan Foydalanishingiz Mumkin!"
            await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)
            await state.finish()
        except Exception as exc:
            userga = f"😕 Kechirasiz Botda Xatolik Bor"
            await dp.bot.send_message(chat_id=-1002075245072, text=f"{exc} Line: 163 Bot Yuksalish Kitobxonlik")
            await dp.channel
            await message.answer(text=userga.capitalize(), reply_markup=register)
            await state.set_state("register")
    else:
        userga = f"😕 Kechirasiz: {message.text} Ism Familyalik Oquvchi Topilmadi"
        await message.answer(text=userga.capitalize(), reply_markup=register)
        await state.set_state("register")


@dp.message_handler(text="📝 Test ishlash")
async def solve_test_handler(message: types.Message, state: FSMContext):
    userga = f"😊 Test Ishlash Uchun Kitob Tanlang!"
    books1 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❌ Bekor qilish")
            ]
        ], resize_keyboard=True, row_width=1
    )
    kitoblar = await get_all_book()
    for kitob in kitoblar:
        books1.insert(KeyboardButton(text=f"{kitob['books']}"))
    await message.answer(text=userga.capitalize(), reply_markup=books1)
    await state.set_state("test_will")

@dp.message_handler(text="👤➕ Admin qoshish")
async def add_new_admin_hander(message: types.Message, state: FSMContext):
    userga = f"😊 Yangi Admin <b>CHAT ID</b> Raqamini Kiriting!"
    await message.answer(text=userga.capitalize(), reply_markup=cancel)
    await state.set_state("new_admin")

@dp.message_handler(state="new_admin")
async def add_new_admin(message: types.Message, state: FSMContext):
    userga = f""
    try:
        adminga = f"😊 Tabriklaymiz Siz Bu Telegram Botda Adminlik Huquqiga Ega Bo'ldingiz\nBotdan Foydalanishingiz Mumkin."
        userga = f"🥳 Yangi Admin Qoshildi"
        await dp.bot.send_message(chat_id=int(message.text), text=adminga, reply_markup=admins_panel)
        await insert_admin(chat_id=int(message.text))
    except ValueError:
        userga = f"😕 Kechirasiz ChAT ID Raqamni Faqat Butun Sonlarda Kiritishingiz Mumkin!"
    except Exception as e:
        await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 206 Bot Yuksalish Kitobxonlik")
        userga = f"😕 Kechirasiz Siz Notogri Chat ID Kiritdingiz Yoki Bu Chat Id Raqamdagi Foydalanuvchi Botda Mavjud Emas!"
    await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    await state.finish()

@dp.message_handler(text="🚫👤 Admin olib tashlash")
async def delete_from_admins_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        userga = f"😊 Olib Tashlamoqchi Adminingizni <b>CHAT ID</b> Raqamini Kiriting"
        await message.answer(text=userga.capitalize())
        await state.set_state("del_admin")
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(state="del_admin")
async def delete_admin_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        try:
            userga = f"👍 Adminlar Orasidan Olip Tashlandi!"
            usergaa1 = f"😕 Kechirasiz: {message.from_user.full_name} Siz Botda Adminlar Orasidan Olip Tashlandingiz!"
            await delete_admin(chat_id=int(message.text))
            await dp.bot.send_message(chat_id=int(message.text), text=usergaa1.capitalize(), reply_markup=user_main_menu)
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
        except Exception as exc:
            await dp.bot.send_message(chat_id=-1002075245072, text=f"{exc} Line: 230 Bot Yuksalish Kitobxonlik")
            userga = f"😕 Kechirasiz Siz Notogri ID Raqam Kiritdingiz Yoki Bunday ID Raqamdagi Admin Mavjud Emas"
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)
    await state.finish()

@dp.message_handler(text="🏛➕ Sinf qoshish")
async def add_new_class_handler(message: types.Message, state: FSMContext):
    if await is_admin(message.chat.id):
        userga = f"😊✍️ Yangi Sinf Raqamini Kiriting."
        await message.answer(text=userga.capitalize(), reply_markup=cancel)
        await state.set_state("add_new_class")
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(text="⭐️ Ballarni ozgartirish")
async def change_scores_handler_1(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        userga = f"😊 Qaysi Bolimni Balini Ozgartirmoqchisiz?"
        await message.answer(text=userga.capitalize(), reply_markup=sccores)
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(text="✅ Togri javob uchun achkoni o'zgartirish")
async def change_true_score_handler(message: types.Message, state: FSMContext):
    userga = f"✅😊 Togri Javob Uchun Bermoqchi Bolgan Yangi Ballingizni Kiriting"
    await message.answer(text=userga.capitalize(), reply_markup=cancel)
    await state.set_state("true_change")

@dp.message_handler(state="true_change")
async def true_score_changing_handler(message: types.Message, state: FSMContext):
    new_score = None
    messagee = message.text
    userga = f""
    try:
        if len(messagee) <= 2:
            new_score = f"{messagee}.0"
            try:
                await update_true_score(new_score=float(new_score))
                userga = f"🛠✅ Togri Javob Uchun Qoshish Kerak Bolgan Ball Muvaffaqqiyatli  O'zgartirildi!"
            except Exception as e:
                await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 276 Bot Yuksalish Kitobxonlik")
                userga = f"😕 Kechirasiz Botda Xatolik Bor Qayta Urinib Koring!"
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
            await state.finish()
        elif float(messagee) >= 100.0:
            userga = f"100 Dan Past Raqam Kiriting!"
            await message.answer(text=userga.capitalize())
        elif len(messagee) >= 3 and "." in messagee:
            new_score = messagee
            userga = f"✅ Togri Javob Uchun Beriladigan Ball Muvaffaqqiyatli  O'zgartirildi!"
            await update_true_score(new_score=float(new_score))
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
            await state.finish()
        elif int(messagee) >= 100:
            userga = f"100 Dan Past Raqam Kiriting!"
            await message.answer(text=userga.capitalize())
        else:
            userga = f"Togri Raqam Kiriting\nMasalan: <b>1.0</b> Kabi"
            await message.answer(text=userga.capitalize(), reply_markup=cancel)
    except ValueError:
        userga = f"❌ Kechirasiz Ballarni Faqat Raqamda Kiritishingiz Mumkin!"
        await message.answer(text=userga.capitalize(), reply_markup=cancel)
    except Exception as e:
        await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 299 Bot Yuksalish Kitobxonlik")
        userga = f"😕 Kechirasiz Xatolik Yuz Berdi Qayta Urinib Koring!"
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)

@dp.message_handler(text="❌ Notogri javob uchun achkoni o'zgartirish")
async def change_true_score_handler(message: types.Message, state: FSMContext):
    userga = f"✅😊 Notogri Javob Uchun Ayirish Uchun Bolgan Yangi Ballingizni Kiriting"
    await message.answer(text=userga.capitalize(), reply_markup=cancel)
    await state.set_state("false_change")

@dp.message_handler(state="false_change")
async def true_score_changing_handler(message: types.Message, state: FSMContext):
    new_score = None
    messagee = message.text
    userga = f""
    try:
        if len(messagee) <= 2:
            new_score = f"{messagee}.0"
            try:
                await update_false_score(new_score=float(new_score))
                userga = f"🛠✅ Notogri Javob Uchun Ayirish Kerak Bolgan Ball Muvaffaqqiyatli  O'zgartirildi!"
            except Exception as e:
                await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 321 Bot Yuksalish Kitobxonlik")
                userga = f"😕 Kechirasiz Botda Xatolik Bor Qayta Urinib Koring!"
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
            await state.finish()
        elif float(messagee) >= 100.0:
            userga = f"100 Dan Past Raqam Kiriting!"
            await message.answer(text=userga.capitalize())
        elif len(messagee) >= 3 and "." in messagee:
            new_score = messagee
            userga = f"✅ Notogri Javob Uchun Ayirib Tashlanadigan Ball Muvaffaqqiyatli  O'zgartirildi!"
            await update_false_score(new_score=float(new_score))
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
            await state.finish()
        elif int(messagee) >= 100:
            userga = f"100 Dan Past Raqam Kiriting!"
            await message.answer(text=userga.capitalize())
        else:
            userga = f"Togri Raqam Kiriting\nMasalan: <b>1.0</b> Kabi"
            await message.answer(text=userga.capitalize(), reply_markup=cancel)
    except ValueError:
        userga = f"❌ Kechirasiz Ballarni Faqat Raqamda Kiritishingiz Mumkin!"
        await message.answer(text=userga.capitalize(), reply_markup=cancel)
    except Exception as e:
        await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 344 Bot Yuksalish Kitobxonlik")
        userga = f"😕 Kechirasiz Xatolik Yuz Berdi Qayta Urinib Koring!"
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)

@dp.message_handler(text="📝 Savollar miqdorini o'zgartirish")
async def change_true_score_handler(message: types.Message, state: FSMContext):
    userga = f"😊 Ota Onalar Uchun Beriladigan Savollar Cheklovini Kiriting"
    await message.answer(text=userga.capitalize(), reply_markup=cancel)
    await state.set_state("cheklov_change")

@dp.message_handler(state="cheklov_change")
async def true_score_changing_handler(message: types.Message, state: FSMContext):
    new_score = None
    messagee = message.text
    userga = f""
    try:
        if "." in messagee:
            userga = f"Kechirasiz Siz Notogri Son Kiritingiz. Butun Son Kiriting\nMasalan: <b>15</b>, <b>50</b>"
            await message.answer(text=userga.capitalize(), reply_markup=cancel)
            await state.set_state("cheklov_change")
        else:
            userga = f"🛠✅ Ota Onalar Uchun Beriladigan Savollar Miqdori Muvaffaqqiyatli Ozgartirildi"
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
            new_score = int(messagee)
            await update_miqdor(new_score=new_score)
            await state.finish()
    except ValueError:
        userga = f"Kechirasiz Faqat Butun Son Kiriting\nMasalan: <b>15</b>, <b>50</b>"
        await message.answer(text=userga, reply_markup=cancel)
        await state.set_state("cheklov_change")
    except Exception as exc:
        await dp.bot.send_message(chat_id=-1002075245072, text=f"{exc} Line: 375 Bot Yuksalish Kitobxonlik")
        await message.answer(text="😔 Kechirasiz Botda Xatolik Bor\nXatolik Xaqidagi Ma'lumot Dasturchiga Yuborildi Qayta Urinib Koring!", reply_markup=admins_panel)
        await state.finish()

@dp.message_handler(state="add_new_class")
async def add_class_handler(message: types.Message, state: FSMContext):
    classs = message.text
    userga = ""
    if await is_admin(message.chat.id):
        if await have_class(class_num=classs.title()):
            userga = f"😕 Kechirasiz Bunday Sinf Mavjud!"
        else:
            try:
                await insert_class(class_num=classs.title())
                userga = f"🥳 Yangi Sinf Qoshildi"
            except Exception as e:
                userga = f"Xato"
                await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 392 Bot Yuksalish Kitobxonlik")
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        userga = f"😕❌ Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

    await state.finish()


@dp.message_handler(state="user_sure", text="✅ Xa")
async def sure_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    if await is_actived(chat_id=message.chat.id):
        await delete_user_result(chat_id=message.chat.id)
    savollar = await get_questions(subject=data["book"])
    if savollar:
        vaqt = message.date
        await insert_test_user(chat_id=message.chat.id, fan=data["book"], date_time=vaqt)
        savolla = []
        for savol in savollar:
            savolla.append(savol["question"])
        random_savol = random.choice(savolla)
        variantla = await get_sovol1(subject=data["book"], savol=random_savol)
        a = variantla["a"]
        b = variantla["b"]
        d = variantla["d"]
        true = variantla["true"]
        userga = f"""
📃❓ Savol: <b>{random_savol}</b>
A Variant: <b>{a}</b>
B Variant: <b>{b}</b>
D Variant: <b>{d}</b>
"""
        await state.update_data({
            "savol": random_savol,
            "book": data["book"],
            "true": true
        })
        await message.answer(text=userga.capitalize(), reply_markup=options)
        await state.set_state('testing')
    else:
        await message.answer(text=f"😔 Kechirasiz bizda bu kitobdan savollar hozirda mavjud emas.\n😊 Bot adminlari bu kitob ustida ishlashmoqda.", reply_markup=user_main_menu)
        await state.finish()

@dp.message_handler(state="true_variant")
async def true_variant_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text in ["A", "B", "D"]:
        await state.update_data({
            "true": message.text
        })
        data1 = await state.get_data()
        await add_question_to_db(data=data1)
        userga = f"🥳 {data['book']} Kitobi Uchun Savol Qoshildi!"
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        userga = f"😕 Kechirasiz Togri Variantni Tugmalar Orqali Tanlang!"
        await message.answer(text=userga.capitalize(), reply_markup=options)
        await state.set_state("true_variant")
    await state.finish()

@dp.message_handler(text='📕 Kitob olib tashlash')
async def remove_book_admin_handler(message: types.Message, state: FSMContext):
    adminga = f'📕 Qaysi kitobni olib tashlamoqchisiz?'
    all_books = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bookss = await get_all_book()
    all_books.insert(KeyboardButton(text='❌ Bekor qilish'))
    for book in bookss:
        all_books.insert(KeyboardButton(text=f"{book[0]}"))
    await message.answer(text=adminga, reply_markup=all_books)
    await state.set_state("remove_book")

@dp.message_handler(state='remove_book')
async def removing_book_sure(message: types.Message, state: FSMContext):
    adminga = f"{message.text} kitobini haqiqatdan ochirib yuborasizmi?"
    await state.update_data({
        "book": message.text
    })
    await message.answer(text=adminga, reply_markup=yes_no)
    await state.set_state("really_delete")

@dp.message_handler(state='really_delete')
async def really_delete_admin_handler(message: types.Message, state: FSMContext):
    adminga = ""
    if message.text[0] == "✅":
        data = await state.get_data()
        await delete_books(data['book'])
        adminga = '✅ Kitoobingiz muvaffaqqiyatli ochirildi.'
    else:
        adminga = '❌ Bekor qilindi.'
    await message.answer(text=adminga, reply_markup=admins_panel)
    await state.finish()

@dp.message_handler(text="🏛➕ Gurux qoshish")
async def add_group(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        userga = f"😊 Qaysi Sinfga Gurux Qoshmoqchisiz?"
        sinflar = await get_all_classes()
        sinfla = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="❌ Bekor qilish")
                ]
            ],row_width=1, resize_keyboard=True
        )
        for classla in sinflar:
            sinfla.add(KeyboardButton(text=classla["class_number"]))
        await message.answer(text=userga.capitalize(), reply_markup=sinfla)
        await state.set_state("select_class_admin")
    else:
        userga = f"😕 Kechirasiz {message.from_user.full_name} Siz Adminlik Xuquqiga Ega Emassiz"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(state="select_class_admin")
async def select_all_class_handler_1(message: types.Message, state: FSMContext):
    await state.update_data({
        "classi": message.text
    })
    userga = f"😊 Yangi Gurux Nomini Kiriting"
    await message.answer(text=userga.capitalize(), reply_markup=cancel)
    await state.set_state("select_class_admin_group")

@dp.message_handler(state="select_class_admin_group")
async def select_all_class_handler_1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    userga = ""
    try:
        await insert_new_group(data=data, new_group=message.text)
        userga = f"✅ Yangi Gurux {data['classi']}larga Qoshildi"
    except Exception as e:
        userga = f"😕 Kechirasiz Botda Xatolik Bor"
        await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line: 519 Bot Yuksalish Kitobxonlik")
    await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    await state.finish()

@dp.message_handler(state='testing', text="A")
async def a_option_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    togrimi = await is_true(data=data, text1="A")
    togri_variant = await get_true(data=data)
    achko = await get_achko(chat_id=message.chat.id)
    nechi_savol = await get_savol(chat_id=message.chat.id)
    falses = await get_user_falses(chat_id=message.chat.id)
    trues = await get_user_trues(chat_id=message.chat.id)
    chegarasi = await chegara()
    savollar = await get_questions(subject=data["book"])
    savolla = list()
    for savol in savollar:
        savolla.append(savol["question"])
    random_savol = random.choice(savolla)
    variantla = await get_sovol1(subject=data["book"], savol=random_savol)
    savolcha = f"""
📄❓ Savol: {random_savol}
A Variant: {variantla["a"]}
B Variant: {variantla["b"]}
D Variant: {variantla["d"]}
"""
    await state.update_data({
        "savol": random_savol,
        "book": data["book"],
        "true": variantla['true']
    })
    await update_user_savol(chat_id=message.chat.id, savol=nechi_savol["sovol"])
    userga = f""
    kottami = ""
    if togrimi:
        userga = f"✅ Togri Javob"
        await message.answer(text=userga.capitalize())
        for chegaraa in chegarasi:
            await update_user_score(chat_id=message.chat.id, scoree=achko["score"], miqdor=chegaraa["one_true_answer"])
            if chegaraa['savollar'] > nechi_savol['sovol']:
                kottami = True
            else:
                kottami = False
        await update_user_trues(chat_id=message.chat.id, trues=trues["trues"])
    else:
        userga = f"❌ Notogri Javob\n\n✅Togri Javob: <b>{togri_variant['true']}-Variant</b> Edi"
        await message.answer(text=userga.capitalize())
        adminga = ""
        usergaa1 = f""
        for chegaraa in chegarasi:
            if achko["score"] != 0:
                await update_user_score_minus(chat_id=message.chat.id, miqdor=chegaraa["one_false_answer"],
                                              scoree=achko["score"])
            await update_user_falses(chat_id=message.chat.id, falses=falses["falses"])
            if chegaraa['savollar'] > nechi_savol['sovol']:
                kottami = True
            else:
                kottami = False
    if kottami == True:
        await message.answer(text=savolcha, reply_markup=options)
        await state.set_state('testing')
    else:
        result = await get_user_result(chat_id=message.chat.id)
        scoresi = await get_achko(chat_id=message.chat.id)
        usergaa1 = f"""
📊 Sizning Testdagi Natijalaringiz:

📕 Tanlangan Kitob: <b>{result["book"]}</b>
⭐️ Umumiy Ball: <b>{result["score"]}</b>
✅ Togri Tanlandi: <b>{result["trues"]}</b> Ta
❌ Notogri Tanlandi: <b>{result["falses"]}</b> Ta
📅 Topshirish Sanasi: <b>{result["date"]}</b>
"""
        user = await get_user(chat_id=message.chat.id)
        username = ""
        if user["username"] != "Mavjud Emas":
            username = f"@{user['username']}"
        else:
            username = f"Mavjud Emas"
        adminga = f"""
👤 Ism: <b>{user["name"]}</b>
👤 Familya: <b>{user["surname"]}</b>
🏛 Farzand Sinfi: <b>{user["farzand_sinf"]}</b>
👤 Farzandi: <b>{user["farzandi"]}</b>
📕 Tanlangan Kitob: <b>{result["book"]}</b>
⭐️ Umumiy Ball: <b>{result["score"]}</b>
✅ Togri Tanladi: <b>{result["trues"]}</b>
❌ Notogri Variantlar: <b>{result["falses"]}</b>
📅 Topshirish Sanasi: <b>{result["date"]}</b>
📞 Telefon Raqam: <b>{user["phone_number"]}</b>
👤 Telegram Username: <b>{username}</b>
"""

        adminlar = await get_all_admins()
        await write_results(user=user, username=username, result=result)
        for id1 in adminlar:
            await dp.bot.send_message(chat_id=int(id1["chat_id"]), text=adminga)
        await message.answer(text=usergaa1.capitalize(), reply_markup=user_main_menu)
        await state.finish()

@dp.message_handler(state='testing', text="B")
async def a_option_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    togrimi = await is_true(data=data, text1="B")
    togri_variant = await get_true(data=data)
    achko = await get_achko(chat_id=message.chat.id)
    nechi_savol = await get_savol(chat_id=message.chat.id)
    falses = await get_user_falses(chat_id=message.chat.id)
    trues = await get_user_trues(chat_id=message.chat.id)
    chegarasi = await chegara()
    savollar = await get_questions(subject=data["book"])
    savolla = list()
    for savol in savollar:
        savolla.append(savol["question"])
    random_savol = random.choice(savolla)
    variantla = await get_sovol1(subject=data["book"], savol=random_savol)
    savolcha = f"""
📄❓ Savol: {random_savol}
A Variant: {variantla["a"]}
B Variant: {variantla["b"]}
D Variant: {variantla["d"]}
"""
    await state.update_data({
        "savol": random_savol,
        "book": data["book"],
        "true": variantla['true']
    })
    await update_user_savol(chat_id=message.chat.id, savol=nechi_savol["sovol"])
    userga = f""
    kottami = ""
    if togrimi:
        userga = f"✅ Togri Javob"
        await message.answer(text=userga.capitalize())
        for chegaraa in chegarasi:
            await update_user_score(chat_id=message.chat.id, scoree=achko["score"], miqdor=chegaraa["one_true_answer"])
            if chegaraa['savollar'] > nechi_savol['sovol']:
                kottami = True
            else:
                kottami = False
        await update_user_trues(chat_id=message.chat.id, trues=trues["trues"])
    else:
        userga = f"❌ Notogri Javob\n\n✅Togri Javob: <b>{togri_variant['true']}-Variant</b> Edi"
        await message.answer(text=userga.capitalize())
        adminga = ""
        usergaa1 = f""
        for chegaraa in chegarasi:
            if achko["score"] != 0:
                await update_user_score_minus(chat_id=message.chat.id, miqdor=chegaraa["one_false_answer"],
                                              scoree=achko["score"])
            await update_user_falses(chat_id=message.chat.id, falses=falses["falses"])
            if chegaraa['savollar'] > nechi_savol['sovol']:
                kottami = True
            else:
                kottami = False
    if kottami == True:
        await message.answer(text=savolcha, reply_markup=options)
        await state.set_state('testing')
    else:
        result = await get_user_result(chat_id=message.chat.id)
        scoresi = await get_achko(chat_id=message.chat.id)
        usergaa1 = f"""
📊 Sizning Testdagi Natijalaringiz:

📕 Tanlangan Kitob: <b>{result["book"]}</b>
⭐️ Umumiy Ball: <b>{result["score"]}</b>
✅ Togri Tanlandi: <b>{result["trues"]}</b> Ta
❌ Notogri Tanlandi: <b>{result["falses"]}</b> Ta
📅 Topshirish Sanasi: <b>{result["date"]}</b>
"""
        user = await get_user(chat_id=message.chat.id)
        username = ""
        if user["username"] != "Mavjud Emas":
            username = f"@{user['username']}"
        else:
            username = f"Mavjud Emas"
        adminga = f"""
👤 Ism: <b>{user["name"]}</b>
👤 Familya: <b>{user["surname"]}</b>
🏛 Farzand Sinfi: <b>{user["farzand_sinf"]}</b>
👤 Farzandi: <b>{user["farzandi"]}</b>
📕 Tanlangan Kitob: <b>{result["book"]}</b>
⭐️ Umumiy Ball: <b>{result["score"]}</b>
✅ Togri Tanladi: <b>{result["trues"]}</b>
❌ Notogri Variantlar: <b>{result["falses"]}</b>
📅 Topshirish Sanasi: <b>{result["date"]}</b>
📞 Telefon Raqam: <b>{user["phone_number"]}</b>
👤 Telegram Username: <b>{username}</b>
"""

        adminlar = await get_all_admins()
        await write_results(user=user, username=username, result=result)
        for id1 in adminlar:
            await dp.bot.send_message(chat_id=int(id1["chat_id"]), text=adminga)
        await message.answer(text=usergaa1.capitalize(), reply_markup=user_main_menu)
        await state.finish()
@dp.message_handler(state='testing', text="D")
async def a_option_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    togrimi = await is_true(data=data, text1="D")
    togri_variant = await get_true(data=data)
    achko = await get_achko(chat_id=message.chat.id)
    nechi_savol = await get_savol(chat_id=message.chat.id)
    falses = await get_user_falses(chat_id=message.chat.id)
    trues = await get_user_trues(chat_id=message.chat.id)
    chegarasi = await chegara()
    savollar = await get_questions(subject=data["book"])
    savolla = list()
    for savol in savollar:
        savolla.append(savol["question"])
    random_savol = random.choice(savolla)
    variantla = await get_sovol1(subject=data["book"], savol=random_savol)
    savolcha = f"""
📄❓ Savol: {random_savol}
A Variant: {variantla["a"]}
B Variant: {variantla["b"]}
D Variant: {variantla["d"]}
"""
    await state.update_data({
        "savol": random_savol,
        "book": data["book"],
        "true": variantla['true']
    })
    await update_user_savol(chat_id=message.chat.id, savol=nechi_savol["sovol"])
    userga = f""
    kottami = ""
    if togrimi:
        userga = f"✅ Togri Javob"
        await message.answer(text=userga.capitalize())
        for chegaraa in chegarasi:
            await update_user_score(chat_id=message.chat.id, scoree=achko["score"], miqdor=chegaraa["one_true_answer"])
            if chegaraa['savollar'] > nechi_savol['sovol']:
                kottami = True
            else:
                kottami = False
        await update_user_trues(chat_id=message.chat.id, trues=trues["trues"])
    else:
        userga = f"❌ Notogri Javob\n\n✅Togri Javob: <b>{togri_variant['true']}-Variant</b> Edi"
        await message.answer(text=userga.capitalize())
        adminga = ""
        usergaa1 = f""
        for chegaraa in chegarasi:
            if achko["score"] != 0:
                await update_user_score_minus(chat_id=message.chat.id, miqdor=chegaraa["one_false_answer"],
                                              scoree=achko["score"])
            await update_user_falses(chat_id=message.chat.id, falses=falses["falses"])
            if chegaraa['savollar'] > nechi_savol['sovol']:
                kottami = True
            else:
                kottami = False

    if kottami == True:
        await message.answer(text=savolcha, reply_markup=options)
        await state.set_state('testing')
    else:
        result = await get_user_result(chat_id=message.chat.id)
        scoresi = await get_achko(chat_id=message.chat.id)
        usergaa1 = f"""
📊 Sizning Testdagi Natijalaringiz:

📕 Tanlangan Kitob: <b>{result["book"]}</b>
⭐️ Umumiy Ball: <b>{result["score"]}</b>
✅ Togri Tanlandi: <b>{result["trues"]}</b> Ta
❌ Notogri Tanlandi: <b>{result["falses"]}</b> Ta
📅 Topshirish Sanasi: <b>{result["date"]}</b>
"""
        user = await get_user(chat_id=message.chat.id)
        username = ""
        if user["username"] != "Mavjud Emas":
            username = f"@{user['username']}"
        else:
            username = f"Mavjud Emas"
        adminga = f"""
👤 Ism: <b>{user["name"]}</b>
👤 Familya: <b>{user["surname"]}</b>
🏛 Farzand Sinfi: <b>{user["farzand_sinf"]}</b>
👤 Farzandi: <b>{user["farzandi"]}</b>
📕 Tanlangan Kitob: <b>{result["book"]}</b>
⭐️ Umumiy Ball: <b>{result["score"]}</b>
✅ Togri Tanladi: <b>{result["trues"]}</b>
❌ Notogri Variantlar: <b>{result["falses"]}</b>
📅 Topshirish Sanasi: <b>{result["date"]}</b>
📞 Telefon Raqam: <b>{user["phone_number"]}</b>
👤 Telegram Username: <b>{username}</b>
"""

        adminlar = await get_all_admins()
        await write_results(user=user, username=username, result=result)
        for id1 in adminlar:
            await dp.bot.send_message(chat_id=int(id1["chat_id"]), text=adminga)
        await message.answer(text=usergaa1.capitalize(), reply_markup=user_main_menu)
        await state.finish()

@dp.message_handler(text="➕👤  O'quvchi qoshish")
async def add_student_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        userga = f"😊 Yangi O'quvchini Qaysi Sinfga Qoshmoqchisiz?"
        sinflar1 = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="❌ Bekor qilish")
                ]
            ], resize_keyboard=True, row_width=1
        )
        sinflar = await get_all_classes()
        for sinf in sinflar:
            sinflar1.insert(KeyboardButton(text=f"{sinf['class_number']}"))
        await message.answer(text=userga.capitalize(), reply_markup=sinflar1)
        await state.set_state("add_student")
    else:
        userga = f"😕 Kechirasiz Siz Adminlik Huquqiga Ega Emassiz!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(state="add_student")
async def add_student_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "classi": message.text
    })
    userga = f"{message.text}larning Qaysi Guruxiga?"
    await state.set_state("new_student_group")
    await message.answer(text=userga.capitalize(), reply_markup=cancel)

@dp.message_handler(state="new_student_group")
async def add_student_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "class_guruxi": message.text
    })
    userga = f"👤 Yangi Oquvchini Ism Familyasini Kiriting"
    await state.set_state("adding_student")
    await message.answer(text=userga.capitalize(), reply_markup=cancel)

@dp.message_handler(state="adding_student")
async def new_student_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "full_name": message.text
    })
    data = await state.get_data()
    if await add_student(data=data):
        userga = f"✅🥳 Yangi Oquvchi Qoshildi"
    else:
        userga = f"Xato"
    await state.finish()
    await message.answer(text=userga.capitalize(), reply_markup=admins_panel)

@dp.message_handler(text="👤📊 Ota onalar natijalari")
async def student_results(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        resultatlar = await get_all_parent_results(id_nomer=1)
        if resultatlar:
            await state.update_data({
                "id_nomer": 1
            })
            adminga = f""
            username = f""
            for resultat in resultatlar:
                user = await get_user(chat_id=int(resultat["chat_id"]))
                if resultat["username"] != "Mavjud Emas":
                    username = f"@{resultat['username']}"
                else:
                    username = f"Mavjud Emas"
                adminga = f"""
👤 Ism: <b>{resultat["name"]}</b>
👤 Familya: <b>{resultat["surname"]}</b>
📞 Telefon Raqam: <code>{resultat["phone_number"]}</code>
©️ Username: <b>{username}</b>
🙍‍♂️ Farzandi: <b>{user["farzandi"]}</b>
🤵‍♂️🧕 Ota\Ona: <b>{resultat["who"]}</b>
🙍‍♂️🏫 Farzandining Sinfi: <b>{resultat["farzand_sinfi"]}</b>
🙍‍♂️👥Farzand Sinf Guruxi: <b>{resultat["farzand_sinfi_guruxi"]}</b>
📕 Kitob: <b>{resultat["book"]}</b>
⭐️ Ball: <b>{resultat["score"]}</b>
✅ Togri Javoblar: <b>{resultat["trues"]}</b>
❌ Notogri Javoblar: <b>{resultat["falses"]}</b>
📅 Topshirish Vaqti <b>{resultat["date"]}</b>
🆔 Chat Id Raqami: <code>{resultat["chat_id"]}</code>
"""
            await message.answer(text=adminga, reply_markup=pagination)
        else:
            userga = f"Ota onalar natijalari Mavjud Emas"
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} Siz Adminlik Huquqiga Ega Emassiz!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.callback_query_handler(text="right")
async def right_handler(call: types.CallbackQuery, state: FSMContext):
    number = await state.get_data()
    await state.update_data({
        "id_nomer": number["id_nomer"] + 1
    })
    data = await state.get_data()
    adminga = f""
    username = f""
    resultatlar = await get_all_parent_results(id_nomer=data["id_nomer"])
    if resultatlar:
        for resultat in resultatlar:
            user = await get_user(chat_id=int(resultat["chat_id"]))
            if resultat["username"] != "Mavjud Emas":
                username = f"@{resultat['username']}"
            else:
                username = f"Mavjud Emas"
            adminga = f"""
👤 Ism: <b>{resultat["name"]}</b>
👤 Familya: <b>{resultat["surname"]}</b>
📞 Telefon Raqam: <code>{resultat["phone_number"]}</code>
©️ Username: <b>{username}</b>
🙍‍♂️ Farzandi: <b>{user["farzandi"]}</b>
🤵‍♂️🧕 Ota\Ona: <b>{resultat["who"]}</b>
🙍‍♂️🏫 Farzandining Sinfi: <b>{resultat["farzand_sinfi"]}</b>
🙍‍♂️👥Farzand Sinf Guruxi: <b>{resultat["farzand_sinfi_guruxi"]}</b>
📕 Kitob: <b>{resultat["book"]}</b>
⭐️ Ball: <b>{resultat["score"]}</b>
✅ Togri Javoblar: <b>{resultat["trues"]}</b>
❌ Notogri Javoblar: <b>{resultat["falses"]}</b>
📅 Topshirish Vaqti <b>{resultat["date"]}</b>
🆔 Chat Id Raqami: <code>{resultat["chat_id"]}</code>
"""
        await call.message.delete()
        await call.message.answer(text=adminga, reply_markup=pagination)
    else:
        await call.answer(text="❌ Bundan Keyin Natijalar Mavjud Emas", show_alert=True)
        await call.message.delete()


@dp.callback_query_handler(text="left")
async def right_handler(call: types.CallbackQuery, state: FSMContext):
    number = await state.get_data()
    await state.update_data({
        "id_nomer": number["id_nomer"] - 1
    })
    data = await state.get_data()
    adminga = f""
    username = f""
    print(data["id_nomer"])
    resultatlar = await get_all_parent_results(id_nomer=data["id_nomer"])
    if resultatlar:
        for resultat in resultatlar:
            user = await get_user(chat_id=int(resultat["chat_id"]))
            if resultat["username"] != "Mavjud Emas":
                username = f"@{resultat['username']}"
            else:
                username = f"Mavjud Emas"
            adminga = f"""
👤 Ism: <b>{resultat["name"]}</b>
👤 Familya: <b>{resultat["surname"]}</b>
📞 Telefon Raqam: <code>{resultat["phone_number"]}</code>
©️ Username: <b>{username}</b>
🙍‍♂️ Farzandi: <b>{user["farzandi"]}</b>
🤵‍♂️🧕 Ota\Ona: <b>{resultat["who"]}</b>
🙍‍♂️🏫 Farzandining Sinfi: <b>{resultat["farzand_sinfi"]}</b>
🙍‍♂️👥Farzand Sinf Guruxi: <b>{resultat["farzand_sinfi_guruxi"]}</b>
📕 Kitob: <b>{resultat["book"]}</b>
⭐️ Ball: <b>{resultat["score"]}</b>
✅ Togri Javoblar: <b>{resultat["trues"]}</b>
❌ Notogri Javoblar: <b>{resultat["falses"]}</b>
📅 Topshirish Vaqti <b>{resultat["date"]}</b>
🆔 Chat Id Raqami: <code>{resultat["chat_id"]}</code>
"""
        await call.message.delete()
        await call.message.answer(text=adminga, reply_markup=pagination)
    else:
        await call.answer(text="❌ Bundan Oldin Natijalar Mavjud Emas", show_alert=True)
        await call.message.delete()



@dp.message_handler(text="➕📝 Savol qoshish")
async def add_question_to_class_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        userga = f"😊 Qaysi Kitobga Savol Qoshmoqchisiz?"
        books_key = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="❌ Bekor qilish")
                ]
            ], resize_keyboard=True, row_width=1
        )
        bookss = await get_all_book()
        for book in bookss:
            books_key.insert(KeyboardButton(text=book["books"]))
        await message.answer(text=userga.capitalize(), reply_markup=books_key)
        await state.set_state("admin_state")
    else:
        userga = f"😕 Kechirasiz Siz Adminlik Huquqiga Ega Emassiz!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(state="admin_state")
async def select_subjects_admin_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        await state.update_data({
            "book": message.text
        })
        userga = f"😊 Savolingizni Kiriting!"
        await message.answer(text=userga.capitalize(), reply_markup=cancel)
        await state.set_state("get_sovoll1")
    else:
        userga = f"😕 Kechirasiz Siz Adminlik Huquqiga Ega Emassiz!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)
        await state.finish()

@dp.message_handler(state="get_sovoll1")
async def get_sovol_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if await get_questions_security(subject=data["book"], question=message.text):
        userga = f"Kechirasiz {data['book']}-Kitobida Bunday Savol Qoshilgan!"
        await state.finish()
        await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
    else:
        userga = f"A) Variant Uchun Javob Kiriting."
        await state.update_data({
            "question": message.text.capitalize(),
            "subject_name": data["book"]
        })
        await message.answer(text=userga.capitalize(), reply_markup=ReplyKeyboardRemove())
        await state.set_state("a_variant")

@dp.message_handler(state="a_variant")
async def a_variant_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "a": message.text
    })
    userga = f"B) Variant Uchun Javob Kiriting!"
    await message.answer(text=userga.capitalize())
    await state.set_state("b_variant")

@dp.message_handler(state="b_variant")
async def a_variant_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "b": message.text
    })
    userga = f"D) Variant Uchun Javob Kiriting!"
    await message.answer(text=userga.capitalize())
    await state.set_state("d_variant")

@dp.message_handler(state="d_variant")
async def a_variant_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "d": message.text
    })
    userga = f"Tog'ri Variantni Tanlang!"
    await message.answer(text=userga.capitalize(), reply_markup=options)
    await state.set_state("true_variant")

@dp.message_handler(text=f"📕➕ Kitob qoshish")
async def add_subject_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        userga = f"😊 Qoshmoqchi Bolgan Yangi Kitobingizni Nomini Kiriting!"
        await message.answer(text=userga.capitalize(), reply_markup=cancel)
        await state.set_state("new_book")
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(state="new_book")
async def select_class_handler(message: types.Message, state: FSMContext):
    if await is_admin(chat_id=message.chat.id):
        try:
            await add_new_book(book_name=message.text)
            userga = f"🥳 Yangi Kitobingiz Kitoblar Bolimiga Qoshildi!"
            await message.answer(text=userga.capitalize(), reply_markup=admins_panel)
            await state.finish()
        except Exception as e:
            await message.answer(text="Kechirasiz Botda Xatolik Yuz Berdi Iltimos Keynroq Urinib Koring")
            await dp.bot.send_message(chat_id=-1002075245072, text=f"{e} Line 1081 Bot Yuksalish Kitobxonlik")
            return False
    else:
        userga = f"😕 Kechirasiz: {message.from_user.full_name} \nSiz Admin Huquqiga Ega Emassiz Bu Funksiya Faqat Adminlar Uchun!"
        await message.answer(text=userga.capitalize(), reply_markup=user_main_menu)

@dp.message_handler(state='test_will')
async def get_class_handler(message: types.Message, state: FSMContext):
    xabar = message.text
    data = await state.get_data()
    kitobmi = await get_book(book=xabar)
    if kitobmi:
        userga = f"😊 {xabar} Kitobidan Test Ishlashga Tayyormisiz?"
        await state.update_data({
            "book": xabar
        })
        await message.answer(text=userga.capitalize(), reply_markup=yes_no)
        await state.set_state("user_sure")