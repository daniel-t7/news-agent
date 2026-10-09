from ollama import chat

MODEL = "qwen3:8b"


def ask(messages: list[dict], tools: list[dict] | None = None):
    """Праща съобщенията към модела и връща неговото съобщение
    (с полета .content и .tool_calls)."""
    response = chat(model=MODEL, messages=messages, tools=tools)
    return response.message


if __name__ == "__main__":
    msg = ask([{"role": "user", "content": "Кажи здравей на български."}])
    print(msg.content)
