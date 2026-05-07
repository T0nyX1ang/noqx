const penpa_edit_hash = "7785887bbc7f985a387199989e2c7d76efec4dab";
const remote_penpa_prefix = `https://cdn.jsdelivr.net/gh/swaroopg92/penpa-edit@${penpa_edit_hash}/docs/`;
const local_penpa_prefix = `./requires/core/${penpa_edit_hash}/`;

// stylesheet loading
const style_sources_ids = [
  "color_theme",
  "base_structure",
  "tab_setting_css",
  "custom_color_css",
  "constraints_settings_css",
];
const style_tag_cache = {
  color_theme: "link#color_theme",
  base_structure: "link#base_structure",
  tab_setting_css: "link#tab_setting_css",
  custom_color_css: "link#custom_color_css",
  constraints_settings_css: "link#constraints_settings_css",
};
const penpa_style_sources = [
  "./css/base-structure.css",
  "./css/vanillaSelectBox.css",
  "./css/spectrum.css",
  "./css/select2.css",
];
for (let i = 0; i < penpa_style_sources.length; i++) {
  const style = document.createElement("link");
  style.rel = "stylesheet";
  style.type = "text/css";
  style.id = style_sources_ids[i + 1];
  style.href = (OFFLINE_MODE ? local_penpa_prefix : remote_penpa_prefix) + penpa_style_sources[i];
  style.async = false;
  document.head.appendChild(style);
  style_tag_cache[style_sources_ids[i + 1]] = style;
}

const noqx_style_sources = ["./css/light_theme.css", "./css/style.css"];
for (let i = 0; i < noqx_style_sources.length; i++) {
  const style = document.createElement("link");
  style.rel = "stylesheet";
  style.type = "text/css";
  style.href = noqx_style_sources[i];
  style.async = false;
  if (i === 0) {
    style.id = style_sources_ids[i];
    style_tag_cache[style_sources_ids[i]] = style;
  }
  document.head.appendChild(style);
}

// script loading
const penpa_script_sources = [
  "./js/libs/jquery-3.7.0.min.js",
  "./js/libs/localforage.min.js",
  "./js/libs/md5.min.js",
  "./js/libs/sweetalert2@11.js",
  "./js/libs/purify.min.js",
  "./js/libs/CanvasRenderingContext2D.ext.js",
  "./js/libs/encoding.js",
  "./js/libs/vanillaSelectBox.js",
  "./js/libs/zlib.js",
  "./js/libs/spectrum.js",
  "./js/libs/canvas2svg.js",
  "./js/libs/select2.full.js",
  "./js/libs/gif.js",
  "./js/libs/easytimer.min.js",
  "./js/settings.js",
  "./js/progress.js",
  "./js/interface.js",
  "./js/conflicts.js",
  "./js/puzzlink.js",
  "./js/modes.js",
  "./js/genre_tags.js",
  "./js/constraints.js",
  "./js/main.js",
  "./js/class_p.js",
  "./js/class_square.js",
  "./js/class_hex.js",
  "./js/class_tri.js",
  "./js/class_pyramid.js",
  "./js/class_uniform.js",
  "./js/class_panel.js",
  "./js/style.js",
  "./js/general.js",
  "./js/customcolor.js",
  "./js/translate.js",
  "./js/timer.js",
  "./js/conversion.js",
];
for (let i = 0; i < penpa_script_sources.length; i++) {
  const script = document.createElement("script");
  script.type = "text/javascript";
  script.src = (OFFLINE_MODE ? local_penpa_prefix : remote_penpa_prefix) + penpa_script_sources[i];
  script.async = false;
  document.head.appendChild(script);
}

const noqx_script_sources = ["./js/app.js", "./js/solver_metadata.js"];
for (let i = 0; i < noqx_script_sources.length; i++) {
  const script = document.createElement("script");
  script.type = "text/javascript";
  script.src = noqx_script_sources[i];
  script.async = false;
  document.head.appendChild(script);
}

if (DEPLOYMENT_MODE) {
  const pyscript_version = "2026.3.1";
  const remote_pyscript_prefix = `https://pyscript.net/releases/${pyscript_version}/`;
  const local_pyscript_prefix = `./pyscript/`;

  const py_script = document.createElement("script");
  py_script.type = "module";
  py_script.src = (OFFLINE_MODE ? local_pyscript_prefix : remote_pyscript_prefix) + "./core.js";
  py_script.async = false;
  document.head.appendChild(py_script);

  const py_link = document.createElement("link");
  py_link.rel = "stylesheet";
  py_link.href = (OFFLINE_MODE ? local_pyscript_prefix : remote_pyscript_prefix) + "./core.css";
  py_link.async = false;
  document.head.appendChild(py_link);

  const user_script = document.createElement("script");
  user_script.type = "mpy";
  user_script.src = "./py/main_deploy.py";
  user_script.async = false;
  user_script.setAttribute("config", "./pyscript.json");
  document.head.appendChild(user_script);

  const clingo_script = document.createElement("script");
  clingo_script.type = "module";
  clingo_script.src = "https://cdn.jsdelivr.net/npm/clingo-wasm@0.3.2/dist/clingo.web.js";
  clingo_script.async = false;
  document.head.appendChild(clingo_script);
}

// message config
const Identity = {
  appOwner: "Noqx",
  okButtonText: "ok 🙂",
  errorTitle: "Noqx says",
  infoTitle: "Noqx says",
  solveTitle: undefined,
  solveDefaultMessage: "Congratulations 🙂", // Default - Congratulations 🙂
  solveOKButtonText: "Hurray!",
  incorrectMessage: "Keep trying 🙂",
  addUsageButtons: {},
};
