#!/usr/bin/env python3
"""Real-browser checks for the unchanged offline lab (not accessibility acceptance).
Needs an existing Playwright installation plus its Chromium or Firefox browser.
Nothing is installed here. Source and standalone are opened as local file URLs.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import re
import tempfile
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


def download_record(page):
    with page.expect_download() as info:
        page.locator('#export').click()
    assert info.value.suggested_filename == 'motion-trace-shape-experiment.json'
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / 'experiment.json'
        info.value.save_as(target)
        return json.loads(target.read_text())


def check_samples(record):
    """Check the downloaded data against equations independent of app JS."""
    assert record['format'] == 'motion-trace-shape-experiment'
    assert record['schema_version'] == 1
    model = record['model']
    assert model['sampling']['sample_count'] == 481
    assert len(model['samples']) == 481
    p = model['parameters']
    assert p == dict(x_cycles=1, y_cycles=1, phase_degrees=90,
                     duration_seconds=8, amplitude_model_units=1)
    for i, sample in enumerate(model['samples']):
        t = i / 60
        assert math.isclose(sample['t'], t, abs_tol=1e-12)
        assert math.isclose(sample['x'], math.sin(2 * math.pi * t / 8), abs_tol=1e-12)
        assert math.isclose(sample['y'], math.sin(2 * math.pi * t / 8 + math.pi / 2), abs_tol=1e-12)


def check_page(browser, filename, screenshots):
    context = browser.new_context(viewport={'width': 1280, 'height': 1000},
                                  reduced_motion='reduce', accept_downloads=True)
    context.set_offline(True)
    page = context.new_page()
    errors, external = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('request', lambda req: external.append(req.url)
            if req.url.startswith(('http://', 'https://')) else None)
    page.goto((ROOT / filename).as_uri())
    for id_ in ['shapeSvg', 'motionSvg', 'timeSvg']:
        expect(page.locator('#' + id_)).to_be_visible()
    expect(page.locator('#shapeGuide')).to_have_attribute('d', re.compile('^M'))
    expect(page.locator('#timeSvg g[stroke] path')).to_have_css('fill', 'none')
    expect(page.locator('#still')).to_be_checked()
    expect(page.locator('#play')).to_be_disabled()
    expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')
    page.locator('#step').click()
    expect(page.locator('#timeValue')).to_have_text('0.125 / 8 s')
    page.locator('#time').focus()
    page.keyboard.press('End')
    expect(page.locator('#timeValue')).to_have_text('8.000 / 8 s')
    expect(page.locator('#step')).to_be_disabled()
    page.keyboard.press('Home')
    expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')

    for preset, label in [('line', 'Line'), ('circle', 'Circle'), ('eight', 'Figure-eight')]:
        page.locator('#preset-' + preset).click()
        expect(page.locator('#shapeName')).to_have_text(label)
        expect(page.locator('#preset-' + preset)).to_have_attribute('aria-pressed', 'true')
    for id_, value in [('xCycles', '2'), ('yCycles', '3'), ('phase', '15')]:
        page.locator('#' + id_).focus()
        page.keyboard.press('ArrowRight')
        expect(page.locator('#' + id_)).to_have_value(value)
        expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')
    page.locator('#preset-circle').click()
    page.locator('#guide').uncheck()
    for id_ in ['shapeGuide', 'xGuide', 'yGuide']:
        expect(page.locator('#' + id_)).to_have_attribute('visibility', 'hidden')
    page.locator('#guide').check()
    expect(page.locator('#shapeGuide')).to_have_attribute('visibility', 'visible')
    for details in page.locator('details').all():
        details.locator('summary').click()
        expect(details).to_have_attribute('open', '')
        details.locator('summary').click()
        assert details.get_attribute('open') is None

    page.locator('#still').uncheck()
    for _ in range(2):
        page.locator('#play').click()
        expect(page.locator('#play')).to_have_text('Pause')
        expect(page.locator('#time')).not_to_have_value('0')
        page.locator('#play').click()
        frozen = page.locator('#time').input_value()
        page.wait_for_timeout(100)
        assert page.locator('#time').input_value() == frozen
        page.locator('#restart').click()
        expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')

    # Interrupt playback through native keyboard scrub and a model change.
    page.locator('#play').click()
    page.locator('#time').focus()
    page.keyboard.press('End')
    expect(page.locator('#play')).to_have_text('Replay one cycle')
    page.keyboard.press('ArrowLeft')
    page.locator('#play').click()
    expect(page.locator('#play')).to_have_text('Replay one cycle')
    expect(page.locator('#timeValue')).to_have_text('8.000 / 8 s')
    page.locator('#play').click()
    expect(page.locator('#play')).to_have_text('Pause')
    page.locator('#preset-circle').click()
    expect(page.locator('#play')).to_have_text('Play one cycle')
    expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')

    # A live system preference change must interrupt play, never auto-resume.
    page.emulate_media(reduced_motion='no-preference')
    page.locator('#play').click()
    page.emulate_media(reduced_motion='reduce')
    expect(page.locator('#still')).to_be_checked()
    expect(page.locator('#play')).to_be_disabled()
    frozen = page.locator('#time').input_value()
    page.emulate_media(reduced_motion='no-preference')
    expect(page.locator('#still')).to_be_checked()
    page.wait_for_timeout(100)
    assert page.locator('#time').input_value() == frozen
    page.locator('#restart').click()
    page.locator('#step').click()

    baseline = download_record(page)
    check_samples(baseline)
    assert baseline['presentation']['time'] == .125
    for speed in ['0.5', '2', '1']:
        page.locator('#speed').select_option(speed)
        record = download_record(page)
        check_samples(record)
        assert record['model'] == baseline['model']
        assert record['presentation']['playback_speed'] == float(speed)
        assert record['presentation']['time'] == .125
        assert record['presentation']['still_mode'] is True

    for width in [1280, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1000 if width == 1280 else 844})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
        box = page.locator('#shapeSvg').bounding_box()
        assert box and box['width'] > 0 and box['height'] > 0, box
        # The SVG viewport may letterbox; its coordinate transform must not stretch circles.
        scale = page.locator('#shapeSvg').evaluate(
            '(svg) => { const m = svg.getScreenCTM(); '
            'return {x: Math.hypot(m.a, m.b), y: Math.hypot(m.c, m.d)}; }')
        assert scale['x'] > 0 and math.isclose(scale['x'], scale['y'], abs_tol=1e-9), scale
        page.locator('#preset-line').click()
        page.locator('#restart').click()
        page.locator('#step').click()
        expect(page.locator('#timeValue')).to_have_text('0.125 / 8 s')
        if screenshots:
            screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshots / f'{filename}-{width}.png'), full_page=True)
    assert not errors, errors
    assert not external, external
    context.close()

    # No preference also starts paused; this is separate from reduced startup.
    context = browser.new_context(reduced_motion='no-preference')
    context.set_offline(True)
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('request', lambda req: external.append(req.url)
            if req.url.startswith(('http://', 'https://')) else None)
    page.goto((ROOT / filename).as_uri())
    expect(page.locator('#still')).not_to_be_checked()
    expect(page.locator('#play')).to_be_enabled()
    page.wait_for_timeout(100)
    expect(page.locator('#timeValue')).to_have_text('0.000 / 8 s')
    assert not errors, errors
    assert not external, external
    context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=['chromium', 'firefox'], default='chromium')
    parser.add_argument('--chromium', help='Existing Chromium executable (Chromium only).')
    parser.add_argument('--screenshots', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.chromium and args.browser != 'chromium':
        parser.error('--chromium cannot be used with --browser firefox')
    with sync_playwright() as p:
        options = {'headless': True}
        if args.chromium:
            options['executable_path'] = args.chromium
        browser = getattr(p, args.browser).launch(**options)
        version = browser.version
        for filename in ['index.html', 'Motion-Trace-Shape.html']:
            check_page(browser, filename, args.screenshots)
        browser.close()
    report = {
        'result': 'passed', 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'browser': args.browser, 'browser_version': version,
        'playwright_version': importlib.metadata.version('playwright'),
        'platform': platform.platform(), 'python': platform.python_version(),
        'mode': 'headless, offline local files; desktop and narrow CSS viewports',
        'files': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                  for name in ['index.html', 'Motion-Trace-Shape.html', 'src/app.js', 'src/core.js', 'src/style.css']},
        'scope': ['both source and standalone', 'SVG visibility, unfilled time axes and equal coordinate scale',
                  'reduced and normal paused startup', 'all presets and parameter keyboard increments',
                  'guide and disclosure toggles', 'play/pause/restart/replay and interruption',
                  'dynamic reduced-motion pause', 'repeated real JSON downloads and 481 analytical samples',
                  'all speed values preserve model data', 'no HTTP(S) requests or browser errors',
                  'no page overflow at 1280/390/320 CSS pixels'],
        'not_tested': ['human visual screenshot review', 'physical touch devices', 'Safari or Edge',
                       'screen readers', 'zoom', 'full accessibility conformance',
                       'background-tab visibility on a real desktop', 'learner or educator acceptance']
    }
    text = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
