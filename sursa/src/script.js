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
