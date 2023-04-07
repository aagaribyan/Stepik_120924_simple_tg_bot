'''
class MyClass:
    def __init__(self) -> None:
        pass

    def __call__(self) -> str:
        return 'Результат вызова экземпляра класса'

my_class_1 = MyClass()
my_class_2 = MyClass()

print(my_class_1)
# Output: <__main__.MyClass object at 0x00000237E6A6BE50>

print(my_class_1())
# Output: Результат вызова экземпляра класса
'''

from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message

import configparser


config = configparser.ConfigParser()
config.read('.ini')
BOT_TOKEN = config['AAGaribyanBot']['BOT_TOKEN']

# создание объектов бота и диспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# список администраторов бота
admin_ids: list[int] = [742654337]

# собственный фильтр, проверяющий пользователя на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # в качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# хендлер на апдейты от админа
@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    await message.answer(text='Вы админ')


# хендлер на апдейт не от админа
@dp.message()
async def answer_if_not_admins_update(message: Message):
    await message.answer(text='Вы не админ')


if __name__ == '__main__':
    dp.run_polling(bot)