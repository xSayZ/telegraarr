import httpx
from config import JELLYFIN_URL, JELLYFIN_API_KEY

HEADERS = {"Authorization": f'MediaBrowser Token="{JELLYFIN_API_KEY}"'}


async def search_library(query: str) -> list[dict]:
    """Search Jellyfin library for movies and series."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{JELLYFIN_URL}/Items",
            headers=HEADERS,
            params={
                "searchTerm": query,
                "Recursive": True,
                "IncludeItemTypes": "Movie,Series",
                "Fields": "ProductionYear,Overview",
                "Limit": 5,
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json().get("Items", [])


async def get_recently_added(limit: int = 5) -> list[dict]:
    """Get recently added items across the library."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{JELLYFIN_URL}/Items/Latest",
            headers=HEADERS,
            params={
                "Limit": limit,
                "IncludeItemTypes": "Movie,Series",
                "Fields": "ProductionYear",
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json()


async def get_library_stats() -> dict:
    """Get total movie and series counts."""
    async with httpx.AsyncClient() as client:
        movies = await client.get(
            f"{JELLYFIN_URL}/Items/Counts",
            headers=HEADERS,
            timeout=10,
        )
        movies.raise_for_status()
        return movies.json()