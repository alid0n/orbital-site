# orbitallauncher.com

The site for Orbital Launcher. Three pages, no build step, no dependencies: what
is in this folder is what gets served.

```
index.html      the front page, kept to things to play with: the turning phone,
                the dock on any edge, the theme builder, the foldable, keyboard
                and Kids mode demos, and the tester form
features.html   the explaining: every dock style, the home layouts, icons,
                Orbital Assistant, the details, privacy and Premium
guide.html      every feature and every setting, page by page
privacy.html    the privacy policy
assets/
  site.css      one stylesheet for every page
  phone.js      draws every phone on the site from a plain description
                (theme, home layout, dock, edge, icon shape); the showcase,
                the edge and icon demos, the theme builder, the foldable,
                keyboard and Kids mode demos and the Ask Orbital demo all
                live here. Docks move by transform only, and phones off
                screen are paused.
  phone.css     how those phones look, sized in cqw so one drawing scales
  orbit.js      the guide's contents as a wheel: idle turn, scroll, drag, keys
  ask.js        the tester form, with a mail fallback
  toc.js        marks the section you are reading in the guide's rail
  favicon.svg
CNAME           orbitallauncher.com, for GitHub Pages
robots.txt, sitemap.xml, 404.html
```

## Looking at it locally

```bash
python -m http.server 8123
```

Then open <http://localhost:8123>. Any static server will do; there is nothing
to compile.

## Putting it up

**GitHub Pages.** Make a public repository, push this folder to it, then
Settings → Pages → *Deploy from a branch* → `main` / root. The `CNAME` file
already names the domain, so Pages will pick it up. At the registrar, point the
domain at GitHub:

| Record | Host  | Value |
| ------ | ----- | ----- |
| A      | `@`   | `185.199.108.153` |
| A      | `@`   | `185.199.109.153` |
| A      | `@`   | `185.199.110.153` |
| A      | `@`   | `185.199.111.153` |
| CNAME  | `www` | `<your-user>.github.io.` |

Then tick *Enforce HTTPS* once the certificate has been issued, which takes a
few minutes.

**Netlify or Cloudflare Pages** work as well and want no configuration: point
either at the repository, or drag this folder into Netlify's deploy box, and add
the domain in their dashboard.

## The privacy policy exists twice

`privacy.html` here is a copy of the one already published at
`alid0n.com/orbital/privacy.html`, with the canonical link and the title
pointing at this domain. **The Play Console listing still points at the
alid0n.com address**, so until that is changed, both copies are live and both
have to be edited together — or the old one turned into a redirect to this one,
which is the tidier answer and needs the Play Console URL changed at the same
time.

Whichever way it goes, the policy text itself should only ever be changed in one
place and copied to the other. A privacy policy that says two different things
about the same app is worse than either version of it.

## House rules

- No build step, no framework, no analytics, no fonts beyond the two from
  Google Fonts that the app's own pages already use.
- Every menu slot is a real `<a>` in the markup. The wheel places them; with no
  JavaScript it is a plain row of links, which is also what somebody who has
  asked for reduced motion gets.
- The guide describes the app as it stands. When a setting is renamed in the
  launcher, rename it here.
