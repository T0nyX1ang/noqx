const ENABLE_DEPLOYMENT = false;

if (ENABLE_DEPLOYMENT) {
  const script = document.createElement("script");
  script.type = "module";
  script.src = "https://pyscript.net/releases/2025.2.4/core.js";
  script.async = false;
  document.head.appendChild(script);

  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "https://pyscript.net/releases/2025.2.4/core.css";
  document.head.appendChild(link);

  const user_script = document.createElement("script");
  user_script.type = "py";
  user_script.src = "./main_deploy.py";
  user_script.async = false;
  user_script.setAttribute("config", "./pyscript.json");
  document.head.appendChild(user_script);
}
