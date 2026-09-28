/* Theme and layout links: orbitallauncher.com/t/<themeId> and /l/<code>.
 *
 * With Orbital installed, Android opens these links in the app (App Links, verified through
 * /.well-known/assetlinks.json) and this page is never seen. Without it, this page shows what was
 * shared and offers two ways on: "Open in Orbital", which asks Android for the app by an intent
 * link and falls back to Google Play, and a plain Google Play button.
 *
 * A link may carry a referral, as ?referrer=ref%3D<code>. It is passed on to Google Play exactly
 * as the Play Install Referrer expects, so the app can read it on first launch. Nothing is stored
 * and nothing is sent anywhere by this page.
 */
(function () {
  var PACKAGE = 'com.alid0n.orbital';
  var REF_RE = /^[0-9A-HJKMNP-TV-Z]{8}$/;
  var CODE_ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

  function referral() {
    var raw = new URLSearchParams(location.search).get('referrer') || '';
    var ref = new URLSearchParams(raw).get('ref') || '';
    return REF_RE.test(ref) ? ref : '';
  }

  function playUrl(ref) {
    var url = 'https://play.google.com/store/apps/details?id=' + PACKAGE;
    return ref ? url + '&referrer=' + encodeURIComponent('ref=' + ref) : url;
  }

  /* An intent link to the same address: Android opens Orbital where it is installed, and the
     browser goes to Play where it is not. */
  function appUrl(path, ref) {
    var query = ref ? '?referrer=' + encodeURIComponent('ref=' + ref) : '';
    return 'intent://orbitallauncher.com' + path + query + '#Intent;scheme=https;package=' + PACKAGE +
      ';S.browser_fallback_url=' + encodeURIComponent(playUrl(ref)) + ';end';
  }

  /* A layout code as typed: any case, ORB- optional, I/L read as 1 and O as 0. */
  function normalizeCode(raw) {
    var text = String(raw || '').toUpperCase().replace(/[\s-]/g, '');
    if (text.indexOf('ORB') === 0) text = text.slice(3);
    text = text.replace(/[IL]/g, '1').replace(/O/g, '0');
    if (text.length < 6 || text.length > 8) return '';
    for (var i = 0; i < text.length; i++) if (CODE_ALPHABET.indexOf(text[i]) < 0) return '';
    return text;
  }

  function layoutCode() {
    var fromPath = /^\/l\/([^/?#]+)/.exec(location.pathname);
    var hash = location.hash.replace(/^#/, '');
    var query = new URLSearchParams(location.search).get('c');
    return normalizeCode((fromPath && decodeURIComponent(fromPath[1])) || hash || query || '');
  }

  var ref = referral();
  var page = document.body.getAttribute('data-share');
  var path = location.pathname;

  if (page === 'layout') {
    var code = layoutCode();
    var shown = document.getElementById('layout-code');
    if (code) {
      if (shown) shown.textContent = 'ORB-' + code;
      path = '/l/' + code;
    } else {
      var missing = document.getElementById('layout-missing');
      if (missing) missing.hidden = false;
      if (shown) shown.textContent = '';
    }
  }

  var open = document.querySelectorAll('[data-open-app]');
  for (var i = 0; i < open.length; i++) open[i].href = appUrl(path, ref);
  var play = document.querySelectorAll('[data-play]');
  for (var j = 0; j < play.length; j++) play[j].href = playUrl(ref);

  window.OrbitalShare = { normalizeCode: normalizeCode, playUrl: playUrl, appUrl: appUrl };
})();
