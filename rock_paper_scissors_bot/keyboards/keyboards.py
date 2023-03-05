from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# ------ Создание клавиатуры через ReplyKeyboardBuilder ----- #

# создание кнопок с ответами согласия и отказа
button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

# инициализация билдера для клавиатуры с кнопками согласия и отказа
yes_no_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# добавление кнопок в билдер
yes_no_kb_builder.row(button_yes, button_no, width=2)

# создание клавиатуры с кнопками согласия и отказа
yes_no_kb = yes_no_kb_builder.as_markup(one_tine_keyboard=True, resize_keyboard=True)


# ----- Создание игровой клавиатуры без использования билдера ----- #

# создание кнопок игровой клавиатуры
button_1: KeyboardButton = KeyboardButton(text=LEXICON_RU['rock'])
button_2: KeyboardButton = KeyboardButton(text=LEXICON_RU['scissors'])
button_3: KeyboardButton = KeyboardButton(text=LEXICON_RU['paper'])
button_4: KeyboardButton = KeyboardButton(text=LEXICON_RU['reptile'])
button_5: KeyboardButton = KeyboardButton(text=LEXICON_RU['Spok'])

# игровая клавиатура
game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1, button_2, button_3],
                                              [button_4, button_5]],
                                    resize_keyboard=True)
