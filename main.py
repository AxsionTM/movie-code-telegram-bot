import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import init_db
from handlers import start, admin, movies, requests, profile

# Включаем логирование
logging.basicConfig(level=logging.WARNING)

async def main():
    # Инициализируем базу данных
    init_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    # Сначала служебные события (заявки), потом админка, потом старт и в конце фильмы
    dp.include_router(requests.router) 
    dp.include_router(profile.router)
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(movies.router)

    print("Бот запущен и готов к работе!")

    # ОСТАВЛЯЕМ ТОЛЬКО ОДИН ЗАПУСК С ПРАВИЛЬНЫМИ НАСТРОЙКАМИ
    await dp.start_polling(
        bot, 
        allowed_updates=["message", "callback_query", "chat_join_request"]
    )
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
