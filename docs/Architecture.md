# TicTac Tetris — Architecture & Design

## Overview

TicTac Tetris will refactor the existing procedural Tetris code into an organized object-oriented structure. The goal is to reduce global variables, separate responsibilities, and make the game easier to maintain and expand.

## Architecture

The main components will be:

```text
              GAME
                |
       +--------+--------+
       |        |        |
     BOARD    PIECE    UI/MENU
```

* **Game** — Controls game state, score, pieces, and overall flow.
* **Board** — Manages the grid, collisions, placed pieces, and line clearing.
* **Piece** — Manages piece type, position, rotation, and movement.
* **UI/Menu** — Handles menus, navigation, input, and display.

## Design Principles

* **Encapsulation** — Keep data and related functionality together.
* **Single Responsibility** — Each component has a clear purpose.
* **Maintainability** — Make the code easier to understand and modify.
* **Extensibility** — Make it easier to add future features.

## Refactoring Goals

* Replace unnecessary global variables with class-based data.
* Separate game logic from the main game loop.
* Organize related functionality into appropriate components.
* Create a foundation for the project's planned features.
