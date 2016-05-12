# Tami, Adam, Misi
# base version for Git

# Import shit
import curses
from curses import wrapper

# Sets up
def initialize(screen):
    global q, dims, R_pos
    # Sets global variables
    R_pos = [0,0]
    q = -1
    dims = screen.getmaxyx()
    # Makes the cursor not blink
    curses.curs_set(False)

# Draws Rezso on the screen
def drawRezso(screen):
    screen.addstr(R_pos[0], R_pos[1], 'R', curses.A_BOLD)

# Reads and interprets the map file into memory
def readMap(screen):
    global wall_coordinates, R_pos
    wall_coordinates = set()
    wall_char = {'#'}
    start_char = {'S','s'}
    a = open('map', 'r')
    f = a.readlines()
    for j in range(0,len(f)):
        for i in range(0,len(f[0])):
            if f[j][i] in start_char:
                R_pos = [j,i]
            if f[j][i] in wall_char:
                #this should follow the curses coordinate system
                wall_coordinates.add((j,i))
            else:
                pass

## need to make coordinates like in curses

# Draws the map (walls, exit, etc) on the screen
def drawMap(screen):
    a = open('map', 'r')
    f = a.read()
    screen.addstr(0, 0, f)

# Controls the movement of Rezso, the 'R' character on screen
def movement(screen):
    # Get global variables
    global R_pos, R_pos_previous, dims, q
    # Save Rezso's position
    R_pos_previous = R_pos
    # Get user input
    q = screen.getch()
    # Movement itself
    if q == curses.KEY_UP and R_pos[0] > 0:
        R_pos[0] -= 1
    elif q == curses.KEY_DOWN and R_pos[0] < dims[0]-1:
        R_pos[0] += 1
    elif q == curses.KEY_LEFT and R_pos[1] > 0:
        R_pos[1] -= 1
    elif q == curses.KEY_RIGHT and R_pos[1] < dims[1]-1:
        R_pos[1] += 1
    else:
        pass

# Decides what happens when Rezso hits a wall or an exit
def checker(screen):
    global R_pos, R_pos_previous
    if (R_pos[0], R_pos[1]) in wall_coordinates:
        screen.addstr(16, 0, 'Wall')
        R_pos = [1,1]
    else:
        pass

# Draws menu, gives tutorial, explains the game
def menu(screen):
    pass

# Define the main() function for the wrapper
def main(screen):
    # We need to pass global variables to the wrapper
    global q
    initialize(screen)
    readMap(screen)
    menu(screen)
    # Make the program run continuously and exit when 'q' is pressed
    while q != ord('q'):
        screen.clear()
        drawMap(screen)
        drawRezso(screen)
        checker(screen)
        screen.addstr(15,0,str(R_pos[0]))
        screen.addstr(15,5,str(R_pos[1]))
        movement(screen)
        checker(screen)
        screen.refresh()
    # End when 'q' is pressed
    curses.endwin()

# Use the wrapper to avoid bugs
wrapper(main)
