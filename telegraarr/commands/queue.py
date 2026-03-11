from telegram import Update
from telegram.ext import ContextTypes
from auth import require_auth
from services.arr import get_all_queues


def _format_size(bytes: float) -> str:
    gb = bytes / (1024 ** 3)
    mb = bytes / (1024 ** 2)
    if gb >= 1:
        return f"{gb:.1f} GB"
    return f"{mb:.0f} MB"


def _format_progress(item: dict) -> str:
    size_left = item.get("sizeleft", 0)
    size_total = item.get("size", 0)

    if size_total > 0:
        pct = int((1 - size_left / size_total) * 100)
        filled = pct // 10
        bar = "█" * filled + "░" * (10 - filled)
        return f"`{bar}` {pct}% ({_format_size(size_left)} left)"
    return "unknown progress"


def _format_item(item: dict, source: str) -> str:
    title = item.get("title", "Unknown")
    status = item.get("status", "").lower()
    tracked = item.get("trackedDownloadStatus", "").lower()
    tracked_state = item.get("trackedDownloadState", "").lower()

    icon = {"sonarr": "📺", "radarr": "🎬", "anime": "🎌"}.get(source, "❓")

    progress = _format_progress(item)

    # Detect problem states
    if tracked == "warning":
        state_label = "⚠️ *stalled*"
    elif tracked_state == "importpending":
        state_label = "📦 *import pending*"
    elif status == "queued":
        state_label = "🕐 *queued*"
    else:
        state_label = ""

    line = f"{icon} *{title}*\n    {progress}"
    if state_label:
        line += f" — {state_label}"

    return line


@require_auth
async def queue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        queues = await get_all_queues()
    except Exception as e:
        await update.message.reply_text(f"❌ Couldn't reach arr services: {e}")
        return

    all_items = [
        (item, source)
        for source, items in queues.items()
        for item in items
    ]

    if not all_items:
        await update.message.reply_text("✅ Nothing currently downloading.")
        return

    stalled = sum(
        1 for item, _ in all_items
        if item.get("trackedDownloadStatus", "").lower() == "warning"
    )

    lines = [f"*Download queue* — {len(all_items)} item{'s' if len(all_items) != 1 else ''}"]
    if stalled:
        lines[0] += f", ⚠️ {stalled} stalled"
    lines.append("")

    for item, source in all_items:
        lines.append(_format_item(item, source))

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")