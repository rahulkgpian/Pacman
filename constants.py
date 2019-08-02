from vectors import Vector2D

# Creating background
TILEWIDTH = 16
TILEHEIGHT = 16
NROWS = 40
NCOLS = 70
SCREENSIZE = (NCOLS*TILEWIDTH, NROWS*TILEHEIGHT)
BLACK = (0, 0, 0, 150)

# Creating Pac-man
UP = Vector2D(0, -1)
DOWN = Vector2D(0, 1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)
STOP = Vector2D()

YELLOW = (255, 255, 0)

# color for nodes
WHITE = (255, 255, 255)
RED = (255, 0, 0)