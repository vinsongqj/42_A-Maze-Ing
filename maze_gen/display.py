"""
MAZE DISPLAYER AND CONTROLLER

This file handles displaying the maze,
coloring the walls/logo/path with ANSI
color codes and listens to keyboard
inputs to either regenerate the maze/
toggle the path visibility/ change the
maze color or quit the program.
"""

import os
import sys
import tty
import termios
from typing import Tuple, Set, Any
from .constants import COLORS, MOVEMENTS, DIRECTION_LABELS


class MazeRenderer:

    """
    The class used to display the maze and handle keyboard input.
    It keeps track of the colors used and whether the solution
    path should be displayed.
    """

    def __init__(self, generator: Any) -> None:

        """
        Sets up colors and links the generator to the maze.
        """

        self.gen = generator
        self.colors = [
            COLORS["white"],
            COLORS["green"],
            COLORS["cyan"],
            COLORS["magenta"],
            COLORS["yellow"],
        ]
        self.path_color = COLORS["red"]
        self.start_color = COLORS["forest"]
        self.end_color = COLORS["red"]
        self.logo_color = COLORS["dim"]
        self.reset = COLORS["reset"]
        self.c_idx = 0
        self.show_path = False

    def _get_path_set(self, start: Tuple[int, int],
                      end: Tuple[int, int]) -> Set[Tuple[int, int]]:

        """
        Turns the letter string from the solver into a list of coordinates.
        """

        path_str = self.gen.solve(start, end)

        if not path_str:
            return {start}

        res = {start}
        cx, cy = start
        char_to_bit = {v: k for k, v in DIRECTION_LABELS.items()}

        for char in path_str:
            if char in char_to_bit:
                bit = char_to_bit[char]
                dx, dy = MOVEMENTS[bit]
                cx += dx
                cy += dy
                res.add((cx, cy))
        return res

    def render(self, entry: Tuple[int, int], exit_p: Tuple[int, int]) -> None:

        """
        Clears the terminal and draws the maze line by line
        by looping through the grid to check the bitwise
        switches (1, 2, 4, 8) to decide where to draw walls.
        It also renders the entry and exit points, path dots
        and 42 logo.
        """

        os.system('clear' if os.name != 'nt' else 'cls')

        c = self.colors[self.c_idx]
        p_set = self._get_path_set(entry, exit_p) if self.show_path else set()

        for y in range(self.gen.height):
            top, mid = "", ""
            for x in range(self.gen.width):
                v = self.gen.grid[y][x]
                top += f"{c}████" if (v & 1) else f"{c}█   "
                west = f"{c}█" if (v & 8) else " "
                marker = "   "
                if (x, y) == entry:
                    marker = f"{self.start_color}███"
                elif (x, y) == exit_p:
                    marker = f"{self.end_color}███"
                elif (x, y) in self.gen.locked_cells:
                    marker = f"{self.logo_color}███{self.reset}{c}"
                elif (x, y) in p_set:
                    marker = f"{self.path_color} • {self.reset}{c}"
                mid += f"{west}{marker}"
            print(f"{top}{c}█{self.reset}")
            print(f"{mid}{c}█{self.reset}")

        print(f"{c}{'████' * self.gen.width}█{self.reset}")

        if self.gen.error_msg:
            print(f"\n{COLORS['red']}{self.gen.error_msg}{self.reset}")

    def _get_key_press(self) -> str:

        """
        Listens for single key presses.
        """

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        except Exception:
            ch = ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

    def handle_input(self) -> bool:

        """
        Determines what to do based on key presses.
        """

        print("\n[R] Regen  [P] Path  [C] Color  [Q] Quit")
        ch = self._get_key_press().lower()

        if ch == "r":
            self.gen.generate(perfect=self.gen.perfect)
        elif ch == "p":
            self.show_path = not self.show_path
        elif ch == "c":
            self.c_idx = (self.c_idx + 1) % len(self.colors)
        return ch != "q"
