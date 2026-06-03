penpa_tags["options"]["puzzlink"].push("fivecells");
penpa_tags["options"]["puzzlink"].push("fourcells");

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
  let puzzlink_pu = new Puzzlink(cols, rows, bstr);

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
    case "fivecells":
    case "fourcells":
      /* base on "nawabari" type */

      pu = new Puzzle_square(cols, rows, size);
      pu.mode_grid("nb_grid2"); // Dashed grid lines
      setupProblem(pu, "combi");

      info_number = puzzlink_pu.decodeNumber10();
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("edgesub");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = [type];
      break;

    case "numlin_bit":
      /* base on "numlin" and "easyasabc" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "combi");

      info_number = puzzlink_pu.decodeNumber16();
      if (type !== "numlin_bit") {
        const string_map = "0ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        for (var i in info_number) {
          info_number[i] = string_map[info_number[i]] || info_number[i];
        }
      }
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("combi");

      if (type === "dominion") pu.subcombimode("blpo");
      else if (type === "nikoji") pu.subcombimode("edgesub");
      else if (["arukone", "numlin_bit"].includes(type)) pu.subcombimode("linex");

      UserSettings.tab_settings = ["Surface", "Composite"];
      if (type !== "numlin_bit") pu.user_tags = [type];
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

  // Set the Source
  document.getElementById("saveinfosource").value = url;

  // Set the tags
  set_genre_tags(pu.user_tags);
}
