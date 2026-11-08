#!/usr/bin/env python3
"""Scoped offline browser checks of the unchanged CC0 Atlas artifact.

Original archive harness (CC BY 4.0). Optional test dependency: Playwright 1.56.0.
Use xvfb-run on Linux; the runner never installs browsers or starts a server.
Main flows use real file navigation, native controls, WebGL2 and saved downloads.
Only the separately labeled unavailable-WebGL scenario replaces getContext.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import shutil
import tempfile
import time
import xml.etree.ElementTree as ET

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
FILENAME = 'Reality_Atlas_Appearance_0.3.1.html'
EXPECTED_HASH = 'fdb0f246ddcf45e3b6b90fae356c95dfce86cfab122fab33a1143659f87bce0d'
SVG_NS = '{http://www.w3.org/2000/svg}'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def settle(page):
    page.wait_for_function('!!window.appearanceLab && appearanceLab.isSettled()', timeout=20000)


def snapshot(page):
    return page.evaluate('appearanceLab.record()')


def frame(page):
    return page.evaluate('''() => {
      const r = appearanceLab.renderer, p = r.pixels(); let hash = 2166136261, lit = 0;
      for (let i = 0; i < p.length; i += 4) {
        for (let j = 0; j < 3; j++) hash = Math.imul(hash ^ p[i+j], 16777619);
        if (p[i] + p[i+1] + p[i+2] > 45) lit++;
      }
      return {hash: hash >>> 0, lit, width: r.canvas.width, height: r.canvas.height,
        error: r.gl.getError(), batches: r.drawCalls,
        points: appearanceLab.getFrame().points.length,
        lines: appearanceLab.getFrame().lines.length,
        spheres: appearanceLab.getFrame().spheres.length};
    }''')


def paint_after_resize(page):
    page.wait_for_function('''() => {
      if (!window.appearanceLab || !appearanceLab.isSettled()) return false;
      const c = appearanceLab.renderer.canvas, b = c.getBoundingClientRect();
      const d = Math.min(devicePixelRatio || 1, 1.5);
      return c.width === Math.round(b.width*d) && c.height === Math.round(b.height*d);
    }''')
    assert frame(page)['lit'] > 100


def slider(page, id_, value):
    """Drive native range keys; do not dispatch synthetic input/change events."""
    control = page.locator('#' + id_)
    minimum = float(control.get_attribute('min'))
    step = float(control.get_attribute('step') or 1)
    increments = (value - minimum) / step
    assert increments >= 0 and math.isclose(increments, round(increments))
    control.focus()
    page.keyboard.press('Home')
    for _ in range(round(increments)):
        page.keyboard.press('ArrowRight')
    expect(control).to_have_value(format(value, 'g'))
    # Some range controls publish their change event on blur.
    page.keyboard.press('Tab')
    settle(page)


def finite_json(value):
    if isinstance(value, float):
        assert math.isfinite(value)
    elif isinstance(value, dict):
        for child in value.values():
            finite_json(child)
    elif isinstance(value, list):
        for child in value:
            finite_json(child)


def downloaded(page, button, filename, folder):
    with page.expect_download() as result:
        page.locator(button).click()
    item = result.value
    assert item.suggested_filename == filename
    path = folder / filename
    item.save_as(path)
    assert item.failure() is None and path.stat().st_size > 100
    return path


def exports(page, output, scenario):
    folder = output / scenario
    folder.mkdir(parents=True, exist_ok=True)
    expected = snapshot(page)
    state = json.loads(downloaded(page, '#a-export', 'reality-appearance-state.json', folder).read_text())
    assert state == expected
    assert state['schema'] == 'reality-atlas:appearance/0.3.1'
    finite_json(state)
    svg = ET.fromstring(downloaded(page, '#a-svg', 'reality-appearance-vector.svg', folder).read_bytes())
    assert svg.tag == SVG_NS + 'svg' and svg.attrib['viewBox'] == '0 0 1200 1000'
    assert json.loads(svg.find(SVG_NS + 'metadata').text) == expected
    assert 'not a volume render' in svg.find(SVG_NS + 'desc').text
    geometry = svg.find(f"{SVG_NS}g[@id='calculated-geometry']")
    assert geometry is not None and len(geometry) > 0
    assert any(x.tag == SVG_NS + 'circle' for x in geometry)
    assert all(x.tag in {SVG_NS + 'circle', SVG_NS + 'path'} for x in geometry)
    text = ET.tostring(svg, encoding='unicode')
    assert 'NaN' not in text and 'Infinity' not in text
    for element in svg.iter():
        assert not any(k.lower().startswith('on') or k.endswith('href') for k in element.attrib)
    return {'scenario': scenario, 'lab': state['lab'], 'mode': state['observation']['mode'],
            'json_path': f'{scenario}/reality-appearance-state.json',
            'svg_path': f'{scenario}/reality-appearance-vector.svg',
            'json_sha256': digest(folder / 'reality-appearance-state.json'),
            'svg_sha256': digest(folder / 'reality-appearance-vector.svg'),
            'svg_glyphs': len(geometry)}


def observe(page, report):
    page.on('pageerror', lambda error: report['page_errors'].append(str(error)))
    page.on('request', lambda request: report['external_requests'].append(request.url)
            if request.url.startswith(('http:', 'https:', 'ws:', 'wss:')) else None)
    page.on('console', lambda message: report['console_errors'].append(message.text)
            if message.type == 'error' else None)


def check(report, name, condition=True, detail=None):
    report['checks'].append({'name': name, 'passed': bool(condition), 'detail': detail})
    assert condition, name


def screenshot(page, folder, name):
    page.screenshot(path=str(folder / f'{name}.png'), full_page=True)


def functional(browser, url, report, folder):
    context = browser.new_context(viewport={'width': 1440, 'height': 1120},
                                  reduced_motion='reduce', device_scale_factor=1, accept_downloads=True)
    context.set_offline(True)
    page = context.new_page()
    observe(page, report)
    page.goto(url, wait_until='load')
    settle(page)
    first = frame(page)
    report['renderer'] = page.evaluate('''() => {
      const g = appearanceLab.renderer.gl, e = g.getExtension('WEBGL_debug_renderer_info');
      return {version: g.getParameter(g.VERSION), vendor: g.getParameter(g.VENDOR),
        renderer: e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER)};
    }''')
    check(report, 'isolated offline HTML initializes WebGL2 with nonblank framebuffer',
          first['error'] == 0 and first['lit'] > 3000 and first['batches'] == 2, first)
    check(report, 'reduced-motion startup pauses the prescribed trajectory', not page.evaluate('appearanceLab.state.playing'))
    expect(page.locator('#a-error')).not_to_be_visible()
    screenshot(page, folder, 'desktop-exposure')
    original = snapshot(page)['settings']
    hashes = {first['hash']}
    for view in ['snapshot', 'trail', 'occupancy', 'exposure']:
        page.locator(f'[data-view="{view}"]').click()
        settle(page)
        current = frame(page)
        assert current['error'] == 0 and current['lit'] > 100
        assert snapshot(page)['settings'] == original
        assert snapshot(page)['observation']['mode'] == view
        expect(page.locator(f'[data-view="{view}"]')).to_have_attribute('aria-pressed', 'true')
        if view != 'exposure':
            assert current['hash'] not in hashes
            hashes.add(current['hash'])
        screenshot(page, folder, 'mode-' + view)
    check(report, 'four observation modes change pixels without changing motion parameters')
    for preset in ['Circle', 'Breathing braid', 'Open weave', 'Woven sphere']:
        before = frame(page)['hash']
        page.select_option('#a-preset', preset)
        settle(page)
        assert frame(page)['hash'] != before and frame(page)['error'] == 0
        expect(page.locator('#a-title')).to_have_text(preset)
    check(report, 'four presets change rendered geometry')
    for id_, value in [('a-orbit', 9), ('a-precession', .7), ('a-vibration', .2), ('a-breathing', .2), ('a-exposure', .27)]:
        before = frame(page)['hash']
        slider(page, id_, value)
        assert frame(page)['hash'] != before
    check(report, 'native keyboard range changes affect orbit precession vibration breathing and window')
    settings = snapshot(page)['settings']
    before = frame(page)['hash']
    page.select_option('#a-color', 'gray')
    settle(page)
    assert frame(page)['hash'] != before and snapshot(page)['settings'] == settings
    page.select_option('#a-frequency', '1000000000000')
    settle(page)
    record = snapshot(page)
    check(report, 'palette preserves parameters and physical/display times remain separate',
          record['settings']['frequencyHz'] == 1e12 and record['display']['referenceCyclesPerDisplaySecond'] == .08
          and record['observation']['physicalTimeSeconds'] == record['observation']['referenceCycles'] / 1e12)
    slider(page, 'a-time', .02)
    frozen = frame(page)['hash']
    page.wait_for_timeout(250)
    assert frame(page)['hash'] == frozen and not page.evaluate('appearanceLab.state.playing')
    page.locator('#a-play').click()
    page.wait_for_function('appearanceLab.state.cycles > .03')
    page.locator('#a-play').click()
    settle(page)
    check(report, 'scrub pauses stable framebuffer and play advances time and pixels', frame(page)['hash'] != frozen)
    before = snapshot(page)['display']['camera']
    page.locator('#a-canvas').focus()
    page.keyboard.press('ArrowRight')
    settle(page)
    assert snapshot(page)['display']['camera']['yaw'] > before['yaw']
    page.locator('#a-zoomin').click()
    settle(page)
    assert snapshot(page)['display']['camera']['zoom'] > before['zoom']
    page.locator('#a-fit').click()
    settle(page)
    assert snapshot(page)['display']['camera'] == {'yaw': .42, 'pitch': .25, 'zoom': 1}
    box = page.locator('#a-canvas').bounding_box()
    x, y = box['x'] + box['width']*.5, box['y'] + box['height']*.6
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + 50, y + 20, steps=5)
    page.mouse.up()
    settle(page)
    assert snapshot(page)['display']['camera']['yaw'] > .42
    check(report, 'keyboard zoom fit and mouse drag update camera')
    page.locator('#a-reset').click()
    settle(page)
    record = snapshot(page)
    check(report, 'motion reset restores selected preset cycle and observation window',
          record['settings'] == original and record['observation']['referenceCycles'] == 1
          and record['observation']['exposureCycles'] == 1)
    report['downloads'].append(exports(page, folder, 'motion-export'))
    check(report, 'motion JSON and SVG are actually downloaded and retain exact finite state')
    page.locator('[data-lab="packing"]').click()
    settle(page)
    current = frame(page)
    assert current['error'] == 0 and current['spheres'] == 32 and current['lit'] > 10000
    expect(page.locator('#a-play')).to_be_disabled()
    before = current['hash']
    page.locator('#a-cut').uncheck()
    settle(page)
    assert frame(page)['hash'] != before
    page.locator('#a-cut').check()
    settle(page)
    screenshot(page, folder, 'packing-matter')
    page.select_option('#a-matter', 'void')
    settle(page)
    assert frame(page)['spheres'] == 0 and frame(page)['points'] > 0
    page.select_option('#a-family', 'Tetrahedral throat')
    settle(page)
    assert page.evaluate('appearanceLab.getVoid().enclosed') == 0
    slider(page, 'a-probe', .1)
    assert page.evaluate('appearanceLab.getVoid().enclosed') >= 1
    expect(page.locator('#a-warning')).to_contain_text('unresolved')
    expect(page.locator('#a-container')).to_be_disabled()
    expect(page.locator('#a-count')).to_be_disabled()
    for grid in ['25', '49', '33']:
        page.select_option('#a-grid', grid)
        settle(page)
        assert snapshot(page)['observation']['grid'] == int(grid) and frame(page)['error'] == 0
    screenshot(page, folder, 'packing-finite-probe')
    report['downloads'].append(exports(page, folder, 'packing-void-export'))
    check(report, 'matter cutaway void finite-probe fixture and three grid sizes render; packing exports preserve state')
    slider(page, 'a-probe', 0)
    page.select_option('#a-family', 'Fibonacci')
    page.select_option('#a-matter', 'matter')
    settle(page)
    assert frame(page)['spheres'] == 8
    page.select_option('#a-family', 'Unequal')
    settle(page)
    balls = snapshot(page)['settings']['balls']
    page.locator('#a-seed').click()
    settle(page)
    assert snapshot(page)['settings']['balls'] != balls
    page.select_option('#a-container', 'sphere')
    settle(page)
    assert snapshot(page)['settings']['kind'] == 'sphere' and frame(page)['error'] == 0
    page.locator('#a-reset').click()
    settle(page)
    record = snapshot(page)
    assert record['settings']['family'] == 'Equal' and record['settings']['kind'] == 'box'
    assert record['settings']['requested'] == 32 and record['observation']['grid'] == 33
    assert record['observation']['probeRadius'] == 0 and record['observation']['mode'] == 'matter'
    check(report, 'Fibonacci unequal seeded arrangement spherical container and packing reset work')
    for width, height in [(390, 844), (320, 844), (844, 390)]:
        page.set_viewport_size({'width': width, 'height': height})
        for lab in ['motion', 'packing', 'motion']:
            page.locator(f'[data-lab="{lab}"]').click()
            settle(page)
            paint_after_resize(page)
            assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
            page.locator('#a-svg').scroll_into_view_if_needed()
            expect(page.locator('#a-svg')).to_be_visible()
        page.locator('[data-view="snapshot"]').click()
        settle(page)
        report['downloads'].append(exports(page, folder, f'layout-{width}-{height}-export'))
        # Full-page Chromium captures can crop a scrollbar-width strip. Retain
        # a normal viewport capture and measured client-width bounds as well.
        metrics = page.evaluate('''() => {
          const root = document.documentElement;
          return {innerWidth, clientWidth: root.clientWidth, scrollWidth: root.scrollWidth,
            controls: ['a-export', 'a-svg'].map(id => {
              const b = document.getElementById(id).getBoundingClientRect();
              return {id, left: b.left, right: b.right};
            })};
        }''')
        assert all(c['left'] >= 0 and c['right'] <= metrics['clientWidth'] for c in metrics['controls'])
        report['layout_metrics'].append({'viewport': [width, height], **metrics})
        page.evaluate('window.scrollTo(0, 0)')
        page.screenshot(path=str(folder / f'viewport-{width}-{height}.png'), full_page=False)
        screenshot(page, folder, f'narrow-{width}-{height}')
    check(report, '390 320 and landscape layouts paint without page overflow after repeated switches; exports work')
    page.reload()
    settle(page)
    record = snapshot(page)
    check(report, 'native reload starts default paused motion without stale packing state',
          record['lab'] == 'motion' and record['observation']['mode'] == 'exposure'
          and record['settings'] == original and not page.evaluate('appearanceLab.state.playing'))
    # Synthetic centered-sphere renderer fixture, separate from UI-level assertions.
    cap = page.evaluate('''() => {
      const r = appearanceLab.renderer;
      r.upload({points:[], lines:[], spheres:[{a:[0,0,0], color:[.2,.8,.6], size:.7, alpha:1}]});
      r.render(true); const pixel = new Uint8Array(4);
      r.gl.readPixels(Math.floor(r.canvas.width/2), Math.floor(r.canvas.height/2), 1, 1, r.gl.RGBA, r.gl.UNSIGNED_BYTE, pixel);
      appearanceLab.rebuild(); return Array.from(pixel);
    }''')
    check(report, 'centered synthetic sphere fixture has a filled cutaway-cap pixel', sum(cap[:3]) > 100, cap)
    # Native test extension triggers a real lost/restored WebGL context.
    available = page.evaluate('''() => {
      window.lossTest = appearanceLab.renderer.gl.getExtension('WEBGL_lose_context');
      if (!lossTest) return false;
      document.querySelector('canvas').addEventListener('webglcontextrestored', () => window.restoredTest = true);
      lossTest.loseContext(); return true;
    }''')
    assert available, 'WEBGL_lose_context is required for the explicitly claimed recovery scenario'
    expect(page.locator('#a-error')).to_contain_text('Graphics context lost')
    page.wait_for_timeout(200)
    page.evaluate('lossTest.restoreContext()')
    page.wait_for_function('window.restoredTest === true')
    expect(page.locator('#a-error')).to_contain_text('Reload')
    page.reload()
    settle(page)
    expect(page.locator('#a-error')).not_to_be_visible()
    assert frame(page)['lit'] > 1000 and frame(page)['error'] == 0
    check(report, 'native context loss and restoration require reload; reload recreates working scene')
    context.close()


def unavailable(browser, url, report):
    context = browser.new_context(reduced_motion='reduce')
    context.set_offline(True)
    context.add_init_script('''(() => {
      const get = HTMLCanvasElement.prototype.getContext;
      HTMLCanvasElement.prototype.getContext = function(type, ...args) {
        return type === 'webgl2' ? null : get.call(this, type, ...args);
      };
    })();''')
    page = context.new_page()
    page.goto(url)
    expect(page.locator('#a-error')).to_contain_text('WebGL2 is required')
    assert page.evaluate('typeof window.appearanceLab') == 'undefined'
    check(report, 'separate synthetic unavailable-WebGL2 fault shows explicit requirement rather than false rendering')
    context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=['chromium', 'firefox'], default='chromium')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'suite': 'archive-reality-atlas-browser/1', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'browser_engine': args.browser, 'platform': platform.platform(),
              'python': platform.python_version(), 'playwright': importlib.metadata.version('playwright'),
              'artifact_sha256': digest(ROOT / FILENAME), 'runner_sha256': digest(Path(__file__)),
              'loading': 'isolated copied HTML via actual file URL; fresh offline browser context',
              'rendering': 'software renderer requested; actual renderer recorded below',
              'checks': [], 'downloads': [], 'layout_metrics': [], 'page_errors': [], 'console_errors': [], 'external_requests': [],
              'not_tested': ['physical mobile/touch', 'Safari or Edge', 'native GPU/Metal or WebGPU',
                             'Unity Unreal or VR', 'screen readers or full keyboard traversal',
                             'accessibility conformance', 'scientific or learner/educator acceptance',
                             'upstream six-scene regression', 'performance benchmarks',
                             'browser profiles extensions or arbitrary file/download permissions']}
    try:
        assert report['artifact_sha256'] == EXPECTED_HASH, 'Preserved source artifact changed'
        with tempfile.TemporaryDirectory(prefix='atlas-offline-') as temp, sync_playwright() as p:
            isolated = Path(temp) / FILENAME
            shutil.copyfile(ROOT / FILENAME, isolated)
            assert list(Path(temp).iterdir()) == [isolated]
            kwargs = {'headless': False}
            if args.browser == 'chromium':
                kwargs['args'] = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
            browser = getattr(p, args.browser).launch(**kwargs)
            report['browser_version'] = browser.version
            functional(browser, isolated.as_uri(), report, args.output)
            unavailable(browser, isolated.as_uri(), report)
            check(report, 'main flow has no uncaught page exceptions or external requests',
                  not report['page_errors'] and not report['external_requests'])
            # Console diagnostics are retained, not silently interpreted as acceptance.
            browser.close()
        report['passed'] = True
    except Exception as error:
        report['failure'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
