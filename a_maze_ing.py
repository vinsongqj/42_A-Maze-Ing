"""
MAIN FILE

Runs together with the config.txt file.
Generates the maze based on the settings in the config.txt file

Comments are allowed in config.txt and must start with '#' per line
Allowed config.txt fields:
    - WIDTH
    - HEIGHT
    - ENTRY
    - EXIT
    - OUTPUT_FILE
    - PERFECT
    - SEED (optional)

"""

import sys
from maze_gen.generator import MazeGenerator
from maze_gen.display import MazeRenderer
from maze_gen.exporter import MazeExporter
import maze_gen.parser as parser
import maze_gen.validator as validator
from maze_gen.validator import ConfigError


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    # cfg = {
    #     "WIDTH": 20,
    #     "HEIGHT": 15,
    #     "ENTRY": (0, 0),
    #     "EXIT": (19, 14),
    #     "PERFECT": False,
    #     "OUTPUT_FILE": "maze.txt",
    #     "SEED": None
    # }

    try:
        cfg = parser.extract_config_data("config.txt")
        validator.validate_fields(cfg)
        gen = MazeGenerator(cfg["WIDTH"], cfg["HEIGHT"], cfg["SEED"])

        gen.generate(perfect=cfg["PERFECT"], use_logo=True)
        ui = MazeRenderer(gen)
        exporter = MazeExporter(gen)

        while True:
            ui.render(cfg["ENTRY"], cfg["EXIT"])

            if not ui.handle_input():
                exporter.save_to_file(
                    cfg["OUTPUT_FILE"],
                    cfg["ENTRY"],
                    cfg["EXIT"]
                )
                break
    except KeyboardInterrupt:
        print("\nSimulation interrupted.")
    except ValueError as e:
        print(e)
    except ConfigError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Unknown Error: {e}")

    finally:
        print("Exiting A-Maze-ing")


if __name__ == "__main__":
    main()
