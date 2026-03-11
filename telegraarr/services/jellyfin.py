import httpx
from telegraarr.config import JELLYFIN_URL, JELLYFIN_API_KEY

HEADERS = {"Authorization": f'MediaBrowser Token="{JELLYFIN_API_KEY}"'}

async def search_library(query: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{JELLYFIN_URL}/Items",
            headers=HEADERS,
            params={
                "searchTerm": query,
                "Recursive": True,
                "IncludeItemTypes": "Movie,Series",
                "Fields": "ProductionYear,Overview,RecursiveItemCount",
                "Limit": 5,
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json().get("Items", [])


async def get_recently_added(limit: int = 5) -> list[dict]:
    async with httpx.AsyncClient() as client:
        # First get the admin user ID
        users = await client.get(
            f"{JELLYFIN_URL}/Users",
            headers=HEADERS,
            timeout=10,
        )
        users.raise_for_status()
        user_id = users.json()[0]["Id"]

        r = await client.get(
            f"{JELLYFIN_URL}/Users/{user_id}/Items/Latest",
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