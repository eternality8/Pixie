from .character_tools import (
    get_character_profile_tool,
    list_characters_tool,
    update_character_profile_tool,
)
from .scenario_tools import (
    get_current_location_tool,
    get_roleplay_overview_tool,
    list_roleplay_characters_tool,
    move_roleplay_character_tool,
    update_current_location_tool,
)

CHARACTER_TOOLS = [
    list_characters_tool,
    get_character_profile_tool,
    update_character_profile_tool,
]

SCENARIO_TOOLS = [
    list_roleplay_characters_tool,
    move_roleplay_character_tool,
    get_roleplay_overview_tool,
    get_current_location_tool,
    update_current_location_tool,
]

CHARACTER_AGENT_TOOLS = CHARACTER_TOOLS + SCENARIO_TOOLS

CHARACTER_CREATION_TOOLS = [
    list_characters_tool,
    get_roleplay_overview_tool,
    get_current_location_tool,
    update_current_location_tool,
    update_character_profile_tool,
    move_roleplay_character_tool,
]

ALL_TOOLS = CHARACTER_AGENT_TOOLS

__all__ = [
    "ALL_TOOLS",
    "CHARACTER_AGENT_TOOLS",
    "CHARACTER_CREATION_TOOLS",
    "CHARACTER_TOOLS",
    "get_character_profile_tool",
    "get_current_location_tool",
    "get_roleplay_overview_tool",
    "list_characters_tool",
    "list_roleplay_characters_tool",
    "move_roleplay_character_tool",
    "update_character_profile_tool",
    "update_current_location_tool",
]
