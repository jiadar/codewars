import time
import pdb
import numpy as np
import pprint
from dataclasses import dataclass, field
import os
import colorama


class g:
    BLACK = 'BLK'
    WHITE = 'WHT'    
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


class BoardUtils:

    @staticmethod
    def _draw(graph, location, orientation, drawsize=20):
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
        print('({:2}, {:2}): {:3} {:1}'.format(location[0], location[1], color, orientation))

    @staticmethod
    def draw(graph,
             location,
             orientation,
             boardsize,
             prev_location,
             prev_color,
             prev_orientation,
             next_color,
             next_orientation,
             num_black_squares,
             step=True):
        BoardUtils._draw(graph, location, orientation, boardsize)
        step and print('Step {:6}: '.format(step), end='')
        BoardUtils.print(prev_location, prev_color, prev_orientation)
        print('Change to  : ', end='')
        BoardUtils.print(prev_location, next_color, next_orientation)
        print('Move to    : ', end='')
        BoardUtils.print(location, graph[location], orientation)
        print('BLK Squares: {:6}'.format(num_black_squares))


class Board:

    def __init__(self, location=(10, 10), boardsize=20, orientation=g.WEST, color=g.WHITE):
        self.location = location
        self.orientation = orientation
        self.graph = {}
        self.graph[location] = color
        self.boardsize = boardsize
        
    def move(self, debug=False, step=100, stepsize=25):
        # Save previos location, color, and orientation for printing the board
        prev_location = self.location
        prev_color = self.graph[self.location]
        prev_orientation = self.orientation
        next_orientation = g.ORIENTATION_LOOKUP[prev_color][prev_orientation]        
        next_location = tuple(np.add(prev_location, (g.MOVES[next_orientation]['row'],
                                                     g.MOVES[next_orientation]['col'])))
        next_color = g.FLIP[prev_color]

        # Flip Color at current location. Only keep black in the graph
        if next_color == g.BLACK:
            self.graph[prev_location] = next_color
        else:
            self.graph.pop(prev_location)

        # Set the color at the next location to white if it has not been visited
        if next_location not in self.graph:
            self.graph[next_location] = g.WHITE
        self.location = next_location
        self.orientation = next_orientation

        # Some printing
        draw_data = {
            'graph': self.graph,
            'location': self.location,
            'orientation': self.orientation,
            'boardsize': self.boardsize,
            'prev_location': prev_location,
            'prev_color': prev_color,
            'prev_orientation': prev_orientation,
            'next_color': next_color,
            'next_orientation': next_orientation,
            'num_black_squares': self.num_black_squares(),
            'step': step
        }
        step % stepsize == 0 and BoardUtils.draw(**draw_data)
        
    def num_black_squares(self):
        count = 0
        for v in self.graph.values():
            if v == g.BLACK:
                count += 1
        return count
        
    def get(self):
        return self.graph


def move_cursor(x, y):
    print("\x1b[{};{}H".format(y+1,x+1))


def clear():
    print("\x1b[2J")
        

map = True
debug = False
stepsize = 50
steps = range(1, 1000)
boardstart = (50, 50)
boardsize = 20

pp = pprint.PrettyPrinter(indent=2)
colorama.init(autoreset=True)
map and move_cursor(0, 0)
map and clear()
ant = Board(boardstart, boardsize)
for step in steps:
    map and move_cursor(0, 0)
    map and debug and clear()
    ant.move(debug=debug, step=step, stepsize=stepsize)
    graph = ant.get()
    debug and print('\nGraph:')
    debug and pp.pprint(graph)
    step % stepsize == 0 and os.system('read -sn 1 -p "Press any key to continue..."')
    
clear()
move_cursor(0, 0)
graph = ant.get()
pp.pprint(graph)
print(f'Number of black squares at step {step}: {len(graph.keys())}')

#pp.pprint(len(graph.keys()))

          
