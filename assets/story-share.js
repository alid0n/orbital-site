/* ============================================================================
   Share, from the header on phones.

   Instagram has no way for a website to post to a story directly. What it
   does take is a picture from the phone's own share sheet, and there it
   offers Stories. So the button opens a picker of story-sized pictures of
   the site (assets/story/, 1080 by 1920), each in a different theme, and
   shares the one chosen, copying the link at the same moment, ready to paste
   into a link sticker. Where a browser cannot share pictures, it shares the
   link instead, and where it cannot share at all, it copies it.

   The pictures are made by a script outside the site from the app's own
   screenshots; add a design there, then add it to DESIGNS here.
   ========================================================================== */

(function () {
  'use strict';

  var URL = 'https://orbitallauncher.com/';
  var TITLE = 'Orbital Launcher — Home, reimagined.';
  var V = '1';
  var DESIGNS = [
    ['orbital', 'Orbital'],
    ['dusk', 'Dusk'],
    ['cybernetic', 'Cybernetic'],
    ['terminal', 'Terminal'],
    ['tiles', 'Tiles'],
    ['widgets', 'Widgets'],
  ];

  var script = document.querySelector('script[src*="story-share.js"]');
  var ROOT = script ? script.src.replace(/story-share\.js.*$/, 'story/') : 'assets/story/';

  /* Each picture is fetched as soon as the picker opens, because Safari only
     lets a page open the share sheet straight from a tap, not after a
     download finishes. */
  var files = {};
  var loading = {};
  function load(key) {
    if (files[key] || loading[key] || !window.fetch || !window.File) return loading[key];
    loading[key] = fetch(ROOT + key + '.jpg?v=' + V).then(function (r) { return r.ok ? r.blob() : null; }).then(function (b) {
      if (b) files[key] = new File([b], 'orbital-launcher-' + key + '.jpg', { type: 'image/jpeg' });
      loading[key] = null;
      return files[key];
    }).catch(function () { loading[key] = null; });
    return loading[key];
  }

  var toast = null;
  var toastTimer = 0;
  function say(words) {
    if (!toast) {
      toast = document.createElement('p');
      toast.className = 'share-toast';
      toast.setAttribute('role', 'status');
      document.body.appendChild(toast);
    }
    toast.textContent = words;
    toast.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('is-on'); }, 4200);
  }

  function copyLink() {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(URL);
    } catch (e) { /* falls through */ }
    return Promise.reject(new Error('no clipboard'));
  }

  function canShareFiles() {
    return !!(navigator.canShare && window.File &&
      navigator.canShare({ files: [new File([''], 'x.jpg', { type: 'image/jpeg' })] }));
  }

  /* ---- the picker ------------------------------------------------------------ */

  var sheet = null;
  var chosen = DESIGNS[0][0];
  var goBtn = null;

  function build() {
    sheet = document.createElement('dialog');
    sheet.className = 'shs';
    sheet.setAttribute('aria-labelledby', 'shs-title');
    sheet.innerHTML =
      '<div class="shs-in">' +
      '<div class="shs-head"><h2 id="shs-title">Share to your story</h2>' +
      '<button type="button" class="shs-x" aria-label="Close">&times;</button></div>' +
      '<p class="shs-lede">Pick a look.</p>' +
      '<div class="shs-list" role="radiogroup" aria-label="Story designs">' +
      DESIGNS.map(function (d, i) {
        return '<button type="button" class="shs-opt" role="radio" aria-checked="' + (i === 0) + '" data-k="' + d[0] + '">' +
          '<img src="' + ROOT + d[0] + '-thumb.webp?v=' + V + '" alt="" width="135" height="240" loading="lazy">' +
          '<span>' + d[1] + '</span></button>';
      }).join('') +
      '</div>' +
      '<button type="button" class="btn shs-go">Share</button>' +
      '<button type="button" class="shs-copy">Copy the link instead</button>' +
      '<p class="shs-note small muted">Instagram: choose Story, then add a link sticker. The link is copied for you.</p>' +
      '</div>';
    document.body.appendChild(sheet);
    goBtn = sheet.querySelector('.shs-go');

    sheet.querySelector('.shs-x').addEventListener('click', close);
    sheet.addEventListener('click', function (e) { if (e.target === sheet) close(); });
    sheet.querySelector('.shs-list').addEventListener('click', function (e) {
      var o = e.target.closest('.shs-opt');
      if (!o) return;
      pick(o.getAttribute('data-k'));
    });
    goBtn.addEventListener('click', go);
    sheet.querySelector('.shs-copy').addEventListener('click', function () {
      copyLink().then(function () { say('Link copied.'); }, function () { say(URL); });
    });
  }

  function pick(key) {
    chosen = key;
    Array.prototype.forEach.call(sheet.querySelectorAll('.shs-opt'), function (o) {
      o.setAttribute('aria-checked', String(o.getAttribute('data-k') === key));
    });
    ready();
  }

  /* The Share button waits, briefly, for the chosen picture to arrive. */
  function ready() {
    if (!canShareFiles() || files[chosen]) {
      goBtn.disabled = false;
      goBtn.textContent = 'Share';
      return;
    }
    goBtn.disabled = true;
    goBtn.textContent = 'Getting it ready…';
    var want = chosen;
    Promise.resolve(load(want)).then(function () { if (chosen === want) ready(); });
  }

  function open() {
    if (!sheet) build();
    if (canShareFiles()) DESIGNS.forEach(function (d) { load(d[0]); });
    ready();
    if (sheet.showModal) sheet.showModal(); else sheet.setAttribute('open', '');
  }

  function close() {
    if (sheet.close) sheet.close(); else sheet.removeAttribute('open');
  }

  function go() {
    var copied = copyLink().then(function () { return true; }, function () { return false; });
    var file = files[chosen];

    if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
      navigator.share({ files: [file], title: TITLE }).then(function () {
        close();
        copied.then(function (ok) {
          if (ok) say('Link copied. In your story, add a link sticker and paste it.');
        });
      }).catch(function () { /* closed the share sheet */ });
      return;
    }
    if (navigator.share) {
      navigator.share({ title: TITLE, url: URL }).then(close).catch(function () { /* closed */ });
      return;
    }
    copied.then(function (ok) { say(ok ? 'Link copied.' : URL); });
  }

  /* ---- the header button ----------------------------------------------------- */

  var ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7.5 7.5L12 3l4.5 4.5M5 12v7.5h14V12"/></svg>';

  function addButton() {
    var nav = document.querySelector('.top nav') || document.querySelector('.site-top nav');
    if (!nav || nav.querySelector('.share-btn')) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'share-btn';
    btn.setAttribute('aria-label', 'Share Orbital Launcher');
    btn.title = 'Share';
    btn.innerHTML = ICON;
    btn.addEventListener('click', open);
    var mode = nav.querySelector('.mode-btn');
    nav.insertBefore(btn, mode || nav.querySelector('.nav-cta') || null);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addButton);
  else addButton();
})();
