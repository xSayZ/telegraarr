from telegram import Update
from telegram.ext import ContextTypes
from telegraarr.auth import require_auth
from telegraarr.services.jellyfin import search_library


ITEM_TYPE_MAP = {
    "Movie": "🎬",
    "Series": "📺",
}


@require_auth
async def available_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage: /available <title>\n"
            "Example: /available breaking bad"
        )
        return

    query = " ".join(context.args)

    try:
        results = await search_library(query)
    except Exception as e:
        await update.message.reply_text(f"❌ Couldn't reach Jellyfin: {e}")
        return

    if not results:
        await update.message.reply_text(
            f'❌ *"{query}"* isn\'t in the library yet.\n'
            f"You can request it in Jellyseerr.",
            parse_mode="Markdown",
        )
        return

    lines = [f'*Results for "{query}":*\n']

    for item in results:
        itype = ITEM_TYPE_MAP.get(item.get("Type"), "❓")
        name = item.get("Name", "Unknown")
        year = item.get("ProductionYear", "")
        overview = item.get("Overview", "")

        # Truncate overview if present
        if overview and len(overview) > 100:
            overview = overview[:97] + "..."

        line = f"{itype} *{name}*{f' ({year})' if year else ''} ✅"
        if overview:
            line += f"\n    _{overview}_"

        lines.append(line)

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")