from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
from database import (
    add_movie, add_sponsor, get_movie_by_code, 
    get_all_sponsors, get_sponsor_by_id, delete_sponsor_by_pk,
    get_admin_stats # Добавили импорт функции статистики
)
from keyboards.inline import (
    admin_panel_keyboard, cancel_keyboard, movie_exists_keyboard, 
    sponsors_manage_keyboard, sponsor_card_keyboard
)

router = Router()

class AdminStates(StatesGroup):
    wait_movie_code = State()
    wait_movie_title = State()
    wait_sponsor_name = State() 
    wait_sponsor_url = State()
    wait_sponsor_id = State()

# Вход в админку (со сбросом состояний)
@router.message(Command("admin"), F.from_user.id == ADMIN_ID)
async def admin_start(message: types.Message, state: FSMContext):
    await state.clear() 
    await message.answer("🛠 <b>Админ-панель</b>. Выберите действие:", 
                         reply_markup=admin_panel_keyboard(), parse_mode="html")

# Кнопка ОТМЕНА / НАЗАД
@router.callback_query(F.data == "cancel_admin")
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.edit_text("🛠 <b>Админ-панель</b>. Выберите действие:", 
                                         reply_markup=admin_panel_keyboard(), parse_mode="html")
    except Exception:
        pass

# --- ЛОГИКА СТАТИСТИКИ ---

@router.callback_query(F.data == "view_stats", F.from_user.id == ADMIN_ID)
async def view_stats_handler(callback: types.CallbackQuery):
    from database import get_admin_stats
    top_movies, total_req, unique_users = get_admin_stats()
    
    # Исправляем извлечение чисел (убираем [0], так как там уже числа)
    total = total_req if total_req else 0
    users = unique_users if unique_users else 0
    
    text = f"📊 <b>СТАТИСТИКА БОТА</b>\n\n"
    text += f"👤 Уникальных пользователей: <b>{users}</b>\n"
    text += f"🔎 Всего поисков: <b>{total}</b>\n\n"
    text += "🔝 <b>ТОП-10 запросов (код — раз):</b>\n"
    
    if not top_movies:
        text += "<i>Данных пока нет...</i>"
    else:
        for i, movie in enumerate(top_movies, 1):
            # movie[0] - код фильма, movie[1] - количество запросов
            text += f"{i}. <code>{movie[0]}</code> — <b>{movie[1]}</b>\n"
            
    try:
        await callback.message.edit_text(text, parse_mode="html", reply_markup=cancel_keyboard())
    except Exception:
        pass

# --- ЛОГИКА ФИЛЬМОВ ---

@router.callback_query(F.data == "add_movie", F.from_user.id == ADMIN_ID)
async def start_add_movie(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("Введите <b>КОД</b> для фильма:", 
                                         reply_markup=cancel_keyboard(), parse_mode="html")
    except Exception:
        pass
    await state.set_state(AdminStates.wait_movie_code)

@router.message(AdminStates.wait_movie_code)
async def process_movie_code(message: types.Message, state: FSMContext):
    code = message.text.strip()
    existing_movie = get_movie_by_code(code)
    
    if existing_movie:
        await state.update_data(temp_code=code)
        await message.answer(f"⚠️ Под кодом <b>{code}</b> уже есть фильм:\n\n<i>{existing_movie}</i>\n\nХотите изменить его?", 
                             reply_markup=movie_exists_keyboard(), parse_mode="html")
    else:
        await state.update_data(movie_code=code)
        await message.answer(f"Код <b>{code}</b> свободен. Теперь введите <b>НАЗВАНИЕ</b> фильма:", 
                             reply_markup=cancel_keyboard(), parse_mode="html")
        await state.set_state(AdminStates.wait_movie_title)

@router.callback_query(F.data == "confirm_movie_change")
async def confirm_change(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(movie_code=data['temp_code'])
    try:
        await callback.message.edit_text("Хорошо, введите <b>НОВОЕ НАЗВАНИЕ</b> фильма:", 
                                         reply_markup=cancel_keyboard(), parse_mode="html")
    except Exception:
        pass
    await state.set_state(AdminStates.wait_movie_title)

@router.message(AdminStates.wait_movie_title)
async def process_movie_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    add_movie(data['movie_code'], message.text)
    await state.clear()
    await message.answer(f"✅ Готово! Фильм под кодом <code>{data['movie_code']}</code> успешно сохранен.", 
                         reply_markup=admin_panel_keyboard(), parse_mode="html")

# --- ЛОГИКА СПОНСОРОВ (CRM) ---

@router.callback_query(F.data == "sponsors_menu", F.from_user.id == ADMIN_ID)
async def show_sponsors_list(callback: types.CallbackQuery):
    sponsors = get_all_sponsors()
    try:
        await callback.message.edit_text("📋 <b>Список спонсоров:</b>\nНажмите на название для управления:", 
                                         reply_markup=sponsors_manage_keyboard(sponsors), parse_mode="html")
    except Exception:
        pass

@router.callback_query(F.data.startswith("view_sp_"))
async def view_sponsor(callback: types.CallbackQuery):
    s_id = int(callback.data.split("_")[2])
    s = get_sponsor_by_id(s_id)
    if s:
        text = (f"📢 <b>Спонсор:</b> {s[1]}\n\n"
                f"🔗 <b>Ссылка:</b> {s[2]}\n"
                f"🆔 <b>ID канала:</b> <code>{s[3]}</code>")
        try:
            await callback.message.edit_text(text, parse_mode="html", reply_markup=sponsor_card_keyboard(s_id))
        except Exception:
            pass

@router.callback_query(F.data.startswith("confirm_del_sp_"))
async def del_sponsor_exec(callback: types.CallbackQuery):
    s_id = int(callback.data.split("_")[3])
    delete_sponsor_by_pk(s_id)
    await callback.answer("✅ Спонсор успешно удален!", show_alert=True)
    await show_sponsors_list(callback)

# Добавление спонсора
@router.callback_query(F.data == "add_sponsor", F.from_user.id == ADMIN_ID)
async def start_add_sponsor(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("Введите <b>НАЗВАНИЕ</b> спонсора (только для вас):", 
                                         reply_markup=cancel_keyboard(), parse_mode="html")
    except Exception:
        pass
    await state.set_state(AdminStates.wait_sponsor_name)

@router.message(AdminStates.wait_sponsor_name)
async def process_sp_name(message: types.Message, state: FSMContext):
    await state.update_data(sp_name=message.text)
    await message.answer("Теперь отправьте <b>ССЫЛКУ</b> на канал:", 
                         reply_markup=cancel_keyboard(), parse_mode="html")
    await state.set_state(AdminStates.wait_sponsor_url)

@router.message(AdminStates.wait_sponsor_url)
async def process_sp_url(message: types.Message, state: FSMContext):
    await state.update_data(sp_url=message.text)
    await message.answer("И последнее: введите <b>ID канала</b> (начинается с -100):", 
                         reply_markup=cancel_keyboard(), parse_mode="html")
    await state.set_state(AdminStates.wait_sponsor_id)

@router.message(AdminStates.wait_sponsor_id)
async def process_sp_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    add_sponsor(data['sp_name'], data['sp_url'], message.text)
    await state.clear()
    await message.answer(f"✅ Спонсор <b>{data['sp_name']}</b> успешно добавлен!", 
                         reply_markup=admin_panel_keyboard(), parse_mode="html")
