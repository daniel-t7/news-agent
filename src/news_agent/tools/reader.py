import httpx
import trafilatura

MAX_CHARS = 6000


def read_article(url: str) -> dict:
    """Изтегля статия и връща чистия ѝ текст без реклами и менюта."""
    try:
        r = httpx.get(
            url,
            timeout=20,
            follow_redirects=True,
            headers={"User-Agent": "news-agent/0.1"},
        )
        r.raise_for_status()
    except httpx.HTTPError as e:
        return {"error": f"Неуспешно изтегляне на статията: {e}"}

    text = trafilatura.extract(r.text, include_comments=False, include_tables=False)

    if not text:
        return {"error": "Не успях да извлека текст от страницата."}

    return {"url": url, "text": text[:MAX_CHARS], "truncated": len(text) > MAX_CHARS}


READ_ARTICLE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_article",
        # Втората част казва на модела КОГА да го ползва.
        "description": "Изтегля уеб страница на статия и връща основния ѝ текст. "
        "Ползвай го, когато заглавието е интересно и ти трябва съдържанието.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL адрес на статията"},
            },
            "required": ["url"],
        },
    },
}

# Test
if __name__ == "__main__":
    from news_agent.tools.feeds import fetch_feed

    articles = fetch_feed("https://hnrss.org/frontpage", limit=5)
    for a in articles:
        result = read_article(a["link"])
        if "text" in result:
            print(a["title"])
            print(result["text"][:500])
            break
        print("Пропускам:", a["title"], "->", result["error"])
