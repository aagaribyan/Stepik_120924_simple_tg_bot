from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

import configparser


# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# объекты инлайн-кнопок
big_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed')

big_button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 2',
    callback_data='big_button_2_pressed')

# объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_1],
                     [big_button_2]])


# хендлер на команду '/start' с отправкой в чат клавиатуры с callback-кнопками
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Это callback-кнопки', reply_markup=keyboard)


# хендлер апдейта типа CallbackQuery с data 'big_button_1_pressed' или 'big_button_2_pressed'
# @dp.callback_query(Text(text=['big_button_1_pressed', 'big_button_2_pressed']))
# async def process_buttons_press(callback: CallbackQuery):
#     await callback.answer()  # считается хорошим тоном отвечать на каждое нажатие callback-кнопки,
                             # чтобы бот не "зависал в задумчивости"

# хендлер апдейта типа CallbackQuery с data 'big_button_1_pressed'
@dp.callback_query(Text(text=['big_button_1_pressed']))
async def process_buttons_1_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1':
        await callback.message.edit_text(text='Была нажата БОЛЬШАЯ КНОПКА 1',
                                         reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(text='Нажата кнопка 1',
                              show_alert=True)


# хендлер апдейта типа CallbackQuery с data 'big_button_2_pressed'
@dp.callback_query(Text(text=['big_button_2_pressed']))
async def defprocess_buttons_2_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 2':
        await callback.message.edit_text(text='Была нажата БОЛЬШАЯ КНОПКА 2',
                                         reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(text='Нажата кнопка 2')


if __name__ == '__main__':
    dp.run_polling(bot)
