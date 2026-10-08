# Site soluții chimice profesionale: pachet de publicare

## Ce conține

- `site/` : exact fișierele care se urcă pe domeniu. Nimic altceva nu ajunge online.
- `sursa/` : sistemul din care se generează pagina. Datele stau în `site.json`, textele în `content.py`, designul în `src/styles.css`.

## Starea actuală

Versiune de lucru. Datele lipsă apar pe pagină marcate cu chenar punctat, iar pagina este blocată la indexare în două locuri: eticheta `robots` din pagină și fișierul `robots.txt`. Blocajul dispare automat la prima generare cu toate datele completate.

## Date de completat în `sursa/site.json`

| Cheie | Ce se completează | Format |
|---|---|---|
| `brand` | Numele sub care apare site-ul | text scurt |
| `persoana` | Prenume și nume | text |
| `zona` | Zona deservită, cum se citește după „din” | „județul X”, „zona X” |
| `localitati` | Localitățile principale | „A, B și C” |
| `telefon_afisat` | Telefonul, cum se vede pe pagină | „07xx xxx xxx” |
| `telefon_international` | Același număr, pentru apel direct | „+407xxxxxxxx” |
| `whatsapp` | Opțional, numărul de WhatsApp | „+407xxxxxxxx” |
| `email` | Adresa de contact | text |
| `program` | Programul, cum se vede pe pagină | „luni–vineri, 08:00–17:00” |
| `program_zile`, `program_deschidere`, `program_inchidere` | Programul pentru Google | `["Monday", ...]`, „08:00”, „17:00” |
| `raspuns` | Timpul de răspuns, cum se citește după „în” | „aceeași zi lucrătoare” |
| `cost_evaluare` | Răspunsul complet la întrebarea despre cost | o propoziție |
| `ani_experienta` | Anii de lucru în teren | număr |
| `industrii` | Industriile în care ai lucrat | „industria alimentară și HoReCa” |
| `linkedin` | Opțional, adresa profilului | adresă completă |
| `foto` | Numele fișierului cu fotografia, pus în `site/` | „foto.webp”, 880 x 1100 px |
| `cazuri` | Cazuri reale. Listă goală `[]` scoate secțiunea | vezi mai jos |
| `domeniu` | Domeniul, fără https | „exemplu.ro” |
| `firma_denumire`, `firma_cui`, `firma_reg_com` | Datele de identificare ale firmei | text |
| `sediu_strada`, `sediu_localitate`, `sediu_judet`, `sediu_cod_postal` | Sediul social | text |
| `politica_url` | Adresa politicii de confidențialitate | „confidentialitate.html” |
| `web3forms_cheie` | Cheia de la web3forms.com, pentru formular | cod |
| `cloudflare_analytics_token` | Opțional, analiză de trafic fără cookie-uri | cod |

Un caz arată așa:

```json
{"facilitate": "Tip de facilitate, localitate", "problema": "Ce nu mergea.", "schimbare": "Ce s-a schimbat.", "rezultat": "Cifra măsurată."}
```

## Texte scrise pe presupuneri, de confirmat

- Cele 7 probleme și intervalele de pH din etichetele de sub titlu: de aliniat cu portofoliul real. Secțiunea detaliată cu aceste probleme este scoasă din pagină. Textele ei rămân în `content.py` și revin cu `SHOW_PROBLEMS = True`.
- Cele 6 tipuri de facilități.
- Cele 8 aplicații pe echipamente, inclusiv echipamentele electrice: rămân doar cele pentru care ai produse.
- Pașii din „Cum lucrez”: vizită la fața locului, probă înainte de comandă, livrare cu fișă tehnică și fișă cu date de securitate, revenire după livrare. Sunt promisiuni publice, rămân doar cele respectate.
- Răspunsurile din „Întrebări frecvente”.

## Pornire pe calculatorul tău

Dublu clic pe `porneste-site.bat`. Pornește serverul inclus în Python, doar pentru acest calculator, și deschide `http://localhost:8000` în browser. Se oprește prin închiderea ferestrei negre. Are nevoie de Python instalat.

## Publicare

1. Domeniu `.ro`, scurt.
2. Cloudflare, secțiunea Workers & Pages: se încarcă folderul `site/`, apoi se leagă domeniul.
3. Cont pe web3forms.com pentru cheia formularului. Un test de trimitere înainte de lansare.
4. După lansare: Google Search Console (se trimite `sitemap.xml`), profil Google Business, verificare cu Rich Results Test.

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
- Dacă adaugi captcha la formular, cere-o din contul Web3Forms. Capcana anti-spam inclusă oprește doar roboții simpli.
