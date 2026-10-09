from .feeds import FETCH_FEED_SCHEMA, fetch_feed
from .reader import READ_ARTICLE_SCHEMA, read_article

TOOLS = {
    "fetch_feed": fetch_feed,
    "read_article": read_article,
}

SCHEMAS = [FETCH_FEED_SCHEMA, READ_ARTICLE_SCHEMA]


def run_tool(name: str, arguments: dict) -> dict | list:
    if name not in TOOLS:
        return {"error": f"Непознат инструмент: {name}"}
    try:
        return TOOLS[name](**arguments)
    except TypeError as e:
        return {"error": f"Грешни аргументи за {name}: {e}"}
    except Exception as e:
        return {"error": f"Грешка в {name}: {e}"}
