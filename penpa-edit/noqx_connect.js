$(document).ready(function () {
  const urlBase = "./penpa-edit/#";
  const issueMessage =
    "Submit an issue <a href='https://github.com/T0nyX1ang/noqx/issues/new/choose' target='_blank'>here</a> to help us improve.";
  const typeSelect = document.getElementById("type");
  const solveButton = document.getElementById("solve");
  const resetButton = document.getElementById("solver_reset");

  let puzzleName = null;
  let puzzleContent = null;
  let solutionList = null;
  let solutionPointer = -1;
  let puzzleParameters = {};

  solveButton.addEventListener("click", () => {
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
      solveButton.textContent = "Solving...";
      solveButton.disabled = true;

      if (solver_metadata[puzzleName].parameters) {
        for (const [k, _] of Object.entries(solver_metadata[puzzleName].parameters)) {
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
      imp(puzzleContent.includes(urlBase) ? puzzleContent : `${urlBase}${puzzleContent}`);
    } else {
      create_newboard();
      advancecontrol_toggle();
      advancecontrol_toggle();
    }
    puzzleContent = null;
    solutionList = [];
    solutionPointer = -1;
    solveButton.textContent = "Solve";
    solveButton.disabled = false;
  });
});
