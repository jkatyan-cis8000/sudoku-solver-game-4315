import random
from sudoku_board import SudokuBoard


class PuzzleGenerator:
    """Generate valid Sudoku puzzles with configurable difficulty."""
    
    EASY_CLUES = 40
    MEDIUM_CLUES = 30
    HARD_CLUES = 20
    
    def __init__(self):
        """Initialize the puzzle generator."""
        self.board = SudokuBoard()
    
    def generate_puzzle(self, difficulty='medium'):
        """Generate a new Sudoku puzzle.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        
        Returns:
            9x9 list representing the puzzle with clues
        """
        clues_count = {
            'easy': self.EASY_CLUES,
            'medium': self.MEDIUM_CLUES,
            'hard': self.HARD_CLUES
        }.get(difficulty, self.MEDIUM_CLUES)
        
        full_solution = self._generate_full_solution()
        
        puzzle = [row[:] for row in full_solution]
        
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        cells_to_remove = 81 - clues_count
        for r, c in cells[:cells_to_remove]:
            puzzle[r][c] = 0
        
        return puzzle
    
    def _generate_full_solution(self):
        """Generate a complete valid Sudoku solution.
        
        Returns:
            9x9 list with a valid complete Sudoku grid
        """
        self.board.initialize_board()
        self._solve_backtracking(self.board)
        return [row[:] for row in self.board.grid]
    
    def _solve_backtracking(self, board):
        """Solve Sudoku using backtracking algorithm.
        
        Args:
            board: SudokuBoard instance to solve
        
        Returns:
            True if solved successfully
        """
        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    
                    for num in numbers:
                        if board.is_valid_move(row, col, num):
                            board.set_cell(row, col, num)
                            
                            if self._solve_backtracking(board):
                                return True
                            
                            board.set_cell(row, col, 0)
                    
                    return False
        
        return True
    
    def count_solutions(self, board_grid):
        """Count number of solutions for a partial board.
        
        Args:
            board_grid: 9x9 list of integers
        
        Returns:
            Number of possible solutions (capped at 2 for efficiency)
        """
        count = [0]
        board_copy = [row[:] for row in board_grid]
        self._count_solutions_helper(board_copy, count, 2)
        return count[0]
    
    def _count_solutions_helper(self, board_grid, count, limit):
        """Helper for counting solutions.
        
        Args:
            board_grid: 9x9 list of integers
            count: List with single int (mutable counter)
            limit: Maximum solutions to count
        """
        if count[0] >= limit:
            return
        
        for row in range(9):
            for col in range(9):
                if board_grid[row][col] == 0:
                    for num in range(1, 10):
                        if self._is_valid_for_count(board_grid, row, col, num):
                            board_grid[row][col] = num
                            self._count_solutions_helper(board_grid, count, limit)
                            board_grid[row][col] = 0
                    return
        
        count[0] += 1
    
    def _is_valid_for_count(self, board_grid, row, col, num):
        """Check validity without using SudokuBoard methods.
        
        Args:
            board_grid: 9x9 list of integers
            row: Row index
            col: Column index
            num: Number to check
        
        Returns:
            True if valid placement
        """
        if board_grid[row][col] != 0:
            return False
        
        for i in range(9):
            if board_grid[row][i] == num:
                return False
            if board_grid[i][col] == num:
                return False
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board_grid[i][j] == num:
                    return False
        
        return True
