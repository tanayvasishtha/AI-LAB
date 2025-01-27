'''
Uniform Cost Search for Optimal Path
Objective: Implement Uniform Cost Search for a weighted graph.
Problem Statement: Given a weighted graph (e.g., a transportation network with travel costs), find the minimum-cost path between two nodes
Tasks:
• Represent the graph as an adjacency list.
• Implement Uniform Cost Search to find the optimal path.
• Compare it with BFS for unweighted graphs
'''

from collections import defaultdict
import heapq
import time

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, from_node, to_node, cost):
        """Add an edge to the graph with its associated cost"""
        self.graph[from_node].append((to_node, cost))
    
    def uniform_cost_search(self, start, goal):
        """
        Implement Uniform Cost Search to find the minimum cost path
        Returns: (path, total_cost, visited_nodes) tuple if path exists, else (None, None, None)
        """
        pq = [(0, start, [start])]
        visited = set()
        visited_order = []  # To track order of node exploration
        
        while pq:
            total_cost, current_node, path = heapq.heappop(pq)
            
            if current_node == goal:
                return path, total_cost, visited_order
            
            if current_node in visited:
                continue
                
            visited.add(current_node)
            visited_order.append(current_node)
            
            for neighbor, edge_cost in self.graph[current_node]:
                if neighbor not in visited:
                    new_cost = total_cost + edge_cost
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))
        
        return None, None, visited_order

    def breadth_first_search(self, start, goal):
        """
        Implement BFS for comparison
        Returns: (path, visited_nodes) if exists, else (None, None)
        """
        queue = [(start, [start])]
        visited = set()
        visited_order = []
        
        while queue:
            current_node, path = queue.pop(0)
            
            if current_node == goal:
                return path, visited_order
                
            if current_node in visited:
                continue
                
            visited.add(current_node)
            visited_order.append(current_node)
            
            for neighbor, _ in self.graph[current_node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        
        return None, visited_order

def calculate_path_cost(graph, path):
    """Calculate the total cost of a given path"""
    if not path:
        return None
    cost = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        for neighbor, edge_cost in graph.graph[current]:
            if neighbor == next_node:
                cost += edge_cost
                break
    return cost

def compare_algorithms(graph, start, goal):
    """Compare UCS and BFS performance"""
    # UCS
    ucs_start_time = time.time()
    ucs_path, ucs_cost, ucs_visited = graph.uniform_cost_search(start, goal)
    ucs_time = time.time() - ucs_start_time
    
    # BFS
    bfs_start_time = time.time()
    bfs_path, bfs_visited = graph.breadth_first_search(start, goal)
    bfs_time = time.time() - bfs_start_time
    bfs_cost = calculate_path_cost(graph, bfs_path)
    
    return {
        'ucs': {
            'path': ucs_path,
            'cost': ucs_cost,
            'visited': ucs_visited,
            'time': ucs_time
        },
        'bfs': {
            'path': bfs_path,
            'cost': bfs_cost,
            'visited': bfs_visited,
            'time': bfs_time
        }
    }

def main():
    # Example 1: Simple case where UCS and BFS find different paths
    print("\nExample 1: Simple case with different optimal paths")
    g1 = Graph()
    g1.add_edge('A', 'B', 1)
    g1.add_edge('B', 'D', 6)
    g1.add_edge('A', 'C', 2)
    g1.add_edge('C', 'D', 3)
    
    results1 = compare_algorithms(g1, 'A', 'D')
    print_comparison_results(results1)
    
    # Example 2: More complex graph with multiple possible paths
    print("\nExample 2: Complex graph with multiple paths")
    g2 = Graph()
    g2.add_edge('A', 'B', 4)
    g2.add_edge('A', 'C', 1)
    g2.add_edge('B', 'D', 3)
    g2.add_edge('C', 'B', 2)
    g2.add_edge('C', 'D', 6)
    g2.add_edge('D', 'E', 2)
    g2.add_edge('B', 'E', 10)
    g2.add_edge('C', 'E', 12)
    
    results2 = compare_algorithms(g2, 'A', 'E')
    print_comparison_results(results2)

def print_comparison_results(results):
    """Print formatted comparison results"""
    print("\nUniform Cost Search:")
    print(f"Path: {' -> '.join(results['ucs']['path'])}")
    print(f"Cost: {results['ucs']['cost']}")
    print(f"Nodes explored: {' -> '.join(results['ucs']['visited'])}")
    print(f"Time taken: {results['ucs']['time']:.6f} seconds")
    
    print("\nBreadth First Search:")
    print(f"Path: {' -> '.join(results['bfs']['path'])}")
    print(f"Cost: {results['bfs']['cost']}")
    print(f"Nodes explored: {' -> '.join(results['bfs']['visited'])}")
    print(f"Time taken: {results['bfs']['time']:.6f} seconds")

if __name__ == "__main__":
    main()