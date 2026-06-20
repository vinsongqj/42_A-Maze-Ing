"""
MAZE GENERATOR

This file generates the maze structure by using the
Depth-First Search Algorithm (DFS). It also handles the
masking of the 42 logo within the walls of the maze.
"""

import random
from typing import List, Tuple, Set, Optional
from .constants import MOVEMENTS, NORTH, EAST, SOUTH, WEST, OPPOSITES
from .solver import MazeSolver
from maze_gen.validator import ConfigError
import time


class MazeGenerator:

    """
    The class that implements the DFS algorithm using
    Recursive Backtracker logic. It carves a path until
    it hits a dead end, and backtracks to the last visited
    junction.
    """

    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None) -> None:

        """
        Sets up basic size and random settings for new maze.
        """

        self.width = width
        self.height = height
        self.error_msg = ""
        self.grid: List[List[int]] = []
        self.locked_cells: Set[Tuple[int, int]] = set()
        self.perfect: bool = True
        if seed is not None:
            random.seed(seed)

    def _apply_42(self) -> None:

        """
        Calculates exactly which cells (x, y) should
        be solid blocks to form the '42' pattern and
        locks them so the generator doesn't carve
        through them.
        """

        self.locked_cells.clear()
        mx = self.width // 2
        my = self.height // 2
        offsets = [

            # 4
            (-4, -2), (-4, -1), (-4, 0), (-3, 0), (-2, 0), (-2, 1), (-2, 2),

            # 2
            (0, -2), (1, -2), (2, -2), (2, -1), (2, 0), (1, 0),
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 2)
        ]

        for dx, dy in offsets:
            tx = mx + dx
            ty = my + dy
            if 0 <= tx < self.width and 0 <= ty < self.height:
                self.locked_cells.add((tx, ty))

    def generate(self, perfect: bool = True, use_logo: bool = True) -> None:

        """
        Carves the maze using recursive backtracking.

        1. Starts at (0, 0) and moves to a random unvisited neighbor
        2. Uses a stack to backtrack when hitting a dead end
        3. If not perfect, removes walls to create loops.
        """

        self.locked_cells.clear()
        self.perfect = perfect
        min_width = 8
        min_height = 7
        if use_logo:
            if self.width < 2 or self.height < 2:
                raise ConfigError("Maze is too small")
            elif self.width < min_width or self.height < min_height:
                print("\nWARNING: Maze will generate with no 42 logo. "
                      "(Too small)\n")
                time.sleep(2)
            else:
                self._apply_42()

        full_block = NORTH | EAST | SOUTH | WEST
        self.grid = [[full_block for _ in range(self.width)]
                     for _ in range(self.height)]

        stack = [(0, 0)]
        visited = set(self.locked_cells)
        visited.add((0, 0))

        while stack:
            cx, cy = stack[-1]
            neighbors = []

            for direction in [NORTH, EAST, SOUTH, WEST]:
                dx, dy = MOVEMENTS[direction]
                nx, ny = cx + dx, cy + dy

                if (0 <= nx < self.width and 0 <= ny < self.height and (nx, ny)
                        not in visited):
                    neighbors.append((nx, ny, direction))

            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self.grid[cy][cx] &= ~direction
                self.grid[ny][nx] &= ~OPPOSITES[direction]

                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        if not perfect:
            for _ in range(int((self.width * self.height) * 0.05)):
                rx = random.randint(0, self.width-1)
                ry = random.randint(0, self.height-1)
                direction = random.choice([NORTH, EAST, SOUTH, WEST])
                dx, dy = MOVEMENTS[direction]
                nx, ny = rx + dx, ry + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and (rx, ry) not in self.locked_cells
                        and (nx, ny) not in self.locked_cells):
                    self.grid[ry][rx] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSITES[direction]

    def solve(self, start: Tuple[int, int] = (0, 0),
              end: Optional[Tuple[int, int]] = None) -> Optional[str]:

        """
        Finds the path through the maze using MazeSolver
        from solver.py.
        """

        if end is None:
            end = (self.width - 1, self.height - 1)
        if MazeSolver.solve(self.grid, start, end) == "":
            raise ConfigError("Cannot find valid path to exit")
        return MazeSolver.solve(self.grid, start, end)
