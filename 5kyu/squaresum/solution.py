from typing import Dict, Set
import math

import pprint


class Graph:
    def __init__(self):
        self.adj: Dict[int, Set[int]] = dict()

    def __repr__(self):
        return pprint.pformat(dict(self.adj))

    def add_edge(self, vertex1: int, vertex2: int):
        if vertex1 in self.adj:
            self.adj[vertex1].add(vertex2)
        else:
            self.adj[vertex1] = set([vertex2])

    def dfs_vertex_cover(self, u, visited, path):
        visited.append(u)
        path.append(u)
        if len(path) == len(self.adj.keys()):
            print(path)
            return path

        else:
            for i in [e for e in self.adj[u] if e not in visited]:
                self.dfs_vertex_cover(i, visited, path)

        path.pop()
        visited.remove(u)


def squaresum(n: int):
    g = Graph()
    perfect_squares = [i ** 2 for i in range(1, int(math.sqrt(2 * n)) + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i + j in perfect_squares:
                g.add_edge(i, j)
                g.add_edge(j, i)

    pprint.pprint(g)
    for i in range(1, 16):
        path = g.dfs_vertex_cover(i, [], [])
        if path:
            print(path)


if __name__ == "__main__":
    squaresum(15)
