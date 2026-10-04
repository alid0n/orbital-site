/* ============================================================================
   Light and dark.

   Loaded in <head> so the page is drawn in the right colours from the first
   frame. The site follows the visitor's system setting until they press the
   button in the header; after that their choice is kept on this device. The
   demo phones keep their own themes either way: they are showing Orbital,
   not the website.
   ========================================================================== */

(function () {
  'use strict';

  var KEY = 'orbital-site-theme';
  var root = document.documentElement;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function system() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function apply(mode) {
    root.setAttribute('data-theme', mode);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', mode === 'light' ? '#f6f7f9' : '#07090e');
  }

  apply(stored() || system());

  /* The theme picked on the front page (pick.js) colours the site for the rest
     of the visit: its accent everywhere, and its background in dark mode (or
     in light mode, for the light themes). Kept as colours rather than a name
     so this runs before anything else has loaded. */
  var VIBE = 'orbital-theme-colors';

  function paint(v) {
    if (!v || !v.a) return;
    var mix = function (c, pct, to) { return 'color-mix(in srgb, ' + c + ' ' + pct + '%, ' + to + ')'; };
    var s = root.style;
    s.setProperty('--va', v.light ? mix(v.a, 45, '#ffffff') : v.a);
    s.setProperty('--va-l', v.light ? v.a : mix(v.a, 55, '#10141a'));
    s.setProperty('--vbg', v.light ? '#07090e' : v.bg);
    s.setProperty('--vpanel', v.light ? '#0c1018' : v.panel);
    s.setProperty('--vbg-l', v.light ? v.bg : '#f6f7f9');
    s.setProperty('--vpanel-l', v.light ? v.panel : '#ffffff');
    s.setProperty('--vm', v.light ? mix(v.a, 55, '#ffffff') : v.a);
    root.classList.add("themed");
  }

  try { paint(JSON.parse(sessionStorage.getItem(VIBE))); } catch (e) { /* nothing picked yet */ }

  window.OrbitalTheme = {
    /* t: { id, name, a, b, bg, panel, light }, an app theme or a store one. */
    apply: function (t, picked) {
      if (!t || !t.a) return;
      var v = { id: t.id, name: t.name, a: t.a, b: t.b, bg: t.bg, panel: t.panel, light: !!t.light };
      try { sessionStorage.setItem(VIBE, JSON.stringify(v)); } catch (e) { /* this page only */ }
      paint(v);
      /* A light theme reads best on the light site and a dark one on the
         dark site, unless the visitor has already chosen for themselves. */
      if (picked && !stored()) apply(v.light ? 'light' : 'dark');
    },
    current: function () {
      try { return JSON.parse(sessionStorage.getItem(VIBE)) || null; } catch (e) { return null; }
    },
  };

  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function () {
      if (!stored()) apply(system());
    });
  }

  var SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>';

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('.top nav') || document.querySelector('.site-top nav');
    if (!nav) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'mode-btn';

    function label() {
      var light = root.getAttribute('data-theme') === 'light';
      btn.innerHTML = light ? MOON : SUN;
      btn.setAttribute('aria-label', light ? 'Switch to dark mode' : 'Switch to light mode');
      btn.title = btn.getAttribute('aria-label');
    }

    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      apply(next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* kept for this page only */ }
      label();
    });

    label();
    document.addEventListener('orbital:theme', label);
    var cta = nav.querySelector('.nav-cta');
    nav.insertBefore(btn, cta || null);
  });
})();
