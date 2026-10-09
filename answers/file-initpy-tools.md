# File ``__init__.py`` for tools

```python
# Вкарваме функциите и схемите им от отделните файлове.
# Точката значи "от същата папка" (относителен импорт).
from .feeds import fetch_feed, FETCH_FEED_SCHEMA
from .reader import read_article, READ_ARTICLE_SCHEMA

# Речник: име на инструмента -> функцията. Името трябва да е същото като
# "name" в схемата, защото моделът ни връща именно името.
TOOLS = {
    "fetch_feed": fetch_feed,
    "read_article": read_article,
}

# Списък със схемите, който подаваме на модела (параметъра tools в ask()).
SCHEMAS = [FETCH_FEED_SCHEMA, READ_ARTICLE_SCHEMA]


# Изпълнява инструмент по име. name и arguments идват директно от модела.
def run_tool(name: str, arguments: dict) -> dict | list:
    # Моделът понякога измисля несъществуващ инструмент.
    if name not in TOOLS:
        return {"error": f"Непознат инструмент: {name}"}
    try:
        # **arguments разпакетира речника в именувани аргументи:
        # {"url": "x", "limit": 3} става fetch_feed(url="x", limit=3).
        return TOOLS[name](**arguments)
    except TypeError as e:
        # Грешни или липсващи аргументи (напр. моделът е измислил параметър).
        return {"error": f"Грешни аргументи за {name}: {e}"}
    except Exception as e:
        # Всяка друга неочаквана грешка. Не искаме един инструмент да убие агента.
        return {"error": f"Грешка в {name}: {e}"}
```
