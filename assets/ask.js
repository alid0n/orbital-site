/* ============================================================================
   Sending a form: asking to be a tester, and feedback.

   A static site cannot send email, so each form posts to a form service and
   the service forwards it. That service is Formspree, and each form's endpoint
   is its `action`; submissions arrive as mail. The address they arrive at lives
   only in the Formspree account, never in this site, so nobody reading the page
   or its source can find it.

   Any form marked data-send is handled here. data-said names the element that
   reports back, and data-thanks is what it says when the post succeeds. If the
   post fails — the service down, the month's quota spent, no network — the page
   says so, keeps what was typed, and offers the same message as an email to
   Orbital's public address instead.
   ========================================================================== */

(function () {
  'use strict';

  var WHERE_TO = 'OrbitalLauncher@gmail.com';
  var forms = document.querySelectorAll('form[data-send]');

  Array.prototype.forEach.call(forms, function (form) {
    var said = document.getElementById(form.getAttribute('data-said'));
    if (!said) return;

    function say(words, good) {
      said.textContent = words;
      said.classList.toggle('is-good', !!good);
    }

    /* The way out that needs nothing from the service: the visitor's own mail
       app, with what they typed already in it. */
    function offerMail() {
      var subject = (form.elements._subject && form.elements._subject.value) || 'Orbital';
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.name.charAt(0) === '_' || !el.value) return;
        if ((el.type === 'radio' || el.type === 'checkbox') && !el.checked) return;
        lines.push(el.name === 'message' ? el.value : el.name + ': ' + el.value);
      });
      said.textContent = '';
      said.classList.remove('is-good');
      var line = document.createElement('span');
      line.textContent = "That didn't go through. ";
      var link = document.createElement('a');
      link.href = 'mailto:' + WHERE_TO + '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n\n'));
      link.textContent = 'Send it as an email instead';
      said.appendChild(line);
      said.appendChild(link);
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var button = form.querySelector('button[type="submit"]');
      if (button) button.disabled = true;
      say('Sending…');

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      }).then(function (answer) {
        if (!answer.ok) throw new Error('rejected');
        form.reset();
        say(form.getAttribute('data-thanks') || 'Thank you!', true);
      }).catch(function () {
        offerMail();
      }).then(function () {
        if (button) button.disabled = false;
      });
    });
  });
})();
