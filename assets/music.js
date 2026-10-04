/* ============================================================================
   An optional soundtrack for the front page.

   The theme picker's sound switch (pick.js) decides whether there is music.
   Nothing is loaded from YouTube unless it is on; then the "orbital" playlist
   plays on the music phone, starting from the song chosen for the picked
   theme. YouTube's terms require its player to stay visible, which is why it
   is a widget rather than hidden audio. The answer is remembered for the
   rest of the visit.
   ========================================================================== */

(function () {
  'use strict';

  var PLAYLIST = 'PLXKmitZHRJ8c';
  var KEY = 'orbital-music';

  /* The song each theme starts on, by its YouTube video id in the playlist,
     spread so each song has about ten themes. App themes go by their own
     ids; theme-store themes by "store:" and theirs. A theme not listed here,
     or a song since taken out of the playlist, starts from the top. */
  var TRACKS = {
    cannedHeat: '-38yJGUvBD8',  // Jamiroquai, Canned Heat: bright, funky, fun
    paradise: '13XuCgfk1Hg',    // Clementine & the Galaxy, Paradise: soft and dreamy
    noOne: 'wZAng0z9TdA',       // Above & Beyond, No One On Earth: airy, spacious
    gravity: 'VsxGptj5Jzg',     // 28mm, Gravity: clean and focused
    strawberry: 'aiRu9hDrzI8',  // VEAUX, Strawberry Blues: calm, natural, cosy
    midnight: '8b-ecNhMIyw',    // Caravan Palace, Midnight: vintage, warm, jazzy
    skeler: 'exoTXpifiHY',      // skeler., Two to the Chest: dark and spooky
    endOfLine: 'NOMa56y_Was',   // Daft Punk, End of Line: neon and digital
  };
  var BY_SONG = {
    cannedHeat: ['bubble', 'store:candy', 'store:crayon_box', 'store:disco', 'store:sparkles',
      'store:summer_splash', 'store:golden_countdown', 'store:midnight_fireworks', 'store:canyon_poster', 'store:solar', 'store:afterglow'],
    paradise: ['blossom', 'lilac', 'rosegold', 'store:cherry_blossom', 'store:spring_bloom', 'store:valentines_day',
      'store:love_letters', 'store:beach', 'store:flamingo', 'store:almond_blossom', 'store:water_lilies', 'store:medusae', 'store:daybreak'],
    noOne: ['galactic', 'fluid', 'glass', 'gravity', 'store:glass', 'store:northern_lights', 'store:constellation',
      'store:space_cadet', 'store:winter_snow', 'store:earthrise', 'store:saturns_hexagon', 'store:midnight'],
    gravity: ['professional', 'slate', 'cupertino', 'minimal', 'sleek', 'android', 'match', 'gallery', 'efficient',
      'store:graphite', 'store:paper', 'store:rhinoceros'],
    strawberry: ['sage', 'daylight', 'store:matcha', 'store:forest_floor', 'store:cozy_cabin', 'store:cozy_rainy_day',
      'store:tropical', 'store:harvest', 'store:autumn_leaves', 'store:willow_bough', 'store:sea_of_fog', 'store:shoreline'],
    midnight: ['silk', 'dusk', 'honeycomb', 'classic', 'marquee', 'store:midnight_jazz', 'store:road_trip',
      'store:desert_dusk', 'store:gismonda', 'store:golden_sierra', 'store:great_wave'],
    skeler: ['store:halloween_night', 'store:haunted_mansion', 'store:witching_hour', 'store:spider_web',
      'store:ghost_glow', 'store:jack_o_lantern', 'store:candy_corn', 'store:pumpkin_patch'],
    endOfLine: ['orbital', 'cybernetic', 'terminal', 'tiles', 'largeprint', 'offgrid', 'forcefield',
      'store:arcade_assistant', 'store:tokyo_night', 'store:night_pass', 'store:skyline'],
  };
  var SONG = {};
  Object.keys(BY_SONG).forEach(function (k) {
    BY_SONG[k].forEach(function (theme) { SONG[theme] = TRACKS[k]; });
  });

  function vibe() {
    var v = window.OrbitalTheme && window.OrbitalTheme.current();
    return (v && v.id) || 'orbital';
  }

  /* Plays the theme's song once the playlist has loaded into the player. */
  function playFor(theme, tries) {
    if (!player || !player.getPlaylist) return;
    var list = player.getPlaylist();
    if (!list || !list.length) {
      if ((tries || 0) < 20) setTimeout(function () { playFor(theme, (tries || 0) + 1); }, 250);
      else player.playVideo();
      return;
    }
    var at = list.indexOf(SONG[theme]);
    player.playVideoAt(at < 0 ? 0 : at);
  }

  function remembered() {
    try { return sessionStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(v) {
    try { sessionStorage.setItem(KEY, v); } catch (e) { /* private mode: ask again next time */ }
  }

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
    if (card) return;
    remember('yes');
    /* The player lives on a second phone beside the hero one: the lower half of
       a home screen in the visitor's vibe (Orbital if they skipped it), enlarged so the Now playing widget is shown at its
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
        card = null;
        player = null;
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
        playerVars: { listType: 'playlist', list: PLAYLIST, index: 0, autoplay: 0, playsinline: 1, rel: 0 },
        events: { onReady: function () { playFor(vibe()); } },
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

  /* The vibe screen (vibe.js) starts the soundtrack with its sound switch.
     A browser will not start music on its own when the visitor comes back to
     this page from another one, so if it was playing earlier in the visit
     they are asked whether to pick it up again. */
  window.OrbitalMusic = { start: start };
  document.addEventListener('orbital:theme', function (e) { if (player) playFor(e.detail.id || 'orbital'); });
  /* Someone coming back, who picked a theme on an earlier visit with the sound
     on, is asked too, since the picker will not show again to start it. */
  function kept(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  var back = !remembered() && kept('orbital-picked') && kept('orbital-pick-sound') !== 'off';
  if (remembered() === 'yes' || back) {
    ask.querySelector('p').textContent = back ? 'Play the soundtrack?' : 'Pick the soundtrack back up?';
    document.body.appendChild(ask);
  }
})();
