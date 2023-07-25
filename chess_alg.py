import chess
import chess.svg
from colorama import init, Fore

def evaluate_board(board):
    """
    A simple evaluation function to determine the advantage of the board for the computer (black).
    """
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        if piece.color == chess.BLACK:
            evaluation += piece_value(piece)
        else:
            evaluation -= piece_value(piece)
    return evaluation

def piece_value(piece):
    """
    Assigns values to each chess piece for evaluation.
    """
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.KING:
        return 100
    return 0

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def computer_move(board, depth):
    """
    Generates the computer's move using the Minimax algorithm with alpha-beta pruning.
    """
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move


def print_colored_board(board):
    """
    Print the chessboard with moves made by White and Black with default colors.
    """
    pieces_mapping = {
        'P': '♙',
        'N': '♘',
        'B': '♗',
        'R': '♖',
        'Q': '♕',
        'K': '♔',
        'p': '♟',
        'n': '♞',
        'b': '♝',
        'r': '♜',
        'q': '♛',
        'k': '♚',
    }

    print("  a b c d e f g h")
    print("  ----------------")
    for row_num in range(8):
        print(f"{ row_num +1} ", end="")
        for col_num in range(8):
            square = chess.square(col_num, row_num)
            piece = board.piece_at(square)
            if piece is None:
                print('.', end=" ")
            else:
                piece_symbol = pieces_mapping[piece.symbol()]
                print(piece_symbol, end=" ")
        print(f"{row_num + 1}")
    print("  ----------------")
    print("  a b c d e f g h")


def main():
    board = chess.Board()
    player_turn = True
    depth = 3  # Adjust the depth for Minimax (higher depth takes more time but plays stronger)

    while not board.is_game_over():
        print_colored_board(board)
        print()
        if player_turn:
            move_str = input("Enter your move (e.g., e2e4): ")
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Invalid move format. Try again.")
                continue
        else:
            move = computer_move(board, depth)
            if move is None:
                print("Computer can't move. You win!")
                break
            board.push(move)

        player_turn = not player_turn

    print("Game Over!")
    print("Result: ", board.result())

if __name__ == "__main__":
    main()
