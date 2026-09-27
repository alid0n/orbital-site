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
    var cta = nav.querySelector('.nav-cta');
    nav.insertBefore(btn, cta || null);
  });
})();
