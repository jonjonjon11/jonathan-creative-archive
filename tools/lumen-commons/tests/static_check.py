"""Deterministic, dependency-free checks for the runtime and standalone package."""
from pathlib import Path
import base64
import hashlib
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'Lumen-Commons-Play.html').read_text(encoding='utf-8')
assert len(html.encode())<250_000, 'Prototype exceeds initial 250 KB budget'
for match in re.finditer(r'<(script|style)>(.*?)</\1>',html,re.S):
    payload=match.group(2)
    digest=base64.b64encode(hashlib.sha256(payload.encode()).digest()).decode()
    assert "'sha256-"+digest+"'" in html, 'CSP hash missing'
assert "connect-src 'none'" in html and "default-src 'none'" in html
assert 'unsafe-eval' not in html and 'unsafe-inline' not in html
runtime='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'src').glob('*.js'))
for pattern in [r'\beval\s*\(',r'\bfetch\s*\(',r'new\s+WebSocket',r'XMLHttpRequest',r'\.innerHTML\s*=',r'getUserMedia',r'navigator\.geolocation']:
    assert not re.search(pattern,runtime), 'Prohibited runtime pattern: '+pattern
before=html
subprocess.run([sys.executable,str(ROOT/'build_single.py')],check=True)
assert before==(ROOT/'Lumen-Commons-Play.html').read_text(encoding='utf-8'), 'Standalone was stale: regenerate it'
print('Static checks passed: source/build parity, CSP hashes, <250 KB budget, no prohibited runtime APIs.')
