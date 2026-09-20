/* ============================================================================
   Asking to be a tester.

   A static site cannot send email, so the form posts to a form service and the
   service forwards it. Formspree is the one it is written for: make a form
   there against alid0ndev@gmail.com and paste its id into the form's `action`
   in index.html, in place of PASTE_FORM_ID.

   Until that is done the form does not pretend to work. It says what is missing
   and offers the one thing that needs no service at all — a mail to the same
   address, composed in whatever the visitor writes mail in. That is deliberate:
   a form that swallows an address and delivers it nowhere is worse than no form,
   because the person leaves believing they have signed up.
   ========================================================================== */

(function () {
  'use strict';

  var form = document.getElementById('ask');
  var said = document.getElementById('ask-said');
  if (!form || !said) return;

  var WHERE_TO = 'alid0ndev@gmail.com';
  var UNSET = 'PASTE_FORM_ID';

  function say(words, good) {
    said.textContent = words;
    said.classList.toggle('is-good', !!good);
  }

  /** The way out that needs nothing set up: the visitor's own mail client. */
  function offerMail(address) {
    said.textContent = '';
    var line = document.createElement('span');
    line.textContent = 'Could not send that from here. ';
    var link = document.createElement('a');
    link.href = 'mailto:' + WHERE_TO +
      '?subject=' + encodeURIComponent('Orbital tester signup') +
      '&body=' + encodeURIComponent('I would like to test Orbital Launcher.\n\n' + (address || ''));
    link.textContent = 'Send it as an email instead';
    said.appendChild(line);
    said.appendChild(link);
    said.classList.remove('is-good');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    var address = (form.elements.email && form.elements.email.value || '').trim();
    if (!address) return;

    if (form.action.indexOf(UNSET) >= 0) {
      offerMail(address);
      return;
    }

    var button = form.querySelector('button');
    if (button) button.disabled = true;
    say('Sending…');

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' },
    }).then(function (answer) {
      if (!answer.ok) throw new Error('rejected');
      form.reset();
      say('Thank you. You will get an email with the download.', true);
    }).catch(function () {
      offerMail(address);
    }).then(function () {
      if (button) button.disabled = false;
    });
  });
})();
