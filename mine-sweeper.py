#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Mine Sweeper Game
"""

__author__ = "Eloi Giacobbo"
__email__ = "eloiluiz@gmail.com"
__version__ = "0.1.0"
__status__ = "Development"

# import the pygame module, so you can use it
import pygame
 

def main():
    """Mine Sweeper Game main function.

    This function initializes and run the Mine Sweeper Game application.
    """

    # Initialize the pygame module
    pygame.init()
    
    # Load and set the game icon
    logo = pygame.image.load("./graphics/mine-icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Minesweeper")
     
    # Create a surface on screen that has the initial size of 800x600 pixels
    screen = pygame.display.set_mode((800,600))
     
    # Define a variable to control the main loop
    running = True
     
    # Run the main loop
    while running:

        # Event handling, get events from the event queue
        for event in pygame.event.get():
            
            # Check for the exit event condition
            if event.type == pygame.QUIT:
                # Change the control flag to False and exit the main loop
                running = False
     
     
# Application entry point
if __name__=="__main__":
    main()