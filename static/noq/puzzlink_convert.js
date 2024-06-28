// FileData.js from pzprjs

class FileIO {
  throwNoImplementation() {
    throw Error("no implementation");
  }

  constructor() {
    this.filever = 0;
    this.lineseek = 0;
    this.dataarray = null;
    this.xmldoc = null;
    this.datastr = "";
    this.currentType = 0;

    // オーバーライド用
    this.decodeData = this.throwNoImplementation;
    this.encodeData = this.throwNoImplementation;
    this.kanpenOpen = this.throwNoImplementation;
    this.kanpenSave = this.throwNoImplementation;
    this.kanpenOpenXML = this.throwNoImplementation;
    this.kanpenSaveXML = this.throwNoImplementation;

    this.PBOX_ADJUST = 0;

    this.UNDECIDED_NUM_XML = -1;
  }
  //---------------------------------------------------------------------------
  // fio.filedecode()  decode from file
  //---------------------------------------------------------------------------
  filedecode(datastr) {
    var puzzle = this.puzzle,
      bd = puzzle.board,
      pzl = pzpr.parser.parseFile(datastr, puzzle.pid); // wwwwww
    var filetype = (this.currentType = pzl.type);

    bd.initBoardSize(pzl.cols, pzl.rows);

    this.filever = pzl.filever;
    if (filetype !== pzl.FILE_PBOX_XML) {
      this.lineseek = 0;
      this.dataarray = pzl.body.split("\n");
    } else {
      this.xmldoc = pzl.body;
    }

    // メイン処理
    switch (filetype) {
      case pzl.FILE_PZPR:
        this.decodeData();
        if ((this.readLine() || "").match(/TrialData/)) {
          this.lineseek--;
          this.decodeTrial();
        }
        break;

      case pzl.FILE_PBOX:
        this.kanpenOpen();
        break;

      case pzl.FILE_PBOX_XML:
        this.kanpenOpenXML();
        break;
    }

    puzzle.metadata.update(pzl.metadata);
    if (pzl.history && filetype === pzl.FILE_PZPR) {
      puzzle.opemgr.decodeHistory(pzl.history);
    }

    bd.rebuildInfo();

    this.dataarray = null;
  }

  static puzzlink_convert_processes(name) {
    let puzzlink_convert_processes = {
      aqre: ["aqre", ["AreaRoom", "CellQnum", "CellAns"]],
    };
    return puzzlink_convert_processes[name];
  }

  //---------------------------------------------------------------------------
  // fio.fileencode()  encode to file
  //---------------------------------------------------------------------------
  fileencode(board, solution) {
    board.rows = board.param_values.r;
    board.cols = board.param_values.c;
    this.board = board;
    this.solution = solution;
    this.datastr = "";
    let name = board.puzzle_type;

    const [name1, funcname_seq] = FileIO.puzzlink_convert_processes(name);
    // console.log(board);
    // console.log(solution);
    for (let func_name of funcname_seq) {
      let func = this["encode" + func_name].bind(this);
      // console.log("encode" + func_name);
      this.encoding_ans = func_name.toLowerCase().includes("ans");
      func();
    }
    let result =
      `pzprv3\n${name}\n${board.rows}\n${board.cols}\n` + this.datastr;
    return result;

    var pzl = new pzpr.parser.FileData("", puzzle.pid);

    this.currentType = filetype =
      filetype || pzl.FILE_PZPR; /* type===pzl.FILE_AUTO(0)もまとめて変換する */
    option = option || {};

    this.filever = 0;
    this.datastr = "";

    this.encodeData();

    pzl.type = filetype;
    pzl.filever = this.filever;
    pzl.cols = board.cols;
    pzl.rows = board.rows;
    pzl.body = this.datastr;
    pzl.metadata.update(puzzle.metadata);
    if (option.history && filetype === pzl.FILE_PZPR) {
      pzl.history = puzzle.opemgr.encodeHistory({ time: !!option.time });
    }

    return pzl.generate();
  }

  //---------------------------------------------------------------------------
  // fio.readLine()    ファイルに書かれている1行の文字列を返す
  // fio.getItemList() ファイルに書かれている改行＋スペース区切りの
  //                   複数行の文字列を配列にして返す
  //---------------------------------------------------------------------------
  readLine() {
    this.lineseek++;
    return this.dataarray[this.lineseek - 1];
  }

  getItemList(rows) {
    var item = [],
      line;
    for (var i = 0; i < rows; i++) {
      if (!(line = this.readLine())) {
        continue;
      }
      var array1 = line.split(" ");
      for (var c = 0; c < array1.length; c++) {
        if (array1[c] !== "") {
          item.push(array1[c]);
        }
      }
    }
    return item;
  }

  //---------------------------------------------------------------------------
  // fio.writeLine()    ファイルに1行出力する
  //---------------------------------------------------------------------------
  writeLine(data) {
    if (typeof data === "number") {
      data = "" + data;
    } else {
      data = data || "";
    } // typeof data==='string'
    this.datastr += data + "\n";
  }

  //---------------------------------------------------------------------------
  // fio.decodeObj()     配列で、個別文字列から個別セルなどの設定を行う
  // fio.decodeCell()    配列で、個別文字列から個別セルの設定を行う
  // fio.decodeCross()   配列で、個別文字列から個別Crossの設定を行う
  // fio.decodeBorder()  配列で、個別文字列から個別Borderの設定を行う
  // fio.decodeCellExCell()  配列で、個別文字列から個別セル/ExCellの設定を行う
  //---------------------------------------------------------------------------
  decodeObj(func, group, startbx, startby, endbx, endby) {
    var bx = startbx,
      by = startby,
      step = 2;
    var item = this.getItemList((endby - startby) / step + 1);
    for (var i = 0; i < item.length; i++) {
      func.call(this, this.board.getObjectPos(group, bx, by), item[i]);

      bx += step;
      if (bx > endbx) {
        bx = startbx;
        by += step;
      }
      if (by > endby) {
        break;
      }
    }
  }
  decodeCell(func) {
    this.decodeObj(
      func,
      "cell",
      1,
      1,
      2 * this.board.cols - 1,
      2 * this.board.rows - 1
    );
  }
  decodeCross(func) {
    this.decodeObj(
      func,
      "cross",
      0,
      0,
      2 * this.board.cols,
      2 * this.board.rows
    );
  }
  decodeBorder(func, hasborder) {
    var puzzle = this.puzzle,
      bd = puzzle.board;
    if (!hasborder) {
      hasborder = bd.hasborder;
    }
    if (hasborder === 1) {
      this.decodeObj(func, "border", 2, 1, 2 * bd.cols - 2, 2 * bd.rows - 1);
      this.decodeObj(func, "border", 1, 2, 2 * bd.cols - 1, 2 * bd.rows - 2);
    } else if (hasborder === 2) {
      if (this.currentType === pzpr.parser.FILE_PZPR) {
        this.decodeObj(func, "border", 0, 1, 2 * bd.cols, 2 * bd.rows - 1);
        this.decodeObj(func, "border", 1, 0, 2 * bd.cols - 1, 2 * bd.rows);
      }
      // pencilboxでは、outsideborderの時はぱずぷれとは順番が逆になってます
      else if (this.currentType === pzpr.parser.FILE_PBOX) {
        this.decodeObj(func, "border", 1, 0, 2 * bd.cols - 1, 2 * bd.rows);
        this.decodeObj(func, "border", 0, 1, 2 * bd.cols, 2 * bd.rows - 1);
      }
    }
  }
  decodeCellExCell(func) {
    this.decodeObj(
      func,
      "obj",
      this.board.minbx + 1,
      this.board.minby + 1,
      this.board.maxbx - 1,
      this.board.maxby - 1
    );
  }

  //---------------------------------------------------------------------------
  // fio.encodeObj()     個別セルデータ等から個別文字列の設定を行う
  // fio.encodeCell()    個別セルデータから個別文字列の設定を行う
  // fio.encodeCross()   個別Crossデータから個別文字列の設定を行う
  // fio.encodeBorder()  個別Borderデータから個別文字列の設定を行う
  // fio.encodeCellExCell()  個別セル/ExCellデータから個別文字列の設定を行う
  //---------------------------------------------------------------------------
  encodeObj(func, group, startbx, startby, endbx, endby) {
    let step = 2;
    for (let by = startby; by <= endby; by += step) {
      let data = "";
      for (let bx = startbx; bx <= endbx; bx += step) {
        let grid = this.encoding_ans ? this.solution : this.board.grid;
        data += func.call(this, grid[`${bx},${by}`]);
      }
      this.writeLine(data);
    }
  }
  encodeCell(func) {
    this.encodeObj(
      func,
      "cell",
      1,
      1,
      2 * this.board.cols - 1,
      2 * this.board.rows - 1
    );
  }
  encodeCross(func) {
    this.encodeObj(
      func,
      "cross",
      0,
      0,
      2 * this.board.cols,
      2 * this.board.rows
    );
  }
  encodeBorder(func, hasborder) {
    var puzzle = this.puzzle,
      bd = puzzle.board;
    if (!hasborder) {
      hasborder = bd.hasborder;
    }
    if (hasborder === 1) {
      this.encodeObj(func, "border", 2, 1, 2 * bd.cols - 2, 2 * bd.rows - 1);
      this.encodeObj(func, "border", 1, 2, 2 * bd.cols - 1, 2 * bd.rows - 2);
    } else if (hasborder === 2) {
      if (this.currentType === pzpr.parser.FILE_PZPR) {
        this.encodeObj(func, "border", 0, 1, 2 * bd.cols, 2 * bd.rows - 1);
        this.encodeObj(func, "border", 1, 0, 2 * bd.cols - 1, 2 * bd.rows);
      }
      // pencilboxでは、outsideborderの時はぱずぷれとは順番が逆になってます
      else if (this.currentType === pzpr.parser.FILE_PBOX) {
        this.encodeObj(func, "border", 1, 0, 2 * bd.cols - 1, 2 * bd.rows);
        this.encodeObj(func, "border", 0, 1, 2 * bd.cols, 2 * bd.rows - 1);
      }
    }
  }
  encodeCellExCell(func) {
    this.encodeObj(
      func,
      "obj",
      this.board.minbx + 1,
      this.board.minby + 1,
      this.board.maxbx - 1,
      this.board.maxby - 1
    );
  }

  //---------------------------------------------------------------------------
  // fio.decodeCellQnum() 問題数字のデコードを行う
  // fio.encodeCellQnum() 問題数字のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellQnum() {
    this.decodeCell(function (cell, ca) {
      if (ca === "-") {
        cell.qnum = -2;
      } else if (ca !== ".") {
        cell.qnum = +ca;
      }
    });
  }
  encodeCellQnum() {
    this.encodeCell(function (num) {
      if (num >= 0) {
        return num + " ";
      } else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellQnumb() 黒背景な問題数字のデコードを行う
  // fio.encodeCellQnumb() 黒背景な問題数字のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellQnumb() {
    this.decodeCell(function (cell, ca) {
      if (ca === "5") {
        cell.qnum = -2;
      } else if (ca !== ".") {
        cell.qnum = +ca;
      }
    });
  }
  encodeCellQnumb() {
    this.encodeCell(function (cell) {
      if (cell.qnum >= 0) {
        return cell.qnum + " ";
      } else if (cell.qnum === -2) {
        return "5 ";
      } else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellQnumAns() 問題数字＋黒マス白マスのデコードを行う
  // fio.encodeCellQnumAns() 問題数字＋黒マス白マスのエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellQnumAns() {
    this.decodeCell(function (cell, ca) {
      if (ca === "#") {
        cell.qans = 1;
      } else if (ca === "+") {
        cell.qsub = 1;
      } else if (ca === "-") {
        cell.qnum = -2;
      } else if (ca !== ".") {
        cell.qnum = +ca;
      }
    });
  }
  encodeCellQnumAns() {
    this.encodeCell(function (cell) {
      if (cell.qnum >= 0) {
        return cell.qnum + " ";
      } else if (cell.qnum === -2) {
        return "- ";
      } else if (cell.qans === 1) {
        return "# ";
      } else if (cell.qsub === 1) {
        return "+ ";
      } else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellDirecQnum() 方向＋問題数字のデコードを行う
  // fio.encodeCellDirecQnum() 方向＋問題数字のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellDirecQnum() {
    this.decodeCell(function (cell, ca) {
      if (ca === "#") {
        cell.qdir = 0;
        cell.qnum = -3;
      } else if (ca !== ".") {
        var inp = ca.split(",");
        cell.qdir = inp[0] !== "0" ? +inp[0] : 0;
        cell.qnum = inp[1] !== "-" ? +inp[1] : -2;
      }
    });
  }
  encodeCellDirecQnum() {
    this.encodeCell(function (cell) {
      if (cell.qnum === -3) {
        return "# ";
      } else if (cell.qnum !== -1) {
        var ca1 = cell.qdir !== 0 ? "" + cell.qdir : "0";
        var ca2 = cell.qnum !== -2 ? "" + cell.qnum : "-";
        return [ca1, ",", ca2, " "].join("");
      } else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellAns() 黒マス白マスのデコードを行う
  // fio.encodeCellAns() 黒マス白マスのエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellAns() {
    this.decodeCell(function (cell, ca) {
      if (ca === "#") {
        cell.qans = 1;
      } else if (ca === "+") {
        cell.qsub = 1;
      }
    });
  }
  encodeCellAns() {
    this.encodeCell(function (num) {
      if (num === 1) {
        //cell.qans, 不知道是啥
        return "# ";
      } /*else if (cell.qsub === 1) {
        return "+ ";
      }*/ else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellQanssub() 黒マスと背景色のデコードを行う
  // fio.encodeCellQanssub() 黒マスと背景色のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellQanssub() {
    this.decodeCell(function (cell, ca) {
      if (ca === "+") {
        cell.qsub = 1;
      } else if (ca === "-") {
        cell.qsub = 2;
      } else if (ca === "=") {
        cell.qsub = 3;
      } else if (ca === "%") {
        cell.qsub = 4;
      } else if (ca !== ".") {
        cell.qans = +ca;
      }
    });
  }
  encodeCellQanssub() {
    this.encodeCell(function (cell) {
      if (cell.qans !== 0) {
        return cell.qans + " ";
      } else if (cell.qsub === 1) {
        return "+ ";
      } else if (cell.qsub === 2) {
        return "- ";
      } else if (cell.qsub === 3) {
        return "= ";
      } else if (cell.qsub === 4) {
        return "% ";
      } else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellAnumsub() 回答数字と背景色のデコードを行う
  // fio.encodeCellAnumsub() 回答数字と背景色のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellAnumsub() {
    this.decodeCell(function (cell, ca) {
      if (cell.enableSubNumberArray && ca.indexOf("[") >= 0) {
        ca = this.setCellSnum(cell, ca);
      }
      if (ca === "+") {
        cell.qsub = 1;
      } else if (ca === "-") {
        cell.qsub = 2;
      } else if (ca === "=") {
        cell.qsub = 3;
      } else if (ca === "%") {
        cell.qsub = 4;
      } else if (ca !== ".") {
        cell.anum = +ca;
      }
    });
  }
  encodeCellAnumsub() {
    this.encodeCell(function (cell) {
      var ca = ".";
      if (cell.anum !== -1) {
        ca = "" + cell.anum;
      } else if (cell.qsub === 1) {
        ca = "+";
      } else if (cell.qsub === 2) {
        ca = "-";
      } else if (cell.qsub === 3) {
        ca = "=";
      } else if (cell.qsub === 4) {
        ca = "%";
      } else {
        ca = ".";
      }
      if (cell.enableSubNumberArray && cell.anum === -1) {
        ca += this.getCellSnum(cell);
      }
      return ca + " ";
    });
  }
  //---------------------------------------------------------------------------
  // fio.setCellSnum() 補助数字のデコードを行う   (decodeCellAnumsubで内部的に使用)
  // fio.getCellSnum() 補助数字のエンコードを行う (encodeCellAnumsubで内部的に使用)
  //---------------------------------------------------------------------------
  setCellSnum(cell, ca) {
    var snumtext = ca.substring(ca.indexOf("[") + 1, ca.indexOf("]"));
    var list = snumtext.split(/,/);
    for (var i = 0; i < list.length; ++i) {
      cell.snum[i] = !!list[i] ? +list[i] : -1;
    }
    return ca.substr(0, ca.indexOf("["));
  }
  getCellSnum(cell) {
    var list = [];
    for (var i = 0; i < cell.snum.length; ++i) {
      list[i] = cell.snum[i] !== -1 ? "" + cell.snum[i] : "";
    }
    var snumtext = list.join(",");
    return snumtext !== ",,," ? "[" + snumtext + "]" : "";
  }
  decodeCellSnum() {
    this.decodeCell(function (cell, ca) {
      ca = this.setCellSnum(cell, ca);
    });
  }
  encodeCellSnum(isforce) {
    if (!isforce) {
      var found = false;
      var cells = this.board.cell;

      for (var c = 0; c < cells.length && !found; c++) {
        var cell = cells[c];
        for (var i = 0; i < cell.snum.length; ++i) {
          if (cell.snum[i] !== -1) {
            found = true;
          }
        }
      }
      if (!found) {
        return;
      }
    }
    this.encodeCell(function (cell) {
      var ca = this.getCellSnum(cell);
      if (ca) {
        return ca + " ";
      }
      return ". ";
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellQsub() 背景色のデコードを行う
  // fio.encodeCellQsub() 背景色のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellQsub() {
    this.decodeCell(function (cell, ca) {
      if (ca !== "0") {
        cell.qsub = +ca;
      }
    });
  }
  encodeCellQsub() {
    this.encodeCell(function (cell) {
      if (cell.qsub > 0) {
        return cell.qsub + " ";
      } else {
        return "0 ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeCrossNum() 交点の数字のデコードを行う
  // fio.encodeCrossNum() 交点の数字のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCrossNum() {
    this.decodeCross(function (cross, ca) {
      if (ca === "-") {
        cross.qnum = -2;
      } else if (ca !== ".") {
        cross.qnum = +ca;
      }
    });
  }
  encodeCrossNum() {
    this.encodeCross(function (cross) {
      if (cross.qnum >= 0) {
        return cross.qnum + " ";
      } else if (cross.qnum === -2) {
        return "- ";
      } else {
        return ". ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeBorderQues() 問題の境界線のデコードを行う
  // fio.encodeBorderQues() 問題の境界線のエンコードを行う
  //---------------------------------------------------------------------------
  decodeBorderQues() {
    this.decodeBorder(function (border, ca) {
      if (ca === "1") {
        border.ques = 1;
      }
    });
  }
  encodeBorderQues() {
    this.encodeBorder(function (border) {
      return (border.ques === 1 ? "1" : "0") + " ";
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeBorderAns() 問題・回答の境界線のデコードを行う
  // fio.encodeBorderAns() 問題・回答の境界線のエンコードを行う
  // fio.decodeBorderArrowAns() Decode lines and dir. aux. marks
  // fio.encodeBorderArrowAns() Encode lines and dir. aux. marks
  //---------------------------------------------------------------------------
  decodeBorderAns(hasborder) {
    this.decodeBorder(function (border, ca) {
      if (ca === "2") {
        border.qans = 1;
        border.qsub = 1;
      } else if (ca === "1") {
        border.qans = 1;
      } else if (ca === "-1") {
        border.qsub = 1;
      }
    }, hasborder);
  }
  encodeBorderAns(hasborder) {
    this.encodeBorder(function (border) {
      if (border.qans === 1 && border.qsub === 1) {
        return "2 ";
      } else if (border.qans === 1) {
        return "1 ";
      } else if (border.qsub === 1) {
        return "-1 ";
      } else {
        return "0 ";
      }
    }, hasborder);
  }
  decodeBorderArrowAns() {
    this.decodeBorder(function (border, ca) {
      var lca = ca.charAt(ca.length - 1);
      if (lca >= "a" && lca <= "z") {
        if (lca === "u") {
          border.qsub = 11;
        } else if (lca === "d") {
          border.qsub = 12;
        } else if (lca === "l") {
          border.qsub = 13;
        } else if (lca === "r") {
          border.qsub = 14;
        }
        ca = ca.substr(0, ca.length - 1);
      }

      if (ca !== "" && ca !== "0") {
        if (ca.charAt(0) === "-") {
          border.line = -ca - 1;
          border.qsub = 2;
        } else {
          border.line = +ca;
        }
      }
    });
  }
  encodeBorderArrowAns() {
    this.encodeBorder(function (border) {
      var ca = "";
      if (border.qsub === 2) {
        ca += "" + (-1 - border.line);
      } else if (border.line > 0) {
        ca += "" + border.line;
      }

      if (border.qsub >= 11) {
        ca += ["u", "d", "l", "r"][border.qsub - 11];
      }

      return ca !== "" ? ca + " " : "0 ";
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeBorderLine() Lineのデコードを行う
  // fio.encodeBorderLine() Lineのエンコードを行う
  //---------------------------------------------------------------------------
  decodeBorderLine() {
    this.decodeBorder(function (border, ca) {
      if (ca === "-1") {
        border.qsub = 2;
      } else if (ca !== "0") {
        border.line = +ca;
      }
    });
  }
  encodeBorderLine() {
    this.encodeBorder(function (border) {
      if (border.line > 0) {
        return border.line + " ";
      } else if (border.qsub === 2) {
        return "-1 ";
      } else {
        return "0 ";
      }
    });
  }
  //---------------------------------------------------------------------------
  // fio.decodeAreaRoom() 部屋のデコードを行う
  // fio.encodeAreaRoom() 部屋のエンコードを行う
  //---------------------------------------------------------------------------
  decodeAreaRoom() {
    this.readLine();
    this.rdata2Border(true, this.getItemList(this.board.rows));

    this.board.roommgr.rebuild();
  }
  encodeAreaRoom() {
    let board = this.board;
    let r = board.param_values.r,
      c = board.param_values.c,
      dxy = [
        [-1, 0],
        [0, -1],
        [1, 0],
        [0, 1],
      ];
    let area_room = Array.from({ length: r }, () =>
      Array.from({ length: c }, () => 0)
    );
    let visited = Array.from({ length: r }, () =>
      Array.from({ length: c }, () => false)
    );
    let cnt = 0;
    for (let i = 0; i < r; i++) {
      for (let j = 0; j < c; j++)
        if (!visited[i][j]) {
          let Q = [[i, j]],
            front = 0;
          while (front < Q.length) {
            let [x, y] = Q[front];
            visited[x][y] = true;
            area_room[x][y] = cnt;
            for (let [dx, dy] of dxy) {
              let x1 = x + dx,
                y1 = y + dy;
              if (
                x1 >= 0 &&
                x1 < r &&
                y1 >= 0 &&
                y1 < c &&
                !(`${x + x1 + 1},${y + y1 + 1}` in board.grid) &&
                !visited[x1][y1]
              )
                Q.push([x1, y1]);
            }
            front++;
          }
          cnt++;
        }
    }
    this.writeLine(cnt);
    for (let i = 0; i < r; i++) {
      let data = "";
      for (let j = 0; j < c; j++)
        data += (area_room[i][j] >= 0 ? area_room[i][j] : ".") + " ";
      this.writeLine(data);
    }
  }
  //---------------------------------------------------------------------------
  // fio.rdata2Border() 入力された配列から境界線を入力する
  //---------------------------------------------------------------------------
  rdata2Border(isques, rdata) {
    var bd = this.board;
    for (var id = 0; id < bd.border.length; id++) {
      var border = bd.border[id],
        cell1 = border.sidecell[0],
        cell2 = border.sidecell[1];
      var isdiff =
        !cell1.isnull && !cell2.isnull && rdata[cell1.id] !== rdata[cell2.id];
      border[isques ? "ques" : "qans"] = isdiff ? 1 : 0;
    }
  }
  //---------------------------------------------------------------------------
  // fio.decodeCellQnum51() [＼]のデコードを行う
  // fio.encodeCellQnum51() [＼]のエンコードを行う
  //---------------------------------------------------------------------------
  decodeCellQnum51() {
    var bd = this.board;
    bd.disableInfo(); /* mv.set51cell()用 */
    this.decodeCellExCell(function (obj, ca) {
      if (ca === ".") {
        return;
      } else if (obj.group === "excell") {
        if (obj.bx !== -1 && obj.by === -1) {
          obj.qnum2 = +ca;
        } else if (obj.bx === -1 && obj.by !== -1) {
          obj.qnum = +ca;
        }
      } else if (obj.group === "cell") {
        var inp = ca.split(",");
        obj.set51cell();
        obj.qnum = +inp[0];
        obj.qnum2 = +inp[1];
      }
    });
    bd.enableInfo(); /* mv.set51cell()用 */
  }
  encodeCellQnum51() {
    this.encodeCellExCell(function (obj) {
      if (obj.group === "excell") {
        if (obj.bx === -1 && obj.by === -1) {
          return "0 ";
        }
        return (obj.by === -1 ? obj.qnum2 : obj.qnum) + " ";
      } else if (obj.group === "cell") {
        if (obj.ques === 51) {
          return obj.qnum + "," + obj.qnum2 + " ";
        }
      }
      return ". ";
    });
  }

  //---------------------------------------------------------------------------
  // fio.decodeDotFile() Decodes Cross/Cell/Border values and empty cells (ques===7)
  // fio.encodeDotFile() Encodes Cross/Cell/Border values and empty cells (ques===7)
  //---------------------------------------------------------------------------
  decodeDotFile() {
    var bd = this.board,
      s = 0,
      data = "";
    for (var i = 0, rows = 2 * bd.rows - 1; i < rows; i++) {
      data += this.readLine();
    }
    bd.disableInfo();
    for (var s = 0; s < data.length; ++s) {
      var dot = bd.dots[s],
        ca = data.charAt(s),
        num = +ca;
      if (num >= 1 && num <= 9) {
        dot.setDot(num);
      } else if (ca === "-") {
        dot.setDot(-2);
      } else if (ca === "X") {
        dot.piece.ques = 7;
      }
    }
    bd.enableInfo();
  }
  encodeDotFile() {
    var bd = this.board,
      s = 0;
    for (var by = 1; by <= 2 * bd.rows - 1; by++) {
      var data = "";
      for (var bx = 1; bx <= 2 * bd.cols - 1; bx++) {
        var dot = bd.dots[s];
        if (dot.getDot() >= 1 && dot.getDot() <= 9) {
          data += dot.getDot();
        } else if (dot.piece.ques === 7) {
          data += "X";
        } else if (dot.getDot() === -2) {
          data += "-";
        } else {
          data += ".";
        }
        s++;
      }
      this.writeLine(data);
    }
  }

  //---------------------------------------------------------------------------
  // fio.decodeQnums() Decode cells with qnums list
  // fio.encodeQnums() Encode cells with qnums list
  //---------------------------------------------------------------------------
  decodeQnums() {
    this.decodeCell(function (cell, ca) {
      if (ca !== ".") {
        cell.qnums = [];
        var array = ca.split(/,/);
        for (var i = 0; i < array.length; i++) {
          cell.qnums.push(array[i] !== "-" ? +array[i] : -2);
        }
      }
    });
  }
  encodeQnums() {
    this.encodeCell(function (cell) {
      if (cell.qnums.length > 0) {
        var array = [];
        for (var i = 0; i < cell.qnums.length; i++) {
          array.push(cell.qnums[i] >= 0 ? "" + cell.qnums[i] : "-");
        }
        return array.join(",") + " ";
      } else {
        return ". ";
      }
    });
  }

  //---------------------------------------------------------------------------
  // fio.decodePieceBank() Decode piece bank preset/custom
  // fio.encodePieceBank() Encode piece bank preset/custom
  //---------------------------------------------------------------------------
  decodePieceBank() {
    var bank = this.board.bank;
    var head = this.readLine();
    if (isNaN(head)) {
      for (var i = 0; i < bank.presets.length; i++) {
        if (bank.presets[i].shortkey === head) {
          bank.initialize(bank.presets[i].constant);
          break;
        }
      }
    } else {
      var pieces = [];
      for (var i = 0; i < +head; i++) {
        pieces.push(this.readLine());
      }

      bank.initialize(pieces);
    }
  }
  encodePieceBank() {
    var bank = this.board.bank;

    var pieces = bank.pieces.map(function (p) {
      return p.serialize();
    });

    for (var i = 0; i < bank.presets.length; i++) {
      if (!bank.presets[i].constant) {
        continue;
      }
      if (this.puzzle.pzpr.util.sameArray(bank.presets[i].constant, pieces)) {
        this.writeLine(bank.presets[i].shortkey);
        return;
      }
    }

    this.writeLine("" + pieces.length);
    for (var i = 0; i < pieces.length; i++) {
      this.writeLine(pieces[i]);
    }
  }
  decodePieceBankQcmp() {
    var nums = (this.readLine() || "").split(" ");
    var count = Math.min(nums.length, this.board.bank.pieces.length);
    for (var i = 0; i < count; i++) {
      this.board.bank.pieces[i].qcmp = +nums[i];
    }
  }
  encodePieceBankQcmp() {
    var data = this.board.bank.pieces
      .map(function (piece) {
        return piece.qcmp + " ";
      })
      .join("");
    this.writeLine(data);
  }

  // decodeFlags() {
  //     var flags = this.readLine().split(",");
  //     for (var i = 0; i < flags.length; i++) {
  //         this.puzzle.setConfig(flags[i], true);
  //     }
  // }
  // encodeFlags(flagnames) {
  //     var flags = [];
  //     for (var i = 0; i < flagnames.length; i++) {
  //         if (this.puzzle.getConfig(flagnames[i])) {
  //             flags.push(flagnames[i]);
  //         }
  //     }
  //     this.writeLine(flags.join(","));
  // }

  // //---------------------------------------------------------------------------
  // // fio.decodeConfigFlag() Set a config bool based on the presence of a string
  // // fio.encodeConfigFlag() Conditionally write a string
  // //---------------------------------------------------------------------------

  // decodeConfigFlag(flag, configkey, truevalue, falsevalue) {
  //     if (truevalue === undefined) {
  //         truevalue = true;
  //     }
  //     if (falsevalue === undefined) {
  //         falsevalue = !truevalue;
  //     }
  //     if (this.dataarray[this.lineseek] === flag) {
  //         this.puzzle.setConfig(configkey, truevalue);
  //         this.readLine();
  //     } else {
  //         this.puzzle.setConfig(configkey, falsevalue);
  //     }
  // }
  // encodeConfigFlag(flag, configkey, truevalue) {
  //     if (truevalue === undefined) {
  //         truevalue = true;
  //     }
  //     if (this.puzzle.getConfig(configkey) === truevalue) {
  //         this.writeLine(flag);
  //     }
  // }

  // //---------------------------------------------------------------------------
  // // fio.decodeCellXMLBoard()  配列で、個別文字列から個別セルの設定を行う (XML board用)
  // // fio.decodeCellXMLBrow()   配列で、個別文字列から個別セルの設定を行う (XML board用)
  // // fio.decodeCellXMLArow()   配列で、個別文字列から個別セルの設定を行う (XML answer用)
  // // fio.encodeCellXMLBoard()  個別セルデータから個別文字列の設定を行う (XML board用)
  // // fio.encodeCellXMLBrow()   個別セルデータから個別文字列の設定を行う (XML board用)
  // // fio.encodeCellXMLArow()   個別セルデータから個別文字列の設定を行う (XML answer用)
  // // fio.createXMLNode()  指定されたattributeを持つXMLのノードを作成する
  // //---------------------------------------------------------------------------
  // decodeCellXMLBoard(func) {
  //     var nodes = this.xmldoc.querySelectorAll("board number");
  //     for (var i = 0; i < nodes.length; i++) {
  //         var node = nodes[i];
  //         var cell = this.board.getc(
  //             +node.getAttribute("c") * 2 - 1,
  //             +node.getAttribute("r") * 2 - 1
  //         );
  //         if (!cell.isnull) {
  //             func(cell, +node.getAttribute("n"));
  //         }
  //     }
  // }
  // encodeCellXMLBoard(func) {
  //     var boardnode = this.xmldoc.querySelector("board");
  //     var bd = this.board;
  //     for (var i = 0; i < bd.cell.length; i++) {
  //         var cell = bd.cell[i],
  //             val = func(cell);
  //         if (val !== null) {
  //             boardnode.appendChild(
  //                 this.createXMLNode("number", {
  //                     r: ((cell.by / 2) | 0) + 1,
  //                     c: ((cell.bx / 2) | 0) + 1,
  //                     n: val
  //                 })
  //             );
  //         }
  //     }
  // }
  // decodeCellXMLBrow(func) {
  //     this.decodeCellXMLrow_com(func, "board", "brow");
  // }
  // encodeCellXMLBrow(func) {
  //     this.encodeCellXMLrow_com(func, "board", "brow");
  // }
  // decodeCellXMLArow(func) {
  //     this.decodeCellXMLrow_com(func, "answer", "arow");
  // }
  // encodeCellXMLArow(func) {
  //     this.encodeCellXMLrow_com(func, "answer", "arow");
  // }
  // decodeCellXMLrow_com(func, parentnodename, targetnodename) {
  //     var rownodes = this.xmldoc.querySelectorAll(
  //         parentnodename + " " + targetnodename
  //     );
  //     var ADJ = this.PBOX_ADJUST;
  //     for (var b = 0; b < rownodes.length; b++) {
  //         var bx = 1 - ADJ,
  //             by = +rownodes[b].getAttribute("row") * 2 - 1 - ADJ;
  //         var nodes = rownodes[b].childNodes;
  //         for (var i = 0; i < nodes.length; i++) {
  //             if (nodes[i].nodeType !== 1) {
  //                 continue;
  //             }
  //             var name = nodes[i].nodeName,
  //                 n = nodes[i].getAttribute("n") || 1;
  //             if (name === "z") {
  //                 name = "n0";
  //             } else if (name === "n") {
  //                 name = "n" + +nodes[i].getAttribute("v");
  //             }
  //             for (var j = 0; j < n; j++) {
  //                 func(this.board.getobj(bx, by), name);
  //                 bx += 2;
  //             }
  //         }
  //     }
  // }
  // encodeCellXMLrow_com(func, parentnodename, targetnodename) {
  //     var boardnode = this.xmldoc.querySelector(parentnodename);
  //     var ADJ = this.PBOX_ADJUST;
  //     var bd = this.board;
  //     for (var by = 1 - ADJ; by <= bd.maxby; by += 2) {
  //         var rownode = this.createXMLNode(targetnodename, {
  //             row: (((by + ADJ) / 2) | 0) + 1
  //         });
  //         for (var bx = 1 - ADJ; bx <= bd.maxbx; bx += 2) {
  //             var piece = bd.getobj(bx, by),
  //                 nodename = func(piece),
  //                 node;
  //             if (nodename.match(/n(\d\d+)/) || nodename.match(/n(\-\d+)/)) {
  //                 node = this.createXMLNode("n", { v: RegExp.$1 });
  //             } else if (nodename === "n0") {
  //                 node = this.createXMLNode("z");
  //             } else {
  //                 node = this.createXMLNode(nodename);
  //             }
  //             rownode.appendChild(node);
  //         }
  //         boardnode.appendChild(rownode);
  //     }
  // }

  // createXMLNode(name, attrs) {
  //     var node = this.xmldoc.createElement(name);
  //     if (!!attrs) {
  //         for (var i in attrs) {
  //             node.setAttribute(i, attrs[i]);
  //         }
  //     }
  //     return node;
  // }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellQnum_kanpen() pencilbox用問題数字のデコードを行う
  //   // fio.encodeCellQnum_kanpen() pencilbox用問題数字のエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellQnum_kanpen() {
  //     this.decodeCell(function (cell, ca) {
  //       if (ca !== ".") {
  //         cell.qnum = +ca;
  //       }
  //     });
  //   }
  //   encodeCellQnum_kanpen() {
  //     this.encodeCell(function (cell) {
  //       return cell.qnum >= 0 ? cell.qnum + " " : ". ";
  //     });
  //   }
  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellAnum_kanpen() pencilbox用回答数字のデコードを行う
  //   // fio.encodeCellAnum_kanpen() pencilbox用回答数字のエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellAnum_kanpen() {
  //     this.decodeCell(function (cell, ca) {
  //       if (ca !== "." && ca !== "0") {
  //         cell.anum = +ca;
  //       }
  //     });
  //   }
  //   encodeCellAnum_kanpen() {
  //     this.encodeCell(function (cell) {
  //       if (cell.qnum !== -1) {
  //         return ". ";
  //       } else if (cell.anum === -1) {
  //         return "0 ";
  //       } else {
  //         return cell.anum + " ";
  //       }
  //     });
  //   }
  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellQnumAns_kanpen() pencilbox用問題数字＋黒マス白マスのデコードを行う
  //   // fio.encodeCellQnumAns_kanpen() pencilbox用問題数字＋黒マス白マスのエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellQnumAns_kanpen() {
  //     this.decodeCell(function (cell, ca) {
  //       if (ca === "#") {
  //         cell.qans = 1;
  //       } else if (ca === "+") {
  //         cell.qsub = 1;
  //       } else if (ca === "?") {
  //         cell.qnum = -2;
  //       } else if (ca !== ".") {
  //         cell.qnum = +ca;
  //       }
  //     });
  //   }
  //   encodeCellQnumAns_kanpen() {
  //     this.encodeCell(function (cell) {
  //       if (cell.qnum >= 0) {
  //         return cell.qnum + " ";
  //       } else if (cell.qnum === -2) {
  //         return "? ";
  //       } else if (cell.qans === 1) {
  //         return "# ";
  //       } else if (cell.qsub === 1) {
  //         return "+ ";
  //       } else {
  //         return ". ";
  //       }
  //     });
  //   }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellQnum_XMLBoard() pencilbox XML用問題用数字のデコードを行う
  //   // fio.encodeCellQnum_XMLBoard() pencilbox XML用問題用数字のエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellQnum_XMLBoard() {
  //     var minnum = this.board.cell[0].getminnum() > 0 ? 1 : 0;
  //     var undecnum = this.UNDECIDED_NUM_XML;
  //     this.decodeCellXMLBoard(function (cell, val) {
  //       if (val === undecnum) {
  //         cell.qnum = -2;
  //       } else if (val >= minnum) {
  //         cell.qnum = val;
  //       }
  //     });
  //   }
  //   encodeCellQnum_XMLBoard() {
  //     var minnum = this.board.cell[0].getminnum() > 0 ? 1 : 0;
  //     var undecnum = this.UNDECIDED_NUM_XML;
  //     this.encodeCellXMLBoard(function (cell) {
  //       var val = null;
  //       if (cell.qnum === -2) {
  //         val = undecnum;
  //       } else if (cell.qnum >= minnum) {
  //         val = cell.qnum;
  //       }
  //       return val;
  //     });
  //   }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellQnum_XMLBoard() pencilbox XML用問題用数字(browタイプ)のデコードを行う
  //   // fio.encodeCellQnum_XMLBoard() pencilbox XML用問題用数字(browタイプ)のエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellQnum_XMLBoard_Brow() {
  //     var undecnum = this.UNDECIDED_NUM_XML;
  //     this.decodeCellXMLBrow(function (cell, name) {
  //       if (name === "n" + undecnum) {
  //         cell.qnum = -2;
  //       } else if (name !== "s") {
  //         cell.qnum = +name.substr(1);
  //       }
  //     });
  //   }
  //   encodeCellQnum_XMLBoard_Brow() {
  //     var undecnum = this.UNDECIDED_NUM_XML;
  //     this.encodeCellXMLBrow(function (cell) {
  //       if (cell.qnum === -2) {
  //         return "n" + undecnum;
  //       } else if (cell.qnum >= 0) {
  //         return "n" + cell.qnum;
  //       }
  //       return "s";
  //     });
  //   }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellAnum_XMLBoard() pencilbox XML用回答用数字のデコードを行う
  //   // fio.encodeCellAnum_XMLBoard() pencilbox XML用回答用数字のエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellAnum_XMLAnswer() {
  //     this.decodeCellXMLArow(function (cell, name) {
  //       if (name === "n0") {
  //         cell.anum = -1;
  //       } else if (name !== "s") {
  //         cell.anum = +name.substr(1);
  //       }
  //     });
  //   }
  //   encodeCellAnum_XMLAnswer() {
  //     this.encodeCellXMLArow(function (cell) {
  //       if (cell.anum > 0) {
  //         return "n" + cell.anum;
  //       } else if (cell.anum === -1) {
  //         return "n0";
  //       }
  //       return "s";
  //     });
  //   }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeAreaRoom_XMLBoard() pencilbox XML用問題用不定形部屋のデコードを行う
  //   // fio.encodeAreaRoom_XMLBoard() pencilbox XML用問題用不定形部屋のエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeAreaRoom_XMLBoard() {
  //     var rdata = [];
  //     this.decodeCellXMLBrow(function (cell, name) {
  //       rdata.push(+name.substr(1));
  //     });
  //     this.rdata2Border(true, rdata);
  //     this.board.roommgr.rebuild();
  //   }
  //   encodeAreaRoom_XMLBoard() {
  //     var bd = this.board;
  //     bd.roommgr.rebuild();
  //     var rooms = bd.roommgr.components;
  //     this.xmldoc
  //       .querySelector("board")
  //       .appendChild(this.createXMLNode("areas", { N: rooms.length }));
  //     this.encodeCellXMLBrow(function (cell) {
  //       var roomid = rooms.indexOf(cell.room);
  //       return "n" + (roomid > 0 ? roomid : -1);
  //     });
  //   }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeCellAns_XMLAnswer() pencilbox XML用黒マスのデコードを行う
  //   // fio.encodeCellAns_XMLAnswer() pencilbox XML用黒マスのエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeCellAns_XMLAnswer() {
  //     this.decodeCellXMLArow(function (cell, name) {
  //       if (name === "w") {
  //         cell.qans = 1;
  //       } else if (name === "s") {
  //         cell.qsub = 1;
  //       }
  //     });
  //   }
  //   encodeCellAns_XMLAnswer() {
  //     this.encodeCellXMLArow(function (cell) {
  //       if (cell.qans === 1) {
  //         return "w";
  //       } else if (cell.qsub === 1) {
  //         return "s";
  //       }
  //       return "u";
  //     });
  //   }

  //   //---------------------------------------------------------------------------
  //   // fio.decodeBorderLine_XMLAnswer() pencilbox XML用Lineのデコードを行う
  //   // fio.encodeBorderLine_XMLAnswer() pencilbox XML用Lineのエンコードを行う
  //   //---------------------------------------------------------------------------
  //   decodeBorderLine_XMLAnswer() {
  //     this.decodeCellXMLArow(function (cell, name) {
  //       var val = 0;
  //       var bdh = cell.adjborder.bottom,
  //         bdv = cell.adjborder.right;
  //       if (name.charAt(0) === "n") {
  //         val = +name.substr(1);
  //       } else {
  //         if (name.match(/h/)) {
  //           val += 1;
  //         }
  //         if (name.match(/v/)) {
  //           val += 2;
  //         }
  //       }
  //       if (val & 1) {
  //         bdh.line = 1;
  //       }
  //       if (val & 2) {
  //         bdv.line = 1;
  //       }
  //       if (val & 4) {
  //         bdh.qsub = 2;
  //       }
  //       if (val & 8) {
  //         bdv.qsub = 2;
  //       }
  //     });
  //   }
  //   encodeBorderLine_XMLAnswer() {
  //     this.encodeCellXMLArow(function (cell) {
  //       var val = 0,
  //         nodename = "";
  //       var bdh = cell.adjborder.bottom,
  //         bdv = cell.adjborder.right;
  //       if (bdh.line === 1) {
  //         val += 1;
  //       }
  //       if (bdv.line === 1) {
  //         val += 2;
  //       }
  //       if (bdh.qsub === 2) {
  //         val += 4;
  //       }
  //       if (bdv.qsub === 2) {
  //         val += 8;
  //       }

  //       if (val === 0) {
  //         nodename = "s";
  //       } else if (val === 1) {
  //         nodename = "h";
  //       } else if (val === 2) {
  //         nodename = "v";
  //       } else if (val === 3) {
  //         nodename = "hv";
  //       } else {
  //         nodename = "n" + val;
  //       }
  //       return nodename;
  //     });
  //   }
}
