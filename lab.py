# Tami, Adam, Misi
# base version for Git

# Import libraries and methods that we need
import curses, random
from curses import wrapper
from copy import deepcopy

# A collection of things that need to be done in the beggining, after readMap()
def initialize(screen):
    global q, map_fog_of_war

    # Set global variables
    q = -1
    map_fog_of_war = set()

    # Makes the cursor not blink
    curses.curs_set(False)

# Generates the position of the key, has to run after readMap()
def keyDropM():
    global key_drop_coordinates
    key_drop = random.sample(space_coordinates, 1)
    key_drop_coordinates = (0, 0)
    key_drop_coordinates = key_drop[0]

# Draws Rezso on the screen
def drawRezso(screen):
    screen.addstr(R_pos[0], R_pos[1], 'R')

# Reads and interprets the map file into memory, we use a lot of global
# variables, maybe there is a better way to do this?
def readMap(screen):
    global map_in_memory, R_pos, wall_coordinates, space_coordinates, key_coordinates, win_coordinates, start_char, wall_char_ver, wall_char_hor, space_char, key_char, win_char

    # Set up variables
    map_in_memory = []
    map_fog_of_war = set()
    wall_coordinates = set()
    space_coordinates = set()
    key_coordinates = set()
    win_coordinates = set()
    start_char = {'S'}
    wall_char_ver = {'8'}
    wall_char_hor = {'a'}
    space_char = {' '}
    key_char = {'K'}
    win_char = {'W'}

    # Read the map file lines into a list
    f = open('map', 'r')
    map_in_memory = f.readlines()
    f.close()

    # Make a nested list representation of the map for each character and
    # collect data into the sets
    for j in range(0,len(map_in_memory)):
        for i in range(0,len(map_in_memory[0])):

            # Rezso's starting position
            if map_in_memory[j][i] in start_char:
                R_pos = [j,i]

            # Space where you can move
            if map_in_memory[j][i] in space_char:
                space_coordinates.add((j, i))

            # Door that will open when you find the key
            if map_in_memory[j][i] in key_char:
                key_coordinates.add((j, i))
                wall_coordinates.add((j, i))

            # Where you need to get to win
            if map_in_memory[j][i] in win_char:
                win_coordinates.add((j, i))

            # Where the walls are
            if map_in_memory[j][i] in wall_char_hor:
                wall_coordinates.add((j, i))

            if map_in_memory[j][i] in wall_char_ver:
                wall_coordinates.add((j, i))

# Draws the map (walls, exit, etc) on the screen
def drawMap(screen):
    for j in range(0,len(map_in_memory)):
        for i in range(0,len(map_in_memory[0])):

            if map_in_memory[j][i] in space_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, ' ')

            if map_in_memory[j][i] in key_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, '?')

            if map_in_memory[j][i] in start_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, '▫')

            if map_in_memory[j][i] in wall_char_hor:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, 'a')

            if map_in_memory[j][i] in wall_char_ver:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, '8')

            if map_in_memory[j][i] in win_char:
                if (j,i) in map_fog_of_war:
                    screen.addstr(j, i, '☺')

            # We draw the key not from the map
            #if map_in_memory[j][i] in key_drop_coordinates:
            if (j,i) in map_fog_of_war:
                screen.addstr(key_drop_coordinates[0], key_drop_coordinates[1], 'k')
            else:
                pass

# Controls the movement of Rezso, the 'R' character on screen
def movement(screen):
    global R_pos, R_pos_previous, q, map_fog_of_war

    # Save Rezso's position
    R_pos_previous = deepcopy(R_pos)

    # Add coordinates to map_fog_of_war set
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
    elif q == curses.KEY_DOWN and R_pos[0] < map_dim[0]-1:
        R_pos[0] += 1
    elif q == curses.KEY_LEFT and R_pos[1] > 0:
        R_pos[1] -= 1
    elif q == curses.KEY_RIGHT and R_pos[1] < map_dim[1]-1:
        R_pos[1] += 1
    else:
        pass

# Decides what happens when Rezso moves into an entity, e.g. a wall
def checker(screen):
    global R_pos, R_pos_previous, wall_coordinates, key_coordinates

    # Makes walls impenetrable
    if (R_pos[0], R_pos[1]) in wall_coordinates:
        R_pos = deepcopy(R_pos_previous)

    # Removes the keys blocking the exit when you pick up the key
    if (R_pos[0], R_pos[1]) == (key_drop_coordinates[0], key_drop_coordinates[1]):
        wall_coordinates -= key_coordinates

# Draws menu, gives tutorial, explains the game
def menu(screen):
    pass

# Checks if terminal is big enough for map, this is independent from wrapper
def testTerminal():
    global map_dim

    # Read map into list
    f = open('map', 'r')
    map_test = f.readlines()
    f.close()

    # Save map dimensions
    map_dim = [0,0]
    map_dim[0] = len(map_test)
    map_dim[1] = len(map_test[0])

    # Test size of terminal
    openpage = curses.initscr()
    max_y, max_x = openpage.getmaxyx()
    if map_dim[0] > max_y or map_dim[1] > max_x:
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

    readMap(screen)
    initialize(screen)
    keyDropM()
    menu(screen)

    while q != ord('q'):
        screen.clear()
        drawMap(screen)
        drawRezso(screen)
        checker(screen)
        movement(screen)
        checker(screen)
        screen.refresh()
    curses.endwin()

# Use the wrapper to avoid bugs
testTerminal()
wrapper(main)
