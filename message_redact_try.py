from aiogram import Bot, Dispatcher
from aiogram.types import (Message, CallbackQuery,
                            InlineKeyboardButton, InlineKeyboardMarkup,
                            InputMediaAudio, InputMediaDocument,
                            InputMediaPhoto, InputMediaVideo)
from aiogram.filters import CommandStart, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

import configparser

# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# создание объектов бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


LEXICON: dict[str, str] = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'video': '🎬 Видео',
    'document': '📑 Документ',
    'voice': '📢 Голосовое сообщение',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': '-//-',
    'photo_id2': '-//-',
    'voice_id1': '-//-',
    'voice_id2': '-//-',
    'audio_id1': '-//-',
    'audio_id2': '-//-',
    'document_id1': '-//-',
    'document_id2': '-//-',
    'video_id1': '-//-',
    'video_id2': '-//-'
}


# функция для генерации клавиатур с инлайн-кнопками
def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    # инициализация билдера
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # инициализация списка для кнопок
    buttons: list[InlineKeyboardButton] = []

    # заполенение списка кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # распаковка списка с кнопками в билдер методом row с параметром width
    kb_builder.row(*buttons, width=width)

    # воврат объекта инлайн-клавиатуры
    return kb_builder.as_markup()


# хендлер на команду '/start'
@dp.message(CommandStart)
async def process_start_command(message: Message):
    markup = get_markup(2, 'photo')
    await message.answer(text=LEXICON['photo_id1'],
                         reply_markup=markup)


# хендлер на наджатие инлайн-кнопки
@dp.callback_query(Text(text=['audio','video','document','photo']))
async def process_button_press(callback: CallbackQuery):
    markup = get_markup(2, 'photo')
    try:
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(media=LEXICON['photo_id2'],
                                                           caption='Это фото 2'),
                                     reply_markup=markup)
    except TelegramBadRequest:
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(media=LEXICON['photo_id1'],
                                                           caption='Это фото 1'),
                                     reply_markup=markup)



# хендлер на остальные сообщения
@dp.message()
async def send_echo(message: Message):
    print(message)
    await message.answer(text='Не понимаю')
