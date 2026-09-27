/* ============================================================================
   An optional soundtrack for the front page.

   On arrival the visitor is asked whether they would like music. Nothing is
   loaded from YouTube unless they say yes; then the "orbital" playlist starts
   from its first track, End of Line, in a small player in the corner. YouTube's
   terms require its player to stay visible, which is why it is a card rather
   than hidden audio. The answer is remembered for the rest of the visit, so
   the question is asked once, not on every return to the page.
   ========================================================================== */

(function () {
  'use strict';

  var PLAYLIST = 'PLRxK8yQIVa0k';
  var KEY = 'orbital-music';

  function remembered() {
    try { return sessionStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(v) {
    try { sessionStorage.setItem(KEY, v); } catch (e) { /* private mode: ask again next time */ }
  }

  if (remembered() === 'no') return;

  var ask = document.createElement('div');
  ask.className = 'music-ask';
  ask.setAttribute('role', 'dialog');
  ask.setAttribute('aria-label', 'Soundtrack');
  ask.innerHTML =
    '<p>Would you like to experience the website with an audio soundtrack?</p>' +
    '<div class="music-ask-btns"><button type="button" class="btn" data-a="yes">Yes, play music</button>' +
    '<button type="button" class="btn ghost" data-a="no">No thanks</button></div>';

  var card = null;
  var player = null;

  function start() {
    /* The player lives on a second phone under the hero one: the lower half of
       a red home screen, enlarged so the Now playing widget is shown at its
       real size. It sits in the open space under the calendar, beside the app
       list and above the orbit dock, the way it would on a phone. */
    var demo = document.querySelector('.hero-demo');
    var zoom = document.createElement('div');
    zoom.className = 'mz';
    var dayOf = new Date().getDate();
    var calRow = function (from) {
      var out = '';
      for (var d = from; d < from + 7; d++) {
        out += '<i' + (d === dayOf ? ' class="on"' : '') + '>' + (d > 30 ? d - 30 : d) + '</i>';
      }
      return out;
    };
    var appRow = function (name, path) {
      return '<span class="mz-app"><b>' + name + '</b><span class="mz-ic"><svg viewBox="0 0 24 24"><path d="' + path + '"/></svg></span></span>';
    };
    zoom.innerHTML =
      '<div class="mz-dev"><div class="mz-scr">' +
      '<div class="mz-floor"></div><div class="mz-glow"></div>' +
      '<div class="mz-left">' +
      '<div class="mz-cal"><div class="mz-cal-g">' + calRow(20) + calRow(27) + '</div>' +
      '<span class="mz-cal-ev"><em>1:00 PM</em> Lunch with Sam</span></div>' +
      '<div class="mz-slot"></div>' +
      '</div>' +
      '<div class="mz-right">' +
      appRow('Maps', 'M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z M14.3 10a2.3 2.3 0 1 1-4.6 0a2.3 2.3 0 1 1 4.6 0') +
      appRow('Messages', 'M4 5h16v11H9l-5 4z') +
      appRow('Music', 'M9 18V5.5l10-2V16 M9 18a2.5 2.5 0 1 1-5 0a2.5 2.5 0 1 1 5 0 M19 16a2.5 2.5 0 1 1-5 0a2.5 2.5 0 1 1 5 0') +
      appRow('Notes', 'M6 3.5h9l3 3V20.5H6z M9 10h6 M9 13.5h6 M9 17h4') +
      appRow('Photos', 'M3.5 5h17v14h-17z M3.5 16l5-5 4 4 3-3 5 5') +
      '<span class="mz-rail">M N O P R S T</span>' +
      '</div>' +
      '<div class="mz-dock">' +
      '<svg class="mz-orb" viewBox="0 0 100 40" preserveAspectRatio="none"><ellipse cx="50" cy="44" rx="46" ry="30"/></svg>' +
      '<span class="mz-d" style="left:12%;top:62%"><svg viewBox="0 0 24 24"><path d="M4 6h16v12H4z M10.5 9.5v5l4-2.5z"/></svg></span>' +
      '<span class="mz-d" style="left:30%;top:30%"><svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg></span>' +
      '<span class="mz-d is-front" style="left:50%;top:18%"><svg viewBox="0 0 24 24"><path d="M6.6 3.5h2.6l1.3 3.6-1.9 1.3a10 10 0 0 0 5 5l1.3-1.9 3.6 1.3v2.6a2 2 0 0 1-2.2 2A15 15 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/></svg></span>' +
      '<span class="mz-d" style="left:70%;top:30%"><svg viewBox="0 0 24 24"><path d="M15 12a3 3 0 1 1-6 0a3 3 0 1 1 6 0 M12 3v3 M12 18v3 M3 12h3 M18 12h3"/></svg></span>' +
      '<span class="mz-d" style="left:88%;top:62%"><svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-18 0a9 9 0 1 1 18 0 M3 12h18"/></svg></span>' +
      '<span class="mz-wx">&#9728; 72&deg;F Clear</span>' +
      '</div>' +
      '</div></div>';
    if (demo) demo.appendChild(zoom); else document.body.appendChild(zoom);
    document.documentElement.classList.add('has-music');

    card = document.createElement('div');
    card.className = 'music-card mz-np';
    var ICON = {
      prev: '<svg viewBox="0 0 24 24"><path d="M6 5v14 M18 5l-9 7 9 7z"/></svg>',
      pause: '<svg viewBox="0 0 24 24"><path d="M8.5 5v14 M15.5 5v14"/></svg>',
      play: '<svg viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z"/></svg>',
      next: '<svg viewBox="0 0 24 24"><path d="M18 5v14 M6 5l9 7-9 7z"/></svg>',
    };

    /* Drawn as the phones' own Now playing widget: the video is the artwork,
       with the song, the artist, the progress and the three buttons under it. */
    card.innerHTML =
      '<div class="music-frame"><div id="music-player"></div></div>' +
      '<div class="music-np">' +
      '<span class="music-np-k">Now playing</span>' +
      '<b class="music-np-t">Loading…</b><span class="music-np-s">&nbsp;</span>' +
      '<span class="music-np-bar"><i></i></span>' +
      '<span class="music-np-ctl">' +
      '<button type="button" data-m="prev" aria-label="Previous song">' + ICON.prev + '</button>' +
      '<button type="button" data-m="toggle" aria-label="Pause">' + ICON.pause + '</button>' +
      '<button type="button" data-m="next" aria-label="Next song">' + ICON.next + '</button>' +
      '<button type="button" data-m="close" class="music-np-x" aria-label="Stop the soundtrack">&times;</button>' +
      '</span></div>';
    zoom.querySelector('.mz-slot').appendChild(card);

    var titleEl = card.querySelector('.music-np-t');
    var byEl = card.querySelector('.music-np-s');
    var barEl = card.querySelector('.music-np-bar i');
    var toggleEl = card.querySelector('[data-m="toggle"]');

    card.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b || !player) return;
      var m = b.getAttribute('data-m');
      if (m === 'close') {
        player.stopVideo();
        clearInterval(sync);
        zoom.remove();
        document.documentElement.classList.remove('has-music');
        remember('no');
      } else if (m === 'prev') {
        player.previousVideo();
      } else if (m === 'next') {
        player.nextVideo();
      } else if (player.getPlayerState() === 1) {
        player.pauseVideo();
      } else {
        player.playVideo();
      }
    });

    /* Once a second, the real song goes into this widget and into every Now
       playing widget on the demo phones, so they all show what is playing. */
    var sync = setInterval(function () {
      if (!player || !player.getVideoData) return;
      var d = player.getVideoData() || {};
      var dur = player.getDuration() || 0;
      var at = dur ? Math.min(1, player.getCurrentTime() / dur) : 0;
      var playing = player.getPlayerState() === 1;
      var title = d.title || 'Loading…';
      /* YouTube names auto-generated artist channels "Artist - Topic". */
      var by = (d.author || '').replace(/\s+-\s+Topic$/, '');

      titleEl.textContent = title;
      byEl.textContent = by || ' ';
      barEl.style.transform = 'scaleX(' + at.toFixed(3) + ')';
      toggleEl.innerHTML = playing ? ICON.pause : ICON.play;
      toggleEl.setAttribute('aria-label', playing ? 'Pause' : 'Play');

      document.documentElement.classList.add('has-music');
      Array.prototype.forEach.call(document.querySelectorAll('.card.np'), function (w) {
        var t = w.querySelector('.t');
        var s = w.querySelector('.s');
        var bar = w.querySelector('.np-bar i');
        if (t && t.textContent !== title) t.textContent = title;
        if (s && s.textContent !== by) s.textContent = by;
        if (bar) bar.style.transform = 'scaleX(' + at.toFixed(3) + ')';
        w.classList.toggle('is-paused', !playing);
      });
    }, 1000);

    window.onYouTubeIframeAPIReady = function () {
      player = new YT.Player('music-player', {
        host: 'https://www.youtube-nocookie.com',
        width: '100%',
        height: '100%',
        playerVars: { listType: 'playlist', list: PLAYLIST, index: 0, autoplay: 1, playsinline: 1, rel: 0 },
        events: { onReady: function (ev) { ev.target.playVideo(); } },
      });
    };
    var s = document.createElement('script');
    s.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(s);
  }

  ask.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    var yes = b.getAttribute('data-a') === 'yes';
    remember(yes ? 'yes' : 'no');
    ask.remove();
    if (yes) start();
  });

  document.body.appendChild(ask);
})();
