# Movie Code Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/aiogram-3.x-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

---

<p align="center">
  <img src="https://wsrv.nl/?url=avatars.githubusercontent.com/u/146373364%3Fv%3D4&w=200&h=200&fit=cover&mask=circle" width="120">
</p>

<h2 align="center">Maxsim (Axsion)</h2>

<p align="center">
  Developer Telegram Bots · Python · Automation
</p>

<p align="center">
  <a href="https://github.com/AxsionTM">
    <img src="https://img.shields.io/badge/GitHub-Axsion-black?style=for-the-badge&logo=github">
  </a>
</p>

---

## Features

### For Users

* Search movies by unique code
* Random movie selection
* User profile:

  * Registration date
  * Experience earned through movie searches
* Fast response without unnecessary delays

### Admin Panel

* Add movies by code and title
* Edit movies
* Delete movies
* Sponsor management:

  * Add channels
  * Edit channels
  * Delete channels
* Statistics:

  * Number of users
  * Most popular movies
  * Request frequency

### Access System

* Subscription verification for sponsor channels
* Movies are unavailable without an active subscription

---

## How It Works

1. User sends a movie code
2. Bot checks the user's subscription
3. If the subscription is active, the movie is displayed
4. Otherwise, the bot asks the user to subscribe

---

## Technologies

* Python 3.10+
* aiogram 3.x
* asyncio

### Main Dependencies

```txt
aiogram==3.26.0
aiohttp==3.13.3
aiofiles==25.1.0
pydantic==2.12.5
```

---

## Installation

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
pip install -r requirements.txt
```

---

## Launch

```bash
python main.py
```

---

## Configuration

Create a `config.py` file:

```python
BOT_TOKEN = "your_token_here"
CHANNEL_ID = "@your_channel"
```

---

## Usage Example

```text
User: 8392
Bot: Movie title: Interstellar
```

---

## Limitations

* Movies are available only after passing the subscription check
* The bot works only with existing movie codes

---

## Roadmap

* [ ] Add movie recommendations
* [ ] Improve statistics system
* [ ] Add categories
* [ ] Create a web panel

---

## Support

If you have ideas or find a bug, open an Issue in the repository.

## Support the Project

If you like the project, consider giving it a star.
