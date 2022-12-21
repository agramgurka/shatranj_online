""" shatranj engine module """

from typing import Optional

from .basics import Piece, Move, Color, Cell, MainPiece
from .shatranj_pieces import SHATRANJ_CLASSICAL_START_POSITION, SHATRJ_PIECE_TYPES,\
    Ferz, WhiteSarbaz, BlackSarbaz

START_POSITION = SHATRANJ_CLASSICAL_START_POSITION
PIECE_TYPES = SHATRJ_PIECE_TYPES


class PositionNotation:
    """ position notation management """

    @classmethod
    def from_notation(cls, notation: str) -> list[dict]:
        """ gets position from the notation"""

        pieces = []
        pieces_notation = notation.split('|')[:-1]
        for piece in pieces_notation:
            color = Color.WHITE if piece[0] == 'W' else Color.BLACK
            position = Cell.from_notation(piece[3:])
            for _type in PIECE_TYPES:
                if _type.code() == piece[1:3]:
                    piece_type = _type
            pieces.append(
                {
                    'color': color,
                    'type': piece_type,
                    'position': position
                }
            )
        return pieces

    @classmethod
    def to_notation(cls, pieces: list[dict]) -> str:
        """ gets notation from pieces' dict """

        notation = ""
        for piece in pieces:
            notation += 'W' if piece['color'] == Color.WHITE else 'B'
            notation += piece['type'].code()
            notation += str(piece['position'])
            notation += '|'
        return notation


class Board:
    """ game board """

    def __init__(self, rows_count: int, cols_count: int, piece_set: list[dict]):
        self.rows_count = rows_count
        self.cols_count = cols_count
        self.cells = [Cell(col, row) for col in range(self.cols_count) for row in range(self.rows_count)]
        self.put_pieces(piece_set)

    @property
    def position_notation(self) -> str:
        """ returns position's notation """

        return PositionNotation.to_notation(self.get_pieces())

    def make_move(self, move: Move) -> None:
        """ make move """
        start_cell = move.start_cell
        piece = move.start_cell.piece
        destination = move.destination
        if self.move_is_promotion(move):
            piece = Piece(piece.piece_color, Ferz)
        start_cell.remove_piece()
        destination.remove_piece()
        destination.put_piece(piece)

    def piece_possible_moves(self, cell: Cell) -> Optional[list[Move]]:
        """ returns piece's possible moves """

        possible_moves = []
        if cell.piece:
            piece = cell.piece
            piece_type = piece.piece_type
            if piece_type.is_long_ranged():
                for direction in piece_type.directions():
                    distance = 1
                    while True:
                        destination = self.get_cell(cell + direction * distance)
                        if destination:
                            move = Move(cell, destination)
                            if not destination.piece:
                                possible_moves.append(move)
                                distance += 1
                                continue
                            if self.move_is_attack(move):
                                possible_moves.append(move)
                        break
            elif piece_type.special_attack_directions():
                for attack in piece_type.special_attack_directions():
                    destination = self.get_cell(cell + attack)
                    if destination:
                        move = Move(cell, destination)
                        if self.move_is_attack(move):
                            possible_moves.append(move)
                for direction in piece_type.directions():
                    destination = self.get_cell(cell + direction)
                    if destination:
                        move = Move(cell, destination)
                        if not destination.piece:
                            possible_moves.append(move)
            else:
                for direction in piece_type.directions():
                    destination = self.get_cell(cell + direction)
                    if destination:
                        move = Move(cell, destination)
                        if not destination.piece or self.move_is_attack(move):
                            possible_moves.append(move)
        return possible_moves

    def put_pieces(self, piece_set: list[dict]) -> None:
        """ put pieces on board """

        for item in piece_set:
            color = item['color']
            piece_type = item['type']
            cell = self.get_cell(item['position'])
            cell.put_piece(Piece(color, piece_type))

    def get_pieces(self) -> Optional[list[dict]]:
        """ gets all pieces from board """

        pieces = []
        for cell in self.cells_with_pieces():
            piece = {
                'color': cell.piece.piece_color,
                'type': cell.piece.piece_type,
                'position': cell
            }
            pieces.append(piece)
        return pieces

    @staticmethod
    def move_is_attack(move: Move) -> bool:
        """ check if move is attack """

        moving_piece = move.start_cell.piece
        attacked_piece = move.destination.piece
        return attacked_piece and moving_piece.piece_color != attacked_piece.piece_color

    def move_is_promotion(self, move: Move) -> bool:
        """ check if move is promotion """

        start_cell = move.start_cell
        destination = move.destination
        piece = start_cell.piece
        if piece and piece.piece_type == WhiteSarbaz:
            if destination.row_number == self.cols_count - 1:
                return True
        elif piece and piece.piece_type == BlackSarbaz:
            if destination.row_number == 0:
                return True
        return False

    def cells_with_pieces(self, color=None) -> Optional[list[Cell]]:
        """ returns cells that have got pieces on them """

        pieces = []
        if color:
            for cell in self.cells:
                if cell.piece and cell.piece.piece_color == color:
                    pieces.append(cell)
        else:
            for cell in self.cells:
                if cell.piece:
                    pieces.append(cell)
        return pieces

    def player_is_checked(self, player_color: Color) -> bool:
        """ check if player is checked """

        opponent_color = Color.opposite_color(player_color)
        pieces = self.cells_with_pieces(opponent_color)
        king = self.get_king(player_color)
        if not king:
            for piece in self.get_pieces():
                print(piece['position'], piece['type'].code(), piece['color'].name)
        for piece in pieces:
            possible_moves = self.piece_possible_moves(piece)
            for move in possible_moves:
                if move.destination == king:
                    return True
        return False

    def get_cell(self, cell: Cell) -> Optional[Cell]:
        """ returns cell from board """

        try:
            cell_idx = self.cells.index(cell)
            return self.cells[cell_idx]
        except ValueError:
            return None

    def get_king(self, color) -> Cell:
        """ returns cell with king"""

        for cell in self.cells:
            if cell.piece and issubclass(cell.piece.piece_type, MainPiece) and cell.piece.piece_color == color:
                return cell
        raise NotImplementedError(f'No {color} king')

    def position_after_move(self, move: Move) -> 'Board':
        """ returns position on board after the move """

        position = Board(self.rows_count, self.cols_count, self.get_pieces())
        start_cell = position.get_cell(move.start_cell)
        destination = position.get_cell(move.destination)
        move = Move(start_cell, destination)
        position.make_move(move)
        return position


class Game:
    """ base game class """

    def __init__(self, settings: dict):
        cols = settings.get('board', {}).get('cols', 8)
        rows = settings.get('board', {}).get('rows', 8)
        position = settings.get('position', SHATRANJ_CLASSICAL_START_POSITION)
        self.board = Board(cols, rows, position)
        self.turn = settings.get('turn', Color.WHITE)
        self._last_move = ''
        self.has_started = settings.get('has_started', False)
        self.has_finished = settings.get('has_finished', False)

    def switch_turn(self) -> None:
        """ switch turn to go """

        self.turn = Color.opposite_color(self.turn)


class OnlineGame(Game):
    """ class maintaining shatranj online game"""

    @property
    def last_move(self) -> str:
        """ returns game's last move notation """

        return str(self._last_move)

    def process_move(self, move: dict) -> None:
        """ processes passed move """

        start_cell = self.board.get_cell(Cell(move['start']['col'], move['start']['row']))
        destination = self.board.get_cell(Cell(move['destination']['col'], move['destination']['row']))
        move = Move(start_cell=start_cell, destination=destination)
        if move in self.possible_moves():
            self.board.make_move(move)
            self._last_move = move
            self.switch_turn()
            if self.is_win() or self.is_draw():
                self.has_finished = True
        else:
            raise ValueError('get impossible move from client')

    def is_win(self) -> bool:
        """ checks if game is won """

        return not self.possible_moves() or self.bare_king_win()

    def is_draw(self) -> bool:
        """ checks if game is drawn """

        return self.bare_king_draw()

    def possible_moves(self) -> Optional[list[Move]]:
        """ returns all possible moves """

        possible_moves = []
        if self.has_finished:
            return possible_moves
        if self.board.player_is_checked(self.turn):
            checked_player_pieces = self.board.cells_with_pieces(self.turn)
            all_moves = []
            checked_player_possible_moves = []
            for piece in checked_player_pieces:
                all_moves.extend(self.board.piece_possible_moves(piece))
            for move in all_moves:
                position = self.board.position_after_move(move)
                if not position.player_is_checked(self.turn):
                    checked_player_possible_moves.append(move)
            if not checked_player_possible_moves:
                self.has_finished = True
            else:
                possible_moves = checked_player_possible_moves
        else:
            for cell in self.board.cells_with_pieces(self.turn):
                for move in self.board.piece_possible_moves(cell):
                    position = self.board.position_after_move(move)
                    if not position.player_is_checked(self.turn):
                        possible_moves.append(move)
        return possible_moves

    def bare_king_win(self) -> bool:
        """ check if game is won with bare king rule """

        pieces = self.board.cells_with_pieces(self.turn)
        if len(pieces) == 1:
            for move in self.possible_moves():
                position = self.board.position_after_move(move)
                opponent_pieces = position.cells_with_pieces(Color.opposite_color(self.turn))
                if len(opponent_pieces) == 1:
                    return False
            return True
        return False

    def bare_king_draw(self) -> bool:
        """ check if game is drawn with bare king rule """

        pieces = self.board.cells_with_pieces(self.turn)
        opponent_pieces = self.board.cells_with_pieces(Color.opposite_color(self.turn))
        return len(pieces) == 1 and len(opponent_pieces) == 1

    def render_board(self) -> dict:
        """ returns board's parameters """

        return {
            "cols": self.board.cols_count,
            "rows": self.board.rows_count
        }

    def render_position(self) -> list[dict]:
        """ returns json serializable representation of pieces position"""

        position = []
        for piece in self.board.get_pieces():
            rendered_piece = {
                "position": piece['position'].to_dict(),
                "color": piece['color'].name,
                "type": piece['type'].code()
            }
            position.append(rendered_piece)
        return position
