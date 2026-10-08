(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('details.app'));
  if (!items.length || !window.matchMedia) return;
  var wide = window.matchMedia('(min-width: 62rem)');
  items.forEach(function (item) {
    item.addEventListener('toggle', function () {
      if (item.open) items.forEach(function (other) { if (other !== item) other.open = false; });
    });
    item.querySelector('summary').addEventListener('click', function (event) {
      if (item.open && wide.matches) event.preventDefault();
    });
  });
})();

(function () {
  var area = document.getElementById('f-problema');
  if (!area) return;
  Array.prototype.forEach.call(document.querySelectorAll('[data-problema]'), function (chip) {
    chip.addEventListener('click', function () {
      if (!area.value) area.value = chip.getAttribute('data-problema') + ': ';
    });
  });
})();

(function () {
  var form = document.getElementById('solicitare');
  if (!form || !window.fetch) return;
  var state = document.getElementById('solicitare-stare');
  var button = form.querySelector('button[type="submit"]');
  var tel = form.getAttribute('data-tel') || '';

  function show(text, kind) {
    state.textContent = text;
    state.className = 'form-state' + (kind ? ' ' + kind : '');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var data = {};
    new FormData(form).forEach(function (value, key) { data[key] = value; });
    delete data.redirect;

    if (!data.access_key || data.access_key.charAt(0) === '[') {
      show('Formularul nu este încă activ. Sunați la ' + tel + '.', 'err');
      return;
    }

    button.disabled = true;
    show('Se trimite solicitarea…', '');

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (response) {
        return response.json().then(function (json) { return response.ok && json.success; });
      })
      .then(function (sent) {
        if (sent) {
          form.reset();
          show('Solicitarea a fost trimisă. Vă sun în cel mai scurt timp.', 'ok');
        } else {
          show('Solicitarea nu a fost trimisă. Încercați din nou sau sunați la ' + tel + '.', 'err');
        }
      })
      .catch(function () {
        show('Serviciul de trimitere nu răspunde. Încercați din nou sau sunați la ' + tel + '.', 'err');
      })
      .then(function () { button.disabled = false; });
  });
})();
