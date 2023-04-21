from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

import configparser

# токен
config = configparser.ConfigParser()
config.read('.ini')
BOT_TOKEN: str = config['AAGaribyanBot']['BOT_TOKEN']

# инициализация хранилища (создание экземпляра класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# создание объектов бота и диспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# создание "базы данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# класс для группы состояний FSM
class FSMFillForm(StatesGroup):
    # создание экземпляра класса State, с последовательным перечислением
    # возможных состояний, в которых будет находиться бот в разные моменты взаимодействия
    fill_name = State()         # состояние ожидания ввода имени
    fill_age = State()          # состояние ожидания ввода возраста
    fill_gender = State()       # состояние ожидания выбора пола
    upload_photo = State()      # состояние ожидания загрузки фото
    fill_education = State()    # состояние ожидания выбора образования
    fill_wish_news = State()    # состояние ожидания выбора получать ли новости


# хендлер на команду "/start" вне состояний с предложением заполнения анкеты
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Этот бот демонстрирует работу FSM\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


# хендлер на команду "/cancel" в любых состояниях, кроме состояния по умолчанию с отключением машины состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
    # сброс состояния
    await state.clear()


# хендлер на команду "/cancel" в состоянии по умолчанию
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


# хендлер на команду "/fillform" с переводом бота в состояние ожидания ввода имени
@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваше имя')

    # установка состояния ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# хендлер на ввод корректного имени с переводом в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # сохранение введенного имени в хранилише по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')

    # установка состояния ожидания ввода вохраста
    await state.set_state(FSMFillForm.fill_age)


# хендлер на некорректный ввод имени
@dp.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel')


# хендлер на ввод корректного возраста с переводом на состояние ожидания выбора пола
@dp.message(StateFilter(FSMFillForm.fill_age), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    # сохранение возраста в хранилище по ключу "age"
    await state.update_data(age=message.text)

    # создание объекта инлайн-кнопок полов
    male_button = InlineKeyboardButton(text='Мужской ♂',
                                       callback_data='male')
    female_button = InlineKeyboardButton(text='Женский ♀',
                                         callback_data='female')
    undefined_button = InlineKeyboardButton(text='Иной',
                                            callback_data='undefined_gender')

    # добавление кнопки в клавиатуру (две в одном ряду и одну ниже)
    keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button], [undefined_button]]
    # создание объекта инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # отправка пользователю сообщения с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите ваш пол',
                         reply_markup=markup)

    # установка состояния ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# хендлер на ввод некорректного возраста
@dp.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(text='Возраст должен быть целым числом от 4 до 120\n\n'
                              'Попробуйте еще раз\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel')


# хендлер на нажатие кнопки выбора пола с переводом в состояние ожидания отправки фото
@dp.callback_query(StateFilter(FSMFillForm.fill_gender), Text(text=['male', 'female', 'undefined_gender']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # сохранение пола (callback.data) в хранилище по ключу "gender"
    await state.update_data(gender=callback.data)

    # удаление сообщения с кнопками(так как следующий этап - загрузка фото)
    await callback.message.delete()
    await callback.message.answer(text='Спасибо! А теперь загрузите, '
                                       'пожалуйста, ваше фото')

    # установка состояния ожидания фото
    await state.set_state(FSMFillForm.upload_photo)


# хендлер на некорректный ввод при выборе пола
@dp.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе пола\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel')


# хендлер на получение фото с переводом в состояние ожижания выбора образования
@dp.message(StateFilter(FSMFillForm.upload_photo), F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
    # сохранение данных о фото (file_unique_id и file_id) в хранилище по ключам "photo_unique_id" и "photo_id"
    await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                            photo_id=largest_photo.file_id)

    # создание объектов инлайн-кнопок образования
    no_edu_button = InlineKeyboardButton(text='Нету',
                                         callback_data='no_edu')
    secondary_button = InlineKeyboardButton(text='Среднее',
                                            callback_data='secondary')
    sec_professional_button = InlineKeyboardButton(text='Среднее профессиональное',
                                                   callback_data='sec_professional')
    bachelor_button = InlineKeyboardButton(text='Бакалавр',
                                           callback_data='bachelor')
    specialist_button = InlineKeyboardButton(text='Специалист',
                                             callback_data='specialist')
    master_button = InlineKeyboardButton(text='Магистр',
                                         callback_data='master')

    # добавление кнопок в клавиатуру (по одной в ряду)
    keyboard: list[list[InlineKeyboardButton]] = [
        [no_edu_button],
        [secondary_button],
        [sec_professional_button],
        [bachelor_button],
        [specialist_button],
        [master_button]
    ]
    # создание объекта инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # отправка пользователю сообщения с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите ваше образование',
                         reply_markup=markup)

    # установка состояния ожидания выбора образования
    await state.set_state(FSMFillForm.fill_education)


# хендлер на некорректный ввод при ожидании фотографии
@dp.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'ваше фото\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel')


# хендлер на выбор образования с переводом в состояние согласия получать новости
@dp.callback_query(StateFilter(FSMFillForm.fill_education),
                   Text(text=['no_edu', 'secondary', 'sec_professional', 'bachelor', 'specialist', 'master']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    # сохранение данных об образовании по ключу "education"
    await state.update_data(education=callback.data)

    # создание объектов инлайн-кнопок для вопроса подписки на новостиэ
    yes_news_button = InlineKeyboardButton(text='Да',
                                           callback_data='yes_news')
    no_news_button = InlineKeyboardButton(text='Нет, спасибо',
                                          callback_data='no_news')

    # добавление кнопок в клавиатуру (в один ряд)
    keyboard: list[list[InlineKeyboardButton]] = [[yes_news_button, no_news_button]]
    # создание объекта инлайн-клавитуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # редактирование предыдущего сообщения с кнопками при отправке нового текста с новой клавиатурой
    await callback.message.edit_text(text='Спасибо!\n\n'
                                          'Остался последний шаг.\n'
                                          'Хотели бы вы получать новости?',
                                     reply_markup=markup)

    # установка состояния ожидания выбора получать ли новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)


# хендлер на некорректный ввод образования
@dp.message(StateFilter(FSMFillForm.fill_education))
async def warning_not_education(message: Message):
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе образования\n\nЕсли вы хотите '
                              'прервать заполнение анкеты - отправьте '
                              'команду /cancel')


# хендлер на выбор получать или новости с выводом из машины состояний (FSM)
@dp.callback_query(StateFilter(FSMFillForm.fill_wish_news), Text(text=['yes_news', 'no_news']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # сохранение данных с помощью менеджера контекста
    await state.update_data(wish_news=callback.data == 'yes_news')  # запись сразу bool
    # добавление анкеты пользователя в "базу данных" по ключу id пользователя
    user_dict[callback.from_user.id] = await state.get_data()

    # завершение машины состояний
    await state.clear()

    # отправка в чат ссобщения о вызоде из машины состояний
    await callback.message.edit_text(text='Спасибо! Ваши данные сохранены!\n\n'
                                          'Вы вышли из машины состояний')
    # отправка в чат предложения посмотреть свою анкету
    await callback.message.answer(text='Чтобы посмотреть данные вашей '
                                       'анкеты - отправьте команду /showdata')


# хендлер на некорректный ввод при выборе получать ли новости
@dp.message(StateFilter(FSMFillForm.fill_wish_news))
async def warning_not_wish_news(message: Message):
    await message.answer(text='Пожалуйста, воспользуйтесь кнопками!\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel')


# хендлер на команду "/showdata" с выводом в чат имеющейся информации по пользователю
@dp.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # отправка пользователю анкеты, если она есть в "базе"
    user_id = message.from_user.id
    if user_id in user_dict:
        await message.answer_photo(photo=user_dict[user_id]['photo_id'],
                                   caption=f'Имя: {user_dict[user_id]["name"]}\n'
                                           f'Возраст: {user_dict[user_id]["age"]}\n'
                                           f'Пол: {user_dict[user_id]["gender"]}\n'
                                           f'Образование: {user_dict[user_id]["education"]}\n'
                                           f'Получать новости: {user_dict[user_id]["wish_news"]}')
    else:
        # предложение заполнить, если анкеты нет
        await message.answer(text='Вы еще не заполняли анкету. '
                                  'Чтобы приступить - отправьте '
                                  'команду /fillform')


# хендлер на любые сообщения вне состояний, кроме учтенных команд
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, я вас не понимаю, попробуйте ввести команду /help')


# запуск поллинга
if __name__ == '__main__':
    dp.run_polling(bot)
