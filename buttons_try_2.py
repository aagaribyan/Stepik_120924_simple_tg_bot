from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)

import configparser

from aiogram.utils.keyboard import ReplyKeyboardBuilder


# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# создание объектов бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# инициализация объекта билдера
kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# создание списка с кнопками (например, 10 кнопок)
buttons: list[KeyboardButton] = [KeyboardButton(text='Кнопка '+str(i+1)) for i in range(10)]

# добавление кнопок методом билдера
kb_builder.row(*buttons, width=3)

# добавление дополнительных кнопок (не затирает уже добавленные)
buttons2: list[KeyboardButton] = [KeyboardButton(text='Кнопка '+str(10+i+1)) for i in range(6)]
kb_builder.row(*buttons2, width=4)
# можно это сделать ещё и методом .add(), но он как-то не очень
# впрочем, его можно подправить с помощью .adjust(), но вряд ли они мне понадобятся


# хендлер на команду /start с отправкой в чат клавиатуры
@dp.message(CommandStart())
async def process_start_command(message: Message):
    # await message.answer(text='Чего кошки бояться больше?', reply_markup=keyboard)

    # передача клавиатуры методом as_markup() как аргумента
    await message.answer(text='Пример клавиатуры полученной с помощью билдера',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Text(text='/help'))
async def process_help_command(message: Message):
    await message.answer('/start - запуск бота\n'
                         'Данный бот исключетильно тестовый для изучения \n'
                         'возможности добавления собственных кнопок')


if __name__ == '__main__':
    dp.run_polling(bot)
