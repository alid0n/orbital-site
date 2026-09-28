/* Seasonal themes: offered in the app only during their season, every year.
 *
 * A season is "from" and "until" as MM-DD, both days included, read in the reader's own time zone
 * as the app reads them; one whose last day comes before its first runs over New Year. February 29
 * is the 28th in a year without one.
 *
 * On a theme's own page (/t/<id>), an element with data-season-from and data-season-until says when
 * the theme is available, and outside those days the "Get it in Orbital" button is put away, since
 * the app would not offer it. themes.html uses the same arithmetic through window.OrbitalSeason.
 */
(function () {
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  function parts(text) {
    var p = String(text || '').split('-').map(Number);
    return p.length === 2 && p[0] >= 1 && p[0] <= 12 && p[1] >= 1 && p[1] <= 31 ? p : null;
  }

  function on(year, md) {
    var leap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
    var day = md[0] === 2 && md[1] === 29 && !leap ? 28 : md[1];
    return new Date(year, md[0] - 1, day);
  }

  /* The occurrence of the season that now is in, or the next one: start included, end not. */
  function seasonWindow(from, until, now) {
    var f = parts(from), u = parts(until);
    if (!f || !u) return null;
    var wraps = u[0] * 100 + u[1] < f[0] * 100 + f[1];
    for (var y = now.getFullYear() - 1; y <= now.getFullYear() + 1; y++) {
      var start = on(y, f);
      var last = on(wraps ? y + 1 : y, u);
      var end = new Date(last.getFullYear(), last.getMonth(), last.getDate() + 1);
      if (now < end) return { start: start, end: end, last: last };
    }
    return null;
  }

  function short(md) {
    var p = parts(md);
    return p ? MONTHS[p[0] - 1] + ' ' + p[1] : '';
  }

  /* "Oct 1–Nov 1" */
  function span(from, until) { return short(from) + '–' + short(until); }

  window.OrbitalSeason = { seasonWindow: seasonWindow, span: span, short: short };

  var note = document.querySelector('[data-season-from]');
  if (!note) return;
  var from = note.getAttribute('data-season-from');
  var until = note.getAttribute('data-season-until');
  var w = seasonWindow(from, until, new Date());
  if (!w) return;
  if (new Date() >= w.start) {
    note.textContent = 'In season now, until ' + short(until) + '.';
  } else {
    note.textContent = 'Available ' + span(from, until) + '.';
    var get = document.querySelectorAll('[data-open-app]');
    for (var i = 0; i < get.length; i++) get[i].style.display = 'none';
  }
})();
