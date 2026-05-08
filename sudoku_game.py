from sudoku_board import SudokuBoard
from puzzle_generator import PuzzleGenerator


class SudokuGame:
    """Manage Sudoku game state, validation, and win detection."""
    
    def __init__(self, difficulty='medium'):
        """Initialize the Sudoku game.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.difficulty = difficulty
        self.board = SudokuBoard()
        self.solution = []
        self.initial_board = []
        self.mistakes = 0
        self.max_mistakes = 3
        self.moves = []
        self.is_game_over = False
        self.is_won = False
        
        self._start_new_game()
    
    def _start_new_game(self):
        """Start a new game with a generated puzzle."""
        generator = PuzzleGenerator()
        puzzle = generator.generate_puzzle(self.difficulty)
        
        self.solution = self._solve_puzzle(puzzle)
        self.board.initialize_board(puzzle)
        self.initial_board = [row[:] for row in puzzle]
        self.mistakes = 0
        self.moves = []
        self.is_game_over = False
        self.is_won = False
    
    def _solve_puzzle(self, puzzle_grid):
        """Solve the puzzle to get the solution.
        
        Args:
            puzzle_grid: 9x9 list of integers
        
        Returns:
            9x9 list with the solved grid
        """
        board = SudokuBoard()
        board.initialize_board(puzzle_grid)
        self._solve_backtracking(board)
        return board.grid
    
    def _solve_backtracking(self, board):
        """Solve using backtracking.
        
        Args:
            board: SudokuBoard to solve
        
        Returns:
            True if solved
        """
        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    for num in range(1, 10):
                        if board.is_valid_move(row, col, num):
                            board.set_cell(row, col, num)
                            if self._solve_backtracking(board):
                                return True
                            board.set_cell(row, col, 0)
                    return False
        return True
    
    def make_move(self, row, col, value):
        """Process a player's move.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            value: Value to place (1-9)
        
        Returns:
            dict with 'valid', 'correct', 'mistakes', 'message' keys
        """
        if self.is_game_over:
            return {
                'valid': False,
                'correct': False,
                'mistakes': self.mistakes,
                'message': 'Game is over'
            }
        
        if not (0 <= row < 9 and 0 <= col < 9):
            return {
                'valid': False,
                'correct': False,
                'mistakes': self.mistakes,
                'message': 'Invalid position'
            }
        
        if value < 1 or value > 9:
            return {
                'valid': False,
                'correct': False,
                'mistakes': self.mistakes,
                'message': 'Invalid value'
            }
        
        if self.initial_board[row][col] != 0:
            return {
                'valid': False,
                'correct': False,
                'mistakes': self.mistakes,
                'message': 'Cannot modify initial cell'
            }
        
        is_correct = value == self.solution[row][col]
        
        if is_correct:
            self.board.set_cell(row, col, value)
            self.moves.append((row, col, value, True))
            self._check_win_condition()
            return {
                'valid': True,
                'correct': True,
                'mistakes': self.mistakes,
                'message': 'Correct move!'
            }
        else:
            self.mistakes += 1
            self.moves.append((row, col, value, False))
            
            if self.mistakes >= self.max_mistakes:
                self.is_game_over = True
                self.is_won = False
                return {
                    'valid': True,
                    'correct': False,
                    'mistakes': self.mistakes,
                    'message': f'Max mistakes reached! Game over. Correct value was {self.solution[row][col]}'
                }
            
            return {
                'valid': True,
                'correct': False,
                'mistakes': self.mistakes,
                'message': f'Incorrect! Mistake {self.mistakes}/{self.max_mistakes}'
            }
    
    def _check_win_condition(self):
        """Check if the player has won."""
        for row in range(9):
            for col in range(9):
                if self.board.grid[row][col] != self.solution[row][col]:
                    return
        
        self.is_game_over = True
        self.is_won = True
    
    def get_hint(self):
        """Get a hint for an empty cell.
        
        Returns:
            (row, col, value) tuple or None if no empty cells
        """
        for row in range(9):
            for col in range(9):
                if self.board.grid[row][col] == 0:
                    return (row, col, self.solution[row][col])
        return None
    
    def check_cell(self, row, col):
        """Check if a cell is correctly filled.
        
        Args:
            row: Row index
            col: Column index
        
        Returns:
            True if correct, False otherwise
        """
        return self.board.grid[row][col] == self.solution[row][col]
    
    def get_status(self):
        """Get current game status.
        
        Returns:
            dict with game state information
        """
        cells_filled = sum(1 for r in range(9) for c in range(9) 
                          if self.board.grid[r][c] != 0)
        cells_remaining = 81 - cells_filled
        
        return {
            'mistakes': self.mistakes,
            'max_mistakes': self.max_mistakes,
            'moves': len(self.moves),
            'cells_filled': cells_filled,
            'cells_remaining': cells_remaining,
            'is_game_over': self.is_game_over,
            'is_won': self.is_won
        }
