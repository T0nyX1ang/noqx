let image_url = (str) =>
  str
    ? `url('static/noq/images/${str + (/^.*\.png$/.test(str) ? "" : ".png")}')`
    : str;
const nav_keys = ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"];
const del_keys = ["Backspace", "Delete", "Escape"];
const COLORS = ["black", "gray", "blue", "green", "yellow", "red"];
const CLIPBOARD_SYMBOLS = {
  1: "│",
  "-": "─",
  L: "└",
  J: "┘",
  "+": "┼",
  7: "┐",
  r: "┌",

  "||": "║",
  "=": "=",

  bulb: "O",

  "1w": "⌽",
  "-w": "⦵",

  black_circle: "⬤",
  white_circle: "◯",

  n: "◡",
  s: "◠",
  w: ")",
  e: "(",
  nw: "╯",
  ne: "╰",
  sw: "╮",
  se: "╭",

  "top-left": "◤",
  "top-right": "◥",
  "bottom-left": "◣",
  "bottom-right": "◢",

  "↑": "↑",
  "←": "←",
  "→": "→",
  "↓": "↓",
  "↱": "↱",
  "⬐": "⬐",
  "↳": "↳",
  "⬑": "⬑",
  "↴": "↴",
  "↰": "↰",
  "↲": "↲",
  "⬏": "⬏",

  tree: "🌲",
  tent: "⛺",
};

function add_json_objects(d1, d2) {
  let d = {};
  for (let key1 in d1) d[key1] = d1[key1];
  for (let key2 in d2) {
    if (d[key2] == undefined) d[key2] = d2[key2];
    // combine into array
    else d[key2] = [d[key2], d2[key2]];
  }
  return d;
}

function set_z_order(elts) {
  let i = 0;
  for (let elt of elts) {
    elt.style.zIndex = i;
    ++i;
  }
}

function puzzle_neighbors(i, j) {
  return {
    nw: get(`puzzle_${i - 2},${j - 2}`),
    n: get(`puzzle_${i - 2},${j}`),
    ne: get(`puzzle_${i - 2},${j + 2}`),
    w: get(`puzzle_${i},${j - 2}`),
    e: get(`puzzle_${i},${j + 2}`),
    sw: get(`puzzle_${i + 2},${j - 2}`),
    s: get(`puzzle_${i + 2},${j}`),
    se: get(`puzzle_${i + 2},${j + 2}`),
  };
}

function toggle_background_image(elt, img) {
  // used in Spiral Galaxies
  if (elt == undefined) return;

  if (elt.raw_image_url == img) {
    elt.raw_image_url = "";
    elt.style.backgroundImage = "";
  } else {
    let neighbors = puzzle_neighbors(elt.i, elt.j);
    let aff_neigh = []; // affected neighbors of elt
    let riu = elt.raw_image_url;
    if (riu == "nw") aff_neigh = ["w", "n", "nw"];
    if (riu == "n") aff_neigh = ["n"];
    if (riu == "ne") aff_neigh = ["e", "n", "ne"];
    if (riu == "w") aff_neigh = ["w"];
    if (riu == "e") aff_neigh = ["e"];
    if (riu == "sw") aff_neigh = ["s", "w", "sw"];
    if (riu == "s") aff_neigh = ["s"];
    if (riu == "se") aff_neigh = ["s", "e", "se"];

    for (let neigh of aff_neigh) {
      // reset their images
      let neighbor = neighbors[neigh];
      if (neighbor) {
        neighbor.raw_image_url = "";
        neighbor.style.backgroundImage = "";
        neighbor.parent.puzzle_image_str = "";
      }
    }

    elt.raw_image_url = img;
    elt.style.backgroundImage = image_url(img);
    elt.parent.puzzle_image_str = img;
  }
}

function restrict_to_grid(elt) {
  // restrict elt to be within the grid
  let curij = elt.id.split(",").map((x) => parseInt(x));
  let curi = curij[0];
  let curj = curij[1];
  return curi < 0 || curj < 0 || curi > 2 * ROWS || curj > 2 * COLS;
}

///////////////////////////////
//       BASE ELF CLASS      //
///////////////////////////////
class Elf {
  static controls() {
    return { "Arrow keys/Mouse": "Select cell", Delete: "Clear cell" };
  }

  constructor(elt, borders, i, j, dots, default_image_url = "") {
    this.elt = elt;
    this.borders = borders;
    this.dots = dots;
    this.i = i;
    this.j = j;
    this.puzzle_borders = {};
    this.solution_borders = {};

    if (borders)
      for (let id of Object.keys(borders)) {
        this.puzzle_borders[id] = borders[id].querySelector(
          ".puzzle_border_horizontal, .puzzle_border_vertical"
        );
        this.solution_borders[id] = borders[id].querySelector(
          ".solution_border_horizontal, .solution_border_vertical"
        );
      }

    this.puzzle_dots = {};
    this.solution_dots = {};
    if (dots)
      for (let id of Object.keys(dots)) {
        this.puzzle_dots[id] = dots[id].querySelector(".puzzle_dot");
        this.solution_dots[id] = dots[id].querySelector(".solution_dot");
      }

    this.puzzle_elt = elt.querySelector(".puzzle_cell");
    this.puzzle_elt.i = this.i;
    this.puzzle_elt.j = this.j;
    this.puzzle_elt.parent = this; // embed this data for convenience
    this.default_image_url = default_image_url;
    this.puzzle_elt.style.backgroundImage = image_url(this.default_image_url);

    this.solution_elt = elt.querySelector(".solution_cell");
    this.solution_elt.i = this.i;
    this.solution_elt.j = this.j;

    this.key = null;
  }

  handle_input(key, modifiers) {
    if (del_keys.includes(key)) {
      let rg = selected_range;
      if (rg) {
        for (let i = rg[0]; i <= rg[1]; i += 2)
          for (let j = rg[2]; j <= rg[3]; j += 2) {
            let elf = ELVES[`${i},${j}`];
            this.puzzle_elt.style = "";
            elf.puzzle_elt.style.backgroundImage = image_url(
              this.default_image_url
            );
            elf.puzzle_elt.innerHTML = "";
            elf.key = null;
          }
      } else {
        this.puzzle_elt.style = "";
        this.puzzle_elt.style.backgroundImage = image_url(
          this.default_image_url
        );
        this.puzzle_image_str = "";
        this.puzzle_elt.innerHTML = "";
        this.key = null;
      }
    }
  }
  load_example(str) {
    if (COLORS.includes(str)) this.puzzle_elt.style.backgroundColor = str;
    else if (/^[0-9\?]+$/.test(str)) this.puzzle_elt.innerHTML = str;
    else if (/^.*\.png$/.test(str)) {
      this.puzzle_elt.style.backgroundImage = image_url(str);
      this.puzzle_image_str = str.substring(0, str.length - 4); // remove `.png` from str
    } else this.puzzle_elt.innerHTML = str;
  }
  load_solution(str) {
    if (COLORS.includes(str)) {
      this.solution_elt.style.backgroundColor = str;
      if (str === "black") this.solution_elt.style.color = "gray";
      this.solution_elt.innerHTML = this.puzzle_elt.innerHTML; // retain the text
    } else if (/^[0-9]+$/.test(str)) this.solution_elt.innerHTML = str;
    else if (/^.+\.png$/.test(str)) {
      let image_urls = [];
      let image_strs = [];
      for (let url of str.split(",")) {
        image_urls.push(image_url(url));
        image_strs.push(url.substring(0, url.length - 4)); // remove `.png` from str
      }
      this.solution_elt.style.backgroundImage = image_urls.join(",");
      this.solution_image_str = image_strs.sort().join(",");
      if (pt === "hashi" && /^[0-9]+$/.test(this.puzzle_elt.innerHTML)) {
        // special case for Hashi solution display
        this.solution_elt.style.clipPath =
          "polygon(0% 0%, 0% 100%, 20% 100%, 20% 20%, 80% 20%, 80% 80%, 20% 80%, 20% 100%, 100% 100%, 100% 0%)";
      }
    } else this.solution_elt.innerHTML = str;
  }
  reset() {
    this.puzzle_elt.style.backgroundImage = image_url(this.default_image_url);
    this.puzzle_image_str = "";
    this.puzzle_elt.style.backgroundColor = "";
    this.puzzle_elt.style.color = "";
    this.puzzle_elt.innerHTML = "";
    for (let obj of Object.values(this.puzzle_borders))
      obj.style.backgroundColor = "";
    this.reset_solution();
  }
  reset_solution() {
    this.solution_elt.style.backgroundImage = "";
    this.solution_image_str = "";
    this.solution_elt.style.backgroundColor = "";
    this.solution_elt.style.color = "";
    this.solution_elt.innerHTML = "";
    for (let key of Object.keys(this.solution_borders)) {
      this.solution_borders[key].style.backgroundColor =
        this.puzzle_borders[key].style.backgroundColor; // reset solution border to puzzle border
    }
  }
  puzzle_neighbors() {
    return {
      nw: get(`puzzle_${this.i - 2},${this.j - 2}`),
      n: get(`puzzle_${this.i - 2},${this.j}`),
      ne: get(`puzzle_${this.i - 2},${this.j + 2}`),
      w: get(`puzzle_${this.i},${this.j - 2}`),
      e: get(`puzzle_${this.i},${this.j + 2}`),
      sw: get(`puzzle_${this.i + 2},${this.j - 2}`),
      s: get(`puzzle_${this.i + 2},${this.j}`),
      se: get(`puzzle_${this.i + 2},${this.j + 2}`),
    };
  }
  toggle_border(
    key,
    val // val = null, true, or false
  ) {
    set_z_order([this.solution_borders[key], this.puzzle_borders[key]]);
    return toggle_border(this.puzzle_borders[key], val);
  }

  generate_copy_td() {
    let td = make_elt("TD");

    // background color
    let background_color =
      this.solution_elt.style.backgroundColor ||
      this.puzzle_elt.style.backgroundColor;
    if (background_color) td.style.backgroundColor = background_color;

    // borders
    const key_to_border = {
      ArrowLeft: "borderLeft",
      ArrowRight: "borderRight",
      ArrowUp: "borderTop",
      ArrowDown: "borderBottom",
    };
    // first, default borders (for edges of grid, not including outside clues)
    if (this.i == 1 && 1 <= this.j && this.j <= 2 * COLS - 1)
      // top border
      td.style.borderTop = "1px solid black";
    if (this.i == 2 * ROWS - 1 && 1 <= this.j && this.j <= 2 * COLS - 1)
      // bottom border
      td.style.borderBottom = "1px solid black";
    if (this.j == 1 && 1 <= this.i && this.i <= 2 * ROWS - 1)
      // left border
      td.style.borderLeft = "1px solid black";
    if (this.j == 2 * COLS - 1 && 1 <= this.i && this.i <= 2 * ROWS - 1)
      // right border
      td.style.borderRight = "1px solid black";
    if (this.borders)
      for (let key of nav_keys) {
        let border_color =
          this.solution_borders[key].style.backgroundColor ||
          this.puzzle_borders[key].style.backgroundColor;
        if (COLORS.includes(border_color) && !td.style[key_to_border[key]])
          td.style[key_to_border[key]] = `1px solid ${border_color}`;
      }

    // text content of cell
    let contents = this.solution_elt.innerHTML || this.puzzle_elt.innerHTML;

    if (CLIPBOARD_SYMBOLS[this.solution_image_str])
      td.innerHTML = CLIPBOARD_SYMBOLS[this.solution_image_str];
    else if (CLIPBOARD_SYMBOLS[this.puzzle_image_str])
      td.innerHTML = CLIPBOARD_SYMBOLS[this.puzzle_image_str];
    else if (contents) {
      td.innerHTML = "'" + contents;

      // flip text color to white, if the cell is black (for e.g. Akari, Shakashaka)
      if (td.style.backgroundColor == "black") td.style.color = "white";
      if (td.style.backgroundColor == "green") td.style.color = "white";
    }

    td.style.textAlign = "center";
    // td.style.verticalAlign = 'middle'; // TODO why doesn't this work?? :(

    return td;
  }
}

///////////////////////////////
// ELF ABSTRACTION FUNCTIONS //
///////////////////////////////

function DirectSum(Elf1, Elf2, priority = "compress", default_image_url = "") {
  return class extends Elf {
    static controls() {
      let controls1 = Elf1.controls();
      let controls2 = Elf2.controls();
      for (let key in controls2) controls1[key] = controls2[key];
      return controls1;
    }

    constructor(elt, borders, i, j, dots) {
      super(elt, borders, i, j, dots, default_image_url);
      this.elf1 = new Elf1(elt, borders, i, j, dots, default_image_url);
      this.elf2 = new Elf2(elt, borders, i, j, dots, default_image_url);
      this.priority = priority;
    }

    handle_input(key, modifiers) {
      this.elf1.handle_input(key, modifiers);
      this.elf2.handle_input(key, modifiers);
    }

    encode_input() {
      let out1 = this.elf1.encode_input();
      let out2 = this.elf2.encode_input();
      if (this.priority == "first") {
        if (out1 !== null) return out1;
        else return out2;
      } else if (this.priority == "second") {
        if (out2 !== null) return out2;
        else return out1;
      } else if (this.priority == "concat") {
        let is_nonempty = false;
        let encoding1 = {};
        if (out1 == null) encoding1[this.elf1.elt.id] = "";
        else if (out1.constructor === {}.constructor) {
          // JSON
          encoding1 = out1;
          is_nonempty = true;
        } else {
          encoding1[this.elf1.elt.id] = out1;
          is_nonempty = true;
        }

        let encoding2 = {};
        if (out2 == null) encoding2[this.elf2.elt.id] = "";
        else if (out2.constructor === {}.constructor) {
          // JSON
          encoding2 = out2;
          is_nonempty = true;
        } else {
          encoding2[this.elf2.elt.id] = out2;
          is_nonempty = true;
        }

        if (is_nonempty) return add_json_objects(encoding1, encoding2);
        return null;
      } else if (this.priority == "compress") {
        let encoding1 = {};
        if (out1 === null);
        else if (out1.constructor === {}.constructor)
          // JSON
          encoding1 = out1;
        else {
          encoding1[this.elf1.elt.id] = out1;
        }

        let encoding2 = {};
        if (out2 === null);
        else if (out2.constructor === {}.constructor)
          // JSON
          encoding2 = out2;
        else {
          encoding2[this.elf2.elt.id] = out2;
        }
        return add_json_objects(encoding1, encoding2);
      }
    }

    load_example_str(str) {
      let res1 = this.elf1.load_example(str);
      if (!res1)
        // if not successful, load using elf2's rules
        this.elf2.load_example(str);
    }

    load_example(clue) {
      if (!Array.isArray(clue)) {
        this.load_example_str(clue);
      } else {
        for (let str of clue) {
          this.load_example_str(str);
        }
      }
    }
  };
}

function InvertSolutionZOrder(Elf1) {
  return class extends Elf1 {
    load_solution(str) {
      super.load_solution(str);
      set_z_order([this.solution_elt, this.puzzle_elt]);
    }
  };
}

///////////////////////////////////////////
//    GENERAL ELF CLASSES/METACLASSES    //
///////////////////////////////////////////

class BorderElf extends Elf {
  static controls() {
    let controls = super.controls();
    controls["Shift + Arrow keys"] = "Toggle borders";
    controls["Click & drag"] = "Toggle borders";
    return controls;
  }

  handle_input(key, modifiers) {
    if (modifiers.shift) {
      let rg = selected_range;
      if (rg) {
        // dealing with the whole rectangle selected
        let up, down, left, right;
        if (key == "Enter") {
          up = true;
          down = true;
          left = true;
          right = true;
        }
        if (key == "ArrowUp") up = true;
        if (key == "ArrowDown") down = true;
        if (key == "ArrowLeft") left = true;
        if (key == "ArrowRight") right = true;

        for (let j = rg[2]; j <= rg[3]; j += 2) {
          if (up) ELVES[`${rg[0]},${j}`].toggle_border("ArrowUp");
          if (down) ELVES[`${rg[1]},${j}`].toggle_border("ArrowDown");
        }
        for (let i = rg[0]; i <= rg[1]; i += 2) {
          if (left) ELVES[`${i},${rg[2]}`].toggle_border("ArrowLeft");
          if (right) ELVES[`${i},${rg[3]}`].toggle_border("ArrowRight");
        }
      } else if (nav_keys.includes(key))
        // only dealing with this cell
        this.toggle_border(key);
    }
  }

  encode_input() {
    let encoding = {};
    for (let border_id of Object.keys(this.borders))
      if (this.puzzle_borders[border_id].style.backgroundColor == "black")
        encoding[this.borders[border_id].id] = "black";
    return encoding;
  }
}

function ImageElf(dict, controls_dict, styles = {}) {
  return class extends Elf {
    static controls() {
      let controls = super.controls();
      for (let key in controls_dict) controls[key] = controls_dict[key];
      return controls;
    }

    constructor(elt, borders, i, j, dots, default_image_url) {
      super(elt, borders, i, j, dots, default_image_url);
      this.dict = dict;
    }

    handle_input(key, modifiers) {
      if (restrict_to_grid(this.elt)) return;

      super.handle_input(key, modifiers);

      if (!this.dict[key]) return false;

      this.key = key;
      // this.puzzle_elt.style = "";
      this.puzzle_elt.style.backgroundImage = image_url(this.dict[key]);
      if (styles[key] !== undefined) {
        for (const [attribute, value] of Object.entries(styles[key])) {
          this.puzzle_elt.style[attribute] = value;
        }
      }
      return true;
    }

    load_example(str) {
      return this.handle_input(str, null);
    }

    encode_input() {
      return this.key;
    }
  };
}

function IntElf(min = 0, max = 99, range = "[0-9]", default_image_url = "") {
  return class extends Elf {
    static controls() {
      let controls = super.controls();
      controls[range] = "Write clue in cell";
      return controls;
    }

    constructor(elt, borders, i, j, dots) {
      super(elt, borders, i, j, dots, default_image_url);
    }

    handle_input(key, modifiers) {
      super.handle_input(key, modifiers);
      if (!"1234567890".includes(key)) return;

      let num = parseInt(this.puzzle_elt.innerHTML + key);

      if (min <= num && num <= max);
      else if (min <= key && key <= max)
        // appending works
        // restarting with this key works
        num = key;
      else return; // nothing works, so do nothing
      this.puzzle_elt.innerHTML = num + ""; // now set the HTML
    }

    load_example(str) {
      for (let ch of str) this.handle_input(ch, null);
      return;
    }

    encode_input() {
      return this.puzzle_elt.innerHTML ? this.puzzle_elt.innerHTML : null;
    }
  };
}

class QuestionMarkElf extends Elf {
  static controls() {
    let controls = super.controls();
    controls["?"] = "Add '?' clue";
    return controls;
  }

  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);
    if (key == "?") {
      this.puzzle_elt.innerHTML = "?";
      return true;
    }
  }

  load_example(str) {
    if (str === "?") this.handle_input("?", null);
    return;
  }

  encode_input() {
    if (this.puzzle_elt.innerHTML == "?") return "?";
    else return null;
  }
}

// keyToColor maps key: [HTML color name, nickname]
// resetInnerHtml = true iff shaded cells cannot have other clues in them
function BgColorElf(
  keyToColor = { x: ["black", "black"] },
  resetInnerHtml = true
) {
  return class extends Elf {
    static controls() {
      let controls = super.controls();
      for (const [key, value] of Object.entries(keyToColor)) {
        controls[key] = `Toggle ${value[0]} cell`;
      }
      return controls;
    }

    handle_input(key, modifiers) {
      if (restrict_to_grid(this.elt)) return;

      super.handle_input(key, modifiers);

      if (key in keyToColor) {
        const bgColor = keyToColor[key][0];
        const innerColor = keyToColor[key][1];
        if (this.puzzle_elt.style.backgroundColor == bgColor) {
          this.puzzle_elt.style.backgroundColor = "";
          this.puzzle_elt.style.color = "";
        } else {
          if (resetInnerHtml) {
            this.puzzle_elt.innerHTML = "";
            this.puzzle_elt.style.backgroundImage = "";
          }
          this.puzzle_elt.style.backgroundColor = bgColor;
          this.puzzle_elt.style.color = innerColor;
        }
      } else if (
        resetInnerHtml &&
        this.puzzle_elt.style.backgroundColor &&
        !del_keys.includes(key)
      ) {
        this.puzzle_elt.innerHTML = "";
        this.puzzle_elt.style.backgroundImage = "";
      }
    }

    encode_input() {
      if (this.puzzle_elt.style.backgroundColor != "")
        return this.puzzle_elt.style.backgroundColor;
      return null;
    }

    load_example(str) {
      if (
        Object.values(keyToColor)
          .map((l) => l[0])
          .includes(str)
      ) {
        this.puzzle_elt.style.backgroundColor = str;
        return true;
      }
      return false;
    }
  };
}

function IntBordersElf(min = 0, max = 99, range = "[0-9]") {
  return DirectSum(IntElf(min, max, range), BorderElf);
}

CircleElf = ImageElf(
  { w: "white_circle", b: "black_circle" },
  { w: "Place white circle", b: "Place black circle" },
  { b: { color: "white" } }
);

function LetterElf(letterset, concat = false) {
  return class extends Elf {
    static controls() {
      let controls = super.controls();
      controls["[" + letterset.toUpperCase() + "]"] = "Write clue in cell";
      return controls;
    }

    handle_input(key, modifiers) {
      super.handle_input(key, modifiers);
      if (
        !letterset.toLowerCase().includes(key) &
        !letterset.toUpperCase().includes(key)
      )
        return;
      // now set the HTML
      const casedKey = letterset.includes(key.toUpperCase())
        ? key.toUpperCase()
        : key.toLowerCase();
      this.puzzle_elt.innerHTML = concat
        ? this.puzzle_elt.innerHTML + casedKey
        : casedKey;
    }

    encode_input() {
      return this.puzzle_elt.innerHTML
        ? encodeURIComponent(this.puzzle_elt.innerHTML)
        : null;
    }
  };
}

/////////////////////////////////////
//   PUZZLE-SPECIFIC ELF CLASSES   //
/////////////////////////////////////

class AkariElf extends DirectSum(
  DirectSum(BgColorElf(), IntElf(0, 4, "[0-4]"), "second"),
  ImageElf(
    { o: "bulb" },
    { o: "Place bulb" },
    { o: { color: "", backgroundColor: "" } }
  )
) {
  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);
    if ("01234".includes(key)) {
      this.puzzle_elt.style.backgroundColor = "black";
      this.puzzle_elt.style.color = "white";
      this.puzzle_elt.style.backgroundImage = "";
    }
  }

  load_example(str) {
    super.load_example(str);
    if ("01234".includes(str)) {
      this.puzzle_elt.style.backgroundColor = "black";
      this.puzzle_elt.style.color = "white";
      this.puzzle_elt.style.backgroundImage = "";
    }
  }
}

// big
class CastleWallElf extends Elf {
  dirToImage = {
    u: "up_arrow.png",
    r: "right_arrow.png",
    d: "down_arrow.png",
    l: "left_arrow.png",
  };

  keyToBg = {
    w: "",
    g: "gray",
    b: "white", // ACTUALLY CORRECT because of CSS inversion.
  };

  dir = "";
  color = "";

  static controls() {
    let controls = super.controls();
    controls["[0-9"] = "Write clue number";
    controls["[urdl]"] = "Specify clue direction";
    controls["[wgb]"] = "Toggle background color of white / gray / black";
    return controls;
  }

  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);

    if ("1234567890".includes(key)) {
      const min = 0;
      const max = 99;
      let num = parseInt(this.puzzle_elt.innerHTML + key);

      if (min <= num && num <= max);
      else if (min <= key && key <= max)
        // appending works
        // restarting with this key works
        num = key;
      else return; // nothing works, so do nothing
      this.puzzle_elt.innerHTML = num + ""; // now set the HTML
    } else if ("urdl".includes(key)) {
      this.puzzle_elt.style.backgroundImage = image_url(this.dirToImage[key]);
      this.dir = key;
    } else if ("wgb".includes(key)) {
      const bgColor = this.keyToBg[key];
      if (this.puzzle_elt.style.backgroundColor === bgColor) {
        this.puzzle_elt.style.backgroundColor = "";
        this.puzzle_elt.style.filter = "";
        this.color = "";
      } else {
        this.puzzle_elt.style.backgroundColor = bgColor;
        this.puzzle_elt.style.filter = key === "b" ? "invert(1)" : "";
        this.color = key;
      }
    } else if (del_keys.includes(key)) {
      this.dir = "";
      this.color = "";
    }
  }

  encode_input() {
    const num = this.puzzle_elt.innerHTML ?? "";
    const dir = this.dir;
    const color = this.color === "" ? "w" : this.color;
    if (num === "" && dir === "" && color === "w") return null;
    return [num, dir, color];
  }

  load_example(arr) {
    for (let str of arr) this.handle_input(str, null);
  }
}

class EasyAsElf extends Elf {
  static controls() {
    let controls = super.controls();
    controls["[Letter]"] = "Write clue in cell";
    return controls;
  }

  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);

    if (!get("param_input_letters").value.includes(key)) return;
    this.puzzle_elt.innerHTML = key;
  }

  encode_input() {
    return this.puzzle_elt.innerHTML ? this.puzzle_elt.innerHTML : null;
  }
}

class KakuroElf extends Elf {
  static controls() {
    let controls = super.controls();
    controls["[0-9]"] = "Write clue";
    controls["Tab"] = "Switch between across and down clues";
    controls["x"] = "Add black cell";
    return controls;
  }

  constructor(elt, borders, i, j) {
    super(elt, borders, i, j);
    this.across_clue = 0;
    this.down_clue = 0;
    this.is_black = false;
    this.across_is_active = true;

    this.across_elt = make_elt("DIV", "kakuro_across_clue", this.puzzle_elt);
    this.down_elt = make_elt("DIV", "kakuro_down_clue", this.puzzle_elt);
  }

  handle_becoming_inactive() {
    // reset outline boxes for clues
    this.across_elt.style.outline = "none";
    this.down_elt.style.outline = "none";
  }

  handle_becoming_active(
    reset_active = true // put outline box around the active clue
  ) {
    this.handle_becoming_inactive();
    if (reset_active) this.across_is_active = true; // reset active clue
    let elt = this.across_is_active ? this.across_elt : this.down_elt;
    elt.style.outline = "2pt solid red";
    elt.style.outlineOffset = "-2px";
  }

  handle_input(key, modifiers) {
    if (key == "Tab") {
      this.across_is_active = !this.across_is_active;
      this.handle_becoming_active(false);
    }

    if (["Backspace", "Delete", "Escape"].includes(key)) {
      if (this.is_black) this.is_black = false;

      if (this.across_is_active) {
        if (this.across_clue == 0)
          // switch to down clue
          this.down_clue = 0;
        else this.across_clue = 0;
      } else {
        if (this.down_clue == 0)
          // switch to across clue
          this.across_clue = 0;
        else this.down_clue = 0;
      }
    }

    if (key == "x") {
      this.puzzle_elt.style.backgroundColor = "black";
      this.across_clue = 0;
      this.down_clue = 0;
      this.is_black = true;
    }

    if (/[0-9]/.test(key)) {
      // append to active clue
      if (this.across_is_active) {
        let num = parseInt(key);
        let new_clue = 10 * this.across_clue + num;
        if (0 < new_clue && new_clue < 100) this.across_clue = new_clue;
        else if (0 < num && num < 100) this.across_clue = num;
      } else {
        let num = parseInt(key);
        let new_clue = 10 * this.down_clue + num;
        if (0 < new_clue && new_clue < 100) this.down_clue = new_clue;
        else if (0 < num && num < 100) this.down_clue = num;
      }
    }

    // set html of clue elements
    this.across_elt.innerHTML = this.across_clue || "";
    this.down_elt.innerHTML = this.down_clue || "";

    // blacken cell if any clue is present
    if (this.across_clue != 0 || this.down_clue != 0 || this.is_black)
      this.puzzle_elt.style.backgroundColor = "black";
    else this.puzzle_elt.style.backgroundColor = "";
  }

  encode_input() {
    if (this.across_clue != 0 || this.down_clue != 0)
      return [this.across_clue, this.down_clue];
    else if (this.is_black) return "black";
    else return null;
  }

  load_example(obj) {
    if (Array.isArray(obj)) {
      this.across_clue = obj[0];
      this.down_clue = obj[1];
      this.handle_input();
    } else if (obj == "black")
      this.handle_input("x"); // simulate a press of X to blacken the cell
    else this.handle_input("Delete"); // simulate removing everything
  }
}

class MagnetsElf extends DirectSum(
  IntBordersElf(),
  BgColorElf({ x: ["gray", "gray"], r: ["red", "red"], b: ["blue", "blue"] })
) {
  static controls() {
    let controls = super.controls();
    controls["+/red"] = "Clues calculated from the top and left";
    controls["-/blue"] = "Clues calculated from on the bottom and right";
    return controls;
  }
}

class NanroElf extends DirectSum(
  InvertSolutionZOrder(IntBordersElf()),
  BgColorElf({ x: ["gray", "gray"] })
) {
  static controls() {
    let controls = super.controls();
    controls["Shift + [0-9]"] = "Add signpost clue";
    return controls;
  }

  constructor(elt, borders, i, j) {
    super(elt, borders, i, j);
    this.signpost_clue = 0; // signpost clue
  }

  handle_input(key, modifiers) {
    if (["Backspace", "Delete", "Escape"].includes(key)) this.signpost_clue = 0;

    if (/[0-9]/.test(key)) this.signpost_clue = 0;

    if (modifiers.shift && /[\!\@\#\$\%\^\&\*\(\)]/.test(key)) {
      let num = {
        "!": 1,
        "@": 2,
        "#": 3,
        $: 4,
        "%": 5,
        "^": 6,
        "&": 7,
        "*": 8,
        "(": 9,
        ")": 0,
      }[key];
      this.signpost_clue = 10 * this.signpost_clue + num;
      if (this.signpost_clue != 0)
        this.puzzle_elt.innerHTML = `<div class='nanro_signpost'>${this.signpost_clue}</div>`;
    }

    return super.handle_input(key, modifiers);
  }

  encode_input() {
    if (this.signpost_clue != 0) {
      let encoding = super.encode_input();
      encoding[`${this.i},${this.j}`] = `s${this.signpost_clue}`;
      return encoding;
    } else return super.encode_input();
  }

  load_example(str) {
    if (/s[0-9]+/.test(str)) {
      // signpost clue
      this.signpost_clue = parseInt(str.substring(1));
      this.puzzle_elt.innerHTML = `<div class='nanro_signpost'>${this.signpost_clue}</div>`;
    } else super.load_example(str);
  }
}

function find_elf_with_func(elf, func_name) {
  let result = null;
  if (typeof elf[func_name] === "function") {
    result = elf;
  } else if (elf.hasOwnProperty("elf1")) {
    let e1 = find_elf_with_func(elf.elf1, func_name);
    result = e1 !== null ? e1 : find_elf_with_func(elf.elf2, func_name);
  }
  return result;
}

// big
class NonogramElf extends DirectSum(
  Elf,
  BgColorElf({ x: ["black", "black"], o: ["green", "green"] })
) {
  static controls() {
    let controls = super.controls();
    controls["Delete"] = "Delete last clue of cell";
    controls["[0-9]"] = "Write clue in cell";
    controls["Space"] = "Add next clue to cell";
    return controls;
  }

  constructor(elt) {
    super(elt);
    this.clue_type = /^\-1.*$/.test(elt.id) ? "top" : "left";

    this.puzzle_elt.style.display = "flex";
    this.puzzle_elt.style.flexDirection = { top: "column", left: "row" }[
      this.clue_type
    ];
    this.puzzle_elt.style.justifyContent = "flex-end";

    this.siblings = [];
    if (this.clue_type == "top")
      for (let j = -1; ; ++j) {
        let sibling_elt = get(`-1,${j}`);
        if (!sibling_elt) break;
        this.siblings.push(sibling_elt);
        this.siblings.push(get(`puzzle_-1,${j}`));
      }
    else if (this.clue_type == "left")
      for (let i = -1; ; ++i) {
        let sibling_elt = get(`${i},-1`);
        if (!sibling_elt) break;
        this.siblings.push(sibling_elt);
        this.siblings.push(get(`puzzle_${i},-1`));
      }

    this.clues = [];
    this.curr_clue = "";

    this.extend_char = { top: "<br>", left: " " }[this.clue_type];
    this.extend_attr = { top: "height", left: "width" }[this.clue_type];
  }

  true_num_clues() {
    return this.clues.length + (this.curr_clue != "" ? 1 : 0);
  }

  handle_input(key, modifiers) {
    if (!restrict_to_grid(this.elt)) {
      this.elf2.handle_input(key, modifiers); // deal with color
      return;
    }

    if (["Backspace", "Delete", "Escape"].includes(key)) {
      if (this.curr_clue == "" && this.clues.length > 0) this.clues.pop();

      this.curr_clue = "";
    }

    if (key == " " && this.curr_clue != "") {
      this.clues.push(this.curr_clue);
      this.curr_clue = "";
    }

    if ("1234567890?".includes(key))
      if (
        this.curr_clue.includes("?") ||
        key === "?" ||
        this.curr_clue.length > 1
      )
        this.curr_clue = key;
      else this.curr_clue += key;

    // resize extender dimension for all siblings, as needed
    let max_size = Math.max(1, this.true_num_clues());
    for (let elt of this.siblings)
      if (ELVES[elt.id]) {
        let elf = find_elf_with_func(ELVES[elt.id], "true_num_clues");
        max_size = Math.max(elf.true_num_clues(), max_size);
      }

    for (let elt of this.siblings)
      elt.style[this.extend_attr] = `calc(${max_size}*var(--dimension))`;

    // now put in clues
    if (this.curr_clue != "") this.clues.push(this.curr_clue);

    this.puzzle_elt.innerHTML = "";
    for (let clue of this.clues)
      this.puzzle_elt.innerHTML += `<div class='aux_cell'>${clue}</div>`;

    if (this.curr_clue != "") this.clues.pop();
  }
  load_example(str) {
    if (!restrict_to_grid(this.elt)) {
      this.elf2.load_example(str); // deal with color
      return;
    }

    this.clues = str.slice();
    this.curr_clue = "";

    let max_size = Math.max(1, this.true_num_clues());
    for (let elt of this.siblings)
      if (ELVES[elt.id]) {
        let elf = find_elf_with_func(ELVES[elt.id], "true_num_clues");
        max_size = Math.max(elf.true_num_clues(), max_size);
      }

    for (let elt of this.siblings)
      elt.style[this.extend_attr] = `${45 * max_size}px`;

    this.puzzle_elt.innerHTML = "";
    for (let clue of this.clues)
      this.puzzle_elt.innerHTML += `<div class='aux_cell'>${clue}</div>`;
  }
  encode_input() {
    let out2 = this.elf2.encode_input();

    if (this.curr_clue != "") {
      this.clues.push(this.curr_clue);
      this.curr_clue = "";
    }
    return this.clues.length == 0 ? out2 : this.clues;
  }
}

// big
class SpiralGalaxiesElf extends Elf {
  static controls() {
    // TODO
    let controls = super.controls();
    controls["q/w/e/a/s/d/z/x/c"] = "Toggle circle next to current cell";
    return controls;
  }

  handle_input(key, modifiers) {
    if (del_keys.includes(key)) {
      toggle_background_image(this.puzzle_elt, "");
      return;
    }

    let key0 = {
      w: "ArrowUp",
      a: "ArrowLeft",
      d: "ArrowRight",
      x: "ArrowDown",
    }[key];
    if ("qweasdzxc".includes(key)) {
      let neighbors = this.puzzle_neighbors();
      if (key == "q" && neighbors["nw"]) {
        // checks that this is in range
        toggle_background_image(this.puzzle_elt, "nw");
        toggle_background_image(neighbors["w"], "ne");
        toggle_background_image(neighbors["nw"], "se");
        toggle_background_image(neighbors["n"], "sw");
      }
      if (key == "w" && neighbors["n"]) {
        toggle_background_image(this.puzzle_elt, "n");
        toggle_background_image(neighbors["n"], "s");
      }
      if (key == "e" && neighbors["ne"]) {
        toggle_background_image(this.puzzle_elt, "ne");
        toggle_background_image(neighbors["e"], "nw");
        toggle_background_image(neighbors["ne"], "sw");
        toggle_background_image(neighbors["n"], "se");
      }
      if (key == "a" && neighbors["w"]) {
        toggle_background_image(this.puzzle_elt, "w");
        toggle_background_image(neighbors["w"], "e");
      }
      if (key == "s") {
        toggle_background_image(this.puzzle_elt, "white_circle");
      }
      if (key == "d" && neighbors["e"]) {
        toggle_background_image(this.puzzle_elt, "e");
        toggle_background_image(neighbors["e"], "w");
      }
      if (key == "z" && neighbors["sw"]) {
        toggle_background_image(this.puzzle_elt, "sw");
        toggle_background_image(neighbors["w"], "se");
        toggle_background_image(neighbors["sw"], "ne");
        toggle_background_image(neighbors["s"], "nw");
      }
      if (key == "x" && neighbors["s"]) {
        toggle_background_image(this.puzzle_elt, "s");
        toggle_background_image(neighbors["s"], "n");
      }
      if (key == "c" && neighbors["se"]) {
        toggle_background_image(this.puzzle_elt, "se");
        toggle_background_image(neighbors["s"], "ne");
        toggle_background_image(neighbors["se"], "nw");
        toggle_background_image(neighbors["e"], "sw");
      }
    }
  }

  load_example(str) {
    this.handle_input(str, null);
  }

  encode_input() {
    let riu = this.puzzle_elt.raw_image_url;
    if (!riu) return {};

    let i0, j0;
    if (riu == "nw") {
      i0 = this.i - 1;
      j0 = this.j - 1;
    }
    if (riu == "n") {
      i0 = this.i - 1;
      j0 = this.j;
    }
    if (riu == "ne") {
      i0 = this.i - 1;
      j0 = this.j + 1;
    }
    if (riu == "w") {
      i0 = this.i;
      j0 = this.j - 1;
    }
    if (riu == "white_circle") {
      i0 = this.i;
      j0 = this.j;
    }
    if (riu == "e") {
      i0 = this.i;
      j0 = this.j + 1;
    }
    if (riu == "sw") {
      i0 = this.i + 1;
      j0 = this.j - 1;
    }
    if (riu == "s") {
      i0 = this.i + 1;
      j0 = this.j;
    }
    if (riu == "se") {
      i0 = this.i + 1;
      j0 = this.j + 1;
    }

    let encoding = {};
    encoding[`${i0},${j0}`] = "yup";
    return encoding;
  }
}

// big
class SudokuElf extends IntElf(1, 9, "[1-9]") {
  static controls() {
    let controls = super.controls();
    controls["(Diagonal)"] = "Add rule: each diagonal contains 1-9";
    controls["(Untouch)"] =
      "Add rule: diagonally adjacent numbers can't be equal";
    controls["(Nonconsecutive)"] =
      "Add rule: diagonally adjacent numbers can't be consecutive";
    controls["(Antiknight)"] =
      "Add rule: knight's-move adjacent numbers can't be equal";
    return controls;
  }

  constructor(elt, borders, i, j) {
    super((elt = elt), borders, (i = i), (j = j));
    this._border_upkeep();
  }

  load_solution(str) {
    super.load_solution(str);
    this._border_upkeep();
  }

  async reset_solution() {
    // enforce the correct order
    await super.reset_solution();
    this._border_upkeep();
  }

  _border_upkeep() {
    if ([5, 11].includes(this.i))
      toggle_border(this.solution_borders["ArrowDown"], true);
    if ([5, 11].includes(this.j))
      toggle_border(this.solution_borders["ArrowRight"], true);
  }
}

// big
class TapaElf extends Elf {
  static controls() {
    let controls = super.controls();
    controls["[1-8]"] = "Write clue in cell";
    return controls;
  }

  constructor(elt) {
    super(elt);
    this.clues = [];
  }

  // assumes this.clues contains a nonzero clue already
  _valid_add(num) {
    let min_space = num == "?" ? 1 : num;
    for (let n of this.clues) min_space += n == "?" ? 1 : n;
    min_space += this.clues.length + 1;
    return min_space <= 8;
  }

  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);
    if (del_keys.includes(key)) this.clues = [];

    if (key == "0") this.clues = [0];
    else if ("12345678?".includes(key)) {
      let num = key == "?" ? key : parseInt(key);

      if (this.clues == [0]) this.clues = [num];
      else if (this._valid_add(num)) this.clues.push(num);
      else this.clues = [num];
    }
    this.display_clues();
  }

  display_clues() {
    if (this.clues.length == 0) this.puzzle_elt.innerHTML = "";

    if (this.clues.length == 1) this.puzzle_elt.innerHTML = this.clues[0];

    if (this.clues.length == 2)
      this.puzzle_elt.innerHTML = `
				<div class='tapa_clue tapa_2L'>${this.clues[0]}</div>
				<div class='tapa_clue tapa_2R'>${this.clues[1]}</div>
				`;

    if (this.clues.length == 3)
      this.puzzle_elt.innerHTML = `
				<div class='tapa_clue tapa_3L'>${this.clues[0]}</div>
				<div class='tapa_clue tapa_3R'>${this.clues[1]}</div>
				<div class='tapa_clue tapa_3D'>${this.clues[2]}</div>
				`;

    if (this.clues.length == 4)
      this.puzzle_elt.innerHTML = `
				<div class='tapa_clue tapa_4U'>${this.clues[0]}</div>
				<div class='tapa_clue tapa_4R'>${this.clues[1]}</div>
				<div class='tapa_clue tapa_4D'>${this.clues[2]}</div>
				<div class='tapa_clue tapa_4L'>${this.clues[3]}</div>
				`;
  }

  load_example(arr) {
    this.clues = arr;
    this.display_clues();
  }

  encode_input() {
    return this.clues.length == 0 ? null : this.clues;
  }
}

class TLLElf extends TapaElf {
  // assumes this.clues contains a nonzero clue already

  static controls() {
    let controls = super.controls();
    controls["(VisitAllGrids)"] =
      "Add rule: All grids must be visited by the loop";
    return controls;
  }

  // @Override
  _valid_add(num) {
    let min_space = num == "?" ? 1 : num;
    for (let n of this.clues) min_space += n == "?" ? 1 : n;
    return min_space <= 8;
  }

  load_example(arr) {
    this.clues = arr;
    this.display_clues();
  }
}

class YajilinElf extends DirectSum(
  DirectSum(
    IntElf(),
    ImageElf(
      {
        u: "up_arrow.png",
        r: "right_arrow.png",
        d: "down_arrow.png",
        l: "left_arrow.png",
      },
      { "[urdl]": "Add arrow to cell" }
    )
  ),
  BgColorElf({ x: ["gray", "black"] }, false)
) {
  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);
    // Clues are automatically gray.
    if ("urdl".includes(key)) {
      this.puzzle_elt.style.backgroundColor = "gray";
    }
  }

  load_example(l) {
    if (l === "gray") {
      this.elf2.load_example("gray");
    } else {
      this.elf1.elf1.load_example(l[0][0]);
      this.elf1.elf2.load_example(l[0][1]);
      this.elf2.load_example(l[1]);
    }
  }
}

class YajikazuElf extends InvertSolutionZOrder(
  DirectSum(
    DirectSum(
      IntElf(),
      ImageElf(
        {
          u: "up_arrow.png",
          r: "right_arrow.png",
          d: "down_arrow.png",
          l: "left_arrow.png",
        },
        { "[urdl]": "Add arrow to cell" }
      )
    ),
    BgColorElf({ x: ["gray", "black"], o: ["green", "white"] }, false)
  )
) {
  handle_input(key, modifiers) {
    super.handle_input(key, modifiers);
  }

  load_example(l) {
    if (l === "gray") {
      this.elf2.load_example("gray");
    } else if (l === "green") {
      this.elf2.load_example("green");
    } else if (
      l.includes("u") ||
      l.includes("r") ||
      l.includes("d") ||
      l.includes("l")
    ) {
      this.elf1.elf1.load_example(l[0]);
      this.elf1.elf2.load_example(l[1]);
    } else {
      this.elf1.elf1.load_example(l[0][0]);
      this.elf1.elf2.load_example(l[0][1]);
      this.elf2.load_example(l[1]);
    }
  }
}

class CustomElf extends Elf {
  handle_input(key, modifiers) {
    if (modifiers.shift) {
      let rg = selected_range;
      if (rg) {
        // dealing with the whole rectangle selected
        let up, down, left, right;
        if (key == "Enter") {
          up = true;
          down = true;
          left = true;
          right = true;
        }
        if (key == "ArrowUp") up = true;
        if (key == "ArrowDown") down = true;
        if (key == "ArrowLeft") left = true;
        if (key == "ArrowRight") right = true;

        for (let j = rg[2]; j <= rg[3]; j += 2) {
          if (up) ELVES[`${rg[0]},${j}`].toggle_border("ArrowUp");
          if (down) ELVES[`${rg[1]},${j}`].toggle_border("ArrowDown");
        }
        for (let i = rg[0]; i <= rg[1]; i += 2) {
          if (left) ELVES[`${i},${rg[2]}`].toggle_border("ArrowLeft");
          if (right) ELVES[`${i},${rg[3]}`].toggle_border("ArrowRight");
        }
      } else if (nav_keys.includes(key))
        // only dealing with this cell
        this.toggle_border(key);
    } else {
      this.puzzle_elt.innerHTML += key;
    }
    super.handle_input(key, modifiers);
  }

  encode_input() {
    let encoding = {};
    for (let border_id of Object.keys(this.borders))
      if (this.puzzle_borders[border_id].style.backgroundColor == "black")
        encoding[this.borders[border_id].id] = "black";
    const innerHtml = this.puzzle_elt.innerHTML;
    encoding[`${this.i},${this.j}`] = innerHtml ? innerHtml : undefined;
    return encoding;
  }
}

let elf_types = {
  lightup: AkariElf,
  aqre: DirectSum(
    InvertSolutionZOrder(IntBordersElf()),
    BgColorElf({ x: ["gray", "black"], o: ["green", "white"] }, false)
  ),
  aquarium: DirectSum(
    IntBordersElf(),
    BgColorElf({ x: ["blue", "blue"], o: ["green", "green"] })
  ),
  balance: DirectSum(IntElf(1, 99), CircleElf, (priority = "concat")),
  battleship: DirectSum(
    ImageElf(
      {
        o: "large_black_circle.png",
        u: "battleship_bottom_end.png",
        d: "battleship_top_end.png",
        l: "battleship_right_end.png",
        r: "battleship_left_end.png",
        m: "black.png",
        w: "battleship_water.png",
      },
      {
        "[oudlrm]": "Specify a part of a battleship",
        w: "Specify water",
        Note:
          "This solver uses the standard battleship fleet of 1 4-length, " +
          "2 3-length, 3 2-length, and 4 1-length ships.",
      }
    ),
    IntElf()
  ),
  binairo: IntElf(0, 1, "[0 or 1]"),
  canal: DirectSum(
    IntElf(),
    BgColorElf({ x: ["black", "black"], o: ["green", "green"] })
  ),
  castle: CastleWallElf,
  cave: DirectSum(
    IntElf(),
    BgColorElf({ x: ["black", "black"], o: ["green", "green"] })
  ),
  chocona: DirectSum(
    InvertSolutionZOrder(IntBordersElf()),
    BgColorElf({ x: ["gray", "black"], o: ["green", "white"] }, false)
  ),
  country: InvertSolutionZOrder(IntBordersElf()),
  doppelblock: DirectSum(IntElf(), BgColorElf()),
  easyas: EasyAsElf,
  fillomino: DirectSum(IntElf(), BorderElf),
  gokigen: DirectSum(
    QuestionMarkElf,
    IntElf(0, 4, "[0-4]", "center_dot"),
    "first"
  ),
  haisu: DirectSum(IntBordersElf(), LetterElf("SG"), "first"),
  hashi: DirectSum(QuestionMarkElf, IntElf(0, 8, "[0-8]"), "first"),
  heteromino: DirectSum(BgColorElf({ x: ["gray", "gray"] }), BorderElf),
  heyawake: DirectSum(
    InvertSolutionZOrder(IntBordersElf()),
    BgColorElf({ x: ["gray", "black"], o: ["green", "white"] }, false)
  ),
  hitori: DirectSum(
    IntElf(),
    BgColorElf({ x: ["black", "white"], o: ["green", "white"] }, false)
  ),
  hotaru: DirectSum(
    IntElf(),
    ImageElf(
      {
        u: "white_circle_u.png",
        r: "white_circle_r.png",
        d: "white_circle_d.png",
        l: "white_circle_l.png",
      },
      {
        "[urdl]": "Create a clue whose beam travels in the specified direction",
      }
    ),
    "compress",
    "center_dot"
  ),
  kakuro: KakuroElf,
  kurotto: DirectSum(
    IntElf(),
    BgColorElf({ x: ["black", "black"], o: ["green", "green"] })
  ),
  kurodoko: DirectSum(
    IntElf(1, 99),
    BgColorElf({ x: ["black", "black"], o: ["green", "green"] })
  ),
  lits: DirectSum(
    BorderElf,
    BgColorElf({ x: ["gray", "gray"], o: ["green", "green"] })
  ),
  magnets: MagnetsElf,
  masyu: CircleElf,
  mines: DirectSum(
    IntElf(0, 8, "[0-8]"),
    BgColorElf({ x: ["black", "black"], o: ["green", "green"] })
  ),
  moonsun: DirectSum(
    ImageElf(
      {
        m: "moon",
        s: "white_circle",
      },
      {
        m: "Put a moon",
        s: "Put a sun",
      }
    ),
    BorderElf
  ),
  nagare: DirectSum(
    ImageElf(
      {
        u: "wide_up_arrow",
        r: "wide_right_arrow",
        d: "wide_down_arrow",
        l: "wide_left_arrow",
        U: "negative_wide_up_arrow",
        R: "negative_wide_right_arrow",
        D: "negative_wide_down_arrow",
        L: "negative_wide_left_arrow",
      },
      {
        "[urdl]": "Put black (path) arrow",
        "[URDL]": "Put white (wind) arrow",
      }
    ),
    BgColorElf(),
    "first"
  ),
  nanro: NanroElf,
  ncells: DirectSum(IntElf(), BorderElf),
  nonogram: NonogramElf,
  norinori: DirectSum(
    BorderElf,
    BgColorElf({ x: ["gray", "gray"], o: ["green", "green"] })
  ),
  numlin: InvertSolutionZOrder(IntElf()),
  nuribou: DirectSum(
    IntElf(1, 99),
    BgColorElf({
      x: ["black", "black"],
      o: ["green", "green"],
      "?": ["yellow", "yellow"],
    })
  ),
  nurikabe: DirectSum(
    IntElf(1, 99),
    BgColorElf({
      x: ["black", "black"],
      o: ["green", "green"],
      "?": ["yellow", "yellow"],
    })
  ),
  nurimisaki: DirectSum(
    IntElf(1, 99),
    BgColorElf({
      x: ["black", "black"],
      o: ["green", "green"],
      "?": ["yellow", "yellow"],
    })
  ),
  onsen: DirectSum(
    QuestionMarkElf,
    InvertSolutionZOrder(IntBordersElf()),
    "first"
  ),
  ripple: IntBordersElf(),
  shakashaka: AkariElf,
  shikaku: DirectSum(DirectSum(QuestionMarkElf, IntElf(), "first"), BorderElf),
  shimaguni: DirectSum(
    InvertSolutionZOrder(IntBordersElf()),
    BgColorElf({ x: ["gray", "black"], o: ["green", "white"] }, false)
  ),
  skyscrapers: IntElf(),
  slither: DirectSum(IntElf(0, 4, "[0-4]"), LetterElf("SW"), "first"),
  spiralgalaxies: DirectSum(SpiralGalaxiesElf, BorderElf),
  starbattle: DirectSum(
    BorderElf,
    BgColorElf({ x: ["gray", "gray"], o: ["green", "green"] })
  ),
  statuepark: CircleElf,
  stostone: DirectSum(
    IntBordersElf(),
    BgColorElf({ x: ["gray", "black"], o: ["green", "white"] }, false)
  ),
  sudoku: SudokuElf,
  tapa: TapaElf,
  tasquare: DirectSum(
    IntElf(1, 99),
    BgColorElf({
      x: ["black", "black"],
      o: ["green", "green"],
      "?": ["yellow", "yellow"],
    })
  ),
  tatamibari: DirectSum(LetterElf("+-|"), BorderElf),
  tents: DirectSum(
    DirectSum(IntElf(0, 99), BgColorElf({ o: ["green", "green"] })),
    ImageElf(
      { n: "tent", e: "tree" },
      {
        n: "Place a t(EN)t",
        e: "Place a tr(EE)",
      }
    )
  ),
  tapaloop: TLLElf,
  yajilin: YajilinElf,
  yajikazu: YajikazuElf,
  yinyang: CircleElf,
};
