import sys
from sudoku_game import SudokuGame


def display_menu():
    """Display the main game menu."""
    print("\n=== Sudoku Game ===")
    print("1. New Game")
    print("2. Difficulty Selection")
    print("3. Instructions")
    print("4. Exit")
    print("==================")


def display_difficulty_menu():
    """Display difficulty selection menu."""
    print("\n--- Select Difficulty ---")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Back")


def display_game_menu():
    """Display in-game menu."""
    print("\n--- Game Actions ---")
    print("Enter move as: row col value (e.g., '1 2 5')")
    print("Or use commands:")
    print("  hint    - Get a hint")
    print("  status  - Show game status")
    print("  board   - Redraw board")
    print("  quit    - Quit game")
    print("-------------------")


def get_move():
    """Get a move from the player.
    
    Returns:
        tuple (row, col, value) or None for invalid input
    """
    try:
        user_input = input("Enter move (row col value): ").strip()
        
        if user_input.lower() == 'quit':
            return 'quit'
        if user_input.lower() == 'hint':
            return 'hint'
        if user_input.lower() == 'status':
            return 'status'
        if user_input.lower() == 'board':
            return 'board'
        
        parts = user_input.split()
        if len(parts) != 3:
            print("Invalid format. Use: row col value")
            return None
        
        row, col, value = int(parts[0]), int(parts[1]), int(parts[2])
        
        if not (0 <= row <= 8 and 0 <= col <= 8 and 1 <= value <= 9):
            print("Invalid values. Row/col: 0-8, Value: 1-9")
            return None
        
        return (row, col, value)
    
    except ValueError:
        print("Invalid input. Use integers.")
        return None


def play_game(difficulty='medium'):
    """Play a single game.
    
    Args:
        difficulty: 'easy', 'medium', or 'hard'
    """
    game = SudokuGame(difficulty)
    print(f"\nStarting {difficulty} game!")
    
    while not game.is_game_over:
        print("\n" + "=" * 21)
        game.board.display()
        display_game_menu()
        
        status = game.get_status()
        print(f"Mistakes: {status['mistakes']}/{status['max_mistakes']}")
        print(f"Cells filled: {status['cells_filled']}/81")
        
        move = get_move()
        
        if move == 'quit':
            print("Thanks for playing!")
            return
        
        if move == 'hint':
            hint = game.get_hint()
            if hint:
                row, col, value = hint
                print(f"Hint: Place {value} at row {row}, col {col}")
            else:
                print("Board is full!")
        
        elif move == 'status':
            continue
        
        elif move == 'board':
            continue
        
        elif move:
            result = game.make_move(move[0], move[1], move[2])
            print(result['message'])
            
            if result['correct']:
                print("Great job!")
        
        if game.is_game_over:
            if game.is_won:
                print("\n🎉 Congratulations! You won! 🎉")
                game.board.display()
            else:
                print("\nGame over! Here's the solution:")
                for row in game.solution:
                    print(row)
        
        input("Press Enter to continue...")


def main():
    """Main entry point for the Sudoku game."""
    print("Welcome to Sudoku!")
    
    while True:
        display_menu()
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            play_game('medium')
        
        elif choice == '2':
            while True:
                display_difficulty_menu()
                diff_choice = input("Enter choice (1-4): ").strip()
                
                if diff_choice == '1':
                    play_game('easy')
                    break
                elif diff_choice == '2':
                    play_game('medium')
                    break
                elif diff_choice == '3':
                    play_game('hard')
                    break
                elif diff_choice == '4':
                    break
                else:
                    print("Invalid choice.")
        
        elif choice == '3':
            print("\n--- Instructions ---")
            print("1. Fill the 9x9 grid with digits 1-9")
            print("2. Each row must contain 1-9 without repeats")
            print("3. Each column must contain 1-9 without repeats")
            print("4. Each 3x3 box must contain 1-9 without repeats")
            print("5. You have 3 mistakes before game over")
            print("--------------------")
            input("Press Enter to continue...")
        
        elif choice == '4':
            print("Thanks for playing!")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
