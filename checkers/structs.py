from pydantic import BaseModel, Field, model_serializer
from enum import StrEnum


class PlayerColor(StrEnum):
    WHITE = "white"
    BLACK = "black"


class PieceEnum(StrEnum):
    WHITE = "w"
    BLACK = "b"


class MoveType(StrEnum):
    CAPTURE = "c"
    MOVE = "m"


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
