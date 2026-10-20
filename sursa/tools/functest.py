"""Test funcțional al paginii. Rulare: py tools/functest.py http://localhost:8000/ (cere Playwright și Chromium)."""
import json, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/"
def launch(p):
    try: return p.chromium.launch()
    except Exception: return p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(1500)
    bg = lambda i: pg.evaluate(f"getComputedStyle(document.querySelectorAll('.cell')[{i}]).backgroundColor")
    before = [bg(0), bg(2), bg(7)]
    pg.hover("#c-calcar"); pg.wait_for_timeout(400)
    after = [bg(0), bg(2), bg(7)]
    print("1 hover chip calcar: cell0,2,7 before", before, "after", after)
    pg.mouse.move(5, 5); pg.wait_for_timeout(300)
    pg.keyboard.press("Tab"); pg.keyboard.press("Tab")
    print("2 focus după Tab:", pg.evaluate("document.activeElement.className + ' | ' + document.activeElement.textContent.trim().slice(0,30)"))
    pg.click("#c-grasimi"); pg.wait_for_timeout(1200)
    print("3 clic chip -> hash", pg.evaluate("location.hash"), "| y formular:", pg.evaluate("Math.round(document.querySelector('#solicitare').getBoundingClientRect().top)"), "| descriere:", repr(pg.input_value("#f-problema")))
    pg.fill("#f-problema", "")
    # formular
    reqs = []
    pg.on("request", lambda r: reqs.append(r.url) if "web3forms" in r.url else None)
    pg.click("#solicitare button[type=submit]"); pg.wait_for_timeout(200)
    print("4 trimitere goală -> stare:", repr(pg.inner_text("#solicitare-stare")), "| valid:", pg.evaluate("document.getElementById('solicitare').checkValidity()"))
    pg.fill("#f-nume", "Test SRL"); pg.fill("#f-telefon", "0700 000 000"); pg.fill("#f-problema", "Calcar pe schimbător")
    pg.click("#solicitare button[type=submit]"); pg.wait_for_timeout(300)
    print("5 cheie lipsă ->", repr(pg.inner_text("#solicitare-stare")), "| cereri:", reqs)
    # cu cheie reală (API simulat)
    sent = {}
    def ok(route):
        sent.update(json.loads(route.request.post_data)); route.fulfill(status=200, content_type="application/json", body='{"success":true,"message":"ok"}')
    pg.route("https://api.web3forms.com/submit", ok)
    pg.evaluate("document.querySelector('[name=access_key]').value='cheie-test'")
    pg.click("#solicitare button[type=submit]"); pg.wait_for_timeout(500)
    print("6 succes ->", repr(pg.inner_text("#solicitare-stare")), "| câmpuri trimise:", sorted(sent), "| nume golit:", repr(pg.input_value("#f-nume")))
    pg.unroute("https://api.web3forms.com/submit")
    pg.route("https://api.web3forms.com/submit", lambda r: r.fulfill(status=400, content_type="application/json", body='{"success":false,"message":"bad"}'))
    pg.evaluate("document.querySelector('[name=access_key]').value='cheie-test'")
    pg.fill("#f-nume", "Test SRL"); pg.fill("#f-telefon", "0700"); pg.fill("#f-problema", "x")
    pg.click("#solicitare button[type=submit]"); pg.wait_for_timeout(500)
    print("7 eroare API ->", repr(pg.inner_text("#solicitare-stare")))
    pg.unroute("https://api.web3forms.com/submit")
    pg.route("https://api.web3forms.com/submit", lambda r: r.abort())
    pg.click("#solicitare button[type=submit]"); pg.wait_for_timeout(500)
    print("8 fără rețea ->", repr(pg.inner_text("#solicitare-stare")), "| buton activ:", pg.evaluate("!document.querySelector('#solicitare button').disabled"))
    print("erori JS:", errs)
    # structură
    print("9 titluri:", pg.evaluate("[...document.querySelectorAll('h1,h2,h3')].map(h=>h.tagName+':'+h.textContent.trim().slice(0,38))"))
    print("10 h1:", pg.evaluate("document.querySelectorAll('h1').length"), "| linkuri interne rupte:", pg.evaluate("[...document.querySelectorAll('a[href^=\"#\"]')].filter(a=>a.getAttribute('href').length>1 && !document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href'))"))
    print("11 id-uri duplicate:", pg.evaluate("(()=>{const s={},d=[];document.querySelectorAll('[id]').forEach(e=>{s[e.id]?d.push(e.id):s[e.id]=1});return d})()"))
    pg.close()
    # fără JavaScript
    ctx = b.new_context(java_script_enabled=False, viewport={"width": 1440, "height": 900})
    p2 = ctx.new_page(); p2.goto(URL)
    print("12 fără JS: aplicații vizibile", p2.locator(".app:visible").count(), "| probleme:", p2.locator(".prob").count(), "| formular cu action:", p2.get_attribute("#solicitare", "action"))
    ctx.close()
    # lățimi înguste
    for w in (320, 360, 414, 768, 1024, 1280, 1920):
        pg = b.new_page(viewport={"width": w, "height": 800}); pg.goto(URL); pg.wait_for_timeout(500)
        over = pg.evaluate("""()=>{const W=document.documentElement.clientWidth;return [...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>W+1||r.left<-1)&&!e.closest('.hp')&&!e.closest('.skip')}).slice(0,5).map(e=>e.className||e.tagName)}""")
        print(f"13 lățime {w}: scrollWidth", pg.evaluate("document.documentElement.scrollWidth"), "| depășiri:", over)
        pg.close()
    b.close()
