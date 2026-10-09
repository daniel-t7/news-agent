import feedparser
import httpx


def fetch_feed(url: str, limit: int = 10) -> list[dict] | dict:
    """Връща последните статии от RSS фийд: заглавие, линк, дата."""
    try:
        r = httpx.get(
            url,
            timeout=15,
            follow_redirects=True,
            headers={"User-Agent": "news-agent/0.1"},
        )
        r.raise_for_status()
    except httpx.HTTPError as e:
        return {"error": f"Неуспешно изтегляне на фийда: {e}"}
    feed = feedparser.parse(r.text)
    return [
        {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
        }
        for entry in feed.entries[:limit]
    ]


FETCH_FEED_SCHEMA = {
    "type": "function",
    "function": {
        "name": "fetch_feed",
        "description": "Взема последните статии от RSS фийд. "
        "Връща списък със заглавие, линк и дата на публикация.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL адрес на RSS фийда"},
                "limit": {
                    "type": "integer",
                    "description": "Максимален брой статии (по подразбиране 10)",
                },
            },
            "required": ["url"],
        },
    },
}

# Test
if __name__ == "__main__":
    import json
    result = fetch_feed("https://hnrss.org/frontpage", limit=3)
    print(json.dumps(result, indent=2, ensure_ascii=False))
