/* The contents rail marks the section you are actually reading.

   An observer rather than a scroll handler: the browser does the work, and a
   page this long would otherwise be running arithmetic on every frame of a
   flick. Where there is no observer the rail is still a list of links to every
   heading, which is all it has to be. */

(function () {
  'use strict';

  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (!links.length || !('IntersectionObserver' in window)) return;

  var byId = {};
  var headings = [];

  links.forEach(function (link) {
    var id = link.getAttribute('href').slice(1);
    var heading = document.getElementById(id);
    if (!heading) return;
    byId[id] = link;
    headings.push(heading);
  });

  var seen = [];

  var watcher = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var id = entry.target.id;
      var at = seen.indexOf(id);
      if (entry.isIntersecting && at < 0) seen.push(id);
      if (!entry.isIntersecting && at >= 0) seen.splice(at, 1);
    });

    /* The first heading still on screen, in document order, rather than the
       last one crossed: scrolling back up otherwise leaves the mark on a
       section that has already gone past the top. */
    var here = null;
    for (var i = 0; i < headings.length; i++) {
      if (seen.indexOf(headings[i].id) >= 0) {
        here = headings[i].id;
        break;
      }
    }

    links.forEach(function (link) { link.classList.remove('is-here'); });
    if (here && byId[here]) byId[here].classList.add('is-here');
  }, {
    /* A band across the upper third: a heading is "where you are" once it has
       reached the top of the reading area, not when its last line leaves. */
    rootMargin: '-72px 0px -66% 0px',
    threshold: 0,
  });

  headings.forEach(function (heading) { watcher.observe(heading); });
})();
