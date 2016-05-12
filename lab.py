# Tami, Adam, Misi
# base version for Git

# Import shit
import curses
from curses import wrapper
from copy import deepcopy
# Sets up
def initialize(screen):
    global q, dims, R_pos, map_fog_of_war
    # Sets global variables
    R_pos = [0,0]
    q = -1
    dims = screen.getmaxyx()
    map_fog_of_war = set()
    # Makes the cursor not blink
    curses.curs_set(False)

# Draws Rezso on the screen
def drawRezso(screen):
    screen.addstr(R_pos[0], R_pos[1], 'R', curses.A_BOLD)

# Reads and interprets the map file into memory
def readMap(screen):
    global wall_coordinates, wall_char, start_char, space_char, R_pos, map_in_memory, map_dim
    # Set up variables
    map_dim = [0,0]
    map_in_memory = []
    map_fog_of_war = set()
    wall_coordinates = set()
    wall_char = {'#'}
    start_char = {'S'}
    space_char = {' '}
    # Read the map file lines into a list
    f = open('map', 'r')
    map_in_memory = f.readlines()
    f.close()
    # Save map dimensions
    map_dim[0] = len(map_in_memory)
    map_dim[1] = len(map_in_memory[0])
    # Make a nested list representation of the map for each character
    for j in range(0,len(map_in_memory)):
        for i in range(0,len(map_in_memory[0])):
            if map_in_memory[j][i] in start_char:
                R_pos = [j,i]
            if map_in_memory[j][i] in wall_char:
                #this should follow the curses coordinate system
                wall_coordinates.add((j,i))

## need to make coordinates like in curses

# Draws the map (walls, exit, etc) on the screen, we can tell it how
def drawMap(screen):
    for j in range(0,len(map_in_memory)):
        for i in range(0,len(map_in_memory[0])):
            if map_in_memory[j][i] in space_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, ' ')
            if map_in_memory[j][i] in start_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, '▫')
            if map_in_memory[j][i] in wall_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, '⦁')

# Controls the movement of Rezso, the 'R' character on screen
def movement(screen):
    # Get global variables
    global R_pos, R_pos_previous, dims, q, map_fog_of_war
    # Save Rezso's position
    R_pos_previous = deepcopy(R_pos)
    # Add coordinates to  map_fog_of_war set
    map_fog_of_war.add((R_pos[0]-1, R_pos[1]-1))
    map_fog_of_war.add((R_pos[0]-1, R_pos[1]+0))
    map_fog_of_war.add((R_pos[0]-1, R_pos[1]+1))
    map_fog_of_war.add((R_pos[0]+0, R_pos[1]-1))
    map_fog_of_war.add((R_pos[0]+0, R_pos[1]+0))
    map_fog_of_war.add((R_pos[0]+0, R_pos[1]+1))
    map_fog_of_war.add((R_pos[0]+1, R_pos[1]-1))
    map_fog_of_war.add((R_pos[0]+1, R_pos[1]+0))
    map_fog_of_war.add((R_pos[0]+1, R_pos[1]+1))
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
        R_pos = deepcopy(R_pos_previous)
    else:
        pass

# Draws menu, gives tutorial, explains the game
def menu(screen):
    pass

# Checks if terminal is big enough for map
def testpage():
    f = open('map', 'r')
    map_in_memory = f.readlines()
    f.close()
    # Save map dimensions
    map_dim = [0,0]
    map_dim[0] = len(map_in_memory)
    map_dim[1] = len(map_in_memory[0])
    openpage = curses.initscr()
    maxy, maxx = openpage.getmaxyx()
    if map_dim[0] > maxy or map_dim[1] > maxx:
        print("Please make the terminal at least " + str(map_dim[1]) +
        " characters wide and " + str(map_dim[0]) + " characters long")
        curses.endwin()
        quit()
    else:
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
#        screen.addstr(15,0,str(R_pos[0]))
#        screen.addstr(15,5,str(R_pos[1]))
        movement(screen)
        checker(screen)
        screen.refresh()
    # End when 'q' is pressed
    curses.endwin()


# Use the wrapper to avoid bugs
testpage()
wrapper(main)
