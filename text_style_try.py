from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import configparser

# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# создание объектов бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# хендлер на команду '/start'
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Привет!\n\nЯ бот, демонстрирующий '
                              'как работает разметка. Отправь команду '
                              'из списка ниже:\n\n'
                              '/html - пример разметки с помощью HTML\n'
                              '/markdownv2 - пример разметки с помощью MarkdownV2\n'
                              '/noformat - пример с разметкой, но без указания '
                              'параметра parse_mode')


# хендлер на команду '/help'
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Привет!\n\nЯ бот, демонстрирующий '
                              'как работает разметка. Отправь команду '
                              'из списка ниже:\n\n'
                              '/html - пример разметки с помощью HTML\n'
                              '/markdownv2 - пример разметки с помощью MarkdownV2\n'
                              '/noformat - пример с разметкой, но без указания '
                              'параметра parse_mode')


# хендлер на команду '/html'
@dp.message(Command(commands='html'))
async def process_html_command(message: Message):
    await message.answer(text='Это текст, демонстрирующий '
                              'как работает HTML-разметка:\n\n'
                              '<b>Это жирный текст</b>\n'
                              '<i>Это наклонный текст</i>\n'
                              '<u>Это подчеркнутый текст</u>\n'
                              '<span class="tg-spoiler">А это спойлер</span>\n\n'
                              'Чтобы еще раз посмотреть список доступных команд - '
                              'отправь команду /help',
                         parse_mode='HTML')


# хендлер на команду '/markdownv2'
@dp.message(Command(commands='markdownv2'))
async def process_markdownv2_command(message: Message):
    await message.answer(text='Это текст, демонстрирующий '
                              'как работает MarkdownV2\-разметка:\n\n'
                              '*Это жирный текст*\n'
                              '_Это наклонный текст_\n'
                              '__Это подчеркнутый текст__\n'
                              '||А это спойлер||\n\n'
                              'Чтобы еще раз посмотреть список доступных команд \- '
                              'отправь команду /help',
                         parse_mode='MarkdownV2')


# хендлер на команду '/noformat'
@dp.message(Command(commands='noformat'))
async def process_noformat_command(message: Message):
    await message.answer(text='Это текст, демонстрирующий '
                              'как отображается текст, если не указать '
                              'параметр parse_mode:\n\n'
                              '<b>Это мог бы быть жирный текст</b>\n'
                              '_Это мог бы быть наклонный текст_\n'
                              '<u>Это мог бы быть подчеркнутый текст</u>\n'
                              '||А это мог бы быть спойлер||\n\n'
                              'Чтобы еще раз посмотреть список доступных команд - '
                              'отправь команду /help')


# хендлер на любые сообщения, кроме учтенных команд
@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Я даже представить себе не могу, '
                              'что ты имеешь в виду\n\n'
                              'Чтобы посмотреть список доступных команд - '
                              'отправь команду /help')


# запуск поллинга
if __name__ == '__main__':
    dp.run_polling(bot)