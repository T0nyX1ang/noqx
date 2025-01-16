function exp() {
  clear_info(); // clear every information created by penpa itself
  document.getElementById("save_undo").checked = true;
  let result = pu.maketext().split("#")[1];
  document.getElementById("save_undo").checked = false;
  return result;
}

function imp(penpa) {
  let urlstring = penpa || document.getElementById("urlstring").value;

  // replace unsupported solver to supported solvers
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

  import_url(urlstring);
  clear_info();
}

function clear_info() {
  document.getElementById("saveinfotitle").value = "";
  document.getElementById("saveinfoauthor").value = "";
  document.getElementById("saveinfosource").value = "";
  document.getElementById("saveinforules").value = "";
  document.getElementById("puzzleinfo").style.display = "none";
}

function hook_update_display() {
  for (let i = 0; i < pu.space.length; i++) {
    pu.space[i] = parseInt(document.getElementById(`nb_space${i + 1}`).value, 10);
  }
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

$(document).ready(function () {
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

  let puzzleSearchBoxInput = document.querySelector(".choices__input.choices__input--cloned");
  puzzleSearchBoxInput.id = "select2_search"; // spoof penpa+ to type words in the search box

  fetch("/api/list/").then((response) => {
    response.json().then((body) => {
      for (const [ptype, pvalue] of Object.entries(body)) {
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
          parameterBox.style.display = "none"; // hide parameter box if no parameters
          parameterButton.textContent = "Show parameters";
          parameterButton.disabled = true;
          while (parameterBox.firstChild) {
            parameterBox.removeChild(parameterBox.lastChild);
          }

          if (body[puzzleName].parameters) {
            parameterButton.disabled = false;
            for (const [k, v] of Object.entries(body[puzzleName].parameters)) {
              const paramDiv = make_param(k, v.type, v.name, v.default);
              parameterBox.appendChild(paramDiv);
            }
          }

          choicesExample.clearStore();
          let exampleList = [{ value: "", label: "Choose Example", selected: true }];
          exampleList.push(...body[puzzleName].examples.map((_, i) => ({ value: i, label: `Example #${i + 1}` })));
          choicesExample.setChoices(exampleList);
        }
      });

      exampleSelect.addEventListener("change", () => {
        solveButton.disabled = false;
        solveButton.textContent = "Solve";
        if (exampleSelect.value !== "") {
          solutionList = null;
          solutionPointer = -1;

          let exampleData = body[puzzleName].examples[exampleSelect.value];
          puzzleContent = exampleData.url ? exampleData.url : `${urlBase}${exampleData.data}`;
          imp(puzzleContent, exampleData.url !== undefined);

          if (body[puzzleName].parameters) {
            for (const [k, v] of Object.entries(body[puzzleName].parameters)) {
              const config = body[puzzleName].examples[exampleSelect.value].config;
              const value = config && config[k] !== undefined ? config[k] : v.default;
              const paramInput = document.getElementById(`param_${k}`);
              if (paramInput.type === "checkbox") paramInput.checked = value;
              else paramInput.value = value;
            }
          }
        }
      });

      ruleButton.addEventListener("click", () => {
        if (ruleButton.disabled || !puzzleName) return;
        window.open(
          `https://puzz.link/rules.html?${puzzleName !== "yajilin_regions" ? puzzleName : "yajilin-regions"}`
        );
      });

      solveButton.addEventListener("click", () => {
        if (!typeSelect.value) {
          Swal.fire({
            icon: "question",
            title: "Select a puzzle type",
            text: "Choose a puzzle type to solve as.",
          });
          return;
        }

        if (solutionPointer === -1) {
          puzzleContent = exp();
          solveButton.textContent = "Solving...";
          solveButton.disabled = true;

          if (body[puzzleName].parameters) {
            for (const [k, _] of Object.entries(body[puzzleName].parameters)) {
              const paramInput = document.getElementById(`param_${k}`);
              if (paramInput.type === "checkbox") puzzleParameters[k] = paramInput.checked;
              else puzzleParameters[k] = paramInput.value;
            }
          }

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
                load(solutionList[solutionPointer]);
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
              choicesExample.setChoiceByValue("");
              solveButton.textContent = `Solution (${solutionPointer + 1}/${
                solutionList.length === 10 ? "10+" : solutionList.length
              })`;
              solveButton.disabled = solutionList.length === 1 || solutionList.length === 0;
            });
        } else {
          solutionPointer++;
          if (solutionPointer >= solutionList.length) {
            solutionPointer = 0;
          }
          solveButton.textContent = `Solution (${solutionPointer + 1}/${
            solutionList.length === 10 ? "10+" : solutionList.length
          })`;
          load(solutionList[solutionPointer]);
        }
      });

      resetButton.addEventListener("click", () => {
        if (puzzleContent !== null) {
          imp(`${urlBase}${puzzleContent}`);
        } else {
          pu.reset_board();
          pu.redraw();
        }
        puzzleContent = null;
        solutionList = [];
        solutionPointer = -1;
        solveButton.textContent = "Solve";
        solveButton.disabled = false;
      });
    });
  });

  document.addEventListener("click", () => focus());
});
