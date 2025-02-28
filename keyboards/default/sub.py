from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

check_button = ReplyKeyboardMarkup(
    keyboard=[  
        [
            KeyboardButton(text='Obunani tekshiriash', callback_data="check_subs"),
        ],
    ],
    resize_keyboard=True
)