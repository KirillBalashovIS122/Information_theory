def valid_moves(board, piece, start_pos):
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
    return linear_moves(board, piece, start_pos, [(1, 0), (-1, 0), (0, 1), (0, -1)])

def bishop_moves(board, piece, start_pos):
    return linear_moves(board, piece, start_pos, [(1, 1), (-1, -1), (1, -1), (-1, 1)])

def queen_moves(board, piece, start_pos):
    return linear_moves(board, piece, start_pos, [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)])

def king_moves(board, piece, start_pos):
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
    moves = []
    row, col = start_pos
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dr, dc in knight_moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == "--" or board[new_row][new_col][0] != piece[0]:
                moves.append((new_row, new_col))
    return moves

def linear_moves(board, piece, start_pos, directions):
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
