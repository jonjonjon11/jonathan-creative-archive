#!/usr/bin/env python3
"""Original archive checks for the offline standalone; not device acceptance.

Requires Playwright and an already installed Chromium or Firefox. Does not
install anything. Only a copy of the standalone is placed in an isolated folder;
no local server, Storage double or disabled CSP is used in the main flow.
"""
# New archive test: CC BY 4.0. Recovered Lumen runtime retains CC0.
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import tempfile
import time

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
FILENAME = 'Lumen-Commons-Play.html'
KEY = 'lumen-commons-v1'
QUESTS = ['fractions', 'trajectory', 'harmony', 'orbit', 'coordinates']
# Only this separate fault-injection scenario replaces the native getter.
DENY_STORAGE = """Object.defineProperty(window, 'localStorage', {
  configurable: true, get() { throw new DOMException('Synthetic denial', 'SecurityError'); }
});"""


def snapshot(page):
    return json.loads(page.evaluate('(key) => localStorage.getItem(key)', KEY))


def close_panel(page, escape=False):
    if escape:
        page.keyboard.press('Escape')
    else:
        page.locator('#closePanel').click()
    expect(page.locator('#panel')).not_to_be_visible()
    expect(page.locator('#world')).to_be_focused()


def slider(page, id_, value):
    control = page.locator('#' + id_)
    minimum = float(control.get_attribute('min'))
    step = float(control.get_attribute('step') or 1)
    increments = (value - minimum) / step
    assert increments >= 0 and increments.is_integer()
    control.focus()
    page.keyboard.press('Home')
    for _ in range(int(increments)):
        page.keyboard.press('ArrowRight')
    expect(control).to_have_value(format(value, 'g'))


def open_settings(page):
    page.locator('#settingsButton').click()
    expect(page.locator('#panelTitle')).to_have_text('☷ Settings')


def download(page):
    with page.expect_download() as result:
        page.get_by_role('button', name='Export local progress', exact=True).click()
    item = result.value
    assert item.suggested_filename == 'lumen-progress.json'
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / item.suggested_filename
        item.save_as(path)
        assert path.stat().st_size < 30000
        return json.loads(path.read_text(encoding='utf-8'))


def restore(page, payload):
    data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    page.locator('#restore').set_input_files({
        'name': 'synthetic-progress.json', 'mimeType': 'application/json', 'buffer': data})


def attach_observers(page, errors, requests):
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('request', lambda request: requests.append(request.url)
            if request.url.startswith(('http:', 'https:', 'ws:', 'wss:')) else None)


def new_context(browser, url, errors, requests, *, denied=False, reduced='no-preference'):
    context = browser.new_context(viewport={'width': 1280, 'height': 1000},
                                  device_scale_factor=1, reduced_motion=reduced, accept_downloads=True)
    context.set_offline(True)
    if denied:
        context.add_init_script(DENY_STORAGE)
    page = context.new_page()
    attach_observers(page, errors, requests)
    page.goto(url, wait_until='load')
    expect(page.locator('#destinations button')).to_have_count(6)
    expect(page.locator('#world')).to_be_visible()
    expect(page.locator('#progressLabel')).to_have_text('0 / 5')
    return context, page


def check_functional(browser, url, errors, requests, screenshots):
    context, page = new_context(browser, url, errors, requests)
    # This would throw if native file-origin storage is unavailable.
    assert page.evaluate('(key) => localStorage.getItem(key)', KEY) is None
    page.locator('#begin').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#panelTitle')).to_have_text('Fraction Forge')
    expect(page.locator('#closePanel')).to_be_focused()
    page.get_by_role('button', name='Try my idea', exact=True).click()
    expect(page.locator('.feedback')).to_contain_text('Not quite')
    page.get_by_role('button', name='Give me a hint', exact=True).click()
    expect(page.locator('.feedback')).to_contain_text('4 equal groups')
    page.locator('#cells').focus()
    page.keyboard.press('Home')
    for _ in range(9):
        page.keyboard.press('ArrowRight')
    expect(page.locator('#cells')).to_have_value('9')
    for _ in range(2):
        page.get_by_role('button', name='Try my idea', exact=True).click()
        expect(page.locator('#progressLabel')).to_have_text('1 / 5')
    close_panel(page, escape=True)

    for count, (title, values) in enumerate([
        ('Sky Ferry Lab', {'speed': 18, 'angle': 45}),
        ('Harmony Garden', {'semitones': 12}),
        ('Star Observatory', {'axis': 4}),
        ('Atlas Conservatory', {'lat': 20, 'lon': 40}),
    ], start=2):
        page.locator('#destinations').get_by_role('button', name=title, exact=True).click()
        for id_, value in values.items():
            slider(page, id_, value)
        page.get_by_role('button', name='Try my idea', exact=True).click()
        expect(page.locator('.feedback')).to_contain_text('Beacon restored')
        expect(page.locator('#progressLabel')).to_have_text(f'{count} / 5')
        if screenshots:
            page.screenshot(path=str(screenshots / f'quest-{count}.png'), full_page=True)
        close_panel(page)

    open_settings(page)
    for language, title in [('es', '☷ Ajustes'), ('ja', '☷ 設定'), ('en', '☷ Settings')]:
        page.locator('#language').select_option(language)
        expect(page.locator('html')).to_have_attribute('lang', language)
        expect(page.locator('#panelTitle')).to_have_text(title)
    page.locator('#quality').select_option('low')
    page.locator('#reduced').check()
    expect(page.locator('body')).to_have_class('reduce')
    close_panel(page)
    page.locator('#cafeButton').click()
    expect(page.locator('.chat p')).to_have_count(1)
    page.get_by_role('button', name='Say hello', exact=True).click()
    expect(page.locator('.chat p')).to_have_count(2)
    expect(page.locator('.chat p').last).to_have_text(
        'Jun · scripted host: Hello, explorer! You never need to be an expert to belong here.')
    page.get_by_role('button', name='Add a star', exact=True).click()
    saved = snapshot(page)
    assert saved['complete'] == QUESTS
    assert saved['art'] == [{'x': .12, 'y': .3, 'hue': 155}]
    assert saved['quality'] == 'low' and saved['reduced'] is True
    assert set(saved) == {'version', 'complete', 'motes', 'lang', 'quality', 'skin', 'reduced', 'art'}
    close_panel(page)

    page.reload()
    expect(page.locator('#progressLabel')).to_have_text('5 / 5')
    assert snapshot(page) == saved
    expect(page.locator('body')).to_have_class('reduce')
    page.close()
    page = context.new_page()
    attach_observers(page, errors, requests)
    page.goto(url)
    expect(page.locator('#progressLabel')).to_have_text('5 / 5')
    assert snapshot(page) == saved
    open_settings(page)
    expect(page.locator('#quality')).to_have_value('low')
    expect(page.locator('#reduced')).to_be_checked()
    assert download(page) == saved
    assert download(page) == saved

    # Cancel never erases; accept erases only this isolated synthetic test state.
    page.once('dialog', lambda dialog: dialog.dismiss())
    page.get_by_role('button', name='Erase local progress', exact=True).click()
    assert snapshot(page) == saved
    expect(page.locator('#panel')).to_be_visible()
    page.once('dialog', lambda dialog: dialog.accept())
    page.get_by_role('button', name='Erase local progress', exact=True).click()
    expect(page.locator('#progressLabel')).to_have_text('0 / 5')
    expect(page.locator('#panel')).not_to_be_visible()
    assert snapshot(page)['art'] == []
    open_settings(page)
    restore(page, saved)
    expect(page.locator('#progressLabel')).to_have_text('5 / 5')
    expect(page.locator('#quality')).to_have_value('low')
    assert snapshot(page) == saved
    assert download(page) == saved
    for invalid, message in [(b'{broken', 'Invalid progress file'),
                             ({'version': 999}, 'Invalid progress file'),
                             (b' ' * 30001, 'Progress file is too large')]:
        # Require a fresh response, not the preceding invalid import's toast.
        page.locator('#toast').evaluate("(toast) => { toast.textContent = ''; }")
        restore(page, invalid)
        expect(page.locator('#toast')).to_contain_text(message)
        assert snapshot(page) == saved
    close_panel(page, escape=True)
    page.reload()
    expect(page.locator('#progressLabel')).to_have_text('5 / 5')
    assert snapshot(page) == saved
    context.close()


def wait_for_world_paint(page):
    """Do not mistake a resized, cleared canvas for a rendered world.

    Native frame scheduling can repaint after set_viewport_size has returned.
    Require correctly resized backing dimensions and nonblack, varied pixels
    twice, 50 ms apart. This is paint readiness, not graphical correctness.
    """
    deadline, consecutive = time.monotonic() + 5, 0
    while time.monotonic() < deadline:
        painted = page.locator('#world').evaluate("""canvas => {
            const r = canvas.getBoundingClientRect();
            if (canvas.width !== Math.round(r.width) ||
                canvas.height !== Math.round(r.height)) return false;
            const c = canvas.getContext('2d'), colors = new Set();
            let bright = 0;
            for (let y = 1; y <= 4; y++) for (let x = 1; x <= 4; x++) {
                const p = c.getImageData(Math.floor(canvas.width*x/5),
                                        Math.floor(canvas.height*y/5), 1, 1).data;
                if (p[3] === 255 && p[0]+p[1]+p[2] > 40) bright++;
                colors.add(Array.from(p).join(','));
            }
            return bright === 16 && colors.size >= 8;
        }""")
        consecutive = consecutive + 1 if painted else 0
        if consecutive >= 2:
            return
        page.wait_for_timeout(50)
    raise AssertionError('World canvas did not paint after viewport resize')


def check_layout(browser, url, errors, requests, screenshots):
    context, page = new_context(browser, url, errors, requests, reduced='reduce')
    expect(page.locator('body')).to_have_class('reduce')
    titles = ['Fraction Forge', 'Sky Ferry Lab', 'Harmony Garden', 'Star Observatory',
              'Atlas Conservatory', 'The Common Table']
    for width, height in [(1280, 1000), (390, 844), (320, 844), (844, 390)]:
        page.set_viewport_size({'width': width, 'height': height})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, height)
        box = page.locator('#world').bounding_box()
        assert box and box['width'] > 0 and box['height'] > 0
        wait_for_world_paint(page)
        if screenshots:
            page.screenshot(path=str(screenshots / f'world-{width}x{height}.png'), full_page=True)
        # Use the toolbar, which stays available when the sidebar is hidden.
        for index, title in enumerate(titles):
            page.locator('#exploreButton').click()
            expect(page.locator('#panelBody .journalitem')).to_have_count(6)
            page.locator('#panelBody .journalitem').nth(index).get_by_role('button').click()
            expect(page.locator('#panelTitle')).to_have_text(title)
            box = page.locator('#panel').bounding_box()
            assert box and box['x'] >= -1 and box['x'] + box['width'] <= width + 1, box
            assert box['y'] >= -1 and box['y'] + box['height'] <= height + 1, box
            assert page.locator('#panel').evaluate('(p) => p.scrollWidth <= p.clientWidth'), title
            if screenshots and index == 0:
                page.screenshot(path=str(screenshots / f'fraction-{width}x{height}.png'), full_page=True)
            if index == 0:
                slider(page, 'cells', 9)
                page.get_by_role('button', name='Try my idea', exact=True).click()
                expect(page.locator('.feedback')).to_contain_text('Beacon restored')
                expect(page.locator('#progressLabel')).to_have_text('1 / 5')
            close_panel(page, escape=index % 2 == 0)
    context.close()


def check_storage_denial(browser, url, errors, requests):
    context, page = new_context(browser, url, errors, requests, denied=True)
    expect(page.locator('#toast')).to_contain_text('Storage is unavailable')
    page.locator('#begin').click()
    slider(page, 'cells', 9)
    page.get_by_role('button', name='Try my idea', exact=True).click()
    expect(page.locator('#progressLabel')).to_have_text('1 / 5')
    close_panel(page)
    open_settings(page)
    assert download(page)['complete'] == ['fractions']
    close_panel(page)
    page.reload()
    expect(page.locator('#progressLabel')).to_have_text('0 / 5')
    expect(page.locator('#toast')).to_contain_text('Storage is unavailable')
    context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=['chromium', 'firefox'], default='chromium')
    parser.add_argument('--chromium', help='Existing Chromium executable; Chromium only.')
    parser.add_argument('--screenshots', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.chromium and args.browser != 'chromium':
        parser.error('--chromium cannot be combined with Firefox')
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    errors, requests = [], []
    with tempfile.TemporaryDirectory(prefix='lumen-standalone-') as folder:
        target = Path(folder) / FILENAME
        shutil.copyfile(ROOT / FILENAME, target)
        assert len(list(Path(folder).iterdir())) == 1
        with sync_playwright() as pw:
            options = {'headless': True}
            if args.chromium:
                options['executable_path'] = args.chromium
            browser = getattr(pw, args.browser).launch(**options)
            version = browser.version
            try:
                check_functional(browser, target.as_uri(), errors, requests, args.screenshots)
                check_layout(browser, target.as_uri(), errors, requests, args.screenshots)
                check_storage_denial(browser, target.as_uri(), errors, requests)
                assert not errors, errors
                assert not requests, requests
            except Exception:
                if args.screenshots:
                    for context in browser.contexts:
                        for index, page in enumerate(context.pages):
                            try:
                                page.screenshot(path=str(args.screenshots / f'failure-{index}.png'),
                                                full_page=True, timeout=5000)
                            except Exception:
                                pass  # Keep the original assertion/launch failure.
                raise
            finally:
                browser.close()
    report = {
        'result': 'passed', 'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'browser': args.browser, 'browser_version': version,
        'playwright_version': importlib.metadata.version('playwright'),
        'python': platform.python_version(), 'platform': platform.platform(),
        'mode': 'headless, offline local file copied alone into a temporary folder',
        'files': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                  for name in [FILENAME, 'index.html', 'src/core.js', 'src/game.js',
                               'src/world.js', 'src/style.css', 'tests/standalone_browser.py']},
        'scope': ['five quests and idempotent repeated completion', 'wrong answer and hint',
                  'keyboard activation, native quest range keys, Escape and Close focus return',
                  'three language switches and reduced-motion/quality settings',
                  'scripted dialogue and local artwork', 'native file-origin storage across reload and same-context tab reopen',
                  'four real JSON downloads including after export/erase/restore roundtrip',
                  'erase Cancel/Accept against isolated synthetic state',
                  'invalid JSON, future-version and oversized restore preserve existing state',
                  'painted world, six destinations, dialog fit and fraction controls at 1280x1000, 390x844, 320x844, 844x390',
                  'separate injected storage denial allows play and export but does not persist',
                  'no page/console errors or external network requests'],
        'not_tested': ['source edition browser navigation', 'browser restart/profile persistence or moving the HTML file',
                       'Safari or Edge', 'physical mobile or touch', 'audio/listening', 'canvas walking or joystick',
                       'screen readers, zoom or full keyboard traversal', 'accessibility conformance',
                       'native-speaker translation review', 'learner or educator acceptance',
                       'human screenshot review', 'production or child-safety acceptance']
    }
    output = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
