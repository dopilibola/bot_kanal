import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from data.config import CHANNELS
from utils.misc import sub
from loader import bot

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message: 
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
            
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else: 
            return 
        logging.info(user)
        result = "Salom, <b>foydalanuvchi</b>"

        # result = "botdan foydalanish uchun quydagi kanallarga obuna bolish kere \n"
        final_status = True
        for channel in CHANNELS:
            status = await sub.check(user_id=user,
                                              channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)

            if not status:
                invite_link = await channel.export_invite_link()
                result += (f"< href='{invite_link}' > {channel.title}</a>\n")
        
        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()