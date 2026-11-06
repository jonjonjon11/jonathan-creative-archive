"""Build a dependency-free, one-file demo with strict hash-based CSP."""
from pathlib import Path
import base64
import hashlib
import re
ROOT = Path(__file__).resolve().parent
html = (ROOT / 'index.html').read_text(encoding='utf-8')
css = (ROOT / 'src/style.css').read_text(encoding='utf-8')
parts = [(ROOT / ('src/' + name)).read_text(encoding='utf-8') for name in ('core.js', 'world.js', 'game.js')]
sha = lambda s: "'sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode() + "'"
html = html.replace("script-src 'self'", 'script-src ' + ' '.join(sha(s) for s in parts))
html = html.replace("style-src 'self'", 'style-src ' + sha(css))
html = html.replace('<link rel="stylesheet" href="src/style.css">', '<style>' + css + '</style>')
html = re.sub(r'<script defer src="src/[^\"]+"></script>\n?', '', html)
html = html.replace('</body>', ''.join('<script>' + s + '</script>' for s in parts) + '</body>')
out = ROOT / 'Lumen-Commons-Play.html'
out.write_text(html, encoding='utf-8', newline='\n')
print(f'{out}: {out.stat().st_size:,} bytes')
