function decode_puzzlink_extra(url) {
  const parts = url.split("?");
  const urldata = parts[1].split("/");
  const type = urldata[0];
  const cols = parseInt(urldata[1]);
  const rows = parseInt(urldata[2]);
  const size = UserSettings.displaysize;

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

  // prettier-ignore
  var info_edge, info_number, info_obj,
      row_ind, col_ind, cell, value, corner_cursor,
      number_style, map_genre_tag;

  switch (type) {
    case "chocona":
    case "cocktail":
    case "hinge":
    case "mannequin":
      /* act as "aqre" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "surface");

      info_edge = puzzlink_pu.decodeBorder();
      info_number = puzzlink_pu.decodeNumber16();
      info_number = puzzlink_pu.moveNumbersToRegionCorners(info_edge, info_number);

      puzzlink_pu.drawBorder(pu, info_edge, 2);
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("surface");
      UserSettings.tab_settings = ["Surface"];
      break;

    case "context":
    case "norinuri":
    case "smullyan":
      /* act as "nuribou" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "surface");

      info_number = puzzlink_pu.decodeNumber16();
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("surface");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      break;

    default:
      errorMsg(PenpaText.get("puzzlink_not_supported", type));
      break;
  }

  // Set PenpaLite
  // document.getElementById('advance_button').value = "1";
  document.getElementById("mode_break").classList.add("is_hidden");
  document.getElementById("mode_txt_space").classList.add("is_hidden");
  advancecontrol_off("url");

  var tabSelect = document.querySelector("ul.multi");
  var tabOptions = UserSettings.tab_settings;
  if (tabSelect) {
    for (var child of tabSelect.children) {
      if (!child.dataset.value) {
        continue;
      }

      if (tabOptions.includes(child.dataset.value)) {
        if (!child.classList.contains("active")) {
          child.click();
        }
      } else {
        if (child.classList.contains("active")) {
          child.click();
        }
      }
    }
  }

  // Redraw the grid
  pu.redraw();
}
