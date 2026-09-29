/* ============================================================================
   Share, from the header on phones.

   Instagram has no way for a website to post to a story directly. What it
   does take is a picture from the phone's own share sheet, and there it
   offers Stories. So the button shares a story-sized picture of the site
   (assets/story.jpg, 1080 by 1920) and copies the link at the same moment,
   ready to paste into a link sticker. Where a browser cannot share pictures,
   it shares the link instead, and where it cannot share at all, it copies it.
   ========================================================================== */

(function () {
  'use strict';

  var URL = 'https://orbitallauncher.com/';
  var IMAGE = 'assets/story.jpg?v=1';
  var TITLE = 'Orbital Launcher — Home, reimagined.';

  /* The picture is fetched ahead of the tap, because Safari only lets a page
     open the share sheet straight from the tap itself, not after a download. */
  var file = null;
  function preload() {
    if (file || !window.fetch || !window.File) return;
    var base = document.querySelector('script[src*="story-share.js"]');
    var src = base ? base.src.replace(/assets\/story-share\.js.*$/, IMAGE) : IMAGE;
    fetch(src).then(function (r) { return r.ok ? r.blob() : null; }).then(function (b) {
      if (b) file = new File([b], 'orbital-launcher.jpg', { type: 'image/jpeg' });
    }).catch(function () { /* the link is shared instead */ });
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

  function share() {
    var copied = copyLink().then(function () { return true; }, function () { return false; });

    if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
      navigator.share({ files: [file], title: TITLE }).then(function () {
        copied.then(function (ok) {
          if (ok) say('Link copied. In your story, add a link sticker and paste it.');
        });
      }).catch(function () { /* closed the share sheet */ });
      return;
    }
    if (navigator.share) {
      navigator.share({ title: TITLE, url: URL }).catch(function () { /* closed */ });
      return;
    }
    copied.then(function (ok) {
      say(ok ? 'Link copied.' : URL);
    });
  }

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
    btn.addEventListener('click', share);
    var mode = nav.querySelector('.mode-btn');
    nav.insertBefore(btn, mode || nav.querySelector('.nav-cta') || null);
    /* Only phones show the button (see site.css), so only they need the picture. */
    if (window.matchMedia && window.matchMedia('(max-width: 760px)').matches) {
      if ('requestIdleCallback' in window) requestIdleCallback(preload); else setTimeout(preload, 1500);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addButton);
  else addButton();
})();
