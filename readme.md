# Pixie Agentic Roleplaying System

## Overview
This is Pixie, an agentic roleplaying system.

It's meant to address weaknesses in programs like sillytavern that rely on inserting bunch of text into the context and having the AI figure it out. This approach has several weaknesses from limited context side, attention and generally decreasing performance/accuracy of LLMs as the context fills. Pixie aims to fix this by using deep agents. Instead of relyign on everything being in context all the time, Pixie aims to keep the context fairly small, and instead adds ability for the AI to use tools and subagents to search for relevant information and isolate contexts from each other to enable better quality and memory, as well as improve on things like 'omniscient' characters.

Pixie is aimed towards scenario based roleplay where you control one character and tell the ai what you want to do, and the AI then controls the other characters and writes up a description of what happens. It will not support the traditional character cards, because the nature of Pixie requires the character data to be organized differently. However it supports individual character files and scenario files, all in yaml format that is easy to edit and share.

Pixie is still heavily WIP.

## Key Ideas
- Deep agent architecture keeps live context small while deferring to on-demand tool calls for memory.
- Scenario-first workflow focuses on YAML-driven worlds and characters instead of static character cards.
- Modular tools and subagents allow focused retrieval of setting, character, and continuity details.

## Getting Started
1. Ensure Python 3.10+ is available on your system (`python --version`).
2. Create and activate a virtual environment:
	- `python -m venv .venv`
	- ` .\.venv\Scripts\Activate`
3. Install dependencies (add them to `requirements.txt` when defined) with `pip install -r requirements.txt`.
4. Configure your scenario and character YAML files (see the sections below).
5. Run `roleplay.py` to launch a CLI-driven session or hook the agents into your own UI layer.


## TODO:
- Implement basic roleplay interfaces (in progress)
- Implement all tools and subagents (in progress)
- Add better example scenarios
- Write better prompts
- Implement scenario creator
- import tool for character cards?
- Web gui (nicegui?)
- docker image
- better instructions

