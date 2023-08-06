
try {
  new Function("import('/hacsfiles/frontend/e.f8ba172a.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/e.f8ba172a.js';
  document.body.appendChild(el);
}
  