from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS, CHANNELS
from keyboards.default.manage_post import confirmation_keyboard, post_callback
from loader import dp, bot
from states.newpost import NewPost


@dp.message_handler(Command("yangi_post"))
async def create_post(message: Message):
    await message.answer("Chop etish uchun post yuboring")
    await NewPost.NewMessage.set()
    

@dp.message_handler(state=NewPost.NewMessage)
async def enter_message(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer("Postni tekshirish uchun yuboraymi?", reply_markup=confirmation_keyboard)
    await NewPost.next()


@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data: 
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post adminga yuborildi")

    for admin in ADMINS:  # Bir nechta admin bo'lsa
        await bot.send_message(admin, f"Foydalanuvchi {mention} quyidagi postni chop etmoqchi:")
        await bot.send_message(admin, text, parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi")


@dp.callback_query_handler(post_callback.filter(action="post"))
async def approve_post(call: CallbackQuery):
    if str(call.from_user.id) not in ADMINS:
        return await call.answer("Sizga ruxsat berilmagan!", show_alert=True)

    await call.answer("Siz postni chop etishga ruxsat berdingiz", show_alert=True)
    target_channel = CHANNELS[0]
    
    message = call.message
    await bot.send_message(target_channel, message.text, parse_mode="HTML")


@dp.callback_query_handler(post_callback.filter(action="cancel"))
async def decline_post(call: CallbackQuery):
    if str(call.from_user.id) not in ADMINS:
        return await call.answer("Sizga ruxsat berilmagan!", show_alert=True)

    await call.answer("Post rad etildi", show_alert=True)
    await call.message.edit_reply_markup()
