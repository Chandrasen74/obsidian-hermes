/* Render exact frames of the layup piece: node render-layup.mjs <outdir> [f0,f1,...] | all */
import { chromium } from "file:///C:/Users/Kanchan%20Verma/OneDrive/Desktop/Opencode/01-Projects/projects/animate/node_modules/playwright/index.mjs";
import { mkdirSync } from "node:fs";
import path from "node:path";

const PIECE = process.argv[2] || "all";
const OUT = process.argv[3];
const frames = PIECE === "all"
  ? Array.from({ length: 180 }, (_, i) => i)
  : PIECE.split(",").map(Number);
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
for (const f of frames) {
  await page.goto(`file:///C:/Users/Kanchan%20Verma/AppData/Local/Temp/opencode/agent-ws/stickman-layup/index.html?f=${f}`);
  await page.waitForFunction(() => window.__done === true);
  const cv = page.locator("#cv");
  await cv.screenshot({ path: path.join(OUT, `f${String(f).padStart(5, "0")}.png`) });
}
await browser.close();
console.log(`rendered ${frames.length} frames -> ${OUT}`);
