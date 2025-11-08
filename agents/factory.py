from __future__ import annotations

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from tools import ALL_TOOLS, CHARACTER_AGENT_TOOLS, CHARACTER_CREATION_TOOLS


def build_character_subagent(instructions: str) -> dict:
    """Return the configuration for the character query subagent."""
    return {
        "name": "character_subagent",
        "description": "Used to answer questions about characters in a roleplay scenario.",
        "system_prompt": instructions,
        "tools": CHARACTER_AGENT_TOOLS,
    }


def build_character_creation_subagent(instructions: str) -> dict:
    """Return the configuration for the character creation subagent."""
    return {
        "name": "character_creation_subagent",
        "description": "Used to design and register new characters for the scenario.",
        "system_prompt": instructions,
        "tools": CHARACTER_CREATION_TOOLS,
    }


def build_subagents(
    character_agent_instructions: str,
    character_creation_agent_instructions: str,
) -> list[dict]:
    """Assemble the configured subagents used by the main agent."""
    return [
        build_character_subagent(character_agent_instructions),
        build_character_creation_subagent(character_creation_agent_instructions),
    ]


def create_roleplay_agent(
    model,
    main_agent_instructions: str,
    character_agent_instructions: str,
    character_creation_agent_instructions: str,
    backend_root: str = "./temp_agent_data",
):
    """Create the composite Deep Agent for the roleplay scenario."""
    subagents = build_subagents(
        character_agent_instructions=character_agent_instructions,
        character_creation_agent_instructions=character_creation_agent_instructions,
    )

    return create_deep_agent(
        subagents=subagents,
        model=model,
        tools=ALL_TOOLS,
        system_prompt=main_agent_instructions,
        backend=FilesystemBackend(root_dir=backend_root),
    )


__all__ = [
    "build_character_creation_subagent",
    "build_character_subagent",
    "build_subagents",
    "create_roleplay_agent",
]
