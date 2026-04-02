from aiogram import Router, types, F
from database import get_user_info, get_random_movie

router = Router()

def get_rank(xp):
    if xp < 5: return "Новичок 👶"
    if xp < 15: return "Киноман 🍿"
    if xp < 50: return "Эксперт 🎬"
    return "Легенда Голливуда 🏆"

@router.callback_query(F.data == "my_profile")
async def profile_handler(callback: types.CallbackQuery):
    info = get_user_info(callback.from_user.id)
    if not info:
        await callback.answer("Ошибка данных!")
        return
        
    username, date, xp = info
    rank = get_rank(xp)
    
    text = (f"👤 <b>ВАШ ПРОФИЛЬ</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Имя:</b> {username}\n"
            f"📅 <b>В клубе с:</b> {date[:10]}\n"
            f"📈 <b>Опыт:</b> {xp} XP\n"
            f"🎖 <b>Ранг:</b> {rank}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<i>Ищи больше фильмов, чтобы повысить свой ранг!</i>")
            
    await callback.message.answer(text, parse_mode="html")
    await callback.answer()

@router.callback_query(F.data == "random_movie")
async def random_movie_handler(callback: types.CallbackQuery):
    movie = get_random_movie()
    if movie:
        await callback.message.answer(f"🎲 <b>Случайный выбор для тебя:</b>\n\n🎬 {movie[1]}\n🔢 Код: {movie[0]}", parse_mode="html")
    else:
        await callback.answer("В базе пока нет фильмов 😔")
    await callback.answer()
