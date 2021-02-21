import pprint
import queue


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj_list = {}

        for i in self.vertices:
            self.adj_list[i] = []

    def add_vertex(self, vertex):
        self.adj_list[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        self.adj_list[from_vertex].append(to_vertex)


vertices = []
n = 15

for i in range(1, n + 1):
    vertices.append(i)

plot = Graph(vertices)


def is_square(num):
    increment = 2
    while increment <= num / increment:
        if num / increment == increment:
            return True
        else:
            increment += 1


squares_list = []
for i in range(2, 2 * n + 1):
    if is_square(i):
        squares_list.append(i)

for j in range(1, n + 1):
    for k in range(len(squares_list)):
        if squares_list[k] - j in plot.adj_list.keys():
            plot.add_edge(j, squares_list[k] - j)


print(squares_list)
pprint.pprint(plot.adj_list)

plot_travel = []
# visited = [False] * n


# def bfs(graph, start_ver):
#     stack = [start_ver]
#     while len(stack) > 0:
#         start_ver = stack.pop()
#         if not visited[int(start_ver) - 1]:
#             plot_travel.append(start_ver)
#             visited[int(start_ver) - 1] = True
#             for neighbors in plot.adj_list[start_ver]:
#                 if not visited[int(neighbors) - 1]:
#                     stack.append(neighbors)
#     if visited == [True] * n:
#         return plot_travel


def bfs(graph, start_ver):
    q = queue.Queue()
    visited = []
    path = []
    q.put(start_ver)
    while not q.empty():
        cur = q.get()
        if cur not in visited:
            path.append(cur)
            visited.append(cur)
            for neighbor in graph.adj_list[cur]:
                if neighbor not in visited:
                    q.put(neighbor)
    if len(visited) == n:
        return path


pprint.pprint(bfs(plot, 6))
