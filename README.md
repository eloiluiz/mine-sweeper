# Mine Sweeper Game

Minesweeper is a single-player logic-based computer game played on a rectangular board whose objective is to locate a predetermined number of randomly placed "mines" in the shortest possible time. Throughout the game, the player must select "safe" squares (cells) from the board, avoiding the squares with mines. If the player selects a mine, the game ends. Otherwise, a number between 0 and 8 is displayed that identifies the total number of mines present in the eight regions neighboring the selected position. Therefore, finding a square containing "8" indicates that all eight adjacent squares contain mines, while a zero (displayed in white) indicates that there are no mines in the surrounding squares. A square suspected of containing a mine can be marked with a flag. There are two ways to finish this game: selecting a mine (defeat); or by selecting all safe positions and completely opening the board (victory).

Minesweeper is a simple and widely known game. For this reason, this game was selected as a work object for the VII MBA-12 Software Project Management course, part of the Postgraduate course MBA in Software Engineering course at UTFPR. This project will be developed throughout the Software Project Management discipline, following the proposed schedule and delivering the required artifacts throughout this process.

## Game Install and Dependencies

To run this game, you will need to have a Python 3 distribution installed on your computer. For more information, please visit [Python.org](https://www.python.org/downloads/).

Furthermore, this game was created using the Pygame library, designed for writing video games. For more information about this module and installation instructions, go to [Pygame.org](https://www.pygame.org/news).

## How to Run the Game

To launch the game, download this repository and open your command terminal in the folder where the source code is available.

Then use the following command to start the game:

```
python mine-sweeper.py
```

## Command Line Options

This game was developed with some command options for game customization. For more information, the game's help options:

```
python mine-sweeper.py -h
```

## Release Notes

### Release V0.3 - Development
In version V0.2, board size customization and time tracking capabilities were added to the game.
Additionally, in this version endgame decision conditions and a major improvement in its graphics have been implemented.

![Release V0.3](/release/Mine-Sweeper%20-%20V0.3.png "Release V0.3")

### Release V0.2 - Development
In version V0.2, the ability to receive user input, through the mouse, was incorporated into the software to perform actions to discover and block positions on the board.

![Release V0.2](/release/Mine-Sweeper%20-%20V0.2.png "Release V0.2")

### Release V0.1 - Development
Game initial version released for testing.
Random creation and board preview features released.

![Release V0.1](/release/Mine-Sweeper%20-%20V0.1.png "Release V0.1")