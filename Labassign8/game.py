import math
import heapq
from collections import deque

BOARD_SPECIAL = {
    # Ladders
    2: 38, 7: 14, 8: 31, 15: 26, 21: 42,
    28: 84, 36: 44, 51: 67, 71: 91, 78: 98, 87: 94,
    # Snakes
    16: 6, 46: 25, 49: 11, 62: 19, 64: 60,
    74: 53, 89: 68, 92: 88, 95: 75, 99: 80
}

START = 1
GOAL = 100

def bfs(start, goal, board):
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for dice in range(1, 7):
            next_square = current + dice
            if next_square > goal:
                continue
            if next_square in board:
                next_square = board[next_square]
            if next_square not in visited:
                visited.add(next_square)
                queue.append((next_square, path + [next_square]))
    return None

def dfs(current, goal, board, visited, path):
    if current == goal:
        return path
    visited.add(current)
    for dice in range(1, 7):
        next_square = current + dice
        if next_square > goal:
            continue
        if next_square in board:
            next_square = board[next_square]
        if next_square not in visited:
            result = dfs(next_square, goal, board, visited, path + [next_square])
            if result:
                return result
    return None

def heuristic(square, goal):
    return math.ceil((goal - square) / 6) if square < goal else 0

def a_star(start, goal, board):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start, [start]))
    g_score = {start: 0}
    
    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        for dice in range(1, 7):
            next_square = current + dice
            if next_square > goal:
                continue
            if next_square in board:
                next_square = board[next_square]
            tentative_g = g + 1
            if next_square not in g_score or tentative_g < g_score[next_square]:
                g_score[next_square] = tentative_g
                f_score = tentative_g + heuristic(next_square, goal)
                heapq.heappush(open_set, (f_score, tentative_g, next_square, path + [next_square]))
    return None

def main():
    print("Snake and Ladder Solver")
    print("===========================\n")
    
    # BFS Implementation
    bfs_path = bfs(START, GOAL, BOARD_SPECIAL)
    print(f"BFS Path ({len(bfs_path)-1} moves): {bfs_path}") if bfs_path else print("BFS: No path found")
    
    # DFS Implementation
    dfs_path = dfs(START, GOAL, BOARD_SPECIAL, set(), [START])
    print(f"\nDFS Path ({len(dfs_path)-1} moves): {dfs_path}") if dfs_path else print("DFS: No path found")
    
    # A* Implementation
    astar_path = a_star(START, GOAL, BOARD_SPECIAL)
    print(f"\nA* Path ({len(astar_path)-1} moves): {astar_path}") if astar_path else print("A*: No path found")

if __name__ == "__main__":
    main()
