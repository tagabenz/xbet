import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand

from xbet1 import Xbet


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню")
    ]
    await bot.set_my_commands(commands)


async def cmd_start(message: types.Message):
    bet=Xbet()
    bet.message=message
    await message.answer('Бот запущен ☑️')
    await bet.scan_live()


# @dp.message_handler()
async def any_text_message(message: types.Message):
    await message.answer(message.text)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    # config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token="5233981407:AAF_L4ZuzXr--RrLXBLqwcgl41C2lLQfOhc")
    dp = Dispatcher(bot)

    # Регистрация хэндлеров
    # register_handlers_common(dp)
    dp.register_message_handler(cmd_start,  commands="start")
    dp.register_message_handler(any_text_message)
    #Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
