from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

# Кнопки для обычных пользователей (подписка)
def get_subscription_keyboard(sponsors_list):
    builder = InlineKeyboardBuilder()
    for i, sponsor in enumerate(sponsors_list, 1):
        # В базе теперь: 0-id, 1-title, 2-url, 3-channel_id
        url = sponsor[2] 
        builder.row(types.InlineKeyboardButton(text=f"Спонсор {i} 📢", url=url))
    
    builder.row(types.InlineKeyboardButton(text="✅ Я ПОДПИСАЛСЯ (ПРОВЕРИТЬ)", callback_data="check_subscription"))
    return builder.as_markup()

# Кнопка поиска после подписки
# keyboards/inline.py

def search_button():
    builder = InlineKeyboardBuilder()
    # Первая кнопка - основной поиск
    builder.row(types.InlineKeyboardButton(text="🔎 Найти фильм", callback_data="start_search"))
    
    # Вторая кнопка - рандом (в ту же строку или в новую)
    builder.row(types.InlineKeyboardButton(text="🎲 Случайный фильм", callback_data="random_movie"))
    
    # Третья кнопка - профиль
    builder.row(types.InlineKeyboardButton(text="👤 Мой Профиль", callback_data="my_profile"))
    
    return builder.as_markup()


# Главное меню админа (ДОБАВИЛИ СТАТИСТИКУ)
def admin_panel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🎬 Добавить фильм", callback_data="add_movie"))
    builder.row(types.InlineKeyboardButton(text="📢 Управление спонсорами", callback_data="sponsors_menu"))
    builder.row(types.InlineKeyboardButton(text="📊 Статистика", callback_data="view_stats"))
    return builder.as_markup()

# Кнопка отмены для FSM
def cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Отмена / Назад", callback_data="cancel_admin"))
    return builder.as_markup()

# Список спонсоров в админке (по именам)
def sponsors_manage_keyboard(sponsors_list):
    builder = InlineKeyboardBuilder()
    for s in sponsors_list:
        builder.row(types.InlineKeyboardButton(text=f"🔗 {s[1]}", callback_data=f"view_sp_{s[0]}"))
    
    builder.row(types.InlineKeyboardButton(text="➕ Добавить нового", callback_data="add_sponsor"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="cancel_admin"))
    return builder.as_markup()

# Карточка конкретного спонсора (удаление)
def sponsor_card_keyboard(s_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🗑 Удалить этого спонсора", callback_data=f"confirm_del_sp_{s_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ К списку спонсоров", callback_data="sponsors_menu"))
    return builder.as_markup()

# Клавиатура при дубликате кода фильма
def movie_exists_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔄 Изменить (Перезаписать)", callback_data="confirm_movie_change"))
    builder.row(types.InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_admin"))
    return builder.as_markup()
