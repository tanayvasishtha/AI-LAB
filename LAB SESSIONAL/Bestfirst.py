#use best first search find the optimal path. Start node is A and end is J
from queue import PriorityQueue

graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 4), ('E', 2)],
    'C': [('F', 5), ('G', 6)],
    'D': [('H', 7)],
    'E': [('I', 8)],
    'F': [('J', 9)],
    'G': [('A', 2)],
    'H': [('I', 11)],
    'I': [('J',13)],
    'J': [('E',9)]
}

def best_first_search(start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start, [start]))  

    while not pq.empty():
        cost, current_node, path = pq.get()

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            return path

        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited:
                pq.put((weight, neighbor, path + [neighbor]))

    return None

optimal_path = best_first_search('A', 'J')

print("The optimal path from A to J is:", optimal_path)
