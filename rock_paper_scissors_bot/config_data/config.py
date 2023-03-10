from dataclasses import dataclass
import configparser


@dataclass
class TgBot:
    token: str   # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    ini = configparser.ConfigParser()
    ini.read(path if path else '.ini')

    return Config(tg_bot=TgBot(token=ini['AAGaribyanBot']['BOT_TOKEN']))
