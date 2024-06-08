"""
Этот код реализует логику ходов фигур в шахматах, включая проверку шаха и мата.
"""
def valid_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для данной фигуры.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- фигура, для которой ищутся ходы.
    start_pos -- начальная позиция фигуры.

    Возвращает:
    Список допустимых ходов для фигуры.
    """
    piece_type = piece[1]
    if piece_type == 'P':
        return pawn_moves(board, piece, start_pos)
    elif piece_type == 'R':
        return rook_moves(board, piece, start_pos)
    elif piece_type == 'N':
        return knight_moves(board, piece, start_pos)
    elif piece_type == 'B':
        return bishop_moves(board, piece, start_pos)
    elif piece_type == 'Q':
        return queen_moves(board, piece, start_pos)
    elif piece_type == 'K':
        return king_moves(board, piece, start_pos)
    return []

def pawn_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для пешки.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- пешка, для которой ищутся ходы.
    start_pos -- начальная позиция пешки.

    Возвращает:
    Список допустимых ходов для пешки.
    """
    moves = []
    row, col = start_pos
    direction = -1 if piece[0] == 'w' else 1
    if board[row + direction][col] == "--":
        moves.append((row + direction, col))
        if (piece[0] == 'w' and row == 6) or (piece[0] == 'b' and row == 1):
            if board[row + 2 * direction][col] == "--":
                moves.append((row + 2 * direction, col))
    if col > 0 and board[row + direction][col - 1] != "--" and board[row + direction][col - 1][0] != piece[0]:
        moves.append((row + direction, col - 1))
    if col < 7 and board[row + direction][col + 1] != "--" and board[row + direction][col + 1][0] != piece[0]:
        moves.append((row + direction, col + 1))
    return moves

def rook_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для ладьи.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- ладья, для которой ищутся ходы.
    start_pos -- начальная позиция ладьи.

    Возвращает:
    Список допустимых ходов для ладьи.
    """
    return linear_moves(board, piece, start_pos, [(1, 0), (-1, 0), (0, 1), (0, -1)])

def bishop_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для слона.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- слон, для которого ищутся ходы.
    start_pos -- начальная позиция слона.

    Возвращает:
    Список допустимых ходов для слона.
    """
    return linear_moves(board, piece, start_pos, [(1, 1), (-1, -1), (1, -1), (-1, 1)])

def queen_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для ферзя.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- ферзь, для которого ищутся ходы.
    start_pos -- начальная позиция ферзя.

    Возвращает:
    Список допустимых ходов для ферзя.
    """
    return linear_moves(
        board, piece, start_pos,
        [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    )

def king_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для короля.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- король, для которого ищутся ходы.
    start_pos -- начальная позиция короля.

    Возвращает:
    Список допустимых ходов для короля.
    """
    moves = []
    row, col = start_pos
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == "--" or board[new_row][new_col][0] != piece[0]:
                moves.append((new_row, new_col))
    return moves

def knight_moves(board, piece, start_pos):
    """
    Возвращает все допустимые ходы для коня.

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- конь, для которого ищутся ходы.
    start_pos -- начальная позиция коня.

    Возвращает:
    Список допустимых ходов для коня.
    """
    moves = []
    row, col = start_pos
    knight_moves_directions = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                               (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dr, dc in knight_moves_directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == "--" or board[new_row][new_col][0] != piece[0]:
                moves.append((new_row, new_col))
    return moves

def linear_moves(board, piece, start_pos, directions):
    """
    Возвращает все допустимые ходы для фигур, 
    которые ходят по прямым или диагональным линиям (ладья, слон, ферзь).

    Аргументы:
    board -- текущее состояние шахматной доски.
    piece -- фигура, для которой ищутся ходы.
    start_pos -- начальная позиция фигуры.
    directions -- список направлений, в которых может ходить фигура.

    Возвращает:
    Список допустимых ходов для фигуры.
    """
    moves = []
    row, col = start_pos
    for dr, dc in directions:
        for i in range(1, 8):
            new_row, new_col = row + dr * i, col + dc * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == "--":
                    moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece[0]:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
            else:
                break
    return moves

def is_in_check(board, color):
    """
    Проверяет, находится ли король под шахом.

    Аргументы:
    board -- текущее состояние шахматной доски.
    color -- цвет короля, который проверяется на шах.

    Возвращает:
    True, если король под шахом, иначе False.
    """
    king_pos = find_king(board, color)
    opponent_color = 'b' if color == 'w' else 'w'
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--" and piece[0] == opponent_color:
                if king_pos in valid_moves(board, piece, (row, col)):
                    return True
    return False

def find_king(board, color):
    """
    Находит позицию короля на доске.

    Аргументы:
    board -- текущее состояние шахматной доски.
    color -- цвет короля, который ищется.

    Возвращает:
    Позицию короля в виде кортежа (row, col).
    """
    for row in range(8):
        for col in range(8):
            if board[row][col] == color + 'K':
                return (row, col)
    return None

def is_checkmate(board, color):
    """
    Проверяет, находится ли король под шахом и не может ли он избежать мата.

    Аргументы:
    board -- текущее состояние шахматной доски.
    color -- цвет короля, который проверяется на мат.

    Возвращает:
    True, если король под матом, иначе False.
    """
    if not is_in_check(board, color):
        return False
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--" and piece[0] == color:
                for move in valid_moves(board, piece, (row, col)):
                    temp_board = [r[:] for r in board]
                    temp_board[move[0]][move[1]] = piece
                    temp_board[row][col] = "--"
                    if not is_in_check(temp_board, color):
                        return False
    return True
