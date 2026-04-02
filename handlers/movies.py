from aiogram import Router, types, Bot, F
from aiogram.exceptions import TelegramForbiddenError
# Заменили add_xp на add_xp_safe для защиты от накрутки
from database import get_movie_by_code, log_movie_request, add_xp_safe 
from handlers.start import check_user_sub

router = Router()

@router.message(F.text)  # Реагируем только на текстовые сообщения
async def handle_movie_request(message: types.Message, bot: Bot):
    # 1. Проверяем подписку
    is_subscribed = await check_user_sub(bot, message.from_user.id)
    
    if not is_subscribed:
        try:
            await message.answer("❌ Доступ ограничен! Сначала подпишитесь на спонсоров в /start")
        except TelegramForbiddenError:
            pass
        return

    # 2. Очищаем код от пробелов
    code = message.text.strip()
    
    # Игнорируем команды
    if code.startswith("/"):
        return

    # 3. Ищем фильм в базе
    result = get_movie_by_code(code)

    if result:
        # ЗАПИСЫВАЕМ В СТАТИСТИКУ
        log_movie_request(message.from_user.id, code)
        
        # Пытаемся начислить опыт (только если фильм найден впервые этим юзером)
        xp_added = add_xp_safe(message.from_user.id, code)

        try:
            if xp_added:
                # Если фильм найден впервые
                await message.answer(
                    f"✅ <b>Фильм найден!</b>\n\n🎬 {result}\n\n<i>Вам начислено +1 XP за поиск! 📈</i>", 
                    parse_mode="HTML"
                )
            else:
                # Если пользователь уже вводил этот код ранее
                await message.answer(
                    f"✅ <b>Фильм найден!</b>\n\n🎬 {result}\n\n<i>Опыт за этот фильм уже был получен ранее. 🍿</i>", 
                    parse_mode="HTML"
                )
        except TelegramForbiddenError:
            pass
    else:
        try:
            await message.answer("⚠️ Фильм по такому коду не найден.")
        except TelegramForbiddenError:
            pass
