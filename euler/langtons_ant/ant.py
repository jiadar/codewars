import sys
import numpy as np


class Constants:
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


class Board:

    def __init__(self, location=(50, 50), orientation=Constants.WEST, color=Constants.WHITE):
        self.location = location
        self.orientation = orientation
        self.graph = {}
        self.graph[location] = color
        
    def move(self, debug=False, step=100, stepsize=25):
        # Save some details about the previous state
        prev_color = self.graph[self.location]
        prev_orientation = self.orientation
        prev_location = self.location
        prev_color_is_black = Constants.FLIP[self.graph[prev_location]] == Constants.BLACK

        # Flip Color at current location. Only keep black in the graph except for the square
        # square that is about to be visited.
        if prev_color_is_black:
            self.graph[prev_location] = Constants.FLIP[self.graph[prev_location]]
        else:
            self.graph.pop(prev_location)

        # Set the color at the next location to white if it has not been visited, otherwise
        # it will not be found during the subsequent move. This is the only white square
        # allowed in the graph
        next_orientation = Constants.ORIENTATION_LOOKUP[prev_color][prev_orientation]        
        next_location = tuple(np.add(prev_location, (Constants.MOVES[next_orientation]['row'],
                                                     Constants.MOVES[next_orientation]['col'])))
        if next_location not in self.graph:
            self.graph[next_location] = Constants.WHITE

        # Set the location and new orientation on the graph
        self.location = next_location
        self.orientation = Constants.ORIENTATION_LOOKUP[prev_color][prev_orientation]

    def num_black_squares(self):
        count = 0
        for v in self.graph.values():
            if v == Constants.BLACK:
                count += 1
        return count
        

if __name__ == "__main__":
    final_step = int(sys.argv[1]) + 1
    steps = range(1, final_step) # should print 118
    ant = Board()
    for step in steps:
        ant.move()
    print(f'Number of black squares at step {step}: {ant.num_black_squares()}')
