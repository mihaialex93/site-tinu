# Site soluții chimice profesionale: pachet de publicare

## Ce conține

- `site/` : exact fișierele care se urcă pe domeniu. Nimic altceva nu ajunge online.
- `sursa/` : sistemul din care se generează pagina. Datele stau în `site.json`, textele în `content.py`, designul în `src/styles.css`.

## Starea actuală

Online la `https://solutiivest.ro`, indexabil din 28 octombrie 2026. Dacă un câmp obligatoriu din `site.json` rămâne vreodată gol, pagina revine automat în versiunea de lucru: datele lipsă apar marcate cu chenar punctat, iar indexarea se blochează în două locuri, eticheta `robots` din pagină și fișierul `robots.txt`.

## Date de completat în `sursa/site.json`

| Cheie | Ce se completează | Format |
|---|---|---|
| `brand` | Numele sub care apare site-ul | text scurt |
| `persoana` | Prenume și nume | text |
| `zona` | Zona deservită, cum se citește după „din” | „județul X”, „zona X” |
| `judete` | Opțional, județele din zonă. Apar în descrierea pentru Google și în datele structurate | `["Timiș", "Arad"]` |
| `telefon_afisat` | Telefonul, cum se vede pe pagină | „07xx xxx xxx” |
| `telefon_international` | Același număr, pentru apel direct | „+407xxxxxxxx” |
| `whatsapp` | Opțional, numărul de WhatsApp | „+407xxxxxxxx” |
| `email` | Adresa de contact | text |
| `program_zile`, `program_deschidere`, `program_inchidere` | Programul pentru Google | `["Monday", ...]`, „08:00”, „17:00” |
| `raspuns` | Timpul de răspuns, cum se citește după „în” | „aceeași zi lucrătoare” |
| `ani_experienta` | Anii de lucru în teren | număr |
| `industrii` | Industriile în care ai lucrat | „industria alimentară și HoReCa” |
| `linkedin` | Opțional, adresa profilului | adresă completă |
| `foto` | Numele fișierului cu fotografia, pus în `sursa/src/img/` (de acolo ajunge în `site/` la regenerare) | „foto.jpg”, 880 x 1100 px |
| `cazuri` | Cazuri reale. Listă goală `[]` scoate secțiunea | vezi mai jos |
| `domeniu` | Domeniul, fără https | „exemplu.ro” |
| `firma_denumire`, `firma_cui`, `firma_reg_com` | Datele de identificare ale firmei | text |
| `sediu_strada`, `sediu_localitate`, `sediu_judet` | Sediul social | text |
| `politica_url` | Opțional, adresa politicii de confidențialitate; dacă e completată, apare link în subsol | „confidentialitate.html” |
| `cloudflare_analytics_token` | Opțional, analiză de trafic fără cookie-uri | cod |

Un caz arată așa:

```json
{"facilitate": "Tip de facilitate, localitate", "problema": "Ce nu mergea.", "schimbare": "Ce s-a schimbat.", "rezultat": "Cifra măsurată."}
```

## Confirmarea textelor

Pe 28 octombrie 2026 proprietarul a confirmat toate textele de pe pagină. Textele scoase de pe pagină și păstrate în `content.py` nu sunt acoperite de confirmare: secțiunea detaliată cu cele 7 probleme (revine cu `SHOW_PROBLEMS = True`) și coloana „Cum se curăță” din aplicații (revine cu `APPS_SHOW_HOW = True`). Se confirmă separat înainte să revină pe site.

## Pornire pe calculatorul tău

Dublu clic pe `porneste-site.bat`. Pornește serverul inclus în Python, doar pentru acest calculator, și deschide `http://localhost:8000` în browser. Se oprește prin închiderea ferestrei negre. Are nevoie de Python instalat.

## Publicare

1. Domeniu `.ro`, scurt. Făcut: `solutiivest.ro`.
2. Cloudflare, legat de depozitul GitHub: fiecare push pe `main` republică site-ul în câteva minute. Făcut.
3. După lansare: Google Search Console (se trimite `sitemap.xml`), profil Google Business, verificare cu Rich Results Test.

## Regenerare

```
cd sursa
python3 build.py --imagini
```

Are nevoie de Python 3. Pentru imagini (`og.png`, `apple-touch-icon.png`) are nevoie și de Playwright cu Chromium. Rezultatul apare în `sursa/dist/`.

## Note tehnice

- Deschisă direct de pe disc, pagina se vede cu fonturi de rezervă, fiindcă browserul blochează fonturile locale. Pe domeniu se încarcă normal.
- Fonturile din `src/fonts` sunt Sofia Sans, tăiate la caracterele românești. Licența (SIL OFL) este în același folder.
- `_headers` este citit de Cloudflare: antete de securitate, cache lung pentru fonturi și blocarea la indexare a adresei tehnice `pages.dev`.
