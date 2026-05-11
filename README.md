*This project has been created as part of the 42 curriculum by ryeong and vgoh.*

# A-Maze-Ing

 ## Description

 A-Maze-Ing is a maze generation algorithm project that generates a solveable maze and includes a reusable package `maze_gen`. 
 
 Our program `a_maze_ing.py` works by reading a user-modified `config.txt` file and generates a maze based on the config parameters using Depth-First Search (Recursive Backtracking) while providing a solution using Breadth-First Search, then displaying it via terminal rendering while listening for user inputs to regenerate the maze / change maze color / display or hide the solution path. It writes to a file the maze in hexadecimal format upon exit, where each digit encodes which walls are closed, along with the entry and exit coordinates and the path solution string in N/E/S/W format. An identical maze can be reproduced by using the same seed in the config.txt.

 ## Instructions
 ### Requirements
 * Python 3.10+
 * pip
 * venv

 ### Installing the Program

 After cloning the repository:

 1. Create the virtual environment and install the dependencies 
    
        make install

 2. Run the program

        make run

3. Additional commands include:
    ```
    make debug        # to debug
    make lint         # to run flake8 and mypy
    make lint-strict  # same as lint but with the
                        --strict flag for mypy
    make clean        # removes build artifacts
    make package      # creates the .whl file of
                        the package to be reused

    # All 'make' commands will automatically create a
      virtual environment if none exists.

4. To run the program without using `make run`:

        python3 a_maze_ing.py config.txt
 



 ### Structure and Format of config.txt

```
# Values can be altered following the key=value format

WIDTH=20               # Number of columns (> 0)
HEIGHT=15              # Number of rows (> 0)
ENTRY=0,0              # Entry coordinates
EXIT=19,14             # Exit coordinates
OUTPUT_FILE=maze.txt   # The file name of the output
PERFECT=True           # Bool that ensures one path if True, and creates loops if False
SEED=*your seed*       # This parameter is optional
```

 ## Maze Generation

 ### What Generation Algorithm We Chose And Why

 We went with Depth-First Search based on the table of comparisons below: 
 
| Feature | Depth-First Search  | Kruskal's Algorithm |
| ------------- |:-------------:|:-------------:|
| **Pathing**    | Long, snaking corridors     | Short, branching paths |
| **Dead Ends**     | Few, but long     | Many, but short |
| **Randomness**  | Has a strong directional bias | Unbiased for all directions
| **Difficulty to implement**    | Easy (Uses recursion)     | Hard (Uses disjoint sets) |
**Time Complexity** |  Faster (O(V + E)\) | Slower (O(E log E)) |

Despite the directional bias of DFS and its lack of dead ends, the choice was weighted upon the ease of implementation and time complexity. We also agreed that aesthetically, DFS seemed to fit what we were looking for (long snaking corridors that are easier to follow).

### MazeGenerator Class

Our generator is where we use the DFS/recursive backtracking logic. It begins by:
1. Initializing a full block of solid cells according to grid dimensions.
2. Designating cells with `_apply_42` to create an immutable boundary in the shape of the '42' pattern.
3. Picking a random unvisited neighbor with `random.choice`.
4. Flipping wall bits off using bitwise operators.
5. Using `pop()` to backtrack the stack by 1 when encountering a dead end, and continues searching for paths.

### MazeSolver Class

For our solver, we used Breadth-First Search instead. Instead of prioritizing depth, it favors breadth, which means its search spans all directions and if the exit point is found we can be sure that it is the fastest possible solution. It begins by:
1. Checking the cells' bits to see if they are open or closed, while marking them as visited to avoid looping.
2. Backtracking like the generator if a dead end is encountered.
3. Encoding the successful path into a string of directions "NESW".


 ## Reusable Sections of Code

 This project comes with a reusable package `maze_gen` that contains several modules:

`MazeGenerator (Class)`: Generates grid data using DFS without visual representation.

    from maze_gen.generator import MazeGenerator

`MazeSolver (Class)`: Finds the shortest path between 2 points of a grid using BFS.

    from maze_gen.solver import MazeSolver

`MazeRenderer (Class)`: Handles terminal ASCII rendering and user input.

    from maze_gen.display import MazeRenderer

`MazeExporter (Class)`: Handles file writing and formatting.

    from maze_gen.exporter import MazeExporter

To start using the modules:

1. Run `make package`.
2. A directory called `/dist` should be created.
3. From `/dist`, copy the .whl file and paste it in the directory of the file you plan to import into.
4. Run `pip install mazegen-1.0.0-py3-none-any.whl` (It is recommended to run within a virtual environment: `python -m venv venv` then `source venv/bin/activate`).
5. Use the modules as demonstrated above.

 ## Role Delegation

**ryeong**

* Created the config parser and added reproducibility via seed.
* Modified the main to handle the parameters parsed and built upon the skeleton.
* Implemented validation and error handling.
* Reviewed code to ensure we were on the right track.
* Edited the readme.

**vgoh**

* Created the maze generator and solver.
* Handled the terminal rendering, output file exporting and user input.
* Built a working skeleton of the main to test maze generation, solving and display.
* Ensuring the .txt output file is written according to subject requirements.
* Linted and fixed all flake8 and mypy errors.
* Edited the readme.

## Planning and Evolution of the Project

**Planning stage** 
* Discussed the possible algorithms to use for the generation and solving.
* Delegated the tasks among ourselves.
* Shared learning resources to ensure consistent understanding between us.
* Coordinated time availability to complete the project before the deadline.
* Decided the directory structure and modularity of the project.

**Building stage**
* Created working version of the main for testing core functionality.
* Worked on building a functional generator, solver, parser, display and exporter.
* Kept each other updated on current progress and git pulled regularly to remain updated.

**Polishing stage**
* Implemented missing validation checks for edge cases.
* Added docstrings and ensured they provided sufficient explanation.
* Ensured that there were no redundancies and cleaned up messy code.
* Final testing to make sure everything functioned as intended.
* Added seed reproducibility from the config.txt due to earlier misinterpretation of the subject PDF.
* Edited the readme.

## What Worked and What Improved

The DFS maze generation worked as intended, and separating the components into separate modules really helped for fixing bugs and reusability. Furthermore, the structure of the project was kept relatively uncluttered with every file having its explicit purpose. 

What could be improved is the display of the path, which we opted to use dots for instead due to difficulty with rendering a solid line that follows the path within the terminal. While it was a possible fix, we decided that we did not have sufficient time to make radical changes and opted to go with the current method. We could have also improved this project by adding in animation and maybe even an option to change generation algorithms, but alas we lacked the time to implement such features.

## Resources

[Graph Traversals - BFS & DFS by Abdul Bari](https://www.youtube.com/watch?v=pcKY4hjDrxk&list=TLPQMDcwNDIwMjankNRSAo0DTg&index=2)

[Geeksforgeeks (DFS)](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/)

[Geeksforgeeks (BFS)](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)

## Tools Used

**Generative AI** - Used to scrutinize our code for any overlooked error handling and edge cases, as well as general consultation about the pros and cons of each algorithm and how the project should be executed.

**YouTube** - Used to educate ourselves about the topics required to take on the project (Kruskal's and BFS).

**flake8 and mypy** - For linting.

**Git** -For version control.



