import random
from lexicon.lexicon_ru import LEXICON_RU

# функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    return random.choice(['rock', 'scissors', 'paper', 'reptile', 'Spok'])

# функция, возвращающая ключ и словаря, по которому хранится значение, хранимое как аргумент - выбор игрока
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            return key
    raise Exception

# функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules: dict = {
        'rock': ['scissors', 'reptile'],
        'scissors': ['paper', 'reptile'],
        'paper': ['rock', 'Spok'],
        'reptile': ['Spok', 'paper'],
        'Spok': ['rock', 'scissors']
    }

    if user_choice == bot_choice:
        return 'nobody_won'
    elif bot_choice in rules[user_choice]:
        return 'user_won'
    else:
        return 'bot_won'
