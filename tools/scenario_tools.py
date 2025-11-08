from __future__ import annotations

import json

from scenario_state import (
    get_current_location,
    get_roleplay_data,
    move_roleplay_character,
    set_current_location,
)


def list_roleplay_characters_tool() -> str:
    """Tool: list character identifiers currently present in the roleplay."""
    print("list_roleplay_characters_tool called with no parameters")
    try:
        roleplay = get_roleplay_data()
        present = roleplay.get("present_characters")
        if present is None:
            present = roleplay.get("characters", [])
        return json.dumps(present)
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to list roleplay characters. Details: {exc}"


def get_roleplay_overview_tool() -> str:
    """Tool: provide an overview summary of the roleplay setup."""
    print("get_roleplay_overview_tool called with no parameters")
    try:
        roleplay = get_roleplay_data()
        overview = {
            "setting": roleplay.get("setting", ""),
            "style and plot": roleplay.get("style and plot", ""),
            "present_characters": roleplay.get("present_characters", roleplay.get("characters", [])),
            "off_stage_characters": roleplay.get("off_stage_characters", []),
            "player_character": roleplay.get("player_character", ""),
        }
        return json.dumps(overview)
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to create roleplay overview. Details: {exc}"


def get_current_location_tool() -> str:
    """Tool: report the current location within the roleplay."""
    print("get_current_location_tool called with no parameters")
    try:
        location = get_current_location()
        if not location:
            return "Error: Current location is not set."
        return json.dumps({"current_location": location})
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to get current location. Details: {exc}"


def update_current_location_tool(input_str: str) -> str:
    """Tool: update the current location using plain text or JSON payload."""
    print(f"update_current_location_tool called with input_str={input_str!r}")
    try:
        stripped = input_str.strip()
        location = ""

        if stripped:
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                location = stripped
            else:
                location = str(payload.get("current_location", "")).strip()

        if not location:
            return "Error: Provide a current_location value as text or JSON."

        updated_location = set_current_location(location)
        return json.dumps({"current_location": updated_location})
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to update current location. Details: {exc}"


def move_roleplay_character_tool(input_str: str) -> str:
    """Tool: move a character between present and off-stage categories."""
    print(f"move_roleplay_character_tool called with input_str={input_str!r}")
    try:
        try:
            payload = json.loads(input_str)
        except json.JSONDecodeError:
            return "Error: Provide a JSON payload with character_id and target_category."

        character_id = str(payload.get("character_id", "")).strip()
        target_category = str(payload.get("target_category", "")).strip().lower().replace(" ", "_")

        if not character_id or not target_category:
            return "Error: The payload must include character_id and target_category."

        normalized_target = ""
        if target_category in {"present", "present_characters", "current", "on_stage"}:
            normalized_target = "present"
        elif target_category in {"off_stage", "offstage", "off_stage_characters", "absent"}:
            normalized_target = "off_stage"
        else:
            return "Error: target_category must be 'present' or 'off_stage'."

        try:
            updated_categories = move_roleplay_character(character_id, normalized_target)
        except ValueError as exc:
            return f"Error: {exc}"

        response = {
            "character_id": character_id,
            "target_category": normalized_target,
            "present_characters": updated_categories["present_characters"],
            "off_stage_characters": updated_categories["off_stage_characters"],
        }
        return json.dumps(response)
    except Exception as exc:  # noqa: BLE001
        return f"Error: Failed to move roleplay character. Details: {exc}"
