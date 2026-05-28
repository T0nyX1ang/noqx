penpa_tags["options"]["puzzlink"].push("suguru (capsules)");
penpa_tags["options"]["puzzlink"].push("chocona");
penpa_tags["options"]["puzzlink"].push("cocktail lamp");
penpa_tags["options"]["puzzlink"].push("heyablock");
penpa_tags["options"]["puzzlink"].push("hinge");
penpa_tags["options"]["puzzlink"].push("mannequin gate");
penpa_tags["options"]["puzzlink"].push("context");
penpa_tags["options"]["puzzlink"].push("cityspace");
penpa_tags["options"]["puzzlink"].push("norinuri");
penpa_tags["options"]["puzzlink"].push("smullyan (smullyanic dynasty)");
penpa_tags["options"]["puzzlink"].push("Inaba's island");
penpa_tags["options"]["puzzlink"].push("oasis");
penpa_tags["options"]["puzzlink"].push("lither (lithersink)");
penpa_tags["options"]["puzzlink"].push("tslither (touch slitherlink)");
penpa_tags["options"]["puzzlink"].push("vslither (vertex slitherlink)");
penpa_tags["options"]["puzzlink"].push("nothree");
penpa_tags["options"]["puzzlink"].push("nuriuzu");
penpa_tags["options"]["puzzlink"].push("fivecells");
penpa_tags["options"]["puzzlink"].push("fourcells");
penpa_tags["options"]["puzzlink"].push("circlesquare");
penpa_tags["options"]["puzzlink"].push("creek");
penpa_tags["options"]["puzzlink"].push("nibunnogo");
penpa_tags["options"]["puzzlink"].push("arukone");
penpa_tags["options"]["puzzlink"].push("coral");
penpa_tags["options"]["puzzlink"].push("cross the streams");
penpa_tags["options"]["puzzlink"].push("japanesesums");
penpa_tags["options"]["puzzlink"].push("simplegako");
penpa_tags["options"]["puzzlink"].push("dotchi-dotchi loop");
penpa_tags["options"]["puzzlink"].push("all or nothing");
penpa_tags["options"]["puzzlink"].push("tetrochain-Y");
penpa_tags["options"]["puzzlink"].push("aquarium");
penpa_tags["options"]["puzzlink"].push("box");
penpa_tags["options"]["puzzlink"].push("alternation");
penpa_tags["options"]["puzzlink"].push("hakoiri (Hakoiri-masashi)");
penpa_tags["options"]["puzzlink"].push("tontonbeya");
penpa_tags["options"]["puzzlink"].push("anglers");
penpa_tags["options"]["puzzlink"].push("doppelblock");
penpa_tags["options"]["puzzlink"].push("aquapelago");
penpa_tags["options"]["puzzlink"].push("barns");
penpa_tags["options"]["puzzlink"].push("battenberg painting");
penpa_tags["options"]["puzzlink"].push("border block");

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
    case "suguru":
      /* base on "cojun" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "number");

      info_edge = puzzlink_pu.decodeBorder();
      info_number = puzzlink_pu.decodeNumber16();

      puzzlink_pu.drawBorder(pu, info_edge, 2); // 2 is for Black Style
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("number");
      UserSettings.tab_settings = ["Surface", "Number Normal", "Sudoku Normal"];
      pu.user_tags = ["suguru (capsules)"];
      break;

    case "chocona":
    case "cocktail":
    case "heyablock":
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
      if (type === "cocktail") pu.user_tags = ["cocktail lamp"];
      else if (type === "mannequin") pu.user_tags = ["mannequin gate"];
      else pu.user_tags = [type];
      break;

    case "context":
    case "cityspace":
    case "norinuri":
    case "smullyan":
      /* base on "nuribou" type */

      pu = new Puzzle_square(cols, rows, size);
      if (type === "cityspace") {
        pu.mode_grid("nb_grid2"); // Dashed gridlines
        pu.mode_grid("nb_out2"); // No outside frame
      }

      setupProblem(pu, "surface");

      info_number = puzzlink_pu.decodeNumber16();
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("surface");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      if (type === "smullyan") pu.user_tags = ["smullyan (smullyanic dynasty)"];
      else pu.user_tags = [type];
      break;

    case "island":
    case "oasis":
      /* base on "nurimisaki" and "kurotto" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "combi");

      info_number = puzzlink_pu.decodeNumber16();
      puzzlink_pu.drawNumbers(pu, info_number, 6, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("blpo"); // Black square and Point
      UserSettings.tab_settings = ["Surface", "Composite"];
      if (type === "island") pu.user_tags = ["Inaba's island"];
      else pu.user_tags = ["oasis"];
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

      switch (type) {
        case "lither":
          pu.user_tags = ["lither (lithersink)"];
          break;
        case "tslither":
          pu.user_tags = ["tslither (touch slitherlink)"];
          break;
        case "vslither":
          pu.user_tags = ["vslither (vertex slitherlink)"];
          break;
      }
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
      pu.user_tags = [type];
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
      pu.user_tags = [type];
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
      pu.mode_set("combi");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = [type];
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
      pu.user_tags = [type];
      break;

    case "arukone":
    case "numlin_bit":
      /* base on "numlin" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "combi");

      info_number = puzzlink_pu.decodeNumber16();
      if (type === "arukone") {
        var row_ind, col_ind, cell, number;

        // Add numbers to grid
        for (var i in info_number) {
          // Determine which row and column
          row_ind = parseInt(i / cols);
          col_ind = i % cols;
          cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
          number = String.fromCharCode(64 + parseInt(info_number[i])); // convert to letters
          pu["pu_q"].number[cell] = [number, 1, "1"];
        }
      } else puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("linex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      if (type === "arukone") pu.user_tags = ["arukone"];
      break;

    case "coral":
    case "cts":
    case "japanesesums":
      /* base on "nonogram" type */

      if (type === "japanesesums") puzzlink_pu = new Puzzlink(cols, rows, urldata[4]); // intercept for extra number

      var max_cols_offset = Math.ceil(cols / 2);
      var max_rows_offset = Math.ceil(rows / 2);

      info_number = puzzlink_pu.decodeNumber16();
      var cols_offset = 0,
        rows_offset = 0;

      for (var i in info_number) {
        if (i < max_rows_offset * cols) {
          rows_offset = Math.max(rows_offset, parseInt(i % max_rows_offset) + 1);
        } else {
          cols_offset = Math.max(cols_offset, parseInt((i - max_rows_offset * cols) % max_cols_offset) + 1);
        }
      }

      document.getElementById("nb_space1").value = rows_offset;
      document.getElementById("nb_space3").value = cols_offset;

      pu = new Puzzle_square(cols + cols_offset, rows + rows_offset, size);
      setupProblem(pu, "combi");

      // Draw numbers
      for (i in info_number) {
        if (i < max_rows_offset * cols) {
          // Top section
          row_ind = rows_offset - (i % max_rows_offset) - 1;
          col_ind = cols_offset + parseInt(i / max_rows_offset);
        } else {
          // Left section
          row_ind = rows_offset + parseInt((i - max_rows_offset * cols) / max_cols_offset);
          col_ind = cols_offset - ((i - max_rows_offset * cols) % max_cols_offset) - 1;
        }
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].number[cell] = [info_number[i] === 0 && type === "cts" ? "*" : info_number[i], 1, "1"];
      }

      // Draw vertical edges
      for (i = cols_offset - 1; i < cols + cols_offset + 5; i += 5) {
        col_ind = Math.min(cols + cols_offset - 1, i);
        var edge_style = 13; // Fat dots
        if (col_ind === cols_offset - 1 || col_ind === cols + cols_offset - 1) {
          edge_style = 2; // Black normal
        }
        for (row_ind = 0; row_ind < rows + rows_offset; row_ind++) {
          var edgex = pu.nx0 * pu.ny0 + pu.nx0 * (1 + row_ind) + 1 + col_ind + 1;
          var edgey = edgex + pu.nx0;
          var key = edgex.toString() + "," + edgey.toString();
          pu["pu_q"]["lineE"][key] = edge_style;
        }
      }

      // Draw horizontal edges
      for (var i = rows_offset - 1; i < rows + rows_offset + 5; i += 5) {
        row_ind = Math.min(rows + rows_offset - 1, i);
        var edge_style = 13; // Fat dots
        if (row_ind === rows_offset - 1 || row_ind === rows + rows_offset - 1) {
          edge_style = 2; // Black normal
        }
        for (col_ind = 0; col_ind < cols + cols_offset; col_ind++) {
          var edgex = pu.nx0 * pu.ny0 + pu.nx0 * (2 + row_ind) + 1 + col_ind;
          var edgey = edgex + 1;
          var key = edgex.toString() + "," + edgey.toString();
          pu["pu_q"]["lineE"][key] = edge_style;
        }
      }

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      if (type === "cts") pu.user_tags = ["cross the streams"];
      else pu.user_tags = [type];
      break;

    case "simplegako":
      /* base on "view" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "number");

      info_number = puzzlink_pu.decodeNumber16();
      puzzlink_pu.drawNumbers(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("number");
      UserSettings.tab_settings = ["Surface", "Edge Normal", "Number Normal"];
      pu.user_tags = [type];
      break;

    case "dotchi2":
      /* base on "dotchi" type */

      pu = new Puzzle_square(cols, rows, size);
      pu.mode_grid("nb_grid2"); // Dashed gridlines
      setupProblem(pu, "combi");

      info_edge = puzzlink_pu.decodeBorder();
      puzzlink_pu.drawBorder(pu, info_edge, 2);

      // Draw Circles
      info_number = puzzlink_pu.decodeNumber3();
      for (i in info_number) {
        if (info_number[i] === 0) {
          continue;
        }
        // Determine which row and column
        row_ind = parseInt(i / cols);
        col_ind = i % cols;
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].symbol[cell] = [info_number[i], "circle_L", 1];
      }

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("linex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["dotchi-dotchi loop"];
      break;

    case "nothing":
      /* base on "moonsun" type */

      pu = new Puzzle_square(cols, rows, size);
      pu.mode_grid("nb_grid2"); // Dashed gridlines
      setupProblem(pu, "combi");

      info_edge = puzzlink_pu.decodeBorder();
      puzzlink_pu.drawBorder(pu, info_edge, 2);

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("linex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["all or nothing"];
      break;

    case "tetrochain":
      /* base on "yajikazu" type */

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "combi");

      var arrows = puzzlink_pu.decodeYajilinArrows(false);

      for (var i in arrows) {
        row_ind = parseInt(i / cols);
        col_ind = i % cols;
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        var number = arrows[i][1] || "?";

        // Not all numbers have arrows
        if (arrows[i][0] !== 0 && number) {
          switch (arrows[i][0]) {
            case 1: // up
              number += "_" + 0;
              break;
            case 2: // down
              number += "_" + 3;
              break;
            case 3: // left
              number += "_" + 1;
              break;
            case 4: // right
              number += "_" + 2;
              break;
          }
        }

        pu["pu_q"].number[cell] = [number, 1, "2"];
      }

      pu.mode_qa("pu_a");
      pu.mode_set("surface");
      UserSettings.tab_settings = ["Surface"];
      pu.user_tags = ["tetrochain-Y"];
      break;

    case "aquarium":
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space3").value = 1;

      pu = new Puzzle_square(cols + 1, rows + 1, size);
      setupProblem(pu, "combi");

      info_edge = puzzlink_pu.decodeBorder();
      drawBorderEx(puzzlink_pu, pu, info_edge, 2);

      puzzlink_nb = new Puzzlink(cols, rows, urldata[4]);
      info_number = puzzlink_nb.decodeNumber16ExCell(true);
      puzzlink_nb.drawNumbersExCell(pu, info_number, 1, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["aquarium"];
      break;

    case "box":
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space2").value = 1;
      document.getElementById("nb_space3").value = 1;
      document.getElementById("nb_space4").value = 1;

      pu = new Puzzle_square(cols + 2, rows + 2, size);
      setupProblem(pu, "number");

      [info_number1, info_number2] = decodeBox(puzzlink_pu);
      puzzlink_pu.drawNumbersExCell(pu, info_number1, 1, "1", false);
      puzzlink_pu.drawNumbersExCell(pu, info_number2, 6, "1", false);

      pu.mode_qa("pu_a");
      pu.mode_set("number");
      UserSettings.tab_settings = ["Surface", "Number Normal"];
      pu.user_tags = ["box"];
      break;

    case "alter":
    case "hakoiri":
    case "tontonbeya":
      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "symbol");

      info_edge = puzzlink_pu.decodeBorder();
      puzzlink_pu.drawBorder(pu, info_edge, 2);

      info_number = puzzlink_pu.decodeNumber10();
      for (i in info_number) {
        if (![1, 2, 3].includes(info_number[i])) continue;
        row_ind = parseInt(i / cols);
        col_ind = i % cols;
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].symbol[cell] = [info_number[i], "ox_B", 1];
      }

      pu.mode_qa("pu_a");
      pu.mode_set("symbol");
      UserSettings.tab_settings = ["Surface", "Shape"];

      switch (type) {
        case "alter":
          pu.user_tags = ["alternation"];
          break;
        case "hakoiri":
          pu.user_tags = ["hakoiri (Hakoiri-masashi)"];
          break;
        case "tontonbeya":
          pu.user_tags = ["tontonbeya"];
          break;
      }
      break;

    case "anglers":
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space2").value = 1;
      document.getElementById("nb_space3").value = 1;
      document.getElementById("nb_space4").value = 1;

      pu = new Puzzle_square(cols + 2, rows + 2, size);
      pu.mode_grid("nb_grid2"); // Dashed gridlines
      setupProblem(pu, "combi");

      [info_number1, info_number2, info_extra] = decodeAnglers(puzzlink_pu);
      puzzlink_pu.drawNumbersExCell(pu, info_number1, 1, "1", false);
      drawNumbersEx(puzzlink_pu, pu, info_number2, 1, "1", false);

      for (var i in info_extra) {
        row_ind = parseInt(i / cols) + 1; // top offset
        col_ind = (i % cols) + 1; // left offset
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        if (info_extra[i] === 0) {
          pu["pu_q"].symbol[cell] = [3, "tents", 1]; // fish symbol
        } else {
          pu["pu_q"].surface[cell] = 4; // shaded cell
        }
      }

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("linex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["anglers"];
      break;

    case "doppelblock":
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space3").value = 1;

      pu = new Puzzle_square(cols + 1, rows + 1, size);
      setupProblem(pu, "number");

      info_number1 = puzzlink_pu.decodeNumber16ExCell(true);
      info_number2 = puzzlink_pu.decodeNumber16();
      puzzlink_pu.drawNumbersExCell(pu, info_number1, 1, "1");
      drawNumbersEx(puzzlink_pu, pu, info_number2, 1, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("number");
      UserSettings.tab_settings = ["Surface", "Number Normal"];
      pu.user_tags = ["doppelblock"];
      break;

    case "aquapelago":
      /* base on "akari" type */
      info_number = puzzlink_pu.decodeNumber16();

      pu = new Puzzle_square(cols, rows, size);
      setupProblem(pu, "combi");
      puzzlink_pu.drawNumbers(pu, info_number, 7, "1");

      // Draw black behind numbers
      for (i in info_number) {
        // Determine which row and column
        row_ind = parseInt(i / cols);
        col_ind = i % cols;
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].surface[cell] = 4;
      }

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("blpo");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["aquapelago"];
      break;

    case "barns":
      pu = new Puzzle_square(cols, rows, size);
      pu.mode_grid("nb_grid2"); // Dashed gridlines
      setupProblem(pu, "combi");

      // Draw icy cells
      info_number = puzzlink_pu.decodeNumber2Binary(puzzlink_pu.rows * puzzlink_pu.cols);
      for (i in info_number) {
        if (info_number[i] === 0) {
          continue;
        }
        row_ind = parseInt(i / cols);
        col_ind = i % cols;
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].surface[cell] = 5;
      }

      info_edge = puzzlink_pu.decodeBorder();
      puzzlink_pu.drawBorder(pu, info_edge, 2); // 2 is for Black Style

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("linex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["barns"];
      break;

    case "batten":
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space3").value = 1;

      pu = new Puzzle_square(cols + 1, rows + 1, size);
      setupProblem(pu, "combi");

      info_crossmark = decodeCrossMark(puzzlink_pu, false);
      for (i in info_crossmark) {
        row_ind = parseInt(i / (cols - 1)) + 1; // border shrink + offset
        col_ind = (i % (cols - 1)) + 1; // border shrink + offset
        cell = pu.nx0 * pu.ny0 + pu.nx0 * (2 + row_ind) + 2 + col_ind;
        if (info_crossmark[i] === 1) {
          pu["pu_q"].symbol[cell] = [1, "sudokuetc", 2];
        }
      }

      info_number = puzzlink_pu.decodeNumber16ExCell(true);
      puzzlink_pu.drawNumbersExCell(pu, info_number, 1, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("linex");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["battenberg painting"];
      break;

    case "bdblock":
      pu = new Puzzle_square(cols, rows, size);
      pu.mode_grid("nb_grid2"); // Dashed gridlines
      setupProblem(pu, "combi");

      info_crossmark = decodeCrossMark(puzzlink_pu, true);
      for (i in info_crossmark) {
        row_ind = parseInt(i / (cols + 1)) - 1; // border expand
        col_ind = (i % (cols + 1)) - 1; // border expand
        cell = pu.nx0 * pu.ny0 + pu.nx0 * (2 + row_ind) + 2 + col_ind;
        if (info_crossmark[i] === 1) {
          pu["pu_q"].symbol[cell] = [2, "circle_SS", 2];
        }
      }

      puzzlink_nb = new Puzzlink(cols, rows, urldata[4]);
      info_number = puzzlink_nb.decodeNumber16();
      puzzlink_nb.drawNumbers(pu, info_number, 1, "1");

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("edgesub");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["border block"];
      break;

    case "battleship":
      document.getElementById("nb_space1").value = 1;
      document.getElementById("nb_space3").value = 1;

      pu = new Puzzle_square(cols + 1, rows + 1, size);
      setupProblem(pu, "combi");

      info_exnumber = puzzlink_pu.decodeNumber16ExCell(true);
      puzzlink_pu.drawNumbersExCell(pu, info_exnumber, 1, "1", true);

      info_number = puzzlink_pu.decodeNumber16();
      const ship_map = [7, 4, 6, 3, 5, 2, 1];

      for (i in info_number) {
        row_ind = parseInt(i / cols) + 1; // row offset
        col_ind = (i % cols) + 1; // column offset
        cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
        pu["pu_q"].symbol[cell] = [ship_map[info_number[i]], "battleship_B", 1];
      }

      pu.mode_qa("pu_a");
      pu.mode_set("combi");
      pu.subcombimode("battleship");
      UserSettings.tab_settings = ["Surface", "Composite"];
      pu.user_tags = ["battleship"];
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

function decodeBox(puzzlink_pu) {
  var number_list1 = {};
  var number_list2 = {};
  var ec = 0,
    i = 0;
  var skipped_bottom = false;

  for (var i = 0; i < puzzlink_pu.gridurl.length; i++) {
    var ca = puzzlink_pu.gridurl.charAt(i);
    if (ca === "-") {
      number_list1[ec] = parseInt(puzzlink_pu.gridurl.substr(i + 1, 2), 32);
      i += 2;
    } else {
      number_list1[ec] = parseInt(ca, 32);
    }

    ec++;
    if (!skipped_bottom && ec >= puzzlink_pu.cols) {
      skipped_bottom = true;
      // append numbers for bottom row
      for (var j = 0; j < puzzlink_pu.cols; j++) number_list2[ec + j] = j + 1;
      ec += puzzlink_pu.cols;
    }

    if (ec >= 2 * puzzlink_pu.cols + puzzlink_pu.rows) {
      // append numbers for rightmost column
      for (var j = 0; j < puzzlink_pu.rows; j++) number_list2[ec + j] = j + 1;
      ec += puzzlink_pu.rows;
    }

    if (ec >= puzzlink_pu.rows * 2 + puzzlink_pu.cols * 2) {
      break; // Finished all four sides
    }
  }

  return [number_list1, number_list2];
}

function decodeAnglers(puzzlink_pu) {
  /* a variant of decodeNumber16 / decodeNumber16ExCell */

  var number_list1 = {};
  var number_list2 = {};
  var extra_list = {};
  var i = 0;
  var c = 0;
  const clen = puzzlink_pu.cols * puzzlink_pu.rows;

  while (i < puzzlink_pu.gridurl.length) {
    var ca = puzzlink_pu.gridurl.charAt(i);
    var res = puzzlink_pu.readNumber16(ca, i);
    if (res[0] !== -1) {
      var val = res[0] === 0 ? -3 : res[0] > 0 ? res[0] - 1 : res[0];

      if (val === 0 || val === -3) {
        extra_list[c] = val; // fish or shaded cells must be inside of the grid
      } else {
        if (c >= clen) {
          number_list1[c - clen] = val; // numbers outside of the grid
        } else {
          number_list2[c] = val; // numbers inside the grid
        }
      }

      i += res[1];
      c++;
    } else if (ca >= "g" && ca <= "z") {
      c += parseInt(ca, 36) - 15;
      i++;
    } else {
      i++;
    }
  }

  // Remove what was parsed so the next function call reads what is left
  puzzlink_pu.gridurl = puzzlink_pu.gridurl.substr(i);

  return [number_list1, number_list2, extra_list];
}

function decodeCrossMark(puzzlink_pu, hasborder = true) {
  var cc = 0,
    i = 0,
    crossmark_list = {};
  var cp = hasborder ? 1 : 0,
    cp2 = cp << 1;
  var rows = puzzlink_pu.rows - 1 + cp2,
    cols = puzzlink_pu.cols - 1 + cp2;

  for (i = 0; i < puzzlink_pu.gridurl.length; i++) {
    var ca = puzzlink_pu.gridurl.charAt(i);

    if (puzzlink_pu.include(ca, "0", "9") || puzzlink_pu.include(ca, "a", "z")) {
      cc += parseInt(ca, 36);
      if (cc >= cols * rows) {
        i++;
        break;
      }
      crossmark_list[cc] = 1;
    } else if (ca === ".") {
      cc += 35;
    }

    cc++;
    if (cc >= cols * rows) {
      i++;
      break;
    }
  }

  // Remove what was parsed so the next function call reads what is left
  puzzlink_pu.gridurl = puzzlink_pu.gridurl.substr(i);
  return crossmark_list;
}

function drawBorderEx(puzzlink_pu, pu, info_edge, edge_style) {
  /* handles the drawing of borders with an offset
     mergable with the original drawBorder function in the future
  */

  var row_ind, col_ind, edgex, edgey;
  var row_offset = pu.space[0];
  var col_offset = pu.space[2];

  // Add edges to grid
  for (var i in info_edge) {
    if (info_edge[i] === 1) {
      // Determine Vertical Border or Horizontal
      if (i < (puzzlink_pu.cols - 1) * puzzlink_pu.rows) {
        row_ind = parseInt(i / (puzzlink_pu.cols - 1)) + row_offset;
        col_ind = (i % (puzzlink_pu.cols - 1)) + col_offset;
        // plus 1 at end because the 0 reference is from column 1 due to inside border
        edgex = pu.nx0 * pu.ny0 + pu.nx0 * (1 + row_ind) + 1 + col_ind + 1;
        edgey = edgex + pu.nx0;
      } else {
        i -= (puzzlink_pu.cols - 1) * puzzlink_pu.rows; //offset to 0
        row_ind = parseInt(i / puzzlink_pu.cols) + row_offset;
        col_ind = (i % puzzlink_pu.cols) + col_offset;
        // 2 + row_ind, as 1st horizontal is the 0 reference
        edgex = pu.nx0 * pu.ny0 + pu.nx0 * (2 + row_ind) + 1 + col_ind;
        edgey = edgex + 1;
      }
      var key = edgex.toString() + "," + edgey.toString();
      pu["pu_q"]["lineE"][key] = edge_style;
    }
  }
}

function drawNumbersEx(puzzlink_pu, pu, info_number, style, sub_mode, hide_ques = true) {
  /* handles the drawing of borders with an offset
     mergable with the original drawNumber function in the future
  */

  var row_ind, col_ind, cell, number;
  var row_offset = pu.space[0];
  var col_offset = pu.space[2];

  // Add numbers to grid
  for (var i in info_number) {
    // Determine which row and column
    row_ind = parseInt(i / puzzlink_pu.cols) + row_offset;
    col_ind = (i % puzzlink_pu.cols) + col_offset;
    cell = pu.nx0 * (2 + row_ind) + 2 + col_ind;
    number = hide_ques && info_number[i] === "?" ? " " : info_number[i];
    pu["pu_q"].number[cell] = [number, style, sub_mode];
  }
}
