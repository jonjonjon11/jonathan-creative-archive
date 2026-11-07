#!/usr/bin/env python3
"""Offline build, local-reference and targeted source checks; not browser acceptance."""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_single', ROOT / 'build_single.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert (ROOT / 'Motion-Trace-Shape.html').read_text(encoding='utf-8') == module.build(), 'Standalone build is stale.'

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.labels=[]; self.refs=[]; self.linked=[]; self.lang=None; self.csp=''
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='html': self.lang=a.get('lang')
        if tag=='label' and 'for' in a: self.labels.append(a['for'])
        for attr in ['aria-labelledby','aria-describedby']:
            self.refs.extend(a.get(attr,'').split())
        if tag=='script' and 'src' in a: self.linked.append(a['src'])
        if tag=='link' and 'href' in a: self.linked.append(a['href'])
        if tag=='meta' and a.get('http-equiv')=='Content-Security-Policy': self.csp=a['content']

for name in ['index.html','Motion-Trace-Shape.html']:
    text=(ROOT/name).read_text(encoding='utf-8'); parser=Inspect();parser.feed(text)
    assert parser.lang=='en'
    assert len(parser.ids)==len(set(parser.ids)), 'Duplicate IDs'
    assert all(i in parser.ids for i in parser.labels+parser.refs), 'Broken label or ARIA reference'
    assert "connect-src 'none'" in parser.csp and "object-src 'none'" in parser.csp
    assert not re.search(r'on(?:click|load|input|change)\s*=', text, re.I), 'Unexpected inline event handler'
    if name.startswith('Motion'): assert not parser.linked, 'Standalone has runtime asset dependencies'
    else:
        for ref in parser.linked: assert (ROOT/ref).is_file(), ref

js='\n'.join((ROOT/'src'/f).read_text(encoding='utf-8') for f in ['core.js','app.js'])
for token in ['fetch(', 'XMLHttpRequest', 'WebSocket', 'sendBeacon', 'localStorage', 'sessionStorage', 'document.cookie', 'eval(', 'new Function']:
    assert token not in js, f'Unexpected network/storage/execution API: {token}'
assert 'visibilitychange' in js and 'prefers-reduced-motion: reduce' in js
assert 'cancelAnimationFrame' in js
css=(ROOT/'src/style.css').read_text(encoding='utf-8')
assert 'max-width:760px' in css and ':focus-visible' in css and 'min-height:46px' in css

def luminance(hex_color):
    values=[int(hex_color[i:i+2],16)/255 for i in [1,3,5]]
    rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(a*b for a,b in zip(rgb,[.2126,.7152,.0722]))
for fg,bg in [('#142c34','#fffef8'),('#445e66','#fffef8'),('#006d77','#fffef8'),('#ab3a30','#fffef8'),('#c7dbdc','#102e39'),('#ffe18a','#102e39'),('#ffffff','#006d77')]:
    a,b=sorted([luminance(fg),luminance(bg)])
    assert (b+.05)/(a+.05)>=4.5, f'Insufficient chosen text-color contrast: {fg}/{bg}'
print('PASS: deterministic build parity, unique IDs, label/ARIA targets, local assets, standalone independence, restrictive connect/object CSP, selected network/storage absence, motion/focus/responsive hooks, and seven text color pairs (4.5:1 minimum).')
print('These source checks do not establish rendered layout, assistive-technology support, browser security or WCAG conformance.')
