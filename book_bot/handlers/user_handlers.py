from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from keyboards.pagitation_kb import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book
from database import user_db, user_dict_template


router: Router = Router()

# хендлер команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # добавление пользователя в user_db, если он новый
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = user_dict_template

    await message.answer(text=LEXICON['/start'])  # , reply_markup=...)

# хендлер команды /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])

# хендлер команды /bookmarks (показ закладок)
@router.message(Command(commands=['/bookmarks']))
async def process_bookmarks_command(message: Message):
    await message.answer(text=LEXICON['bookmarks'], reply_markup=create_bookmarks_keyboard(...))

# хендлер команды /beginning (переход в начало книги)
@router.message(Command(commands=['beginning']))
async def process_beginnig_command(message: Message):
    # переводим указатель этого пользователя в нашей "базе" на страницу 1
    user_db[message.from_user.id]['page'] = 1
    # выводим первую страницу
    await message.answer(text=book[1])

# хендлер команды /continue (продолжение чтения)
@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    # отображаем страницу, на которой остановился пользователь
    await message.answer(text=book[message.from_user.id])

# хендлер перехода на следующую страницу
@router.message(Text(text=LEXICON['forward']))
async def process_next_page(message: Message):
    user_id = message.from_user.id
    await message.answer(text=book[user_id],
                         reply_markup=create_pagination_keyboard(['backward',
                                                                  f'{user_db[user_id]["page"]}/{len(book)}',
                                                                  'forward']))

# хендлер перехода на предыдущую страницу
@router.message(Text(text=LEXICON['backward']))
async def process_previous_page(message: Message):

    await message.answer(...)
