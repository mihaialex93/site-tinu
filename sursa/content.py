"""Conținutul paginii. Textele folosesc {cheie} pentru datele din site.json."""

TITLE = "Soluții chimice pentru industrie și instituții, {zona}"
DESCRIPTION = (
    "Soluții chimice pentru industrie, instituții și industria alimentară: mentenanță, curățare, "
    "dezinfecție. {judete_lista}. Doar firme."
)
PREVIEW_TITLE = "Site soluții chimice profesionale"

H1 = ("Soluții chimice pentru mentenanță industrială, întreținere instituțională, "
      "curățare și dezinfecție în\u00a0industria\u00a0alimentară")
LEAD = (
    "Consultanță tehnică (identific cea mai eficientă soluție pentru proces), "
    "optimizare procese de curățenie, performanță în timp."
)

# Secțiunea detaliată „Probleme de curățare pe care le rezolv” este scoasă din pagină.
# Textele rămân aici: True o readuce, iar etichetele din hero și scala de pH folosesc în continuare lista.
SHOW_PROBLEMS = False

# (id, titlu, pH de la, pH până la, tip de soluție, ce este, unde apare, cum se tratează, greșeala frecventă)
PROBLEMS = [
    dict(
        id="rugina", short="Rugină pe inox", title="Rugină și pete de oxizi pe inox",
        lo=1, hi=2, kind="Soluție acidă",
        what="Pete ruginii pe oțel inoxidabil, apărute de obicei după contaminarea cu particule de fier (scule, șpan, bureți metalici) sau după contactul prelungit cu cloruri. Inoxul rezistă datorită unui strat pasiv de oxid de crom. Când stratul este deteriorat, apare coroziunea.",
        where="Mese de lucru, utilaje și rezervoare din inox, suduri, balustrade, zone în care se folosesc frecvent produse clorinate.",
        how="Cu o soluție acidă care dizolvă oxizii de fier și ajută la refacerea stratului pasiv (decapare și pasivare), urmată de o clătire abundentă.",
        mistake="Acid clorhidric sau bureți de sârmă din oțel obișnuit. Clorurile atacă inoxul punctiform, iar sârma lasă particule de fier care ruginesc din nou.",
    ),
    dict(
        id="calcar", short="Calcar și piatră", title="Calcar și depuneri minerale",
        lo=1, hi=3, kind="Soluție acidă (detartrant)",
        what="Depuneri dure, albicioase sau gălbui, formate din sărurile de calciu și de magneziu din apa dură. În industria alimentară apar și depuneri mixte, cum sunt piatra de lapte și piatra de bere, în care mineralele sunt legate de proteine.",
        where="Schimbătoare de căldură, boilere, mașini de spălat vase și navete, duze, instalații de spălare CIP, grupuri sanitare.",
        how="Cu un detartrant acid ales după materialul instalației, cu inhibitori de coroziune acolo unde este nevoie. La depunerile mixte se alternează spălarea alcalină cu cea acidă.",
        mistake="Un acid mai tare, pe ideea că va curăța mai bine. Fără inhibitori, acidul atacă metalul, garniturile și suprafețele cromate. În plus, calcarul revine repede dacă nu se corectează cauza: duritatea apei, temperatura sau dozarea.",
    ),
    dict(
        id="suprafete-sensibile", short="Suprafețe sensibile", title="Aluminiu și alte suprafețe sensibile",
        lo=6, hi=8, kind="Soluție neutră",
        what="Aluminiu, suprafețe vopsite, pardoseli tratate cu ceară sau cu polimeri, piatră naturală, linoleum. Sunt materiale care se pătează sau se degradează la contactul cu soluții puternic acide ori puternic alcaline.",
        where="Showroomuri, birouri, holuri și recepții, utilaje cu componente din aluminiu, caroserii, zone placate cu marmură sau cu travertin.",
        how="Cu un detergent neutru, dozat controlat. Chimia blândă se compensează prin acțiune mecanică și timp de contact.",
        mistake="Degresant puternic alcalin pe aluminiu sau produs acid pe marmură. Aluminiul se înnegrește și se corodează, iar marmura își pierde luciul definitiv.",
    ),
    dict(
        id="pardoseli", short="Pardoseli și urme de anvelope", title="Pardoseli industriale și urme de anvelope",
        lo=9, hi=11, kind="Soluție moderat alcalină",
        what="Praf aderent, urme de cauciuc lăsate de stivuitoare, ulei scurs și murdărie tasată pe beton, rășină epoxidică sau gresie.",
        where="Depozite, hale de producție, rampe de încărcare, parcări, ateliere.",
        how="Cu un detergent alcalin cu spumare redusă, potrivit pentru mașina de spălat pardoseli, lăsat să acționeze înainte de aspirare. Urmele vechi de cauciuc cer produse cu solvenți.",
        mistake="Un produs cu multă spumă în mașina de spălat pardoseli. Spuma ajunge la motorul de aspirare, iar pardoseala rămâne lipicioasă și se murdărește mai repede.",
    ),
    dict(
        id="grasimi", short="Grăsimi și uleiuri", title="Grăsimi și uleiuri",
        lo=11, hi=13, kind="Soluție alcalină (degresant)",
        what="Grăsimi vegetale și animale, uleiuri minerale, unsori și emulsii de prelucrare. Soluțiile alcaline transformă grăsimile vegetale și animale în săpun solubil (saponificare). Uleiurile minerale nu se saponifică, de aceea trebuie emulsionate.",
        where="Bucătării profesionale, linii de procesare, abatoare, ateliere mecanice, piese și utilaje.",
        how="Cu un degresant alcalin ales după tipul grăsimii și după suprafață, aplicat la cald atunci când se poate. La uleiurile minerale contează agenții tensioactivi și solvenții mai mult decât pH-ul.",
        mistake="Mai mult produs în loc de temperatură și de timp de contact. Supradozarea lasă reziduuri alunecoase, costă mai mult și nu salvează o soluție rece, aplicată în grabă.",
    ),
    dict(
        id="proteine-biofilm", short="Proteine și biofilm", title="Proteine și biofilm",
        lo=11, hi=13, kind="Soluție alcalină clorinată sau enzimatică, apoi dezinfecție",
        what="Reziduuri de lapte, sânge, ou sau carne și stratul lipicios în care bacteriile se fixează pe suprafețele umede. Biofilmul este protejat de o matrice care împiedică dezinfectantul să ajungă la bacterii.",
        where="Conducte și rezervoare, benzi transportoare, garnituri, sifoane de pardoseală, colțuri greu accesibile.",
        how="Clătire cu apă călduță, spălare cu detergent alcalin clorinat sau enzimatic și acțiune mecanică, clătire, apoi dezinfecție. Dezinfectanții sunt produse biocide: se folosesc doar cele avizate și doar conform etichetei.",
        mistake="Prima clătire cu apă fierbinte și dezinfectant aplicat peste murdărie. Apa fierbinte coagulează proteinele și le fixează pe suprafață, iar dezinfectantul nu trece prin stratul de murdărie.",
    ),
    dict(
        id="carbonizate", short="Depuneri carbonizate", title="Depuneri carbonizate",
        lo=13, hi=14, kind="Soluție puternic alcalină",
        what="Grăsimi arse și polimerizate, întărite de încălziri repetate, pe care degresanții obișnuiți nu le mai dizolvă.",
        where="Cuptoare, grătare, friteuze, hote și filtre, celule de afumare, tăvi și forme de copt.",
        how="Cu un produs puternic alcalin, sub formă de gel sau de spumă aderentă pentru suprafețele verticale, aplicat pe suprafața caldă și lăsat să acționeze. Echipamentul de protecție este obligatoriu.",
        mistake="Același produs și pe tăvile sau formele din aluminiu. Soluțiile caustice atacă aluminiul. Pentru el există produse alcaline cu inhibitori.",
    ),
]

# Domeniile de aplicare, date de proprietar pe 20 octombrie 2026. Au înlocuit secțiunea „Facilități pentru care lucrez”.
DOMAINS_TITLE = "Domenii de aplicare"
DOMAINS = [
    "Industria auto și mecanică",
    "Industria alimentară",
    "Instituții publice și centre comerciale",
    "Curățări grele",
    "Ferme și abatoare de păsări și animale",
]

# Vechea listă de facilități, cu descrieri. Nu mai apare pe pagină.
FACILITIES = [
    ("Industrie alimentară și băuturi", "Lactate, carne, băuturi și panificație: linii de procesare, instalații de spălare CIP, rezervoare și spații de ambalare, unde igiena se verifică la fiecare control."),
    ("Bucătării profesionale și HoReCa", "Restaurante, hoteluri, cantine, firme de catering și laboratoare de cofetărie, de la hotă și cuptor până la mașina de spălat vase."),
    ("Depozite și logistică", "Pardoseli industriale, rampe de încărcare și zone cu trafic intens de stivuitoare."),
    ("Producție și ateliere mecanice", "Degresarea pieselor și a utilajelor, curățarea halelor, îndepărtarea uleiurilor și a emulsiilor."),
    ("Service-uri și flote auto", "Spălarea autovehiculelor și a pieselor, curățarea canalelor de vizitare și a pardoselilor de atelier."),
    ("Clădiri de birouri și spații comerciale", "Firme de curățenie și administratori de clădiri care au nevoie de produse profesionale, dozate corect."),
]

STEPS = [
    ("Îmi descrieți problema", "Prin telefon sau prin formular. Pentru început ajung câteva detalii despre depunere, suprafață și instalație."),
    ("Vin la fața locului", "Văd depunerea, materialul, apa și procedura actuală de curățare. Unele probleme se rezolvă din dozare sau din temperatură, fără schimbarea produsului."),
    ("Testăm soluția", "Facem o probă pe o zonă mică sau pe un ciclu de spălare și notăm parametrii: concentrație, temperatură, timp de contact."),
    ("Livrez și urmăresc rezultatul", "Produsul vine cu fișa tehnică și cu fișa cu date de securitate, în limba română. Revin să verific rezultatul și ajustăm dozarea, dacă este nevoie."),
]

SINNER_TITLE = "Patru factori decid rezultatul"
SINNER_TEXT = [
    "Orice curățare depinde de patru factori: chimia, temperatura, timpul de contact și acțiunea mecanică. Principiul este cunoscut drept cercul lui Sinner.",
    "Dacă unul dintre factori scade, altul trebuie să crească. De aceea, uneori ajung cinci minute sau zece grade în plus, fără un produs mai tare.",
]

# Cazurile rămân marcate până vin datele reale. Fără cifre inventate.
CASE_FIELDS = [
    ("Facilitate", "[tipul facilității, localitatea]"),
    ("Problema", "[ce nu mergea și de cât timp]"),
    ("Ce am schimbat", "[produs, concentrație, temperatură, timp de contact]"),
    ("Rezultat", "[o cifră măsurabilă: timp, consum, cost sau frecvență]"),
]
CASE_COUNT = 3

ABOUT = [
    "{persoana}, consultant tehnic pentru soluții chimice profesionale. Lucrez în teren de {ani_text}, în {industrii}.",
    "Studii postuniversitare, inginer. Tehnician în protecția și calitatea mediului. Antreprenor. Reprezentant tehnic. "
    "Experiență de 10 ani în servicii speciale și curățare cu gheață carbonică.",
    "Nu am magazin online și nu trimit oferte fără să văd problema. Vin, evaluez și răspund pentru recomandarea făcută.",
    "Acopăr {zona}, cu deplasare la sediul dumneavoastră.",
]

FAQ = [
    ("Lucrați și cu persoane fizice?",
     "Nu. Lucrez exclusiv cu firme și instituții, în domeniile de aplicare de mai sus: industria auto și mecanică, "
     "industria alimentară, instituții publice și centre comerciale, curățări grele, ferme și abatoare."),
    ("Ce zonă acoperiți?",
     "Acopăr {zona}. Pentru proiecte mai mari discutăm și în afara zonei."),
    ("Pot testa soluția înainte de comandă?",
     "Da. Recomandarea se verifică printr-o probă la fața locului, pe o zonă mică sau pe un ciclu de spălare, înainte de orice comandă."),
    ("Primesc documentația produselor?",
     "Da. Fiecare produs se livrează cu fișa tehnică și cu fișa cu date de securitate, în limba română."),
    ("Cum aleg detergentul industrial potrivit?",
     "După patru lucruri: tipul depunerii, materialul suprafeței, metoda de curățare și apa folosită. Abia apoi contează produsul. Un detergent bun, folosit la concentrația sau la temperatura greșită, dă același rezultat ca unul slab."),
    ("De ce nu afișați produsele și prețurile pe site?",
     "Pentru că alegerea depinde de depunere, de material și de instalație. Același produs poate rezolva o problemă într-un loc și poate strica o suprafață în altul. Întâi evaluez, apoi recomand."),
    ("Cum îmi dau seama dacă am nevoie de o soluție acidă sau de una alcalină?",
     "Ca regulă generală, depunerile minerale (calcar, rugină) cer soluții acide, iar murdăria organică (grăsimi, proteine) cere soluții alcaline. În practică apar des depuneri mixte, de aceea este nevoie de evaluare."),
    ("Produsele sunt sigure pentru inox și aluminiu?",
     "Depinde de produs. Inoxul nu tolerează contactul prelungit cu clorurile, iar aluminiul este atacat atât de soluțiile puternic alcaline, cât și de cele puternic acide. Verific compatibilitatea înainte de orice recomandare."),
    ("În cât timp primesc un răspuns?",
     "Răspund la solicitări în {raspuns}. Pentru urgențe, sunați direct."),
]

FACILITY_OPTIONS = DOMAINS + ["Alt domeniu"]

KNOWS_ABOUT = [
    "curățarea schimbătoarelor de căldură", "pasivarea inoxului", "degresarea pieselor metalice",
    "detergenți profesionali", "curățare industrială", "detartrare", "degresare industrială",
    "igienizare în industria alimentară", "instalații de spălare CIP", "întreținerea pardoselilor industriale",
    "curățarea bazinelor de apă potabilă", "curățare cu gheață carbonică",
]


# Aplicații pe echipamente. [[id|text]] face legătura către o problemă din listă.
APPS_TITLE = "Aplicații pe echipamente"
# Coloana „Cum se curăță” este scoasă din pagină. Textele rămân în lista de mai jos: True o readuce.
APPS_SHOW_HOW = False
APPS_INTRO = ("Aceeași depunere se tratează diferit de la un echipament la altul. "
              "Alegeți echipamentul și vedeți ce se depune și cum se verifică rezultatul.")
APPS_INTRO_WITH_HOW = ("Aceeași depunere se tratează diferit de la un echipament la altul. "
                       "Pentru fiecare aplicație contează trei lucruri: ce se depune, cum se curăță și cum se verifică rezultatul.")
APPS = [
    dict(id="instalatii-cip", unit='m/s', token='1,5 m/s', token_note='Viteza minimă de curgere în conducte',
         title="Instalații CIP",
         soil="[[grasimi|Grăsimi]], [[proteine-biofilm|proteine]] și [[calcar|piatră de lapte sau de bere]], pe toată lungimea circuitului.",
         how="Prin circulare: clătire, spălare alcalină, clătire, spălare acidă, clătire și, la nevoie, dezinfecție. Inoxul și garniturile decid ce produse sunt admise.",
         check="Concentrația, prin conductivitate sau prin titrare, temperatura pe retur și viteza de curgere, de regulă minimum 1,5 m/s în conducte."),
    dict(id="schimbatoare-de-caldura", unit='Δp', token='Δp', token_note='Căderea de presiune pe schimbător',
         title="Schimbătoare de căldură și pasteurizatoare",
         soil="Depuneri arse de [[proteine-biofilm|proteine]] și de [[calcar|minerale]], care izolează termic plăcile sau țevile.",
         how="Prin circulare, cu spălare alcalină urmată de spălare acidă. Garniturile limitează temperatura și tipul de produs, iar plăcile subțiri nu iartă un acid ales greșit.",
         check="Căderea de presiune și temperatura de ieșire revin la valorile unui schimbător curat."),
    dict(id="rezervoare", unit='pH', token='pH', token_note='pH-ul apei de clătire, egal cu cel al apei de rețea',
         title="Rezervoare și tancuri",
         soil="Peliculă de [[grasimi|grăsimi]] și de [[proteine-biofilm|proteine]], plus inelul de depunere de la nivelul lichidului.",
         how="Cu soluție recirculată prin capete de spălare, fixe sau rotative. La rezervoarele fără instalație proprie, prin spumare și clătire.",
         check="Inspecție vizuală cu lanterna, teste rapide ATP și pH-ul apei de clătire, care trebuie să revină la cel al apei de rețea."),
    dict(id="conducte", unit='UFC', token='UFC', token_note='Probe microbiologice din apa de clătire',
         title="Conducte și furtunuri",
         soil="[[proteine-biofilm|Biofilm]] și depuneri în coturi, la îmbinări și în zonele moarte, unde soluția nu circulă.",
         how="Prin circulare la viteză suficientă. Zonele moarte se elimină din traseu sau se demontează și se curăță separat.",
         check="Probe microbiologice din apa de clătire și controlul vizual al garniturilor și al îmbinărilor demontabile."),
    dict(id="masini-de-spalat-navete", unit='°C', token='°C', token_note='Temperatura din baia de spălare',
         title="Mașini de spălat lăzi și navete",
         soil="[[calcar|Calcar]] pe duze și pe rezistențe, [[grasimi|grăsimi]] și resturi de etichete în baie.",
         how="Cu detergent alcalin cu spumare redusă, dozat automat, și cu detartrarea periodică a mașinii.",
         check="Duze libere, concentrația din baie și temperatura de spălare, verificate prin măsurare."),
    dict(id="utilaje-de-procesare", unit='ATP', token='ATP', token_note='Teste rapide în punctele greu accesibile',
         title="Utilaje și linii de procesare",
         soil="[[grasimi|Grăsimi]], [[proteine-biofilm|proteine]] și amidon pe suprafețe deschise: benzi, mașini de tocat, mese, malaxoare.",
         how="Prin spumare cu detergent alcalin, cu timp de contact fără ca spuma să se usuce, clătire la presiune joasă și dezinfecție. Presiunea mare împrăștie murdăria sub formă de aerosoli.",
         check="Control vizual pe suprafața uscată și teste rapide ATP în punctele greu accesibile."),
    dict(id="piese-metalice", unit='H₂O', token='H₂O', token_note='Pelicula de apă se întinde uniform pe suprafață',
         title="Piese și componente metalice",
         soil="[[grasimi|Uleiuri minerale]], unsori, emulsii de prelucrare și șpan.",
         how="În băi de degresare, în mașini de spălat piese sau prin pulverizare. După spălarea cu soluții pe bază de apă, oțelul are nevoie de protecție temporară împotriva coroziunii, iar [[suprafete-sensibile|aluminiul]] cere produse cu inhibitori.",
         check="Apa se întinde uniform pe suprafața degresată, fără să se strângă în picături, iar piesa se usucă fără pete."),
    dict(id="echipamente-electrice", unit='MΩ', token='MΩ', token_note='Rezistența de izolație, înainte de repunerea sub tensiune',
         title="Echipamente electrice",
         soil="Praf, ulei și depuneri de carbon pe motoare, pe contacte și în tablouri.",
         how="Cu solvenți dielectrici, fără apă, cu evaporare controlată, numai pe echipamente scoase de sub tensiune.",
         check="Rezistența de izolație, măsurată înainte de repunerea sub tensiune."),
    # Date de la proprietar, 20 octombrie 2026. Mărimea de control: pH, cu buletin de analiză a apei la predare.
    dict(id="bazine-apa-potabila", unit='pH', token='pH', token_note='Buletin de analiză a apei, înainte de predare',
         title="Bazine de apă potabilă",
         soil="[[rugina|Oxizi]], [[calcar|depuneri minerale]] și [[proteine-biofilm|biofilm]], pe bazine cu membrană, din inox, din fibră sau din beton.",
         how="Soluții tehnice și pași de curățare diferiți, în funcție de tipul materialului, de depunere și de timpul de acțiune.",
         check="Igienizare cu dezinfectant avizat pentru apă potabilă, înainte de predare. Serviciu disponibil în județul Timiș."),
]

APPS_NOTE = ("Informațiile de pe această pagină sunt orientative. Produsul, concentrația, temperatura și timpul de contact "
             "se stabilesc după evaluare, conform fișei tehnice și fișei cu date de securitate.")

NEED_TITLE = "Ce îmi spuneți la primul telefon"
NEED_INTRO = "Cu aceste șase informații ajung pregătit la evaluare."
NEED = [
    "Materialul echipamentului sau al suprafeței.",
    "Tipul depunerii.",
    "Temperatura de lucru.",
    "Metoda de curățare folosită acum.",
    "Produsul și concentrația folosite în prezent.",
    "Timpul disponibil pentru curățare.",
]


# Cele 30 de aplicații uzuale, date de proprietar pe 20 octombrie 2026. Doar titluri, numerotate continuu.
USUAL_TITLE = "30 de aplicații uzuale"
USUAL_INTRO = "Situațiile pe care le întâlnesc cel mai des. Dacă a dumneavoastră nu este aici, sunați."
USUAL = [
    ("Curățare și depuneri", [
        "Curățarea instalațiilor CIP",
        "Depuneri minerale în instalații CIP",
        "Piatra de lapte",
        "Depuneri de calcar",
        "Depuneri proteice",
        "Depuneri de grăsimi",
        "Biofilm în instalații",
        "Depuneri carbonizate",
        "Curățarea schimbătoarelor de căldură",
        "Curățarea conductelor industriale",
    ]),
    ("Metale și suprafețe", [
        "Îndepărtarea ruginii",
        "Pete de rugină pe inox",
        "Curățarea inoxului",
        "Oxizi metalici",
        "Degresarea suprafețelor metalice",
        "Pasivarea inoxului",
        "Protecția împotriva coroziunii",
        "Curățarea aluminiului",
    ]),
    ("Industria alimentară", [
        "Curățarea instalațiilor din industria laptelui",
        "Curățarea instalațiilor de procesare carne",
        "Curățarea fabricilor de băuturi",
        "Curățarea utilajelor alimentare",
        "Curățarea mașinilor de spălat lăzi",
        "Curățarea rezervoarelor alimentare",
        "Curățarea conductelor pentru produse alimentare",
    ]),
    ("Mentenanță industrială", [
        "Curățarea utilajelor industriale",
        "Îndepărtarea uleiurilor și grăsimilor",
        "Curățarea componentelor tehnice",
        "Curățarea electrică și tehnică specială",
        "Alegerea detergentului industrial potrivit",
    ]),
]
