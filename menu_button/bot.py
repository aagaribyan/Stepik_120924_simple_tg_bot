# ...

from aiogram import Bot, Dispatcher
from keyboards.set_menu import set_main_menu

# ...

from config_data.config import Config, load_config


# функция конфигурирования и запуска бота
async def main():
    # ...

    # загрузка конфигураций в переменную config
    config: Config = load_config()

    # инициализация бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # настройка кнопки Menu
    await set_main_menu(bot)

    # ...