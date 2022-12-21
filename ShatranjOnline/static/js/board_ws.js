const ws = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/game/' +
    game_id +
    '/'
);
setTimeout(function () {
    ws.send(
        JSON.stringify({
            "command": "init",
        })
    );
}, 100);

ws.onmessage = function (response) {
    const res = JSON.parse(response.data);
    const command = res.command;
    if (command == "position") {
        drawPieces(res.position, player_color);
        switch_turn();
        write_moves_history(res.move);
    }
    if (command == "over") {
        game_over(res.winner);
    }
    if (command == "init") {
        write_moves_history(res.moves);
    }
    if (command == "suggest_draw") {
        if (res.to == user) display_draw_menu();
    }
};

function display_draw_menu() {
    let draw_menu = document.getElementById('draw_menu');
    draw_menu.classList.remove('hidden');
};

function game_over(winner) {
    let turn = document.getElementById('turn');
    if (winner) turn.innerHTML = "GAME OVER, " + winner + " won";
    else turn.innerHTML = "Draw";
}

function write_moves_history(moves) {
    let moves_history = document.getElementById('moves');
    moves_history.innerHTML += "|" + moves;
}

function switch_turn() {
    let turn = document.getElementById('turn');
    if (turn.innerHTML == "Turn: " + "WHITE") {
        turn.innerHTML = "Turn: " + "BLACK";
    } else {
        turn.innerHTML = "Turn: " + "WHITE";
    }
}