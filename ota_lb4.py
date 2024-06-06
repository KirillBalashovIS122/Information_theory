from collections import deque

# Определение графа в виде матрицы смежности
graph = [
    [0, 1, 0, 0, 0, 0, 0, 1], # 1
    [1, 0, 1, 0, 0, 0, 0, 0], # 2
    [0, 1, 0, 1, 0, 1, 0, 1], # 3
    [0, 0, 1, 0, 1, 0, 0, 0], # 4
    [0, 0, 0, 1, 0, 1, 0, 0], # 5
    [0, 0, 1, 0, 1, 0, 1, 1], # 6
    [0, 0, 0, 0, 0, 1, 0, 1], # 7
    [1, 0, 1, 0, 0, 1, 1, 0]  # 8
]

def bfs(graph, start):
    V = len(graph)
    visited = [False] * V
    parent = [None] * V
    
    queue = deque([start])
    visited[start] = True
    
    while queue:
        v = queue.popleft()
        
        for u in range(V):
            if graph[v][u] == 1 and not visited[u]:
                visited[u] = True
                parent[u] = v
                queue.append(u)
                
    return parent

def build_bfs_tree_matrix(parent):
    V = len(parent)
    bfs_tree = [[0] * V for _ in range(V)]
    
    for i in range(V):
        if parent[i] is not None:
            u = parent[i]
            bfs_tree[u][i] = 1
            bfs_tree[i][u] = 1
            
    return bfs_tree

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

start_vertex = 0  # начнем с вершины 1, которая в Python имеет индекс 0
parent = bfs(graph, start_vertex)

# Построение матрицы смежности для дерева поиска в ширину
bfs_tree_matrix = build_bfs_tree_matrix(parent)

# Вывод матрицы смежности
print("Adjacency matrix of the BFS tree:")
print_matrix(bfs_tree_matrix)
