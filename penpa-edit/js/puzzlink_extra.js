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
      /* base on "aqre" type */

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
      /* base on "nuribou" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "surface");

      info_number = puzzlink_pu.decodeNumber16();
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("surface");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      break;

    case "lither":
    case "tslither":
    case "vslither":
      /* base on "slitherlink" type */
      pu = new Puzzle_square(cols, rows, size);
      // Draw grid dots only
      pu.mode_grid("nb_grid3");
      pu.mode_grid("nb_lat1");
      pu.mode_grid("nb_out2");
      setupProblem(pu, "combi");

      info_number = puzzlink_pu.decodeNumber4();
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("edgex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      break;

    case "nothree":
    case "nuriuzu":
      /* base on "tentaisho" type */

      pu = new Puzzle_square(cols, rows, size);
      pu.mode_grid("nb_grid2"); // Dashed gridlines
      setupProblem(pu, "surface");

      info_edge = puzzlink_pu.decodeMidloop();
      puzzlink_pu.drawMidloop(pu, info_edge);

      pu.mode_qa("pu_a");
      pu.mode_set("surface");
      UserSettings.tab_settings = ["Surface"];
      break;

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
      break;

    case "circlesquare":
    case "statuepark":
      /* base on "yinyang" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "combi");

      info_number = puzzlink_pu.decodeNumber3();
      // Draw the circles
      for (i in info_number) {
        if (info_number[i] === 0) {
          continue;
        }
        // Determine which row and column
        row_ind = parseInt(i / cols);
        col_ind = i % cols;
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].symbol[cell] = [info_number[i], "circle_M", 1];
      }

      pu.mode_qa("pu_a");
      UserSettings.tab_settings = ["Surface"];
      break;

    case "creek":
    case "nibunnogo":
      /* base on "gokigen" type */
      // Outside padding
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space2").value = 1;
      document.getElementById("nb_space3").value = 1;
      document.getElementById("nb_space4").value = 1;

      pu = new Puzzle_square(cols + 2, rows + 2, size);

      pu.mode_grid("nb_grid2"); // Dashed gridlines
      pu.mode_grid("nb_out2"); // No grid frame
      setupProblem(pu, "lineE");

      info_number = puzzlink_pu.decodeNumber4();

      for (var i in info_number) {
        row_ind = 2 + parseInt(i / (cols + 1));
        col_ind = 2 + (i % (cols + 1));
        cell = pu.nx0 * pu.ny0 + pu.nx0 * row_ind + col_ind;
        value = info_number[i] === "?" ? " " : info_number[i];
        pu["pu_q"].number[cell] = [value, 6, "1"];
      }

      pu.mode_qa("pu_a");
      pu.mode_set("lineE");
      pu.submode_check("sub_lineE2");
      UserSettings.tab_settings = ["Edge Diagonal"];
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
