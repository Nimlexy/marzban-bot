from telegram import Update
from telegram.ext import ContextTypes
from db.models import SessionLocal, User
from bot.marzban_api import get_user_info

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id

    async with SessionLocal() as session:
        result = await session.execute(
            "SELECT * FROM users WHERE telegram_id = :tg_id",
            {"tg_id": tg_id}
        )
        user = result.fetchone()
        if not user:
            await update.message.reply_text("Ты не зарегистрирован. Напиши /start.")
            return

        marzban_info = await get_user_info(user.marzban_username)
        if not marzban_info:
            await update.message.reply_text("Не удалось получить данные от Marzban.")
            return

        quota = marzban_info['data']['usage']['download'] + marzban_info['data']['usage']['upload']
        expiry = marzban_info['data']['expire']

        text = f"""👤 *Профиль*
Marzban: `{user.marzban_username}`
📅 Истекает: `{expiry}`
📊 Использовано: `{quota / 1024 / 1024:.2f} MB`"""

        await update.message.reply_text(text, parse_mode="Markdown")
