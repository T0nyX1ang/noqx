function exp() {
  return iframe.contentWindow.pu.maketext().split("#")[1];
}

function imp(penpa) {
  iframe.contentWindow.import_url(penpa);
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

window.onload = function () {
  const iframe = document.getElementById("iframe");
  const urlBase = "./penpa-edit/#";
  const issueMessage =
    "Submit an issue <a href='https://github.com/T0nyX1ang/noqx/issues/new/choose' target='_blank'>here</a> to help us improve.";
  const exampleSelect = document.getElementById("example");
  const typeSelect = document.getElementById("type");
  const ruleButton = document.getElementById("rules");
  const solveButton = document.getElementById("solve");
  const resetButton = document.getElementById("solver_reset");
  const readmeButton = document.getElementById("readme");
  const parameterBox = document.getElementById("parameter_box");

  let foundUrl = null;
  let puzzleType = null;
  let puzzleContent = null;
  let Swal = iframe.contentWindow.Swal;
  let solutionList = null;
  let solutionPointer = -1;
  let puzzleParameters = {};

  fetch("/api/list").then((response) => {
    response.json().then((body) => {
      for (const [ptype, pvalue] of Object.entries(body)) {
        let categorySelect = document.getElementById(`type_${pvalue.category}`);
        const typeOption = document.createElement("option");
        typeOption.value = ptype;
        typeOption.text = pvalue.name;
        categorySelect.append(typeOption);
      }

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
          for (let i = exampleSelect.options.length - 1; i > 0; i--)
            exampleSelect.remove(i); // remove all options except the first one

          for (let i = 0; i < body[puzzleType].examples.length; i++) {
            const exampleOption = document.createElement("option");
            exampleOption.value = i;
            exampleOption.text = `Example ${i + 1}`;
            exampleSelect.add(exampleOption);
          }
        }
      });

      exampleSelect.addEventListener("change", () => {
        solveButton.disabled = false;
        if (exampleSelect.value !== "") {
          solutionList = null;
          solutionPointer = -1;

          let exampleData = body[puzzleType].examples[exampleSelect.value];
          puzzleContent = exampleData.url
            ? exampleData.url
            : `${urlBase}${exampleData.data}`;
          imp(puzzleContent, exampleData.url !== undefined);

          if (body[puzzleType].parameters) {
            for (const [k, v] of Object.entries(body[puzzleType].parameters)) {
              const config =
                body[puzzleType].examples[exampleSelect.value].config;
              const value =
                config && config[k] !== undefined ? config[k] : v.default;
              const paramInput = document.getElementById(`param_${k}`);
              if (paramInput.type === "checkbox") paramInput.checked = value;
              else paramInput.value = value;
            }
          }
        }
      });

      ruleButton.addEventListener("click", () => {
        if (ruleButton.disabled || !puzzleType) return;
        window.open(
          `https://puzz.link/rules.html?${
            puzzleType !== "ncells" ? puzzleType : "fivecells"
          }`
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

          if (body[puzzleType].parameters) {
            for (const [k, _] of Object.entries(body[puzzleType].parameters)) {
              const paramInput = document.getElementById(`param_${k}`);
              if (paramInput.type === "checkbox")
                puzzleParameters[k] = paramInput.checked;
              else puzzleParameters[k] = paramInput.value;
            }
          }

          fetch("/api/solve", {
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
              } else {
                solutionList = body.url;
                if (solutionList.length === 0) {
                  Swal.fire({
                    icon: "error",
                    title: "Oops...",
                    text: "No solution found or time limit exceeded.",
                    footer: issueMessage,
                  });
                  return;
                }
                solutionPointer = 0;
                iframe.contentWindow.load(solutionList[solutionPointer]);
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
              exampleSelect.value = "";
              solveButton.textContent = `Solution (${solutionPointer + 1}/${
                solutionList.length === 10 ? "10+" : solutionList.length
              })`;
              solveButton.disabled = solutionList.length === 1;
            });
        } else {
          solutionPointer++;
          if (solutionPointer >= solutionList.length) {
            solutionPointer = 0;
          }
          solveButton.textContent = `Solution (${solutionPointer + 1}/${
            solutionList.length === 10 ? "10+" : solutionList.length
          })`;
          iframe.contentWindow.load(solutionList[solutionPointer]);
          foundUrl = exp();
        }
      });

      resetButton.addEventListener("click", () => {
        if (foundUrl && puzzleContent !== null) {
          imp(`${urlBase}${puzzleContent}`);
          foundUrl = null;
        } else {
          iframe.contentWindow.pu.reset_board();
          iframe.contentWindow.pu.redraw();
        }
        puzzleContent = null;
        solutionList = [];
        solutionPointer = -1;
        solveButton.textContent = "Solve";
        solveButton.disabled = false;
      });

      readmeButton.addEventListener("click", () => {
        window.open("https://github.com/T0nyX1ang/noqx");
      });
    });
  });

  iframe.contentWindow.document.addEventListener("click", () =>
    iframe.contentWindow.focus()
  );

  setInterval(() => {
    if (solveButton.textContent !== "Solving..." && exp() !== foundUrl) {
      foundUrl = null;
      solveButton.textContent = "Solve";
    }
  }, 200);
};
