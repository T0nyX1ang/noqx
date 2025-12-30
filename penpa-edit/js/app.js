function exp() {
  clear_info(); // clear every information created by penpa itself
  document.getElementById("save_undo").checked = true;
  let result = pu.maketext().split("#")[1];
  document.getElementById("save_undo").checked = false;
  return result;
}

function imp(penpa, load_info = true) {
  let urlstring = penpa || document.getElementById("urlstring").value;

  // replace unsupported solver to supported solvers
  urlstring = urlstring.replace("arukone", "numlin");
  urlstring = urlstring.replace("chocona", "aqre");
  urlstring = urlstring.replace("cocktail", "aqre");
  urlstring = urlstring.replace("context", "nuribou");
  urlstring = urlstring.replace("coral", "nonogram");
  urlstring = urlstring.replace("circlesquare", "yinyang");
  urlstring = urlstring.replace("creek", "gokigen");
  urlstring = urlstring.replace("fivecells", "nawabari");
  urlstring = urlstring.replace("fourcells", "nawabari");
  urlstring = urlstring.replace("heyablock", "heyawake");
  urlstring = urlstring.replace("hinge", "aqre");
  urlstring = urlstring.replace("norinuri", "nuribou");
  urlstring = urlstring.replace("nothing", "moonsun");
  urlstring = urlstring.replace("nothree", "tentaisho");
  urlstring = urlstring.replace("nuriuzu", "tentaisho");
  urlstring = urlstring.replace("simplegako", "view");
  urlstring = urlstring.replace("squarejam", "shikaku");
  urlstring = urlstring.replace("statuepark", "yinyang");
  urlstring = urlstring.replace("swslither", "slitherlink");
  urlstring = urlstring.replace("tetrochain", "yajikazu");
  urlstring = urlstring.replace("tslither", "slitherlink");
  urlstring = urlstring.replace("vslither", "slitherlink");

  // replace unsupported host to supported host
  urlstring = urlstring.replace("pzplus.tck.mn", "puzz.link");

  // interception for solver mode
  if (urlstring && urlstring.includes("m=solve")) {
    Swal.fire({
      icon: "error",
      title: "Import error",
      text: "SOLVER/CONTEST mode is not supported in noqx. Please export in EDIT mode.",
    });
    return;
  }

  try {
    import_url(urlstring);
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Import error",
      text: "The URL may be invalid or corrupted.",
    });
    return;
  }

  clear_info();
  if (load_info) hook_load(exp()); // load twice to extract the information
}

function clear_info() {
  document.getElementById("saveinfotitle").value = "";
  document.getElementById("saveinfoauthor").value = "";
  document.getElementById("saveinfosource").value = "";
  document.getElementById("saveinforules").value = "";
  document.getElementById("puzzleinfo").style.display = "none";
  document.title = "Noqx - Extended logic puzzle solver";
}

function hook_update_display() {
  for (let i = 0; i < pu.space.length; i++) {
    pu.space[i] = parseInt(document.getElementById(`nb_space${i + 1}`).value, 10);
  }
}

function hook_load(data) {
  load(data);
  clear_info();
}

function invoke_param_box() {
  const parameterBox = document.getElementById("parameter_box");
  const parameterButton = document.getElementById("param");

  if (parameterBox.style.display === "none") {
    parameterBox.style.display = "inline-block";
    parameterButton.textContent = "Hide parameters";
  } else {
    parameterBox.style.display = "none";
    parameterButton.textContent = "Show parameters";
  }
}

function make_param(id, type, name, value) {
  let paramDiv = document.createElement("div");
  paramDiv.className = "parameter_div";

  let paramLabel = document.createElement("label");
  paramLabel.for = `param_${name}`;
  paramLabel.innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;${name}&nbsp;`;

  let paramInput = null;
  if (type !== "select") {
    paramInput = document.createElement("input");
    paramInput.type = type;
    paramInput.className = "param_input";
    paramInput.id = `param_${id}`;

    if (type === "number") {
      paramInput.min = 0;
    }
    if (type === "checkbox") paramInput.checked = value;
    else paramInput.value = value;
  } else {
    paramInput = document.createElement("select");
    paramInput.id = `param_${id}`;
    for (const [k, v] of Object.entries(value)) {
      let option = document.createElement("option");
      option.value = k;
      option.text = v;
      paramInput.appendChild(option);
    }
  }

  paramDiv.appendChild(paramLabel);
  paramDiv.appendChild(paramInput);
  return paramDiv;
}

function reset_grid_type(puzzleType, oldTypeFlag = "square") {
  let typeFlag = "square";

  if (puzzleType === "kakuro") typeFlag = "kakuro";
  if (puzzleType === "sudoku") typeFlag = "sudoku";

  if (typeFlag !== oldTypeFlag) {
    document.getElementById("gridtype").value = typeFlag; // grid type
    changetype();
  }
  return typeFlag;
}

function reset_grid_mode(puzzleType, oldModeFlag = ["1", "2", "1"]) {
  let modeFlag = ["1", "2", "1"]; // default grid mode
  const puzzleCategory = solver_metadata[puzzleType].category;

  if (["loop", "region"].includes(puzzleCategory)) modeFlag = ["2", "2", "1"]; // loop/region mode

  if (["juosan", "shakashaka", "walllogic"].includes(puzzleType)) modeFlag = ["2", "2", "1"];

  if (["cave", "firefly", "gokigen"].includes(puzzleType)) modeFlag = ["2", "2", "2"];

  if (["hashi"].includes(puzzleType)) modeFlag = ["3", "2", "2"];

  if (["mejilink"].includes(puzzleType)) modeFlag = ["2", "1", "2"];

  if (["myopia", "slitherlink"].includes(puzzleType)) modeFlag = ["3", "1", "2"];

  if (modeFlag.join("_") !== oldModeFlag.join("_")) pu.mode.grid = modeFlag;
  return modeFlag;
}

function reset_board_size(puzzleType, oldSizeFlag = 0) {
  let sizeFlag = 0; // a flag for extra margin sum

  document.getElementById("nb_space1").value = 0; // over space
  document.getElementById("nb_space2").value = 0; // under space
  document.getElementById("nb_space3").value = 0; // left space
  document.getElementById("nb_space4").value = 0; // right space

  if (["aquarium", "battleship", "doppelblock", "snake", "tents", "tilepaint", "triplace"].includes(puzzleType)) {
    sizeFlag = 1;
    document.getElementById("nb_space1").value = 1; // over space
    document.getElementById("nb_space3").value = 1; // left space
  }

  if (
    ["anglers", "box", "creek", "easyasabc", "firefly", "gokigen", "magnets", "skyscrapers", "starbattle"].includes(
      puzzleType
    )
  ) {
    sizeFlag = 2;
    document.getElementById("nb_space1").value = 1; // over space
    document.getElementById("nb_space2").value = 1; // under space
    document.getElementById("nb_space3").value = 1; // left space
    document.getElementById("nb_space4").value = 1; // right space
  }

  if (["coral", "nonogram"].includes(puzzleType)) {
    sizeFlag = 5;
    document.getElementById("nb_space1").value = 5; // over space
    document.getElementById("nb_space3").value = 5; // left space
  }

  if (sizeFlag !== oldSizeFlag) {
    document.getElementById("nb_size1").value = 10 + sizeFlag; // columns
    document.getElementById("nb_size2").value = 10 + sizeFlag; // rows
  }

  return sizeFlag;
}

$(window).on("load", function () {
  const CLINGO_WASM_URL = `https://cdn.jsdelivr.net/npm/clingo-wasm@0.3.2/dist/clingo.wasm`;
  if (ENABLE_DEPLOYMENT) {
    clingo.init(CLINGO_WASM_URL);
  }

  const urlBase = "./penpa-edit/#";
  const issueMessage =
    "Submit an issue <a href='https://github.com/T0nyX1ang/noqx/issues/new/choose' target='_blank'>here</a> to help us improve.";
  const exampleSelect = document.getElementById("example");
  const typeSelect = document.getElementById("type");
  const ruleButton = document.getElementById("rules");
  const solveButton = document.getElementById("solve");
  const resetButton = document.getElementById("solver_reset");
  const parameterBox = document.getElementById("parameter_box");
  const parameterButton = document.getElementById("param");

  const categoryName = {
    shade: "- Shading -",
    loop: "- Loop / Path -",
    region: "- Area Division -",
    num: "- Number -",
    var: "- Variety -",
    unk: "- Unknown -",
  };

  const choicesType = new Choices(typeSelect, {
    itemSelectText: "",
    searchFields: ["label", "value", "customProperties.aliases"],
    searchResultLimit: 5,
    searchPlaceholderValue: "Type to search",
    shouldSort: false,
  });
  let puzzleTypeDict = {};
  for (const [k, v] of Object.entries(categoryName)) {
    puzzleTypeDict[k] = { label: v, choices: [] };
  }

  const choicesExample = new Choices(exampleSelect, {
    itemSelectText: "",
    searchEnabled: false,
    noChoicesText: "No examples found",
  });

  let puzzleName = null;
  let puzzleContent = null;
  let solutionList = null;
  let solutionPointer = -1;
  let puzzleParameters = {};
  let puzzleGridTypeFlag = "square";
  let puzzleBoardSizeFlag = 0;
  let puzzleGridModeFlag = ["1", "2", "1"];

  let puzzleSearchBoxInput = document.querySelector(".choices__input.choices__input--cloned");
  puzzleSearchBoxInput.id = "select2_search"; // spoof penpa+ to type words in the search box

  // solver_metadata is defined in solver_metadata.js
  for (const [ptype, pvalue] of Object.entries(solver_metadata)) {
    typeOption = {
      value: ptype,
      label: pvalue.name,
      customProperties: { aliases: pvalue.aliases },
    };
    puzzleTypeDict[pvalue.category].choices.push(typeOption);
  }

  for (const [k, _] of Object.entries(categoryName)) {
    if (puzzleTypeDict[k].choices.length === 0) delete puzzleTypeDict[k]; // remove empty category
  }

  choicesType.setChoices(Object.values(puzzleTypeDict));

  typeSelect.addEventListener("change", () => {
    ruleButton.disabled = false;
    puzzleName = typeSelect.value;
    if (puzzleName !== "") {
      let newgridTypeFlag = reset_grid_type(puzzleName, puzzleGridTypeFlag); // reset the grid type when puzzle type changes
      puzzleGridTypeFlag = newgridTypeFlag;

      let newBoardSizeFlag = reset_board_size(puzzleName, puzzleBoardSizeFlag); // reset the board when puzzle type changes
      puzzleBoardSizeFlag = newBoardSizeFlag;

      let newGridModeFlag = reset_grid_mode(puzzleName, puzzleGridModeFlag); // reset the grid mode when puzzle type changes
      puzzleGridModeFlag = newGridModeFlag;

      create_newboard();
      advancecontrol_toggle();

      parameterBox.style.display = "none"; // hide parameter box if no parameters
      parameterButton.textContent = "Show parameters";
      parameterButton.disabled = true;
      while (parameterBox.firstChild) {
        parameterBox.removeChild(parameterBox.lastChild);
      }

      if (Object.keys(solver_metadata[puzzleName].parameters).length > 0) {
        parameterButton.disabled = false;
        for (const [k, v] of Object.entries(solver_metadata[puzzleName].parameters)) {
          const paramDiv = make_param(k, v.type, v.name, v.default);
          parameterBox.appendChild(paramDiv);
        }
      }

      choicesExample.clearStore();
      let exampleList = [{ value: "", label: "Choose Example", selected: true }];
      exampleList.push(
        ...solver_metadata[puzzleName].examples.map((_, i) => ({
          value: i,
          label: `Example #${i + 1}`,
        }))
      );
      choicesExample.setChoices(exampleList);
    }
  });

  exampleSelect.addEventListener("change", () => {
    solveButton.disabled = false;
    solveButton.textContent = "Solve";
    if (exampleSelect.value !== "") {
      solutionList = null;
      solutionPointer = -1;

      let exampleData = solver_metadata[puzzleName].examples[exampleSelect.value];
      imp(exampleData.url ? exampleData.url : `${urlBase}${exampleData.data}`);

      if (Object.keys(solver_metadata[puzzleName].parameters).length > 0) {
        for (const [k, v] of Object.entries(solver_metadata[puzzleName].parameters)) {
          const config = solver_metadata[puzzleName].examples[exampleSelect.value].config;
          const value = config && config[k] !== undefined ? config[k] : v.default;
          const paramInput = document.getElementById(`param_${k}`);
          if (paramInput.type === "checkbox") paramInput.checked = value;
          else paramInput.value = value;
        }
      }
    } else {
      reset_board_size(puzzleName); // reset the board when puzzle type changes
      create_newboard();
      advancecontrol_toggle();
    }
  });

  ruleButton.addEventListener("click", () => {
    if (ruleButton.disabled || !puzzleName) return;
    window.open(`https://puzz.link/rules.html?${puzzleName !== "yajilin_regions" ? puzzleName : "yajilin-regions"}`);
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

    puzzleName = typeSelect.value;

    if (solutionPointer === -1) {
      puzzleContent = exp();
      choicesType.disable();
      choicesType.containerOuter.element.setAttribute("title", "Reset the puzzle to change puzzle type.");
      choicesExample.disable();
      choicesExample.containerOuter.element.setAttribute("title", "Reset the puzzle to change example.");
      solveButton.textContent = "Solving...";
      solveButton.disabled = true;

      if (Object.keys(solver_metadata[puzzleName].parameters).length > 0) {
        for (const [k, _] of Object.entries(solver_metadata[puzzleName].parameters)) {
          const paramInput = document.getElementById(`param_${k}`);
          if (paramInput.type === "checkbox") puzzleParameters[k] = paramInput.checked;
          else puzzleParameters[k] = paramInput.value;
        }
      } else {
        puzzleParameters = {}; // reset parameters
      }

      if (ENABLE_DEPLOYMENT) {
        try {
          const puzzle = prepare_puzzle(puzzleName, puzzleContent, puzzleParameters);
          if (!puzzle["success"]) {
            throw new Error(puzzle["result"]);
          }

          const program = generate_program(puzzle["result"]);
          if (!program["success"]) {
            throw new Error(program["result"]);
          }

          const options = "--sat-prepro --trans-ext=dynamic --eq=1 --models=10";
          const result = await clingo.run(program["result"], options);

          if (result.Result === "ERROR") {
            console.error(result.Error);
            throw new Error("Clingo program error.");
          }

          if (result.Result === "UNSATISFIABLE") {
            throw new Error("No solution found.");
          }

          const puz_name = solver_metadata[puzzleName].name;
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
          hook_load(solutionList[solutionPointer]);
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
            puzzle_name: puzzleName,
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
              hook_load(solutionList[solutionPointer]);
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
      hook_load(solutionList[solutionPointer]);
    }
  });

  resetButton.addEventListener("click", async () => {
    if (puzzleContent !== null) {
      if (ENABLE_DEPLOYMENT && solveButton.textContent === "Solving..." && solveButton.disabled === true) {
        await clingo.restart(CLINGO_WASM_URL); // reinitialize clingo-wasm
      }
      hook_load(puzzleContent);
      choicesType.enable();
      choicesType.containerOuter.element.removeAttribute("title");
      choicesExample.enable();
      choicesExample.containerOuter.element.removeAttribute("title");
    } else {
      create_newboard();
      advancecontrol_toggle();
      choicesExample.setChoiceByValue("");
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
      const choicesContainer = choicesType.containerOuter.element;
      const choicesExampleContainer = choicesExample.containerOuter.element;
      if (undoButton.disabled) {
        if (!solutionList || solutionList.length === 0) {
          choicesType.enable();
          choicesContainer.removeAttribute("title");
          choicesExample.enable();
          choicesExampleContainer.removeAttribute("title");
        } else {
          choicesType.disable();
          choicesContainer.setAttribute("title", "Reset the puzzle to change puzzle type.");
          choicesExample.disable();
          choicesExampleContainer.setAttribute("title", "Reset the puzzle to change example.");
        }
      } else {
        choicesType.disable();
        choicesContainer.setAttribute("title", "Reset the puzzle to change puzzle type.");
        choicesExample.disable();
        choicesExampleContainer.setAttribute("title", "Reset the puzzle to change example.");
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
