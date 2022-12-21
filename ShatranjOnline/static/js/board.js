function drawBoard(board, player_color) {
    var board_elem = document.getElementById('board');

    for (var i = board.rows - 1; i >= 0; i--) {
        var board_row = document.createElement('tr');
        for (var j = 0; j < board.cols; j++) {
            var board_cell = document.createElement('td');
            board_cell.classList.add('cell')
            if ((i + j) % 2 === 0) {
                board_cell.classList.add('black_field');
            } else {
                board_cell.classList.add('white_field');
            }
            board_row.appendChild(board_cell);
        }
        board_elem.appendChild(board_row);
    }
    if (player_color == "BLACK") {
        board_elem.classList.add('rotated')
    }
}

function drawPieces(position, player_color) {
    var board = document.getElementById('board')
    var rows_cnt = board.rows.length;
    for (var i = 0; i < rows_cnt; i++) {
        row = board.rows[i];
        for (var j = 0, cell; cell = row.cells[j]; j++) {
            var classes = cell.className.split(' ');
            classes.forEach(name => {
                if (name != 'cell' &&
                    name != 'white_field' &&
                    name != 'black_field') {
                    cell.classList.remove(name);
                }
            })
            position.forEach((piece) => {
                if (piece.position.row === rows_cnt - 1 - i && piece.position.col === j) {
                    cell.onclick = select_piece;
                    cell.classList.add(piece.type);
                    cell.classList.add(piece.color);
                    cell.classList.add("piece");
                    if (player_color == "BLACK") {
                        cell.classList.add('rotated')
                    }
                }
            });

        }
    }
}

function select_piece() {
    this.classList.add("selected_piece");
    cells = document.getElementsByClassName("cell");
    for (var idx in cells) {
        cells[idx].onclick = select_move;
    }
}

function select_move() {
    this.classList.add("selected_move");
    cells = document.getElementsByClassName("cell");
    for (var idx in cells) {
        cells[idx].onclick = null;
    }
    process_move();
}

function get_move() {
    var board = document.getElementById('board')
    var rows_cnt = board.rows.length;
    var start = null;
    var dist = null;

    for (var i = 0; i < rows_cnt; i++) {
        row = board.rows[i];
        for (var j = 0, cell; cell = row.cells[j]; j++) {
            if (cell.classList.contains('selected_piece')) {
                start = {
                    "col": j,
                    "row": rows_cnt - 1 - i
                };
                cell.classList.remove('selected_piece');
            }
            if (cell.classList.contains('selected_move')) {
                dist = {
                    "col": j,
                    "row": rows_cnt - 1 - i
                };
                cell.classList.remove('selected_move');
            }
        }
    }
    return {
        "start": start,
        "destination": dist
    }
}

function process_move() {
    move = get_move();
    ws.send(
        JSON.stringify({
            "command": "make_move",
            "move": move,
        }));
    cells = document.getElementsByClassName("cell");
    for (var idx in cells) {
        cells[idx].onclick = null;
    }
    pieces = document.getElementsByClassName("piece");
    for (var idx in pieces) {
        pieces[idx].onclick = select_piece;
    }

}

drawBoard(board, player_color);
drawPieces(position, player_color);