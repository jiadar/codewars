import pdb
import queue
import enum
import pprint
from itertools import permutations
from typing import List


class Solution:

    graph = {}
    
    def vertices(self):
        return list(self.graph.keys())

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, edge):
        if len(edge) < 2:
            return
        (vertex1, vertex2) = edge
        if vertex1 in self.graph:
            if (vertex2 not in self.graph[vertex1] and vertex1 != vertex2):
                self.graph[vertex1].append(vertex2)
        else:
            self.graph[vertex1] = [vertex2]

    def edges(self):
        edge_list = []
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                if {neighbour, vertex} not in edge_list:
                    edge_list.append({vertex, neighbour})
        return edge_list
    
    def to_str(self):
        res = "vertices: "
        for k in self.graph:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res

    def g(self):
        return self.graph
    
    class Direction(enum.Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    @staticmethod
    def move(board, direction):
        board_lst = list(board)
        zero_idx = board_lst.index('0');
        operator = {
            Solution.Direction.UP: -3,
            Solution.Direction.DOWN: 3,
            Solution.Direction.LEFT: -1,
            Solution.Direction.RIGHT: 1
        }

        left_not_possible = (zero_idx == 0 or zero_idx == 3)
        right_not_possible = (zero_idx == 2 or zero_idx == 5)
        up_not_possible = (zero_idx < 3)
        down_not_possible = (zero_idx > 2)

        move_not_possible = ((direction == Solution.Direction.LEFT and left_not_possible) or
                             (direction == Solution.Direction.RIGHT and right_not_possible) or
                             (direction == Solution.Direction.DOWN and down_not_possible) or
                             (direction == Solution.Direction.UP and up_not_possible))
        
        if move_not_possible:
            return board

        swap_idx = zero_idx + operator[direction]
        board_lst[swap_idx], board_lst[zero_idx] = board_lst[zero_idx], board_lst[swap_idx]
        return ''.join(board_lst)

    def find_path(self, start_vertex, end_vertex, path=None):
        if path == None:
            path = []
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in self.graph:
            return None
        for vertex in self.graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, 
                                               end_vertex, 
                                               path)
                if extended_path:
                    return extended_path
        return None

    def bfs(self, start, goal='123450'):
        visited = {vertex: False for vertex in self.graph.keys()}
        # parents = {}
        levels = {}
        q = queue.Queue()
        visited[start] = True
        levels[start] = 0
        q.put(start)
        while not q.empty():
            v = q.get()
            if (v == goal):
                return levels[goal]
            for adjacent in self.graph[v]:
                if not visited[adjacent]:
                    visited[adjacent] = True
                    # parents[adjacent] = v
                    q.put(adjacent)
                    levels[adjacent] = levels[v] + 1
                    
s = Solution()
base_board = '012345'
for board_tuple in permutations(base_board):
    board = ''.join(board_tuple)
    for direction in [s.Direction.UP, s.Direction.DOWN, s.Direction.LEFT, s.Direction.RIGHT]:
        next_board = Solution.move(board, direction)
        s.add_edge((board, next_board))

path = s.bfs('123540')
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(path)
#pp.pprint(path)
#pp.pprint(s.g())
#graph = s.g()
#pdb.set_trace()
