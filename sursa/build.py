#!/usr/bin/env python3
"""Construiește site-ul: dist/ (de urcat pe domeniu) și preview/ (previzualizare).

Rulare:  python3 build.py            -> doar fișierele
         python3 build.py --imagini  -> regenerează și imaginile (og.png, apple-touch-icon.png)
"""
import base64, datetime, hashlib, html, json, os, re, shutil, sys

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.environ.get("OUT_DIR", ROOT)                       # pentru build-uri de test
DIST, PREVIEW = os.path.join(OUT, "dist"), os.path.join(OUT, "preview")
SITE = json.load(open(os.environ.get("SITE_JSON", os.path.join(ROOT, "site.json")), encoding="utf-8"))

# ---------------------------------------------------------------- date și marcaje
LABELS = {
    "brand": "[Nume brand]",
    "persoana": "[Prenume Nume]",
    "zona": "[zona]",
    "localitati": "[localitățile deservite]",
    "telefon_afisat": "[07xx xxx xxx]",
    "email": "[adresa de e-mail]",
    "program": "[luni–vineri, 08:00–17:00]",
    "raspuns": "[intervalul de răspuns]",
    "cost_evaluare": "[Evaluarea este gratuită sau are un tarif: de completat.]",
    "ani_experienta": "[X]",
    "industrii": "[industriile în care am lucrat]",
    "domeniu": "[domeniu.ro]",
    "firma_denumire": "[Denumirea firmei, cu forma juridică]",
    "firma_cui": "[CUI]",
    "firma_reg_com": "[J00/000/0000]",
    "sediu_strada": "[strada și numărul]",
    "sediu_localitate": "[localitatea]",
    "sediu_judet": "[județul]",
    "sediu_cod_postal": "[codul poștal]",
    "web3forms_cheie": "[CHEIE-WEB3FORMS]",
}
OPTIONAL = {"whatsapp", "linkedin", "cloudflare_analytics_token", "telefon_international",
            "program_zile", "program_deschidere", "program_inchidere", "_nota"}
missing = [k for k in LABELS if not SITE.get(k)]
if not SITE.get("politica_url"):
    missing.append("politica_url")
if SITE.get("telefon_afisat") and not SITE.get("telefon_international"):
    missing.append("telefon_international")
# cazuri: null = de completat (apar marcate) | [] = secțiunea se scoate | listă = cazuri reale
CASES = SITE.get("cazuri")
if CASES is None:
    missing.append("cazuri")
if not SITE.get("foto"):
    missing.append("foto")
DRAFT = bool(missing)


def esc(s):
    return html.escape(str(s), quote=True)


def years_text():
    """«12 ani», dar «20 de ani»: de la 20 în sus se pune «de», cu excepția terminațiilor 01-19."""
    n = str(SITE.get("ani_experienta") or "").strip()
    if not n.isdigit():
        return None
    return f"{n} ani" if 2 <= int(n) % 100 <= 19 else f"{n} de ani"


def H(key):
    """Valoare pentru HTML: reală sau marcaj vizibil."""
    if key == "ani_text":
        return esc(years_text()) if years_text() else f'<span class="ph">{esc(LABELS["ani_experienta"])}</span> ani'
    v = SITE.get(key)
    return esc(v) if v else f'<span class="ph">{esc(LABELS[key])}</span>'


def T(key):
    """Valoare pentru text simplu (meta, date structurate)."""
    if key == "ani_text":
        return years_text() or LABELS["ani_experienta"] + " ani"
    return str(SITE.get(key) or LABELS[key])


def fmt_html(text):
    out = esc(text)
    out = re.sub(r"\{(\w+)\}", lambda m: H(m.group(1)), out)
    return re.sub(r"(?<!>)(\[[^\]<]+\])(?!<)", r'<span class="ph">\1</span>', out)


SHOW_PROBLEMS = getattr(C, "SHOW_PROBLEMS", True)
PROBLEM_IDS = {p["id"] for p in C.PROBLEMS}


def rich(text):
    """Text cu legături interne scrise ca [[id|text]]. Legătura dispare dacă ținta nu mai este în pagină."""
    def link(m):
        target, label = m.group(1), m.group(2)
        if target in PROBLEM_IDS and not SHOW_PROBLEMS:
            return label
        return f'<a href="#{target}">{label}</a>'
    return re.sub(r"\[\[([\w-]+)\|([^\]]+)\]\]", link, esc(text))


def fmt_text(text):
    return re.sub(r"\{(\w+)\}", lambda m: T(m.group(1)), text)


TEL_TEXT = T("telefon_afisat")
TEL_HREF = f'tel:{SITE["telefon_international"]}' if SITE.get("telefon_international") else "#contact"
DOMAIN = SITE.get("domeniu") or "domeniu.ro"
BASE = f"https://{DOMAIN}/"

# ---------------------------------------------------------------- culori pH
PH = ["#C81E2B", "#DA3A25", "#E7591F", "#EE7B1D", "#F29F22", "#F2C230", "#C9C63A", "#5FAE46",
      "#2E9E73", "#1C8F9A", "#1F78B4", "#2B5DAE", "#3A46A3", "#4E3597", "#5E2A86"]
INK = "#12324A"


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


ON = [INK if contrast(c, INK) >= contrast(c, "#FFFFFF") else "#FFFFFF" for c in PH]
PH_VARS = "".join(f"  --ph{i}: {c}; --on{i}: {ON[i]};\n" for i, c in enumerate(PH))

# ---------------------------------------------------------------- fonturi
FONTS = [
    ("Sofia Sans", "sofia-sans.woff2", "400 700"),
    ("Sofia Sans Extra Condensed", "sofia-sans-extra-condensed.woff2", "500 900"),
]
FALLBACK_FACES = (
    '@font-face{font-family:"Titlu fallback";font-weight:500 900;'
    'src:local("Arial Bold"),local("Arial-BoldMT"),local("Roboto Bold"),local("Liberation Sans Bold");'
    'size-adjust:64.8%;ascent-override:138.8%;descent-override:46.3%;line-gap-override:0%}\n'
    '@font-face{font-family:"Text fallback";'
    'src:local("Arial"),local("ArialMT"),local("Roboto"),local("Liberation Sans");'
    'size-adjust:97.4%;ascent-override:92.4%;descent-override:30.8%;line-gap-override:0%}\n'
)


def font_bytes(name):
    return open(os.path.join(SRC, "fonts", name), "rb").read()


def hashed(name):
    digest = hashlib.sha256(font_bytes(name)).hexdigest()[:8]
    stem, ext = os.path.splitext(name)
    return f"{stem}.{digest}{ext}"


def font_faces(inline):
    out = ""
    for family, name, weight in FONTS:
        if inline:
            url = "data:font/woff2;base64," + base64.b64encode(font_bytes(name)).decode()
        else:
            url = "fonts/" + hashed(name)
        out += (f'@font-face{{font-family:"{family}";font-style:normal;font-weight:{weight};'
                f'font-display:swap;src:url("{url}") format("woff2")}}\n')
    return out + FALLBACK_FACES


# ---------------------------------------------------------------- CSS
def chip_rules():
    rules = []
    for p in C.PROBLEMS:
        rules.append(
            f'.hero:has(#c-{p["id"]}:is(:hover,:focus-visible)) '
            f'.cell:not(:nth-child(n+{p["lo"] + 1}):nth-child(-n+{p["hi"] + 1}))'
            "{background:var(--off);color:var(--ink-soft)}"
        )
    return "\n".join(rules)


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def build_css(inline_fonts):
    css = open(os.path.join(SRC, "styles.css"), encoding="utf-8").read()
    faces = font_faces(inline_fonts)
    css = css.replace("/*@FONT_FACES@*/", "").replace("/*@PH_VARS@*/", PH_VARS).replace("/*@CHIP_RULES@*/", chip_rules())
    return faces + minify_css(css)


# ---------------------------------------------------------------- fragmente SVG
MARK = (f'<svg viewBox="0 0 36 36" aria-hidden="true" focusable="false">'
        f'<rect x="3" y="4" width="8" height="28" fill="{PH[1]}"/>'
        f'<rect x="14" y="4" width="8" height="28" fill="{PH[7]}"/>'
        f'<rect x="25" y="4" width="8" height="28" fill="{PH[13]}"/></svg>')
FAVICON = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">'
           f'<rect width="36" height="36" rx="5" fill="#FFFFFF"/>'
           f'<rect x="5" y="6" width="7" height="24" fill="{PH[1]}"/>'
           f'<rect x="14.5" y="6" width="7" height="24" fill="{PH[7]}"/>'
           f'<rect x="24" y="6" width="7" height="24" fill="{PH[13]}"/></svg>\n')
DIAMOND = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
           '<path d="M12 1.8 22.2 12 12 22.2 1.8 12Z" fill="#fff" stroke="#C8202C" stroke-width="2.4" stroke-linejoin="round"/>'
           '<path d="M12 6.8v6.4" stroke="#12324A" stroke-width="2.4" stroke-linecap="round"/>'
           '<circle cx="12" cy="16.9" r="1.45" fill="#12324A"/></svg>')
SINNER = ('<svg viewBox="0 0 240 240" role="img" aria-label="Cercul lui Sinner: chimie, temperatură, timp de contact și acțiune mecanică">'
          '<path d="M120 120V8a112 112 0 0 1 112 112Z" fill="#12324A"/>'
          '<path d="M120 120h112a112 112 0 0 1-112 112Z" fill="#2F5A7A"/>'
          '<path d="M120 120v112A112 112 0 0 1 8 120Z" fill="#C6D2DA"/>'
          '<path d="M120 120H8A112 112 0 0 1 120 8Z" fill="#E1E8EC"/>'
          '<path d="M120 4v232M4 120h232" stroke="#fff" stroke-width="4"/>'
          '<text x="166" y="80" text-anchor="middle" fill="#fff">Chimie</text>'
          '<text x="166" y="170" text-anchor="middle" fill="#fff">Temperatură</text>'
          '<text x="74" y="170" text-anchor="middle" fill="#12324A">Timp de contact</text>'
          '<text x="74" y="71" text-anchor="middle" fill="#12324A">Acțiune</text>'
          '<text x="74" y="90" text-anchor="middle" fill="#12324A">mecanică</text></svg>')


# ---------------------------------------------------------------- HTML: secțiuni
def ph_range(p):
    return f'pH {p["lo"]}–{p["hi"]}'


def zone_index(p):
    return (p["lo"] + p["hi"]) // 2


def html_header():
    return f'''<header class="wrap top">
  <a class="brand" href="#sus">{MARK}<span><span class="brand-name">{H("brand")}</span><span class="brand-sub">Soluții chimice profesionale</span></span></a>
  <nav class="nav" aria-label="Secțiunile paginii">
    <ul>
{'      <li><a href="#probleme">Probleme</a></li>' + chr(10) if SHOW_PROBLEMS else ''}      <li><a href="#aplicatii">Aplicații</a></li>
      <li><a href="#facilitati">Facilități</a></li>
      <li><a href="#cum-lucrez">Cum lucrez</a></li>
      <li><a href="#intrebari">Întrebări</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>
  <a class="top-tel" href="{TEL_HREF}">{H("telefon_afisat")}</a>
</header>'''


AFTER_LINE = ('<p class="after">Problema dumneavoastră nu este în listă? <a href="#contact">Descrieți problema</a> '
              'și vă spun dacă o pot rezolva.</p>')


def chip_href(p):
    """Cu secțiunea de probleme scoasă, eticheta duce la formular și îi precompletează descrierea."""
    if SHOW_PROBLEMS:
        return f'#{p["id"]}'
    return f'#solicitare" data-problema="{esc(p["short"])}'


def html_hero():
    after = "" if SHOW_PROBLEMS else f'\n  <div class="wrap">{AFTER_LINE}</div>'
    chips = "\n".join(
        f'      <li><a class="chip" id="c-{p["id"]}" href="{chip_href(p)}" style="--a:var(--ph{p["lo"]});--b:var(--ph{p["hi"]})">'
        f'<span class="chip-sw"></span>{esc(p["short"])} <span class="chip-ph">{ph_range(p)}</span></a></li>'
        for p in C.PROBLEMS)
    cells = "".join(f'<span class="cell" style="--c:var(--ph{i});--on:var(--on{i});--i:{i}">{i}</span>' for i in range(15))
    return f'''<section class="hero" id="sus">
  <div class="wrap">
    <h1>{esc(C.H1)}</h1>
    <div class="hero-row">
      <div>
        <p class="lead">{fmt_html(C.LEAD)}</p>
        <div class="cta">
          <a class="btn" href="{TEL_HREF}">Sunați la {H("telefon_afisat")}</a>
          <a class="btn btn-ghost" href="#contact">Descrieți problema</a>
        </div>
      </div>
      <dl class="facts">
        <div><dt>Clienți</dt><dd>Exclusiv firme</dd></div>
        <div><dt>Zonă</dt><dd>{H("zona")}</dd></div>
        <div><dt>Răspuns</dt><dd>{H("raspuns")}</dd></div>
      </dl>
    </div>
    <nav class="pick" aria-labelledby="alege">
      <p class="pick-q" id="alege">Ce aveți de curățat?</p>
      <ul class="chips">
{chips}
      </ul>
    </nav>
  </div>
  <div class="scale" role="img" aria-label="Scala de pH, de la 0 (acid) la 14 (alcalin)">{cells}</div>
  <div class="scale-key" aria-hidden="true"><span>Acid</span><span>Neutru</span><span>Alcalin</span></div>{after}
</section>'''


def html_problems():
    if not SHOW_PROBLEMS:
        return ""
    rows = []
    for p in C.PROBLEMS:
        mini = "".join(
            f'<span class="on" style="--c:var(--ph{i})"></span>' if p["lo"] <= i <= p["hi"] else "<span></span>"
            for i in range(15))
        rows.append(f'''    <article class="prob" id="{p["id"]}" style="--zone:var(--ph{zone_index(p)})">
      <div class="prob-meta">
        <p class="prob-ph">{ph_range(p)}</p>
        <p class="prob-kind">{esc(p["kind"])}</p>
        <div class="mini" aria-hidden="true">{mini}</div>
      </div>
      <div class="prob-body">
        <h3>{esc(p["title"])}</h3>
        <p><strong>Ce este.</strong> {esc(p["what"])}</p>
        <p><strong>Unde apare.</strong> {esc(p["where"])}</p>
        <p><strong>Cum se tratează.</strong> {esc(p["how"])}</p>
      </div>
      <div class="warn">
        <p class="warn-h">{DIAMOND}Greșeala frecventă</p>
        <p>{esc(p["mistake"])}</p>
      </div>
    </article>''')
    return f'''<section class="sec" id="probleme">
  <div class="wrap">
    <h2>Probleme de curățare pe care le rezolv</h2>
    <p class="intro">Fiecare tip de murdărie cere altă chimie. Lista este ordonată de la soluții acide la soluții alcaline. Intervalele de pH sunt orientative și se referă la soluția de lucru.</p>
    <div class="probs">
{chr(10).join(rows)}
    </div>
    <div class="rule">
      <p class="rule-main">{DIAMOND}<span>Regulă valabilă peste tot: produsele clorinate nu se amestecă niciodată cu produse acide. Din reacție rezultă clor gazos, toxic.</span></p>
      <p class="rule-note">Informațiile de pe această pagină sunt orientative. Produsul, concentrația, temperatura și timpul de contact se stabilesc după evaluare, conform fișei tehnice și fișei cu date de securitate.</p>
    </div>
    {AFTER_LINE}
  </div>
</section>'''


def html_apps():
    """Selector de echipamente: listă în stânga, fișa echipamentului ales în dreapta (acordeon pe mobil)."""
    show_how = getattr(C, "APPS_SHOW_HOW", True)
    ranges = {p["id"]: (p["lo"], p["hi"]) for p in C.PROBLEMS}

    def deposits(text):
        """[[id|depunere]] devine depunerea marcată cu culorile zonei ei de pH, ca în etichetele de sub titlu."""
        def mark(m):
            lo, hi = ranges[m.group(1)]
            return f'<span class="dep" style="--a:var(--ph{lo});--b:var(--ph{hi})">{m.group(2)}</span>'
        return re.sub(r"\[\[([\w-]+)\|([^\]]+)\]\]", mark, esc(text))

    items = []
    for i, a in enumerate(C.APPS):
        how = (f'\n          <div><p class="app-label">Cum se curăță</p><p>{rich(a["how"])}</p></div>' if show_how else "")
        items.append(f'''      <details class="app" id="{a["id"]}" name="aplicatie"{" open" if i == 0 else ""}>
        <summary><h3>{esc(a["title"])}</h3><span class="app-unit" aria-hidden="true">{esc(a["unit"])}</span></summary>
        <div class="app-panel">
          <p class="app-token">{esc(a["token"])}</p>
          <p class="app-note">{esc(a["token_note"])}</p>
          <div class="app-cols">
            <div><p class="app-label">Ce se depune</p><p>{deposits(a["soil"])}</p></div>{how}
            <div><p class="app-label">Cum se verifică</p><p>{rich(a["check"])}</p></div>
          </div>
          <a class="btn" href="#solicitare" data-problema="{esc(a["title"])}">Descrieți problema</a>
        </div>
      </details>''')
    intro = C.APPS_INTRO_WITH_HOW if show_how else C.APPS_INTRO
    note = "" if SHOW_PROBLEMS else f'\n    <p class="apps-note">{esc(C.APPS_NOTE)}</p>'
    return f'''<section class="sec{" sec-tight" if SHOW_PROBLEMS else ""}" id="aplicatii">
  <div class="wrap">
    <h2>{esc(C.APPS_TITLE)}</h2>
    <p class="intro">{esc(intro)}</p>
    <div class="apps">
{chr(10).join(items)}
    </div>{note}
  </div>
</section>'''


def html_facilities():
    items = "\n".join(f"      <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in C.FACILITIES)
    return f'''<section class="sec sec-tight" id="facilitati">
  <div class="wrap">
    <h2>Facilități pentru care lucrez</h2>
    <p class="intro">Lucrez exclusiv cu firme din {H("zona")}.</p>
    <ul class="fac">
{items}
    </ul>
  </div>
</section>'''


def html_process():
    steps = "\n".join(f"      <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in C.STEPS)
    paras = "\n".join(f"        <p>{esc(t)}</p>" for t in C.SINNER_TEXT)
    return f'''<section class="sec sec-tight" id="cum-lucrez">
  <div class="wrap">
    <h2>Cum lucrez</h2>
    <ol class="steps">
{steps}
    </ol>
    <div class="sinner">
      {SINNER}
      <div>
        <h3>{esc(C.SINNER_TITLE)}</h3>
{paras}
      </div>
    </div>
  </div>
</section>'''


def html_cases():
    def card(pairs, render):
        rows = "".join(
            f'<div><dt>{esc(label)}</dt><dd{" class=\"result\"" if label == "Rezultat" else ""}>{render(value)}</dd></div>'
            for label, value in pairs)
        return f'      <article class="case"><dl>{rows}</dl></article>'

    if CASES is None:
        cards = [card(C.CASE_FIELDS, fmt_html) for _ in range(C.CASE_COUNT)]
        intro = fmt_html("[Trei situații reale, cu cifre măsurate la client. Fără date reale, secțiunea se scoate din pagină.]")
    elif not CASES:
        return ""
    else:
        labels = [label for label, _ in C.CASE_FIELDS]
        keys = ["facilitate", "problema", "schimbare", "rezultat"]
        cards = [card([(l, case[k]) for l, k in zip(labels, keys)], esc) for case in CASES]
        intro = "Situații reale, cu rezultate măsurate la client."
    return f'''<section class="sec sec-tight" id="cazuri">
  <div class="wrap">
    <h2>Cazuri din teren</h2>
    <p class="intro">{intro}</p>
    <div class="cases">
{chr(10).join(cards)}
    </div>
  </div>
</section>'''


def html_about():
    if SITE.get("foto"):
        photo = (f'<img class="photo-img" src="{esc(SITE["foto"])}" width="880" height="1100" '
                 f'alt="{esc(T("persoana"))}, consultant tehnic, la un client" loading="lazy" decoding="async">')
    else:
        photo = '<div class="photo">[Fotografie reală, în teren sau la un client. Format vertical 4:5, minimum 880 x 1100 px.]</div>'
    paras = "\n".join(f"      <p>{fmt_html(t)}</p>" for t in C.ABOUT)
    return f'''<section class="sec sec-tight" id="despre">
  <div class="wrap about">
    {photo}
    <div class="about-text">
      <h2>Cine răspunde la telefon</h2>
{paras}
    </div>
  </div>
</section>'''


def html_faq():
    items = "\n".join(
        f"      <details><summary>{esc(q)}</summary><p>{fmt_html(a)}</p></details>" for q, a in C.FAQ)
    return f'''<section class="sec sec-tight" id="intrebari">
  <div class="wrap">
    <h2>Întrebări frecvente</h2>
    <div class="faq">
{items}
    </div>
  </div>
</section>'''


def html_contact(preview):
    options = "".join(f"<option>{esc(o)}</option>" for o in C.FACILITY_OPTIONS)
    ways = []
    if SITE.get("whatsapp"):
        digits = re.sub(r"\D", "", SITE["whatsapp"])
        ways.append(f'<div><dt>WhatsApp</dt><dd><a href="https://wa.me/{digits}">Scrieți pe WhatsApp</a></dd></div>')
    elif DRAFT:
        ways.append(f'<div><dt>WhatsApp</dt><dd>{fmt_html("[link WhatsApp, dacă îl folosești]")}</dd></div>')
    email = SITE.get("email")
    ways.append(f'<div><dt>E-mail</dt><dd>{f"<a href=\"mailto:{esc(email)}\">{esc(email)}</a>" if email else H("email")}</dd></div>')
    ways.append(f'<div><dt>Program</dt><dd>{H("program")}</dd></div>')
    ways.append(f'<div><dt>Zonă</dt><dd>{H("zona")}</dd></div>')
    action = "" if preview else ' action="https://api.web3forms.com/submit" method="POST"'
    redirect = "" if preview else f'\n        <input type="hidden" name="redirect" value="{BASE}#trimis">'
    privacy = (f'<a href="{esc(SITE["politica_url"])}">politica de confidențialitate</a>' if SITE.get("politica_url")
               else '<a class="ph" href="#contact">[politica de confidențialitate]</a>')
    return f'''<section class="band" id="contact">
  <div class="wrap sec contact">
    <div>
      <h2>Descrieți problema</h2>
      <p class="intro">Sunați sau completați formularul. Cu cât detaliile sunt mai exacte, cu atât recomandarea vine mai repede.</p>
      <a class="tel-xl" href="{TEL_HREF}">{H("telefon_afisat")}</a>
      <dl class="ways">
        {"".join(ways)}
      </dl>
      <div class="need">
        <h3>{esc(C.NEED_TITLE)}</h3>
        <p>{esc(C.NEED_INTRO)}</p>
        <ul>{"".join(f"<li>{esc(n)}</li>" for n in C.NEED)}</ul>
      </div>
    </div>
    <div>
      <p class="sent" id="trimis">Solicitarea a fost trimisă. Vă sun în cel mai scurt timp.</p>
      <form class="form" id="solicitare"{action} data-tel="{esc(TEL_TEXT)}">
        <input type="hidden" name="access_key" value="{esc(T("web3forms_cheie"))}">
        <input type="hidden" name="subject" value="Solicitare nouă de pe site">
        <input type="hidden" name="from_name" value="{esc(T("brand"))}">{redirect}
        <input class="hp" type="checkbox" name="botcheck" id="f-verificare" tabindex="-1" aria-hidden="true">
        <div class="form-row">
          <div class="field"><label for="f-nume">Nume și firmă</label><input id="f-nume" name="nume_si_firma" type="text" autocomplete="organization" required></div>
          <div class="field"><label for="f-telefon">Telefon</label><input id="f-telefon" name="telefon" type="tel" inputmode="tel" autocomplete="tel" required></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-localitate">Localitate</label><input id="f-localitate" name="localitate" type="text" autocomplete="address-level2"></div>
          <div class="field"><label for="f-facilitate">Tipul facilității</label><select id="f-facilitate" name="tipul_facilitatii"><option value="">Alegeți</option>{options}</select></div>
        </div>
        <div class="field">
          <label for="f-problema">Ce aveți de curățat?</label>
          <textarea id="f-problema" name="problema" rows="4" required aria-describedby="f-problema-ajutor"></textarea>
          <span class="hint" id="f-problema-ajutor">Tipul depunerii, suprafața sau instalația și ce ați încercat până acum.</span>
        </div>
        <button class="btn" type="submit">Trimiteți solicitarea</button>
        <p class="form-state" id="solicitare-stare" role="status" aria-live="polite"></p>
        <p class="form-note">Folosesc datele doar pentru a răspunde la această solicitare. Detalii în {privacy}.</p>
      </form>
    </div>
  </div>
  <footer class="wrap foot">
    <div class="foot-in">
      <p>{H("firma_denumire")}, CUI {H("firma_cui")}, nr. Reg. Com. {H("firma_reg_com")}. Sediu: {H("sediu_strada")}, {H("sediu_localitate")}, jud. {H("sediu_judet")}.</p>
      <p>© {datetime.date.today().year} {H("brand")}</p>
    </div>
  </footer>
</section>'''


def html_dock():
    return f'''<div class="dock">
  <a class="btn" href="{TEL_HREF}">Sunați</a>
  <a class="btn btn-ghost" href="#contact">Descrieți problema</a>
</div>'''


def html_body(preview):
    draft = ('<div class="draft-bar"><div class="wrap">Versiune de lucru. Textele marcate așteaptă datele reale, '
             'iar pagina rămâne blocată la indexare până la completarea lor.</div></div>\n') if DRAFT else ""
    parts = [html_header(), "<main id=\"continut\">", html_hero(), html_problems(), html_apps(), html_facilities(),
             html_process(), html_cases(), html_about(), html_faq(), "</main>", html_contact(preview), html_dock()]
    return f'<a class="skip" href="#continut">Salt la conținut</a>\n{draft}' + "\n".join(parts)


# ---------------------------------------------------------------- date structurate
def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def json_ld():
    title, desc = fmt_text(C.TITLE), fmt_text(C.DESCRIPTION)
    business = {
        "@type": "ProfessionalService",
        "@id": BASE + "#firma",
        "name": T("brand"),
        "legalName": T("firma_denumire"),
        "description": desc,
        "url": BASE,
        "image": BASE + "og.png",
        "telephone": SITE.get("telefon_international") or T("telefon_afisat"),
        "email": T("email"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": T("sediu_strada"),
            "addressLocality": T("sediu_localitate"),
            "addressRegion": T("sediu_judet"),
            "postalCode": T("sediu_cod_postal"),
            "addressCountry": "RO",
        },
        "areaServed": {"@type": "AdministrativeArea", "name": T("zona")},
        "knowsAbout": C.KNOWS_ABOUT,
    }
    if SITE.get("program_zile") and SITE.get("program_deschidere") and SITE.get("program_inchidere"):
        business["openingHoursSpecification"] = [{
            "@type": "OpeningHoursSpecification", "dayOfWeek": SITE["program_zile"],
            "opens": SITE["program_deschidere"], "closes": SITE["program_inchidere"]}]
    if SITE.get("firma_cui"):
        business["vatID"] = SITE["firma_cui"]
    if SITE.get("linkedin"):
        business["sameAs"] = [SITE["linkedin"]]
    graph = [
        business,
        {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": T("brand"), "inLanguage": "ro-RO",
         "publisher": {"@id": BASE + "#firma"}},
        {"@type": "WebPage", "@id": BASE + "#pagina", "url": BASE, "name": title, "description": desc,
         "inLanguage": "ro-RO", "isPartOf": {"@id": BASE + "#site"}, "about": {"@id": BASE + "#firma"}},
        {"@type": "FAQPage", "@id": BASE + "#intrebari", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": fmt_text(a)}}
            for q, a in C.FAQ]},
    ]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return data.replace("</", "<\\/")


# ---------------------------------------------------------------- pagini
def page_production():
    title, desc = fmt_text(C.TITLE), fmt_text(C.DESCRIPTION)
    robots = "noindex, nofollow" if DRAFT else "index, follow, max-image-preview:large"
    preload = "\n".join(
        f'<link rel="preload" href="fonts/{hashed(name)}" as="font" type="font/woff2" crossorigin>' for _, name, _ in reversed(FONTS))
    token = SITE.get("cloudflare_analytics_token")
    analytics = (f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{esc(token)}"}}\'></script>'
                 if token else "<!-- Analiză de trafic fără cookie-uri: se activează din site.json (cloudflare_analytics_token) sau direct din panoul Cloudflare. -->")
    js = open(os.path.join(SRC, "script.js"), encoding="utf-8").read().strip()
    return f'''<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{BASE}">
{preload}
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="{INK}">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:locale" content="ro_RO">
<meta property="og:site_name" content="{esc(T("brand"))}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>{build_css(False)}</style>
<script type="application/ld+json">{json_ld()}</script>
</head>
<body>
{html_body(False)}
<script>{js}</script>
{analytics}
</body>
</html>
'''


def page_preview():
    js = open(os.path.join(SRC, "script.js"), encoding="utf-8").read().strip()
    return f'''<title>{esc(C.PREVIEW_TITLE)}</title>
<style>{build_css(True)}</style>
{html_body(True)}
<script>{js}</script>
'''


PAGE_404 = f'''<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pagina nu există</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>body{{margin:0;min-height:100vh;display:grid;place-content:center;gap:1rem;padding:1.5rem;background:#EDF0F1;color:{INK};font:1.0625rem/1.6 Arial,Helvetica,sans-serif}}h1{{margin:0;font-size:2.25rem;line-height:1.1}}p{{margin:0;max-width:32rem}}a{{color:inherit;font-weight:700}}</style>
</head>
<body>
<h1>Pagina nu există</h1>
<p>Adresa este greșită sau pagina a fost mutată. Tot conținutul site-ului se află pe <a href="/">prima pagină</a>.</p>
</body>
</html>
'''


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    for d in (os.path.join(DIST, "fonts"),):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    for _, name, _ in FONTS:
        shutil.copyfile(os.path.join(SRC, "fonts", name), os.path.join(DIST, "fonts", hashed(name)))
    shutil.copyfile(os.path.join(SRC, "fonts", "OFL.txt"), os.path.join(DIST, "fonts", "LICENTA-FONTURI.txt"))

    write(os.path.join(DIST, "index.html"), page_production())
    write(os.path.join(PREVIEW, "index.html"), page_preview())
    write(os.path.join(DIST, "404.html"), PAGE_404)
    write(os.path.join(DIST, "favicon.svg"), FAVICON)
    robots = "User-agent: *\nDisallow: /\n" if DRAFT else f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n"
    write(os.path.join(DIST, "robots.txt"), robots)
    write(os.path.join(DIST, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"  <url>\n    <loc>{BASE}</loc>\n    <lastmod>{datetime.date.today().isoformat()}</lastmod>\n  </url>\n</urlset>\n")
    write(os.path.join(DIST, "_headers"),
          "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
          "  X-Frame-Options: DENY\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n"
          "/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n\n"
          "# Adresa tehnică de la Cloudflare nu trebuie să apară în Google ca dublură a domeniului.\n"
          "https://:project.pages.dev/*\n  X-Robots-Tag: noindex\n\n"
          "https://:version.:project.pages.dev/*\n  X-Robots-Tag: noindex\n")

    if "--imagini" in sys.argv:
        import images
        images.render(ROOT, DIST, SRC, PH, ON, INK, C.H1, T("brand"), FAVICON)

    # ------------------------------------------------------------ raport
    title, desc = fmt_text(C.TITLE), fmt_text(C.DESCRIPTION)
    size = lambda p: os.path.getsize(p)
    index = os.path.join(DIST, "index.html")
    fonts = sum(size(os.path.join(DIST, "fonts", f)) for f in os.listdir(os.path.join(DIST, "fonts")) if f.endswith(".woff2"))
    print(f"Mod: {'LUCRU (noindex)' if DRAFT else 'FINAL (indexabil)'}")
    print(f"Titlu: {len(title)} caractere | Descriere: {len(desc)} caractere")
    print(f"index.html: {size(index) / 1024:.1f} KB | fonturi: {fonts / 1024:.1f} KB | previzualizare: {size(os.path.join(PREVIEW, 'index.html')) / 1024:.1f} KB")
    if len(title) > 60:
        print(f"ATENȚIE: titlul are {len(title)} caractere (recomandat: maximum 60).")
    if len(desc) > 160:
        print(f"ATENȚIE: descrierea are {len(desc)} caractere (recomandat: maximum 160).")
    if missing:
        print("Date lipsă:", ", ".join(missing))


if __name__ == "__main__":
    main()
