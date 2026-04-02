# 🎬 Movie Code Bot

<p align="center">
  🔍 Movie search by codes • 🔐 Subscription check • ⚡ Fast & Convenient
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/aiogram-3.x-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

---

## 👤 Author

<table border="0">
  <tr>
    <td>
      <strong>Maxim</strong> (Axsion)<br>
      <em>Python Developer & Bot Creator</em><br>
      <a href="https://github.com">
        <img src="https://shields.io" alt="GitHub">
      </a>
    </td>
  </tr>
</table>

---


## 📌 Features

### 👤 For Users

* 🔎 Search movies by unique code
* 🎲 Random movie (if you don't know what to watch)
* 👤 User profile:

  * 📅 Registration date
  * ⭐ Experience (earned by searching movies)
* ⚡ Fast performance without delays

---

### 🛠 Admin Panel (In-bot)

* ➕ Add movies (code + title)

* ✏️ Edit movies

* 🗑 Delete movies

* 📢 Sponsor management:

  * ➕ Add channels
  * ✏️ Edit channels
  * ❌ Delete channels

* 📊 Statistics:

  * 📈 Number of users
  * 🔥 Most popular movies
  * 🎯 Request frequency

---

### 🔐 Access System

* ✅ Subscription check for sponsors
* 🚫 Movies are not shown without subscription

---

## 🧠 How It Works

1. User sends a code 🎫
2. Bot checks the subscription 📡
3. If subscribed — shows the movie 🎬
4. If not — asks to subscribe 🚫

---

## ⚙️ Technologies

* 🐍 Python 3.10+
* 🤖 aiogram 3.x
* ⚡ asyncio

### 📦 Main Dependencies

```txt
aiogram==3.26.0
aiohttp==3.13.3
aiofiles==25.1.0
pydantic==2.12.5
```

---

## 📥 Installation

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
pip install -r requirements.txt
```

---

## ▶️ Launch

```bash
python main.py
```

---

## 🔑 Setup

Create a config.py file:

```
BOT_TOKEN=your_token_here
CHANNEL_ID=@your_channel
```

---

## 📸 Usage Example

```
User: 8392  
Bot: 🎬 Movie title: Interstellar
```

---

## 🚫 Limitations

* ❌ Movies are not shown without subscription
* ❌ Works only with existing codes 

---

## 💡 Roadmap

* [ ] Add movie recommendations
* [ ] Improve statistics system
* [ ] Add categories
* [ ] Create a web panel

---

## 🤝 Support

If you have ideas or found bugs — open an Issue 😉

---

## ⭐ Support the Project

Give it a star ⭐ if you liked the bot!

