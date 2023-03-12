from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


# функция генерации клавиатуры для страницы книги
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # инициализация билдера
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # добавление в билдер ряд кнопок
    kb_builder.row(*[InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                                          callback_data=button) for button in buttons])
    # возвращение объекта инлайн-клавиатуры
    return kb_builder.as_markup()

