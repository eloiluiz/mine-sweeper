#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mine Sweeper Game
"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "0.4.1"
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

    HEADER_HEIGHT_IN_PIXELS = 53
    FOOTER_HEIGHT_IN_PIXELS = 7
    LEFT_BORDER_WIDTH_IN_PIXELS = 9
    RIGHT_BORDER_WIDTH_IN_PIXELS = 8

    DISPLAY_WIDTH_IN_PIXELS = 13
    DISPLAY_HEIGHT_IN_PIXELS = 23
    CELL_SIZE_IN_PIXELS = 16

    def __init__(self, boardWidth=9, boardHeight=9, minesNumber=10):
        """Initialize the game board texture objects.
        """

        # Initialize the pygame module
        pygame.init()

        # Define the board parameters
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.minesNumber = minesNumber
        self.minesUndiscovered = minesNumber

        print("Creating a board with size of " + str(boardWidth) + "x" + str(boardHeight) + " cells and " +
              str(minesNumber) + " mines.")

        # Define the rendering properties
        self.windowWidth = self.LEFT_BORDER_WIDTH_IN_PIXELS
        self.windowWidth += (boardWidth * self.CELL_SIZE_IN_PIXELS)
        self.windowWidth += self.RIGHT_BORDER_WIDTH_IN_PIXELS

        self.windowHeight = self.HEADER_HEIGHT_IN_PIXELS
        self.windowHeight += (boardHeight * self.CELL_SIZE_IN_PIXELS)
        self.windowHeight += self.FOOTER_HEIGHT_IN_PIXELS

        self.windowSize = Vector2(self.windowWidth, self.windowHeight)

        self.displaySize = Vector2(self.DISPLAY_WIDTH_IN_PIXELS, self.DISPLAY_HEIGHT_IN_PIXELS)
        self.displaySprite = pygame.image.load("./graphics/7-seg-sprite.png")

        self.cellSize = Vector2(self.CELL_SIZE_IN_PIXELS, self.CELL_SIZE_IN_PIXELS)
        self.cellSprite = pygame.image.load("./graphics/cell-sprite.png")

        # Create the board window
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))

        # Load and set the game icon
        icon = pygame.image.load("./graphics/mine-icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Minesweeper")

        # Print the board background
        self.renderBackground()

        # Initialize the board values
        self.boardVisibility = np.zeros((self.boardHeight, self.boardWidth))
        # self.boardVisibility = np.ones((self.boardHeight, self.boardWidth))
        self.boardValues = np.zeros((self.boardHeight, self.boardWidth))

        # Define the game time system
        self.match_start_time_ms = pygame.time.get_ticks()

        # Define the control variables
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

    def renderBackground(self):
        """Function designed to print the game board background on screen.
        """

        # Clear the screen area (gray background)
        self.window.fill((192, 192, 192))

        # Load the background sprites
        backgroundSprite = pygame.image.load("./graphics/background-sprite.png")

        # Print the borders
        for x in range(self.LEFT_BORDER_WIDTH_IN_PIXELS, self.windowWidth - self.RIGHT_BORDER_WIDTH_IN_PIXELS + 1):
            spritePoint = Vector2(x, 0)
            texturePoint = Vector2(59, 0)
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(1), int(self.HEADER_HEIGHT_IN_PIXELS))
            self.window.blit(backgroundSprite, spritePoint, textureRect)

        for x in range(self.LEFT_BORDER_WIDTH_IN_PIXELS, self.windowWidth - self.RIGHT_BORDER_WIDTH_IN_PIXELS + 1):
            borderPosition = self.windowHeight - self.FOOTER_HEIGHT_IN_PIXELS
            spritePoint = Vector2(x, borderPosition)
            texturePoint = Vector2(11, 56)
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(1), int(self.FOOTER_HEIGHT_IN_PIXELS))
            self.window.blit(backgroundSprite, spritePoint, textureRect)

        for y in range(self.HEADER_HEIGHT_IN_PIXELS, self.windowHeight - self.FOOTER_HEIGHT_IN_PIXELS + 1):
            spritePoint = Vector2(0, y)
            texturePoint = Vector2(0, 54)
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.LEFT_BORDER_WIDTH_IN_PIXELS), int(1))
            self.window.blit(backgroundSprite, spritePoint, textureRect)

        for y in range(self.HEADER_HEIGHT_IN_PIXELS, self.windowHeight - self.FOOTER_HEIGHT_IN_PIXELS + 3):
            borderPosition = self.windowWidth - self.RIGHT_BORDER_WIDTH_IN_PIXELS
            spritePoint = Vector2(borderPosition, y)
            texturePoint = Vector2(143, 54)
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.RIGHT_BORDER_WIDTH_IN_PIXELS), int(1))
            self.window.blit(backgroundSprite, spritePoint, textureRect)

        borderPosition = self.windowHeight - self.FOOTER_HEIGHT_IN_PIXELS
        spritePoint = Vector2(0, borderPosition)
        texturePoint = Vector2(0, 56)
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.LEFT_BORDER_WIDTH_IN_PIXELS),
                           int(self.FOOTER_HEIGHT_IN_PIXELS))
        self.window.blit(backgroundSprite, spritePoint, textureRect)

        # Print the header
        spritePoint = Vector2(0, 0)
        texturePoint = Vector2(0, 0)
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(58), int(53))
        self.window.blit(backgroundSprite, spritePoint, textureRect)

        smilePosition = (self.windowWidth / 2) - 13
        spritePoint = Vector2(smilePosition, 0)
        texturePoint = Vector2(61, 0)
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(27), int(53))
        self.window.blit(backgroundSprite, spritePoint, textureRect)

        spritePoint = Vector2(self.windowWidth - 58, 0)
        texturePoint = Vector2(93, 0)
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(58), int(53))
        self.window.blit(backgroundSprite, spritePoint, textureRect)

    def render(self):
        """Function designed to print the game board on screen.
        """

        # Print the number of undiscovered mines
        mineCounter = self.minesUndiscovered
        if (mineCounter < 0):
            mineCounter = 0
        
        digits = [int(mineCounter / 100), int((mineCounter % 100) / 10), int(mineCounter % 10)]

        for index, digit in enumerate(digits):
            digitPosition = 14 + (index * 13)
            spritePoint = Vector2(digitPosition, 14)
            texturePoint = Vector2(digit, 0).elementwise() * self.displaySize
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.displaySize.x),
                               int(self.displaySize.y))
            self.window.blit(self.displaySprite, spritePoint, textureRect)

        # Print the match running time
        if (self.match_ongoing == True):
            self.match_time_ms = (pygame.time.get_ticks() - self.match_start_time_ms)

        # Calculate the match time
        match_time_s = int(self.match_time_ms / 1000)
        digits = [int(match_time_s % 10), int((match_time_s % 100) / 10), int(match_time_s / 100)]

        # Print each display digit on screen
        for index, digit in enumerate(digits):
            digitPosition = self.windowWidth - 28 - (index * 13)
            spritePoint = Vector2(digitPosition, 14)
            texturePoint = Vector2(digit, 0).elementwise() * self.displaySize
            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.displaySize.x),
                               int(self.displaySize.y))
            self.window.blit(self.displaySprite, spritePoint, textureRect)

        # Print the board tiles
        for (line, column), value in np.ndenumerate(self.boardValues):

            spriteOffset = Vector2(self.LEFT_BORDER_WIDTH_IN_PIXELS, self.HEADER_HEIGHT_IN_PIXELS)
            spritePoint = (Vector2(column, line).elementwise() * self.cellSize) + spriteOffset

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
            self.window.blit(self.cellSprite, spritePoint, textureRect)

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
        self.match_time_ms = (pygame.time.get_ticks() - self.match_start_time_ms)
        self.match_ongoing = False
        self.match_win = True
        print("Game Over. You Win!")

        # Calculate the score and display
        self.match_score = int((self.minesNumber * 100) / (self.match_time_ms / 1000))
        print("Match Score = " + str(self.match_score) + " points!")

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

                targetCell.x = (mousePosition[BUTTON_X_POSITION_INDEX] - self.LEFT_BORDER_WIDTH_IN_PIXELS)
                targetCell.x = int(targetCell.x / self.CELL_SIZE_IN_PIXELS)
                targetCell.y = (mousePosition[BUTTON_Y_POSITION_INDEX] - self.HEADER_HEIGHT_IN_PIXELS)
                targetCell.y = int(targetCell.y / self.CELL_SIZE_IN_PIXELS)

                # TODO: remove after testing - middle mouse button will close every cell
                if (button[1]):
                    # Reset the board
                    self.boardVisibility = np.zeros((self.boardHeight, self.boardWidth))
                    # Reset the control variables
                    self.match_start_time_ms = pygame.time.get_ticks()
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
                    self.match_time_ms = (pygame.time.get_ticks() - self.match_start_time_ms)
                    self.match_ongoing = False
                    self.match_win = False
                    print("Game Over. You Lose!")

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
                    self.minesUndiscovered -= 1

                elif (self.boardVisibility[targetLine, targetColumn] == self.CELL_BLOCKED_STATE):
                    self.boardVisibility[targetLine, targetColumn] = self.CELL_CLOSED_STATE
                    self.minesUndiscovered += 1

    def run(self):
        """Function designed to run the game application.
        """

        # Run the main loop
        while self.running:
            self.render()
            self.processInput()


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
