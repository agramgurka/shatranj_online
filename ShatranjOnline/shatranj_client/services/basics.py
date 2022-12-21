""" game basic classes """

from abc import ABC, abstractmethod
from enum import Enum
from typing import Type, Optional


class Color(Enum):
    """ piece color """

    WHITE = "white"
    BLACK = "black"

    @staticmethod
    def opposite_color(color: 'Color') -> 'Color':
        """ return opposite color for passed """

        return Color.BLACK if color == Color.WHITE else Color.WHITE


class Direction:
    """ piece's move direction """

    def __init__(self, cols_dir: int, rows_dir: int):
        self.cols_dir = cols_dir
        self.rows_dir = rows_dir

    def __mul__(self, other: int):
        if other > 0:
            cols_dir = self.cols_dir * other
            rows_dir = self.rows_dir * other
            return Direction(cols_dir, rows_dir)
        return self


class PieceType(ABC):
    """ abstract class for pieces' types """

    @classmethod
    @abstractmethod
    def directions(cls) -> Optional[tuple[Direction]]:
        """ returns possible directions for piece type"""


    @classmethod
    @abstractmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """


    @classmethod
    @abstractmethod
    def special_attack_directions(cls) -> Optional[tuple[Direction]]:
        """ returns special attack directions for piece type if presented """


class MainPiece:
    """ class indicating the main piece of the piece set e.g. king"""


class Piece:
    """ game piece"""

    def __init__(self, piece_color: Color, piece_type: Type[PieceType]):
        self.piece_color = piece_color
        self.piece_type = piece_type

    def __str__(self) -> str:
        return f'{self.piece_color.name} {self.piece_type.code()}'


class Cell:
    """ board cell"""

    def __init__(self, col_number: int, row_number: int):
        self.col_number = col_number
        self.row_number = row_number
        self.color = Color.BLACK if (col_number + row_number) % 2 == 0 else Color.WHITE
        self.piece = None

    def __add__(self, other: Direction) -> 'Cell':
        destination = Cell(self.col_number + other.cols_dir, self.row_number + other.rows_dir)
        return destination

    def __eq__(self, other: 'Cell') -> bool:
        return self.col_number == other.col_number and self.row_number == other.row_number

    def __str__(self) -> str:
        cell_notation = chr(ord('A') + self.col_number) + str(self.row_number + 1)
        return cell_notation

    @classmethod
    def from_notation(cls, notation: str) -> 'Cell':
        """ returns Cell object from literal notation """

        col = ord(notation[0].upper()) - ord('A')
        row = int(notation[1:]) - 1
        return cls(col, row)

    def put_piece(self, piece: Piece) -> None:
        """ put piece on a cell """

        self.piece = piece

    def remove_piece(self) -> None:
        """ remove piece from a cell """

        self.piece = None

    def to_dict(self) -> dict:
        """ converts Cell object to dict """

        return {'col': self.col_number, 'row': self.row_number}


class Move:
    """ piece move """

    def __init__(self, start_cell: Cell, destination: Cell):
        self.start_cell = start_cell
        self.destination = destination

    def to_chess_notation(self) -> str:
        """ converts move to chess notation """
        notation = f'{self.start_cell} {self.destination}'
        return notation

    def __str__(self) -> str:
        return self.to_chess_notation()

    def __eq__(self, other) -> bool:
        return self.start_cell == other.start_cell and self.destination == other.destination

    def as_dict(self) -> dict:
        """ converts Move object to dict """

        return {
            'start': {'row': self.start_cell.col_number, 'col': self.start_cell.row_number},
            'destination': {'row': self.destination.col_number, 'col': self.destination.row_number},
        }
