function parsePenpaParam(data) {
  let param = data.split("&");
  let paramArray = {};
  for (let i = 0; i < param.length; i++) {
    let paramItem = param[i].split("=");
    paramArray[paramItem[0]] = paramItem[1];
  }
  return paramArray;
}

function exp(saveUndo = false) {
  clearInfo(); // clear every information created by penpa itself
  const undoStatus = document.getElementById("save_undo").checked;

  if (!saveUndo) {
    document.getElementById("save_undo").checked = false;
    const result = pu.maketext().split("#")[1]; // return the puzzle data without saving undo record
    if (undoStatus) document.getElementById("save_undo").checked = true; // restore undo status
    return result;
  }

  document.getElementById("save_undo").checked = true;
  let result = pu.maketext().split("#")[1];
  if (!undoStatus) document.getElementById("save_undo").checked = false; // restore undo status
  return result;
}

function hookExp() {
  const baseUrl = pu.maketext_baseurl();
  let result = exp(document.getElementById("save_undo").checked);
  let paramArray = parsePenpaParam(result);
  let rawData = decrypt_data(paramArray.p).split("\n");
  rawData[0] = rawData[0]
    .split(",")
    .map((v, i) => (i === 21 ? "" : v))
    .join(","); // clear puzzle background image
  if (rawData[7]) rawData[7] = "{}"; // clear solution metadata
  if (rawData[16]) rawData[16] = "{}"; // clear shared solution data
  if (rawData[17]) rawData[17] = "[]"; // clear genre
  if (rawData[18]) rawData[18] = ""; // clear solving comment

  paramArray.p = encrypt_data(rawData.join("\n"));
  const final = `${baseUrl}#${Object.keys(paramArray)
    .map((key) => `${key}=${paramArray[key]}`)
    .join("&")}`;
  update_textarea(final);
}

function imp(penpa, example = false) {
  let urlstring = penpa || document.getElementById("urlstring").value;
  let puzzleType = null;
  const puzzleVariants = [];

  // replace unsupported host to supported host
  urlstring = urlstring.replace("pzplus.tck.mn", "puzz.link");
  urlstring = urlstring.replace("p.html", "p");

  // pre-fetch the puzzle type for puzz.link relevant URL
  if (urlstring.match(/\/puzz.link\/p\?|pzprxs\.vercel\.app\/p\?|\/pzv\.jp\/p(\.html)?\?/)) {
    const parts = urlstring.split("?");
    const urldata = parts[1].split("/");
    puzzleType = urldata[0];
    for (let i = 1; i < urldata.length; i++) {
      if (urldata[i] && isNaN(urldata[i])) puzzleVariants.push(urldata[i]);
      else break;
    }

    for (const puzzleVariant of puzzleVariants) urlstring = urlstring.replace(`/${puzzleVariant}/`, "/");
  }

  const puzzleTypeConverter = {
    arukone: "numlin",
    chocona: "aqre",
    cityspace: "cave",
    cocktail: "aqre",
    context: "nuribou",
    coral: "nonogram",
    circlesquare: "yinyang",
    creek: "gokigen",
    dotchi2: "dotchi",
    fivecells: "nawabari",
    fourcells: "nawabari",
    heyablock: "heyawake",
    hinge: "aqre",
    island: "kurotto",
    lither: "slitherlink",
    nibunnogo: "gokigen",
    norinuri: "nuribou",
    nothing: "moonsun",
    nothree: "tentaisho",
    numlin_bit: "numlin",
    nuriuzu: "tentaisho",
    oasis: "nurimisaki",
    mannequin: "aqre",
    simplegako: "view",
    smullyan: "nuribou",
    squarejam: "shikaku",
    statuepark: "yinyang",
    suguru: "cojun",
    swslither: "slitherlink",
    tetrochain: "yajikazu",
    tslither: "slitherlink",
    vslither: "slitherlink",
  };

  if (puzzleType && puzzleType in puzzleTypeConverter) {
    urlstring = urlstring.replace(puzzleType, puzzleTypeConverter[puzzleType]);
  }

  // normalize the puzzle type
  if (puzzleType && !(puzzleType in solver_metadata)) {
    for (const [pid, data] of Object.entries(solver_metadata)) {
      if (data.aliases && data.aliases.includes(puzzleType)) {
        puzzleType = pid;
        break;
      }
    }
  }

  // interception for solver mode
  if (urlstring && urlstring.includes("m=solve")) {
    let paramArray = parsePenpaParam(urlstring.split("#")[1]);
    let rawData = decrypt_data(paramArray.p).split("\n");
    rawData[2] = rawData[11];
    rawData[4] = rawData[14];
    rawData[15] = rawData[14];
    paramArray.p = encrypt_data(rawData.join("\n"));
    paramArray.m = "edit";

    // reconstruct the URL for solver mode
    urlstring = `${urlstring.split("#")[0]}#${Object.keys(paramArray)
      .map((key) => `${key}=${paramArray[key]}`)
      .join("&")}`;
  }

  try {
    import_url(urlstring);
    const importErrorDialog = document.getElementById("swal2-html-container");
    if (puzzleType in solver_metadata) {
      resetGridType(puzzleType);
      resetGridMode(puzzleType);
      resetBoardSize(puzzleType);
    } else {
      const currentType = document.getElementById("type").value;
      resetGridType(currentType);
      resetGridMode(currentType);
      resetBoardSize(currentType);
    }

    if (importErrorDialog && importErrorDialog.textContent.startsWith("It currently does not support puzzle type")) {
      create_newboard();
      advancecontrol_toggle();

      // interception for the error message of unsupported puzzle type from penpa+
      Swal.update({ hideClass: { popup: "", backdrop: "" } });
      Swal.close(); // close the popup window itself
      decode_puzzlink_extra(urlstring);
    } else redraw_grid();
  } catch (error) {
    clearInfo();
    let errorMessage = null;
    if (!document.getElementById("type").value) {
      errorMessage = "Please select type before importing Penpa+ links.";
    } else if (puzzleType in solver_metadata || urlstring.includes("m=edit")) {
      errorMessage = "The URL may be invalid or corrupted.";
    } else {
      errorMessage = `Unsupported puzzle type: ${puzzleType}.`;
    }
    Swal.fire({
      icon: "error",
      title: "Import error",
      text: errorMessage,
    });
    return;
  }

  if (!example) {
    const exampleSelect = document.getElementById("example");
    exampleSelect.value = "";
  }

  clearInfo();
  const currentContent = exp();

  // manually set the puzzle type if pre-fetched
  if (puzzleType in solver_metadata) {
    const previousParameterBoxStatus = document.getElementById("parameter_box").style.display;
    const typeSelect = document.getElementById("type");
    typeSelect.value = puzzleType;
    typeSelect.dispatchEvent(new Event("change"));
    if (previousParameterBoxStatus === "inline-block") toggleParamBox();

    // parse variant for specific puzzle types if available
    if (puzzleVariants.includes("f")) {
      // for the visit_all parameter
      const visitAllParam = document.getElementById("param_visit_all");
      if (visitAllParam) visitAllParam.checked = true;
    }

    // parse shapeset for statuepark from URL if available
    if (puzzleType === "statuepark") {
      const actionSelect = document.getElementById("shapeset_action_shapeset");
      const convertDict = { "//p": "pento", "//d": "double_tetro", "//t": "tetro" };
      if (actionSelect) {
        let flag = true;
        for (const [key, value] of Object.entries(convertDict)) {
          if (urlstring.endsWith(key)) {
            actionSelect.value = value;
            actionSelect.dispatchEvent(new Event("change"));
            flag = false;
            break;
          }
        }
        if (flag) {
          const puzzlinkSegment = urlstring.split("/");
          const shapes = [];
          if (puzzlinkSegment[7] && puzzlinkSegment.length >= 8 + parseInt(puzzlinkSegment[7])) {
            for (let i = 0; i < parseInt(puzzlinkSegment[7]); i++) {
              const shapeStr = puzzlinkSegment[8 + i];
              const shapeColNumber = parseInt(shapeStr[0]);
              const shapeRowNumber = parseInt(shapeStr[1]);

              let shapeFullStr = "";
              for (let ch of shapeStr.slice(2)) shapeFullStr += parseInt(ch, 36).toString(2).padStart(5, "0");
              shapeFullStr = shapeFullStr.padEnd(shapeRowNumber * shapeColNumber, "0");

              let reshapedStr = "";
              for (let r = 0; r < shapeRowNumber; r++) {
                reshapedStr += shapeFullStr.slice(r * shapeColNumber, (r + 1) * shapeColNumber) + "|";
              }
              reshapedStr = reshapedStr.slice(0, -1);
              shapes.push({ shape: reshapedStr, count: 1 });
            }
            const paramInput = document.getElementById("param_shapeset");
            if (paramInput) paramInput.value = shapes;
          }
        }
      }
    }
  }

  hookLoad(currentContent);
}

function clearInfo() {
  document.getElementById("saveinfotitle").value = "";
  document.getElementById("saveinfoauthor").value = "";
  document.getElementById("saveinfosource").value = "";
  document.getElementById("saveinforules").value = "";
  document.getElementById("puzzleinfo").style.display = "none";
  document.title = "Noqx - Extended logic puzzle solver";
}

function hookUpdateDisplay() {
  for (let i = 0; i < pu.space.length; i++) {
    pu.space[i] = parseInt(document.getElementById(`nb_space${i + 1}`).value, 10);
  }
}

function hookLoad(data) {
  load(data);
  clearInfo();
}

function resetGridType(puzzleType) {
  const oldTypeFlag = document.getElementById("gridtype").value;
  let typeFlag = "square";

  if (puzzleType === "kakuro") typeFlag = "kakuro";
  if (puzzleType === "sudoku") typeFlag = "sudoku";

  if (typeFlag !== oldTypeFlag) {
    document.getElementById("gridtype").value = typeFlag; // set grid type
    changetype();
  }
}

function resetGridMode(puzzleType) {
  const puzzleCategory = solver_metadata[puzzleType].category;
  const oldModeFlag = pu.mode.grid;
  let modeFlag = ["1", "2", "1"]; // default grid mode

  if (["route", "region"].includes(puzzleCategory)) modeFlag = ["2", "2", "1"]; // route/region mode

  if (["juosan", "shakashaka", "walllogic"].includes(puzzleType)) modeFlag = ["2", "2", "1"];

  if (["cave", "cityspace", "firefly", "gokigen", "ichimaga"].includes(puzzleType)) modeFlag = ["2", "2", "2"];

  if (["hashi", "keywest"].includes(puzzleType)) modeFlag = ["3", "2", "2"];

  if (["mejilink"].includes(puzzleType)) modeFlag = ["2", "1", "2"];

  if (["lither", "myopia", "scrin", "slitherlink"].includes(puzzleType)) modeFlag = ["3", "1", "2"];

  if (modeFlag.join("_") !== oldModeFlag.join("_")) pu.mode.grid = modeFlag;
}

function resetBoardSize(puzzleType) {
  const oldSizeFlag = [
    document.getElementById("nb_space1").value, // top space
    document.getElementById("nb_space2").value, // bottom space
    document.getElementById("nb_space3").value, // left space
    document.getElementById("nb_space4").value, // right space
  ];
  let sizeFlag = [0, 0, 0, 0]; // a flag for margin size

  if (
    ["aquarium", "batten", "battleship", "doppelblock", "snake", "tents", "tilepaint", "triplace"].includes(puzzleType)
  )
    sizeFlag = [1, 0, 1, 0];

  if (
    ["anglers", "box", "creek", "easyasabc", "firefly", "gokigen", "magnets", "skyscrapers", "starbattle"].includes(
      puzzleType
    )
  )
    sizeFlag = [1, 1, 1, 1];

  if (["coral", "japanesesums", "nonogram"].includes(puzzleType)) sizeFlag = [5, 0, 5, 0];

  if (sizeFlag.join("_") !== oldSizeFlag.join("_")) {
    document.getElementById("nb_size1").value = 10 + sizeFlag[0] + sizeFlag[1]; // columns
    document.getElementById("nb_size2").value = 10 + sizeFlag[2] + sizeFlag[3]; // rows
    document.getElementById("nb_space1").value = sizeFlag[0]; // top space
    document.getElementById("nb_space2").value = sizeFlag[1]; // bottom space
    document.getElementById("nb_space3").value = sizeFlag[2]; // left space
    document.getElementById("nb_space4").value = sizeFlag[3]; // right space
  }

  return sizeFlag;
}

// detect the content change in page_settings button to avoid language check glitch
const pageSettingsButton = document.getElementById("page_settings");
if (pageSettingsButton) {
  const observer = new MutationObserver(() => {
    if (UserSettings.app_language === "EN" && pageSettingsButton.textContent !== "Settings")
      pageSettingsButton.textContent = "Settings";
  });
  observer.observe(pageSettingsButton, { childList: true, characterData: true, subtree: true });
}

$(window).on("load", function () {
  const CLINGO_WASM_URL =
    (OFFLINE_MODE ? window.location.href + local_clingo_prefix : remote_clingo_prefix) + `./clingo.wasm`;
  if (DEPLOYMENT_MODE) clingo.init(CLINGO_WASM_URL);

  // Update the exact Penpa+ link according to the hash
  const penpaLink = document.getElementById("penpa-link");
  penpaLink.href = `https://github.com/swaroopg92/penpa-edit/tree/${penpa_edit_hash}`;
  penpaLink.textContent = penpa_edit_hash.slice(0, 7);

  const urlBase = "./penpa-edit/#";
  const issueMessage =
    "Submit an issue <a href='https://github.com/T0nyX1ang/noqx/issues/new/choose' target='_blank'>here</a> to help us improve.";
  const exampleSelect = document.getElementById("example");
  const typeSelect = document.getElementById("type");
  const ruleButton = document.getElementById("rules");
  const solveButton = document.getElementById("solve");
  const resetButton = document.getElementById("solver_reset");

  const categoryName = {
    shade: "- Shading -",
    route: "- Loop / Path -",
    region: "- Area Division -",
    num: "- Number -",
    var: "- Variety -",
    unk: "- Unknown -",
  };

  const variantMap = {
    lits: { param_invlitso: "invlitso" },
    slitherlink: {
      param_tslither: "tslither",
      param_vslither: "vslither",
      param_swslither: "swslither",
    },
    ichimaga: {
      param_ichimagam: "ichimagam",
      param_ichimagax: "ichimagax",
    },
    pipelink: {
      param_pipelinkr: "pipelinkr",
    },
  };

  const customMatcher = (params, data) => {
    if ($.trim(params.term) === "") return data;
    if (typeof data.text === "undefined") return null;

    const term = params.term.toLowerCase().replace(/\s+/g, "");
    const stripper = (str) => str.toLowerCase().replace(/\s+/g, "");

    let isMatch = false;
    if (stripper(data.text).indexOf(term) > -1) isMatch = true;
    if (data.id && stripper(data.id).indexOf(term) > -1) isMatch = true;
    if (data.aliases && data.aliases.some((a) => stripper(a).indexOf(term) > -1)) isMatch = true;

    if (isMatch) return data;

    if (data.children && data.children.length > 0) {
      const match = $.extend(true, {}, data);
      for (let c = data.children.length - 1; c >= 0; c--) {
        const child = data.children[c];
        let childMatched = false;
        if (stripper(child.text).indexOf(term) > -1) childMatched = true;
        if (child.id && stripper(child.id).indexOf(term) > -1) childMatched = true;
        if (child.aliases && child.aliases.some((a) => stripper(a).indexOf(term) > -1)) childMatched = true;

        if (!childMatched) match.children.splice(c, 1);
      }
      if (match.children.length > 0) return match;
    }
    return null;
  };

  let puzzleTypeDict = {};
  for (const [k, v] of Object.entries(categoryName)) {
    puzzleTypeDict[k] = { text: v, children: [] };
  }

  let puzzleType = null;
  let puzzleContent = null;
  let solutionList = null;
  let solutionPointer = -1;
  let puzzleParameters = {};

  // solver_metadata is defined in solver_metadata.js
  for (const [ptype, pvalue] of Object.entries(solver_metadata)) {
    const typeOption = { id: ptype, text: pvalue.name, aliases: pvalue.aliases };
    puzzleTypeDict[pvalue.category].children.push(typeOption);
  }

  for (const [k, _] of Object.entries(categoryName)) {
    if (puzzleTypeDict[k].children.length === 0) delete puzzleTypeDict[k]; // remove empty category
  }

  $(typeSelect).select2({ data: Object.values(puzzleTypeDict), placeholder: "Type to search", matcher: customMatcher });
  $(exampleSelect).select2({ minimumResultsForSearch: Infinity });
  $(typeSelect).on("change", () => {
    const isPuzzleTypeChanged = puzzleType !== typeSelect.value;
    if (isPuzzleTypeChanged) $(typeSelect).val(typeSelect.value).trigger("change.select2");
    ruleButton.disabled = false;
    puzzleType = typeSelect.value;
    puzzleParameters = {};
    if (puzzleType !== "") {
      resetGridType(puzzleType);
      resetGridMode(puzzleType);
      resetBoardSize(puzzleType);
      create_newboard();
      advancecontrol_toggle();
      initParamBox();

      if (exampleSelect.value !== "" && !isPuzzleTypeChanged) return;

      $(exampleSelect).empty();
      let exampleList = [{ id: "", text: "Choose Example", selected: true }];
      exampleList.push(
        ...solver_metadata[puzzleType].examples.map((_, i) => ({
          id: String(i),
          text: `Example #${i + 1}`,
        }))
      );
      $(exampleSelect).select2({ data: exampleList, minimumResultsForSearch: Infinity });
    }
  });

  $(exampleSelect).on("change", () => {
    solveButton.disabled = false;
    solveButton.textContent = "Solve";
    if (exampleSelect.value !== "") {
      solutionList = null;
      solutionPointer = -1;

      let exampleData = solver_metadata[puzzleType].examples[exampleSelect.value];
      imp(exampleData.url ? exampleData.url : `${urlBase}${exampleData.data}`, true);

      if (Object.keys(solver_metadata[puzzleType].parameters).length > 0) {
        for (const [k, v] of Object.entries(solver_metadata[puzzleType].parameters)) {
          const config = solver_metadata[puzzleType].examples[exampleSelect.value].config;
          const value = config && config[k] !== undefined ? config[k] : v.default;
          const paramInput = document.getElementById(`param_${k}`);
          if (k === "shapeset") {
            if (value && Array.isArray(value)) paramInput.value = value;
            else if (presetData[value]) paramInput.value = presetData[value].config;
            else paramInput.value = [];
          } else if (paramInput.type === "checkbox") paramInput.checked = value;
          else paramInput.value = value;
        }
      }
    } else {
      resetBoardSize(puzzleType); // reset the board when puzzle type changes
      create_newboard();
      advancecontrol_toggle();
      resetParamBox();
    }
  });

  ruleButton.addEventListener("click", () => {
    if (ruleButton.disabled || !puzzleType) return;
    let urlPuzzleType = `https://pzprjs.vercel.app/rules.html?${
      puzzleType !== "yajilin_regions" ? puzzleType : "yajilin-regions"
    }`;
    if (puzzleType === "fillpix") urlPuzzleType = "https://www.cross-plus-a.com/html/cros7fpix.htm";
    if (puzzleType === "shingoki") urlPuzzleType = "https://www.puzzle-shingoki.com";
    if (puzzleType === "yajikabe") urlPuzzleType = "https://www.cross-plus-a.com/html/cros7yajk.htm";

    if (variantMap[puzzleType]) {
      for (const [paramId, variant] of Object.entries(variantMap[puzzleType])) {
        const element = document.getElementById(paramId);
        if (element && element.checked) {
          urlPuzzleType = `https://pzprjs.vercel.app/rules.html?${variant}`;
        }
      }
    }
    window.open(urlPuzzleType);
  });

  solveButton.addEventListener("click", async () => {
    if (!typeSelect.value) {
      Swal.fire({
        icon: "question",
        title: "Select a puzzle type",
        text: "Choose a puzzle type to solve as.",
      });
      return;
    }

    puzzleType = typeSelect.value;

    if (solutionPointer === -1) {
      puzzleContent = exp(true);
      $(typeSelect).prop("disabled", true);
      $(typeSelect)
        .next(".select2-container")
        .find(".select2-selection__rendered")
        .attr("title", "Reset the puzzle to change puzzle type.");
      $(exampleSelect).prop("disabled", true);
      $(exampleSelect)
        .next(".select2-container")
        .find(".select2-selection__rendered")
        .attr("title", "Reset the puzzle to change example.");
      solveButton.textContent = "Solving...";
      solveButton.disabled = true;

      if (Object.keys(solver_metadata[puzzleType].parameters).length > 0) {
        for (const [k, _] of Object.entries(solver_metadata[puzzleType].parameters)) {
          const paramInput = document.getElementById(`param_${k}`);
          if (paramInput.type === "checkbox") puzzleParameters[k] = paramInput.checked;
          else puzzleParameters[k] = paramInput.value;
        }
      } else {
        puzzleParameters = {}; // reset parameters
      }

      if (DEPLOYMENT_MODE) {
        try {
          const puzzle = prepare_puzzle(puzzleType, puzzleContent, puzzleParameters);
          if (!puzzle["success"]) {
            throw new Error(puzzle["result"]);
          }

          const program = generate_program(puzzle["result"]);
          if (!program["success"]) {
            throw new Error(program["result"]);
          }

          const options = "--trans-ext=dynamic --eq=1 --models=10";
          const result = await clingo.run(program["result"], options);

          if (result.Result === "ERROR") {
            console.error(result.Error);
            throw new Error("Clingo program error.");
          }

          if (result.Result === "UNSATISFIABLE") {
            throw new Error("No solution found.");
          }

          const puz_name = solver_metadata[puzzleType].name;
          console.info(`[Solver] ${puz_name} puzzle solved.`);
          console.info(`[Solver] ${puz_name} solver took ${result.Time.Total} seconds.`);

          solutionList = [];
          for (const solution_data of result.Call[0].Witnesses) {
            const solution = store_solution(puzzle["result"], solution_data.Value.join(" "));
            if (!solution["success"]) {
              throw new Error(solution["result"]);
            }

            solutionList.push(solution["result"]);
          }

          solutionPointer = 0;
          hookLoad(solutionList[solutionPointer]);
        } catch (e) {
          console.log(e);

          Swal.fire({
            icon: "error",
            title: "Error",
            text: e.message,
            footer: issueMessage,
          });
        } finally {
          if (solutionList) {
            solveButton.textContent = `Solution (${solutionPointer + 1}/${
              solutionList.length === 10 ? "10+" : solutionList.length
            })`;
            solveButton.disabled = solutionList.length === 1 || solutionList.length === 0;
          }
        }
      } else {
        fetch("/api/solve/", {
          method: "POST",
          body: JSON.stringify({
            puzzle_name: puzzleType,
            puzzle: puzzleContent,
            param: puzzleParameters,
          }),
          headers: { "Content-type": "application/json" },
        })
          .then(async (response) => {
            let body = await response.json();
            if (response.status === 400 || response.status === 500) {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: body.detail || "Unknown error.",
                footer: issueMessage,
              });
              solveButton.textContent = "Solve";
              return;
            } else if (response.status === 504) {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Time limit exceeded.",
                footer: issueMessage,
              });
              solveButton.textContent = "Solve";
              return;
            } else {
              solutionList = body.url;
              if (solutionList.length === 0) {
                Swal.fire({
                  icon: "error",
                  title: "Oops...",
                  text: "No solution found.",
                  footer: issueMessage,
                });
                return;
              }
              solutionPointer = 0;
              hookLoad(solutionList[solutionPointer]);
            }
          })
          .catch((e) => {
            Swal.fire({
              icon: "question",
              title: "Unexpected error",
              text: e,
              footer: issueMessage,
            });
          })
          .finally(() => {
            solveButton.textContent = `Solution (${solutionPointer + 1}/${
              solutionList.length === 10 ? "10+" : solutionList.length
            })`;
            solveButton.disabled = solutionList.length === 1 || solutionList.length === 0;
          });
      }
    } else {
      solutionPointer++;
      if (solutionPointer >= solutionList.length) {
        solutionPointer = 0;
      }
      solveButton.textContent = `Solution (${solutionPointer + 1}/${
        solutionList.length === 10 ? "10+" : solutionList.length
      })`;
      hookLoad(solutionList[solutionPointer]);
    }
  });

  resetButton.addEventListener("click", async () => {
    if (puzzleContent !== null) {
      if (DEPLOYMENT_MODE && solveButton.textContent === "Solving..." && solveButton.disabled === true) {
        await clingo.restart(CLINGO_WASM_URL); // reinitialize clingo-wasm
      }
      hookLoad(puzzleContent);
      $(typeSelect).prop("disabled", false);
      $(typeSelect).next(".select2-container").find(".select2-selection__rendered").removeAttr("title");
      $(exampleSelect).prop("disabled", false);
      $(exampleSelect).next(".select2-container").find(".select2-selection__rendered").removeAttr("title");
    } else {
      create_newboard();
      advancecontrol_toggle();
      resetParamBox();
      $(exampleSelect).val("").trigger("change.select2");
    }
    puzzleContent = null;
    solutionList = [];
    solutionPointer = -1;
    solveButton.textContent = "Solve";
    solveButton.disabled = false;
  });

  const undoButton = document.getElementById("tb_undo");
  if (undoButton) {
    const updateChoicesType = () => {
      if (undoButton.disabled && (!solutionList || solutionList.length === 0)) {
        $(typeSelect).prop("disabled", false);
        $(typeSelect).next(".select2-container").find(".select2-selection__rendered").removeAttr("title");
        $(exampleSelect).prop("disabled", false);
        $(exampleSelect).next(".select2-container").find(".select2-selection__rendered").removeAttr("title");
      } else {
        $(typeSelect).prop("disabled", true);
        $(typeSelect)
          .next(".select2-container")
          .find(".select2-selection__rendered")
          .attr("title", "Reset the puzzle to change puzzle type.");
        $(exampleSelect).prop("disabled", true);
        $(exampleSelect)
          .next(".select2-container")
          .find(".select2-selection__rendered")
          .attr("title", "Reset the puzzle to change example.");
      }
    };

    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === "attributes" && mutation.attributeName === "disabled") {
          updateChoicesType();
        }
      });
    });
    observer.observe(undoButton, { attributes: true });
  }

  document.addEventListener("click", () => focus());
});
