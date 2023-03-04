from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)

import configparser


# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# создание объектов бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# создание объектов кнопок
button_1: KeyboardButton = KeyboardButton(text='Собак 🦮')
button_2: KeyboardButton = KeyboardButton(text='Огурцов 🥒')

# создание объекта клавиатуры, с добавлением в неё кнопок
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
                                                    resize_keyboard=True,  # чтобы кнопки не были такими большими
                                                    one_time_keyboard=True)  # вместо reply_markup



# хендлер на команду /start с отправкой в чат клавиатуры
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Чего кошки бояться больше?', reply_markup=keyboard)

# хендлер для ответа "Собак" с удалением клавиатуры после ответа
@dp.message(Text(text='Собак 🦮'))
async def process_dog_answer(message: Message):
    await message.answer(text='Да, несомненно, кошки бояться собак. '
                                'Но вы видели как они бояться огурцов?')  # , reply_markup=ReplyKeyboardRemove)

# хендлер для ответа "Огурцов" с удалением клавиатуры после ответа
@dp.message(Text(text='Огурцов'))
async def process_cucmber_answer(message: Message):
    await message.answer(text='Да, иногда кажется, что огурцов '
                                'кошки бояться больше')  # , reply_markup=ReplyKeyboardRemove)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Text(text='/help'))
async def process_help_command(message: Message):
    await message.answer('/start - запуск бота\n'
                         'Данный бот исключетильно тестовый для изучения \n'
                         'возможности добавления собственных кнопок')


if __name__ == '__main__':
    dp.run_polling(bot)
