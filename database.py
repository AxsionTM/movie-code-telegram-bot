import sqlite3
from config import DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Таблица для фильмов
    cur.execute('''CREATE TABLE IF NOT EXISTS movies 
                   (code TEXT PRIMARY KEY, title TEXT)''')
    
    # Таблица для спонсоров
    cur.execute('''CREATE TABLE IF NOT EXISTS sponsors 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    url TEXT, 
                    channel_id TEXT)''')

    # Таблица для заявок в закрытые каналы
    cur.execute('''CREATE TABLE IF NOT EXISTS join_requests 
               (user_id INTEGER, channel_id TEXT, PRIMARY KEY (user_id, channel_id))''')
    
    # НОВАЯ ТАБЛИЦА СТАТИСТИКИ (добавляется без вреда остальным)
    cur.execute('''CREATE TABLE IF NOT EXISTS stats 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, 
                    movie_code TEXT, 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
               (user_id INTEGER PRIMARY KEY, 
                username TEXT, 
                joined_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
                xp INTEGER DEFAULT 0)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS user_found_movies 
               (user_id INTEGER, movie_code TEXT, PRIMARY KEY (user_id, movie_code))''')
    
    conn.commit()
    conn.close()

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ФИЛЬМАМИ ---

def add_movie(code, title):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO movies (code, title) VALUES (?, ?)", (code, title))
    conn.commit()
    conn.close()

def get_movie_by_code(code):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT title FROM movies WHERE code = ?", (code,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# --- ФУНКЦИИ ДЛЯ РАБОТЫ СО СПОНСОРАМИ ---

def add_sponsor(title, url, channel_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO sponsors (title, url, channel_id) VALUES (?, ?, ?)", 
                (title, url, channel_id))
    conn.commit()
    conn.close()

def get_all_sponsors():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, title, url, channel_id FROM sponsors")
    results = cur.fetchall()
    conn.close()
    return results

def get_sponsor_by_id(s_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, title, url, channel_id FROM sponsors WHERE id = ?", (s_id,))
    res = cur.fetchone()
    conn.close()
    return res

def delete_sponsor_by_pk(s_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM sponsors WHERE id = ?", (s_id,))
    conn.commit()
    conn.close()

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ЗАЯВКАМИ ---

def add_join_request(user_id, channel_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO join_requests VALUES (?, ?)", (user_id, channel_id))
    conn.commit()
    conn.close()

def has_user_requested(user_id, channel_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM join_requests WHERE user_id = ? AND channel_id = ?", (user_id, str(channel_id)))
    res = cur.fetchone()
    conn.close()
    return res is not None

# --- ФУНКЦИИ СТАТИСТИКИ (НОВОЕ) ---

def log_movie_request(user_id, movie_code):
    """Записывает лог поиска фильма"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO stats (user_id, movie_code) VALUES (?, ?)", (user_id, movie_code))
    conn.commit()
    conn.close()

def get_admin_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute('''SELECT movie_code, COUNT(movie_code) as count 
                   FROM stats GROUP BY movie_code ORDER BY count DESC LIMIT 10''')
    top_movies = cur.fetchall()
    
    cur.execute("SELECT COUNT(id) FROM stats")
    total_requests = cur.fetchone()[0] # Берем число сразу
    
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM stats")
    unique_users = cur.fetchone()[0] # Берем число сразу
    
    conn.close()
    return top_movies, total_requests, unique_users

# Функции для профиля
def register_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def add_xp(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET xp = xp + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_user_info(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT username, joined_date, xp FROM users WHERE user_id = ?", (user_id,))
    res = cur.fetchone()
    conn.close()
    return res

def get_random_movie():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT code, title FROM movies ORDER BY RANDOM() LIMIT 1")
    res = cur.fetchone()
    conn.close()
    return res

def add_xp_safe(user_id, movie_code):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # 1. Проверяем, находил ли юзер этот фильм раньше
    cur.execute("SELECT 1 FROM user_found_movies WHERE user_id = ? AND movie_code = ?", (user_id, movie_code))
    already_found = cur.fetchone()
    
    if not already_found:
        # 2. Если не находил — записываем факт находки
        cur.execute("INSERT INTO user_found_movies (user_id, movie_code) VALUES (?, ?)", (user_id, movie_code))
        # 3. Начисляем опыт
        cur.execute("UPDATE users SET xp = xp + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True # Опыт начислен
    
    conn.close()
    return False # Опыт уже был получен за этот код