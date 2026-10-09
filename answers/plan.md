# Plan

1. ``llm.py``: връзка с Ollama
2. ``tools/feeds.py``: четене на RSS
3. ``tools/reader.py``: четене на статия
4. ``tools/__init__.py``: регистър на инструментите
5. ``agent.py``: цикълът с tool calling (без памет)
6. ``db.py``: SQLite памет за видяни статии, включена в агента
7. Запис на дайджест във файл и пускане с ``cron``
