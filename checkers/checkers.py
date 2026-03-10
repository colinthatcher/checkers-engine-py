import logging
from structs import *


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


def check_winner(board) -> str | None:
    black_count = 0
    white_count = 0
    for row in board:
        for piece in row:
            if piece is None:
                continue
            if piece.color == PieceEnum.BLACK:
                black_count += 1
            elif piece.color == PieceEnum.WHITE:
                white_count += 1

    # Not a race condition™
    if black_count == 0:
        return PlayerColor.WHITE
    elif white_count == 0:
        return PlayerColor.BLACK

    # TODO: Check for stalemate position where one player has blocked any valid moves from the other

    return None


def check_draw(board, move_history) -> bool:
    # TODO: determine if a draw condition has occured according to the rules
    pass


def auto_king(piece: Piece, player_color: PlayerColor, end: Coord):
    if player_color == PlayerColor.BLACK and end.y == 0:
        piece.king = True
    elif player_color == PlayerColor.WHITE and end.y == 7:
        piece.king = True


# TODO: We will need to check an array of moves, dunno if we want that in here or in a wrapper method
def attempt_move(
    board, player_color: PlayerColor, move: MoveType, start: Coord, end: Coord
) -> bool:
    if start == None or end == None:
        print("start or end coord is empty")
        return False

    if (
        start.x < 0
        or start.y < 0
        or end.x < 0
        or end.y < 0
        or start.x > 7
        or start.y > 7
        or end.x > 7
        or end.y > 7
    ):
        # Bounds checking xd
        print("coordinates are out of bounds")
        return False

    if start.x == end.x and start.y == end.y:
        # Same location dummy
        print("start and end are the same")
        return False

    start_piece: Piece = board[start.y][start.x]
    end_location: None = board[end.y][end.x]

    if start_piece is None:
        # Invalid move, piece location incorrect
        print("start piece coord is empty")
        return False

    if (
        start_piece.color is start_piece.color.WHITE
        and player_color is not player_color.WHITE
    ) or (
        start_piece.color is start_piece.color.BLACK
        and player_color is not player_color.BLACK
    ):
        print("start piece does not belong to the player")
        return False

    if end_location is not None:
        # Invalid move, must be empty to move here
        print("end location is not empty")
        return False

    dist_x = end.x - start.x
    dist_y = end.y - start.y
    if abs(dist_x) > 2 or abs(dist_y) > 2:
        # Invalid move, no valid move can cross a distance of more than two squares
        print("distance is too large")
        return False
    elif dist_x == 0 or dist_y == 0:
        # if either distance is zero the direction of the move wasn't diagonal
        print("distance is zero on one axis")
        return False

    if not start_piece.king:
        # make sure player color is moving the correct direction, only the y distance
        # indicates if the piece is moving the correct direction.
        if player_color == PlayerColor.BLACK:
            if dist_y > 0:
                print("wrong direction for a black piece")
                return False
        elif player_color == PlayerColor.WHITE:
            if dist_y < 0:
                print("wrong direction for a white piece")
                return False

    match move:
        case MoveType.MOVE:
            # ensure the destination is only one square away
            if abs(dist_x) != 1 or abs(dist_y) != 1:
                print("distance too large for a move")
                return False

            # valid move
            auto_king(start_piece, player_color, end)
            board[end.y][end.x] = start_piece
            board[start.y][start.x] = None
            return True
        case MoveType.CAPTURE:
            print(dist_x, dist_y)
            if abs(dist_x) != 2 or abs(dist_y) != 2:
                print("too short/long of a capture")
                return False
            captured_piece_coords = Coord(
                x=start.x + (dist_x // 2), y=start.y + (dist_y // 2)
            )
            captured_piece: Piece = board[captured_piece_coords.y][
                captured_piece_coords.x
            ]
            if captured_piece == None:
                print("no piece to capture")
                return False
            if (
                captured_piece.color == PieceEnum.WHITE
                and start_piece.color == PieceEnum.WHITE
            ):
                print("white can't capture white")
                return False
            elif (
                captured_piece.color == PieceEnum.BLACK
                and start_piece.color == PieceEnum.BLACK
            ):
                print("black can't capture black")
                return False

            # valid move
            auto_king(start_piece, player_color, end)
            board[captured_piece_coords.y][captured_piece_coords.x] = None
            board[end.y][end.x] = start_piece
            board[start.y][start.x] = None
            return True
        case _:
            print("move type invalid")
            return False

    print("unmitigated disaster")
    return False


class Checkers(BaseModel):
    board: list[list[str | None]] = Field(frozen=True, default=init_board())
