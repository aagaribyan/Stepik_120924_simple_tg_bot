from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import configparser


# токен
config = configparser.ConfigParser()
config.read('.ini')
API_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# создание объекта бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

LEXICON: dict[str, str] = {'but_1': 'Кнопка 1',
                           'but_2': 'Кнопка 2',
                           'but_3': 'Кнопка 3',
                           'but_4': 'Кнопка 4',
                           'but_5': 'Кнопка 5',
                           'but_6': 'Кнопка 6',
                           'but_7': 'Кнопка 7'}

BUTTONS: dict[str, str] = {'btn_1': '1',
                           'btn_2': '2',
                           'btn_3': '3',
                           'btn_4': '4',
                           'btn_5': '5',
                           'btn_6': '6',
                           'btn_7': '7'}


# функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int, *args: str, last_btn: str | None = None, **kwargs: str) -> InlineKeyboardMarkup:
    # инициализация билдера
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # инициализация списка для кнопок
    buttons: list[InlineKeyboardButton] = []

    # заполнение списка кнопок из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                                                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text,
                                                callback_data=button))

    # распаковка списка кнопок в билдер
    kb_builder.row(*buttons, width=width)
    # добавление в билдер последней кнопки, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(text=last_btn,
                                            callback_data='last_btn'))

    # возвращение объекта инлайн-клавиатуры
    return kb_builder.as_markup()


# хендлер на команду /start с отправкой в чат клавиатуры
@dp.message(CommandStart())
async def process_start_command(message: Message):
    # keyboard = create_inline_kb(2, 'but_1', 'but_3', 'but_7')
    # keyboard = create_inline_kb(2, btn_tel = 'Телефон', btn_email = 'email', btn_website = 'Web-сайт', btn_vk = 'VK', btn_tgbot = 'Наш телеграм-бот')
    keyboard = create_inline_kb(4, last_btn='Последняя кнопка', **BUTTONS)

    await message.answer(text='Получившаяся клавиатура',
                         reply_markup=keyboard)

if __name__ == '__main__':
    dp.run_polling(bot)