function exp() {
  return iframe.contentWindow.pu.maketext().split("#")[1];
}

function imp(penpa) {
  iframe.contentWindow.load(penpa);
}

window.onload = function () {
  const iframe = document.getElementById("iframe");
  const exampleSelect = document.getElementById("example");
  const typeSelect = document.getElementById("type");
  const solveButton = document.getElementById("solve");
  const resetButton = document.getElementById("solver_reset");
  const readmeButton = document.getElementById("readme");

  let foundUrl = null;
  let puzzleType = null;
  let puzzleContent = null;
  let Swal = iframe.contentWindow.Swal;
  let solutionList = null;
  let solutionPointer = -1;

  fetch("/api/list").then((response) => {
    response.json().then((body) => {
      for (const [ptype, pvalue] of Object.entries(body)) {
        const typeOption = document.createElement("option");
        typeOption.value = ptype;
        typeOption.text = pvalue.name;
        typeSelect.add(typeOption);
      }

      typeSelect.addEventListener("change", () => {
        puzzleType = typeSelect.value;
        if (puzzleType !== "") {
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
          puzzleContent = body[puzzleType].examples[exampleSelect.value];
          imp(puzzleContent);
        }
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
          fetch("/api/solve", {
            method: "POST",
            body: JSON.stringify({
              puzzle_type: puzzleType,
              puzzle: puzzleContent,
            }),
            headers: { "Content-type": "application/json" },
          })
            .then(async (response) => {
              let body = await response.json();
              if (response.status === 400 || response.status === 500) {
                Swal.fire({
                  icon: "error",
                  title: "Oops...",
                  text: body.detail,
                });
              } else if (response.status === 503) {
                Swal.fire({
                  icon: "error",
                  title: "Oops...",
                  text: "The server is too busy. Please try again later.",
                });
              } else {
                solutionList = body.url;
                if (solutionList.length === 0) {
                  Swal.fire({
                    icon: "error",
                    title: "Oops...",
                    text: "No solution found.",
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
          imp(puzzleContent);
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
        Swal.fire({
          icon: "info",
          title: "Noqx - Extended logic puzzle solver",
          html: '<a href="https://github.com/T0nyX1ang/noqx">Noqx</a> by <a href="https://github.com/T0nyX1ang/">T0nyX1ang</a> and <a href="https://github.com/zhuyaoyu/">zyy</a> using <a href="https://github.com/potassco/clingo">clingo</a> <br> Original <a href="https://noq.solutions">Noq</a> project by <a href="https://github.com/jenna-h/">Jenna</a> and <a href="https://mstang.xyz">Michael</a> using <a href="https://github.com/danyq/claspy">claspy</a> <br> General layout and encoding by <a href="https://github.com/kevinychen/nikoli-puzzle-solver">nikoli-puzzle-solver</a> <br>',
          footer: "Licensed under GPL-3",
        });
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
