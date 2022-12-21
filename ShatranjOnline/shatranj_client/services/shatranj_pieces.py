""" shatranj pieces' classes """

from typing import Optional, Iterable

from .basics import Color, PieceType, MainPiece, Direction, Cell


class Shah(PieceType, MainPiece):
    """ shatranj shah piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for shah piece type"""

        return (
            Direction(-1, -1),
            Direction(-1, 0),
            Direction(-1, 1),
            Direction(0, -1),
            Direction(0, 1),
            Direction(1, -1),
            Direction(1, 0),
            Direction(1, 1)
        )

    @classmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """

        return False

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for shah piece type """

        return None

    @classmethod
    def code(cls) -> str:
        """ returns shah piece type code """

        return "SH"


class Ferz(PieceType):
    """ shatranj ferz piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for ferz piece type"""

        return (
            Direction(-1, -1),
            Direction(-1, 1),
            Direction(1, -1),
            Direction(1, 1)
        )

    @classmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """

        return False

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for ferz piece type """

        return None

    @classmethod
    def code(cls) -> str:
        """ returns ferz piece type code """

        return "FZ"


class Rukh(PieceType):
    """ shatranj rukh piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for rukh piece type"""

        return (
                Direction(-1, 0),
                Direction(0, -1),
                Direction(1, 0),
                Direction(0, 1)
                )

    @classmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """

        return True

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for rukh piece type """

        return None

    @classmethod
    def code(cls) -> str:
        """ returns rukh piece type code """

        return "RH"


class Pil(PieceType):
    """ shatranj pil piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for pil piece type"""

        return (
                Direction(-2, -2),
                Direction(-2, 2),
                Direction(2, -2),
                Direction(2, 2)
        )

    @classmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """

        return False

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for pil piece type """

        return None

    @classmethod
    def code(cls) -> str:
        """ returns pil piece type code """

        return "PL"


class Asb(PieceType):
    """ shatranj asb piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for asb piece type"""

        return (
                Direction(-2, -1),
                Direction(-2, 1),
                Direction(-1, -2),
                Direction(-1, 2),
                Direction(1, -2),
                Direction(1, 2),
                Direction(2, -1),
                Direction(2, 1)
                )

    @classmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """

        return False

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for asb piece type """

        return None

    @classmethod
    def code(cls) -> str:
        """ returns asb piece type code """

        return "AB"


class Sarbaz(PieceType):
    """ shatranj sarbaz base piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for sarbaz piece type"""

        return None

    @classmethod
    def is_long_ranged(cls) -> bool:
        """ checks if piece type is long ranged """

        return False

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for sarbaz piece type """

        return None


class WhiteSarbaz(Sarbaz):
    """ shatranj white sarbaz piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for white sarbaz piece type"""

        return Direction(0, 1),

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for white sarbaz piece type """

        return (
               Direction(-1, 1),
               Direction(1, 1)
               )

    @classmethod
    def code(cls) -> str:
        """ returns white sarbaz piece type code """

        return "WS"


class BlackSarbaz(Sarbaz):
    """ shatranj black sarbaz piece"""

    @classmethod
    def directions(cls) -> Optional[Iterable[Direction]]:
        """ returns possible directions for black sarbaz piece type"""

        return Direction(0, -1),

    @classmethod
    def special_attack_directions(cls) -> Optional[Iterable[Direction]]:
        """ returns special attack directions for black sarbaz piece type """

        return (
               Direction(-1, -1),
               Direction(1, -1)
               )

    @classmethod
    def code(cls) -> str:
        """ returns black sarbaz piece type code """

        return "BS"


SHATRJ_PIECE_TYPES = [Shah, Ferz, Rukh, Pil, Asb, WhiteSarbaz, BlackSarbaz]


def get_classical_piece_set() -> list[dict]:
    """ returns classical shatranj pieceset"""

    piece_set = []

    for i in range(8):
        white_sarbaz = {
            'color': Color.WHITE,
            'type': WhiteSarbaz,
            'position': Cell(i, 1)
        }
        black_sarbaz = {
            'color': Color.BLACK,
            'type': BlackSarbaz,
            'position': Cell(i, 6)
        }

        piece_set.extend((white_sarbaz, black_sarbaz))
        if i in (0, 7):
            white_rukh = {
                'color': Color.WHITE,
                'type': Rukh,
                'position': Cell(i, 0)
            }
            black_rukh = {
                'color': Color.BLACK,
                'type': Rukh,
                'position': Cell(i, 7)
            }
            piece_set.extend((white_rukh, black_rukh))
        if i in (1, 6):
            white_asb = {
                'color': Color.WHITE,
                'type': Asb,
                'position': Cell(i, 0)
            }
            black_asb = {
                'color': Color.BLACK,
                'type': Asb,
                'position': Cell(i, 7)
            }
            piece_set.extend((white_asb, black_asb))
        if i in (2, 5):
            white_pil = {
                'color': Color.WHITE,
                'type': Pil,
                'position': Cell(i, 0)
            }
            black_pil = {
                'color': Color.BLACK,
                'type': Pil,
                'position': Cell(i, 7)
            }
            piece_set.extend((white_pil, black_pil))
        if i == 3:
            white_shah = {
                'color': Color.WHITE,
                'type': Shah,
                'position': Cell(i, 0)
            }
            black_shah = {
                'color': Color.BLACK,
                'type': Shah,
                'position': Cell(i, 7)
            }
            piece_set.extend((white_shah, black_shah))
        if i == 4:
            white_ferz = {
                'color': Color.WHITE,
                'type': Ferz,
                'position': Cell(i, 0)
            }
            black_ferz = {
                'color': Color.BLACK,
                'type': Ferz,
                'position': Cell(i, 7)
            }
            piece_set.extend((white_ferz, black_ferz))
    return piece_set


SHATRANJ_CLASSICAL_START_POSITION = get_classical_piece_set()
