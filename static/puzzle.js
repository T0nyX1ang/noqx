let puzzle_data = null;

function get(elt_id) {
  return document.getElementById(elt_id);
}

function make_elt(type, class_name, parent, innerHTML) {
  let elt = document.createElement(type);
  if (class_name !== undefined) elt.classList.add(class_name);
  if (parent !== undefined) parent.appendChild(elt);
  if (innerHTML !== undefined) elt.innerHTML = innerHTML;
  return elt;
}

// register expand/reduce operations

get("menu_expand_top").addEventListener("click", function () {
  puzzle.board.operate("expandup");
});

get("menu_expand_bottom").addEventListener("click", function () {
  puzzle.board.operate("expanddn");
});

get("menu_expand_left").addEventListener("click", function () {
  puzzle.board.operate("expandlt");
});

get("menu_expand_right").addEventListener("click", function () {
  puzzle.board.operate("expandrt");
});

get("menu_reduce_top").addEventListener("click", function () {
  puzzle.board.operate("reduceup");
});

get("menu_reduce_bottom").addEventListener("click", function () {
  puzzle.board.operate("reducedn");
});

get("menu_reduce_left").addEventListener("click", function () {
  puzzle.board.operate("reducelt");
});

get("menu_reduce_right").addEventListener("click", function () {
  puzzle.board.operate("reducert");
});

get("menu_turn_left").addEventListener("click", function () {
  puzzle.board.operate("turnl");
});

get("menu_turn_right").addEventListener("click", function () {
  puzzle.board.operate("turnr");
});

get("menu_flip_horiz").addEventListener("click", function () {
  puzzle.board.operate("flipx");
});

get("menu_flip_vert").addEventListener("click", function () {
  puzzle.board.operate("flipy");
});

get("menu_solve").addEventListener("click", function () {
  console.log(puzzle.getFileData());
  puzzle_data = puzzle.getFileData();

  current_request = new XMLHttpRequest();
  current_request.open(
    "GET",
    `solver/?puzzle_type=${puzzle.pid}&puzzle=${encodeURI(puzzle_data)}`
  );
  current_request.onreadystatechange = function () {
    if (this.stopped) return;
    else if (this.readyState == 4) {
      if (this.status == 200) {
        // solve went through correctly
        // set_solved();
        console.log(this.responseText);
      } else if (this.status != 200 && this.status != 0)
        // something went wrong
        display_error_message(this.responseText);
    }
  };
  current_request.send();
  spinner((start = true));
});

get("menu_clear").addEventListener("click", function () {
  puzzle.setMode("edit");
  if (puzzle_data !== null) {
    puzzle.open(puzzle_data);
    puzzle_data = null;
  } else puzzle.clear();
});

get("menu_undo").addEventListener("click", function () {
  puzzle.undo();
});

get("menu_redo").addEventListener("click", function () {
  puzzle.redo();
});

get("menu_editmode").addEventListener("click", function () {
  puzzle.setMode("edit");
  get("menu_editmode").setAttribute("class", "checked");
  get("menu_playmode").setAttribute("class", "check");
});

get("menu_playmode").addEventListener("click", function () {
  puzzle.setMode("play");
  get("menu_editmode").setAttribute("class", "check");
  get("menu_playmode").setAttribute("class", "checked");
});

let spinner_pos = null;
const spinner_values = [
  "Solving.&nbsp;&nbsp;",
  "Solving..&nbsp;",
  "Solving...",
];

function spinner(start = false, timeout = 500) {
  if (!start && spinner_pos == null) return;

  if (start) spinner_pos = 0;

  get("header_div").innerHTML = spinner_values[spinner_pos];
  spinner_pos = (spinner_pos + 1) % spinner_values.length;
  setTimeout(spinner, timeout);
}

function display_error_message(error_str) {
  spinner_pos = null; // stop the spinner

  error = JSON.parse(error_str);
  get("header_div").innerHTML = error.detail || "An unknown error occurred";
}
