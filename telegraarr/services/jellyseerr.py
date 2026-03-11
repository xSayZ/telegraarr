import httpx
from config import JELLYSEERR_URL, JELLYSEERR_API_KEY

HEADERS = {"X-Api-Key": JELLYSEERR_API_KEY}


async def search_requests(query: str) -> list[dict]:
    """Search requests by title."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{JELLYSEERR_URL}/api/v1/request",
            headers=HEADERS,
            params={"take": 20, "skip": 0, "sort": "added", "filter": "all"},
            timeout=10,
        )
        r.raise_for_status()
        results = r.json().get("results", [])

    query_lower = query.lower()
    return [
        req for req in results
        if query_lower in (req.get("media", {}).get("originalTitle") or "").lower()
        or query_lower in (req.get("media", {}).get("title") or "").lower()
    ]


async def get_request_counts() -> dict:
    """Get request counts by status."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{JELLYSEERR_URL}/api/v1/request/count",
            headers=HEADERS,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()


async def get_user_by_email(email: str) -> dict | None:
    """Look up a Jellyseerr user by email to validate registration."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{JELLYSEERR_URL}/api/v1/user",
            headers=HEADERS,
            params={"take": 50, "skip": 0},
            timeout=10,
        )
        r.raise_for_status()
        users = r.json().get("results", [])

    email_lower = email.lower()
    return next(
        (u for u in users if (u.get("email") or "").lower() == email_lower),
        None
    )