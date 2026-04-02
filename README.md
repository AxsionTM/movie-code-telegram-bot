# MovieCode Bot (Telegram)

--- РУССКИЙ ОПИСАНИЕ (RUSSIAN) ---

Телеграм-бот для автоматической выдачи названий фильмов по кодам. Основная фишка — обязательная проверка подписки на каналы-спонсоры перед получением информации. Это идеальное решение для тех, кто гонит трафик из TikTok, Instagram Reels или YouTube Shorts.

Основные функции:
- Контент-локер: пользователь не увидит название фильма, пока не подпишется на всех спонсоров.
- Умная проверка: бот засчитывает подписку, даже если пользователь только отправил заявку в закрытый канал.
- Удобная админка: добавление и удаление фильмов или спонсоров прямо через интерфейс бота.
- Аналитика и статистика: отслеживание самых популярных запросов и активности аудитории по часам.
- Универсальные коды: в качестве кода можно использовать цифры, слова или эмодзи-комбинации.

Технологический стек:
- Язык: Python 3.10+
- Библиотека: AIOGram 3.x (Асинхронность)
- База данных: SQLite
- Секреты: Dotenv для хранения токенов

Установка и запуск:

1. Клонируйте проект:
git clone https://github.com
cd название_репозитория

2. Установите необходимые библиотеки:
pip install -r requirements.txt

3. Настройте конфигурацию:
Создайте файл .env в корне проекта и впишите туда свои данные:
BOT_TOKEN=ваш_токен_от_BotFather
ADMIN_ID=ваш_телеграм_айди

4. Запустите бота:
python main.py

Автор: [\\](https://github.com/AxsionTM)

================================================================

--- ENGLISH DESCRIPTION (ENGLISH) ---

A Telegram bot designed to provide movie titles based on specific codes. The core feature is a mandatory subscription check for sponsor channels before revealing the content. This is a perfect tool for creators driving traffic from TikTok, Instagram Reels, or YouTube Shorts.

Key Features:
- Content Locker: Users cannot see the movie title until they subscribe to all listed sponsor channels.
- Smart Verification: The bot detects subscriptions even if the user has only sent a join request to a private channel.
- Admin Dashboard: Manage movies and sponsors directly within the Telegram interface.
- Analytics & Stats: Track the most popular movie queries and user activity peaks by hour.
- Versatile Codes: Supports numbers, text strings, or emoji combinations as movie identifiers.

Tech Stack:
- Language: Python 3.10+
- Framework: AIOGram 3.x (Asynchronous)
- Database: SQLite
- Security: Dotenv for environment variables

Installation & Setup:

1. Clone the repository:
git clone https://github.com
cd repo_name

2. Install dependencies:
pip install -r requirements.txt

3. Configure environment variables:
Create a .env file in the root directory and add:
BOT_TOKEN=your_bot_token_from_BotFather
ADMIN_ID=your_telegram_user_id

4. Run the bot:
python main.py

Author: [\\](https://github.com/AxsionTM)
