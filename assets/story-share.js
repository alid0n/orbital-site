/* ============================================================================
   Share, from the header on phones.

   Instagram has no way for a website to post to a story directly. What it
   does take is a picture from the phone's own share sheet, and there it
   offers Stories. So the button opens a picker of story-sized pictures of
   the site (assets/story/, 1080 by 1920), each in a different theme, and
   shares the one chosen. The link is copied when the picker opens, ready to
   paste into a link sticker. Where a browser cannot share pictures, such as
   the ones inside Instagram and TikTok, the picture is shown to save.

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
  var HOME = script ? script.src.replace(/assets\/story-share\.js.*$/, '') : './';

  var MORE = {
    site: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7.5 7.5L12 3l4.5 4.5M5 12v7.5h14V12"/></svg>',
    link: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/></svg>',
    photo: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v14H4z M4 16l5-5 4 4 3-3 4 4"/><circle cx="15.5" cy="8.5" r="1.3"/></svg>',
  };

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
      '<p class="shs-note small muted">Choose Instagram, then Story. The link is already copied, ready for a link sticker.</p>' +
      '<div class="shs-more">' +
      '<button type="button" data-do="site">' + MORE.site + 'Share the site</button>' +
      '<button type="button" data-do="link">' + MORE.link + 'Copy link</button>' +
      '<button type="button" data-do="photo">' + MORE.photo + 'Copy photo</button>' +
      '</div>' +
      '<a class="shs-tester" href="' + HOME + '#get">Become a tester</a>' +
      /* Where the browser cannot share a picture (the browsers inside
         Instagram, TikTok and Facebook among them), the picture is shown to
         save instead, to post from Instagram itself. */
      '<div class="shs-save" hidden>' +
      '<img alt="The story picture">' +
      '<p class="shs-save-how">Press and hold the picture and choose <b>Save</b> (or <b>Add to Photos</b>), then post it from Instagram.</p>' +
      '<a class="btn shs-dl" download>Download the picture</a>' +
      '<button type="button" class="shs-back">Pick another look</button>' +
      '</div>' +
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
    sheet.querySelector('.shs-more').addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      var what = b.getAttribute('data-do');
      if (what === 'site') shareSite();
      else if (what === 'link') copyLink().then(function () { say('Link copied.'); }, function () { say(URL); });
      else copyPhoto();
    });
    sheet.querySelector('.shs-tester').addEventListener('click', function () {
      close();
      /* On the front page the form is right here; elsewhere the link goes there. */
      var form = document.getElementById('get');
      if (form) setTimeout(function () { var i = document.getElementById('email'); if (i) i.focus({ preventScroll: true }); }, 400);
    });
    sheet.querySelector('.shs-back').addEventListener('click', function () { saving(false); });
  }

  function saving(on) {
    var box = sheet.querySelector('.shs-save');
    box.hidden = !on;
    sheet.querySelector('.shs-list').hidden = on;
    sheet.querySelector('.shs-lede').hidden = on;
    goBtn.hidden = on;
    sheet.querySelector('.shs-note').hidden = on;
    sheet.querySelector('.shs-more').hidden = on;
    sheet.querySelector('.shs-tester').hidden = on;
    if (on) {
      var src = ROOT + chosen + '.jpg?v=' + V;
      box.querySelector('img').src = src;
      var dl = box.querySelector('.shs-dl');
      dl.href = src;
      dl.setAttribute('download', 'orbital-launcher-' + chosen + '.jpg');
    }
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
    if (!canShareFiles()) {
      goBtn.disabled = false;
      goBtn.textContent = 'Get the picture';
      return;
    }
    if (files[chosen]) {
      goBtn.disabled = false;
      goBtn.textContent = 'Share to Instagram';
      return;
    }
    goBtn.disabled = true;
    goBtn.textContent = 'Getting it ready…';
    var want = chosen;
    Promise.resolve(load(want)).then(function () { if (chosen === want) ready(); });
  }

  function open() {
    if (!sheet) build();
    /* The link is copied here, on the tap that opens the picker. Copying it
       on the Share tap instead used that tap up in Safari, which then
       refused to open the share sheet. */
    copyLink().catch(function () { /* the sticker can be typed */ });
    if (canShareFiles()) DESIGNS.forEach(function (d) { load(d[0]); });
    saving(false);
    ready();
    if (sheet.showModal) sheet.showModal(); else sheet.setAttribute('open', '');
  }

  function close() {
    if (sheet.close) sheet.close(); else sheet.removeAttribute('open');
  }

  /* Nothing may run before navigator.share on this tap: it has to be the
     first thing the tap does, or Safari refuses it. */
  function go() {
    var file = files[chosen];
    if (!file || !navigator.canShare || !navigator.canShare({ files: [file] })) {
      saving(true);
      return;
    }
    navigator.share({ files: [file], title: TITLE }).then(function () {
      close();
      say('In your story, add a link sticker and paste the link.');
    }).catch(function (err) {
      /* Closing the share sheet is fine; anything else means it could not
         open, so the picture is offered to save instead. */
      if (!err || err.name !== 'AbortError') saving(true);
    });
  }

  /* The site itself, as a link: to messages, email, anywhere. */
  function shareSite() {
    if (navigator.share) {
      navigator.share({ title: TITLE, url: URL }).catch(function () { /* closed */ });
      return;
    }
    copyLink().then(function () { say('Link copied.'); }, function () { say(URL); });
  }

  /* The chosen picture onto the clipboard. Clipboards take pictures only as
     PNG, so the JPG is redrawn as one; the promise goes straight into the
     ClipboardItem so Safari still counts it as part of the tap. */
  function asPng(src) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = function () {
        var c = document.createElement('canvas');
        c.width = img.naturalWidth;
        c.height = img.naturalHeight;
        c.getContext('2d').drawImage(img, 0, 0);
        c.toBlob(function (b) { if (b) resolve(b); else reject(new Error('no png')); }, 'image/png');
      };
      img.onerror = reject;
      img.src = src;
    });
  }

  function copyPhoto() {
    var src = ROOT + chosen + '.jpg?v=' + V;
    if (!navigator.clipboard || !navigator.clipboard.write || !window.ClipboardItem) {
      saving(true);
      return;
    }
    navigator.clipboard.write([new ClipboardItem({ 'image/png': asPng(src) })]).then(function () {
      say('Photo copied.');
    }).catch(function () { saving(true); });
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
