#!/usr/bin/env python3
"""Optional real-browser smoke test. Needs Playwright + a supported local Chromium.
This checks browser behavior, not a screen-reader audit or physical touch device.
Run: python3 tests/browser_smoke.py [--chromium /path/to/chromium] [--screenshots DIR]
No packages are installed by this script. No HTTP server is needed.
"""
from pathlib import Path
import argparse
import json
import tempfile
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--chromium')
parser.add_argument('--screenshots', type=Path)
args=parser.parse_args()
with sync_playwright() as p:
    options={'headless':True}
    if args.chromium: options['executable_path']=args.chromium
    browser=p.chromium.launch(**options)
    for filename in ['index.html','Motion-Trace-Shape.html']:
        context=browser.new_context(viewport={'width':1280,'height':1000},reduced_motion='reduce',accept_downloads=True)
        context.set_offline(True)
        page=context.new_page(); errors=[]; external=[]
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda req: external.append(req.url) if req.url.startswith(('http://','https://')) else None)
        page.goto((ROOT/filename).as_uri())
        expect(page.locator('#shapeGuide')).to_have_attribute('d',__import__('re').compile('^M'))
        expect(page.locator('#still')).to_be_checked(); expect(page.locator('#play')).to_be_disabled()
        expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')
        page.locator('#step').click(); expect(page.locator('#timeValue')).to_have_text('0.125 / 8 s')
        page.locator('#time').focus(); page.keyboard.press('End'); expect(page.locator('#timeValue')).to_have_text('8.000 / 8 s')
        page.keyboard.press('Home');expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')
        page.locator('#preset-eight').click(); expect(page.locator('#yCycles')).to_have_value('2')
        expect(page.locator('#shapeName')).to_have_text('Figure-eight')
        page.locator('#xCycles').focus(); page.keyboard.press('ArrowRight');expect(page.locator('#xCycles')).to_have_value('2')
        page.locator('#preset-circle').click(); page.locator('#guide').uncheck()
        expect(page.locator('#shapeGuide')).to_have_attribute('visibility','hidden')
        page.locator('#still').uncheck();page.locator('#play').click();page.wait_for_timeout(250);page.locator('#play').click()
        assert float(page.locator('#time').input_value())>0
        frozen=page.locator('#time').input_value();page.wait_for_timeout(100);assert page.locator('#time').input_value()==frozen
        page.locator('#restart').click();expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')
        page.locator('#step').click()
        with page.expect_download() as info: page.locator('#export').click()
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'experiment.json';info.value.save_as(target);record=json.loads(target.read_text())
            assert record['model']['sampling']['sample_count']==481
            assert record['presentation']['time']==.125
        assert not errors, errors
        assert not external, external
        if args.screenshots:
            args.screenshots.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(args.screenshots/(filename+'-desktop.png')),full_page=True)
        for width in [390,320]:
            page.set_viewport_size({'width':width,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
            page.locator('#preset-line').click();page.locator('#step').click()
            if args.screenshots: page.screenshot(path=str(args.screenshots/(filename+f'-{width}.png')),full_page=True)
        context.close()
    browser.close()
print('PASS: source and standalone load offline, reduced-motion start, keyboard time/model sliders, presets, guide, play/pause/restart, JSON download and 320/390 CSS-pixel width smoke checks.')
print('Not tested: physical touch, Safari/Firefox, screen readers, zoom, visual screenshot review, curriculum efficacy or full accessibility conformance.')
