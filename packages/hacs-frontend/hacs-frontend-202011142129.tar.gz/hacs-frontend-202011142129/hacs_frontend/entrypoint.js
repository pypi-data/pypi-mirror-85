
try {
  new Function("import('/hacsfiles/frontend/e.b4de010b.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/e.b4de010b.js';
  document.body.appendChild(el);
}
  