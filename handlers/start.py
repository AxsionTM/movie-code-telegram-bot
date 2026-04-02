from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.types import FSInputFile 
import os 

from keyboards.inline import get_subscription_keyboard, search_button
# Добавили register_user в импорт
from database import get_all_sponsors, has_user_requested, register_user

router = Router()

PHOTO_PATH = "img/fon.png"

async def check_user_sub(bot: Bot, user_id: int):
    sponsors = get_all_sponsors()
    if not sponsors:
        return True
    for sponsor in sponsors:
        channel_id = sponsor[3] 
        
        is_member = False
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in ["left", "kicked"]:
                is_member = True
        except Exception:
            pass

        if not is_member:
            if not has_user_requested(user_id, channel_id):
                return False 
                
    return True

@router.message(Command("start"))
async def start_handler(message: types.Message, bot: Bot):
    # РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ ПРИ СТАРТЕ
    register_user(message.from_user.id, message.from_user.first_name)
    
    is_subscribed = await check_user_sub(bot, message.from_user.id)
    
    if is_subscribed:
        if os.path.exists(PHOTO_PATH):
            photo = FSInputFile(PHOTO_PATH)
            await message.answer_photo(
                photo=photo,
                caption="🍿 Привет! Ты успешно подписан на всех спонсоров.\nНажми на кнопку ниже, чтобы найти фильм:",
                reply_markup=search_button()
            )
        else:
            await message.answer(
                "🍿 Привет! Ты успешно подписан на всех спонсоров.\nНажми на кнопку ниже, чтобы найти фильм:",
                reply_markup=search_button()
            )
    else:
        sponsors = get_all_sponsors()
        kb = get_subscription_keyboard(sponsors)
        await message.answer(
            "⚠️ <b>ПОДПИШИТЕСЬ НА НАШИХ СПОНСОРОВ ЧТОБЫ ПРОДОЛЖИТЬ</b>",
            reply_markup=kb,
            parse_mode="HTML"
        )

@router.callback_query(F.data == "check_subscription")
async def check_btn_handler(callback: types.CallbackQuery, bot: Bot):
    is_subscribed = await check_user_sub(bot, callback.from_user.id)
    
    if is_subscribed:
        try:
            await callback.message.delete()
        except:
            pass
        
        if os.path.exists(PHOTO_PATH):
            photo = FSInputFile(PHOTO_PATH)
            await callback.message.answer_photo(
                photo=photo,
                caption="✅ Проверка пройдена! Нажми на кнопку для поиска:",
                reply_markup=search_button()
            )
        else:
            await callback.message.answer(
                "✅ Проверка пройдена! Нажми на кнопку для поиска:",
                reply_markup=search_button()
            )
    else:
        await callback.answer("❌ Ты подписан не на всех спонсоров или не подал заявку!", show_alert=True)

@router.callback_query(F.data == "start_search")
async def start_search_handler(callback: types.CallbackQuery):
    await callback.message.answer("⌨️ <b>Введите код фильма:</b>", parse_mode="HTML")
    await callback.answer()
