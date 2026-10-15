import argparse


def main() -> None:
    from news_agent.agent import run_agent

    parser = argparse.ArgumentParser(
        prog="news-agent",
        description="Следи новини по зададена тема и пише дайджест.",
    )
    parser.add_argument(
        "topic",
        nargs="?",
        default="изкуствен интелект и големи езикови модели",
        help="Тема, по която да се търсят новини.",
    )
    args = parser.parse_args()
    print(run_agent(args.topic))


if __name__ == "__main__":
    main()
