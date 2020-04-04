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
    def draw(graph, location, orientation, size=20):
        rows = [ [] for x in range(0, size) ]
        for r in range(0, size):
            rows[r] = [ ' ' for c in range(0, size) ]
        for key in graph.keys():
            color = graph[key].color
            (row, col) = key
            if color == g.BLACK:
                rows[row][col] = '@'
        row = location[0]
        col = location[1]
        ori = orientation
        facing_ant = {
            g.NORTH: '^',
            g.WEST:  '<',
            g.SOUTH: 'v',
            g.EAST:  '>'
        }
        rows[row][col] = facing_ant[ori]
        rval = 'Ant Facing Dir : ' + orientation + '\n'
        rval += 'Color Under Ant: ' + color + '\n'
        rval += 'Ant Position is: ( {:2}, {:2} )'.format(location[0], location[1]) + '\n'
        for row in range(0, size):
            rval += '{:2}'.format(row) + ' '
            for col in range(0, size):
                rval += rows[row][col] + ' '
            rval += '\n'
        rval += '  '
        for x in range(0, int(size/10 + 1)):
            rval += ' 0 1 2 3 4 5 6 7 8 9'
        rval += '\n'
        print(rval)

    @staticmethod
    def print(location, color, orientation):
        print('({:2}, {:2}): {:6} {:2}'.format(location[0], location[1], color, orientation), end=' ')
#        print('({:2}, {:2}): {:2}'.format(location[0], location[1], state.orientation), end=' ')

    @staticmethod
    def printloc(location):
        print('({:2}, {:2})'.format(location[0], location[1]), end='')
        

class Board:

    def __init__(self, location=(10, 10), orientation=g.WEST, color=g.WHITE):
        self.location = location
        self.orientation = orientation
        self.graph = {}
        self.graph[location] = color
        
    def move(self, debug=False, step=None):
        debug and BoardFun.draw(self.graph, self.location, 8)
        cur_location = self.location
        (cur_row, cur_col) = cur_location
        cur_color = self.graph[self.location]
        cur_orientation = self.orientation
        next_color = g.FLIP[cur_color]

        # Flip Color at current location
        self.graph[cur_location] = next_color

        next_orientation = g.ORIENTATION_LOOKUP[cur_color][cur_orientation]        
        next_row = cur_row + g.MOVES[next_orientation]['row']
        next_col = cur_col + g.MOVES[next_orientation]['col']
        next_location = (next_row, next_col)
        debug and step and print('{:2}: '.format(step), end='')
        debug and BoardFun.print(cur_location, cur_color, cur_orientation)
        debug and print(' ==> ', end=' ')
        debug and BoardFun.print(cur_location, next_color, next_orientation)
        debug and print(' ==> ', end=' ')
        
        if next_location not in self.graph:
            self.graph[next_location] = default_state
        else:
            self.graph[next_location] = cur_state
        self.location = next_location
        debug and BoardFun.printloc(self.location)
        debug and print()

    def get(self):
        return self.graph


def move_cursor(x, y):
    print("\x1b[{};{}H".format(y+1,x+1))


def clear():
    print("\x1b[2J")
        

map = True
colorama.init(autoreset=True)
map and clear()
map and move_cursor(0, 0)
ant = Board((3,3))
for step in range(1, 12):
    map and move_cursor(0, 0)
#    map and BoardFun.draw(ant.graph, ant.location, 8)
    pp = pprint.PrettyPrinter(indent=2)
    ant.move(debug=True, step=step)
    print()
    map and pp.pprint(ant.get())
    print()
    os.system('read -sn 1 -p "Press any key to continue..."')
    print
    

#pp.pprint(len(graph.keys()))

          
