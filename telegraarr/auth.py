from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegraarr.config import ADMIN_TELEGRAM_ID
from telegraarr.database import is_approved


def require_auth(func):
    """Restrict command to approved users only."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not await is_approved(user_id):
            await update.message.reply_text(
                "⛔ You're not registered.\n"
                "Use /register <your-jellyseerr-email> to request access."
            )
            return
        return await func(update, context)
    return wrapper


def require_admin(func):
    """Restrict command to admin only."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id != ADMIN_TELEGRAM_ID:
            await update.message.reply_text("⛔ Admin only.")
            return
        return await func(update, context)
    return wrapper