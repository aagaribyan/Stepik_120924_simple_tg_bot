from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

# Инициализация роутера
router: Router = Router()


# хендлер на любые сообщения, кроме команд /start и /help
@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat_id)
    except:
        await message.reply(text=LEXICON_RU['no_echo'])