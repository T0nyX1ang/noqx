const ENABLE_DEPLOYMENT = false;

if (ENABLE_DEPLOYMENT) {
  const clingo_script = document.createElement("script");
  clingo_script.type = "module";
  clingo_script.src = "https://cdn.jsdelivr.net/npm/clingo-wasm@0.3.2/dist/clingo.web.js";
  clingo_script.async = false;
  document.head.appendChild(clingo_script);

  const py_script = document.createElement("script");
  py_script.type = "module";
  py_script.src = "https://pyscript.net/releases/2026.3.1/core.js";
  py_script.async = false;
  document.head.appendChild(py_script);

  const py_link = document.createElement("link");
  py_link.rel = "stylesheet";
  py_link.href = "https://pyscript.net/releases/2026.3.1/core.css";
  document.head.appendChild(py_link);

  const user_script = document.createElement("script");
  user_script.type = "mpy";
  user_script.src = "./py/main_deploy.py";
  user_script.async = false;
  user_script.setAttribute("config", "./pyscript.json");
  document.head.appendChild(user_script);
}
