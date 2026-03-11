from telegram import Update
from telegram.ext import ContextTypes
from telegraarr.auth import require_auth
from telegraarr.services.arr import get_all_queues, get_disk_space
from telegraarr.services.jellyseerr import get_request_counts
from telegraarr.services.jellyfin import get_recently_added, get_library_stats


def _format_disk(disks: list[dict]) -> str:
    lines = []
    for disk in disks:
        label = disk.get("label") or disk.get("path", "?")
        free = disk.get("freeSpace", 0) / (1024 ** 3)
        total = disk.get("totalSpace", 0) / (1024 ** 3)
        if total == 0:
            continue
        used_pct = int((1 - free / total) * 100)
        filled = used_pct // 10
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(
            f"`{bar}` {used_pct}%\n"
            f"    {free:.1f} GB free of {total:.1f} GB ({label})"
        )
    return "\n".join(lines) if lines else "N/A"


def _format_recently_added(items: list[dict]) -> str:
    if not items:
        return "Nothing recently added."
    lines = []
    for item in items:
        itype = "🎬" if item.get("Type") == "Movie" else "📺"
        name = item.get("Name", "Unknown")
        year = item.get("ProductionYear", "")
        lines.append(f"{itype} *{name}*{f' ({year})' if year else ''}")
    return "\n".join(lines)


@require_auth
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Fetching status...")

    try:
        queues = await get_all_queues()
        disks = await get_disk_space()
        counts = await get_request_counts()
        recently_added = await get_recently_added(limit=5)
        library_stats = await get_library_stats()
    except Exception as e:
        await update.message.reply_text(f"❌ Couldn't fetch status: {e}")
        return

    all_items = [
        item
        for items in queues.values()
        for item in items
    ]

    stalled = sum(
        1 for item in all_items
        if item.get("trackedDownloadStatus", "").lower() == "warning"
    )

    movies_count = library_stats.get("MovieCount", "?")
    series_count = library_stats.get("SeriesCount", "?")
    episode_count = library_stats.get("EpisodeCount", "?")

    lines = [
        "*Server status*\n",

        "*📥 Downloads*",
        f"Active: {len(all_items)}",
        f"Stalled: {stalled}",
        "",

        "*📋 Requests*",
        f"Pending: {counts.get('pending', 0)}",
        f"Approved: {counts.get('approved', 0)}",
        f"Available: {counts.get('available', 0)}",
        "",

        "*📚 Library*",
        f"🎬 {movies_count} movies",
        f"📺 {series_count} series ({episode_count} episodes)",
        "",

        "*🆕 Recently added*",
        _format_recently_added(recently_added),
        "",

        "*💾 Disk space*",
        _format_disk(disks),
    ]

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")