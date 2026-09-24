/* ============================================================================
   The menu, as the launcher's own dock.

   Slots ride an ellipse, the one at the front is the one you are on, and the
   whole thing turns slowly by itself until somebody touches it. Scrolling over
   it spins it — down goes forward, up goes backward — and the spin carries on
   and slows down the way the real one does.

   Three rules this is written to keep:

   1. Every slot is a real anchor in the HTML. The script places them and does
      nothing else to them, so the menu works with no JavaScript at all, reads
      correctly to a screen reader, and is a list of links to a crawler.

   2. The page keeps its scroll. A wheel event is only taken when the pointer
      is over the wheel AND the wheel is still going to move because of it; at
      the ends of the spin range there are none, so nothing is ever swallowed.

   3. prefers-reduced-motion means what it says: no idle turning, no spin, no
      animation frames at all. The slots are placed once and the plain row of
      links underneath is shown instead.
   ========================================================================== */

(function () {
  'use strict';

  var root = document.querySelector('[data-orbit]');
  if (!root) return;

  var items = Array.prototype.slice.call(root.querySelectorAll('.orbit-item'));
  if (!items.length) return;

  var nameEl = root.querySelector('.orbit-name strong');
  var blurbEl = root.querySelector('.orbit-name span');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Where a slot sits on the ellipse, as a fraction of the box it is drawn in.
     The front of the wheel is the bottom of the ellipse, which is where the
     launcher puts the app you are turned to. */
  var CENTRE_Y = 0.42;
  var RADIUS_X = 0.44;
  var RADIUS_Y = 0.30;

  /* How fast it turns when nobody is touching it: a hair under three degrees a
     second, which is enough to notice and not enough to chase. */
  var IDLE = 0.05;

  /* What a notch of scroll is worth, and how quickly a spin gives up. */
  var PER_SCROLL = 0.0016;
  var FRICTION = 2.4;
  var FASTEST = 9;

  var angle = 0;
  var spin = 0;
  var pointerOver = false;
  var lastTime = 0;
  var frame = 0;
  var front = -1;

  var step = (Math.PI * 2) / items.length;

  function place() {
    var w = root.clientWidth;
    var h = root.clientHeight;
    var nearest = -1;
    var nearestDepth = -2;

    for (var i = 0; i < items.length; i++) {
      var a = angle + i * step;
      /* sin runs 1 at the front and -1 at the back, which is exactly the
         "how near is this" number the size and the fade both want. */
      var depth = Math.sin(a);
      var x = w * (0.5 + RADIUS_X * Math.cos(a));
      var y = h * (CENTRE_Y + RADIUS_Y * depth);
      var scale = 0.62 + 0.38 * ((depth + 1) / 2);
      var fade = 0.35 + 0.65 * ((depth + 1) / 2);

      var el = items[i];
      el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) scale(' + scale.toFixed(3) + ')';
      el.style.opacity = fade.toFixed(3);
      /* Behind the ones in front of them, so the wheel reads as having depth
         rather than as a ring of equals. */
      el.style.zIndex = String(Math.round(depth * 100) + 200);

      if (depth > nearestDepth) {
        nearestDepth = depth;
        nearest = i;
      }
    }

    if (nearest !== front) {
      if (front >= 0) items[front].classList.remove('is-front');
      items[nearest].classList.add('is-front');
      front = nearest;
      if (nameEl) nameEl.textContent = items[nearest].dataset.name || '';
      if (blurbEl) blurbEl.textContent = items[nearest].dataset.blurb || '';
    }
  }

  function tick(now) {
    var dt = lastTime ? Math.min((now - lastTime) / 1000, 0.05) : 0;
    lastTime = now;

    angle += (IDLE + spin) * dt;

    if (spin !== 0) {
      /* Exponential rather than linear, so a hard flick slows quickly and the
         last of it drifts, which is what a heavy thing on a bearing does. */
      var keep = Math.exp(-FRICTION * dt);
      spin *= keep;
      if (Math.abs(spin) < 0.01) spin = 0;
    }

    place();
    frame = window.requestAnimationFrame(tick);
  }

  function turn(by) {
    spin += by;
    if (spin > FASTEST) spin = FASTEST;
    if (spin < -FASTEST) spin = -FASTEST;
  }

  /* ---- the finger and the wheel ---------------------------------------- */

  root.addEventListener('pointerenter', function () { pointerOver = true; });
  root.addEventListener('pointerleave', function () { pointerOver = false; });

  root.addEventListener('wheel', function (event) {
    if (still.matches) return;
    if (!pointerOver) return;
    /* Taken rather than shared: the page carries on scrolling everywhere else
       on the screen, and over the wheel the wheel is what is being turned. */
    event.preventDefault();
    turn(event.deltaY * PER_SCROLL);
  }, { passive: false });

  /* Dragging it sideways turns it too, which is the gesture the launcher's own
     dock answers and the only one a touch screen can offer. */
  var dragFrom = null;
  var dragAt = 0;

  root.addEventListener('pointerdown', function (event) {
    if (still.matches) return;
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    dragFrom = event.clientX;
    dragAt = event.clientX;
  });

  root.addEventListener('pointermove', function (event) {
    if (dragFrom === null) return;
    var moved = event.clientX - dragAt;
    dragAt = event.clientX;
    angle -= moved * 0.006;
    place();
  });

  function letGo(event) {
    if (dragFrom === null) return;
    var travelled = Math.abs(event.clientX - dragFrom);
    dragFrom = null;
    /* A drag that went somewhere hands its last movement to the spin; one that
       did not travel was a tap on a link and is left entirely alone. */
    if (travelled > 6) turn(0);
  }

  root.addEventListener('pointerup', letGo);
  root.addEventListener('pointercancel', letGo);

  /* A drag that crossed a link must not also open it. */
  items.forEach(function (el) {
    el.addEventListener('click', function (event) {
      if (dragFrom !== null) event.preventDefault();
    });
  });

  /* ---- the keyboard ----------------------------------------------------- */

  root.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
      turn(1.6);
      event.preventDefault();
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
      turn(-1.6);
      event.preventDefault();
    }
  });

  /* A slot reached by tabbing is brought to the front, so the name in the
     middle is the name of the thing that is about to be opened. */
  items.forEach(function (el, index) {
    el.addEventListener('focus', function () {
      angle = (Math.PI / 2) - index * step;
      spin = 0;
      place();
    });
  });

  /* ---- starting, stopping, and coming back ------------------------------ */

  function start() {
    if (frame) return;
    lastTime = 0;
    frame = window.requestAnimationFrame(tick);
  }

  function stop() {
    if (!frame) return;
    window.cancelAnimationFrame(frame);
    frame = 0;
  }

  /* Nothing turns while the tab is in the background: a wheel spinning where
     nobody can see it is a phone getting warm for no reason. */
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop();
    else if (!still.matches && onScreen) start();
  });

  /* Nor while it is scrolled out of view, which on the front page is most of
     the time: it sits at the very bottom. */
  var onScreen = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      onScreen = entries[0].isIntersecting;
      if (!onScreen) stop();
      else if (!still.matches && !document.hidden) start();
    }).observe(root);
  }

  window.addEventListener('resize', place);

  function settle() {
    if (still.matches) {
      stop();
      /* Placed once so the slots are where they belong, and the plain row of
         links is shown under them as the menu that does not move. */
      angle = Math.PI / 2;
      spin = 0;
      place();
      var plain = document.querySelector('.orbit-fallback');
      if (plain) plain.style.display = 'flex';
    } else {
      start();
    }
  }

  if (still.addEventListener) still.addEventListener('change', settle);
  settle();
})();
