const presetData = {
  tetro: {
    name: "Tetrominoes",
    config: [
      { shape: "10|11|10", count: 1 },
      { shape: "11|11", count: 1 },
      { shape: "1|1|1|1", count: 1 },
      { shape: "10|10|11", count: 1 },
      { shape: "10|11|01", count: 1 },
    ],
  },
  double_tetro: {
    name: "2x Tetrominoes",
    config: [
      { shape: "10|11|10", count: 2 },
      { shape: "11|11", count: 2 },
      { shape: "1|1|1|1", count: 2 },
      { shape: "10|10|11", count: 2 },
      { shape: "10|11|01", count: 2 },
    ],
  },
  pento: {
    name: "Pentominoes",
    config: [
      { shape: "100|111|010", count: 1 },
      { shape: "1|1|1|1|1", count: 1 },
      { shape: "10|10|10|11", count: 1 },
      { shape: "1100|0111", count: 1 },
      { shape: "11|11|10", count: 1 },
      { shape: "111|010|010", count: 1 },
      { shape: "101|111", count: 1 },
      { shape: "100|100|111", count: 1 },
      { shape: "110|011|001", count: 1 },
      { shape: "010|111|010", count: 1 },
      { shape: "10|11|10|10", count: 1 },
      { shape: "110|010|011", count: 1 },
    ],
  },
  ship3: {
    name: "Ships (size 3)",
    config: [
      { shape: "1", count: 3 },
      { shape: "1|1", count: 2 },
      { shape: "1|1|1", count: 1 },
    ],
  },
  ship4: {
    name: "Ships (size 4)",
    config: [
      { shape: "1", count: 4 },
      { shape: "1|1", count: 3 },
      { shape: "1|1|1", count: 2 },
      { shape: "1|1|1|1", count: 1 },
    ],
  },
  ship5: {
    name: "Ships (size 5)",
    config: [
      { shape: "1", count: 5 },
      { shape: "1|1", count: 4 },
      { shape: "1|1|1", count: 3 },
      { shape: "1|1|1|1", count: 2 },
      { shape: "1|1|1|1|1", count: 1 },
    ],
  },
};

function toggleParamBox() {
  const parameterBox = document.getElementById("parameter_box");
  const parameterButton = document.getElementById("param");

  if (parameterBox.style.display === "none") {
    parameterBox.style.display = "inline-block";
    parameterButton.textContent = "Hide Parameters";
  } else {
    parameterBox.style.display = "none";
    parameterButton.textContent = "Show Parameters";
  }
}

function resetParamBox() {
  const puzzleType = document.getElementById("type").value;
  if (puzzleType && Object.keys(solver_metadata[puzzleType].parameters).length > 0) {
    for (const [k, v] of Object.entries(solver_metadata[puzzleType].parameters)) {
      const paramInput = document.getElementById(`param_${k}`);
      if (paramInput.type === "checkbox") paramInput.checked = v.default;
      else paramInput.value = v.default;
    }
  }
}

function makeParam(id, type, name, value) {
  const paramDiv = document.createElement("div");
  paramDiv.className = "parameter_div";

  const paramLabel = document.createElement("label");
  paramLabel.htmlFor = `param_${id}`;
  paramLabel.innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;${name}&nbsp;`;

  let paramInput = null;
  if (type === "shapeset") {
    const puzzleType = document.getElementById("type").value;
    const config = solver_metadata[puzzleType].parameters[id];

    paramInput = document.createElement("div");
    paramInput.id = `param_${id}`;
    paramInput.style.display = "inline-flex";
    paramInput.style.alignItems = "flex-start";

    const actionSelect = document.createElement("select");
    actionSelect.id = `shapeset_action_${id}`;
    actionSelect.style.textAlign = "center";
    actionSelect.style.width = "150px";

    let optionsHTML = `<option value="" disabled selected>Choose an action</option>
                       <option value="add">Add Single Shape</option>`;
    if (config.presets) {
      for (const presetKey of config.presets)
        optionsHTML += `<option value="${presetKey}">${presetData[presetKey].name} Preset</option>`;
    }
    optionsHTML += `<option value="clear">Clear All</option>`;
    actionSelect.innerHTML = optionsHTML;

    actionSelect.addEventListener("change", (e) => {
      if (e.target.value === "add") {
        addShapeRow();
      } else if (["clear", "tetro", "double_tetro", "pento", "ship3", "ship4", "ship5"].includes(e.target.value)) {
        listDiv.innerHTML = "";
        if (e.target.value !== "clear") {
          const presetKey = e.target.value;
          const presetConfig = presetData[presetKey].config;
          for (const { shape, count } of presetConfig) addShapeRow(shape, count);
        }
        updateSummary();
      }
      e.target.value = "";
    });
    paramInput.appendChild(actionSelect);

    const detailsBlock = document.createElement("details");
    const summary = document.createElement("summary");
    summary.style.minWidth = "180px";

    const summaryText = document.createElement("span");
    summaryText.textContent = "Shapes (0)";
    summary.appendChild(summaryText);
    detailsBlock.appendChild(summary);
    paramInput.appendChild(detailsBlock);

    const containerDiv = document.createElement("div");
    containerDiv.style.padding = "4px";
    containerDiv.style.marginTop = "4px";

    const listDiv = document.createElement("div");
    const addShapeRow = (shapeStr = "", qty = 1) => {
      const shapeRow = document.createElement("div");
      shapeRow.style.marginBottom = "2px";
      shapeRow.innerHTML = `
        <input type="text" class="shape_name" value="${shapeStr}" style="width: 80px;"> x
        <input type="number" class="shape_qty" value="${qty}" min="1" style="width: 30px;">
        <button type="button" class="shape_remove">&nbsp;&ndash;&nbsp;</button>
      `;
      listDiv.appendChild(shapeRow);
      updateSummary();

      const renderShapePreview = (shapeStr) => {
        const rows = shapeStr.split("|").map((row) => row.split("").map(Number));
        const cols = Math.max(...rows.map((row) => row.length));
        const px_size = 20; // pixel size per cell
        const canvas = document.createElement("canvas");
        canvas.width = cols * px_size || px_size;
        canvas.height = rows.length * px_size;

        const ctx = canvas.getContext("2d");
        rows.forEach((row, r) => {
          row.forEach((cell, c) => {
            if (cell == "1") {
              ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue("--fgMain").trim() || "black";
              ctx.fillRect(c * px_size, r * px_size, px_size, px_size);
            }
          });
        });

        return canvas;
      };

      const removeBtn = shapeRow.querySelector("button");
      removeBtn.addEventListener("mouseover", (e) => {
        const shapeStr = shapeRow.querySelector(".shape_name").value;
        if (!shapeStr) return;

        const canvas = renderShapePreview(shapeStr);
        canvas.style.position = "fixed";
        canvas.style.pointerEvents = "none";
        canvas.style.backgroundColor = "opaque";
        canvas.style.padding = "5px";
        canvas.style.zIndex = "1000";

        document.body.appendChild(canvas);
        const rect = removeBtn.getBoundingClientRect();
        canvas.style.left = rect.right + 10 + "px";
        canvas.style.top = rect.top + "px";
        canvas.dataset.preview = "true";
      });

      removeBtn.addEventListener("mouseout", () => {
        document.querySelector("canvas[data-preview='true']")?.remove();
      });

      removeBtn.addEventListener("click", () => {
        document.querySelector("canvas[data-preview='true']")?.remove();
        removeBtn.parentElement.remove();
      });
    };
    containerDiv.appendChild(listDiv);
    detailsBlock.appendChild(containerDiv);

    const updateSummary = () => {
      const count = listDiv.querySelectorAll("div").length;
      summaryText.textContent = `Shapes (${count})`;
      if (count === 0) detailsBlock.removeAttribute("open");
    };

    Object.defineProperty(paramInput, "value", {
      get: function () {
        const shapes = [];
        listDiv.querySelectorAll("div").forEach((row) => {
          const name = row.querySelector(".shape_name").value;
          const qty = parseInt(row.querySelector(".shape_qty").value, 10);
          if (name) shapes.push({ shape: name, count: qty || 1 });
        });
        return shapes;
      },
      set: function (val) {
        listDiv.innerHTML = ""; // clear list
        if (Array.isArray(val)) val.forEach((v) => addShapeRow(v.shape, v.count));
        updateSummary();
      },
    });

    if (value && Array.isArray(value)) paramInput.value = value;
    listDiv.addEventListener("click", (e) => {
      if (e.target.tagName === "BUTTON") setTimeout(updateSummary, 0);
    });
  } else {
    paramInput = document.createElement("input");
    paramInput.type = type;
    paramInput.className = "param_input";
    paramInput.id = `param_${id}`;

    if (type === "number") paramInput.min = 0;
    if (type === "checkbox") paramInput.checked = value;
    else paramInput.value = value;
  }

  paramDiv.appendChild(paramLabel);
  paramDiv.appendChild(paramInput);
  return paramDiv;
}
