const fs = require("fs");

const PATCHES = {

  TEST_PATCH: {
    file: "voynich.html",
    marker: "<!-- NAVI_PATCH_TEST -->",
    content: `
<!-- NAVI_PATCH_TEST -->
<div style="padding:10px;background:#0f172a;border:1px solid #334155;margin-top:10px;">
  <strong>NAVI PATCH TEST OK</strong>
</div>
`
  }

};

function applyPatch(patchName){
  const patch = PATCHES[patchName];

  if(!patch){
    console.log("❌ Patch not found:", patchName);
    return;
  }

  let html = fs.readFileSync(patch.file, "utf8");

  if(html.includes(patch.marker)){
    console.log("⚠️ Patch already exists:", patchName);
    return;
  }

  // wstawiamy przed </body>
  html = html.replace("</body>", patch.content + "\n</body>");

  fs.writeFileSync(patch.file, html);

  console.log("✅ Patch applied:", patchName);
}

const patchName = process.argv[2];
applyPatch(patchName);