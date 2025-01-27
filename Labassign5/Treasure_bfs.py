'''Search for Treasure using the Best-First Search
Objective: Use Best-First Search to find a treasure in a grid.
Problem Statement: The treasure is hidden in a grid, and each cell has a heuristic value representing its "closeness" to the treasure. Implement Best-First Search to locate the treasure.
Tasks:
• Use Manhattan distance as a heuristic.
• Implement the algorithm to always move to the most promising cell first (minimum heuristic value).
• Analyze how heuristic choice affects performance.
'''
from queue import PriorityQueue
from typing import List, Tuple, Set
import numpy as np

class TreasureGrid:
    def __init__(self, grid: List[List[int]], treasure_pos: Tuple[int, int]):
        self.grid = np.array(grid)
        self.rows, self.cols = self.grid.shape
        self.treasure_pos = treasure_pos
        
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions."""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                neighbors.append((new_x, new_y))
        return neighbors
    
    def best_first_search(self, start_pos: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
        """
        Implement Best-First Search to find the treasure.
        Returns: (path, nodes_explored)
        """
        frontier = PriorityQueue()
        frontier.put((0, start_pos))
        
        came_from = {start_pos: None}
        nodes_explored = 0
        
        while not frontier.empty():
            _, current = frontier.get()
            nodes_explored += 1
            
            if current == self.treasure_pos:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1], nodes_explored
            
            for next_pos in self.get_neighbors(current):
                if next_pos not in came_from:
                    priority = self.manhattan_distance(next_pos, self.treasure_pos)
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current
        
        return [], nodes_explored  # No path found

def print_path_on_grid(grid: np.ndarray, path: List[Tuple[int, int]]):
    """Visualize the path on the grid."""
    display_grid = grid.copy().astype(str)
    
    # Mark path with '*'
    for x, y in path:
        display_grid[x, y] = '*'
    
    # Mark start and end points
    if path:
        display_grid[path[0]] = 'S'
        display_grid[path[-1]] = 'T'
    
    print("\nPath visualization ('*' marks the path, 'S' is start, 'T' is treasure):")
    print(display_grid)

# Example usage
if __name__ == "__main__":
    # Create a sample grid (lower values indicate better paths)
    grid = [
        [4, 3, 2, 3, 4],
        [3, 2, 1, 2, 3],
        [2, 1, 0, 1, 2],
        [3, 2, 1, 2, 3],
        [4, 3, 2, 3, 4]
    ]
    
    # Set treasure position (center of grid)
    treasure_pos = (2, 2)
    
    # Create TreasureGrid instance
    treasure_grid = TreasureGrid(grid, treasure_pos)
    
    # Run Best-First Search from top-left corner
    start_pos = (0, 0)
    path, nodes = treasure_grid.best_first_search(start_pos)
    
    # Print results
    print("Grid values (lower numbers are better paths):")
    print(np.array(grid))
    print(f"\nPath found: {path}")
    print(f"Number of nodes explored: {nodes}")
    
    # Visualize path
    print_path_on_grid(np.array(grid), path)