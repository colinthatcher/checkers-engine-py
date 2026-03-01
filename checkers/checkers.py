import math
from pydantic import BaseModel, Field, model_serializer
from enum import StrEnum


def print_board(board):
    print()
    for row in board:
        row_str = ""
        for square in row:
            if square is not None:
                row_str += f" {square.color} "
            else:
                row_str += " - "
        print(row_str)


def init_board() -> list[list[Piece | None]]:
    board = []
    for y in range(8):
        row = []
        for x in range(8):
            # alternate placement of pieces on dark squares
            if y % 2 == 0 and x % 2 == 1:
                if y == 0 or y == 1 or y == 2:
                    row.append(Piece(color=PieceEnum.WHITE))
                elif y == 5 or y == 6 or y == 7:
                    row.append(Piece(color=PieceEnum.BLACK))
                else:
                    row.append(None)
            elif y % 2 == 1 and x % 2 == 0:
                if y == 0 or y == 1 or y == 2:
                    row.append(Piece(color=PieceEnum.WHITE))
                elif y == 5 or y == 6 or y == 7:
                    row.append(Piece(color=PieceEnum.BLACK))
                else:
                    row.append(None)
            else:
                row.append(None)

        board.append(row)
    return board


# TOTALLY UNTESTED
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


def attempt_move(board, player_color: PlayerColor, move: MoveType, start: Coord, end: Coord) -> bool:
    if start == None or end == None:
        return False

    if start.x < 0 or start.y < 0 or end.x < 0 or end.y < 0 or \
       start.x > 7 or start.y > 7 or end.x > 7 or end.y > 7:
        # Bounds checking xd
        return False

    if start.x == end.x and start.y == end.y:
        # Same location dummy
        return False

    start_piece: Piece = board[start.y][start.x]
    end_location: None = board[end.y][end.x]

    if start_piece is None:
        # Invalid move, piece location incorrect
        return False

    if end_location is not None:
        # Invalid move, must be empty to move here
        return False
    
    # valid_moves = []
    # if start_piece.king:
    #     # King valid moves
    #     pass

    dist_x = end.x - start.x
    dist_y = end.y - start.y
    if abs(dist_x) > 1 or abs(dist_y) > 1:
        # Invalid move, no valid move can cross a distance of more than two squares
        return False
    elif dist_x == 0 or dist_y == 0:
        # if either distance is zero the direction of the move wasn't diagonal
        return False

    if not start_piece.king:
        # make sure player color is moving the correct direction
        if player_color == PlayerColor.BLACK:
            if dist_x > 0 and dist_y > 0:
                return False
        elif player_color == PlayerColor.WHITE:
            if dist_x < 0 and dist_y < 0:
                return False
    
    match move:
        case MoveType.MOVE:
            pass
        case MoveType.CAPTURE:
            pass
        case MoveType.KING_ME:
            pass
        case _:
            return False

    return True


class PlayerColor(StrEnum):
    WHITE = "white"
    BLACK = "black"

class PieceEnum(StrEnum):
    WHITE = "w"
    BLACK = "b"
    
class MoveType(StrEnum):
    KING_ME = "K"
    CAPTURE = "c"
    MOVE    = "m"

class Player(BaseModel):
    color: PlayerColor

class Piece(BaseModel):
    color: PieceEnum
    king: bool = Field(default=False)

    @model_serializer
    def serialize(self):
        return self.color

class Coord(BaseModel):
    x: int
    y: int

class Checkers(BaseModel):
    board: list[list[str | None]] = Field(frozen=True, default=init_board())























        # if player_color == PlayerColor.WHITE:
        #     move_1 = board[start.x-1][start.y+1]
        #     move_2 = board[start.x+1][start.y+1]
        #     move_3 = board[start.x-2][start.y+2]
        #     move_4 = board[start.x+2][start.y+2]
        # elif player_color == PlayerColor.BLACK:
        #     move_1 = board[start.x-1][start.y-1]
        #     move_2 = board[start.x+1][start.y-1]
        #     move_3 = board[start.x-2][start.y-2]
        #     move_4 = board[start.x+2][start.y-2]
        
        # if move_1 is not None:
        #     valid_moves.append(move_1)
        # if move_2 is not None:
        #     valid_moves.append(move_2)
    
    # if len(valid_moves) == 0:
    #     # Invalid move, piece has no possible moves
    #     return False