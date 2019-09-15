__author__ = "Ethan Garza"

import pygame

pygame.init()

# As there are 6 rows and 7 columns, leads to a nice 6 to 7 ratio, each by a factor of 84 (6*7*2)
width = 588
# the additional 200 was to have 100 pixels free above and below the board
height = 504+200
# delta represents the factor mentioned earlier (dimen of box to hold circle for conect four)
delta = 84
radius = delta // 2

# colors stored in RGB tuple format
WHITE = (255,255,255)
BLUE = (0,0,255)
YELLOW = (255,255,153)
RED = (255,0,0)
BLACK = (0, 0, 0)

# determines the start and end positions of the board (upper left-hand corner anyways)
start_x = 0
start_y = 100
# start is a boolean whether or not to start a game. This allows the restart function seen later
start = True
end_x = width
end_y = height




"""
Holds actual interactive gameplay of Connect Four that allows the game to be played several times! (hence two while loops)
"""
while True:
    gameDisplay = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Had too much to drink?')
    clock = pygame.time.Clock()
    """
    For loop reads the keyboard for inputs
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            """
            allows player to close the window by pressing the 'x'
            """
            print("QUIT")
            pygame.quit()
            gameRunning = False
            quit()
        if event.type == pygame.KEYDOWN:
            # This allows a col to be entered by a number on a key (keys 1 through 7)
            # r resets the game
            col = 0
            if event.key == pygame.K_1:
                col = 1

    pygame.display.update()
    clock.tick(60)
