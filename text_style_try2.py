from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

import configparser


# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# создание объектов бота и диспетчера
# в этом варианте parse_mode указываем один раз и он будет применен ко всем отправляемым сообщениям
bot: Bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher()


# хендлер на команду '/start'
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Привет!\n\nЯ бот, демонстрирующий '
                             'как работает HTML-разметка. Отправь команду '
                             'из списка ниже:\n\n'
                             '/bold - жирный текст\n'
                             '/italic - наклонный текст\n'
                             '/underline - подчеркнутый текст\n'
                             '/spoiler - спойлер')


# хендлер на команду '/help'
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Я бот, демонстрирующий '
                             'как работает HTML-разметка. Отправь команду '
                             'из списка ниже:\n\n'
                             '/bold - жирный текст\n'
                             '/italic - наклонный текст\n'
                             '/underline - подчеркнутый текст\n'
                             '/spoiler - спойлер')


# хендлер на команду '/bold
@dp.message(Command(commands='bold'))
async def process_bold_command(message: Message):
    await message.answer(text='<b>Это текст, демонстрирующий '
                             'как работает HTML-разметка, '
                             'делающая текст жирным.\n\n'
                             'Чтобы еще раз посмотреть список доступных команд - '
                             'отправь команду /help</b>')


# хендлер на команду '/italic'
@dp.message(Command(commands='italic'))
async def process_italic_command(message: Message):
    await message.answer(text='<i>Это текст, демонстрирующий '
                             'как работает HTML-разметка, '
                             'делающая текст наклонным.\n\n'
                             'Чтобы еще раз посмотреть список доступных команд - '
                             'отправь команду /help</i>')


# хендлер на команду '/underline'
@dp.message(Command(commands='underline'))
async def process_underline_command(message: Message):
    await message.answer(text='<u>Это текст, демонстрирующий '
                             'как работает HTML-разметка, '
                             'делающая текст подчеркнутым.\n\n'
                             'Чтобы еще раз посмотреть список доступных команд - '
                             'отправь команду /help</u>')


# хендлер на команду '/spoiler'
@dp.message(Command(commands='spoiler'))
async def process_spoiler_command(message: Message):
    await message.answer(text='<tg-spoiler>Это текст, демонстрирующий '
                             'как работает HTML-разметка, '
                             'убирающая текст под спойлер.\n\n'
                             'Чтобы еще раз посмотреть список доступных команд - '
                             'отправь команду /help</tg-spoiler>')


# хендлер на команду "/strike"
@dp.message(Command(commands='strike'))
async def process_strike_command(message: Message):
    await message.answer(text='<s>Это зачеркнутый текст</s>\n\n'
                             '<strike>И это зачеркнутый текст</strike>\n\n'
                             '<del>И это тоже зачеркнутый текст</del>')


# хендлер на остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Я даже представить себе не могу, '
                             'что ты имеешь в виду\n\n'
                             'Чтобы посмотреть список доступных команд - '
                             'отправь команду /help')


# запуск поллинга
if __name__ == '__main__':
    dp.run_polling(bot)