from telegram import Update
from telegram.ext import ContextTypes
from telegraarr.auth import require_auth
from telegraarr.services.jellyseerr import search_requests

STATUS_MAP = {
    1: "⏳ Pending",
    2: "✅ Approved",
    3: "❌ Declined",
    4: "🔄 Processing",
    5: "🎉 Available",
}

MEDIA_MAP = {
    "movie": "🎬",
    "tv": "📺",
}


@require_auth
async def requests_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage: /requests <query>\n"
            "Example: /requests breaking bad"
        )
        return

    query = " ".join(context.args)

    try:
        results = await search_requests(query)
    except Exception as e:
        await update.message.reply_text(f"❌ Couldn't reach Jellyseerr: {e}")
        return

    if not results:
        await update.message.reply_text(f'❌ No requests found matching "{query}".')
        return

    lines = [f'*Requests matching "{query}":*\n']

    for req in results:
        media = req.get("media", {})
        title = media.get("originalTitle") or media.get("title") or "Unknown"
        year = (media.get("releaseDate") or "")[:4]
        status = STATUS_MAP.get(req.get("status"), "❓ Unknown")
        mtype = MEDIA_MAP.get(req.get("type"), "❓")
        requested_by = req.get("requestedBy", {}).get("displayName", "Unknown")

        lines.append(
            f"{mtype} *{title}*{f' ({year})' if year else ''}\n"
            f"    Status: {status} — Requested by: {requested_by}"
        )

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")