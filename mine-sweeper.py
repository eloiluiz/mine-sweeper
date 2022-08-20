#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mine Sweeper Game
"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "0.1.0"
__status__ = "Development"

# Import libraries
import numpy as np
import pygame
from pygame import Rect
from pygame.math import Vector2
from random import randint


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

    CELL_CLOSED_STATE = 0
    CELL_OPEN_STATE = 1
    CELL_BLOCKED_STATE = 2

    CELL_SIZE_IN_PIXELS = 58

    def __init__(self, board_width=9, board_height=9, mines_number=10):
        """Initialize the game board texture objects.
        """

        # Initialize the pygame module
        pygame.init()

        # Define the board parameters
        self.header_height = 1
        self.board_width = board_width
        self.board_height = board_height
        self.mines_number = mines_number

        self.window_width = board_width
        self.window_height = self.header_height + board_height

        # self.board_visibility = np.zeros((self.board_width, self.board_height))
        self.board_visibility = np.ones((self.board_width, self.board_height))
        self.board_values = np.zeros((self.board_width, self.board_height))

        # Generate a random board
        self.generate_board()

        # Define the rendering properties
        self.cellSize = Vector2(self.CELL_SIZE_IN_PIXELS, self.CELL_SIZE_IN_PIXELS)
        self.boardSize = Vector2(self.window_width, self.window_height)
        self.unitsTexture = pygame.image.load("./graphics/tile_set_small.png")

        # Create the board window
        windowSize = self.boardSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))

        # Load and set the game icon
        icon = pygame.image.load("./graphics/mine-icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Minesweeper")

        # Define a variable to control the main loop
        self.clock = pygame.time.Clock()
        self.running = True

    def generate_board(self):

        # First place the required number of mines at random positions
        remaining_mines = self.mines_number

        while (remaining_mines > 0):

            # Get a random position
            line = randint(0, (self.board_height - 1))
            column = randint(0, (self.board_width - 1))

            # Place the mine in the board
            if (self.board_values[line, column] != self.CELL_MINE_VALUE):
                self.board_values[line, column] = self.CELL_MINE_VALUE
                remaining_mines -= 1

        # Then, iterate over the board and update the board values
        for (line, column), value in np.ndenumerate(self.board_values):

            # Skip if the position has a mine
            if (value == self.CELL_MINE_VALUE):
                continue

            # Check each neighbor position for mines
            mines_found = 0
            for line_offset in range(-1, 2):
                for column_offset in range(-1, 2):

                    # Get neighbor position
                    neighbor_line = line + line_offset
                    neighbor_column = column + column_offset

                    # Discard invalid neighbors
                    if ((neighbor_line < 0) or (neighbor_column < 0)):
                        continue
                    if ((neighbor_line >= self.board_height) or (neighbor_column >= self.board_width)):
                        continue
                    if ((neighbor_line == line) and (neighbor_column == column)):
                        continue

                    # Check for mines
                    if (self.board_values[neighbor_line, neighbor_column] == self.CELL_MINE_VALUE):
                        mines_found += 1

            # Update the cell value
            self.board_values[line, column] = mines_found

    def render(self):
        """Function designed to print the game board on screen.
        """

        # Clear the screen area (white background)
        self.window.fill((255, 255, 255))

        # Print the board tiles
        for (line, column), value in np.ndenumerate(self.board_values):

            spritePoint = Vector2(column, line + self.header_height).elementwise() * self.cellSize

            visibility = self.board_visibility[line, column]
            if (visibility == self.CELL_CLOSED_STATE):
                texturePoint = Vector2(self.CELL_CLOSED_VALUE, 0).elementwise() * self.cellSize
            elif (visibility == self.CELL_BLOCKED_STATE):
                texturePoint = Vector2(self.CELL_FLAG_VALUE, 0).elementwise() * self.cellSize
            else:
                texturePoint = Vector2(value, 0).elementwise() * self.cellSize

            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
            self.window.blit(self.unitsTexture, spritePoint, textureRect)

        pygame.display.update()

    def run(self):
        """Function designed to run the game application.
        """

        # Run the main loop
        while self.running:

            # Event handling, get events from the event queue
            for event in pygame.event.get():

                # Check for the exit event condition
                if event.type == pygame.QUIT:
                    # Change the control flag to False and exit the main loop
                    self.running = False

            self.render()
            self.clock.tick(60)


def main():
    """Mine Sweeper Game main function.

    This function initializes and run the Mine Sweeper Game application.
    """
    game = MineSweeperGame()
    game.run()


# Application entry point
if __name__ == "__main__":
    main()
