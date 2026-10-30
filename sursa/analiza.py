"""Google Analytics 4 cu acordul vizitatorului (Legea 506/2004).

Fără acord nu se pun cookie-uri: modul de consimțământ pornește cu totul refuzat, iar analiza se acceptă
doar din banner. Alegerea se păstrează în browser (localStorage, cheia „analiza”) și se poate schimba din
butonul „Setări cookie-uri” din subsol. Totul lipsește din pagină cât timp google_analytics_id e gol.
"""
import os
import re

KEY = "analiza"


def ga_id(site):
    gid = (site.get("google_analytics_id") or "").strip()
    if gid and not re.fullmatch(r"G-[A-Z0-9]{4,20}", gid):
        raise SystemExit(f"google_analytics_id invalid: {gid!r}. Formatul este G-XXXXXXXXXX.")
    return gid


def head(gid):
    """Se pune imediat după meta viewport. Acordul implicit se citește din alegerea salvată."""
    if not gid:
        return ""
    return f'''
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag("consent", "default", {{"ad_storage": "denied", "ad_user_data": "denied", "ad_personalization": "denied",
  "analytics_storage": (function () {{ try {{ return localStorage.getItem("{KEY}") === "da" ? "granted" : "denied"; }} catch (e) {{ return "denied"; }} }})()}});
gtag("js", new Date());
gtag("config", "{gid}");
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'''


def banner(gid, politica_url):
    """Bannerul e ascuns implicit; scriptul îl arată doar dacă nu există o alegere salvată."""
    if not gid:
        return ""
    policy = f' Detalii în <a href="{politica_url}">politica de confidențialitate</a>.' if politica_url else ""
    return f'''<section class="consent" id="consimtamant" aria-labelledby="consimtamant-titlu" tabindex="-1" hidden>
  <h2 id="consimtamant-titlu">Cookie-uri de analiză</h2>
  <p>Folosesc Google Analytics ca să văd câți vizitatori are site-ul și de unde vin. Cookie-urile de analiză se pun doar dacă acceptați. Alegerea se poate schimba oricând din subsolul paginii.{policy}</p>
  <div class="consent-actions">
    <button type="button" class="btn" data-consent="da">Accept</button>
    <button type="button" class="btn" data-consent="nu">Refuz</button>
  </div>
</section>'''


def footer_button(gid):
    if not gid:
        return ""
    return ' · <button type="button" class="foot-btn" data-consent-open>Setări cookie-uri</button>'


CSS = """
.consent{position:fixed;z-index:30;left:1rem;bottom:1rem;width:min(30rem,calc(100% - 2rem));background:var(--panel);color:var(--ink);border:2px solid var(--ink);border-radius:var(--radius);padding:1.1rem 1.25rem 1.25rem;box-shadow:0 .75rem 2.5rem rgb(18 50 74 / .28)}
.consent[hidden]{display:none}
.consent:focus{outline:3px solid var(--ph10);outline-offset:3px}
.consent h2{font-size:1.75rem;line-height:1}
.consent p{margin-top:.55rem;font-size:.9375rem;line-height:1.5}
.consent a{font-weight:700}
.consent-actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.6rem;margin-top:1rem}
.consent .btn{min-height:2.9rem;padding:.55rem 1rem;font-size:1rem}
.foot-btn{background:none;border:0;padding:0;font:inherit;color:#fff;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:.18em;cursor:pointer}
@media (max-width:43.99rem){.consent{left:.75rem;width:calc(100% - 1.5rem);bottom:.75rem}.dock ~ .consent{bottom:calc(3.9rem + 1px + .75rem + env(safe-area-inset-bottom,0px))}}
"""


def css(gid):
    return CSS if gid else ""


def script(gid, src_dir):
    if not gid:
        return ""
    js = open(os.path.join(src_dir, "analiza.js"), encoding="utf-8").read().strip()
    return f"<script>{js}</script>"
