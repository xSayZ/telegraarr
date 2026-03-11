import httpx
from telegraarr.config import (
    SONARR_URL, SONARR_API_KEY,
    SONARR_ANIME_URL, SONARR_ANIME_API_KEY,
    RADARR_URL, RADARR_API_KEY,
)


async def _get_queue(base_url: str, api_key: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{base_url}/api/v3/queue",
            headers={"X-Api-Key": api_key},
            params={"pageSize": 50, "includeUnknownMovieItems": True},
            timeout=10,
        )
        r.raise_for_status()
        return r.json().get("records", [])


async def _get_disk_space(base_url: str, api_key: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{base_url}/api/v3/diskspace",
            headers={"X-Api-Key": api_key},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()


async def get_sonarr_queue() -> list[dict]:
    return await _get_queue(SONARR_URL, SONARR_API_KEY)


async def get_radarr_queue() -> list[dict]:
    return await _get_queue(RADARR_URL, RADARR_API_KEY)


async def get_sonarr_anime_queue() -> list[dict]:
    if not SONARR_ANIME_URL or not SONARR_ANIME_API_KEY:
        return []
    return await _get_queue(SONARR_ANIME_URL, SONARR_ANIME_API_KEY)


async def get_all_queues() -> dict[str, list[dict]]:
    """Fetch all queues, labelled by source."""
    sonarr = await get_sonarr_queue()
    radarr = await get_radarr_queue()
    anime = await get_sonarr_anime_queue()

    return {
        "sonarr": sonarr,
        "radarr": radarr,
        "anime": anime,
    }


async def get_disk_space() -> list[dict]:
    """Get disk space from Sonarr (represents shared storage)."""
    return await _get_disk_space(SONARR_URL, SONARR_API_KEY)