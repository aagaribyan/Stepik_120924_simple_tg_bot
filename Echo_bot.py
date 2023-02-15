from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import ContentType
from aiogram import F

import configparser
from re import split as rsplit




config = configparser.ConfigParser()
config.read('token.ini')
API_TOKEN = config['AAGaribyanBot']['Token']

# создаем объекты Бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# этот хендлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет,\n Я Эхо-бот, напиши мне что-нибудь.')
    # аналог await bot.send_message(message.chat.id, message.text)
    # можно отвечать и не в тот же чат с помощью await bot.send_message(chat_id='ID или название чата', text='текст')

# этот хендлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе последнее твое предложение')
'''
# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    # print(message)
    await message.answer_photo(message.photo[0].file_id)  # reply_photo(message.photo[0].file_id)
    # Для аудио используется message.answer_audio(...), для видео - message.answer_video(...), для стикеров message.answer_sticker(...)
    # не забывать еще указывать соответствующий тип контента в качестве фильтра при регистрации хэндлеров

async def send_sticker_echo(message: Message):
    await message.answer_sticker(message.sticker.file_id)
'''


# этот хендлер будет срабатывать на любые текстовые сообщения, кроме команд /start и /help
#@dp.message(ContentType.TEXT)
#async def send_text_echo(message: Message):
#    await message.answer(text=rsplit("\. |\.\.\. |\? |\! ", message.text)[-1])
        # reply(text=message.text.split('. ')[-1])

@dp.message()
async def send_copy(message: Message):  # send_message(message: Message):
    try:
        if message.text:
            await message.answer(text=rsplit("\. |\.\.\. |\? |\! ", message.text)[-1])
        else:
            await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается '
                                 'методом send_copy')


# если без декораторов, то вот так
# Регистрируем хэндлеры
# dp.message.register(process_start_command, Command(commands=["start"]))
# dp.message.register(process_help_command, Command(commands=['help']))
# dp.message.register(send_photo_echo, F.photo)  # (send_photo_echo, F.content_type == ContentType.PHOTO)
# dp.message.register(send_sticker_echo, F.content_type == ContentType.STICKER)
#dp.message.register(send_message)




if __name__ == '__main__':
    dp.run_polling(bot)
