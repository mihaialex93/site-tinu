"""Generează og.png (1200x630) și apple-touch-icon.png (180x180) cu Chromium."""
import base64, html, os, pathlib

from playwright.sync_api import sync_playwright


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:
        return p.chromium.launch(executable_path="/opt/pw-browsers/chromium")


def render(root, dist, src, PH, ON, INK, h1, brand, favicon_svg):
    data = lambda name: "data:font/woff2;base64," + base64.b64encode(pathlib.Path(src, "fonts", name).read_bytes()).decode()
    font = data("sofia-sans-extra-condensed.woff2")
    body = data("sofia-sans.woff2")
    cells = "".join(f'<span style="background:{c};color:{ON[i]}">{i}</span>' for i, c in enumerate(PH))
    og = f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:D;src:url("{font}");font-weight:500 900}}
@font-face{{font-family:B;src:url("{body}");font-weight:400 700}}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;background:#EDF0F1;color:{INK};display:flex;flex-direction:column;justify-content:space-between}}
.t{{padding:64px 72px 0}}
.b{{font:700 30px/1 B;display:flex;align-items:center;gap:14px}}
.b i{{display:inline-flex;gap:4px}}.b i b{{width:10px;height:34px;display:block}}
h1{{font:800 104px/.94 D;margin-top:48px;max-width:1056px;text-wrap:balance}}
.s{{display:grid;grid-template-columns:repeat(15,1fr)}}
.s span{{height:118px;display:flex;align-items:flex-end;padding:8px 10px;font:800 34px/1 D}}
</style><div class="t"><div class="b"><i><b style="background:{PH[1]}"></b><b style="background:{PH[7]}"></b><b style="background:{PH[13]}"></b></i>{html.escape(brand)}</div>
<h1>{html.escape(h1)}</h1></div><div class="s">{cells}</div>'''
    icon = f'<!doctype html><meta charset="utf-8"><style>*{{margin:0}}body{{width:180px;height:180px;background:#fff}}svg{{width:180px;height:180px;display:block}}</style>{favicon_svg}'
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        page.set_content(og)
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(dist, "og.png"))
        page.set_viewport_size({"width": 180, "height": 180})
        page.set_content(icon)
        page.screenshot(path=os.path.join(dist, "apple-touch-icon.png"))
        browser.close()
    print("Imagini generate: og.png, apple-touch-icon.png")
