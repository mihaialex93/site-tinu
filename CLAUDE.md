# Site soluții chimice profesionale

Context de lucru pentru Claude Code. Proiectul a fost construit într-o sesiune Claude pe 8 octombrie 2026 și continuă aici.
`CITESTE-MA.md` este ghidul pentru om (date de completat, publicare). Acest fișier este pentru tine.

## Pe scurt

- **Ce este:** o singură pagină de prezentare, statică, pentru un consultant tehnic care revinde produse chimice profesionale de curățare.
- **Ce nu este:** magazin online. Pe pagină nu apar produse, prețuri sau denumiri comerciale.
- **Public:** exclusiv firme cu facilități: industrie alimentară, HoReCa, depozite, ateliere, service-uri auto, clădiri de birouri. Nu persoane fizice.
- **Scop:** să fie găsit în Google pe zona lui și să primească apeluri sau cereri prin formular.
- **Stare:** versiune de lucru. Datele reale lipsesc, apar pe pagină marcate cu chenar punctat, iar indexarea este blocată automat.

## Reguli fixe

1. **Furnizorul produselor nu apare nicăieri pe site**: nici nume, nici fișe tehnice, nici denumiri de produse. Proprietarul este revânzător și prezintă doar propria activitate.
2. **Limba română corectă**, verificată la fiecare modificare: diacritice cu virgulă (ș, ț), niciodată cu sedilă (ş, ţ). Fără linie de pauză (—): se folosesc virgule, puncte sau două puncte. Titlurile au majusculă doar la început.
3. **Nimic inventat**: fără cifre, cazuri, testimoniale sau clienți fictivi și fără lorem ipsum. Ce lipsește rămâne marcat `[așa]`.
4. **Informațiile tehnice rămân orientative.** Nota de sub „Aplicații pe echipamente” rămâne, fiindcă acoperă răspunderea pentru sfaturile publicate.
5. **`site/` este generat.** Nu se editează de mână. Se modifică sursa, se regenerează, apoi se copiază rezultatul.
6. **Fără `git push --force`** și fără rescrierea istoricului.

## Structura

```
site/                  fișierele care se urcă pe domeniu (generate)
  index.html           pagina, cu CSS și JS incluse
  fonts/               Sofia Sans, tăiată la caracterele românești, cu nume care includ hash-ul
  _headers             antete pentru Cloudflare (securitate, cache fonturi, noindex pe pages.dev)
  robots.txt, sitemap.xml, 404.html, favicon.svg, apple-touch-icon.png, og.png
sursa/
  site.json            datele reale; null înseamnă câmp marcat pe pagină
  content.py           toate textele și comutatoarele de secțiuni
  build.py             generatorul: date + texte + stiluri -> HTML
  images.py            generează og.png și apple-touch-icon.png (Playwright)
  src/styles.css       stilurile, cu tokenuri în :root
  src/script.js        selectorul de aplicații, precompletarea formularului, trimiterea formularului
  src/fonts/           fonturile sursă tăiate (licență SIL OFL)
  tools/fonts.py       retaie fonturile din fișierele TTF complete (nu sunt în depozit)
  tools/functest.py    test funcțional în browser
porneste-site.bat      server local la http://localhost:8000
CITESTE-MA.md          ghidul pentru om
```

## Cum se lucrează (Windows)

```
cd sursa
py build.py                 # regenerează pagina
py build.py --imagini       # și imaginile; cere: py -m pip install playwright, apoi py -m playwright install chromium
cd ..
robocopy sursa\dist site /MIR
```

- `build.py` scrie în `sursa/dist/` și `sursa/preview/`, nu direct în `site/`. Pasul `robocopy /MIR` este obligatoriu și șterge fonturile vechi când li se schimbă hash-ul.
- `/MIR` șterge din `site/` tot ce nu există în `sursa/dist/`. Fotografia reală trebuie deci copiată de `build.py` (de exemplu din `sursa/src/`), nu pusă direct în `site/`, cum spune încă `CITESTE-MA.md`.
- `sursa/preview/index.html` este varianta cu fonturile incluse în fișier, folosită pentru previzualizarea publicată ca artefact. Nu se urcă pe domeniu.
- La final, `build.py` afișează modul (LUCRU sau FINAL), lungimea titlului și a descrierii și câmpurile lipsă.
- Verificare: pornește `porneste-site.bat`, apoi `py sursa\tools\functest.py http://localhost:8000/`.
- Nu am lăsat scripturi pentru validarea HTML sau pentru Lighthouse. Le-am rulat cu `npx html-validate` (fără erori) și `npx lighthouse`.

## Modul de lucru și modul final

- Cât timp lipsește orice câmp din `site.json`, inclusiv `cazuri`, `foto` și `politica_url`, pagina are `noindex`, `robots.txt` blochează tot și apare bara „Versiune de lucru”.
- Când toate câmpurile sunt completate, același build trece automat în modul final: indexabil, `robots.txt` cu sitemap, fără marcaje.
- `cazuri`: `null` înseamnă carduri marcate, `[]` scoate secțiunea, iar o listă înseamnă cazuri reale. Formatul este în `CITESTE-MA.md`.
- Comutatoare în `content.py`:
  - `SHOW_PROBLEMS = False`: secțiunea detaliată „Probleme de curățare pe care le rezolv” a fost scoasă la cererea proprietarului. Textele au rămas în `PROBLEMS`.
  - `APPS_SHOW_HOW = False`: coloana „Cum se curăță” din aplicații a fost scoasă la cererea proprietarului. Textele au rămas în câmpul `how`.

## Ce conține pagina acum, în ordine

1. Bara „Versiune de lucru” (doar în modul de lucru).
2. Antetul: brand, meniu (Aplicații, Facilități, Cum lucrez, Întrebări, Contact) și telefon.
3. Hero: titlul H1, textul de deschidere, butoanele „Sunați” și „Descrieți problema”, rândurile Clienți, Zonă și Răspuns.
   - „Ce aveți de curățat?”: 7 etichete cu interval de pH. Duc la formular și precompletează descrierea.
   - Scala de pH 0–14 pe toată lățimea; la trecerea mouse-ului peste o etichetă se aprinde intervalul ei.
   - Propoziția „Problema dumneavoastră nu este în listă?”, păstrată explicit de proprietar.
4. **Aplicații pe echipamente:** selector interactiv, cu lista în stânga și fișa în dreapta de la 62rem în sus, acordeon pe mobil. Este construit cu `<details name="aplicatie">` și funcționează și fără JavaScript.
   - 8 echipamente, fiecare cu mărimea de control scrisă mare: Instalații CIP (1,5 m/s), Schimbătoare de căldură și pasteurizatoare (Δp), Rezervoare și tancuri (pH), Conducte și furtunuri (UFC), Mașini de spălat lăzi și navete (°C), Utilaje și linii de procesare (ATP), Piese și componente metalice (H₂O), Echipamente electrice (MΩ).
   - Fiecare fișă are „Ce se depune”, cu depunerile marcate în culorile lor de pH, „Cum se verifică” și un buton care precompletează formularul.
5. Facilități: 6 tipuri.
6. Cum lucrez: 4 pași și cercul lui Sinner (chimie, temperatură, timp de contact, acțiune mecanică).
7. Cazuri din teren: 3 carduri marcate, fără date.
8. Despre: fotografie marcată și text cu câmpuri lipsă.
9. Întrebări frecvente: 10.
10. Contact: telefon mare, WhatsApp, e-mail, program, zonă, lista „Ce îmi spuneți la primul telefon” (6 puncte) și formularul (nume și firmă, telefon, localitate, tipul facilității, descriere), plus subsolul cu datele firmei.
11. Bara fixă pe mobil, cu „Sunați” și „Descrieți problema”.

## Direcția de design

- Elementul central este scala de pH, culorile cartelei de indicator de la 0 la 14. Ordonează vizual conținutul de la acid la alcalin. Restul paginii rămâne sobru.
- Paleta: gri rece de inox (#EDF0F1), bleumarin de bidon industrial (#12324A), alb de etichetă, roșu de pictogramă de pericol pentru avertizări. Magenta (#B8177A) este rezervată marcajelor de lucru.
- Tipografie: Sofia Sans Extra Condensed pentru titluri și Sofia Sans pentru text, găzduite local. Fonturile de rezervă au metricile ajustate, deci deplasarea de layout este 0.
- Proprietarul a cerut pagina „catchy” și secțiunile dinamice, nu statice.

## Decizii tehnice

- HTML static, fără CMS și fără framework. Singurul JavaScript gestionează selectorul și formularul.
- Găzduire planificată: Cloudflare (Workers cu fișiere statice sau Pages), care servește gratuit fișierele statice, cu domeniu propriu și SSL.
- Formular: Web3Forms (250 de trimiteri pe lună pe planul gratuit), trimis prin `fetch`, cu varianta fără JavaScript prin `action`. Capcana anti-spam `botcheck` este marcată ca depășită de Web3Forms, deci captcha rămâne de activat din contul lor.
- Date structurate: ProfessionalService, WebSite, WebPage și FAQPage. Google a scos rezultatele îmbogățite FAQ din 7 mai 2026, dar marcajul rămâne valid. Pentru LocalBusiness, Google cere obligatoriu adresa, deci sediul intră în cod.
- Analiză de trafic: Cloudflare Web Analytics, fără cookie-uri, activată prin `cloudflare_analytics_token`.
- Măsurători Lighthouse pe mobil, server local, 8 octombrie 2026: performanță, accesibilitate și bune practici 100. SEO 100 pe o generare de test în modul final (66 în modul de lucru, intenționat). LCP 1,5 s, CLS 0, circa 106 KB transferați.

## Ce lipsește

1. Datele reale din `site.json`: brand, persoană, zonă și localități, contact, program, timp de răspuns, costul evaluării, experiență, industrii, domeniu, datele firmei și sediul, cheia Web3Forms.
2. Cazuri reale cu cifre măsurate (sau `[]`) și o fotografie reală, verticală 4:5, minimum 880 x 1100 px.
3. Pagina cu politica de confidențialitate și adresa ei în `politica_url`.
4. Confirmări de conținut de la proprietar, fiindcă textele sunt scrise pe presupuneri:
   - simbolurile de măsură din aplicații și dacă echipamentele electrice rămân;
   - ordinea echipamentelor (primul este singurul vizibil fără clic);
   - cele 6 facilități și cei 4 pași din „Cum lucrez” (sunt promisiuni publice);
   - răspunsurile din întrebările frecvente și intervalele de pH din etichete.
5. Publicarea: domeniu .ro, Cloudflare, test real al formularului, Google Search Console cu sitemap, profil Google Business.
6. Opțional: planul cu pagini separate pe probleme, aplicații și industrii. Textele scoase din pagină sunt deja în `content.py`.

## Atenție

- **Remote-ul real este `origin` = `https://github.com/mihaialex93/site-tinu.git`, ramura `main`**, sincronizată cu commitul `1881ea1`. Inițial se plănuise depozitul `mihaialex93/tinu`.
- `urca-pe-github.bat` a fost șters din depozit pe 20 octombrie 2026: reseta `origin` la vechea adresă `mihaialex93/tinu.git` și făcea push fără verificare. Nu se recreează.
- Push-ul de pe laptopul proprietarului a eșuat cu HTTP 403 cât timp VPN-ul era activ. La un nou 403, nu se umblă la setările de proxy din Git: se raportează.
- `PLAN-PUSH-GITHUB.md` este ignorat local prin `.git/info/exclude`, iar `urcare-github.log` este în `.gitignore`. Ambele pot fi șterse.
- Mesajul „doar firme” mai apare în hero („Clienți: Exclusiv firme”) și în întrebarea „Lucrați și cu persoane fizice?”. Proprietarul a cerut scoasă doar propoziția „Nu vând persoanelor fizice.” din secțiunea Facilități.
- Imaginile din `site/` au primit metadate de proveniență C2PA la transferul pe acest calculator. Sunt valide; la următorul `py build.py --imagini` se regenerează fără ele.
- Pagina deschisă direct de pe disc (`file://`) se vede cu fonturi de rezervă. Se verifică doar prin `porneste-site.bat`.
