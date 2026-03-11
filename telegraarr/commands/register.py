from telegram import Update
from telegram.ext import ContextTypes
from telegraarr.config import ADMIN_TELEGRAM_ID
from telegraarr.database import add_pending, get_pending, get_failed_attempts, add_failed_attempt, is_blocked, block_user
from telegraarr.services.jellyseerr import get_user_by_email

MAX_FAILED_ATTEMPTS = 5


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    display_name = user.full_name or user.username or str(user.id)

    # Check if blocked
    if await is_blocked(user.id):
        await update.message.reply_text(
            "⛔ You have been blocked from registering.\n"
            "Contact the admin if you think this is a mistake."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /register <your-jellyseerr-email>\n"
            "Example: /register felix@example.com"
        )
        return

    email = context.args[0].strip().lower()

    # Check if already pending
    existing = await get_pending(user.id)
    if existing:
        await update.message.reply_text(
            "⏳ You already have a pending registration request.\n"
            "Please wait for the admin to approve it."
        )
        return

    # Validate email exists in Jellyseerr
    jellyseerr_user = await get_user_by_email(email)
    if not jellyseerr_user:
        attempts = await get_failed_attempts(user.id)
        await add_failed_attempt(user.id, display_name, email)

        remaining = MAX_FAILED_ATTEMPTS - attempts - 1

        if remaining <= 0:
            await block_user(user.id, display_name)
            await update.message.reply_text(
                "⛔ Too many failed attempts. You have been blocked.\n"
                "Contact the admin if you think this is a mistake."
            )
            await context.bot.send_message(
                chat_id=ADMIN_TELEGRAM_ID,
                text=(
                    f"🚨 *User auto-blocked after {MAX_FAILED_ATTEMPTS} failed registration attempts*\n\n"
                    f"Name: {display_name}\n"
                    f"Telegram ID: `{user.id}`\n"
                    f"Last attempted email: `{email}`\n\n"
                    f"Unblock: /unblock `{user.id}`"
                ),
                parse_mode="Markdown",
            )
            return

        await update.message.reply_text(
            f"❌ That email wasn't found in Jellyseerr.\n"
            f"Make sure you're using the email you signed up with.\n"
            f"⚠️ {remaining} attempt{'s' if remaining != 1 else ''} remaining before you are blocked."
        )
        return

    # Store pending request
    await add_pending(user.id, display_name, email)

    await update.message.reply_text(
        "✅ Registration request sent!\n"
        "You'll get a message here once the admin approves you."
    )

    await context.bot.send_message(
        chat_id=ADMIN_TELEGRAM_ID,
        text=(
            f"🔔 *New registration request*\n\n"
            f"Name: {display_name}\n"
            f"Telegram ID: `{user.id}`\n"
            f"Jellyseerr email: `{email}`\n\n"
            f"Approve: /approve `{user.id}`\n"
            f"Deny: /deny `{user.id}`"
        ),
        parse_mode="Markdown",
    )