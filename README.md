# TicTac Tetris

TicTac Tetris is a team project focused on improving and expanding a bare-bones Tetris game using better software design and new gameplay features.

## Team

* **Xander Murphy** — Architecture, Design & Refactoring
* **Joseph Gallucci** — Mission Mode & Quality-of-Life
* **Tanner Andrews** — UI Overhaul & Challenges

## Features

* **UI Overhaul** — Improved menus, visuals, and usability
* **Challenges** — Unique gameplay challenges and effects
* **Mission Mode** — Objective-based Tetris gameplay
* **Quality-of-Life** — Quick drop, wall kicks, high scores, etc.

## Setup

### Requirements

* Python
* uv
* Pygame

### Run

```bash
uv venv
uv add pygame
uv run src/tetris.py
```

## Development Plan

**Sprint 1**

* Project setup
* Analyze and refactor existing code
* Begin feature development

**Sprint 2**

* Complete planned features
* Polish the game
* Add final improvements

## Architecture

The project is being refactored from procedural code into an organized object-oriented structure using:

**Game = Board + Piece + UI/Menu**

The goal is to improve maintainability, organization, and extensibility.

**Status:** Work in Progress
