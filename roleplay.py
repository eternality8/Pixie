import json
from pathlib import Path

import yaml

from tavily import TavilyClient
from langchain_openai import ChatOpenAI

from agents import create_roleplay_agent
from config import load_prompts, load_scenario_config, load_settings
from scenario_state import get_roleplay_data, initialize_scenario


settings = load_settings()
prompts = load_prompts()
base_dir = Path(__file__).resolve().parent
scenario_dir = base_dir / "Star Trek scenario"
scenario_config = load_scenario_config(scenario_dir)
initialize_scenario(scenario_config)

ai_settings = settings["ai_provider"]

chat_openai_kwargs = {
    "model": ai_settings.get("model", "z-ai/glm-4.6"),
    "api_key": ai_settings["api_key"],
    "base_url": ai_settings["base_url"],
    "verbose": False,
}

for optional_key in ("temperature", "max_tokens"):
    optional_value = ai_settings.get(optional_key)
    if optional_value is not None:
        chat_openai_kwargs[optional_key] = optional_value

model = ChatOpenAI(**chat_openai_kwargs)

tavily_client = TavilyClient(api_key=settings["tavily"]["api_key"])



roleplay: dict = get_roleplay_data()
conversation_file: Path = base_dir / "messages.yaml"


def save_messages_to_file(entries: list[dict]) -> None:
    """Persist conversation messages to YAML for continuity between runs."""
    conversation_file.parent.mkdir(parents=True, exist_ok=True)
    with conversation_file.open("w", encoding="utf-8") as file:
        yaml.safe_dump(entries, file, sort_keys=False, allow_unicode=False)


def load_messages_from_file() -> list[dict]:
    """Restore prior conversation state if available; otherwise seed with start message."""
    if conversation_file.exists() and conversation_file.stat().st_size > 0:
        try:
            with conversation_file.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: Failed to load existing messages: {exc}")
        else:
            if isinstance(data, list) and data:
                return data
            if isinstance(data, list) and not data:
                print("Warning: Conversation history file is empty; restoring default state.")

    default_messages: list[dict] = [
        {"role": "assistant", "content": roleplay.get("starting_message", "")}
    ]
    save_messages_to_file(default_messages)
    return default_messages


def add_message(entry: dict) -> None:
    """Append a message to the in-memory log and snapshot it to disk."""
    messages.append(entry)
    save_messages_to_file(messages)


messages: list[dict] = load_messages_from_file()

character_agent_instructions = prompts["character_agent_instructions"]
character_creation_agent_instructions = prompts["character_creation_agent_instructions"]
base_main_agent_instructions = prompts["main_agent_instructions"]


def build_main_agent_instructions(
    base_instructions: str,
    roleplay_config: dict,
    conversation_history: list[dict],
) -> str:
    """Append roleplay metadata and recent conversation turns to the planner prompt."""
    instructions = base_instructions.rstrip()

    instructions += "\n\n## Roleplay Details\n"
    instructions += json.dumps(roleplay_config, indent=2)

    history_lines: list[str] = []
    for entry in conversation_history:
        if entry.get("role") in {"assistant", "user"}:
            role = entry.get("role", "unknown").capitalize()
            content = entry.get("content", "")
            history_lines.append(f"{role}: {content}")

    if history_lines:
        instructions += "\n\n## Conversation History\n"
        instructions += "\n".join(history_lines)

    return instructions




# def internet_search(
#     query: str,
#     max_results: int = 5,
#     topic: Literal["general", "news", "finance"] = "general",
#     include_raw_content: bool = False,
# ):
#     """Run a web search"""
#     print(
#         f"internet_search called with query={query!r}, max_results={max_results}, topic={topic!r}, include_raw_content={include_raw_content}"
#     )
#     try:
#         return tavily_client.search(
#             query,
#             max_results=max_results,
#             include_raw_content=include_raw_content,
#             topic=topic,
#         )
#     except Exception as exc:  # noqa: BLE001
#         return f"Error: Failed to perform internet search. Details: {exc}"

main_agent_instructions = build_main_agent_instructions(
    base_instructions=base_main_agent_instructions,
    roleplay_config=roleplay,
    conversation_history=messages,
)

agent = create_roleplay_agent(
    model=model,
    main_agent_instructions=main_agent_instructions,
    character_agent_instructions=character_agent_instructions,
    character_creation_agent_instructions=character_creation_agent_instructions,
    backend_root="./temp_agent_data",
)


def process_user_turn(user_input: str) -> dict:
    """Stream a user input through the agent and return the final response message."""
    add_message({"role": "user", "content": user_input})
    results: list[dict] = []
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode="values",
    ):
        if "messages" in chunk:
            results.extend(chunk["messages"])
    final_message = results[-1]
    add_message(final_message)
    return final_message


def latest_assistant_message() -> str:
    """Return the most recent assistant message for session continuity."""
    for entry in reversed(messages):
        if entry.get("role") == "assistant":
            return str(entry.get("content", ""))
    return str(roleplay.get("starting_message", ""))


print(latest_assistant_message())
while True:
    user_input = input("You: ")
    response_message = process_user_turn(user_input)
    print(response_message)

