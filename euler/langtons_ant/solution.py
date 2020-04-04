import time
import pdb
import pprint
from dataclasses import dataclass, field
import os
import colorama


class g:
    BLACK = 'BLK L'
    WHITE = 'WHT R'    
    NORTH = '^'
    SOUTH = 'v'
    EAST = '>'
    WEST = '<'

    CCW = {
        NORTH: WEST,
        WEST:  SOUTH,
        SOUTH: EAST,
        EAST:  NORTH
    }
    CW = {
        NORTH: EAST,
        EAST:  SOUTH,
        SOUTH: WEST,
        WEST:  NORTH,
    }
    MOVES = {
        NORTH: {'row': -1, 'col': 0},
        WEST: {'row': 0, 'col': -1},
        SOUTH: {'row': 1, 'col': 0},
        EAST: {'row': 0, 'col': 1}
    }
    FLIP = {
        WHITE: BLACK,
        BLACK: WHITE
    }
    ORIENTATION_LOOKUP = {
        BLACK: CCW,
        WHITE: CW
    }


class BoardFun:

    @staticmethod
    def draw(graph, location, orientation, drawsize=20):
        size = 100
        rows = [ [] for x in range(0, size) ]
        for r in range(0, size):
            rows[r] = [ ' ' for c in range(0, size) ]
        for key in graph.keys():
            color = graph[key]
            (row, col) = key
            if color == g.BLACK:
                rows[row][col] = '@'
        row = location[0]
        col = location[1]
        facing_ant = {
            g.NORTH: '^',
            g.WEST:  '<',
            g.SOUTH: 'v',
            g.EAST:  '>'
        }
        rows[row][col] = facing_ant[orientation]
        rval = ''
        rval += 'Ant Facing Dir : ' + orientation + '\n'
        rval += 'Color Under Ant: ' + color + '\n'
        rval += 'Ant Position is: ( {:2}, {:2} )'.format(location[0], location[1]) + '\n'

        s = int((size - drawsize) / 2)
        e = int((size + drawsize) / 2)
        for row in range(s, e):
            rval += '{:2}'.format(row) + ' '
            for col in range(s, e):
                 rval += rows[row][col] + ' '
            rval += '\n'
        rval += '  '
        for x in range(s, e):
            rval += f' {str(x % 10)}'
        print(rval)

    @staticmethod
    def print(location, color, orientation):
        print('({:2}, {:2}): {:6} {:2}'.format(location[0], location[1], color, orientation), end=' ')
#        print('({:2}, {:2}): {:2}'.format(location[0], location[1], state.orientation), end=' ')

    @staticmethod
    def printloc(location):
        print('({:2}, {:2})'.format(location[0], location[1]), end='')
        

class Board:

    def __init__(self, location=(10, 10), boardsize=20, orientation=g.WEST, color=g.WHITE):
        self.location = location
        self.orientation = orientation
        self.graph = {}
        self.graph[location] = color
        self.boardsize = boardsize
        
    def move(self, debug=False, step=100, stepsize=25):
        cur_location = self.location
        (cur_row, cur_col) = cur_location
        cur_color = self.graph[self.location]
        cur_orientation = self.orientation
        next_color = g.FLIP[cur_color]
        next_orientation = g.ORIENTATION_LOOKUP[cur_color][cur_orientation]        
        next_row = cur_row + g.MOVES[next_orientation]['row']
        next_col = cur_col + g.MOVES[next_orientation]['col']
        next_location = (next_row, next_col)

        # Some printing
        if (step % stepsize == 0):
            BoardFun.draw(self.graph, self.location, self.orientation, self.boardsize)
            step and print('Step {:2}: '.format(step), end='')
            BoardFun.print(cur_location, cur_color, cur_orientation)
            print(' ==> ', end=' ')
            BoardFun.print(cur_location, next_color, next_orientation)
            print(' ==> ', end=' ')
            print()

        # Flip Color at current location
        self.graph[cur_location] = next_color

        # Set the color at the next location to white if it has not been visited
        if next_location not in self.graph:
            self.graph[next_location] = g.WHITE
        self.location = next_location
        self.orientation = next_orientation

    def get(self):
        return self.graph


def move_cursor(x, y):
    print("\x1b[{};{}H".format(y+1,x+1))


def clear():
    print("\x1b[2J")
        

map = True
debug = False
stepsize = 100
steps = range(1, 1000)
colorama.init(autoreset=True)
map and move_cursor(0, 0)
map and clear()
ant = Board((50, 50), 30)
for step in steps:
    map and move_cursor(0, 0)
#    map and BoardFun.draw(ant.graph, ant.location, 8)
    pp = pprint.PrettyPrinter(indent=2)
    ant.move(debug=debug, step=step, stepsize=stepsize)
    debug and pp.pprint(ant.get())
    step % stepsize == 0 and os.system('read -sn 1 -p "Press any key to continue..."')
    
    

#pp.pprint(len(graph.keys()))

          
