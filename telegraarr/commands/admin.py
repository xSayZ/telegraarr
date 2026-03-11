from telegram import Update
from telegram.ext import ContextTypes
from auth import require_admin
from database import approve_user, deny_user, unblock_user, get_pending


@require_admin
async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /approve <telegram_id>")
        return

    try:
        telegram_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid Telegram ID.")
        return

    pending = await get_pending(telegram_id)
    if not pending:
        await update.message.reply_text("❌ No pending request found for that ID.")
        return

    success = await approve_user(telegram_id)
    if not success:
        await update.message.reply_text("❌ Something went wrong approving that user.")
        return

    # Notify admin
    await update.message.reply_text(
        f"✅ Approved *{pending['telegram_name']}* (`{telegram_id}`)",
        parse_mode="Markdown",
    )

    # Notify user
    await context.bot.send_message(
        chat_id=telegram_id,
        text=(
            "✅ *You've been approved!*\n\n"
            "You can now use the following commands:\n"
            "/requests <query> — search requests\n"
            "/queue — active downloads\n"
            "/available <title> — search the library\n"
            "/status — server overview"
        ),
        parse_mode="Markdown",
    )


@require_admin
async def deny_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /deny <telegram_id>")
        return

    try:
        telegram_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid Telegram ID.")
        return

    pending = await get_pending(telegram_id)
    if not pending:
        await update.message.reply_text("❌ No pending request found for that ID.")
        return

    await deny_user(telegram_id)

    # Notify admin
    await update.message.reply_text(
        f"🚫 Denied *{pending['telegram_name']}* (`{telegram_id}`)",
        parse_mode="Markdown",
    )

    # Notify user
    await context.bot.send_message(
        chat_id=telegram_id,
        text="🚫 Your registration request was denied.\nContact the admin if you think this is a mistake."
    )


@require_admin
async def unblock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unblock <telegram_id>")
        return

    try:
        telegram_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid Telegram ID.")
        return

    await unblock_user(telegram_id)

    await update.message.reply_text(
        f"✅ Unblocked `{telegram_id}` — they can now attempt to register again.",
        parse_mode="Markdown",
    )

    await context.bot.send_message(
        chat_id=telegram_id,
        text="✅ You have been unblocked. You can try /register again."
    )