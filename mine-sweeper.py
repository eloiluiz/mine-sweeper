#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mine Sweeper Game
"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "0.1.0"
__status__ = "Development"

# Import libraries
import pygame
import numpy as np
from pygame import Rect
from pygame.math import Vector2

# Define a sample board
header_height = 1
board_width = 9
board_height = 9

window_width = board_width
window_height = header_height + board_height

board_visibility = np.zeros((board_width, board_height))
board_visibility[3, 0] = 1
board_visibility[4, 1] = 1
board_visibility[5, 2] = 2

# yapf: disable
board_values = np.array([
    [+1, +1, +2, +1, +1, +0, +1, +2, +2],
    [+1, +9, +3, +9, +1, +0, +1, +9, +9],
    [+1, +2, +9, +2, +1, +1, +2, +3, +2],
    [+0, +1, +1, +1, +1, +2, +9, +1, +0],
    [+1, +1, +1, +0, +1, +9, +2, +1, +0],
    [+1, +9, +1, +0, +1, +1, +1, +1, +1],
    [+1, +1, +1, +0, +0, +0, +0, +1, +9],
    [+0, +0, +0, +0, +0, +0, +0, +2, +2],
    [+0, +0, +0, +0, +0, +0, +0, +1, +9]
])
# yapf: enable


class MineSweeperGame:
    """Mine Sweeper Game board texture definition class.

    Returns:
        board_texture: the game texture producer class.
    """

    def __init__(self):
        """Initialize the game board texture objects.
        """
        # Initialize the pygame module
        pygame.init()

        # Define the rendering properties
        self.cellSize = Vector2(58, 58)
        self.boardSize = Vector2(window_width, window_height)
        self.unitsTexture = pygame.image.load("./graphics/tile_set_small.png")

        # Create the board window
        windowSize = self.boardSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        self.window.fill((255, 255, 255))

        # Load and set the game icon
        logo = pygame.image.load("./graphics/mine-icon.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Minesweeper")

        # Define a variable to control the main loop
        self.clock = pygame.time.Clock()
        self.running = True

    def render(self):
        # Clear the screen area (white background)
        self.window.fill((255, 255, 255))

        # Print the board tiles
        for (line, column), value in np.ndenumerate(board_values):
            spritePoint = Vector2(column, line + header_height).elementwise() * self.cellSize

            visibility = board_visibility[line, column]
            if (visibility == 0):
                texturePoint = Vector2(11, 0).elementwise() * self.cellSize
            elif (visibility == 2):
                texturePoint = Vector2(10, 0).elementwise() * self.cellSize
            else:
                texturePoint = Vector2(value, 0).elementwise() * self.cellSize

            textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
            self.window.blit(self.unitsTexture, spritePoint, textureRect)

        pygame.display.update()

    def run(self):
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

    # Initialize and run the game
    game = MineSweeperGame()
    game.run()


# Application entry point
if __name__ == "__main__":
    main()