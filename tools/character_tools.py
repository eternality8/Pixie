from __future__ import annotations

import json

from scenario_state import (
    get_character_profile,
    list_characters,
    update_character_profile,
)


def list_characters_tool() -> str:
    """Tool: list known character identifiers."""
    print("list_characters_tool called with no parameters")
    try:
        return json.dumps(list_characters())
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to list characters. Details: {exc}"


def get_character_profile_tool(input_str: str) -> str:
    """Tool: fetch a character profile based on the provided identifier."""
    print(f"get_character_profile_tool called with input_str={input_str!r}")
    try:
        character_id = ""
        payload = None
        stripped = input_str.strip()

        if stripped:
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                character_id = stripped
        else:
            payload = {}

        if payload is not None:
            character_id = str(payload.get("character_id", "")).strip()

        if not character_id:
            return "Error: provide a character_id."
        try:
            profile = get_character_profile(character_id)
        except ValueError:
            return f"Error: Could not find character '{character_id}'."
        return json.dumps(profile)
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to fetch character profile. Details: {exc}"


def update_character_profile_tool(input_str: str) -> str:
    """Tool: update a character field using JSON payload."""
    print(f"update_character_profile_tool called with input_str={input_str!r}")
    try:
        try:
            payload = json.loads(input_str)
        except json.JSONDecodeError:
            return "Error: Please provide a JSON payload that includes character_id, field, and value."

        character_id = str(payload.get("character_id", "")).strip()
        field = str(payload.get("field", "")).strip()
        value = str(payload.get("value", ""))

        if not character_id or not field:
            return "Error: The payload must include both character_id and field."

        updated = update_character_profile(character_id, field, value)
        return json.dumps(updated)
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to update character profile. Details: {exc}"
