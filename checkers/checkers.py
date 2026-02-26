from pydantic import BaseModel, Field


WHITE_PIECE = "w"
BLACK_PIECE = "b"


def init_board() -> list[str | None]:
    board = []
    for i in range(8):
        row = []
        if i == 0 or i == 1:
            row = init_row(BLACK_PIECE)
        elif i == 6 or i == 7:
            row = init_row(WHITE_PIECE)
        else:
            row = init_row(None)
        board.append(row)
    return board


def init_row(piece_to_place: str | None) -> list[str | None]:
    row = []
    for _ in range(8):
        row.append(piece_to_place)
    return row


class Checkers(BaseModel):
    board: list[str | None] = Field(frozen=True, default=init_board())
