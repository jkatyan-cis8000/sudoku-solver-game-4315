class SudokuBoard:
    """9x9 Sudoku board representation."""
    
    def __init__(self):
        """Initialize empty 9x9 grid."""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
    
    def initialize_board(self, initial_values=None):
        """Initialize board with provided values or empty.
        
        Args:
            initial_values: 9x9 list of integers or None for empty board
        """
        if initial_values:
            self.grid = [row[:] for row in initial_values]
        else:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
    
    def display(self):
        """Display the Sudoku grid in a formatted way."""
        print("-" * 21)
        for i, row in enumerate(self.grid):
            if i > 0 and i % 3 == 0:
                print("-" * 21)
            row_str = ""
            for j, cell in enumerate(row):
                if j > 0 and j % 3 == 0:
                    row_str += "| "
                cell_str = str(cell) if cell != 0 else "."
                row_str += cell_str + " "
            print(row_str)
        print("-" * 21)
    
    def get_cell(self, row, col):
        """Get value at specified cell.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
        
        Returns:
            Cell value (0-9)
        """
        return self.grid[row][col]
    
    def set_cell(self, row, col, value):
        """Set value at specified cell.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            value: Value to set (0-9)
        """
        self.grid[row][col] = value
    
    def is_valid_move(self, row, col, value):
        """Check if placing value at (row, col) is valid.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            value: Value to check (1-9)
        
        Returns:
            True if valid move
        """
        if value == 0:
            return True
        
        if self.grid[row][col] != 0:
            return False
        
        for i in range(9):
            if self.grid[row][i] == value:
                return False
            if self.grid[i][col] == value:
                return False
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == value:
                    return False
        
        return True
