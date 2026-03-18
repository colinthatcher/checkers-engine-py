from datetime import time
from collections import defaultdict
from typing import Annotated, Dict
from pydantic import BaseModel, Field
from .structs import *
from .tools import *

CLOCK_START_TIME = 60 * 5  # 5m

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


class Checkers(BaseModel):
    board: list[list[str | None]] = Field(frozen=True, default=init_board())
    # record the number of times each unique position occurs for draw checking
    position_tracker: Annotated[
        Dict[str, int],
        Field(default_factory=lambda: defaultdict[str, int](lambda: 0)),
    ]
    game_started: bool = Field(default=False)
    # Maps client id -> player color
    client_color_map: dict = Field(default=dict())
    # shared state to determine when both clients are ready to start
    clients_ready: set = Field(default=set())
    # player color of who's turn it currently is
    player_turn: PlayerColor = Field(default=PlayerColor.BLACK)
    # Clock tracking
    black_clock: time = Field(default=None)
    white_clock: time = Field(default=None)
    black_clock_remaining: float = Field(default=CLOCK_START_TIME)
    white_clock_remaining: float = Field(default=CLOCK_START_TIME)
    # Draw tracking
    normal_piece_advance_counter: int = Field(default=0)
    capture_counter: int = Field(default=0)

    def model_post_init(self, _) -> None:
        self.position_tracker[hash_board(self.board)] += 1
