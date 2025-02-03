"""Solve the 8-puzzle using A* search
Problem Statement: The 8-puzzle involves sliding tiles to achieve a goal state. Use A* to solve it.
Tasks:
Define heuristic functions:
H1: Number of misplaced tiles.
H2: Sum of Manhattan distances of all tiles from their goal positions.
Implement A* with both heuristics.
Compare the performance of the two heuristics in terms of the number of nodes explored and solution depth."""



import heapq
import sys
import time

# Define the goal state (using 0 as the blank)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state    # Puzzle state as a tuple of length 9
        self.parent = parent  # Parent Node for reconstructing the solution path
        self.g = g            # Cost from the start node
        self.h = h            # Heuristic cost to goal (depends on chosen heuristic)
        self.f = g + h        # Total cost

    def __lt__(self, other):
        return self.f < other.f

def misplaced_tiles(state):
    """Heuristic H1: Count of misplaced tiles (excluding the blank)."""
    return sum(1 for i, tile in enumerate(state) if tile != 0 and tile != goal_state[i])

def manhattan_distance(state):
    """Heuristic H2: Sum of Manhattan distances for each tile (excluding the blank)."""
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            current_row, current_col = divmod(i, 3)
            # Find the position of the tile in the goal state
            goal_index = goal_state.index(tile)
            goal_row, goal_col = divmod(goal_index, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    """Generate valid neighboring states by sliding the blank."""
    neighbors = []
    blank_index = state.index(0)
    row, col = divmod(blank_index, 3)
    moves = []
    if row > 0: moves.append(-3)  # Up
    if row < 2: moves.append(3)   # Down
    if col > 0: moves.append(-1)  # Left
    if col < 2: moves.append(1)   # Right

    for move in moves:
        new_index = blank_index + move
        new_state = list(state)
        # Swap the blank with the target tile
        new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
        neighbors.append(tuple(new_state))
    return neighbors

def reconstruct_path(node):
    """Trace back from the goal node to the start to reconstruct the path."""
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

def a_star(initial, heuristic_func):
    start_time = time.time()
    open_list = []
    closed_set = set()

    h = heuristic_func(initial)
    root = Node(initial, None, 0, h)
    heapq.heappush(open_list, root)
    nodes_expanded = 0

    while open_list:
        current_node = heapq.heappop(open_list)
        nodes_expanded += 1

        if current_node.state == goal_state:
            end_time = time.time()
            return reconstruct_path(current_node), nodes_expanded, current_node.g, end_time - start_time

        closed_set.add(current_node.state)

        for neighbor in get_neighbors(current_node.state):
            if neighbor in closed_set:
                continue
            g = current_node.g + 1
            h = heuristic_func(neighbor)
            neighbor_node = Node(neighbor, current_node, g, h)
            heapq.heappush(open_list, neighbor_node)

    return None, nodes_expanded, 0, 0

def main():
    if len(sys.argv) != 11:
        print("Usage: python script.py <heuristicChoice> <tile1> <tile2> ... <tile9>")
        print("Example: python script.py 1 1 4 2 6 3 5 _ 7 8   (use '_' or '0' as the blank)")
        sys.exit(1)

    try:
        heuristic_choice = int(sys.argv[1])
        initial = []
        for val in sys.argv[2:]:
            if val == '_' or val == '0':
                initial.append(0)
            else:
                initial.append(int(val))
        if len(initial) != 9:
            raise ValueError
        initial = tuple(initial)
    except Exception as e:
        print("Invalid input. Ensure you provide 9 tiles with the blank as '_' or '0'.")
        sys.exit(1)

    if heuristic_choice == 1:
        heuristic_func = misplaced_tiles
    elif heuristic_choice == 2:
        heuristic_func = manhattan_distance
    else:
        print("Invalid heuristic choice. Use 1 for Misplaced Tiles, 2 for Manhattan Distance")
        sys.exit(1)

    path, nodes_expanded, depth, runtime = a_star(initial, heuristic_func)

    if path:
        print("Solution found!")
        print("Solution depth:", depth)
        print("Nodes expanded:", nodes_expanded)
        print("Runtime (seconds):", runtime)
        print("\nSolution path (each board state shown as 3 rows):\n")
        for state in path:
            for i in range(3):
                print(state[i*3:(i+1)*3])
            print("")
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
