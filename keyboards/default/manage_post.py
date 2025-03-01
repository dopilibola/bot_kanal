from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

post_callback = CallbackData("create_post", "action")

confirmation_keyboard = ReplyKeyboardMarkup(
    keyboard=[  
        [
            KeyboardButton(text='chop etish', callback_data=post_callback.new(action="post")),
            KeyboardButton(text='Obunani tekshiriash', callback_data=post_callback.new(action="cancel")),
        ],
    ],
)