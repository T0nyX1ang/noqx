function decode_puzzlink_extra(url) {
  const parts = url.split("?");
  const urldata = parts[1].split("/");
  const type = urldata[0];
  const cols = parseInt(urldata[1]);
  const rows = parseInt(urldata[2]);

  if (cols > pu.gridmax["square"] || rows > pu.gridmax["square"]) {
    errorMsg(PenpaText.get("puzzlink_row_column", pu.gridmax["square"].toString()));
    return;
  }

  const bstr = urldata[3];
  const puzzlink_pu = new Puzzlink(cols, rows, bstr);

  // Set border whitespace to 0 for consistency
  document.getElementById("nb_space1").value = 0;
  document.getElementById("nb_space2").value = 0;
  document.getElementById("nb_space3").value = 0;
  document.getElementById("nb_space4").value = 0;

  function setupProblem(puzzle, mode) {
    puzzle.reset_frame(); // Draw the board
    panel_pu.draw_panel();
    document.getElementById("modal").style.display = "none";
    puzzle.mode_set(mode); //include redraw
  }
}
