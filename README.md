# Maze Generator and Solver

This project generates and solves a maze using Python and Pygame.

## Features

- Random maze generation
- DFS stack-based algorithm
- Dynamic wall removal animation
- Maze solving with backtracking
- Red path visualization
- Blue dead-end visualization

## Technologies

- Python
- Pygame

## How the Maze Works

The maze is generated using a Depth-First Search (DFS) algorithm with a stack.

An invisible “mouse” visits cells and randomly removes walls between unvisited neighbors.

When the mouse reaches a dead end, it backtracks using the stack until it finds another possible path.

## Assignment Requirements Covered

- Rectangular maze generation
- Random path generation
- Stack-based DFS algorithm
- Maze traversal and solving
- Dynamic graphical visualization
- Backtracking solver

## Solver

The maze solver also uses backtracking to find a path from start to end.

- Red cells = current solution path
- Blue cells = dead ends

## Installation

Install pygame:

```bash
pip install pygame

