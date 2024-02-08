from aiogram import Bot, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from data.config import CHANNELS
from keyboards.inline.inline_keyboards import channels
async def check(user_id, channel_id):
    bot = Bot.get_current()
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel_id)
    return member.is_chat_member()

class CheckSub(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        user_id = 0
        subscribed = True
        if update.message:
            user_id = update.message.chat.id
        if update.callback_query:
            user_id = update.callback_query.message.chat.id
            if update.callback_query.data == "check":
                user_id = update.callback_query.message.chat.id
                for channel_id in CHANNELS:
                    status = await check(user_id=int(user_id), channel_id=-int(channel_id))
                    if status == False:
                        subscribed = False
                if subscribed == False:
                    if update.message:
                        await update.message.answer(
                            text="😊 Yuksalish Maktabi Botidan Foydalanish Uchun Kanallarga Obuna Boling!",
                            reply_markup=channels)
                    else:
                        await update.callback_query.answer(text="❌ Kanallarga Toliq Obuna Boling!", show_alert=True)
                    raise CancelHandler()
                else:
                    await update.callback_query.message.delete()
                    await update.callback_query.message.answer(text="✅ /start Buyrugini Kiriting")
                    return
        for channel_id in CHANNELS:
            status = await check(user_id=int(user_id), channel_id=-int(channel_id))
            if status == False:
                subscribed = False
        if subscribed == False:
            if update.message:
                await update.message.answer(text="😊 Yuksalish Maktabi Botidan Foydalanish Uchun Kanallarga Obuna Boling!",reply_markup=channels)
            else:
                await update.callback_query.answer(text="❌ Kanallarga Toliq Obuna Boling!", show_alert=True)
            raise CancelHandler()
        else:

            return