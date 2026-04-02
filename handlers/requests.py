# handlers/requests.py
from aiogram import Router, types, Bot
from database import add_join_request

router = Router()

@router.chat_join_request()
async def handle_join_request(update: types.ChatJoinRequest, bot: Bot):
    user_id = update.from_user.id
    channel_id = str(update.chat.id)
    
    add_join_request(user_id, channel_id)
    
    # Можно оставить только отправку сообщения юзеру, чтобы он знал, что делать дальше
    try:
        await bot.send_message(user_id, "✅ Заявка принята! Теперь нажми «ПРОВЕРИТЬ» в боте.")
    except:
        pass

