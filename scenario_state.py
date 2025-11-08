from __future__ import annotations

from typing import Literal


characters: dict[str, dict] = {}
roleplay: dict = {}
character_alias_map: dict[str, str] = {}


def initialize_scenario(config: dict) -> None:
    """Load scenario data into module-level state for reuse."""
    global characters, roleplay, character_alias_map
    characters = config.get("characters", {})
    roleplay = config.get("roleplay", {})
    character_alias_map = config.get("character_alias_map", {})


def get_roleplay_data() -> dict:
    """Return the mutable roleplay configuration."""
    return roleplay


def _register_character_alias(alias: str, canonical_id: str) -> None:
    key = str(alias or "").strip()
    if not key:
        return
    character_alias_map[key.casefold()] = canonical_id


def _resolve_character_id(character_id: str) -> str:
    key = str(character_id or "").strip()
    if not key:
        return key
    return character_alias_map.get(key.casefold(), key)


def list_characters() -> list[str]:
    """Return identifiers for all known characters."""
    return sorted(characters.keys())


def get_character_profile(character_id: str) -> dict:
    """Fetch the full profile for a specific character."""
    canonical_id = _resolve_character_id(character_id)
    if canonical_id not in characters:
        raise ValueError(f"Character '{character_id}' not found.")
    return characters[canonical_id]


def update_character_profile(character_id: str, field: str, value: str) -> dict:
    """Update or create a character entry and return the updated profile."""
    canonical_id = _resolve_character_id(character_id)
    target_id = canonical_id or str(character_id).strip()
    if not target_id:
        raise ValueError("Character identifier cannot be empty.")

    if target_id not in characters:
        record = characters.setdefault(
            target_id,
            {
                "name": target_id,
                "description": "",
                "physical_description": "",
                "personality_description": "",
            },
        )
        _register_character_alias(target_id, target_id)
    else:
        record = characters[target_id]

    _register_character_alias(character_id, target_id)

    record[field] = value

    if field in {"short_name", "id"}:
        _register_character_alias(value, target_id)

    return record


def get_current_location() -> str:
    """Return the current location within the roleplay scenario."""
    return str(roleplay.get("current_location", ""))


def set_current_location(location: str) -> str:
    """Persist a new current location and return it."""
    roleplay["current_location"] = location
    return location


def move_roleplay_character(character_id: str, target_category: Literal["present", "off_stage"]) -> dict:
    """Move a character between presence categories and return updated lists."""
    canonical_id = _resolve_character_id(character_id)
    if canonical_id not in characters:
        raise ValueError(f"Character '{character_id}' not found.")
    character_id = canonical_id

    if "present_characters" not in roleplay:
        legacy_present = roleplay.get("characters", [])
        roleplay["present_characters"] = list(legacy_present)
    present = roleplay["present_characters"]
    if not isinstance(present, list):
        present = list(present)
        roleplay["present_characters"] = present

    off_stage = roleplay.setdefault("off_stage_characters", [])
    if not isinstance(off_stage, list):
        off_stage = list(off_stage)
        roleplay["off_stage_characters"] = off_stage

    roleplay.pop("characters", None)

    if target_category == "present":
        if character_id not in present:
            present.append(character_id)
        if character_id in off_stage:
            off_stage.remove(character_id)
    elif target_category == "off_stage":
        if character_id not in off_stage:
            off_stage.append(character_id)
        if character_id in present:
            present.remove(character_id)
    else:
        raise ValueError("target_category must be 'present' or 'off_stage'.")

    return {
        "present_characters": list(present),
        "off_stage_characters": list(off_stage),
    }
