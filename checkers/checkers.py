from pydantic import BaseModel, Field
from enum import StrEnum


def init_board() -> list[list[Piece | None]]:
    board = []
    for i in range(8):
        row = []
        if i == 0 or i == 1:
            row = init_row(PieceEnum.WHITE)
        elif i == 6 or i == 7:
            row = init_row(PieceEnum.BLACK)
        else:
            row = init_row(None)
        board.append(row)
    return board


def init_row(piece_to_place: PieceEnum | None) -> list[Piece | None]:
    row = []
    for _ in range(8):
        if piece_to_place is None:
            row.append(piece_to_place)
        else:
            piece = Piece(color=piece_to_place)
            row.append(piece)
    return row


def check_winner(board) -> str | None:
    black_count = 0
    white_count = 0
    for row in board:
        for piece in row:
            if piece == Piece.BLACK_PIECE:
                black_count += 1
            elif piece == Piece.WHITE_PIECE:
                white_count += 1
    
    if black_count == 0:
        return "black"
    elif white_count == 0:
        return "white"
    return None


def attempt_move(board, player_color: PlayerColor, start: Coord, end: Coord) -> bool:
    start_piece: Piece = board[start.x][start.y]
    end_location: Piece | None = board[end.x][end.y]

    if start_piece is None:
        # Invalid move, piece location incorrect
        return False
    
    valid_moves = []
    if start_piece.king:
        # King valid moves
        pass
    else:
        # kill me, omega bounds checking
        if player_color == PlayerColor.WHITE:
            move_1 = board[start.x-1][start.y+1]
            move_2 = board[start.x+1][start.y+1]
            move_3 = board[start.x-2][start.y+2]
            move_4 = board[start.x+2][start.y+2]
        elif player_color == PlayerColor.BLACK:
            move_1 = board[start.x-1][start.y-1]
            move_2 = board[start.x+1][start.y-1]
        
        if move_1 is not None:
            valid_moves.append(move_1)
        if move_2 is not None:
            valid_moves.append(move_2)
    
    if len(valid_moves) == 0:
        # Invalid move, piece has no possible moves
        return False

class PlayerColor(StrEnum):
    WHITE = "white"
    BLACK = "black"

class PieceEnum(StrEnum):
    WHITE = "w"
    BLACK = "b"

class Player(BaseModel):
    color: PlayerColor

class Piece(BaseModel):
    color: PieceEnum
    king: bool = Field(default=False)

class Coord(BaseModel):
    x: int
    y: int

class Checkers(BaseModel):
    board: list[list[str | None]] = Field(frozen=True, default=init_board())
