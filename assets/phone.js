/* ============================================================================
   The phones on the front page.

   Every phone on the page — the one in the hero that turns over every few
   seconds, the small ones beside each feature, and the one you can set up
   yourself — is drawn by the same few functions from a plain description:
   which theme, which home layout, which dock on which edge, which icon shape.
   A description is all a scene is, so the phones cannot drift apart from each
   other or from the settings they are showing.

   Rules this keeps:

   1. Nothing here is needed to read the page. Without script the phones are
      simply absent and every feature is still described in words beside them.

   2. prefers-reduced-motion is honoured: nothing turns, falls, pans or flips
      by itself. Docks are placed once and the hero waits for its buttons.

   3. Only phones on screen do any work. Each one is watched, and a phone that
      has scrolled away stops being ticked.
   ========================================================================== */

(function () {
  'use strict';

  var still = window.matchMedia('(prefers-reduced-motion: reduce)');
  var TAU = Math.PI * 2;
  var H = 216.667; /* the screen's height when its width is 100 */

  /* ---- drawings ----------------------------------------------------------- */

  var GLYPH = {
    phone: 'M6.6 3.5h2.6l1.3 3.6-1.9 1.3a10 10 0 0 0 5 5l1.3-1.9 3.6 1.3v2.6a2 2 0 0 1-2.2 2A15 15 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z',
    chat: 'M4 5h16v11H9l-5 4z',
    camera: 'M4 8h3.5L9 5.5h6L16.5 8H20v11H4z M15.3 13.5a3.3 3.3 0 1 1-6.6 0a3.3 3.3 0 1 1 6.6 0',
    photos: 'M3.5 5h17v14h-17z M3.5 16l5-5 4 4 3-3 5 5',
    globe: 'M21 12a9 9 0 1 1-18 0a9 9 0 1 1 18 0 M3 12h18 M12 3c3 3.2 3 14.8 0 18 M12 3c-3 3.2-3 14.8 0 18',
    mail: 'M3.5 6h17v12h-17z M3.5 6l8.5 7 8.5-7',
    pin: 'M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z M14.3 10a2.3 2.3 0 1 1-4.6 0a2.3 2.3 0 1 1 4.6 0',
    music: 'M9 18V5.5l10-2V16 M9 18a2.5 2.5 0 1 1-5 0a2.5 2.5 0 1 1 5 0 M19 16a2.5 2.5 0 1 1-5 0a2.5 2.5 0 1 1 5 0',
    calendar: 'M4 6h16v14H4z M4 10h16 M8 3.5v4 M16 3.5v4',
    clock: 'M20.5 12a8.5 8.5 0 1 1-17 0a8.5 8.5 0 1 1 17 0 M12 7v5l3.5 2',
    notes: 'M6 3.5h9l3 3V20.5H6z M9 10h6 M9 13.5h6 M9 17h4',
    cloud: 'M7 18.5h10a4 4 0 0 0 .6-8A5.5 5.5 0 0 0 7 9.5a4.5 4.5 0 0 0 0 9z',
    play: 'M4 6h16v12H4z M10.5 9.5v5l4-2.5z',
    folder: 'M3.5 6.5h6l2 2h9v10h-17z',
    bag: 'M5 8h14l-1 12H6z M9 8a3 3 0 0 1 6 0',
    person: 'M15.5 8a3.5 3.5 0 1 1-7 0a3.5 3.5 0 1 1 7 0 M5 20c.8-4 3.6-6 7-6s6.2 2 7 6',
    mic: 'M12 3.5a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0v-5a3 3 0 0 1 3-3z M6.5 11.5a5.5 5.5 0 0 0 11 0 M12 17v3.5',
    gear: 'M15 12a3 3 0 1 1-6 0a3 3 0 1 1 6 0 M12 3v3 M12 18v3 M3 12h3 M18 12h3 M5.6 5.6l2.1 2.1 M16.3 16.3l2.1 2.1 M5.6 18.4l2.1-2.1 M16.3 7.7l2.1-2.1',
    prev: 'M6 5v14 M18 5l-9 7 9 7z',
    pause: 'M8.5 5v14 M15.5 5v14',
    next: 'M18 5v14 M6 5l9 7-9 7z',
    search: 'M16.5 10.5a6 6 0 1 1-12 0a6 6 0 1 1 12 0 M15 15l5 5',
    back: 'M15 5l-7 7 7 7',
    torch: 'M8 3h8v4l-2 3v11h-4V10L8 7z',
    wifi: 'M3 9.5a13 13 0 0 1 18 0 M6.5 13a8 8 0 0 1 11 0 M10 16.5a3 3 0 0 1 4 0',
    moon: 'M19 14.5A7.5 7.5 0 0 1 9.5 5a7.5 7.5 0 1 0 9.5 9.5z',
    tube: 'M3.5 8a3 3 0 0 1 3-3h11a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-11a3 3 0 0 1-3-3z M10 9v6l5-3z',
    game: 'M7.5 8h9a4.5 4.5 0 0 1 4.5 4.5v.5a3 3 0 0 1-5.3 1.9L14.5 13.5h-5l-1.2 1.4A3 3 0 0 1 3 13v-.5A4.5 4.5 0 0 1 7.5 8z M8 10v3.5 M6.25 11.75h3.5 M15.5 11h.01 M17.5 12.5h.01',
  };

  function glyph(name) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + GLYPH[name] + '"/></svg>';
  }

  /* Made-up apps with plain drawings, so no real company's icon is borrowed.
     The last field is the outline each one "came with", used when the icon
     shape is left as the app made it. */
  var APPS = [
    ['Phone', 'phone', '#2BB673', 'circle'],
    ['Messages', 'chat', '#3B82F6', 'squircle'],
    ['Browser', 'globe', '#2563EB', 'circle'],
    ['Camera', 'camera', '#64748B', 'rounded'],
    ['Photos', 'photos', '#F59E0B', 'squircle'],
    ['Music', 'music', '#F43F5E', 'circle'],
    ['Maps', 'pin', '#10B981', 'squircle'],
    ['Mail', 'mail', '#EF4444', 'rounded'],
    ['Calendar', 'calendar', '#6366F1', 'rounded'],
    ['Settings', 'gear', '#6B7280', 'circle'],
    ['Clock', 'clock', '#0EA5A4', 'circle'],
    ['Notes', 'notes', '#EAB308', 'rounded'],
    ['Weather', 'cloud', '#38BDF8', 'squircle'],
    ['Video', 'play', '#DC2626', 'rounded'],
    ['Files', 'folder', '#A16207', 'squircle'],
    ['Store', 'bag', '#16A34A', 'rounded'],
    ['Contacts', 'person', '#8B5CF6', 'circle'],
    ['Podcasts', 'mic', '#A855F7', 'squircle'],
  ];

  function app(name) {
    for (var i = 0; i < APPS.length; i++) if (APPS[i][0] === name) return APPS[i];
    return APPS[0];
  }

  var LETTERS = ['B', 'C', 'F', 'M', 'N', 'P', 'S', 'V', 'W'];

  function appsFor(letter) {
    return APPS.filter(function (a) { return a[0].charAt(0) === letter; }).slice(0, 4);
  }

  /* ---- themes ------------------------------------------------------------- */

  /* The launcher's own colours for each theme, and the things each one sets
     when it is picked. Anything a scene says overrides these. */
  var BASE = {
    layout: 'pages', dock: 'orbit', anchor: 'bottom', holds: 'apps', orbits: 1,
    icons: 'squircle', style: 'original', widgets: 'card', clock: 'center',
    names: 'front', marks: 'dots', fx: [], font: 'sans', radius: 4,
    cards: ['ask', 'weather'], appGrid: false, page: 'default',
    at: 'start', edge: 'clock', drift: false, text: '#EEF2F6', light: false,
  };

  var THEMES = {
    android: { name: 'Android', free: true, a: '#D0BCFF', b: '#B69DF8', bg: '#141218', panel: '#1D1B20', text: '#E6E0E9', icons: 'made', cards: ['ask', 'weather'] },
    orbital: { name: 'Orbital', free: true, a: '#7FE7C4', b: '#4FC3A1', bg: '#0A0D11', panel: '#10151B', icons: 'squircle', drift: true, cards: ['ask', 'cal'] },
    sleek: { name: 'Sleek', free: true, a: '#FFFFFF', b: '#CED3D9', bg: '#060708', panel: '#0D0F12', anchor: 'right', icons: 'circle', style: 'theme', widgets: 'outline', clock: 'left', names: 'none', radius: 6, cards: ['weather', 'next'] },
    classic: { name: 'Classic', free: true, a: '#8CCB8A', b: '#B5DCA9', bg: '#121315', panel: '#1E2023', dock: 'flat', icons: 'made', names: 'all', cards: ['weather'], appGrid: true },
    largeprint: { name: 'Large Print', free: true, a: '#FFD60A', b: '#9DD5FF', bg: '#000000', panel: '#0B0B0B', text: '#FFFFFF', dock: 'flat', icons: 'rounded', widgets: 'solid', clock: 'bold', names: 'all', page: 'big', cards: ['weather'] },
    dusk: { name: 'Dusk', a: '#F4A97A', b: '#D2708C', bg: '#1A1016', panel: '#201520', widgets: 'solid', cards: ['next', 'play'] },
    professional: { name: 'Professional', a: '#6E9BF0', b: '#8FB4F5', bg: '#0E1219', panel: '#141A22', dock: 'flat', icons: 'rounded', names: 'all', radius: 1.5, cards: ['cal'] },
    cybernetic: { name: 'Cybernetic', a: '#00E5FF', b: '#7AF0FF', bg: '#000000', panel: '#00090C', icons: 'square', style: 'theme', widgets: 'brackets', clock: 'line', fx: ['glow', 'pulse'], radius: 1, cards: ['next', 'weather'] },
    galactic: { name: 'Galactic', a: '#9B8CFF', b: '#63D2FF', bg: '#070519', panel: '#110E2A', icons: 'circle', style: 'theme', widgets: 'solid', names: 'none', fx: ['glow'], radius: 6, cards: ['play'] },
    terminal: { name: 'Terminal', a: '#35E06A', b: '#9BF5B4', bg: '#000000', panel: '#010401', text: '#C9F7D6', icons: 'square', style: 'theme', widgets: 'brackets', clock: 'line', marks: 'tabs', fx: ['scan', 'glow'], font: 'term', radius: 1, cards: ['next', 'note'] },
    tiles: { name: 'Tiles', a: '#2FA8FF', b: '#7CC8FF', bg: '#080B10', panel: '#111822', dock: 'flat', icons: 'tile', style: 'theme', widgets: 'solid', names: 'all', marks: 'none', radius: 0 },
    honeycomb: { name: 'Honeycomb', a: '#FFB627', b: '#FFD27A', bg: '#120C04', panel: '#1E1508', dock: 'flat', icons: 'hex', names: 'none', radius: 3 },
    clockwork: { name: 'Clockwork', a: '#C9A227', b: '#E6C766', bg: '#0D0B08', panel: '#17130D', icons: 'circle', style: 'theme', widgets: 'outline', clock: 'line', cards: ['cal'] },
    glass: { name: 'Glass', a: '#9FD8FF', b: '#D8BCFF', bg: '#0C1220', panel: '#101829', widgets: 'glass', radius: 7, wall: 'glass', cards: ['weather', 'play'] },
    cupertino: { name: 'Cupertino', a: '#0A84FF', b: '#64B5FF', bg: '#000000', panel: '#1C1C1E', dock: 'flat', icons: 'rounded', names: 'all', radius: 5, cards: ['weather'], appGrid: true },
    slate: { name: 'Slate', a: '#5AA0F8', b: '#F7C66B', bg: '#161C26', panel: '#232C3A', dock: 'flat', anchor: 'right', icons: 'rounded', widgets: 'paper', names: 'all', cards: ['weather', 'next'], appGrid: true },
    daylight: { name: 'Daylight', a: '#0A625E', b: '#9A4210', bg: '#F4F2ED', panel: '#FBFAF7', text: '#1B222A', light: true, dock: 'flat', names: 'all', cards: ['weather', 'cal'] },
    minimal: { name: 'Minimal', a: '#C9BFAE', b: '#E6DFD2', bg: '#121110', panel: '#1A1917', dock: 'flat', icons: 'rounded', style: 'muted', widgets: 'none', clock: 'stack', names: 'none', marks: 'none', radius: 3, cards: ['agenda'] },
    blossom: { name: 'Blossom', a: '#8E2F57', b: '#7C4A22', bg: '#FBF2F4', panel: '#FFF8FA', text: '#261B23', light: true, dock: 'flat', icons: 'circle', names: 'all', font: 'serif', radius: 6, cards: ['next', 'note'] },
    rosegold: { name: 'Rose Gold', a: '#E8B4A0', b: '#D98C8C', bg: '#15100F', panel: '#1C1614', icons: 'rounded', font: 'serif', cards: ['cal'] },
    lilac: { name: 'Lilac', a: '#C8A9E8', b: '#E8B8D4', bg: '#14111A', panel: '#1C1826', icons: 'circle', widgets: 'outline', radius: 5, cards: ['weather', 'next'] },
    silk: { name: 'Silk', a: '#E7D3A8', b: '#CBA6C3', bg: '#0F1220', panel: '#161A2B', font: 'serif', clock: 'bare', cards: ['play'] },
    sage: { name: 'Sage', a: '#A8C8A8', b: '#E0CDA8', bg: '#0D120E', panel: '#141A15', dock: 'flat', icons: 'circle', widgets: 'outline', names: 'all', cards: ['weather', 'note'] },
    fluid: { name: 'Fluid', a: '#3FE0C8', b: '#8C9BFF', bg: '#05100F', panel: '#071614', widgets: 'outline', fx: ['glow', 'flow'], radius: 5, cards: ['next', 'play'] },
    bubble: { name: 'Bubble', a: '#FF8FC7', b: '#FFC2A0', bg: '#17091A', panel: '#1F0D24', icons: 'circle', widgets: 'pill', radius: 8, cards: ['weather', 'note'] },
    system: { name: "Your phone's colors", a: '#A8C7FA', b: '#C2E7FF', bg: '#111418', panel: '#1D2024', style: 'theme', radius: 5, cards: ['ask', 'weather'] },
  };

  var THEME_ORDER = Object.keys(THEMES);

  function preset(id) {
    var t = THEMES[id] || THEMES.orbital;
    var cfg = {};
    var k;
    for (k in BASE) cfg[k] = BASE[k];
    for (k in t) cfg[k] = t[k];
    cfg.theme = id;
    cfg.fx = (t.fx || []).slice();
    cfg.cards = (t.cards || BASE.cards).slice();
    return cfg;
  }

  function scene(o) {
    var cfg = preset(o.theme);
    for (var k in o) if (k !== 'theme') cfg[k] = Array.isArray(o[k]) ? o[k].slice() : o[k];
    return cfg;
  }

  /* ---- the time, kept current in every phone at once ---------------------- */

  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  function two(n) { return (n < 10 ? '0' : '') + n; }

  function nowText(kind, d) {
    var h = d.getHours();
    var h12 = h % 12 || 12;
    switch (kind) {
      case 'hm': return h12 + ':' + two(d.getMinutes());
      case 'hm24': return two(h) + ':' + two(d.getMinutes());
      case 'hms24': return two(h) + ':' + two(d.getMinutes()) + ':' + two(d.getSeconds());
      case 'hh': return two(h12);
      case 'mm': return two(d.getMinutes());
      case 'date': return DAYS[d.getDay()] + ', ' + MONTHS[d.getMonth()] + ' ' + d.getDate();
      case 'day': return DAYS[d.getDay()];
      case 'dnum': return String(d.getDate());
      case 'month': return MONTHS[d.getMonth()];
      default: return '';
    }
  }

  function freshen(root) {
    var d = new Date();
    var els = (root || document).querySelectorAll('[data-now]');
    for (var i = 0; i < els.length; i++) {
      var t = nowText(els[i].getAttribute('data-now'), d);
      if (els[i].textContent !== t) els[i].textContent = t;
    }
  }

  window.setInterval(function () { if (!document.hidden) freshen(); }, 1000);

  /* ---- pieces of a screen ------------------------------------------------- */

  function icon(a, cfg, o) {
    o = o || {};
    var shape = cfg.icons === 'made' ? a[3] : cfg.icons;
    var style = cfg.icons === 'made' ? 'original' : cfg.style;
    var name = o.name ? '<i>' + a[0] + '</i>' : '';
    var inside = shape === 'tile';
    return '<span class="ic s-' + shape + ' st-' + style + (o.cls ? ' ' + o.cls : '') + '" style="--c:' + a[2] + '">' +
      '<span class="ic-face">' + glyph(a[1]) + (inside ? '<i>' + a[0] + '</i>' : '') + '</span>' +
      (inside ? '' : name) + '</span>';
  }

  function clockBlock(cfg, extra) {
    var c = cfg.clock;
    var cls = 'clk clk-' + c + (extra ? ' ' + extra : '');
    if (c === 'none') return '';
    if (c === 'stack') return '<div class="' + cls + '"><b data-now="hh"></b><b data-now="mm"></b><span data-now="date"></span></div>';
    if (c === 'line') return '<div class="' + cls + '"><b data-now="hms24"></b><span data-now="date"></span></div>';
    if (c === 'bare') return '<div class="' + cls + '"><b data-now="hm"></b></div>';
    return '<div class="' + cls + '"><b data-now="hm"></b><span data-now="date"></span></div>';
  }

  function calGrid() {
    var d = new Date();
    var first = new Date(d.getFullYear(), d.getMonth(), 1).getDay();
    var days = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
    var prevDays = new Date(d.getFullYear(), d.getMonth(), 0).getDate();
    var out = '';
    'SMTWTFS'.split('').forEach(function (l) { out += '<i class="dh">' + l + '</i>'; });
    var cells = Math.ceil((first + days) / 7) * 7;
    for (var i = 0; i < cells; i++) {
      var n = i - first + 1;
      if (n < 1) out += '<i class="dim">' + (prevDays + n) + '</i>';
      else if (n > days) out += '<i class="dim">' + (n - days) + '</i>';
      else out += '<i' + (n === d.getDate() ? ' class="today"' : '') + '>' + n + '</i>';
    }
    return '<div class="calg">' + out + '</div>';
  }

  var CARDS = {
    ask: function () {
      return '<div class="card ask-pill"><span class="ask-dot"></span><span>Ask Orbital</span></div>';
    },
    cal: function () {
      return '<div class="card cal"><div class="cal-h"><b data-now="month"></b><span>&lsaquo;&nbsp;&nbsp;&rsaquo;</span></div>' + calGrid() + '</div>';
    },
    weather: function () {
      return '<div class="card wx"><span class="wx-g">' + glyph('cloud') + '</span><div><b class="t">18&deg;</b><span class="s">Partly cloudy &middot; H 21&deg; L 12&deg;</span></div></div>';
    },
    next: function () {
      return '<div class="card nx"><span class="k">Up next</span><b class="t">Lunch with Sam</b><span class="s">1:00 PM &middot; Caf&eacute; Rosa</span></div>';
    },
    play: function () {
      return '<div class="card np"><span class="np-art"></span><div class="np-txt"><b class="t">Midnight Drive</b><span class="s">The Satellites</span><span class="np-bar"><i></i></span></div>' +
        '<span class="np-ctl">' + glyph('prev') + glyph('pause') + glyph('next') + '</span></div>';
    },
    note: function () {
      return '<div class="card nt"><span class="k">Note</span><span class="t2">Pick up the dry cleaning on the way home</span></div>';
    },
    agenda: function () {
      return '<div class="card ag"><span><b>1:00</b> Lunch with Sam</span><span><b>3:30</b> Dentist</span><span><b>6:00</b> Pick up flowers</span></div>';
    },
  };

  function cards(cfg) {
    var list = cfg.lite ? cfg.cards.slice(0, 1) : cfg.cards;
    return list.map(function (k) { return CARDS[k] ? CARDS[k]() : ''; }).join('');
  }

  function marks(cfg) {
    if (cfg.marks === 'dots') return '<div class="marks"><i></i><i class="on"></i><i></i></div>';
    return '';
  }

  function tabs(cfg) {
    if (cfg.marks !== 'tabs') return '';
    return '<div class="tabs"><b>Home</b><span>Work</span><span>Media</span></div>';
  }

  /* ---- home layouts ------------------------------------------------------- */

  function pagePages(cfg) {
    if (cfg.icons === 'hex') return pageHoney(cfg);
    if (cfg.icons === 'tile') return pageTiles(cfg);
    if (cfg.page === 'big' && !cfg.lite) return pageBig(cfg);
    var out = tabs(cfg) + clockBlock(cfg) + cards(cfg);
    if (cfg.appGrid && !cfg.lite) {
      out += '<div class="agrid">' + ['Mail', 'Maps', 'Music', 'Notes', 'Files', 'Store', 'Clock', 'Video']
        .map(function (n) { return icon(app(n), cfg, { name: cfg.names !== 'none' }); }).join('') + '</div>';
    }
    return '<div class="pg pg-default">' + out + marks(cfg) + '</div>';
  }

  /* A honeycomb: hexagons standing on a point, each row sitting in the
     notches of the one above. */
  function pageHoney(cfg) {
    var ins = insets(cfg);
    var W = Math.min(16.4, (100 - ins.l - ins.r - 8 - 5.6) / 5);
    var X = W + 1.4, V = W * 1.1547 * 0.75 + 1.2;
    var rows = cfg.lite ? 3 : 5;
    var out = '';
    var k = 3;
    for (var r = 0; r < rows; r++) {
      var odd = r % 2 === 1;
      var cols = odd ? 4 : 5;
      for (var c = 0; c < cols; c++) {
        var a = APPS[k++ % APPS.length];
        var left = 1 + c * X + (odd ? X / 2 : 0);
        out += '<span class="hx" style="left:' + left.toFixed(2) + 'cqw;top:' + (r * V).toFixed(2) + 'cqw">' + icon(a, cfg) + '</span>';
      }
    }
    var h = (rows - 1) * V + W * 1.1547;
    return '<div class="pg pg-honey">' + clockBlock(cfg, 'clk-sm') +
      '<div class="comb" style="height:' + h.toFixed(1) + 'cqw;--hw:' + W.toFixed(2) + 'cqw">' + out + '</div>' + marks(cfg) + '</div>';
  }

  function pageTiles(cfg) {
    function t(span, cls, inner) {
      return '<div class="tl ' + cls + '" style="grid-column:span ' + span[0] + ';grid-row:span ' + span[1] + '">' + inner + '</div>';
    }
    function appTile(n) { return t([1, 1], 'tl-app', icon(app(n), cfg)); }
    var out =
      t([2, 2], 'tl-live', '<div class="lv"><div class="lv-a"><span data-now="day"></span><b data-now="dnum"></b><span data-now="month"></span></div>' +
        '<div class="lv-b"><span>Up next</span><b>Lunch with Sam</b><span>1:00 PM</span></div></div><em>Calendar</em>') +
      t([2, 2], 'tl-clock', '<b data-now="hm"></b><span data-now="day"></span><em>Clock</em>') +
      appTile('Music') + appTile('Settings') +
      t([2, 1], 'tl-wx', '<b>18&deg;</b><span>Partly cloudy</span>') +
      t([2, 2], 'tl-photo', '<em>Photos</em>') +
      appTile('Files') + appTile('Browser') + appTile('Maps') + appTile('Video') +
      appTile('Contacts') + appTile('Camera') + appTile('Store') + appTile('Mail');
    return '<div class="pg pg-tiles"><div class="twall">' + out + '</div></div>';
  }

  function pageBig(cfg) {
    var btn = ['Phone', 'Messages', 'Camera', 'Photos'].map(function (n) {
      return '<span class="bigb">' + icon(app(n), cfg) + '<b>' + n + '</b></span>';
    }).join('');
    return '<div class="pg pg-big">' + clockBlock(cfg) + CARDS.weather() + '<div class="bigg">' + btn + '</div></div>';
  }

  /* Free roam: one canvas bigger than the screen, panned about, with the
     compass that shows which folder you are in and where on its canvas. */
  function pageRoam(cfg) {
    function at(l, t, w, inner, cls) {
      return '<div class="rm ' + (cls || '') + '" style="left:' + l + '%;top:' + t + '%;width:' + w + '%">' + inner + '</div>';
    }
    function folder(name, apps) {
      return '<div class="fold"><div class="fold-lid">' +
        apps.map(function (n) { return icon(app(n), cfg); }).join('') +
        '<span class="fold-card"></span></div><i>' + name + '</i></div>';
    }
    function loose(n) { return icon(app(n), cfg, { name: true }); }
    var canvas =
      at(4, 4, 30, clockBlock(scene({ theme: cfg.theme, clock: cfg.clock === 'line' ? 'line' : 'center' }))) +
      at(38, 7, 22, CARDS.weather()) +
      at(66, 5, 24, CARDS.note()) +
      at(7, 36, 13, folder('Travel', ['Maps', 'Photos', 'Weather', 'Browser']), 'fold-a') +
      at(27, 37, 5, loose('Music')) + at(33, 44, 5, loose('Camera')) + at(26, 50, 5, loose('Mail')) +
      at(44, 32, 25, '<div class="card ph"><span class="ph-img"></span><b class="t">Lake weekend</b></div>') +
      at(74, 36, 13, folder('Work', ['Mail', 'Calendar', 'Notes', 'Files']), 'fold-b') +
      at(6, 64, 27, CARDS.play()) +
      at(40, 66, 24, CARDS.next()) +
      at(70, 66, 13, folder('Games', ['Video', 'Store', 'Podcasts', 'Contacts']));
    var mini =
      '<i style="left:4%;top:4%;width:30%;height:14%"></i><i style="left:38%;top:7%;width:22%;height:9%"></i>' +
      '<i style="left:66%;top:5%;width:24%;height:10%"></i><i class="f" style="left:7%;top:36%;width:13%;height:16%"></i>' +
      '<i style="left:44%;top:32%;width:25%;height:22%"></i><i class="f" style="left:74%;top:36%;width:13%;height:16%"></i>' +
      '<i style="left:6%;top:64%;width:27%;height:11%"></i><i style="left:40%;top:66%;width:24%;height:10%"></i>' +
      '<i class="f" style="left:70%;top:66%;width:13%;height:16%"></i>';
    return '<div class="pg pg-roam">' +
      '<div class="canvas">' + canvas + '<span class="spread"><i></i><i></i></span></div>' +
      '<div class="compass"><span class="lv3"><i></i><i></i><i></i></span>' +
      '<span class="mm">' + mini + '<b class="mm-frame"></b></span>' +
      '<span class="path">Home <em>&rsaquo;</em> <b>Weekend</b></span></div>' +
      '</div>';
  }

  /* The app list as the home screen: search at the top, a widget above the
     list, and the alphabet down the edge. */
  function pageList(cfg) {
    var sorted = APPS.slice().sort(function (a, b) { return a[0] < b[0] ? -1 : 1; });
    var rows = '';
    var last = '';
    sorted.forEach(function (a) {
      var l = a[0].charAt(0);
      if (l !== last) { rows += '<span class="lh">' + l + '</span>'; last = l; }
      rows += '<span class="lr">' + icon(a, cfg) + '<b>' + a[0] + '</b></span>';
    });
    var rail = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(function (l) { return '<i>' + l + '</i>'; }).join('');
    return '<div class="pg pg-list">' +
      '<div class="srch">' + glyph('search') + '<span>Search or ask Orbital</span></div>' +
      '<div class="lwin"><div class="lin">' + (cfg.lite ? '' : CARDS[cfg.cards[0] === 'ask' ? 'weather' : cfg.cards[0]]()) + rows + '</div></div>' +
      '<div class="rail">' + rail + '</div></div>';
  }

  /* Somebody else's app, for the dock to be seen over. Drawn in plain greys so
     it reads as not being the launcher. */
  function pageApp() {
    return '<div class="pg pg-app"><div class="fa">' +
      '<div class="fa-bar">' + glyph('back') + '<b>Morning Brief</b></div>' +
      '<div class="fa-hero"></div>' +
      '<b class="fa-h">City opens its new riverside park this weekend</b>' +
      '<span class="fa-l" style="width:94%"></span><span class="fa-l" style="width:88%"></span><span class="fa-l" style="width:91%"></span>' +
      '<span class="fa-l" style="width:62%"></span><span class="fa-gap"></span>' +
      '<span class="fa-l" style="width:90%"></span><span class="fa-l" style="width:95%"></span><span class="fa-l" style="width:84%"></span>' +
      '<span class="fa-l" style="width:70%"></span>' +
      '</div></div>';
  }

  /* ---- docks -------------------------------------------------------------- */

  /* Where an orbit sits for each edge, as fractions of the screen. The front of
     the wheel is the point nearest the middle of the screen. */
  var GEOM = {
    bottom: { cx: 0.5, cy: 1.0, rx: 0.47, ry: 0.155, front: -Math.PI / 2, grow: [0.3, 0.55] },
    top: { cx: 0.5, cy: 0.05, rx: 0.47, ry: 0.155, front: Math.PI / 2, grow: [0.3, 0.55] },
    right: { cx: 1.05, cy: 0.56, rx: 0.34, ry: 0.28, front: Math.PI, grow: [0.4, 0.25] },
    left: { cx: -0.05, cy: 0.56, rx: 0.34, ry: 0.28, front: 0, grow: [0.4, 0.25] },
  };

  /* narrow shrinks the width of the ellipse: an open foldable showing the
     folded screen's layout keeps a wheel the width of the folded phone,
     sitting in the middle of a screen twice as wide. */
  function geom(anchor, level, narrow) {
    var g = GEOM[anchor] || GEOM.bottom;
    var L = level || 0;
    return {
      cx: g.cx, cy: g.cy, front: g.front,
      rx: g.rx * (1 + g.grow[0] * L) * (narrow || 1),
      ry: g.ry * (1 + g.grow[1] * L),
    };
  }

  var DOCK_APPS = ['Phone', 'Messages', 'Browser', 'Camera', 'Photos', 'Music', 'Maps', 'Mail', 'Calendar', 'Settings'];

  function orbitDock(cfg) {
    var letters = cfg.holds === 'letters';
    var levels = letters ? 1 : Math.max(1, Math.min(3, cfg.orbits || 1));
    var lines = '';
    var rings = '';
    for (var L = 0; L < levels; L++) {
      var g = geom(cfg.anchor, L, cfg.narrow);
      lines += '<ellipse cx="' + (g.cx * 100).toFixed(2) + '" cy="' + (g.cy * H).toFixed(2) + '" rx="' + (g.rx * 100).toFixed(2) + '" ry="' + (g.ry * H).toFixed(2) + '"' + (L ? ' class="outer"' : '') + '/>';
      var items = '';
      if (letters) {
        items = LETTERS.map(function (l) { return '<span class="ri lt"><b>' + l + '</b></span>'; }).join('');
      } else {
        var names = L === 0 ? DOCK_APPS : (L === 1 ? ['Notes', 'Files', 'Store', 'Clock', 'Weather', 'Video', 'Contacts', 'Podcasts'] : ['Weather', 'Clock', 'Store', 'Notes', 'Files', 'Video', 'Podcasts']);
        items = names.map(function (n) {
          return '<span class="ri' + (L ? ' ri-far' : '') + '">' + icon(app(n), cfg) + '</span>';
        }).join('');
      }
      rings += '<div class="ring" data-level="' + L + '">' + items + '</div>';
    }
    var label = (!letters && cfg.names !== 'none' && (cfg.anchor === 'bottom' || cfg.anchor === 'top')) ? '<span class="fname"></span>' : '';
    var hub = (!letters && levels === 1 && cfg.anchor === 'bottom' && !cfg.lite) ? '<span class="hub"><b>Lunch with Sam</b><span>Up next &middot; 1:00 PM</span></span>' : '';
    return '<div class="dk dk-orbit">' +
      '<svg class="orb" viewBox="0 0 100 ' + H + '" preserveAspectRatio="none" aria-hidden="true">' + lines + '</svg>' +
      rings + label + hub + (letters ? '<div class="band"></div>' : '') +
      '<div class="ring-hit" aria-hidden="true"></div></div>';
  }

  function stripOf() {
    return '<div class="strip"><div class="strip-in">' +
      LETTERS.map(function (l) { return '<b>' + l + '</b>'; }).join('') + '</div></div>';
  }

  function flatDock(cfg) {
    if (cfg.holds === 'letters') {
      return '<div class="dk dk-flat is-letters"><div class="band"></div>' + stripOf() + '</div>';
    }
    var n = cfg.dockCount || 5;
    var list = DOCK_APPS.slice(0, n);
    return '<div class="dk dk-flat"><div class="row">' +
      list.map(function (x) { return icon(app(x), cfg, { name: cfg.names === 'all' }); }).join('') +
      '</div></div>';
  }

  function containerDock(cfg) {
    var side = cfg.anchor === 'left' || cfg.anchor === 'right';
    var inner;
    if (cfg.holds === 'letters') {
      inner = stripOf();
    } else {
      var list = DOCK_APPS.concat(DOCK_APPS.slice(0, 4));
      inner = '<div class="cont-in">' + list.map(function (x) { return icon(app(x), cfg); }).join('') + '</div>';
    }
    var fill = '';
    if (cfg.at !== 'center' && !side) {
      if (cfg.edge === 'clock') fill = '<div class="efill ef-clock"><b data-now="hm"></b><span data-now="day"></span></div>';
      else if (cfg.edge === 'battery') fill = '<div class="efill ef-batt"><span class="batt"><i></i></span><b>82%</b></div>';
      else if (cfg.edge === 'controls') fill = '<div class="efill ef-ctl"><i>' + glyph('torch') + '</i><i class="on">' + glyph('wifi') + '</i><i>' + glyph('moon') + '</i></div>';
      else if (cfg.edge === 'frosted') fill = '<div class="efill ef-frost"></div>';
    }
    return '<div class="dk dk-cont at-' + cfg.at + (cfg.holds === 'letters' ? ' is-letters' : '') + '">' +
      (cfg.holds === 'letters' ? '<div class="band"></div>' : '') +
      '<div class="cont">' + inner + '</div>' + fill + '</div>';
  }

  function dockHtml(cfg) {
    if (cfg.dock === 'orbit') return orbitDock(cfg);
    if (cfg.dock === 'flat') return flatDock(cfg);
    if (cfg.dock === 'container') return containerDock(cfg);
    return '';
  }

  /* How much of the screen the page gives up to the dock, per edge. Top and
     bottom are in percent of the height, the sides in percent of the width. */
  function insets(cfg) {
    var ins = { t: 7.5, r: 0, b: 2.5, l: 0 };
    var side = cfg.anchor === 'left' || cfg.anchor === 'right';
    var letters = cfg.holds === 'letters';
    var d = 0;
    if (cfg.layout === 'app') return ins;
    if (cfg.dock === 'orbit') {
      var extra = letters ? 0 : (Math.max(1, cfg.orbits) - 1);
      d = side ? 35 + extra * 13 + (letters ? 14 : 0) : 23 + extra * 8.5 + (letters ? 9 : 0);
    } else if (cfg.dock === 'flat') {
      d = side ? (cfg.icons === 'tile' ? 22 : 17) + (letters ? 14 : 0) : (cfg.icons === 'tile' ? 12 : 11) + (cfg.names === 'all' && !letters ? 2.5 : 0) + (letters ? 8 : 0);
    } else if (cfg.dock === 'container') {
      d = side ? 20 + (letters ? 14 : 0) : 11.5 + (letters ? 9 : 0);
    }
    if (!d) return ins;
    if (cfg.anchor === 'bottom') ins.b = d;
    else if (cfg.anchor === 'top') ins.t = d + 4.5;
    else if (cfg.anchor === 'right') ins.r = d;
    else ins.l = d;
    return ins;
  }

  /* ---- the whole screen --------------------------------------------------- */

  function fxLayers(cfg) {
    var out = '';
    if (cfg.fx.indexOf('matrix') >= 0) {
      var chars = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ0123456789';
      var cols = '';
      for (var i = 0; i < 16; i++) {
        var s = '';
        for (var j = 0; j < 22; j++) s += chars.charAt((i * 7 + j * 13) % chars.length);
        cols += '<span style="left:' + (i * 6.4 + 1).toFixed(1) + '%;animation-duration:' + (5 + (i * 37 % 50) / 10).toFixed(1) + 's;animation-delay:-' + ((i * 53) % 70 / 10).toFixed(1) + 's">' + s + '</span>';
      }
      out += '<div class="fxl-mx" aria-hidden="true">' + cols + '</div>';
    }
    if (cfg.fx.indexOf('pulse') >= 0) out += '<div class="fxl-pulse" aria-hidden="true"></div>';
    return out;
  }

  function render(scr, cfg) {
    var t = THEMES[cfg.theme] || THEMES.orbital;
    var ins = insets(cfg);
    var cls = ['scr', 'th-' + cfg.theme, 'anc-' + cfg.anchor, 'dock-' + cfg.dock, 'lay-' + cfg.layout,
      'w-' + cfg.widgets, 'f-' + cfg.font, 'ic-' + cfg.icons];
    if (cfg.light) cls.push('light');
    if (cfg.lite) cls.push('lite');
    if (cfg.holds === 'letters') cls.push('holds-letters');
    cfg.fx.forEach(function (f) { cls.push('fx-' + f); });
    scr.className = cls.join(' ');
    scr.style.cssText =
      '--a:' + t.a + ';--b:' + t.b + ';--bg:' + t.bg + ';--panel:' + t.panel + ';--text:' + (cfg.text || BASE.text) +
      ';--r:' + cfg.radius + 'cqw;--pt:' + ins.t + '%;--pb:' + ins.b + '%;--pl:' + ins.l + '%;--pr:' + ins.r + '%' +
      ';--pw:' + (100 - ins.l - ins.r) + 'cqw';

    /* An open foldable is two screens with one dock across both: the pages
       are drawn with room left for a dock they do not draw (hideDock), and
       the dock is drawn alone on a layer spanning the pair (dockOnly). */
    if (cfg.dockOnly) {
      scr.classList.add('dock-only');
      scr.innerHTML = dockHtml(cfg) + '<span class="gbar"></span>';
      mount(scr, cfg);
      return;
    }
    /* And the wallpaper and status bar are drawn once, behind both halves, so
       the open screen reads as one screen rather than two phones side by side. */
    if (cfg.backOnly) {
      scr.innerHTML = '<div class="wall' + (t.wall ? ' wall-' + t.wall : '') + '"></div>' +
        '<div class="sb"><span data-now="hm"></span><span class="sb-r"><i></i><i></i><b></b></span></div>';
      freshen(scr);
      return;
    }

    var page;
    if (cfg.layout === 'roam') page = pageRoam(cfg);
    else if (cfg.layout === 'list') page = pageList(cfg);
    else if (cfg.layout === 'app') page = pageApp(cfg);
    else page = pagePages(cfg);

    var dock = cfg.hideDock ? '' : dockHtml(cfg);
    if (cfg.layout === 'app') {
      dock = '<div class="ov">' + dock + '</div><span class="handle"></span><span class="touch"></span>';
    }

    if (cfg.bare) scr.classList.add('bare');
    scr.innerHTML =
      (cfg.bare ? '' : '<div class="wall' + (t.wall ? ' wall-' + t.wall : '') + '"></div>') + fxLayers(cfg) +
      (cfg.bare ? '' : '<div class="sb"><span data-now="hm"></span><span class="sb-r"><i></i><i></i><b></b></span></div>') +
      page + dock + (cfg.fx.indexOf('scan') >= 0 ? '<div class="fxl-scan" aria-hidden="true"></div>' : '') +
      (cfg.bare ? '' : '<span class="gbar"></span>');
    freshen(scr);
    mount(scr, cfg);
  }

  /* ---- things that move --------------------------------------------------- */

  function Ring(el, scr, o) {
    this.el = el;
    this.scr = scr;
    this.items = Array.prototype.filter.call(el.children, function (c) { return c.classList.contains('ri'); });
    this.n = this.items.length;
    this.anchor = o.anchor;
    this.g = geom(o.anchor, o.level, o.narrow);
    this.step = TAU / this.n;
    this.angle = this.g.front - (o.start || 0) * this.step;
    this.v = 0;
    this.target = null;
    this.drift = !!o.drift;
    this.dir = o.dir || 1;
    this.every = o.every || 2600;
    this.quiet = 0;
    this.front = -1;
    this.onFront = o.onFront || null;
    this.dragging = false;
    this.place();
  }

  Ring.prototype.nearest = function () {
    var f = this.g.front;
    return f + Math.round((this.angle - f) / this.step) * this.step;
  };

  Ring.prototype.tick = function (dt) {
    if (this.dragging) return;
    if (this.v) {
      this.angle += this.v * dt;
      this.v *= Math.exp(-3 * dt);
      if (Math.abs(this.v) < 0.35) {
        this.v = 0;
        this.target = this.nearest();
      }
    } else if (this.drift && this.target === null) {
      this.angle += 0.12 * dt * this.dir;
    } else if (this.target === null) {
      this.quiet += dt * 1000;
      if (this.quiet > this.every) {
        this.quiet = 0;
        this.target = this.nearest() + this.step * this.dir;
      }
    }
    if (this.target !== null) {
      this.angle += (this.target - this.angle) * (1 - Math.exp(-7 * dt));
      if (Math.abs(this.target - this.angle) < 0.002) {
        this.angle = this.target;
        this.target = null;
        this.quiet = 0;
      }
    }
    this.place();
  };

  /* Placed with transforms alone, in pixels from the screen's cached size, so
     turning a dock never asks the browser to lay the page out again. A dock
     that has not moved since the last frame is not touched at all. */
  Ring.prototype.place = function (force) {
    if (!force && this.angle === this.placed) return;
    this.placed = this.angle;
    var size = sizeOf(this.scr);
    var g = this.g;
    var best = -2;
    var bi = 0;
    for (var i = 0; i < this.n; i++) {
      var a = this.angle + i * this.step;
      var depth = Math.cos(a - g.front);
      var x = (g.cx + g.rx * Math.cos(a)) * size.w;
      var y = (g.cy + g.ry * Math.sin(a)) * size.h;
      var s = 0.66 + 0.34 * Math.max(0, depth);
      var op = Math.max(0, Math.min(1, (depth + 0.2) / 0.45));
      var el = this.items[i];
      el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) translate(-50%,-50%) scale(' + s.toFixed(3) + ')';
      el.style.opacity = op.toFixed(2);
      el.style.zIndex = String(60 + Math.round(depth * 40));
      if (depth > best) { best = depth; bi = i; }
    }
    if (bi !== this.front) {
      if (this.front >= 0) this.items[this.front].classList.remove('is-front');
      this.items[bi].classList.add('is-front');
      this.front = bi;
      if (this.onFront) this.onFront(bi);
    }
  };

  /* A drag along the dock turns it; the tangent at the front decides which
     way a finger's movement counts. */
  Ring.prototype.grab = function (hit) {
    var self = this;
    var last = null;
    hit.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      self.dragging = true;
      self.v = 0;
      self.target = null;
      last = { x: e.clientX, y: e.clientY, t: performance.now() };
      try { hit.setPointerCapture(e.pointerId); } catch (err) { /* nothing to capture */ }
      self.scr.dispatchEvent(new CustomEvent('orbital:touch', { bubbles: true }));
      e.preventDefault();
    });
    hit.addEventListener('pointermove', function (e) {
      if (!self.dragging || !last) return;
      var w = sizeOf(self.scr).w;
      var h = sizeOf(self.scr).h;
      var dx = e.clientX - last.x;
      var dy = e.clientY - last.y;
      var da;
      switch (self.anchor) {
        case 'top': da = -dx / (self.g.rx * w); break;
        case 'right': da = -dy / (self.g.ry * h); break;
        case 'left': da = dy / (self.g.ry * h); break;
        default: da = dx / (self.g.rx * w);
      }
      var now = performance.now();
      var dt = Math.max(0.008, (now - last.t) / 1000);
      self.angle += da;
      self.v = 0.6 * self.v + 0.4 * (da / dt);
      last = { x: e.clientX, y: e.clientY, t: now };
      self.place();
    });
    function up() {
      if (!self.dragging) return;
      self.dragging = false;
      self.quiet = -2400;
      if (Math.abs(self.v) < 1) {
        self.v = 0;
        self.target = self.nearest();
      } else {
        self.v = Math.max(-12, Math.min(12, self.v));
      }
    }
    hit.addEventListener('pointerup', up);
    hit.addEventListener('pointercancel', up);
  };

  /* A thing that moves on by one every so often: the letters on a strip, the
     apps sliding through a container. */
  function Stepper(n, every, on) {
    this.n = n;
    this.i = 0;
    this.every = every;
    this.t = 0;
    this.on = on;
    on(0);
  }

  Stepper.prototype.tick = function (dt) {
    this.t += dt * 1000;
    if (this.t >= this.every) {
      this.t = 0;
      this.i = (this.i + 1) % this.n;
      this.on(this.i);
    }
  };

  function fillBand(band, letter, cfg) {
    if (!band) return;
    var list = appsFor(letter);
    band.innerHTML = '<em>' + letter + '</em>' + list.map(function (a) { return icon(a, cfg); }).join('');
    band.classList.remove('in');
    void band.offsetWidth;
    band.classList.add('in');
  }

  function centreStrip(strip, i) {
    var inner = strip.querySelector('.strip-in');
    var cells = inner.children;
    if (!cells[i]) return;
    Array.prototype.forEach.call(cells, function (c, k) { c.classList.toggle('on', k === i); });
    var vertical = strip.clientHeight > strip.clientWidth;
    var off = vertical
      ? strip.clientHeight / 2 - (cells[i].offsetTop + cells[i].offsetHeight / 2)
      : strip.clientWidth / 2 - (cells[i].offsetLeft + cells[i].offsetWidth / 2);
    inner.style.transform = vertical ? 'translateY(' + off + 'px)' : 'translateX(' + off + 'px)';
  }

  var live = new Map();

  /* A phone off screen is asleep: its docks are not ticked, and the .asleep
     class pauses every CSS animation inside it. */
  var seen = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var rec = live.get(e.target);
      if (rec) rec.visible = e.isIntersecting;
      e.target.classList.toggle('asleep', !e.isIntersecting);
    });
  }, { rootMargin: '80px' }) : null;

  /* Each screen's size, measured once and then kept current by an observer,
     so nothing that runs every frame has to ask for it. */
  function sizeOf(scr) {
    if (!scr._size) scr._size = { w: scr.clientWidth, h: scr.clientHeight };
    return scr._size;
  }

  var resized = 'ResizeObserver' in window ? new ResizeObserver(function (entries) {
    entries.forEach(function (e) {
      var scr = e.target;
      scr._size = { w: scr.clientWidth, h: scr.clientHeight };
      var rec = live.get(scr);
      if (rec) rec.movers.forEach(function (m) { if (m.place) m.place(true); });
    });
  }) : null;

  function mount(scr, cfg) {
    unmount(scr);
    scr._size = null;
    var movers = [];
    var rec = { movers: movers, visible: !seen };

    var ringEls = scr.querySelectorAll('.ring');
    Array.prototype.forEach.call(ringEls, function (el) {
      var level = Number(el.getAttribute('data-level')) || 0;
      var dock = el.parentNode;
      var label = dock.querySelector('.fname');
      var band = dock.querySelector('.band');
      var letters = el.querySelector('.lt') !== null;
      var ring = new Ring(el, scr, {
        anchor: cfg.anchor,
        level: level,
        narrow: cfg.narrow,
        drift: cfg.drift && level === 0,
        dir: level === 1 ? -1 : 1,
        every: level ? 3600 + level * 900 : (letters ? 2000 : 2600),
        start: 0,
        onFront: level === 0 ? function (i) {
          if (letters) fillBand(band, LETTERS[i], cfg);
          else if (label) label.textContent = DOCK_APPS[i] || '';
        } : null,
      });
      if (level === 0) {
        var hit = dock.querySelector('.ring-hit');
        if (hit) ring.grab(hit);
      }
      movers.push(ring);
    });

    Array.prototype.forEach.call(scr.querySelectorAll('.strip'), function (strip) {
      var band = strip.parentNode.querySelector('.band') || strip.parentNode.parentNode.querySelector('.band');
      movers.push(new Stepper(LETTERS.length, 1900, function (i) {
        centreStrip(strip, i);
        fillBand(band, LETTERS[i], cfg);
      }));
    });

    Array.prototype.forEach.call(scr.querySelectorAll('.cont-in'), function (inner) {
      var side = cfg.anchor === 'left' || cfg.anchor === 'right';
      movers.push(new Stepper(DOCK_APPS.length, 2200, function (i) {
        var first = inner.children[0];
        if (!first) return;
        var gap = parseFloat(getComputedStyle(inner).gap) || 0;
        var size = (side ? first.offsetHeight : first.offsetWidth) + gap;
        if (i === 0) {
          inner.style.transition = 'none';
          inner.style.transform = 'none';
          void inner.offsetWidth;
          inner.style.transition = '';
          return;
        }
        inner.style.transform = side ? 'translateY(' + (-i * size) + 'px)' : 'translateX(' + (-i * size) + 'px)';
      }));
    });

    live.set(scr, rec);
    if (seen) seen.observe(scr);
    if (resized) resized.observe(scr);
  }

  function unmount(scr) {
    if (!live.has(scr)) return;
    live.delete(scr);
    if (seen) seen.unobserve(scr);
    if (resized) resized.unobserve(scr);
  }

  var tickers = [];
  var lastT = 0;

  function frame(now) {
    var dt = lastT ? Math.min((now - lastT) / 1000, 0.05) : 0;
    lastT = now;
    if (!still.matches && !document.hidden) {
      live.forEach(function (rec) {
        if (!rec.visible) return;
        for (var i = 0; i < rec.movers.length; i++) rec.movers[i].tick(dt);
      });
    }
    for (var k = 0; k < tickers.length; k++) tickers[k](dt);
    window.requestAnimationFrame(frame);
  }
  window.requestAnimationFrame(frame);

  function device(extra) {
    return '<div class="device' + (extra ? ' ' + extra : '') + '"><div class="scr"></div></div>';
  }

  /* ---- the hero: a phone that turns over to show another setup ------------ */

  var SCENES = [
    { theme: 'orbital', title: 'The orbit dock', line: 'Your favorite apps on a wheel. Turn it with your thumb; try dragging it.' },
    { theme: 'honeycomb', title: 'Honeycomb', line: 'Hexagon icons, laid out edge to edge like a comb.' },
    { theme: 'tiles', title: 'Tiles', line: 'Square tiles that fill the screen, with live tiles that turn over.' },
    { theme: 'terminal', title: 'Terminal', line: 'Named tabs, scan lines and a monospaced clock with seconds.' },
    { theme: 'sleek', title: 'Sleek', line: 'Monochrome, with the orbit running down the right-hand edge.' },
    { theme: 'galactic', layout: 'roam', title: 'Free roam', line: 'One open canvas that scrolls in every direction, with folders you can walk into.' },
    { theme: 'daylight', layout: 'list', title: 'Drawer layout', line: 'Every app right on the home screen, with a widget above them.' },
    { theme: 'glass', dock: 'container', at: 'start', edge: 'clock', title: 'Container dock', line: 'A compact card of apps, with the clock beside it on the same edge.' },
    { theme: 'cybernetic', holds: 'letters', fx: ['glow', 'matrix'], clock: 'line', title: 'Drawer mode', line: 'The dock becomes an alphabet. Spin to a letter and its apps appear.' },
    { theme: 'dusk', layout: 'app', title: 'Over other apps', line: 'The dock waits at the edge of any app and slides out when you reach for it.' },
    { theme: 'slate', title: 'Slate', line: 'Bright white widgets, full-color icons and a dock down the side.' },
    { theme: 'largeprint', title: 'Large Print', line: 'High contrast, big buttons and every app named. Free for everyone.' },
    { theme: 'minimal', title: 'Minimal', line: 'Hours over minutes, muted icons, and nothing extra.' },
    { theme: 'orbital', orbits: 3, cards: ['weather'], title: 'Three orbits', line: 'Add rings behind the first for the apps you reach for a little less.' },
  ];

  function Showcase(root) {
    var LENGTH = 6000;
    root.innerHTML =
      '<div class="flip"><div class="flip-in">' + device() + '</div></div>' +
      '<div class="sc-meta">' +
      '<p class="sc-text" aria-live="polite"><b></b><span></span></p>' +
      '<div class="sc-row">' +
      '<button type="button" class="sc-btn" data-go="-1" aria-label="Previous setup"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>' +
      '<button type="button" class="sc-btn sc-play" aria-label="Pause"><svg viewBox="0 0 24 24"><path class="i-pause" d="M9 5v14M15 5v14"/><path class="i-play" d="M8 5l11 7-11 7z"/></svg></button>' +
      '<button type="button" class="sc-btn" data-go="1" aria-label="Next setup"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>' +
      '<span class="sc-count"></span>' +
      '</div>' +
      '<div class="sc-bar"><i></i></div>' +
      '</div>';

    var inner = root.querySelector('.flip-in');
    var scr = root.querySelector('.scr');
    var titleEl = root.querySelector('.sc-text b');
    var lineEl = root.querySelector('.sc-text span');
    var countEl = root.querySelector('.sc-count');
    var bar = root.querySelector('.sc-bar i');
    var playBtn = root.querySelector('.sc-play');

    var index = 0;
    var busy = false;
    var elapsed = 0;
    var playing = !still.matches;
    var holding = false;
    var onScreen = true;

    function describe() {
      var s = SCENES[index];
      titleEl.textContent = s.title;
      lineEl.textContent = s.line;
      countEl.textContent = (index + 1) + ' / ' + SCENES.length;
    }

    function setPlaying(p) {
      playing = p;
      root.classList.toggle('is-paused', !p);
      playBtn.setAttribute('aria-label', p ? 'Pause' : 'Play');
    }

    /* The phone turns away until it is edge-on, the new setup goes onto its
       screen while none of it can be seen, and it turns back. Two plain
       half-turns rather than a card with two faces: one screen to draw, and
       nothing for a browser's 3D stacking to get wrong. */
    function go(dir) {
      if (busy) return;
      index = (index + dir + SCENES.length) % SCENES.length;
      elapsed = 0;
      describe();
      if (still.matches) {
        render(scr, scene(SCENES[index]));
        return;
      }
      busy = true;
      inner.style.transition = 'transform 0.42s cubic-bezier(0.55, 0, 0.9, 0.45)';
      inner.style.transform = 'rotateY(' + (dir * 90) + 'deg) scale(0.92)';
      window.setTimeout(function () {
        render(scr, scene(SCENES[index]));
        inner.style.transition = 'none';
        inner.style.transform = 'rotateY(' + (-dir * 90) + 'deg) scale(0.92)';
        void inner.offsetWidth;
        inner.style.transition = 'transform 0.5s cubic-bezier(0.1, 0.55, 0.45, 1)';
        inner.style.transform = 'none';
        window.setTimeout(function () { busy = false; }, 520);
      }, 430);
    }

    render(scr, scene(SCENES[0]));
    describe();
    setPlaying(playing);

    root.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      if (b === playBtn) { setPlaying(!playing); return; }
      var d = Number(b.getAttribute('data-go'));
      if (d) go(d);
    });

    var flip = root.querySelector('.flip');
    flip.addEventListener('pointerenter', function () { holding = true; });
    flip.addEventListener('pointerleave', function () { holding = false; });
    root.addEventListener('orbital:touch', function () { elapsed = Math.min(elapsed, LENGTH * 0.2); });
    root.addEventListener('focusin', function () { holding = true; });
    root.addEventListener('focusout', function () { holding = false; });

    if (seen) {
      new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; }).observe(root);
    }

    tickers.push(function (dt) {
      if (!playing || holding || !onScreen || document.hidden) return;
      elapsed += dt * 1000;
      bar.style.transform = 'scaleX(' + Math.min(1, elapsed / LENGTH).toFixed(4) + ')';
      if (elapsed >= LENGTH) go(1);
    });
  }

  /* ---- small phones beside the features ----------------------------------- */

  function Mini(root) {
    var o = {};
    try { o = JSON.parse(root.getAttribute('data-mini') || '{}'); } catch (e) { o = {}; }
    o.theme = o.theme || 'orbital';
    root.innerHTML = device('is-small');
    render(root.querySelector('.scr'), scene(o));
  }

  /* ---- the anchor demo: one phone, every edge ----------------------------- */

  function segmented(name, label, options, value) {
    return '<fieldset class="seg" data-key="' + name + '"><legend>' + label + '</legend><div class="seg-opts">' +
      options.map(function (o) {
        return '<label><input type="radio" name="' + name + '" value="' + o[0] + '"' + (o[0] === value ? ' checked' : '') + '><span>' + o[1] + '</span></label>';
      }).join('') + '</div></fieldset>';
  }

  var uid = 0;

  function Anchors(root) {
    var id = 'anc' + (++uid);
    var state = { dock: 'orbit', anchor: 'bottom', at: 'start' };
    var CYCLE = [
      { dock: 'orbit', anchor: 'bottom' }, { dock: 'orbit', anchor: 'right' }, { dock: 'container', anchor: 'bottom', at: 'start' },
      { dock: 'container', anchor: 'bottom', at: 'end' }, { dock: 'flat', anchor: 'left' }, { dock: 'orbit', anchor: 'top' },
      { dock: 'container', anchor: 'right' }, { dock: 'orbit', anchor: 'left' }, { dock: 'flat', anchor: 'bottom' },
    ];
    root.innerHTML = '<div class="anc-phone">' + device('is-small') + '</div><div class="anc-ctl">' +
      segmented(id + 'd', 'Style', [['orbit', 'Orbit'], ['flat', 'Flat row'], ['container', 'Container']], state.dock) +
      segmented(id + 'e', 'Edge', [['bottom', 'Bottom'], ['left', 'Left'], ['right', 'Right'], ['top', 'Top']], state.anchor) +
      '<div class="anc-at">' + segmented(id + 'p', 'Position', [['start', 'Start'], ['center', 'Center'], ['end', 'End']], state.at) + '</div>' +
      '</div>';
    var scr = root.querySelector('.scr');
    var atBox = root.querySelector('.anc-at');
    var auto = !still.matches;
    var t = 0;
    var ci = 0;

    function draw() {
      render(scr, scene({ theme: 'orbital', dock: state.dock, anchor: state.anchor, at: state.at, edge: 'clock', names: 'none', cards: ['weather'], lite: true, clock: 'center' }));
      atBox.hidden = state.dock !== 'container';
      ['d', 'e', 'p'].forEach(function (k) {
        var v = k === 'd' ? state.dock : k === 'e' ? state.anchor : state.at;
        var inp = root.querySelector('input[name="' + id + k + '"][value="' + v + '"]');
        if (inp) inp.checked = true;
      });
    }

    root.addEventListener('change', function (e) {
      var n = e.target.name;
      if (n === id + 'd') state.dock = e.target.value;
      if (n === id + 'e') state.anchor = e.target.value;
      if (n === id + 'p') state.at = e.target.value;
      auto = false;
      root.classList.add('is-manual');
      draw();
    });
    root.addEventListener('orbital:touch', function () { auto = false; });

    draw();
    tickers.push(function (dt) {
      if (!auto || document.hidden) return;
      t += dt;
      if (t > 3.2) {
        t = 0;
        ci = (ci + 1) % CYCLE.length;
        var c = CYCLE[ci];
        state.dock = c.dock; state.anchor = c.anchor; state.at = c.at || 'start';
        draw();
      }
    });
  }

  /* ---- icon shapes -------------------------------------------------------- */

  var SHAPES = [['made', 'As the app made it'], ['squircle', 'Squircle'], ['circle', 'Circle'], ['rounded', 'Rounded square'], ['square', 'Square'], ['tile', 'Tiled'], ['hex', 'Hexagon']];
  var STYLES = [['original', 'Original'], ['flat', 'Flat'], ['theme', 'Theme colors'], ['custom', 'Custom colors']];

  function Shapes(root) {
    var id = 'shp' + (++uid);
    var state = { icons: 'squircle', style: 'original' };
    root.innerHTML = '<div class="shp-board scr-vars"><div class="shp-grid"></div></div><div class="shp-ctl">' +
      segmented(id + 's', 'Shape', SHAPES, state.icons) +
      segmented(id + 't', 'Style', STYLES, state.style) + '</div>';
    var board = root.querySelector('.shp-board');
    var grid = root.querySelector('.shp-grid');
    var t = THEMES.orbital;
    board.style.cssText = '--a:' + t.a + ';--b:' + t.b + ';--bg:' + t.bg + ';--panel:' + t.panel + ';--text:#EEF2F6';
    var auto = !still.matches;
    var clock = 0;
    var si = 1;
    var list = ['Phone', 'Messages', 'Browser', 'Camera', 'Photos', 'Music', 'Maps', 'Mail', 'Calendar', 'Notes', 'Weather', 'Settings'];

    function draw() {
      var cfg = { icons: state.icons, style: state.style };
      grid.className = 'shp-grid g-' + state.icons;
      grid.innerHTML = list.map(function (n) { return icon(app(n), cfg, { name: state.icons !== 'tile' && state.icons !== 'hex' }); }).join('');
      var s = root.querySelector('input[name="' + id + 's"][value="' + state.icons + '"]');
      if (s) s.checked = true;
    }

    root.addEventListener('change', function (e) {
      if (e.target.name === id + 's') state.icons = e.target.value;
      if (e.target.name === id + 't') state.style = e.target.value;
      auto = false;
      draw();
    });

    draw();
    tickers.push(function (dt) {
      if (!auto || document.hidden) return;
      clock += dt;
      if (clock > 2.2) {
        clock = 0;
        si = (si + 1) % SHAPES.length;
        state.icons = SHAPES[si][0];
        draw();
      }
    });
  }

  /* ---- build your own ----------------------------------------------------- */

  function Builder(root) {
    var id = 'bld' + (++uid);
    var cfg = preset('orbital');

    /* Twenty-six themes are too many to lay out as buttons, so they are a
       dropdown: free ones first, then Premium, each with its two colours. */
    function chip(t) {
      return '<span class="sw-chip" style="--a:' + t.a + ';--b:' + t.b + ';--bg:' + t.bg + ';--panel:' + t.panel + '"><i></i><i></i></span>';
    }
    function option(k) {
      var t = THEMES[k];
      return '<li role="option" id="' + id + '-' + k + '" data-theme="' + k + '" aria-selected="false">' + chip(t) +
        '<span>' + t.name + '</span>' + (t.free ? '' : '<em title="Orbital Premium">&#10022;</em>') + '</li>';
    }
    var free = THEME_ORDER.filter(function (k) { return THEMES[k].free; });
    var paid = THEME_ORDER.filter(function (k) { return !THEMES[k].free; });

    root.innerHTML =
      '<div class="b-phone">' + device() + '<p class="b-note small muted">Drag the orbit to turn it.</p></div>' +
      '<div class="b-ctl">' +
      '<div class="b-group"><p class="b-label" id="' + id + '-lbl">Theme</p><div class="tsel">' +
      '<button type="button" class="tsel-btn" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="' + id + '-lbl ' + id + '-cur">' +
      '<span class="tsel-chip"></span><span class="tsel-name" id="' + id + '-cur"></span><span class="tsel-tag"></span>' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>' +
      '<ul class="tsel-list" role="listbox" tabindex="-1" aria-labelledby="' + id + '-lbl" hidden>' +
      '<li class="tsel-h" role="presentation">Free</li>' + free.map(option).join('') +
      '<li class="tsel-h" role="presentation">Orbital Premium</li>' + paid.map(option).join('') +
      '</ul></div></div>' +
      segmented(id + 'l', 'Home layout', [['pages', 'Traditional pages'], ['roam', 'Free roam'], ['list', 'Drawer']], cfg.layout) +
      segmented(id + 'd', 'Dock', [['orbit', 'Orbit'], ['flat', 'Flat row'], ['container', 'Container'], ['none', 'None']], cfg.dock) +
      segmented(id + 'h', 'The dock holds', [['apps', 'Apps'], ['letters', 'Letters (drawer mode)']], cfg.holds) +
      segmented(id + 'e', 'Edge', [['bottom', 'Bottom'], ['left', 'Left'], ['right', 'Right'], ['top', 'Top']], cfg.anchor) +
      segmented(id + 'i', 'Icons', SHAPES.map(function (s) { return [s[0], s[0] === 'made' ? 'As made' : s[1]]; }), cfg.icons) +
      '</div>';

    var scr = root.querySelector('.scr');
    var noteEl = root.querySelector('.b-note');
    var btn = root.querySelector('.tsel-btn');
    var list = root.querySelector('.tsel-list');
    var opts = Array.prototype.slice.call(list.querySelectorAll('[role="option"]'));
    var KEYS = { l: 'layout', d: 'dock', h: 'holds', e: 'anchor', i: 'icons' };

    function sync() {
      Object.keys(KEYS).forEach(function (k) {
        var inp = root.querySelector('input[name="' + id + k + '"][value="' + cfg[KEYS[k]] + '"]');
        if (inp) inp.checked = true;
      });
      opts.forEach(function (o) {
        o.setAttribute('aria-selected', String(o.getAttribute('data-theme') === cfg.theme));
      });
      list.setAttribute('aria-activedescendant', id + '-' + cfg.theme);
      var t = THEMES[cfg.theme];
      btn.querySelector('.tsel-chip').innerHTML = chip(t);
      btn.querySelector('.tsel-name').textContent = t.name;
      btn.querySelector('.tsel-tag').textContent = t.free ? 'Free' : 'Premium';
      noteEl.textContent = cfg.dock === 'orbit' && cfg.holds === 'apps'
        ? 'Drag the orbit to turn it.'
        : 'Every combination here is a real setting.';
    }

    function draw() {
      render(scr, cfg);
      scr.classList.add('fresh');
      sync();
    }

    function pick(k) {
      if (!THEMES[k] || k === cfg.theme) return;
      cfg = preset(k);
      draw();
      var o = document.getElementById(id + '-' + k);
      if (o && !list.hidden) o.scrollIntoView({ block: 'nearest' });
    }

    function open(yes) {
      list.hidden = !yes;
      btn.setAttribute('aria-expanded', String(yes));
      root.querySelector('.tsel').classList.toggle('is-open', yes);
      if (yes) {
        list.focus();
        var o = document.getElementById(id + '-' + cfg.theme);
        if (o) o.scrollIntoView({ block: 'nearest' });
      }
    }

    btn.addEventListener('click', function () { open(list.hidden); });
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); open(true); }
    });

    list.addEventListener('click', function (e) {
      var o = e.target.closest('[role="option"]');
      if (!o) return;
      pick(o.getAttribute('data-theme'));
      open(false);
      btn.focus();
    });

    /* The arrow keys move through the themes and show each one as they go;
       Enter or Escape closes the list on whichever is showing. */
    list.addEventListener('keydown', function (e) {
      var order = free.concat(paid);
      var at = order.indexOf(cfg.theme);
      if (e.key === 'ArrowDown') pick(order[Math.min(order.length - 1, at + 1)]);
      else if (e.key === 'ArrowUp') pick(order[Math.max(0, at - 1)]);
      else if (e.key === 'Home') pick(order[0]);
      else if (e.key === 'End') pick(order[order.length - 1]);
      else if (e.key === 'Enter' || e.key === 'Escape' || e.key === 'Tab') {
        open(false);
        if (e.key !== 'Tab') btn.focus();
        if (e.key === 'Tab') return;
      } else return;
      e.preventDefault();
    });

    document.addEventListener('click', function (e) {
      if (!list.hidden && !root.querySelector('.tsel').contains(e.target)) open(false);
    });

    root.addEventListener('change', function (e) {
      var n = e.target.name;
      var k = n.slice(id.length);
      if (KEYS[k]) cfg[KEYS[k]] = e.target.value;
      if (k === 'i' && cfg.icons === 'made') cfg.style = 'original';
      draw();
    });

    draw();
  }

  /* ---- Ask Orbital: a line typed, and what it would do ---------------------- */

  var ASKS = [
    { line: 'text sam running late', kind: 'Text', g: 'chat', head: 'To Sam', body: 'Running late', act: 'Send' },
    { line: 'lunch with sam friday 1pm', kind: 'Event', g: 'calendar', head: 'Friday at 1:00 PM', body: 'Lunch with Sam', act: 'Add' },
    { line: 'todo call the dentist', kind: 'To-do', g: 'notes', head: 'When should I remind you?', body: 'Call the dentist', chips: ['This evening', 'Tomorrow', 'Pick a time'] },
    { line: '18% of 64', kind: 'Sum', g: 'notes', head: '18% of 64', body: '11.52', sum: true },
    { line: 'directions to the airport', kind: 'Maps', g: 'pin', head: 'Directions', body: 'To the airport', act: 'Go' },
  ];

  function Ask(root) {
    var MARKS = [['@', 'Text'], ['+', 'Event'], ['-', 'Note'], ['*', 'Reminder'], ['^', 'Open'], ['#', 'Call'], ['&amp;', 'To-do']];
    root.innerHTML =
      '<div class="askd-win">' +
      '<div class="askd-top"><i></i><i></i><i></i><span>Orbital Assistant</span></div>' +
      '<div class="askd-line"><span class="askd-dot"></span><span class="askd-prompt">C:\\ORBITAL&gt;</span><span class="askd-typed"></span><span class="askd-caret"></span></div>' +
      '<div class="askd-out" aria-live="polite"></div>' +
      '<div class="askd-marks">' + MARKS.map(function (m) { return '<span><b>' + m[0] + '</b> ' + m[1] + '</span>'; }).join('') + '</div>' +
      '</div>' +
      '<label class="askd-toggle"><input type="checkbox"><span class="askd-sw"></span>Command prompt look <em title="Orbital Premium">&#10022;</em></label>';

    var typed = root.querySelector('.askd-typed');
    var out = root.querySelector('.askd-out');
    var box = root.querySelector('input');
    var i = 0;
    var visible = true;

    box.addEventListener('change', function () { root.classList.toggle('is-console', box.checked); });

    if (seen) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(root);

    function result(a) {
      var extra = a.chips
        ? '<span class="askd-chips">' + a.chips.map(function (c) { return '<i>' + c + '</i>'; }).join('') + '</span>'
        : (a.act ? '<span class="askd-act"><i>Edit</i><b>' + a.act + '</b></span>' : '');
      return '<div class="askd-card' + (a.sum ? ' is-sum' : '') + '">' +
        '<span class="askd-g">' + glyph(a.g) + '</span>' +
        '<span class="askd-txt"><em>' + a.kind + ' &middot; ' + a.head + '</em><b>' + a.body + '</b></span>' + extra + '</div>' +
        '<p class="askd-cli"><span>' + a.kind.toUpperCase() + '</span> ' + a.head + ': "' + a.body + '"<br>' +
        (a.sum ? '= ' + a.body : 'Press Enter to ' + (a.act ? a.act.toLowerCase() : 'choose') + ', Esc to change it') + '</p>';
    }

    function show(a) {
      typed.textContent = a.line;
      out.innerHTML = result(a);
      out.classList.add('in');
    }

    if (still.matches) { show(ASKS[0]); return; }

    function wait(ms, fn) {
      window.setTimeout(function again() {
        if (!visible || document.hidden) { window.setTimeout(again, 400); return; }
        fn();
      }, ms);
    }

    function run() {
      var a = ASKS[i];
      var n = 0;
      out.classList.remove('in');
      typed.textContent = '';
      (function type() {
        if (n <= a.line.length) {
          typed.textContent = a.line.slice(0, n++);
          wait(45 + Math.random() * 55, type);
        } else {
          wait(350, function () {
            out.innerHTML = result(a);
            void out.offsetWidth;
            out.classList.add('in');
            i = (i + 1) % ASKS.length;
            wait(2900, run);
          });
        }
      })();
    }
    wait(600, run);
  }

  /* A wait that holds still while its element is off screen or the tab is in
     the background, so a scripted demo never runs where nobody can see it. */
  function patient(el) {
    var visible = true;
    if (seen) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(el);
    return function wait(ms, fn) {
      window.setTimeout(function again() {
        if (!visible || document.hidden) { window.setTimeout(again, 400); return; }
        fn();
      }, ms);
    };
  }

  /* ---- foldables: the same phone folded and open ---------------------------- */

  /* Folded, the cover screen is an ordinary phone with its own dock. Open,
     the two pages leave room for a dock they do not draw, and one dock is
     drawn across both: the same orbit, centred over the hinge, for "two pages
     side by side"; a longer flat row of its own for "a layout of its own". */
  var FOLD = {
    cover: { theme: 'orbital', cards: ['ask', 'cal'] },
    pairBack: { theme: 'orbital', backOnly: true },
    pairLeft: { theme: 'orbital', cards: ['ask', 'cal'], hideDock: true, bare: true, marks: 'none' },
    pairRight: { theme: 'orbital', cards: ['weather', 'next'], clock: 'none', appGrid: true, hideDock: true, bare: true, marks: 'none' },
    pairDock: { theme: 'orbital', names: 'none', lite: true, dockOnly: true, narrow: 0.5 },
    ownBack: { theme: 'dusk', backOnly: true },
    ownLeft: { theme: 'dusk', dock: 'flat', names: 'none', cards: ['next', 'play', 'note'], hideDock: true, bare: true, marks: 'none' },
    ownRight: { theme: 'dusk', dock: 'flat', names: 'none', clock: 'none', cards: ['weather', 'cal'], hideDock: true, bare: true, marks: 'none' },
    ownDock: { theme: 'dusk', dock: 'flat', names: 'none', dockCount: 8, dockOnly: true },
  };

  function Foldable(root) {
    var id = 'fld' + (++uid);
    root.innerHTML =
      '<div class="fold-stage"><div class="fdev">' +
      '<div class="fback"><div class="scr"></div></div>' +
      '<div class="fhalf fl"><div class="scr"></div></div>' +
      '<div class="fhalf fr"><div class="scr"></div></div>' +
      '<div class="fdock"><div class="scr"></div></div>' +
      '</div></div>' +
      '<div class="fold-ctl">' +
      segmented(id + 's', 'Phone', [['closed', 'Folded'], ['open', 'Open']], 'closed') +
      segmented(id + 'm', 'The open screen', [['pair', 'Two pages side by side'], ['own', 'A layout of its own ✦']], 'pair') +
      '</div>';
    var dev = root.querySelector('.fdev');
    var left = root.querySelector('.fl .scr');
    var right = root.querySelector('.fr .scr');
    var across = root.querySelector('.fdock .scr');
    var back = root.querySelector('.fback .scr');
    var state = { open: false, mode: 'pair' };
    var drawn = '';
    var auto = !still.matches;
    var wait = patient(root);

    function draw() {
      var key = state.open ? state.mode : 'closed';
      dev.classList.toggle('is-open', state.open);
      root.querySelector('input[name="' + id + 's"][value="' + (state.open ? 'open' : 'closed') + '"]').checked = true;
      root.querySelector('input[name="' + id + 'm"][value="' + state.mode + '"]').checked = true;
      if (key === drawn) return;
      drawn = key;
      if (key === 'own') {
        render(back, scene(FOLD.ownBack));
        render(left, scene(FOLD.ownLeft));
        render(right, scene(FOLD.ownRight));
        render(across, scene(FOLD.ownDock));
      } else if (key === 'pair') {
        render(back, scene(FOLD.pairBack));
        render(left, scene(FOLD.pairLeft));
        render(right, scene(FOLD.pairRight));
        render(across, scene(FOLD.pairDock));
      } else {
        render(left, scene(FOLD.cover));
      }
    }

    root.addEventListener('change', function (e) {
      if (e.target.name === id + 's') state.open = e.target.value === 'open';
      if (e.target.name === id + 'm') { state.mode = e.target.value; state.open = true; }
      auto = false;
      draw();
    });

    var CYCLE = [{ open: false, mode: 'pair' }, { open: true, mode: 'pair' }, { open: true, mode: 'own' }];
    var ci = 0;
    draw();
    render(right, scene(FOLD.pairRight));
    render(across, scene(FOLD.pairDock));
    (function next() {
      wait(ci === 0 ? 2600 : 4200, function () {
        if (!auto) return;
        ci = (ci + 1) % CYCLE.length;
        state.open = CYCLE[ci].open;
        state.mode = CYCLE[ci].mode;
        draw();
        next();
      });
    })();
  }

  /* ---- a phone with a keyboard: type on the home screen ----------------------- */

  var KEYROWS = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'del'],
    ['alt', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'sym', 'enter'],
    ['shift', '0', 'space', '@', 'shift2'],
  ];
  var KEYFACE = { del: '⌫', alt: 'alt', sym: 'sym', enter: '↵', shift: '⇧', shift2: '⇧', space: '', '0': '0', '@': '@' };

  function Keyboard(root) {
    var t = THEMES.orbital;
    var keys = KEYROWS.map(function (row) {
      return '<div class="kb-row">' + row.map(function (k) {
        return '<span class="key' + (k.length > 1 && k !== 'space' ? ' key-fn' : '') + (k === 'space' ? ' key-space' : '') + '" data-k="' + k + '">' + (KEYFACE[k] !== undefined ? KEYFACE[k] : k) + '</span>';
      }).join('') + '</div>';
    }).join('');
    var dock = ['Phone', 'Messages', 'Browser', 'Camera', 'Mail'].map(function (n) { return icon(app(n), { icons: 'squircle', style: 'original' }); }).join('');
    root.innerHTML =
      '<div class="kbdev">' +
      '<div class="scr kb-scr" style="--a:' + t.a + ';--b:' + t.b + ';--bg:' + t.bg + ';--panel:' + t.panel + ';--r:4cqw">' +
      '<div class="wall"></div>' +
      '<div class="sb"><span data-now="hm"></span><span class="sb-r"><i></i><i></i><b></b></span></div>' +
      '<div class="kb-home"><div class="clk clk-center"><b data-now="hm"></b><span data-now="date"></span></div></div>' +
      '<div class="kb-line">' + glyph('search') + '<span class="kb-typed"></span><span class="kb-caret"></span></div>' +
      '<div class="kb-out"></div>' +
      '<div class="kb-dock">' + dock + '</div>' +
      '</div>' +
      '<div class="kb-keys">' + keys + '</div>' +
      '</div>' +
      '<p class="kb-say small muted" aria-live="polite"></p>';
    freshen(root);

    var scr = root.querySelector('.kb-scr');
    var typed = root.querySelector('.kb-typed');
    var out = root.querySelector('.kb-out');
    var say = root.querySelector('.kb-say');
    var wait = patient(root);

    function press(ch, hold) {
      var k = ch === ' ' ? 'space' : ch === '\n' ? 'enter' : ch.toUpperCase();
      var el = root.querySelector('.key[data-k="' + k + '"]');
      if (!el) return;
      el.classList.add(hold ? 'held' : 'down');
      window.setTimeout(function () { el.classList.remove('down', 'held'); }, hold ? 1100 : 150);
    }

    function results(q) {
      var hits = APPS.filter(function (a) { return a[0].toLowerCase().indexOf(q) >= 0; }).slice(0, 3);
      return hits.map(function (a, i) {
        var n = a[0];
        var at = n.toLowerCase().indexOf(q);
        var label = n.slice(0, at) + '<b>' + n.slice(at, at + q.length) + '</b>' + n.slice(at + q.length);
        return '<span class="kb-hit' + (i === 0 ? ' on' : '') + '">' + icon(a, { icons: 'squircle', style: 'original' }) + '<span>' + label + '</span></span>';
      }).join('');
    }

    var SCRIPT = [
      { line: 'ma', say: 'Start typing anywhere on the home screen to find an app.', show: function (q) { return results(q); }, done: '<span class="kb-toast">Opening Maps</span>' },
      { line: '@sam running late', say: 'Start with a shortcut mark to hand the line to Orbital Assistant.', show: function (q) {
        return q.length > 4 ? '<span class="kb-card"><em>Text &middot; To Sam</em><b>' + (q.slice(5) ? q.slice(5).charAt(0).toUpperCase() + q.slice(6) : '&nbsp;') + '</b><i>Send</i></span>' : '';
      }, done: '<span class="kb-toast">Sent to Sam</span>' },
      { hold: 'C', say: 'Hold a key for a shortcut you choose.', done: '<span class="kb-toast"><b>C</b> Opening Camera</span>' },
    ];
    var si = 0;

    function reset() {
      typed.textContent = '';
      out.innerHTML = '';
      scr.classList.remove('is-typing');
    }

    function run() {
      var s = SCRIPT[si];
      si = (si + 1) % SCRIPT.length;
      say.textContent = s.say;
      if (s.hold) {
        press(s.hold, true);
        wait(900, function () {
          out.innerHTML = s.done;
          scr.classList.add('is-typing', 'is-done');
          wait(1700, function () { scr.classList.remove('is-done'); reset(); wait(700, run); });
        });
        return;
      }
      scr.classList.add('is-typing');
      var n = 0;
      (function type() {
        if (n < s.line.length) {
          var ch = s.line.charAt(n++);
          press(ch);
          typed.textContent = s.line.slice(0, n);
          out.innerHTML = s.show(s.line.slice(0, n));
          wait(110 + Math.random() * 70, type);
        } else {
          wait(900, function () {
            press('\n');
            out.innerHTML = s.done;
            scr.classList.add('is-done');
            wait(1500, function () { scr.classList.remove('is-done'); reset(); wait(900, run); });
          });
        }
      })();
    }

    if (still.matches) {
      scr.classList.add('is-typing');
      typed.textContent = 'ma';
      out.innerHTML = results('ma');
      say.textContent = SCRIPT[0].say;
      return;
    }
    wait(900, run);
  }

  /* ---- Kids mode: big named apps, and a PIN to leave ------------------------- */

  function Kids(root) {
    var t = THEMES.bubble;
    /* The apps a parent might pick. YouTube Kids is named, but drawn with a
       plain play button rather than its maker's logo. */
    var apps = [
      ['YouTube Kids', 'tube', '#E62117', 'rounded'],
      app('Music'),
      ['Games', 'game', '#7C5CFF', 'squircle'],
      app('Camera'),
      app('Photos'),
      app('Clock'),
    ];
    var cfg = { icons: 'squircle', style: 'original' };
    var pad = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', ''].map(function (d, i) {
      var x = 26 + (i % 3) * 24;
      var y = 50 + Math.floor(i / 3) * 10;
      return d ? '<span class="pin-k" style="left:' + x + '%;top:' + y + '%">' + d + '</span>' : '';
    }).join('');
    root.innerHTML = device('is-small') + '';
    var scr = root.querySelector('.scr');
    scr.className = 'scr kids';
    scr.style.cssText = '--a:' + t.a + ';--b:' + t.b + ';--bg:' + t.bg + ';--panel:' + t.panel + ';--r:6cqw';
    scr.innerHTML =
      '<div class="wall"></div>' +
      '<div class="sb"><span data-now="hm"></span><span class="sb-r"><i></i><i></i><b></b></span></div>' +
      '<div class="kid-top"><b>Kids mode</b><span class="kid-lock"><svg viewBox="0 0 24 24"><path d="M7 11V8a5 5 0 0 1 10 0v3 M5.5 11h13v9h-13z"/></svg></span></div>' +
      '<div class="kid-grid">' + apps.map(function (a) { return '<span class="kid-app">' + icon(a, cfg) + '<b>' + a[0] + '</b></span>'; }).join('') + '</div>' +
      '<div class="pin"><b>Enter your PIN to leave</b><span class="pin-dots"><i></i><i></i><i></i><i></i></span>' + pad + '</div>' +
      '<span class="kid-finger"></span>' +
      '<span class="gbar"></span>';
    freshen(scr);
    mount(scr, preset('bubble'));
  }

  /* ---- start everything that is on this page ------------------------------ */

  function each(sel, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(sel), function (el) { fn(el); });
  }

  each('[data-showcase]', Showcase);
  each('[data-mini]', Mini);
  each('[data-anchors]', Anchors);
  each('[data-shapes]', Shapes);
  each('[data-builder]', Builder);
  each('[data-ask]', Ask);
  each('[data-foldable]', Foldable);
  each('[data-keyboard]', Keyboard);
  each('[data-kids]', Kids);
})();
