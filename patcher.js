const fs = require("fs");

function insertAfter(html, target, content){
  if(!html.includes(target)){
    console.log("❌ Target not found");
    return html;
  }
  return html.replace(target, target + "\n" + content);
}

function applyPatch({file, id, target, content}){

  let html = fs.readFileSync(file, "utf8");

  if(html.includes(id)){
    console.log("⚠️ Patch already exists:", id);
    return;
  }

  html = insertAfter(html, target, content);

  fs.writeFileSync(file, html);

  console.log("✅ Patch applied:", id);
}

const PATCHES = {

  ADD_BUTTON_UNDER_RUN: {
    file: "voynich.html",
    id: "PATCH_BUTTON_UNDER_RUN",
    target: '<button id="runButton" type="button">Translate / Read</button>',
    content: `
<!-- PATCH_BUTTON_UNDER_RUN -->
<button style="margin-top:10px;background:#00ffaa;color:black;padding:8px 12px;border-radius:6px;border:none;">
  NEW NAVI BUTTON
</button>
`
  }

};

const name = process.argv[2];

if(!PATCHES[name]){
  console.log("❌ Patch not found");
} else {
  applyPatch(PATCHES[name]);
}