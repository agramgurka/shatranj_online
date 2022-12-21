const ws = new WebSocket(
    'ws://' + window.location.host + '/ws/game_pool/'
);
let game_id = null;
ws.onmessage = function(response) {
    const res = JSON.parse(response.data);
    const command = res.command;
    if (command == "active_games_update") {
        let table = document.getElementById("active_games");
        table.innerHTML = "";
        let head = document.createElement("thead");
        head.innerHTML = "<thead> <tr> <th colspan=3><h2 class='text-center'>ACTIVE GAMES</h2></th></tr><tr><th>Color</th><th>Player</th><th></th></tr></thead>"
        table.appendChild(head);
        let games = res.active_games;
        let body = document.createElement('tbody');

        for (let i in games) {
            let board_row = document.createElement('tr');
            let game = document.createElement('td');

            let color = document.createElement('td');
            let white = document.createElement('td');
            let black = document.createElement('td');

            if (games[i].white) {
                color.classList.add('play_for_black')
                white.appendChild(document.createTextNode(games[i].white));
            }
            if (games[i].black) {
                color.classList.add('play_for_white')
                black.appendChild(document.createTextNode(games[i].black));
            }
            let join = document.createElement("button");
            join.innerHTML = "JOIN";
            join.id = games[i].id;
            join.onclick = join_game;
            join.type = "button";
            join.classList.add('btn');
            join.classList.add('btn-outline-dark');
            game.appendChild(join);
            board_row.appendChild(color);
            if (games[i].white) board_row.appendChild(white);
            if (games[i].black) board_row.appendChild(black);
            board_row.appendChild(game);

            body.appendChild(board_row);

        }
        table.appendChild(body);

    }
    if (command == "start_game") {
        if (typeof check_opponent_interval !== 'undefined') clearInterval(check_opponent_interval);
        window.open(origin + "/" + res.game, "_self");
    }
    if (command == "game_created") {
        game_id = res.game_id;
        check_opponent_interval = setInterval(check_opponent, 1000, game_id);
        let waiting_opponent = document.getElementById("waiting_opponent");
        waiting_opponent.classList.remove("hidden");
    }
    if (command == "not_authorized") {
        display_auth_window();
    }
};

function get_games() {
    ws.send(
        JSON.stringify({
            "command": "get_games",
        }));
}
setTimeout(get_games, 100);
let update_interval = setInterval(get_games, 1000);

function check_opponent(game_id) {
    ws.send(
        JSON.stringify({
            "command": "check_opponent",
            "game_id": game_id
        }));
}

function join_game() {
    ws.send(
        JSON.stringify({
            "command": "join",
            "game_id": this.id
        }));
}

function display_auth_window() {
    let auth_window = document.getElementById("auth");
    auth.classList.remove("hidden");
}