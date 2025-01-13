from pyMaze import maze, agent, COLOR, textLabel
from bfs import BFS
from dfs import DFS
import time

class MazeComparison:
    def __init__(self, rows, cols, loop_percent=20):
        """
        Initialize maze comparison with given dimensions
        
        Args:
            rows (int): Number of rows in maze
            cols (int): Number of columns in maze
            loop_percent (int): Percentage of loops in maze (0-100)
        """
        self.rows = rows
        self.cols = cols
        self.loop_percent = loop_percent
        self.maze = None
        self.results = {}

    def create_maze(self):
        """Create a new maze with specified dimensions"""
        self.maze = maze(self.rows, self.cols)
        self.maze.CreateMaze(loopPercent=self.loop_percent)
        return self.maze

    def solve_maze(self):
        """
        Solve maze using both BFS and DFS algorithms
        Returns dict with solving metrics
        """
        if not self.maze:
            self.create_maze()

        # BFS solution
        bfs_start_time = time.time()
        bfs_path = BFS(self.maze)
        bfs_time = time.time() - bfs_start_time
        bfs_explored = len(set(bfs_path.keys()) | set(bfs_path.values()))

        # DFS solution
        dfs_start_time = time.time()
        dfs_path = DFS(self.maze)
        dfs_time = time.time() - dfs_start_time
        dfs_explored = len(set(dfs_path.keys()) | set(dfs_path.values()))

        self.results = {
            'bfs': {
                'path': bfs_path,
                'explored_cells': bfs_explored,
                'path_length': len(bfs_path) + 1,
                'time': bfs_time
            },
            'dfs': {
                'path': dfs_path,
                'explored_cells': dfs_explored,
                'path_length': len(dfs_path) + 1,
                'time': dfs_time
            }
        }
        return self.results

    def visualize(self, delay=300):
        """
        Visualize both BFS and DFS paths on the maze
        
        Args:
            delay (int): Delay between steps in milliseconds
        """
        if not self.results:
            self.solve_maze()

        # Create agents
        bfs_agent = agent(self.maze, footprints=True, color=COLOR.blue, shape='square')
        dfs_agent = agent(self.maze, footprints=True, color=COLOR.red, shape='square')

        # Add path tracers
        self.maze.tracePath({bfs_agent: self.results['bfs']['path']}, delay=delay)
        self.maze.tracePath({dfs_agent: self.results['dfs']['path']}, delay=delay)

        # Add metrics labels
        textLabel(self.maze, 'BFS Path Length', self.results['bfs']['path_length'])
        textLabel(self.maze, 'BFS Cells Explored', self.results['bfs']['explored_cells'])
        textLabel(self.maze, 'BFS Time (s)', f"{self.results['bfs']['time']:.3f}")
        
        textLabel(self.maze, 'DFS Path Length', self.results['dfs']['path_length'])
        textLabel(self.maze, 'DFS Cells Explored', self.results['dfs']['explored_cells'])
        textLabel(self.maze, 'DFS Time (s)', f"{self.results['dfs']['time']:.3f}")

        # Run visualization
        self.maze.run()

def run_comparison_tests(test_sizes=None):
    """
    Run comparison tests for different maze sizes
    
    Args:
        test_sizes (list): List of tuples containing (rows, cols) for different maze sizes
    """
    if test_sizes is None:
        test_sizes = [(5,5), (10,10), (15,15)]

    print("\nMaze Solver Comparison Results:")
    print("-" * 60)

    for size in test_sizes:
        print(f"\nMaze Size: {size[0]}x{size[1]}")
        print("-" * 30)
        
        try:
            comparison = MazeComparison(*size)
            results = comparison.solve_maze()

            # Print BFS results
            print("BFS Results:")
            print(f"  - Cells Explored: {results['bfs']['explored_cells']}")
            print(f"  - Path Length: {results['bfs']['path_length']}")
            print(f"  - Time: {results['bfs']['time']:.3f} seconds")

            # Print DFS results
            print("DFS Results:")
            print(f"  - Cells Explored: {results['dfs']['explored_cells']}")
            print(f"  - Path Length: {results['dfs']['path_length']}")
            print(f"  - Time: {results['dfs']['time']:.3f} seconds")

            # Calculate efficiency metrics
            bfs_efficiency = results['bfs']['path_length'] / results['bfs']['explored_cells']
            dfs_efficiency = results['dfs']['path_length'] / results['dfs']['explored_cells']
            print("\nEfficiency (Path Length / Cells Explored):")
            print(f"  - BFS: {bfs_efficiency:.3f}")
            print(f"  - DFS: {dfs_efficiency:.3f}")

            # Visualize the paths
            comparison.visualize()

        except Exception as e:
            print(f"Error running comparison for size {size}: {str(e)}")

if __name__ == '__main__':
    # Run tests with different maze sizes
    test_sizes = [
        (5, 5),    # Small maze
        (10, 10),  # Medium maze
        (15, 15),  # Large maze
    ]
    run_comparison_tests(test_sizes)