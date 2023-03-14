from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.file_handling import book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    # объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # наполнение клавиатуры кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(text=f'{button} - {book[button][:80]}',
                                            callback_data=str(button)))

    # кнопки Редактировать и Отменить в конце клавиатуры
    kb_builder.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'],
                                        callback_data='edit_bookmarks'),
                   InlineKeyboardButton(text=LEXICON['cancel'],
                                        callback_data='cancel'),
                   width=2)

    return kb_builder.as_markup()

def create_edit_keyboard(*args: int) -> InlineKeyboardBuilder:
    # объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # наполнение коавиатуры кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(text=f'стр. {LEXICON["del"]} {button} - {book[button][:80]}',
                                            callback_data=f'{button}del'))
    # кнопка Отменить
    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'],
                                        callback_data='cancel'))

    return kb_builder.as_markup()
