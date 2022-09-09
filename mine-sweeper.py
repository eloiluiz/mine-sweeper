#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mine Sweeper Game
"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "0.3.1"
__status__ = "Development"

# Import libraries
import argparse
import numpy as np
import pygame
import random
from pygame import Rect
from pygame.math import Vector2


class MineSweeperGame:
    """Mine Sweeper Game board texture definition class.

    Returns:
        board_texture: the game texture producer class.
    """

    # Texture constant definition
    CELL_EMPTY_VALUE = 0
    CELL_MINE_VALUE = 9
    CELL_FLAG_VALUE = 10
    CELL_CLOSED_VALUE = 11
    CELL_EXPLODED_MINE_VALUE = 12
    CELL_WRONG_FLAG_VALUE = 13

    CELL_CLOSED_STATE = 0
    CELL_OPEN_STATE = 1
    CELL_BLOCKED_STATE = 2
    CELL_EXPLODED_MINE_STATE = 3
    CELL_WRONG_BLOCKED_STATE = 4

    CELL_SIZE_IN_PIXELS = 58

    def __init__(self, boardWidth=9, boardHeight=9, minesNumber=10):
        """Initialize the game board texture objects.
        """

        # Initialize the pygame module
        pygame.init()

        # Define the board parameters
        self.headerHeight = 1
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.minesNumber = minesNumber

        print("Creating a board with size of " + str(boardWidth) + "x" + str(boardHeight) + " cells and " +
              str(minesNumber) + " mines.")

        self.windowWidth = boardWidth
        self.windowHeight = self.headerHeight + boardHeight

        self.boardVisibility = np.zeros((self.boardHeight, self.boardWidth))
        # self.boardVisibility = np.ones((self.boardHeight, self.boardWidth))
        self.boardValues = np.zeros((self.boardHeight, self.boardWidth))

        # Define the rendering properties
        self.cellSize = Vector2(self.CELL_SIZE_IN_PIXELS, self.CELL_SIZE_IN_PIXELS)
        self.boardSize = Vector2(self.windowWidth, self.windowHeight)
        self.unitsTexture = pygame.image.load("./graphics/tile_set_small.png")

        # Create the board window
        windowSize = self.boardSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))

        # Load and set the game icon
        icon = pygame.image.load("./graphics/mine-icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Minesweeper")

        # Define the control variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_first_click = True
        self.match_ongoing = True
        self.match_win = False

    def getNeighbors(self, line, column):
        """Identify the selected cell neighbor positions and returns it.

        Args:
            line (int): cell line coordinate.
            column (int): cell column coordinate.

        Returns:
            list: the list of neighbor coordinates.
        """

        neighbors = []

        for lineOffset in range(-1, 2):
            for columnOffset in range(-1, 2):

                # Get neighbor position
                neighborLine = line + lineOffset
                neighborColumn = column + columnOffset

                # Discard invalid neighbors
                if ((neighborLine < 0) or (neighborColumn < 0)):
                    continue
                if ((neighborLine >= self.boardHeight) or (neighborColumn >= self.boardWidth)):
                    continue
                if ((neighborLine == line) and (neighborColumn == column)):
                    continue

                # Populate the neighbors list
                neighbors.append([neighborLine, neighborColumn])

        return neighbors

    def generateBoard(self, initialLine, initialColumn):
        """Generate a random board.

        This method will generate a random board using the game configuration parameters. The initial cell coordinates
        are guaranteed to not have a mine places on it.

        Args:
            initialLine (int): The initial cell line coordinate.
            initialColumn (int): the initial cell column coordinate.
        """

        # Reset the board state
        self.boardVisibility = np.zeros((self.boardHeight, self.boardWidth))
        self.boardValues = np.zeros((self.boardHeight, self.boardWidth))

        # Open the initial position
        self.boardVisibility[initialLine, initialColumn] = self.CELL_OPEN_STATE

        # Place the required number of mines at random positions
        remainingMines = self.minesNumber
        while (remainingMines > 0):

            # Get a random line position
            line = random.randint(0, (self.boardHeight - 1))

            # Get the list of available cells on that line
            columnList = []
            for column, value in enumerate(self.boardValues[line]):
                if ((value != self.CELL_MINE_VALUE) and (self.boardVisibility[line, column] != self.CELL_OPEN_STATE)):
                    columnList.append(column)

            # Place the mine in the board
            if (len(columnList) > 0):
                column = int(random.choice(columnList))
                self.boardValues[line, column] = self.CELL_MINE_VALUE
                remainingMines -= 1

        # Then, iterate over the board and update the board values
        for (line, column), value in np.ndenumerate(self.boardValues):

            # Skip if the position has a mine
            if (value == self.CELL_MINE_VALUE):
                continue

            # Check each neighbor position for mines
            minesFound = 0
            neighbors = self.getNeighbors(line, column)

            for (neighborLine, neighborColumn) in neighbors:

                # Check for mines
                if (self.boardValues[neighborLine, neighborColumn] == self.CELL_MINE_VALUE):
                    minesFound += 1

            # Update the cell value
            self.boardValues[line, column] = minesFound

    def render(self):
        """Function designed to print the game board on screen.
        """

        # Clear the screen area (white background)
        self.window.fill((255, 255, 255))

        # Print the board tiles
        for (line, column), value in np.ndenumerate(self.boardValues):

            spritePoint = Vector2(column, line + self.headerHeight).elementwise() * self.cellSize

            visibility = self.boardVisibility[line, column]
            if (visibility == self.CELL_CLOSED_STATE):
                texturePoint = Vector2(self.CELL_CLOSED_VALUE, 0).elementwise() * self.cellSize
            elif (visibility == self.CELL_BLOCKED_STATE):
                texturePoint = Vector2(self.CELL_FLAG_VALUE, 0).elementwise() * self.cellSize
            elif (visibility == self.CELL_EXPLODED_MINE_STATE):
                texturePoint = Vector2(self.CELL_EXPLODED_MINE_VALUE, 0).elementwise() * self.cellSize
            elif (visibility == self.CELL_WRONG_BLOCKED_STATE):
                texturePoint = Vector2(self.CELL_WRONG_FLAG_VALUE, 0).elementwise() * self.cellSize
            else:
                texturePoint = Vector2(value, 0).elementwise() * self.cellSize

            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
            self.window.blit(self.unitsTexture, spritePoint, textureRect)

        pygame.display.update()

    def openCell(self, line, column, force):
        """Open the selected cell position.

        Args:
            line (int): cell line coordinate.
            column (int): cell column coordinate.
            force (bool): force the open action and neighbors discovery.
        """

        # First, check if the cell is still closed, then proceed opening it
        if ((self.boardVisibility[line, column] == self.CELL_CLOSED_STATE) or (force == True)):

            self.boardVisibility[line, column] = self.CELL_OPEN_STATE

            # Also, if the opened cell value is zero, open it's neighbors
            if (self.boardValues[line, column] == self.CELL_EMPTY_VALUE):

                neighbors = self.getNeighbors(line, column)

                for (neighborLine, neighborColumn) in neighbors:
                    self.openCell(neighborLine, neighborColumn, False)

    def openMines(self):
        """Open every closed mine position and indicate invalid flags.
        """

        # Iterate over the board and mark the desired position
        for (line, column), value in np.ndenumerate(self.boardValues):

            visibility = self.boardVisibility[line, column]

            if ((visibility == self.CELL_CLOSED_STATE) and (value == self.CELL_MINE_VALUE)):
                self.boardVisibility[line, column] = self.CELL_OPEN_STATE

            elif ((visibility == self.CELL_BLOCKED_STATE) and (value != self.CELL_MINE_VALUE)):
                self.boardVisibility[line, column] = self.CELL_WRONG_BLOCKED_STATE

    def checkVictory(self):
        """Check for the game victory condition.
        """

        # Iterate over the board and look for closed numbered positions
        for (line, column), value in np.ndenumerate(self.boardValues):

            visibility = self.boardVisibility[line, column]

            if ((visibility == self.CELL_CLOSED_STATE) and (value < self.CELL_MINE_VALUE)):
                return

        # Block (flag) every mine position
        for (line, column), value in np.ndenumerate(self.boardValues):
            if (value == self.CELL_MINE_VALUE):
                self.boardVisibility[line, column] = self.CELL_BLOCKED_STATE

        # Indicate the victory
        self.match_ongoing = False
        self.match_win = True

    def processInput(self):
        """Process the user input commands.
        """

        LEFT_BUTTON_INDEX = 0
        RIGHT_BUTTON_INDEX = 2

        BUTTON_X_POSITION_INDEX = 0
        BUTTON_Y_POSITION_INDEX = 1

        leftButtonEvent = False
        rightButtonEvent = False
        targetCell = Vector2()

        # Event handling, get events from the event queue
        for event in pygame.event.get():

            # Check for the exit event condition (Window Close)
            if (event.type == pygame.QUIT):
                # Change the control flag to False and exit the main loop
                self.running = False
                continue

            # Check for the exit event condition (ESC Key)
            elif (event.type == pygame.KEYDOWN):

                if (event.key == pygame.K_ESCAPE):
                    # Change the control flag to False and exit the main loop
                    self.running = False
                    continue

            # Check for click events and identify which button was pressed
            elif (event.type == pygame.MOUSEBUTTONDOWN):

                button = pygame.mouse.get_pressed()

                if (button[LEFT_BUTTON_INDEX]):
                    leftButtonEvent = True

                elif (button[RIGHT_BUTTON_INDEX]):
                    rightButtonEvent = True

                mousePosition = pygame.mouse.get_pos()

                targetCell.x = int(mousePosition[BUTTON_X_POSITION_INDEX] / self.CELL_SIZE_IN_PIXELS)
                targetCell.y = int(mousePosition[BUTTON_Y_POSITION_INDEX] / self.CELL_SIZE_IN_PIXELS)
                targetCell.y -= self.headerHeight

                # TODO: remove after testing - middle mouse button will close every cell
                if (button[1]):
                    self.boardVisibility = np.zeros((self.boardHeight, self.boardWidth))
                    self.match_ongoing = True
                    self.match_win = False

            # In case the match has already ended, skip the game button actions
            if (self.match_ongoing == False):
                continue

            # Cast the target coordinated to integers
            targetLine = int(targetCell.y)
            targetColumn = int(targetCell.x)

            # Process the open cell event
            if (leftButtonEvent == True):

                leftButtonEvent == False

                # In case this is the first click for the match, generate the board
                if (self.is_first_click == True):
                    self.is_first_click = False
                    self.generateBoard(targetLine, targetColumn)
                    self.openCell(targetLine, targetColumn, True)
                    continue

                # Next, check if the opened cell is a mine
                value = self.boardValues[targetLine, targetColumn]
                if (value == self.CELL_MINE_VALUE):
                    # Explode the selected mine and open every other
                    self.boardVisibility[targetLine, targetColumn] = self.CELL_EXPLODED_MINE_STATE
                    self.openMines()
                    # End the match (defeat)
                    self.match_ongoing = False
                    self.match_win = False

                # Otherwise, open the cell as usual
                else:
                    self.openCell(targetLine, targetColumn, False)

                # Lastly, check if the game has ended in victory
                self.checkVictory()

            # Process the block cell event
            if (rightButtonEvent == True):

                rightButtonEvent == False

                # In case this is the first click for the match, generate the board
                if (self.is_first_click == True):
                    self.is_first_click = False
                    self.generateBoard(targetLine, targetColumn)

                # Next, process the event
                if (self.boardVisibility[targetLine, targetColumn] == self.CELL_CLOSED_STATE):
                    self.boardVisibility[targetLine, targetColumn] = self.CELL_BLOCKED_STATE

                elif (self.boardVisibility[targetLine, targetColumn] == self.CELL_BLOCKED_STATE):
                    self.boardVisibility[targetLine, targetColumn] = self.CELL_CLOSED_STATE

    def run(self):
        """Function designed to run the game application.
        """

        # Run the main loop
        while self.running:
            self.render()
            self.processInput()
            self.clock.tick(60)


def main(args):
    """Mine Sweeper Game main function.

    This function initializes and run the Mine Sweeper Game application.

    Args:
        args (object): the argparse class parsed result object.
    """

    EASY_WIDTH = 9
    EASY_HEIGHT = 9
    EASY_MINES = 10

    MEDIUM_WIDTH = 16
    MEDIUM_HEIGHT = 16
    MEDIUM_MINES = 40

    HARD_WIDTH = 30
    HARD_HEIGHT = 16
    HARD_MINES = 100

    boardWidth = 0
    boardHeight = 0
    minesNumber = 0

    # Parse the game input commands
    if ((isinstance(args.difficulty, str) == True) and (args.difficulty != '')):

        if (args.difficulty == 'medium'):
            print("Medium difficulty selected.")
            boardWidth = MEDIUM_WIDTH
            boardHeight = MEDIUM_HEIGHT
            minesNumber = MEDIUM_MINES

        elif (args.difficulty == 'hard'):
            print("Hard difficulty selected.")
            boardWidth = HARD_WIDTH
            boardHeight = HARD_HEIGHT
            minesNumber = HARD_MINES

        else:
            print("Easy difficulty selected.")
            boardWidth = EASY_WIDTH
            boardHeight = EASY_HEIGHT
            minesNumber = EASY_MINES

    else:
        print("Easy difficulty selected by default.")
        boardWidth = EASY_WIDTH
        boardHeight = EASY_HEIGHT
        minesNumber = EASY_MINES

    # Create the game instance and run
    game = MineSweeperGame(boardWidth, boardHeight, minesNumber)
    game.run()


# Application entry point
if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser()

    # Define the supported arguments
    parser.add_argument('-d',
                        '--difficulty',
                        type=str,
                        choices=['easy', 'medium', 'hard'],
                        default='',
                        help='Define the game difficulty')

    # Parse the input arguments
    args = parser.parse_args()

    # Call the main game function
    main(args)
