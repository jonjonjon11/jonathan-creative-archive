#!/usr/bin/env python3
"""Build a deterministic, offline HTML file using only Python's standard library."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'Motion-Trace-Shape.html'

def build():
    text = (ROOT / 'index.html').read_text(encoding='utf-8')
    css = (ROOT / 'src/style.css').read_text(encoding='utf-8')
    text = text.replace('<link rel="stylesheet" href="src/style.css">', '<style>\n' + css + '</style>')
    for name in ('core', 'app'):
        js = (ROOT / f'src/{name}.js').read_text(encoding='utf-8')
        if '</script' in js.lower():
            raise ValueError('Script contains an HTML script closing tag.')
        text = text.replace(f'<script src="src/{name}.js"></script>', '<script>\n' + js + '</script>')
    return text

if __name__ == '__main__':
    OUTPUT.write_text(build(), encoding='utf-8')
    print(f'Built {OUTPUT.name} ({OUTPUT.stat().st_size:,} bytes)')
