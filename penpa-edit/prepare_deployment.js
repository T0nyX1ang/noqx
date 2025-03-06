const ENABLE_DEPLOYMENT = false;

if (ENABLE_DEPLOYMENT) {
  const CLINGO_SRC = ["./clingo.web.js", "./clingo.web.worker.js"];
  for (const src_name of CLINGO_SRC) {
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src = src_name;
    script.async = false;
    document.head.appendChild(script);
  }

  const BRYTHON_SRC = ["./brython.js", "./brython_modules.js"];
  for (const src_name of BRYTHON_SRC) {
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src = src_name;
    script.async = false;
    document.head.appendChild(script);
  }

  const user_script = document.createElement("script");
  user_script.type = "py";
  user_script.src = "./main_deploy.py";
  user_script.async = false;
  document.head.appendChild(user_script);
}
