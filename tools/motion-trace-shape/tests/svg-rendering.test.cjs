/* Targeted markup regression, CC BY 4.0. Real rendering is checked separately. */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

for (const filename of ['index.html', 'Motion-Trace-Shape.html']) {
  test(`${filename}: time axes never default to a filled polygon`, () => {
    const html = fs.readFileSync(path.join(__dirname, '..', filename), 'utf8');
    const svg = html.match(/<svg id="timeSvg"[^>]*>([\s\S]*?)<\/svg>/);
    assert.ok(svg, 'time plot must be present');
    const axes = svg[1].match(/<g stroke="#b7c9c9"[^>]*>([\s\S]*?)<\/g>/);
    assert.ok(axes, 'time axes must be present');
    const paths = axes[1].match(/<path\b[^>]*>/g);
    assert.ok(paths?.length, 'time axes must contain drawing paths');
    for (const element of paths) {
      assert.match(element, /\bfill="none"/, 'Open axis paths must not close into an opaque triangle');
    }
  });
}
