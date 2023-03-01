from dataclasses import dataclass
import configparser


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    ini = configparser.ConfigParser()  # создаем экземпляр класса ConfigParser
    ini.read(path if path else '.ini')  # считываем .ini файл

    # Создаем экземпляр класса Config, наполняем его данными из файла .ini и возвращаем
    return Config(tg_bot=TgBot(token=ini['AAGaribyanBot']['BOT_TOKEN'],
                               admin_ids=list(map(int, ini['AAGaribyanBot']['ADMIN_IDS'].split(',')))),
                  db=DatabaseConfig(database=ini['AAGaribyanBot']['DATABASE'],
                                    db_host=ini['AAGaribyanBot']['DB_HOST'],
                                    db_user=ini['AAGaribyanBot']['DB_USER'],
                                    db_password=ini['AAGaribyanBot']['DB_PASSWORD']))
