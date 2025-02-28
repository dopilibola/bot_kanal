import logging
from aiogram import types
from data.config import CHANNELS
from keyboards.default.sub import check_button
from loader import bot, dp
from utils.misc import sub


async def check_subscriptions(user_id):
    """ Foydalanuvchi barcha kanallarga obuna bo'lganligini tekshiradi. """
    not_subscribed = []
    
    for channel in CHANNELS:
        status = await sub.check(user_id, channel)
        if not status:
            not_subscribed.append(channel)

    return not_subscribed


@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    user_id = message.from_user.id
    not_subscribed = await check_subscriptions(user_id)

    if not_subscribed:  # Agar foydalanuvchi barcha kanallarga obuna bo'lmagan bo'lsa
        channels_format = ""
        for channel in not_subscribed:
            chat = await bot.get_chat(channel)
            try:
                invite_link = await chat.export_invite_link()
                channels_format += f"<a href='{invite_link}'> {chat.title}</a>\n"
            except Exception as e:
                logging.error(f"Link olishda xatolik: {e}")
                channels_format += f"{chat.title} (havola yo'q)\n"

        await message.answer(f"Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling: \n"
                             f"{channels_format}",
                             reply_markup=check_button,
                             disable_web_page_preview=True)
    else:
        await message.answer("Siz barcha kanallarga obuna bo'lgansiz! Botdan foydalanishingiz mumkin.")


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    user_id = call.from_user.id
    not_subscribed = await check_subscriptions(user_id)

    if not_subscribed:  # Agar foydalanuvchi hali ham obuna bo'lmagan bo'lsa
        result = ""
        for channel in not_subscribed:
            chat = await bot.get_chat(channel)
            try:
                invite_link = await chat.export_invite_link()
                result += (f"<b>{chat.title}</b> kanalga obuna bo'lmagansiz. "
                           f"<a href='{invite_link}'>Obuna bo'lish</a>\n\n")
            except Exception as e:
                logging.error(f"Link olishda xatolik: {e}")
                result += f"{chat.title} kanalga obuna bo'lmagansiz (havola yo'q)\n\n"

        await call.message.answer(result, disable_web_page_preview=True)
    else:
        await call.message.answer("Siz barcha kanallarga obuna bo'lgansiz! Botdan foydalanishingiz mumkin.")
