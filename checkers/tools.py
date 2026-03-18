from hashlib import blake2b


def hash_board(board) -> str:
    board_str = ""
    for row in board:
        for piece in row:
            if piece is None:
                board_str += "-"
            else:
                board_str += str(piece)
    return blake2b(board_str.encode()).hexdigest()
