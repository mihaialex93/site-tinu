(function () {
  if (typeof gtag !== "function") return;
  var KEY = "analiza";
  var box = document.getElementById("consimtamant");

  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  // La refuz se șterg și cookie-urile puse după un acord anterior.
  function clearGa() {
    var host = location.hostname, parts = host.split(".");
    var domains = ["", host, "." + host];
    if (parts.length > 2) domains.push("." + parts.slice(-2).join("."));
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (name.indexOf("_ga") !== 0) return;
      domains.forEach(function (d) {
        document.cookie = name + "=; Max-Age=0; path=/" + (d ? "; domain=" + d : "");
      });
    });
  }

  function choose(v) {
    save(v);
    gtag("consent", "update", { analytics_storage: v === "da" ? "granted" : "denied" });
    if (v !== "da") clearGa();
    if (box) box.hidden = true;
  }

  if (box) {
    box.querySelector('[data-consent="da"]').addEventListener("click", function () { choose("da"); });
    box.querySelector('[data-consent="nu"]').addEventListener("click", function () { choose("nu"); });
    var saved = read();
    if (saved !== "da" && saved !== "nu") box.hidden = false;
  }
  document.querySelectorAll("[data-consent-open]").forEach(function (b) {
    b.addEventListener("click", function () { if (box) { box.hidden = false; box.focus(); } });
  });

  // Clicurile de contact: telefon, WhatsApp și e-mail (inclusiv adresa ascunsă de Cloudflare).
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var h = a.getAttribute("href") || "", ev = "";
    if (h.indexOf("tel:") === 0) ev = "contact_telefon";
    else if (h.indexOf("wa.me/") !== -1) ev = "contact_whatsapp";
    else if (h.indexOf("mailto:") === 0 || h.indexOf("email-protection") !== -1) ev = "contact_email";
    if (!ev) return;
    var zone = a.closest("[id], .dock, header");
    var name = zone ? (zone.id || (zone.classList.contains("dock") ? "bara-mobil" : "antet")) : "";
    gtag("event", ev, { sectiune: name });
  });
})();
