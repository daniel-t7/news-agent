import json

from news_agent import db
from news_agent.llm import ask
from news_agent.tools import SCHEMAS, run_tool

MAX_STEPS = 10

SOURCES = [
    "https://hnrss.org/frontpage",
    "https://hnrss.org/newest?q=AI+LLM",
]

SYSTEM_PROMPT = """Ти си агент, който следи новини по зададена тема.
Работи строго по този ред:
1. Вземи статиите от всеки източник с fetch_feed.
2. Избери най-много 3 статии, свързани с темата.
3. ЗАДЪЛЖИТЕЛНО извикай read_article за всяка избрана статия.
4. Пиши резюме САМО по прочетения текст. Никога не пиши резюме само по заглавие.
5. Формат за всяка статия: заглавие, 2-3 изречения резюме, линк към статията.
Не измисляй факти. Ако статия не се чете, пропусни я и го спомени.
Пиши на правилен, естествен български. Запазвай техническите термини
(DoS, LLM, GPU, IOMMU) непреведени. Казвай "отворен код", не "отворени източници".
Преди отговор прегледай текста за правописни грешки и слепени думи."""


def run_agent(topic: str) -> str:
    messages : list = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role":"user", "content" : f"Тема: {topic}\nИзточници: " + ", ".join(SOURCES)},
    ]

    read_urls: list[str] = []

    new_found = 0
    nagged = False

    for step in range(MAX_STEPS):
        msg = ask(messages, tools=SCHEMAS)
        messages.append(msg)

        if not msg.tool_calls:
            if new_found > 0 and not read_urls and not nagged:
                nagged = True
                messages.append({
                    "role": "user",
                    "content": "Не си прочел нито една статия. Извикай read_article "
                               "за избраните статии, преди да напишеш дайджеста.",
                })
                continue

            digest = msg.content or ""
            if read_urls:
                db.save_digest(topic, digest)
                for url in read_urls:
                    db.mark_seen(url)

            return digest

        for call in msg.tool_calls:
            name = call.function.name
            args = dict(call.function.arguments)
            print(f"[стъпка {step + 1}] {name}({args})")

            result = run_tool(name, args)

            if name == "feed_fetch" and isinstance(result, list):
                result = [a for a in result if not db.is_seen(a["link"])]
                new_found += len(result)

            if name == "read_article" and isinstance(result, dict) and "text" in result:
                read_urls.append(result["url"])

            messages.append({
                "role":"tool",
                "tool_name": name,
                "content":json.dumps(result, ensure_ascii=False)
            })

    return "Достигнат лимит на стъпките без финален отговор."

#Test
if __name__ == "__main__":
    print(run_agent("изкуствен интелект и големи езикови модели"))
