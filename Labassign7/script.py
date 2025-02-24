import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue, Queue

def manhattan_distance(point1, point2):
    """Calculate Manhattan distance between two points."""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def euclidean_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

def a_star_search(grid, start, goal, heuristic):
    """Perform A* search on a grid."""
    rows, cols = grid.shape
    open_set = PriorityQueue()
    open_set.put((0, start))  # (priority, node)
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while not open_set.empty():
        _, current = open_set.get()
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Reverse the path
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 0:
                move_cost = 14 if dx != 0 and dy != 0 else 10
                tentative_g_score = g_score[current] + move_cost
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))
    
    return None  # No path found

def bfs(grid, start, goal):
    """Perform Breadth-First Search on a grid."""
    rows, cols = grid.shape
    queue = Queue()
    queue.put(start)
    came_from = {}
    
    while not queue.empty():
        current = queue.get()
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 0 and neighbor not in came_from:
                queue.put(neighbor)
                came_from[neighbor] = current
    
    return None

def uniform_cost_search(grid, start, goal):
    """Perform Uniform Cost Search on a grid."""
    rows, cols = grid.shape
    open_set = PriorityQueue()
    open_set.put((0, start))  # (cost-so-far, node)
    
    came_from = {}
    cost_so_far = {start: 0}
    
    while not open_set.empty():
        _, current = open_set.get()
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 0:
                new_cost = cost_so_far[current] + 10
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    open_set.put((priority, neighbor))
                    came_from[neighbor] = current
    
    return None

def visualize_path(grid, paths_dict):
    """Visualize the grid and paths from different algorithms."""
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap='Greys', origin='lower')
    
    colors = {'A*_Manhattan': 'red', 'A*_Euclidean': 'blue', 'BFS': 'green', 'UCS': 'orange'}
    
    for algo_name, path in paths_dict.items():
        if path:
            for point in path:
                plt.plot(point[1], point[0], 'o', color=colors.get(algo_name))
    
    plt.title("Pathfinding Algorithms Comparison")
    plt.show()

# Define the grid (0: free space; 1: obstacle)
grid = np.array([
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0]
])

start = (0, 0)   # Starting point
goal = (4, 4)    # Goal point

# Perform searches with different algorithms
path_a_star_manhattan = a_star_search(grid.copy(), start=start,
                                      goal=goal,
                                      heuristic=manhattan_distance)

path_a_star_euclidean = a_star_search(grid.copy(), start=start,
                                      goal=goal,
                                      heuristic=euclidean_distance)

path_bfs = bfs(grid.copy(), start=start,
               goal=goal)

path_ucs = uniform_cost_search(grid.copy(), start=start,
                               goal=goal)

# Visualize results
paths_dict = {
    "A*_Manhattan": path_a_star_manhattan,
    "A*_Euclidean": path_a_star_euclidean,
    "BFS": path_bfs,
    "UCS": path_ucs
}

visualize_path(grid=grid.copy(), paths_dict=paths_dict)
