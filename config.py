from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml


@lru_cache(maxsize=1)
def load_settings(settings_path: Path = Path(__file__).with_name("settings.yaml")) -> dict:
    """Read configuration values for external services."""
    return yaml.safe_load(settings_path.read_text(encoding="utf-8"))


def _read_yaml(file_path: Path) -> dict:
    """Return parsed YAML content from a file path."""
    return yaml.safe_load(file_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_prompts(prompts_path: Path = Path(__file__).with_name("prompts.yaml")) -> dict:
    """Load system prompt text used by the agents."""
    return _read_yaml(prompts_path)


@lru_cache(maxsize=None)
def load_scenario_config(scenario_dir: Path) -> dict:
    """Load the roleplay setting and individual character profiles from a folder."""
    base_path = Path(scenario_dir)
    if not base_path.is_dir():
        raise FileNotFoundError(f"Scenario directory '{base_path}' not found.")

    setting_file: Optional[Path] = None
    for candidate in ("setting.yaml", "setting.yml", "roleplay.yaml", "roleplay.yml"):
        candidate_path = base_path / candidate
        if candidate_path.is_file():
            setting_file = candidate_path
            break

    if setting_file is None:
        raise FileNotFoundError(
            "No setting file found. Expected one of setting.yaml, setting.yml, roleplay.yaml, or roleplay.yml."
        )

    setting_data = _read_yaml(setting_file) or {}
    if not isinstance(setting_data, dict):
        raise ValueError(f"Setting file '{setting_file}' must contain a mapping at the top level.")

    roleplay_data = setting_data.get("roleplay", setting_data)

    characters_dir = base_path / "characters"
    characters: dict[str, dict] = {}
    alias_map: dict[str, str] = {}
    if characters_dir.is_dir():
        for char_file in sorted(characters_dir.glob("*.y*ml")):
            char_data = _read_yaml(char_file) or {}
            if not isinstance(char_data, dict):
                raise ValueError(f"Character file '{char_file}' must contain a mapping at the top level.")

            character_id = str(char_file.stem)
            characters[character_id] = char_data
            alias_map[character_id.casefold()] = character_id

            for alias_key in ("id", "short_name"):
                alias_value = char_data.get(alias_key)
                alias = str(alias_value).strip() if alias_value is not None else ""
                if alias:
                    alias_map[alias.casefold()] = character_id

    return {
        "roleplay": roleplay_data,
        "characters": characters,
        "character_alias_map": alias_map,
    }
