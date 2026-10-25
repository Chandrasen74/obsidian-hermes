// Renders all 180 frames of index.html to frames/frame_00000.png .. frame_00179.png
// Usage: node render.cjs [startFrame endFrame]   (defaults 0 179)
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const start = parseInt(process.argv[2] || '0', 10);
  const end = parseInt(process.argv[3] || '179', 10);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  for (let f = start; f <= end; f++) {
    const url = 'file://' + path.resolve(__dirname, 'index.html') + '?f=' + f;
    await page.goto(url);
    await page.waitForFunction('window.__done === true');
    const out = path.resolve(__dirname, 'frames', 'frame_' + String(f).padStart(5, '0') + '.png');
    await page.locator('#cv').screenshot({ path: out });
    if (f % 15 === 0 || f === end) console.log('rendered frame', f);
  }
  await browser.close();
  console.log('DONE', start, end);
})();
