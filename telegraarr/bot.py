import logging
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN
from database import init_db
from commands.register import register_command
from commands.admin import approve_command, deny_command, unblock_command
from commands.requests import requests_command
from commands.queue import queue_command
from commands.available import available_command
from commands.status import status_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Welcome to Telegraarr!\n\n"
        f"Your Telegram ID is: `{update.effective_user.id}`\n\n"
        f"To get started, register with your Jellyseerr email:\n"
        f"/register <your-email>",
        parse_mode="Markdown",
    )


async def post_init(application):
    """Set bot command menu shown in Telegram clients."""
    await application.bot.set_my_commands([
        BotCommand("start", "Introduction and your Telegram ID"),
        BotCommand("register", "Request access with your Jellyseerr email"),
        BotCommand("requests", "Search requests by title"),
        BotCommand("queue", "View active downloads"),
        BotCommand("available", "Check if a title is in the library"),
        BotCommand("status", "Server overview"),
    ])


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Unhandled exception", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "❌ Something went wrong. Please try again later."
        )


def main():
    # Initialise database on startup
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Public commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_command))

    # Authenticated commands
    app.add_handler(CommandHandler("requests", requests_command))
    app.add_handler(CommandHandler("queue", queue_command))
    app.add_handler(CommandHandler("available", available_command))
    app.add_handler(CommandHandler("status", status_command))

    # Admin commands
    app.add_handler(CommandHandler("approve", approve_command))
    app.add_handler(CommandHandler("deny", deny_command))
    app.add_handler(CommandHandler("unblock", unblock_command))

    app.add_error_handler(error_handler)

    logger.info("Telegraarr started")
    app.run_polling()


if __name__ == "__main__":
    main()