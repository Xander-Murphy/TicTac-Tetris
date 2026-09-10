# TicTac Tetris — Software Design Document

## Purpose

This document describes the planned software structure for TicTac Tetris and how the main components will interact.

## Components

### Game

Manages game state, score, current/next pieces, and overall game flow.

### Board

Stores the game grid and handles collision detection, placing pieces, and clearing lines.

### Piece

Stores the piece's type, position, color, and rotation. Handles movement, rotation, and dropping.

### UI/Menu

Handles menus, navigation, user input, and displaying game information.

## Component Interaction

```text
Player Input
     ↓
  UI/Menu
     ↓
    Game
     ↓
   Piece
     ↓
   Board
     ↓
Collision / Line Clearing
```

The **Game** acts as the main coordinator between the other components.

## Design Goals

* Keep responsibilities separated.
* Reduce dependencies between components.
* Make changes easier to implement.
* Support future features such as Challenges, Mission Mode, UI improvements, and Quality-of-Life updates.

## Scope

This is a **planned design** for the project. The structure may be adjusted as development and refactoring progress.
