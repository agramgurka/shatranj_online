function display_settings() {
    let settings = document.getElementById("game_settings");
    settings.classList.remove("hidden");
    new_game.classList.add("hidden");
};
let new_game_btn = document.getElementById("new_game");
new_game_btn.onclick = display_settings;

function close_settings() {
    let settings = document.getElementById("game_settings");
    settings.classList.add("hidden");
    let new_game = document.getElementById("new_game");
    new_game.classList.remove("hidden");
};
let close_settings_btn = document.getElementById("close_settings");
close_settings_btn.onclick = close_settings;

function create_new_game() {
    let settings = document.getElementById("game_settings");
    json_settings = new FormData(settings);
    close_settings();
    ws.send(
        JSON.stringify({
            "command": "create",
            "settings": Object.fromEntries(json_settings)
        }));
};

let create_new_game_btn = document.getElementById("create_new_game");
create_new_game_btn.onclick = create_new_game;

function cancel_created_game() {
    ws.send(
        JSON.stringify({
            "command": "cancel_created_game",
            "game_id": game_id
        }));
    if (typeof check_opponent_interval !== 'undefined') clearInterval(check_opponent_interval);
    game_id = null;
    let waiting_opponent = document.getElementById("waiting_opponent");
    waiting_opponent.classList.add("hidden");
    let new_game = document.getElementById("new_game");
    new_game.classList.remove("hidden");
};
let cancel_created_game_btn = document.getElementById("cancel_created_game");
cancel_created_game_btn.onclick = cancel_created_game;


function log_out() {
    ws.send(
        JSON.stringify({
            "command": "log_out",
        }));
    location.reload()
}
let log_out_button = document.getElementById('log_out');
log_out_button.onclick = log_out;

function display_auth_window() {
    let auth_window = document.getElementById("auth");
    auth.classList.remove("hidden");
}
let log_in_btn2 = document.getElementById("log_in");
log_in_btn2.onclick = display_auth_window;

function hide_auth_window() {
    let auth_window = document.getElementById("auth");
    auth.classList.add("hidden");
    alert = document.getElementById('alert');
    alert.classList.add('hidden');
}
let cancel_auth_btn = document.getElementById("cancel_auth");
cancel_auth_btn.onclick = hide_auth_window;


function register() {
    window.open(origin + "/register/", "_self");
}
let register_btn = document.getElementById('register');
register_btn.onclick = register;