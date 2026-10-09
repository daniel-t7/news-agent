# File ``reader.py``

```python
# httpx изтегля страницата по HTTP.
import httpx
# trafilatura вади основния текст от HTML и маха менюта, реклами и подножия.
import trafilatura

# Константа: максимум знаци, които връщаме. Дългите статии биха препълнили
# контекста на модела (колко текст може да "държи" наведнъж).
MAX_CHARS = 6000


# Приема адрес на статия, връща речник: или с текста, или с ключ "error".
def read_article(url: str) -> dict:
    """Изтегля статия и връща чистия ѝ текст без реклами и менюта."""
    # Хващаме мрежови грешки, за да не се срине агентът.
    try:
        # Същата заявка като във feeds.py, но с по-дълъг таймаут (20 сек),
        # защото страниците на статиите са по-тежки от RSS фийдовете.
        r = httpx.get(url, timeout=20, follow_redirects=True,
                      headers={"User-Agent": "news-agent/0.1"})
        # Хвърля изключение при статус 4xx/5xx (404, 403, 500...).
        r.raise_for_status()
    except httpx.HTTPError as e:
        # Грешката се връща като данни, за да я види моделът.
        return {"error": f"Неуспешно изтегляне на статията: {e}"}

    # Вади основния текст от HTML. Връща None, ако не намери нищо
    # (например страницата е PDF, пейуол или се рендира с JavaScript).
    text = trafilatura.extract(r.text, include_comments=False, include_tables=False)
    # "if not text" хваща и None, и празен низ.
    if not text:
        return {"error": "Не успях да извлека текст от страницата."}

    # text[:MAX_CHARS] е срез: първите 6000 знака.
    # "truncated" казва на модела дали текстът е отрязан.
    return {"url": url, "text": text[:MAX_CHARS], "truncated": len(text) > MAX_CHARS}


# Описание на инструмента за модела (както във feeds.py).
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


# Тест: изпълнява се само при директно пускане на файла.
if __name__ == "__main__":
    # Импорт на нашия инструмент от другия файл (пълен път от пакета).
    from news_agent.tools.feeds import fetch_feed

    # Взимаме 5 статии от фийда.
    articles = fetch_feed("https://hnrss.org/frontpage", limit=5)
    # Минаваме през тях една по една.
    for a in articles:
        result = read_article(a["link"])
        # Ако в резултата има ключ "text", четенето е успешно.
        if "text" in result:
            print(a["title"])
            # Печатаме първите 500 знака, не цялата статия.
            print(result["text"][:500])
            # Спираме на първата успешна статия.
            break
        # Иначе показваме защо е пропусната и пробваме следващата.
        print("Пропускам:", a["title"], "->", result["error"])
```
