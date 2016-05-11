# Tami, Adam, Misi
# base version for Git

# Import shit
import curses
from curses import wrapper

# Sets up
def initialize(screen):
    global y, x, q, dims
    # Sets global variables
    y = 0
    x = 0
    q = -1
    dims = screen.getmaxyx()
    # Makes the cursor not blink
    curses.curs_set(False)

# Draws Rezso on the screen
def drawRezso(screen):
    screen.addstr(y, x, 'R', curses.A_BOLD)

# Draws the map (walls, exit, etc) on the screen
def drawMap(screen):
    pass

# Controls the movement of Rezso, the 'R' character on screen
def movement(screen):
    # Get global variables
    global y, x, dims, q
    # Get user input
    q = screen.getch()
    # Movement itself
    # Gets max y and x coordinates in a list
    if q == curses.KEY_UP and y > 0:
        y -= 1
    elif q == curses.KEY_DOWN and y < dims[0]-2:
        y += 1
    elif q == curses.KEY_LEFT and x > 0:
        x -= 1
    elif q == curses.KEY_RIGHT and x < dims[1]-2:
        x += 1

# Decides what happens when Rezso hits a wall or an exit
def checker(screen):
    pass

# Draws menu, gives tutorial, explains the game
def menu(screen):
    pass

# Define the main() function for the wrapper

def main(screen):
    # Get global variables
    global y, x, dims, q
    initialize(screen)
    menu(screen)
    # Make the program run continuously and exit when 'q' is pressed
    while q != ord('q'):
        screen.clear()
        drawRezso(screen)
        drawMap(screen)
        movement(screen)
        checker(screen)
        screen.refresh()
    # End when 'q' is pressed
    curses.endwin()

# Use the wrapper to avoid bugs
wrapper(main)
