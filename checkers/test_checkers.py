from checkers import (
    init_board,
    Coord,
    Piece,
    PieceEnum,
    print_board,
    attempt_move,
    PlayerColor,
    MoveType,
)


def helper_empty_board() -> list[list[None]]:
    board = []
    for y in range(8):
        row = []
        for x in range(8):
            row.append(None)
        board.append(row)
    return board


def helper_setup_board(
    board: list[list[None]], pieces: list[tuple[Coord, Piece]]
) -> list[list[Piece | None]]:
    for piece in pieces:
        board[piece[0].y][piece[0].x] = piece[1]
    return board


def test_attempt_move_none_coord():
    # create board
    board = helper_empty_board()
    valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, None, None)
    assert not valid_move


def test_attempt_move_bounds_checks():
    # create board
    board = helper_empty_board()
    coord = Coord(x=0, y=0)
    invalid_moves = [
        Coord(x=-1, y=0),
        Coord(x=8, y=0),
        Coord(x=0, y=-1),
        Coord(x=0, y=8),
    ]
    # check start coordinate bounds
    for move in invalid_moves:
        valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, move, coord)
        # validate output
        assert not valid_move
    # check end coordinate bounds
    for move in invalid_moves:
        valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, move, coord)
        # validate output
        assert not valid_move


def test_attempt_move_duplicated_coord():
    board = helper_empty_board()
    coord = Coord(x=0, y=0)
    valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, coord, coord)
    assert not valid_move


def test_attempt_move_start_piece_is_none():
    board = helper_empty_board()
    start = Coord(x=0, y=0)
    end = Coord(x=1, y=1)
    valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, start, end)
    assert not valid_move


def test_attempt_move_end_location_is_not_none():
    pieces = [
        (Coord(x=0, y=0), Piece(color=PieceEnum.WHITE)),
        (Coord(x=1, y=1), Piece(color=PieceEnum.WHITE)),
    ]
    board = helper_setup_board(helper_empty_board(), pieces)
    start = Coord(x=0, y=0)
    end = Coord(x=1, y=1)
    valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, start, end)
    assert not valid_move


def test_attempt_move_distance_too_great():
    pieces = [
        (Coord(x=4, y=4), Piece(color=PieceEnum.WHITE)),
    ]
    board = helper_setup_board(helper_empty_board(), pieces)
    start = Coord(x=4, y=4)
    invalid_end_coords = [
        Coord(x=0, y=0),
        Coord(x=7, y=7),
        Coord(x=0, y=7),
        Coord(x=7, y=0),
        Coord(x=6, y=6),
        Coord(x=2, y=2),
    ]
    for coord in invalid_end_coords:
        valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, start, coord)
        assert not valid_move


def test_attempt_move_not_diagonal():
    pieces = [
        (Coord(x=0, y=0), Piece(color=PieceEnum.WHITE)),
    ]
    board = helper_setup_board(helper_empty_board(), pieces)
    start = Coord(x=0, y=0)
    invalid_end_coords = [
        Coord(x=0, y=1),
        Coord(x=1, y=0),
        Coord(x=0, y=2),
        Coord(x=2, y=0),
    ]
    for coord in invalid_end_coords:
        valid_move = attempt_move(board, PlayerColor.WHITE, MoveType.MOVE, start, coord)
        assert not valid_move


def test_attempt_move_incorrect_direction():
    black_piece = (Coord(x=3, y=2), Piece(color=PieceEnum.BLACK))
    white_piece = (Coord(x=2, y=5), Piece(color=PieceEnum.WHITE))
    board = helper_setup_board(helper_empty_board(), [black_piece, white_piece])
    moves = [
        (PlayerColor.BLACK, black_piece[0], Coord(x=4, y=3)),
        (PlayerColor.WHITE, white_piece[0], Coord(x=1, y=4)),
    ]
    for move in moves:
        valid_move = attempt_move(
            board, move[0], MoveType.MOVE, move[1], move[2]
        )
        assert not valid_move


def test_attempt_move_successful_move():
    white_piece = (Coord(x=3, y=2), Piece(color=PieceEnum.WHITE))
    black_piece = (Coord(x=2, y=5), Piece(color=PieceEnum.BLACK))
    board = helper_setup_board(helper_empty_board(), [white_piece, black_piece])
    moves = [
        (PlayerColor.WHITE, white_piece[0], Coord(x=4, y=3)),
        (PlayerColor.BLACK, black_piece[0], Coord(x=1, y=4)),
    ]
    for move in moves:
        valid_move = attempt_move(
            board, move[0], MoveType.MOVE, move[1], move[2]
        )
        assert valid_move


def test_attempt_move_successful_capture():
    white_piece = (Coord(x=1, y=2), Piece(color=PieceEnum.WHITE))
    black_piece = (Coord(x=2, y=3), Piece(color=PieceEnum.BLACK))
    board = helper_setup_board(helper_empty_board(), [white_piece, black_piece])
    moves = [
        (PlayerColor.WHITE, MoveType.CAPTURE, white_piece[0], Coord(x=3, y=4)),
    ]
    for move in moves:
        valid_move = attempt_move(
            board, move[0], move[1], move[2], move[3]
        )
        assert valid_move


def test_attempt_move():
    # create board
    pieces = [(Coord(x=0, y=0), Piece(color=PieceEnum.WHITE))]
    board = helper_setup_board(helper_empty_board(), pieces)
    # call test
    valid_move = attempt_move(
        board, PlayerColor.WHITE, MoveType.MOVE, Coord(x=0, y=0), Coord(x=1, y=1)
    )
    # validate output
    assert valid_move


def test_attempt_first_move():
    board = init_board()
    valid_move = attempt_move(
        board, PlayerColor.BLACK, MoveType.MOVE, Coord(x=2, y=5), Coord(x=1, y=4)
    )
    assert valid_move


# def test_attempt_move_dev():
#     board = init_board()
#     # 2,5 -> 1,4
#     valid_move = attempt_move(
#         board, PlayerColor.WHITE, MoveType.MOVE, Coord(x=2, y=5), Coord(x=1, y=4)
#     )
#     assert valid_move
