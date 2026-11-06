"""Browser integration test. Uses set_content, no external hosting or network.
The optional memory Storage double tests save/restore logic, NOT native persistence.
Run: python tests/browser_smoke.py (Playwright + Chromium required).
"""
import json
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'Lumen-Commons-Play.html').read_text(encoding='utf-8')
OUT = ROOT / 'test-results'
OUT.mkdir(exist_ok=True)
results=[]
STORE="""() => {const values=new Map();Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,String(v)),removeItem:k=>values.delete(k)}});} """
def check(label, condition):
    if not condition: raise AssertionError(label)
    results.append(label)
def load(browser,width=1440,height=1000,memory=True,touch=False):
    p=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,is_mobile=touch,has_touch=touch)
    errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
    if memory:p.evaluate(STORE)
    p.set_content(HTML,wait_until='load');p.wait_for_timeout(300)
    return p,errs
def slider(page,id,value):
    page.locator('#'+id).fill(str(value));page.locator('#'+id).dispatch_event('input')
with sync_playwright() as pw:
    executable=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
    kwargs={'headless':True,'args':['--no-sandbox']}
    if executable:kwargs['executable_path']=executable
    b=pw.chromium.launch(**kwargs)
    p,errs=load(b)
    check('six accessible destinations',p.locator('#destinations button').count()==6)
    p.locator('#begin').click();check('first quest opens',p.locator('#panelTitle').inner_text()=='Fraction Forge')
    p.get_by_role('button',name='Try my idea',exact=True).click()
    check('incorrect answer is supportive',p.locator('.feedback').inner_text().startswith('Not quite'))
    p.get_by_role('button',name='Give me a hint',exact=True).click()
    check('explanatory hint', '4 equal groups' in p.locator('.feedback').inner_text())
    slider(p,'cells',9);p.get_by_role('button',name='Try my idea',exact=True).click()
    check('fraction completion',p.locator('#progressLabel').inner_text()=='1 / 5')
    p.get_by_role('button',name='Try my idea',exact=True).click()
    check('no duplicate completion',p.locator('#progressLabel').inner_text()=='1 / 5')
    p.locator('#closePanel').click()
    for title,values in [('Sky Ferry Lab',{'speed':18,'angle':45}),('Harmony Garden',{'semitones':12}),('Star Observatory',{'axis':4}),('Atlas Conservatory',{'lat':20,'lon':40})]:
        p.locator('#destinations').get_by_role('button',name=title,exact=True).click()
        for k,v in values.items():slider(p,k,v)
        p.get_by_role('button',name='Try my idea',exact=True).click()
        check(title+' completion','Beacon restored' in p.locator('.feedback').inner_text())
        if title=='Sky Ferry Lab':p.screenshot(path=str(OUT/'physics-lab.png'))
        p.locator('#closePanel').click()
    check('all five beacons completed',p.locator('#progressLabel').inner_text()=='5 / 5')
    p.locator('#settingsButton').click();p.locator('#language').select_option('es')
    check('Spanish document language',p.locator('html').get_attribute('lang')=='es')
    check('Spanish settings',p.locator('#panelTitle').inner_text()=='☷ Ajustes')
    p.locator('#language').select_option('ja')
    check('Japanese document language',p.locator('html').get_attribute('lang')=='ja')
    p.locator('#language').select_option('en');p.locator('#quality').select_option('low')
    p.locator('#reduced').check();check('reduced motion setting',p.locator('body').get_attribute('class')=='reduce')
    p.locator('#closePanel').click();p.locator('#cafeButton').click()
    p.get_by_role('button',name='Say hello',exact=True).click();check('cafe dialogue explicitly scripted','scripted host' in p.locator('.chat').inner_text())
    p.get_by_role('button',name='Add a star',exact=True).click()
    saved=json.loads(p.evaluate("localStorage.getItem('lumen-commons-v1')"))
    check('local artwork stored',len(saved['art'])==1)
    check('all quest flags stored',len(saved['complete'])==5)
    p.locator('#closePanel').click()
    p.set_content(HTML);p.wait_for_timeout(200)
    check('reload logic restores state from Storage double',p.locator('#progressLabel').inner_text()=='5 / 5')
    check('no page exceptions in functional flow',not errs)
    p.close()
    # Check accessible destinations and viewport fit across desktop and phone layouts.
    for width,height in [(1440,1000),(1280,720),(390,844),(844,390)]:
        p,errs=load(b,width,height,touch=width<900)
        p.wait_for_timeout(500)
        check(f'no horizontal overflow {width}x{height}',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        p.locator('#exploreButton').click()
        check(f'all destinations reachable {width}x{height}',p.locator('#panelBody .journalitem').count()==6)
        p.locator('#closePanel').click()
        p.screenshot(path=str(OUT/f'world-{width}x{height}.png'))
        check(f'no exceptions {width}x{height}',not errs)
        p.close()
    p,errs=load(b,390,844,memory=False,touch=True)
    p.wait_for_timeout(650)
    check('unavailable storage is explained','Storage is unavailable' in p.locator('#toast').inner_text())
    p.locator('#exploreButton').click()
    check('still playable without storage',p.locator('#panelBody .journalitem').count()==6)
    check('no exceptions without storage',not errs)
    p.close();b.close()
report={'engine':'System Chromium, headless','tests_passed':len(results),'checks':results,'limits':['Browser viewport emulation, not physical iPhone or Android tests.','HTML loaded via Playwright set_content; local file and HTTP navigation blocked by this environment.','Persistence logic checked with memory Storage double; native browser persistence not verified.','WebKit/Firefox unavailable; browser download failed DNS resolution.','Not an accessibility certification or a multiplayer/child-safety audit.']}
(OUT/'browser-report.json').write_text(json.dumps(report,indent=2), encoding='utf-8')
print(json.dumps(report,indent=2))
