"""Builds the front page's theme picker: one picture per setup, drawn by the
site's own phone renderer (assets/phone.js), plus assets/pick/setups.js,
which lists them for assets/pick.js.

Each setup is a theme together with a way of using Orbital (a home layout, a
dock, an edge, icon shapes, effects), so the picker shows the range of what
Orbital can look like, not one home screen in many colors. Themes from the
theme store are drawn in their catalogue colors.

Run from the site folder:  python tools/make_picker.py
Needs Python with Pillow, and Microsoft Edge for the headless screenshot.
"""
import json
import pathlib
import subprocess
import tempfile
import time

from PIL import Image

SITE = pathlib.Path(__file__).resolve().parent.parent
OUT = SITE / 'assets' / 'pick'
EDGE = r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
PORT = 8133
W, HT = 240, 480

# name, theme, how it is set up. Themes from the store are "store:<id>".
# Special kinds: {"pad": true} is Orbit Pad held open, {"showcase": true} the Showcase layout.
# Store themes with a wallpaper of their own (the art themes) are added after these by
# own_setups(), each drawn as its theme file sets it up.
ROW1 = [
    ('The orbit', 'orbital', {'cards': ['ask', 'cal']}),
    ('Orbit, right', 'sleek', {}),
    ('Orbit Pad', 'gravity', {'pad': True}),
    ('Free roam', 'fluid', {'layout': 'roam'}),
    ('Honeycomb', 'honeycomb', {}),
    ('Three orbits', 'store:tokyo_night', {'orbits': 3, 'cards': ['play', 'weather']}),
    ('Live tiles', 'tiles', {}),
    ('Showcase', 'marquee', {'showcase': True}),
    ('Letter dock', 'cybernetic', {'holds': 'letters', 'fx': ['glow', 'matrix'], 'clock': 'line'}),
    ('Clock dock', 'glass', {'dock': 'container', 'at': 'start', 'edge': 'clock'}),
    ('App drawer', 'offgrid', {'layout': 'list'}),
    ('Orbit, left', 'lilac', {'anchor': 'left'}),
    ('In any app', 'dusk', {'layout': 'app'}),
    ('Named tabs', 'terminal', {}),
    ('Classic row', 'store:paper', {'dock': 'flat', 'names': 'all', 'appGrid': True, 'cards': ['weather', 'cal']}),
    ('Orbit, top', 'silk', {'anchor': 'top', 'cards': ['play']}),
    ('Large Print', 'largeprint', {}),
    ('Hex grid', 'forcefield', {}),
    ('No dock', 'minimal', {'dock': 'none'}),
    ('Two orbits', 'bubble', {'orbits': 2, 'anchor': 'right'}),
]
ROW2 = [
    ('Side row', 'slate', {}),
    ('Orbit Pad', 'store:desert_dusk', {'pad': True}),
    ('App grid', 'cupertino', {}),
    ('App drawer', 'store:matcha', {'layout': 'list', 'icons': 'rounded'}),
    ('Toggle dock', 'cybernetic', {'dock': 'container', 'at': 'start', 'edge': 'controls'}),
    ('Square frames', 'gallery', {'appGrid': True}),
    ('Showcase', 'store:arcade_assistant', {'showcase': True}),
    ('Letters, left', 'galactic', {'holds': 'letters', 'anchor': 'left'}),
    ('Hex grid', 'honeycomb', {'dock': 'none'}),
    ('Tiles, right', 'tiles', {'anchor': 'right'}),
    ('Flow effect', 'fluid', {'orbits': 2, 'fx': ['glow', 'flow']}),
    ('Dock on top', 'glass', {'dock': 'container', 'anchor': 'top', 'at': 'start', 'edge': 'battery'}),
    ('In any app', 'store:constellation', {'layout': 'app'}),
    ('Quiet row', 'efficient', {}),
    ('Free roam', 'rosegold', {'layout': 'roam'}),
    ('Center dock', 'store:crayon_box', {'dock': 'container', 'at': 'center', 'icons': 'circle'}),
    ('Original icons', 'android', {'icons': 'made', 'dock': 'flat'}),
    ('Three orbits', 'sage', {'orbits': 3}),
    ('App drawer', 'daylight', {'layout': 'list'}),
    ('Frosted dock', 'store:space_cadet', {'dock': 'container', 'at': 'end', 'edge': 'frosted'}),
]

HOME = {'PAGES': 'pages', 'FREE_ROAM': 'roam', 'DRAWER': 'list'}
DOCK = {'ORBIT': 'orbit', 'ROW': 'flat', 'CARD': 'container', 'NONE': 'none'}
SHAPE = {'CIRCLE': 'circle', 'ROUNDED': 'rounded', 'HEX': 'hex', 'TILE': 'tile', 'SQUARE': 'square', 'SQUIRCLE': 'squircle'}
CLOCK = {'STACK': 'stack', 'LINE': 'line', 'BARE': 'bare'}
WIDGET = {'GLASS': 'glass', 'CARD': 'card', 'SOLID': 'solid', 'OUTLINE': 'outline'}


def own_setups():
    """The store themes that bring a wallpaper and a setup of their own, drawn as set up."""
    cat = json.loads((SITE / 'themes' / 'index.json').read_text(encoding='utf-8'))
    # Seasonal themes are left out, since the picker is the same all year, and so is any
    # store theme the rows above already show.
    seasonal = {i for s in (cat.get('featured') or {}).get('seasonal', []) for i in s.get('themes', [])}
    used = {t[1][6:] for t in ROW1 + ROW2 if t[1].startswith('store:')}
    out = []
    for t in cat['themes']:
        if t['id'] in seasonal or t['id'] in used:
            continue
        path = SITE / 'themes' / t['id'] / 'theme.json'
        if not path.exists():
            continue
        d = json.loads(path.read_text(encoding='utf-8'))
        if not (d.get('wallpaper') or {}).get('image'):
            continue
        look, lay = d.get('look') or {}, d.get('layout') or {}
        home, dock = lay.get('homeLayout', 'PAGES'), lay.get('dockStyle', 'ORBIT')
        cfg = {'wallpaper': 'themes/%s/%s' % (t['id'], d['wallpaper']['image'])}
        shape = SHAPE.get(look.get('iconShape'))
        if home == 'ORBIT_PAD' or dock == 'PAD':
            cfg['pad'] = True
            name = 'Orbit Pad'
        elif home == 'CONSOLE':
            cfg['showcase'] = True
            name = 'Showcase'
        else:
            cfg['layout'] = HOME.get(home, 'pages')
            cfg['dock'] = DOCK.get(dock, 'orbit')
            cfg['anchor'] = (lay.get('anchor') or 'BOTTOM').lower()
            if shape:
                cfg['icons'] = shape
            if look.get('clockFace') in CLOCK:
                cfg['clock'] = CLOCK[look['clockFace']]
            if look.get('widgetLook') in WIDGET:
                cfg['widgets'] = WIDGET[look['widgetLook']]
            if look.get('glow'):
                cfg['fx'] = ['glow']
            if cfg['layout'] == 'roam':
                name = 'Free roam'
            elif cfg['layout'] == 'list':
                name = 'App drawer'
            elif shape == 'hex':
                name = 'Hex grid'
            elif shape == 'tile':
                name = 'Live tiles'
            elif cfg['dock'] == 'container':
                name = 'Container dock'
            elif cfg['dock'] == 'flat':
                name = 'Classic row'
            elif cfg['anchor'] != 'bottom':
                name = 'Orbit, ' + cfg['anchor']
            else:
                name = 'The orbit'
        out.append((name, 'store:' + t['id'], cfg))
    return out


def store_themes():
    cat = json.loads((SITE / 'themes' / 'index.json').read_text(encoding='utf-8'))
    out = {}
    for t in cat['themes']:
        c = t.get('colors') or {}
        if not c:
            continue
        out[t['id']] = {
            'name': t['name'], 'free': not t.get('premium'),
            'a': c['accent'], 'b': c.get('accentAlt') or c['accent'],
            'bg': c['surface'], 'panel': c.get('elevated') or c['surface'],
            'text': c.get('ink') or ('#1B222A' if c.get('light') else '#EEF2F6'), 'light': bool(c.get('light')),
        }
    return out


def main():
    store = store_themes()
    setups = []
    # The art themes go in turn into the two rows, every third card or so.
    own = own_setups()
    rows_in = [list(ROW1), list(ROW2)]
    for k, item in enumerate(own):
        r = rows_in[k % 2]
        r.insert(min(len(r), 1 + (k // 2) * 3), item)
    for row, items in ((0, rows_in[0]), (1, rows_in[1])):
        for i, (name, theme, cfg) in enumerate(items):
            key = 'r%d-%02d' % (row + 1, i + 1)
            setups.append({'key': key, 'row': row, 'name': name, 'theme': theme, 'cfg': cfg})

    # Store themes go into phone.js's table under a plain key, so the renderer
    # can draw them like its own.
    inject = {('st_' + k): {'name': v['name'], 'a': v['a'], 'b': v['b'], 'bg': v['bg'], 'panel': v['panel'],
                            'text': v['text'], 'light': v['light']} for k, v in store.items()}

    cols = 10
    rows = (len(setups) + cols - 1) // cols
    cells = []
    walls = []
    shows = 0
    for n, s in enumerate(setups):
        theme = s['theme'].replace('store:', 'st_')
        x, y = (n % cols) * W, (n // cols) * HT
        cfg = dict(s['cfg'])
        wall = cfg.pop('wallpaper', None)
        if wall:
            walls.append('.th-%s .wall { background: url(%s) center / cover no-repeat; }' % (theme, wall))
        if cfg.pop('pad', False):
            body = '<div class="pad" data-orbitpad data-theme="%s"></div>' % theme
        elif cfg.pop('showcase', False):
            shows += 1
            body = '<div data-showcase-home data-theme="%s" data-focus="%d"></div>' % (theme, shows * 2)
        else:
            cfg['theme'] = theme
            body = "<div class=\"mini\" data-mini='%s'></div>" % json.dumps(cfg)
        cells.append('<div class="cell" style="left:%dpx;top:%dpx">%s</div>' % (x, y, body))

    html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="assets/phone.css">
<style>
html, body { margin: 0; background: #000; overflow: hidden; }
*, *::before, *::after { transition: none !important; animation-play-state: paused !important; }
.cell { position: absolute; width: %dpx; height: %dpx; overflow: hidden; }
.cell .device { padding: 0; border-radius: 0; box-shadow: none; background: none; }
.cell .scr { aspect-ratio: 1 / 2; border-radius: 0; }
.cell .pad-hint { display: none; }
%s
</style></head><body>%s
<script src="assets/phone.js"></script>
<script>
Object.assign(window.OrbitalThemes, %s);
/* Orbit Pad held open on its third app; the keyboard also stops its own demo. */
setTimeout(function () {
  document.querySelectorAll('.pad .opad-pad').forEach(function (p) {
    p.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
    for (var i = 0; i < 2; i++) p.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight' }));
  });
}, 400);
</script></body></html>""" % (W, HT, '\n'.join(walls), ''.join(cells), json.dumps(inject))

    page = SITE / '_picker_capture.html'
    page.write_text(html, encoding='utf-8')
    shot = pathlib.Path(tempfile.gettempdir()) / 'orbital-picker.png'
    if shot.exists():
        shot.unlink()
    profile = tempfile.mkdtemp(prefix='orbital-edge-')
    server = subprocess.Popen(['python', '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(SITE)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.5)
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--user-data-dir=' + profile, '--window-size=%d,%d' % (cols * W, rows * HT),
                        '--virtual-time-budget=3000', '--screenshot=' + str(shot),
                        'http://127.0.0.1:%d/_picker_capture.html' % PORT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Edge can finish writing the picture a moment after it exits.
        for _ in range(60):
            if shot.exists() and shot.stat().st_size > 0:
                break
            time.sleep(1)
        time.sleep(1)
    finally:
        server.terminate()
        page.unlink()

    for old in OUT.glob('*.webp'):
        old.unlink()
    OUT.mkdir(exist_ok=True)
    im = Image.open(shot).convert('RGB')
    listed = []
    for n, s in enumerate(setups):
        x, y = (n % cols) * W, (n // cols) * HT
        im.crop((x, y, x + W, y + HT)).save(OUT / (s['key'] + '.webp'), quality=82)
        t = s['theme']
        if t.startswith('store:'):
            c = store[t[6:]]
        else:
            c = None
        listed.append({'key': s['key'], 'row': s['row'], 'name': s['name'], 'theme': t, 'colors': c})
    im.resize((im.width // 2, im.height // 2)).save(pathlib.Path(tempfile.gettempdir()) / 'orbital-picker-peek.png')

    (OUT / 'setups.js').write_text(
        '/* Made by tools/make_picker.py: the theme picker\'s setups and their pictures. App themes\n'
        '   take their colors from phone.js; store themes carry theirs here. */\n'
        'window.OrbitalSetups = ' + json.dumps(listed, indent=1) + ';\n', encoding='utf-8')
    print(len(listed), 'setups')


if __name__ == '__main__':
    main()
