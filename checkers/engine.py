import logging
import json
import pydantic
import time
import random
from fastapi import WebSocket

from .ConnectionManager import ConnectionManager
from .checkers import Checkers
from .structs import *
from .tools import *


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


async def main_loop(game: Checkers, manager: ConnectionManager, websocket: WebSocket, client_id: int):
    while True:
        raw_msg = await websocket.receive_text()
        # await manager.send_message(f"Received:{raw_msg}", websocket)

        try:
            raw_json = json.loads(raw_msg)['messageText']
        except KeyError:
            await manager.send_message(f"JSON failed to parse, invalid move from client: {client_id}", websocket)
            continue
 
        if not game.game_started:
            if "ready" in raw_json.lower():
                await manager.send_message(f"ACK Client #{client_id} READY", websocket)
                game.clients_ready.add(client_id)

            if len(game.clients_ready) >= 2:
                first_client_color = random.choice(list(PlayerColor))
                second_client_color = PlayerColor.WHITE if first_client_color == PlayerColor.BLACK else PlayerColor.BLACK
                game.client_color_map[list(game.clients_ready)[0]] = first_client_color
                game.client_color_map[list(game.clients_ready)[1]] = second_client_color

                print("Starting game!")
                await manager.broadcast(f"Game started, {game.client_color_map}")

                game.black_clock = time.time()
                game.game_started = True
            continue
        
        await manager.broadcast(f"Move received from Client #{client_id}")

        # Payload Example:
        # {"move_type": "m", "start_position": {"x": 2, "y": 5}, "end_position": {"x": 1, "y": 4}}   BLACK
        # {"move_type": "m", "start_position": {"x": 1, "y": 2}, "end_position": {"x": 2, "y": 3}}   WHITE
        # {"move_type": "m", "start_position": {"x": 3, "y": 2}, "end_position": {"x": 4, "y": 3}}   WHITE
        try:
            data = MovePayload.model_validate_json(raw_json)
        except pydantic.ValidationError as validation_error:
            print(validation_error.errors())
            await manager.send_message(f"JSON failed to parse, invalid move from client: {client_id}", websocket)
            continue
        
        player_color = game.client_color_map[client_id]
        move_type = data.move_type
        start_coord = data.start_position
        end_coord = data.end_position

        if game.player_turn != player_color:
            # Not the player's turn
            await manager.send_message(f"You must wait until your turn", websocket)
            continue

        # TODO: If one player never makes a valid move, the clock won't call a winner until a valid move is played
        is_move_success = attempt_move(game.board, player_color, move_type, start_coord, end_coord)
        if not is_move_success:
            await manager.send_message(f"Invalid move, try again", websocket)
            continue
        
        last_move_timestamp = time.time()

        # setup white's clock once black makes valid first move
        if player_color == PlayerColor.BLACK and game.white_clock is None:
            game.white_clock = time.time()
        
        if player_color == PlayerColor.BLACK:
            game.black_clock_remaining -= last_move_timestamp - game.black_clock
        elif player_color == PlayerColor.WHITE:
            game.white_clock_remaining -= last_move_timestamp - game.white_clock
        
        if game.black_clock_remaining <= 0:
            # Declare winner, black lost on time
            await manager.broadcast(f"White won the game because Black ran out of time!")
            return
        if game.white_clock_remaining <= 0:
            # Declare winner, white lost on time
            await manager.broadcast(f"Black won the game because White ran out of time!")
            return
        
        winner = check_winner(game.board)
        if winner is not None:
            # Declare winner
            await manager.broadcast(f"{winner} won the game!")
            return
        
        game.position_tracker[hash_board(game.board)] += 1
        if game.position_tracker[hash_board(game.board)] >= 3:
            # Game is a draw, same position repeated three times
            await manager.broadcast(f"Black and White draw the game because the same position repeated three times!")
            return

        if move_type == MoveType.CAPTURE:
            game.capture_counter = 0
        else:
            game.capture_counter += 1
        
        if game.capture_counter >= 39:
            # Game is a draw, no capture occured in the last 40 moves
            await manager.broadcast(f"Black and White draw the game because no captures in the last 40 turns!")
            return
        
        game.normal_piece_advance_counter += 1
        piece: Piece = game.board[end_coord.y][end_coord.x]
        if not piece.king:
            dist_y = end_coord.y - start_coord.y
            if dist_y < 0 and player_color == PlayerColor.BLACK:
                game.normal_piece_advance_counter = 0
            elif dist_y > 0 and player_color == PlayerColor.WHITE:
                game.normal_piece_advance_counter = 0

        if game.normal_piece_advance_counter >= 39:
            # Game is a draw, neither player has moved one of their
            # normal pieces towards the opposing player in the last 40 moves
            await manager.broadcast(f"Black and White draw the game, neither player moved with a normal piece in the last 40 moves!")
            return

        # tell the other player it's their turn and move turn
        if player_color == PlayerColor.BLACK:
            game.white_clock = time.time()
            game.player_turn = PlayerColor.WHITE
        elif player_color == PlayerColor.WHITE:
            game.black_clock = time.time()
            game.player_turn = PlayerColor.BLACK
        
        await manager.broadcast(f"{player_color} moved, now it's {game.player_turn} turn!")
        await manager.broadcast(game.board)
        print_board(game.board)


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
