import asyncio

from aiogram import Bot, Dispatcher
from config_data import Config, load_config
from handlers import other_handlers, user_handlers

# Функция конфигурации и запуска бота
async def main() -> None:

    # Загрузка конфига в перменную config
    config: Config = load_config()

    # Инициализия бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистрация роутеров в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропуск накопившихся апдейтов и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
