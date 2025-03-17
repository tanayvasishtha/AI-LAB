import math
import time

class WaterJugsGame:
    def __init__(self, capacity_a, capacity_b, target):
        self.capacity_a = capacity_a
        self.capacity_b = capacity_b
        self.target = target
        
    def is_goal_state(self, state):
        """Check if either jug contains the target amount."""
        x, y = state
        return x == self.target or y == self.target
    
    def get_possible_moves(self, state):
        """Generate all possible next states from current state."""
        x, y = state
        moves = []
        
        # Fill jug A (only if not already full)
        if x < self.capacity_a:
            moves.append((self.capacity_a, y))
        
        # Fill jug B (only if not already full)
        if y < self.capacity_b:
            moves.append((x, self.capacity_b))
        
        # Empty jug A (only if not already empty)
        if x > 0:
            moves.append((0, y))
        
        # Empty jug B (only if not already empty)
        if y > 0:
            moves.append((x, 0))
        
        # Pour water from A to B (only if A has water and B is not full)
        if x > 0 and y < self.capacity_b:
            pour = min(x, self.capacity_b - y)
            # Only add if the pour actually changes the state
            if pour > 0:
                moves.append((x - pour, y + pour))
        
        # Pour water from B to A (only if B has water and A is not full)
        if y > 0 and x < self.capacity_a:
            pour = min(y, self.capacity_a - x)
            # Only add if the pour actually changes the state
            if pour > 0:
                moves.append((x + pour, y - pour))
        
        return moves
    
    def utility(self, state, is_maximizing_player):
        """Evaluate utility of a state."""
        if self.is_goal_state(state):
            return 10 if is_maximizing_player else -10
        
        # Distance-based heuristic for non-terminal states
        x, y = state
        distance_a = abs(x - self.target)
        distance_b = abs(y - self.target)
        min_distance = min(distance_a, distance_b)
        
        # Prefer states closer to the goal
        score = 5 - min_distance
        return score if is_maximizing_player else -score

def minimax(state, depth, is_maximizing_player, game):
    """Minimax algorithm implementation."""
    # Terminal conditions: goal state or maximum depth reached
    if game.is_goal_state(state) or depth == 0:
        return game.utility(state, is_maximizing_player)
    
    possible_moves = game.get_possible_moves(state)
    
    # If no valid moves are available, it's a draw
    if not possible_moves:
        return 0
    
    if is_maximizing_player:
        max_eval = float('-inf')
        for move in possible_moves:
            eval = minimax(move, depth - 1, False, game)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves:
            eval = minimax(move, depth - 1, True, game)
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move_minimax(state, depth, game):
    """Find the best move using the minimax algorithm."""
    best_move = None
    best_value = float('-inf')
    
    for move in game.get_possible_moves(state):
        move_value = minimax(move, depth - 1, False, game)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    
    return best_move, best_value

def alpha_beta_pruning(state, depth, alpha, beta, is_maximizing_player, game):
    """Minimax algorithm with alpha-beta pruning."""
    # Terminal conditions: goal state or maximum depth reached
    if game.is_goal_state(state) or depth == 0:
        return game.utility(state, is_maximizing_player)
    
    possible_moves = game.get_possible_moves(state)
    
    # If no valid moves are available, it's a draw
    if not possible_moves:
        return 0
    
    if is_maximizing_player:
        max_eval = float('-inf')
        for move in possible_moves:
            eval = alpha_beta_pruning(move, depth - 1, alpha, beta, False, game)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves:
            eval = alpha_beta_pruning(move, depth - 1, alpha, beta, True, game)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

def find_best_move_alpha_beta(state, depth, game):
    """Find the best move using the alpha-beta pruning algorithm."""
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for move in game.get_possible_moves(state):
        move_value = alpha_beta_pruning(move, depth - 1, alpha, beta, False, game)
        if move_value > best_value:
            best_value = move_value
            best_move = move
        alpha = max(alpha, best_value)
    
    return best_move, best_value

def compare_performance(game, initial_state, depth):
    """Compare the performance of minimax and alpha-beta pruning."""
    print("\n--- Performance Comparison ---")
    
    # Measure time for Minimax
    start_time = time.time()
    move, value = find_best_move_minimax(initial_state, depth, game)
    minimax_time = time.time() - start_time
    print(f"Minimax best move: {move} with value: {value}")
    print(f"Minimax execution time: {minimax_time:.6f} seconds")
    
    # Measure time for Alpha-Beta Pruning
    start_time = time.time()
    move, value = find_best_move_alpha_beta(initial_state, depth, game)
    alpha_beta_time = time.time() - start_time
    print(f"Alpha-Beta best move: {move} with value: {value}")
    print(f"Alpha-Beta execution time: {alpha_beta_time:.6f} seconds")
    
    # Calculate improvement ratio
    if minimax_time > 0:
        improvement = minimax_time / alpha_beta_time
        print(f"Alpha-Beta is {improvement:.2f}x faster than Minimax")
    
    return minimax_time, alpha_beta_time

def play_game(game, initial_state, use_alpha_beta=True, depth=5):
    """Play the Water Jugs game with human vs AI."""
    state = initial_state
    player_turn = False  # AI starts first
    
    print(f"\n--- Water Jugs Game (Capacities: {game.capacity_a}L, {game.capacity_b}L, Target: {game.target}L) ---")
    print("Players take turns making moves. First to achieve target volume wins.")
    
    while True:
        print(f"\nCurrent state: Jug A = {state[0]}L, Jug B = {state[1]}L")
        
        # Check for win condition
        if game.is_goal_state(state):
            winner = "Human" if player_turn else "AI"
            print(f"{winner} wins!")
            return winner
        
        possible_moves = game.get_possible_moves(state)
        
        # Check for draw condition
        if not possible_moves:
            print("No valid moves left. Game ends in a draw.")
            return "Draw"
        
        if player_turn:
            # Human player's turn
            print("\nYour turn (Human):")
            for i, move in enumerate(possible_moves):
                print(f"{i+1}: Pour to get (Jug A = {move[0]}L, Jug B = {move[1]}L)")
            
            try:
                choice = int(input("Enter your choice (number): ")) - 1
                if 0 <= choice < len(possible_moves):
                    state = possible_moves[choice]
                else:
                    print("Invalid choice. Try again.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
        else:
            # AI's turn
            print("\nAI is thinking...")
            
            start_time = time.time()
            if use_alpha_beta:
                best_move, value = find_best_move_alpha_beta(state, depth, game)
                algorithm = "Alpha-Beta Pruning"
            else:
                best_move, value = find_best_move_minimax(state, depth, game)
                algorithm = "Minimax"
            
            end_time = time.time()
            
            print(f"AI chooses: Jug A = {best_move[0]}L, Jug B = {best_move[1]}L")
            print(f"AI used {algorithm} (value: {value}, time: {end_time - start_time:.4f}s)")
            
            state = best_move
        
        # Switch turns
        player_turn = not player_turn

def display_rules():
    """Display the rules of the Water Jugs game."""
    print("\n--- Water Jugs Game Rules ---")
    print("1. Two players take turns making moves.")
    print("2. Each player can perform one of the following actions:")
    print("   - Fill either jug completely")
    print("   - Empty either jug completely")
    print("   - Pour water from one jug to another until one is empty or the other is full")
    print("3. The first player to achieve the target volume in either jug wins.")
    print("4. If no valid moves are left, the game ends in a draw.")

def main():
    """Main function to set up and run the Water Jugs game."""
    display_rules()
    
    # Get game parameters
    try:
        capacity_a = int(input("\nEnter capacity of jug A (in liters): "))
        capacity_b = int(input("Enter capacity of jug B (in liters): "))
        target = int(input("Enter target volume (in liters): "))
        
        if capacity_a <= 0 or capacity_b <= 0 or target <= 0:
            print("Capacities and target must be positive.")
            return
        
        if target > max(capacity_a, capacity_b):
            print("Target cannot be greater than the capacity of the largest jug.")
            return
        
        # Check if the target is achievable using the GCD
        import math
        gcd = math.gcd(capacity_a, capacity_b)
        if target % gcd != 0:
            print(f"Warning: Target volume {target}L may not be achievable with jugs of {capacity_a}L and {capacity_b}L.")
            print(f"Target must be a multiple of GCD({capacity_a}, {capacity_b}) = {gcd}")
    except ValueError:
        print("Please enter valid numbers.")
        return
    
    # Set up the game
    game = WaterJugsGame(capacity_a, capacity_b, target)
    initial_state = (0, 0)  # Both jugs start empty
    
    # Ask for search depth
    try:
        depth = int(input("Enter search depth for AI (3-7 recommended): "))
        if depth <= 0:
            print("Depth must be positive. Using default depth of 5.")
            depth = 5
    except ValueError:
        print("Using default depth of 5.")
        depth = 5
    
    # Compare algorithm performance
    compare_performance(game, initial_state, depth)
    
    # Ask if player wants to use Alpha-Beta pruning
    use_alpha_beta = input("Use Alpha-Beta pruning for AI? (y/n): ").lower() == 'y'
    
    # Play the game
    play_game(game, initial_state, use_alpha_beta, depth)
    
    # Ask if player wants to play again
    if input("\nPlay again? (y/n): ").lower() == 'y':
        main()

if __name__ == "__main__":
    main()
