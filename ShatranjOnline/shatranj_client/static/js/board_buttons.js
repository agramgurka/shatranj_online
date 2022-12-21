function hide_draw_menu() {
    let draw_menu = document.getElementById('draw_menu');
    draw_menu.classList.add('hidden');
};

let decline_draw_btn = document.getElementById('decline_draw');
decline_draw_btn.onclick = hide_draw_menu;


function accept_draw() {
    hide_draw_menu();
    ws.send(
        JSON.stringify({
            "command": "accept_draw",
        }));
}
let accept_draw_btn = document.getElementById('accept_draw');

accept_draw_btn.onclick = accept_draw;

function resign() {
    ws.send(
        JSON.stringify({
            "command": "resign",
        }));
};

let resign_btn = document.getElementById("resign");
resign_btn.onclick = resign;

function suggest_draw() {
    ws.send(
        JSON.stringify({
            "command": "suggest_draw",
        }));
};

let draw_btn = document.getElementById("draw");
draw_btn.onclick = suggest_draw;