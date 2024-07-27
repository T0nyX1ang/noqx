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

  let foundGrid = null;
  let foundUrl = null;
  let puzzle_type = null;
  let puzzle_content = null;

  fetch("/api/list").then((response) => {
    response.json().then((body) => {
      for (const [ptype, pvalue] of Object.entries(body)) {
        const typeOption = document.createElement("option");
        typeOption.value = ptype;
        typeOption.text = pvalue.name;
        typeSelect.add(typeOption);
      }

      typeSelect.addEventListener("change", () => {
        puzzle_type = typeSelect.value;
        if (puzzle_type !== "") {
          for (let i = exampleSelect.options.length - 1; i > 0; i--)
            exampleSelect.remove(i); // remove all options except the first one

          for (let i = 0; i < body[puzzle_type].examples.length; i++) {
            const exampleOption = document.createElement("option");
            exampleOption.value = i;
            exampleOption.text = `Example ${i + 1}`;
            exampleSelect.add(exampleOption);
          }
        }
      });

      exampleSelect.addEventListener("change", () => {
        if (exampleSelect.value !== "") {
          puzzle_content = body[puzzle_type].examples[exampleSelect.value];
          imp(puzzle_content);
        }
      });

      solveButton.addEventListener("click", () => {
        if (!typeSelect.value) {
          alert("Choose a puzzle type to solve as.");
          return;
        }
        solveButton.textContent = "Solving...";
        solveButton.disabled = true;
        fetch("/api/solve", {
          method: "POST",
          body: JSON.stringify({
            puzzle_type: puzzle_type,
            puzzle: exp(),
          }),
          headers: { "Content-type": "application/json" },
        })
          .then(async (response) => {
            let body = await response.json();
            if (response.status == 400) {
              alert(body.detail);
            } else if (response.status == 500) {
              alert("An unknown error occurred.");
            } else if (response.status == 503) {
              alert("The server is too busy. Please try again later.");
            } else {
              if (body.url === null) {
                alert(
                  foundGrid ? "No other solution found." : "No solution found."
                );
                return;
              }
              iframe.contentWindow.load(body.url);
              foundGrid = body.grid;
              foundUrl = exp();
            }
          })
          .catch((e) => {
            alert("Unexpected error: " + e);
          })
          .finally(() => {
            solveButton.textContent =
              exp() === foundUrl ? "Find another solution" : "Solve";
            solveButton.disabled = false;
          });
      });
    });
  });

  iframe.contentWindow.document.addEventListener("click", () =>
    iframe.contentWindow.focus()
  );

  setInterval(() => {
    if (solveButton.textContent !== "Solving..." && exp() !== foundUrl) {
      foundGrid = null;
      foundUrl = null;
      solveButton.textContent = "Solve";
    }
  }, 1000);
};
