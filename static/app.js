function exp() {
  return pu.maketext().split("#")[1];
}

function imp(penpa) {
  import_url(penpa);
}

function make_param(id, type, name, value) {
  let paramDiv = document.createElement("div");

  let paramLabel = document.createElement("label");
  paramLabel.for = `param_${name}`;
  paramLabel.textContent = `${name} `;

  let paramInput = null;
  if (type !== "select") {
    paramInput = document.createElement("input");
    paramInput.type = type;
    paramInput.className = "param_input";
    paramInput.id = `param_${id}`;

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

  const categoryName = {
    shade: "- Shading -",
    loop: "- Loop / Path -",
    region: "- Area Division -",
    num: "- Number -",
    var: "- Variety -",
    draw: "- Drawing -",
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
  });

  let foundUrl = null;
  let puzzleType = null;
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
      choicesType.setChoices(Object.values(puzzleTypeDict));

      typeSelect.addEventListener("change", () => {
        ruleButton.disabled = false;
        puzzleType = typeSelect.value;
        if (puzzleType !== "") {
          parameterBox.style.display = "none"; // hide parameter box if no parameters
          while (parameterBox.firstChild) {
            parameterBox.removeChild(parameterBox.lastChild);
          }

          if (body[puzzleType].parameters) {
            let legendElement = document.createElement("legend");
            legendElement.textContent = "Parameters";
            parameterBox.appendChild(legendElement);

            for (const [k, v] of Object.entries(body[puzzleType].parameters)) {
              const paramDiv = make_param(k, v.type, v.name, v.default);
              parameterBox.appendChild(paramDiv);
            }

            parameterBox.style.display = "block";
          }

          choicesExample.clearChoices();
          let exampleList = [{ value: "", label: "Choose Example", selected: true }];
          exampleList.push(...body[puzzleType].examples.map((_, i) => ({ value: i, label: `Example #${i + 1}` })));
          choicesExample.setChoices(exampleList);
        }
      });

      exampleSelect.addEventListener("change", () => {
        solveButton.disabled = false;
        if (exampleSelect.value !== "") {
          solutionList = null;
          solutionPointer = -1;

          let exampleData = body[puzzleType].examples[exampleSelect.value];
          puzzleContent = exampleData.url ? exampleData.url : `${urlBase}${exampleData.data}`;
          imp(puzzleContent, exampleData.url !== undefined);

          if (body[puzzleType].parameters) {
            for (const [k, v] of Object.entries(body[puzzleType].parameters)) {
              const config = body[puzzleType].examples[exampleSelect.value].config;
              const value = config && config[k] !== undefined ? config[k] : v.default;
              const paramInput = document.getElementById(`param_${k}`);
              if (paramInput.type === "checkbox") paramInput.checked = value;
              else paramInput.value = value;
            }
          }
        }
      });

      ruleButton.addEventListener("click", () => {
        if (ruleButton.disabled || !puzzleType) return;
        window.open(`https://puzz.link/rules.html?${puzzleType !== "ncells" ? puzzleType : "fivecells"}`);
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

          if (body[puzzleType].parameters) {
            for (const [k, _] of Object.entries(body[puzzleType].parameters)) {
              const paramInput = document.getElementById(`param_${k}`);
              if (paramInput.type === "checkbox") puzzleParameters[k] = paramInput.checked;
              else puzzleParameters[k] = paramInput.value;
            }
          }

          fetch("/api/solve/", {
            method: "POST",
            body: JSON.stringify({
              puzzle_type: puzzleType,
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
                foundUrl = null;
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
                foundUrl = exp();
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
          foundUrl = exp();
        }
      });

      resetButton.addEventListener("click", () => {
        if (puzzleContent !== null) {
          imp(`${urlBase}${puzzleContent}`);
          foundUrl = null;
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

  setInterval(() => {
    if (solveButton.textContent !== "Solving..." && foundUrl !== null && exp() !== foundUrl) {
      foundUrl = null;
      solveButton.textContent = "Solve";
    }
  }, 200);
});
