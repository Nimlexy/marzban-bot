from telegram import Update
from telegram.ext import ContextTypes
from db.models import SessionLocal, User

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    username = update.effective_user.username

    async with SessionLocal() as session:
        user = await session.get(User, {"telegram_id": tg_id})
        if not user:
            user = User(telegram_id=tg_id, username=username, marzban_username=username)
            session.add(user)
            await session.commit()

    await update.message.reply_text("Привет! Добро пожаловать в VPN-бот. Напиши /profile, чтобы посмотреть информацию о подписке.")
