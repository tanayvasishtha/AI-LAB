import numpy as np
import time

class FourQueensGame:
    def __init__(self):
        # Initialize 4x4 board with zeros (empty cells)
        self.board = np.zeros((4, 4), dtype=int)
        self.current_player = 1  # Player 1 starts (AI), Player 2 is human
    
    def print_board(self):
        """Display the current state of the board"""
        symbols = {0: '.', 1: 'A', 2: 'H'}  # 0: empty, 1: AI queen, 2: Human queen
        print("\nCurrent Board:")
        print("  0 1 2 3")
        for i in range(4):
            row = f"{i} "
            for j in range(4):
                row += symbols[self.board[i][j]] + " "
            print(row)
        print()
    
    def is_valid_move(self, row, col):
        """Check if placing a queen at (row, col) is valid"""
        # Check if cell is already occupied
        if self.board[row][col] != 0:
            return False
        
        # Check row
        for c in range(4):
            if self.board[row][c] != 0:
                return False
        
        # Check column
        for r in range(4):
            if self.board[r][col] != 0:
                return False
        
        # Check diagonals
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != 0:
                    # Check if (i,j) and (row,col) are on the same diagonal
                    if abs(i - row) == abs(j - col):
                        return False
        
        return True
    
    def get_valid_moves(self):
        """Return list of all valid moves as (row, col) tuples"""
        valid_moves = []
        for i in range(4):
            for j in range(4):
                if self.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves
    
    def make_move(self, row, col, player=None):
        """Place a queen at (row, col) for the specified player"""
        if player is None:
            player = self.current_player
        
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def undo_move(self, row, col):
        """Remove a queen from (row, col)"""
        self.board[row][col] = 0
    
    def is_game_over(self):
        """Check if the game is over (no valid moves left)"""
        return len(self.get_valid_moves()) == 0
    
    def count_queens(self):
        """Count the number of queens placed by each player"""
        ai_queens = np.sum(self.board == 1)
        human_queens = np.sum(self.board == 2)
        return ai_queens, human_queens
    
    def utility(self):
        """
        Evaluate the board state
        Positive score favors AI, negative favors human
        """
        if self.is_game_over():
            ai_queens, human_queens = self.count_queens()
            
            # If all 4 queens are placed, it's a win for both (draw)
            if ai_queens + human_queens == 4:
                return 0
            
            # If current player can't move, they lose
            if self.current_player == 1:  # AI's turn but can't move
                return -100  # AI loses
            else:  # Human's turn but can't move
                return 100  # AI wins
        
        # For non-terminal states, evaluate based on placement options
        valid_moves = len(self.get_valid_moves())
        ai_queens, human_queens = self.count_queens()
        
        # Prefer states where AI has placed more queens
        return 10 * (ai_queens - human_queens) + valid_moves
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning
        Returns (best_score, best_move)
        """
        if depth == 0 or self.is_game_over():
            return self.utility(), None
        
        valid_moves = self.get_valid_moves()
        
        if maximizing_player:  # AI's turn (player 1)
            best_score = float('-inf')
            best_move = None
            
            for move in valid_moves:
                row, col = move
                self.make_move(row, col, 1)
                self.current_player = 2  # Switch to human
                
                score, _ = self.minimax(depth - 1, alpha, beta, False)
                
                self.undo_move(row, col)
                self.current_player = 1  # Switch back to AI
                
                if score > best_score:
                    best_score = score
                    best_move = move
                
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return best_score, best_move
        
        else:  # Human's turn (player 2)
            best_score = float('inf')
            best_move = None
            
            for move in valid_moves:
                row, col = move
                self.make_move(row, col, 2)
                self.current_player = 1  # Switch to AI
                
                score, _ = self.minimax(depth - 1, alpha, beta, True)
                
                self.undo_move(row, col)
                self.current_player = 2  # Switch back to human
                
                if score < best_score:
                    best_score = score
                    best_move = move
                
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return best_score, best_move
    
    def ai_move(self):
        """Make the best move for the AI using minimax with alpha-beta pruning"""
        start_time = time.time()
        
        # Use minimax with alpha-beta pruning (depth 5 should be sufficient for 4x4)
        _, best_move = self.minimax(5, float('-inf'), float('inf'), True)
        
        end_time = time.time()
        print(f"AI thinking time: {end_time - start_time:.4f} seconds")
        
        if best_move:
            row, col = best_move
            self.make_move(row, col, 1)
            print(f"AI places a queen at position ({row}, {col})")
            self.current_player = 2  # Switch to human
            return True
        return False
    
    def human_move(self):
        """Get and process human player's move"""
        self.print_board()
        valid_moves = self.get_valid_moves()
        
        if not valid_moves:
            return False
        
        print("Valid moves:", [(r, c) for r, c in valid_moves])
        
        while True:
            try:
                row = int(input("Enter row (0-3): "))
                col = int(input("Enter column (0-3): "))
                
                if 0 <= row < 4 and 0 <= col < 4:
                    if self.make_move(row, col, 2):
                        self.current_player = 1  # Switch to AI
                        return True
                    else:
                        print("Invalid move. This position is under attack or occupied.")
                else:
                    print("Invalid input. Row and column must be between 0 and 3.")
            except ValueError:
                print("Invalid input. Please enter numbers.")
    
    def play_game(self):
        """Main game loop"""
        print("Welcome to the 4-Queens Game!")
        print("You are playing against an AI that uses Minimax with Alpha-Beta pruning.")
        print("The goal is to place queens such that no two queens threaten each other.")
        print("The player unable to make a valid move loses the game.")
        
        # Decide who goes first
        first = input("Do you want to go first? (y/n): ").lower()
        if first == 'y':
            self.current_player = 2  # Human starts
        else:
            self.current_player = 1  # AI starts
        
        # Game loop
        while True:
            if self.current_player == 1:  # AI's turn
                print("\nAI's turn...")
                if not self.ai_move():
                    print("AI can't make a valid move. You win!")
                    break
            else:  # Human's turn
                print("\nYour turn...")
                if not self.human_move():
                    print("You can't make a valid move. AI wins!")
                    break
            
            # Check if all 4 queens are placed
            ai_queens, human_queens = self.count_queens()
            if ai_queens + human_queens == 4:
                print("\nAll 4 queens have been placed successfully!")
                print("It's a draw - both players win!")
                break
        
        # Final board state
        self.print_board()
        print("Game Over!")

# Run the game
if __name__ == "__main__":
    game = FourQueensGame()
    game.play_game()
