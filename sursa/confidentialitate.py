"""Pagina „Politica de confidențialitate”, publicată la /confidentialitate.

Textele folosesc {cheie} pentru datele din site.json. Descriu ce face site-ul tehnic (Google Analytics cu acord,
Cloudflare, fonturi locale) și contactul prin telefon, WhatsApp și e-mail. Textul trebuie confirmat de proprietar.
"""

UPDATED = "30 octombrie 2026"
PATH = "confidentialitate"

SECTIONS = [
    ("Cine prelucrează datele", [
        "{firma_denumire}, CUI {firma_cui}, nr. Reg. Com. {firma_reg_com}, cu sediul în {sediu_strada}, {sediu_localitate}, "
        "jud. {sediu_judet}. Pentru orice întrebare despre datele dumneavoastră: {email} sau {telefon_afisat}.",
    ]),
    ("Măsurarea vizitelor, doar cu acordul dumneavoastră", [
        "Dacă apăsați „Accept” în fereastra despre cookie-uri, site-ul folosește Google Analytics ca să afle câți vizitatori are, "
        "ce pagini sunt citite, de pe ce tip de dispozitiv și din ce localitate aproximativă vin vizitatorii, prin ce căutare sau "
        "link au ajuns aici și dacă au apăsat pe telefon, WhatsApp sau e-mail. Google pune în browser cookie-urile „_ga”, "
        "cu un identificator aleator. Temeiul este consimțământul dumneavoastră, conform art. 6 alin. (1) lit. a din "
        "Regulamentul (UE) 2016/679.",
        "Dacă apăsați „Refuz” sau nu alegeți nimic, nu se pun cookie-uri de analiză. Google primește doar semnale fără "
        "cookie-uri, pe care le folosește pentru statistici generale.",
        "Pentru vizitatorii din Uniunea Europeană, Google folosește adresa IP doar ca să stabilească localitatea aproximativă, "
        "apoi o șterge. Datele de analiză se păstrează în Google Analytics cel mult 14 luni.",
        "Furnizorul serviciului este Google Ireland Limited. Datele pot ajunge și la Google LLC, în Statele Unite, "
        "cu garanțiile prevăzute de Regulamentul (UE) 2016/679 pentru transferurile în afara Uniunii Europene.",
    ]),
    ("Contactul prin telefon, WhatsApp și e-mail", [
        "Când sunați, scrieți pe WhatsApp sau trimiteți un e-mail, folosesc datele pe care mi le transmiteți, cum ar fi numele, "
        "firma, telefonul, adresa de e-mail și descrierea problemei, doar ca să vă răspund, să evaluez problema și să vă fac o "
        "ofertă. Temeiul este pregătirea sau executarea unui contract, conform art. 6 alin. (1) lit. b din Regulamentul (UE) 2016/679.",
        "Păstrez aceste date cât durează discuția. Dacă lucrăm împreună, le păstrez cât cere legislația contabilă și fiscală.",
        "Mesajele pe WhatsApp trec prin serviciul WhatsApp, operat de WhatsApp Ireland Limited, după propriile reguli de "
        "confidențialitate.",
    ]),
    ("Găzduirea și securitatea site-ului", [
        "Site-ul este găzduit și protejat de Cloudflare. La fiecare vizită, Cloudflare prelucrează date tehnice, cum ar fi "
        "adresa IP și tipul de browser, ca să livreze pagina și să o apere de atacuri. Temeiul este interesul legitim de a avea "
        "un site sigur și funcțional, conform art. 6 alin. (1) lit. f din Regulamentul (UE) 2016/679. Cloudflare ascunde și "
        "adresa de e-mail de pe pagină față de programele care colectează adrese pentru mesaje nedorite.",
        "Fonturile sunt găzduite pe site, fără servicii externe.",
    ]),
    ("Ce se păstrează în browser", [
        "Alegerea dumneavoastră despre cookie-urile de analiză se păstrează în browser, ca fereastra să nu apară la fiecare "
        "vizită. Este strict necesară și nu se trimite nicăieri.",
    ]),
    ("Drepturile dumneavoastră", [
        "Aveți dreptul de acces, de rectificare, de ștergere, de restricționare a prelucrării, de opoziție și la portabilitatea "
        "datelor. Vă puteți retrage oricând acordul pentru analiză, din butonul „Setări cookie-uri” din subsolul paginii. "
        "Retragerea nu afectează prelucrarea făcută înainte.",
        "Pentru orice cerere, scrieți la {email}. Dacă vi se pare că datele nu sunt prelucrate corect, vă puteți adresa "
        "Autorității Naționale de Supraveghere a Prelucrării Datelor cu Caracter Personal, la www.dataprotection.ro.",
    ]),
]

CSS = """
.legal{padding-block:clamp(2.5rem,6vw,4.5rem)}
.legal h1{font-size:clamp(2.5rem,5.5vw,4rem)}
.legal .updated{margin-top:.75rem;color:var(--ink-soft)}
.legal h2{margin-top:clamp(2rem,4vw,2.75rem);font-size:clamp(1.75rem,3vw,2.25rem);line-height:1.02}
.legal p{margin-top:.8rem;max-width:44rem}
.legal .back{display:inline-block;margin-top:2.5rem;font-weight:700}
"""


def render(fmt, esc, css, preload, ga_head, header, footer, banner, script, base, brand):
    """Pagina completă. fmt pune datele din site.json în text, deja escapat pentru HTML."""
    body = []
    for title, paragraphs in SECTIONS:
        body.append(f"<h2>{esc(title)}</h2>")
        for p in paragraphs:
            html = fmt(p).replace("www.dataprotection.ro",
                                  '<a href="https://www.dataprotection.ro/" rel="noopener">www.dataprotection.ro</a>')
            body.append(f"<p>{html}</p>")
    sections = "\n".join(body)
    return f'''<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{ga_head}
<title>Politica de confidențialitate | {esc(brand)}</title>
<meta name="description" content="Cum prelucrează {esc(brand)} datele vizitatorilor și ale celor care iau legătura prin telefon, WhatsApp sau e-mail.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{base}{PATH}">
{preload}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>{css}{CSS}</style>
</head>
<body>
{header}
<main id="continut" class="wrap legal">
<h1>Politica de confidențialitate</h1>
<p class="updated">Ultima actualizare: {UPDATED}.</p>
{sections}
<a class="back" href="/">Înapoi la prima pagină</a>
</main>
<div class="band">
{footer}
</div>
{banner}
{script}
</body>
</html>
'''
