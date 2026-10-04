/* ============================================================================
   "Pick a theme": the first thing a visitor sees on the front page.

   A full screen with the logo, the slogan and two rows of Orbital's themes
   drifting in opposite directions: the themes built into the app on one row,
   the theme store's on the other (only the ones in season, as in the app).
   Scrolling or swiping on a row pushes it along faster, or back the other
   way, and it eases back to its drift when let go.

   Picking one colours the whole site in that theme (theme.js), puts it on the
   music phone, and, with the sound switch on, starts the soundtrack on the
   song chosen for it (music.js). The pick is kept for the rest of the visit,
   so the screen shows once; "Change theme" in the hero brings it back.
   ========================================================================== */

(function () {
  'use strict';

  var APP = window.OrbitalThemes || {};
  var KEY = 'orbital-picked';
  var SOUND = 'orbital-pick-sound';
  var CATALOG = 'themes/index.json';

  function get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* this page only */ } }

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- the two rows ---------------------------------------------------------- */

  /* The app's own themes, pictured by the site's phone renderer
     (assets/pick/<id>.webp). "Your phone's colors" is left out: it has no
     colours of its own until it is on a phone. */
  function appThemes() {
    return Object.keys(APP).filter(function (id) { return id !== 'system'; }).map(function (id) {
      var t = APP[id];
      return { id: id, name: t.name, free: !!t.free, img: 'assets/pick/' + id + '.webp',
        a: t.a, b: t.b, bg: t.bg, panel: t.panel, light: !!t.light };
    });
  }

  /* A seasonal theme shows only inside its window, which may run over New
     Year (from 12-26 until 01-07). */
  function inSeason(win, now) {
    var md = function (s) { var p = s.split('-'); return +p[0] * 100 + +p[1]; };
    var today = (now.getMonth() + 1) * 100 + now.getDate();
    var from = md(win.from);
    var until = md(win.until);
    return from <= until ? today >= from && today <= until : today >= from || today <= until;
  }

  function storeThemes(catalog) {
    var now = new Date();
    var seasonal = {};
    var open = {};
    ((catalog.featured && catalog.featured.seasonal) || catalog.seasonal || []).forEach(function (s) {
      (s.themes || []).forEach(function (id) {
        seasonal[id] = true;
        if (inSeason(s, now)) open[id] = true;
      });
    });
    return (catalog.themes || []).filter(function (t) {
      return t.colors && t.thumbnail && (!seasonal[t.id] || open[t.id]);
    }).map(function (t) {
      var c = t.colors;
      return { id: 'store:' + t.id, name: t.name, free: !t.premium, img: 'themes/' + t.thumbnail,
        a: c.accent, b: c.accentAlt || c.accent, bg: c.surface, panel: c.elevated || c.surface, light: !!c.light };
    });
  }

  var byId = {};

  function card(t, quiet) {
    byId[t.id] = t;
    return '<button type="button" class="vibe" data-pick="' + t.id + '"' + (quiet ? ' tabindex="-1"' : '') +
      ' aria-label="' + t.name + (t.free ? ', free' : ', Orbital Premium') + '">' +
      '<span class="vp-img"><img src="' + t.img + '" alt="" width="240" height="480" loading="lazy" decoding="async" draggable="false">' +
      '<em class="vp-tag' + (t.free ? '' : ' is-premium') + '">' + (t.free ? 'Free' : 'Premium') + '</em></span>' +
      '<span class="vibe-name">' + t.name + '</span>' +
      '</button>';
  }

  /* Two copies of a row, so it can loop without a gap; the second is for
     looks only and is skipped by the keyboard and screen readers. */
  function fill(rowEl, list) {
    var a = list.map(function (t) { return card(t, false); }).join('');
    var b = list.map(function (t) { return card(t, true); }).join('');
    rowEl.querySelector('.vibe-track').innerHTML =
      '<div class="vibe-set">' + a + '</div><div class="vibe-set" aria-hidden="true">' + b + '</div>';
  }

  /* ---- the screen ------------------------------------------------------------ */

  var screen = null;
  var rows = [];
  var raf = 0;

  function build() {
    screen = document.createElement('div');
    screen.className = 'vibes';
    screen.setAttribute('role', 'dialog');
    screen.setAttribute('aria-modal', 'true');
    screen.setAttribute('aria-labelledby', 'vibes-h');
    var soundOn = get(SOUND) !== 'off';
    screen.innerHTML =
      '<div class="vibes-top">' +
      '<svg class="vibes-logo" viewBox="0 0 32 32" aria-hidden="true"><ellipse cx="16" cy="19" rx="12" ry="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="16" cy="12.5" r="3.4" fill="currentColor"/><circle cx="4.6" cy="20.4" r="2.1" fill="currentColor"/><circle cx="27.4" cy="20.4" r="2.1" fill="currentColor"/></svg>' +
      '<p class="vibes-brand">Orbital Launcher</p>' +
      '<p class="vibes-slogan">Home, reimagined.</p>' +
      '<h1 class="vibes-h" id="vibes-h">Pick a theme</h1>' +
      '</div>' +
      '<div class="vibes-rows">' +
      '<div class="vibe-row" data-row="app" aria-label="Themes in the app"><div class="vibe-track"></div></div>' +
      '<div class="vibe-row" data-row="store" aria-label="Themes from the theme store"><div class="vibe-track"></div></div>' +
      '</div>' +
      '<div class="vibes-foot">' +
      '<label class="vibes-sound"><input type="checkbox" role="switch"' + (soundOn ? ' checked' : '') + '>' +
      '<span class="sw" aria-hidden="true"></span><span class="vibes-sound-l">Soundtrack</span></label>' +
      '<button type="button" class="vibes-skip">Skip</button>' +
      '</div>';
    document.body.appendChild(screen);
    document.documentElement.classList.add('vibes-open');

    var rowEls = screen.querySelectorAll('.vibe-row');
    fill(rowEls[0], appThemes());
    rows = [Row(rowEls[0], -1)];

    /* The store row fills in when the catalog arrives; until then it shows
       the app's themes the other way round, so it is never empty. */
    var appBack = appThemes().reverse();
    fill(rowEls[1], appBack);
    rows.push(Row(rowEls[1], 1));
    fetch(CATALOG).then(function (r) { return r.ok ? r.json() : null; }).then(function (cat) {
      var list = cat ? storeThemes(cat) : [];
      if (list.length < 6 || !screen) return;
      fill(rowEls[1], list);
      rows[1].measure();
    }).catch(function () { /* keeps the app themes */ });

    var last = 0;
    raf = requestAnimationFrame(function tick(now) {
      var dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
      last = now;
      rows.forEach(function (r) { r.step(dt); });
      raf = requestAnimationFrame(tick);
    });

    screen.querySelector('.vibes-sound input').addEventListener('change', function (e) {
      put(SOUND, e.target.checked ? 'on' : 'off');
    });
    screen.querySelector('.vibes-skip').addEventListener('click', function () { choose(null); });
    screen.addEventListener('keydown', function (e) { if (e.key === 'Escape') choose(null); });
    var first = screen.querySelector('.vibe');
    if (first) first.focus({ preventScroll: true });
  }

  /* One row: it drifts at its own speed, a wheel or a swipe adds to that, and
     the extra fades away again over about a second. */
  function Row(el, dir) {
    var track = el.querySelector('.vibe-track');
    var drift = reduced ? 0 : 34 * dir;
    var x = 0;
    var v = drift;
    var width = 0;
    var drag = null;
    var moved = 0;

    function measure() {
      var set = el.querySelector('.vibe-set');
      width = set ? set.offsetWidth : 0;
    }
    measure();

    function place() {
      if (!width) measure();
      if (!width) return;
      var p = ((x % width) + width) % width;
      track.style.transform = 'translate3d(' + (-p) + 'px,0,0)';
    }
    window.addEventListener('resize', measure);

    /* The wheel: down pushes the row along the way it is already going, up
       sends it back. Sideways scrolling moves it the way you scroll. */
    el.addEventListener('wheel', function (e) {
      e.preventDefault();
      var d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY * dir;
      if (e.deltaMode === 1) d *= 32;
      v = Math.max(-2600, Math.min(2600, v + d * 9));
    }, { passive: false });

    /* A swipe drags the row under the finger, then lets it coast. */
    el.addEventListener('pointerdown', function (e) {
      if (e.button) return;
      drag = { id: e.pointerId, x: e.clientX, y: e.clientY, t: performance.now(), vx: 0, on: false };
      moved = 0;
    });
    el.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      var dx = e.clientX - drag.x;
      if (!drag.on) {
        if (Math.abs(dx) < 6 || Math.abs(dx) < Math.abs(e.clientY - drag.y)) return;
        drag.on = true;
        try { el.setPointerCapture(e.pointerId); } catch (err) { /* fine without */ }
        el.classList.add('is-dragging');
      }
      var now = performance.now();
      var dt = Math.max(1, now - drag.t) / 1000;
      x -= dx;
      moved += Math.abs(dx);
      drag.vx = drag.vx * 0.6 + (-dx / dt) * 0.4;
      drag.x = e.clientX;
      drag.t = now;
    });
    function up(e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (drag.on) v = Math.max(-3000, Math.min(3000, drag.vx));
      drag = null;
      el.classList.remove('is-dragging');
    }
    el.addEventListener('pointerup', up);
    el.addEventListener('pointercancel', up);
    /* A tap picks; the end of a swipe does not. */
    el.addEventListener('click', function (e) {
      if (moved > 8) { e.preventDefault(); e.stopPropagation(); moved = 0; return; }
      var b = e.target.closest('.vibe');
      if (b) choose(b.getAttribute('data-pick'), b);
    }, true);

    return {
      measure: measure,
      step: function (dt) {
        if (!drag || !drag.on) {
          v += (drift - v) * (1 - Math.exp(-dt * 1.6));
          x += v * dt;
        }
        place();
      },
    };
  }

  function choose(id, from) {
    if (!screen) return;
    var t = id ? byId[id] : null;
    if (t && window.OrbitalTheme) window.OrbitalTheme.apply(t, true);
    put(KEY, t ? t.id : 'skip');
    var sound = screen.querySelector('.vibes-sound input').checked;
    if (from) from.classList.add('is-picked');
    screen.classList.add('is-leaving');
    document.documentElement.classList.remove('vibes-open');
    if (location.hash) history.replaceState(null, '', location.pathname);
    window.scrollTo(0, 0);
    var s = screen;
    screen = null;
    setTimeout(function () {
      cancelAnimationFrame(raf);
      s.remove();
    }, reduced ? 0 : 650);
    document.dispatchEvent(new CustomEvent('orbital:theme', { detail: { id: t ? t.id : null, sound: sound } }));
    if (sound && window.OrbitalMusic) window.OrbitalMusic.start();
  }

  function open() { if (!screen) build(); }
  window.OrbitalPicker = { open: open };

  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-pick-theme]');
    if (a) { e.preventDefault(); open(); }
  });

  /* Anyone arriving on a link to part of the page (#get, #feedback) goes
     straight there; everyone else gets the picker once per visit. */
  if (!get(KEY) && !location.hash) open();
})();
