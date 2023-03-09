from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import configparser


# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# объекты инлайн-кнопок
url_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Курс "Телеграм-боты на Python и AIOgram"',
    url='https://stepik.org/120924')
url_button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Документация Telegram Bot API',
    url='https://core.telegram.org/bots/api')

# кнопки со ссылками в сам телешрам
group_name = 'aiogram_stepik_course'
url_button_group: InlineKeyboardButton = InlineKeyboardButton(
    text='Группа "Телеграм-боты на AIOgram"',
    url=f'tg://resolve?domain={group_name}')

user_id = 742654337  # мой Id
url_button_user: InlineKeyboardButton = InlineKeyboardButton(
    text='Автор бота',
    url=f'tg://user?id={user_id}')  # либо https://t.me/armen_garibyan

channel_name = 'toBeAnMLspecialist'
url_button_channel: InlineKeyboardButton = InlineKeyboardButton(
    text='Канал "Стать специалистом по машинному обучению"',
    url=f'https://t.me/{channel_name}')

# объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1],
                     [url_button_2],
                     [url_button_group],
                     [url_button_user],
                     [url_button_channel]])

# хендлер на команду '/start' с отправкой в чат клавиатуры с url-кнопками
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Это инлайн-кнопки с параметром "url"', reply_markup=keyboard)


if __name__ == '__main__':
    dp.run_polling(bot)
