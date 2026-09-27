/* ============================================================================
   Feedback, from the top of every page.

   A "Feedback" button in the header opens a small form in a dialog. It posts
   to Orbital's own forms server, which emails OrbitalLauncher@gmail.com and
   takes feedback from each visitor once every three days; past that it answers
   429 with the hours left, and the form says when to come back. The same form
   also lives on feedback.html for anybody who arrives there directly.
   ========================================================================== */

(function () {
  'use strict';

  var ENDPOINT = 'https://forms.orbitallauncher.com/send';
  var PUBLIC = 'OrbitalLauncher@gmail.com';

  function whenBack(hours) {
    if (!hours || hours <= 1) return 'in about an hour';
    if (hours < 24) return 'in about ' + hours + ' hours';
    var days = Math.round(hours / 24);
    return 'in about ' + days + (days === 1 ? ' day' : ' days');
  }

  var dialog = document.createElement('dialog');
  dialog.className = 'fbd';
  dialog.setAttribute('aria-labelledby', 'fbd-title');
  dialog.innerHTML =
    '<form class="fbd-form" method="dialog">' +
    '<div class="fbd-head"><h2 id="fbd-title">Send feedback</h2>' +
    '<button type="button" class="fbd-x" aria-label="Close">&times;</button></div>' +
    '<p class="fbd-lede">Ideas, something that isn\'t working, or a question. Every message is read.</p>' +
    '<fieldset class="seg"><legend>What is it about?</legend><div class="seg-opts">' +
    '<label><input type="radio" name="kind" value="Idea" checked><span>An idea</span></label>' +
    '<label><input type="radio" name="kind" value="Something isn\'t working"><span>Something isn\'t working</span></label>' +
    '<label><input type="radio" name="kind" value="Question"><span>A question</span></label>' +
    '<label><input type="radio" name="kind" value="Other"><span>Something else</span></label>' +
    '</div></fieldset>' +
    '<label class="fb-field"><span>Your message</span>' +
    '<textarea name="message" rows="5" required maxlength="5000" placeholder="What\'s on your mind?"></textarea></label>' +
    '<label class="fb-field"><span>Your email <em>so you can get a reply</em></span>' +
    '<input type="email" name="email" required autocomplete="email" spellcheck="false" placeholder="you@example.com"></label>' +
    '<input type="hidden" name="_subject" value="Orbital feedback">' +
    '<input class="sr-only" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">' +
    '<div class="fbd-foot"><button type="submit" class="btn">Send feedback</button>' +
    '<span class="fbd-note small muted">This form is rate limited to prevent spam.</span></div>' +
    '<p class="fbd-said small" role="status" aria-live="polite"></p>' +
    '</form>';

  var form = dialog.querySelector('form');
  var said = dialog.querySelector('.fbd-said');
  var sendBtn = form.querySelector('button[type="submit"]');

  function say(words, good) {
    said.textContent = words;
    said.classList.toggle('is-good', !!good);
  }

  function open() {
    if (!dialog.isConnected) document.body.appendChild(dialog);
    say('');
    if (dialog.showModal) dialog.showModal(); else dialog.setAttribute('open', '');
    var first = form.querySelector('textarea');
    if (first) first.focus();
  }

  function close() {
    if (dialog.close) dialog.close(); else dialog.removeAttribute('open');
  }

  dialog.querySelector('.fbd-x').addEventListener('click', close);
  dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    sendBtn.disabled = true;
    say('Sending…');
    fetch(ENDPOINT, {
      method: 'POST',
      body: new URLSearchParams(new FormData(form)),
      headers: { Accept: 'application/json' },
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (res.status === 429) {
          say("You've already sent feedback recently. You can send more " + whenBack(data.retryHours) + '.');
          return;
        }
        if (!res.ok) throw new Error('rejected');
        form.reset();
        say('Thank you! Your feedback has been sent.', true);
        setTimeout(close, 2200);
      });
    }).catch(function () {
      said.textContent = '';
      said.classList.remove('is-good');
      said.appendChild(document.createTextNode("That didn't go through. You can email "));
      var a = document.createElement('a');
      a.href = 'mailto:' + PUBLIC + '?subject=' + encodeURIComponent('Orbital feedback');
      a.textContent = PUBLIC;
      said.appendChild(a);
      said.appendChild(document.createTextNode(' instead.'));
    }).then(function () { sendBtn.disabled = false; });
  });

  function addButton() {
    var nav = document.querySelector('.top nav') || document.querySelector('.site-top nav');
    if (!nav || nav.querySelector('.fb-open')) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'fb-open';
    btn.textContent = 'Feedback';
    btn.addEventListener('click', open);
    var mode = nav.querySelector('.mode-btn');
    var cta = nav.querySelector('.nav-cta');
    nav.insertBefore(btn, mode || cta || null);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addButton);
  else addButton();

  /* A link to #feedback anywhere on the site opens the form too. */
  if (location.hash === '#feedback') open();
  window.addEventListener('hashchange', function () { if (location.hash === '#feedback') open(); });
})();
