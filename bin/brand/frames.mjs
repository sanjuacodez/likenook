import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire(process.cwd() + '/package.json');
const { chromium } = require('playwright-core');
const [id, size, out, frames, duration] = [process.argv[2], +process.argv[3], process.argv[4], +process.argv[5], +process.argv[6]];
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ channel: 'chrome' });
const p = await (await b.newContext({ viewport: { width: 600, height: 600 }, deviceScaleFactor: 1 })).newPage();
await p.goto(process.argv[7] ? 'file://' + process.argv[7] : 'file://' + process.cwd() + '/bin/brand/icon.html');
await p.evaluate(([id, size]) => { const s = document.getElementById(id); s.setAttribute('width', size); s.setAttribute('height', size); }, [id, size]);
const el = p.locator('#' + id);
for (let i = 0; i < frames; i++) {
  const t = (i / (frames - 1)) * duration;
  await p.evaluate(([id, t]) => window.render(id, t), [id, t]);
  await el.screenshot({ path: `${out}/f${String(i).padStart(3, '0')}.png` });
}
await b.close();
