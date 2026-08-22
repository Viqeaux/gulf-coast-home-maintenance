/* =============================================================================
   The calendar feed buttons, shared by the home page and /calendars/.

   Split out of an inline block in index.html in 1.23.0, when the individual
   feed cards moved to their own page and two pages needed the same machinery.
   Same reasoning as site.css and theme.css: a thing two pages share cannot
   live inside one of them.

   Everything here is guarded by an existence check, so the file is safe on any
   page that loads it. The home page has the picker and the signup and no feed
   cards; the calendars page has the four cards and neither of the others; a
   page with no #calendars section at all returns immediately.

   The picker lives in here too rather than in index.html, because it calls
   renderActions and keeping them in one closure is simpler than exporting a
   function across files for one caller.
   ============================================================================= */

(function () {
    var COPY_LABEL = 'Copy feed URL';
    var calendars = document.getElementById('calendars');

    // The signup posts straight to MailerLite through a hidden frame,
    // so there is no library to load and the visitor never leaves the page. We
    // cannot read the response across origins, but the frame firing `load`
    // confirms the request completed, and double opt-in means the real
    // confirmation is the email they are about to get either way.
    //
    // Bound BEFORE the #calendars guard below, because since 1.29.0 the form
    // lives in the footer of pages that may carry no feed section at all.
    var signup = document.querySelector('.signup');
    if (signup) {
      signup.addEventListener('submit', function (event) {
        // Anything in the honeypot means this is not a person. Say nothing
        // about why: a bot that gets told it failed is a bot that gets fixed.
        var hp = signup.querySelector('input[name="website"]');
        if (hp && hp.value) {
          event.preventDefault();
          signup.hidden = true;
          document.querySelector('.signup-done').hidden = false;
          return;
        }
        // Disabled controls are not submitted, so MailerLite never sees a
        // parameter it has no field for.
        if (hp) { hp.disabled = true; }

        var sink = document.querySelector('iframe[name="ml-sink"]');
        var swap = function () {
          signup.hidden = true;
          document.querySelector('.signup-done').hidden = false;
        };
        sink.addEventListener('load', swap, { once: true });
        // If the frame never reports back, show it anyway rather than leaving
        // them staring at a form that looks like it did nothing.
        setTimeout(swap, 2500);
      });
    }

    // Everything below touches the feed section; a page without one is done.
    if (!calendars) { return; }

    // Both notices go in the same place, above the tier cards. The tag varies
    // because one of them is a disclosure: the preview warning is always worth
    // reading, the Android note only matters to the people it happens to.
    function notice(tag, className, html) {
      var el = document.createElement(tag);
      el.className = className;
      el.innerHTML = html;
      calendars.querySelector('.deck').insertAdjacentElement('afterend', el);
    }

    // Subscribe links are built from wherever this page is hosted, so the files
    // work on any domain without editing.
    //
    // Subscribing only works from a public HTTPS origin: Google fetches the .ics
    // from its own servers, so file://, localhost, and http:// are unreachable to
    // it. Rather than render a button that silently does nothing, say so.
    var local = /^(localhost|127\.0\.0\.1|\[::1\]|.*\.local)$/i.test(location.hostname);
    var publicHost = location.protocol === 'https:' && !local;

    if (!publicHost) {
      notice('div', 'preview-warning',
        '<strong>Preview only, subscribing won\'t work yet.</strong> ' +
        (/^https?:$/.test(location.protocol)
          ? 'This page is being served from ' + location.host + '.'
          : 'This page is open as a local file.') +
        ' Google fetches the calendar file from its own servers, so it has to be on a ' +
        'public <code>https://</code> address first. Download still works, and importing ' +
        'a downloaded file is a good way to check the events read correctly.');
    }

    // Android can route calendar.google.com links into the Google Calendar app,
    // which has no way to subscribe to a URL. The app just opens and sits
    // there. It depends on a per-device "open supported links" setting, so it
    // hits some Android users and not others, and neither we nor they can tell
    // in advance.
    //
    // A closed disclosure rather than an open card. How often interception
    // actually happens is still unmeasured, so this was a paragraph of
    // troubleshooting sitting on top of the buttons for every Android visitor,
    // most of whom never needed it. Collapsed, it costs one line and is still
    // right there at the moment someone taps a button and nothing happens.
    // If it turns out to be common, promote it back.
    if (publicHost && /android/i.test(navigator.userAgent)) {
      notice('details', 'android-note',
        '<summary>On Android and nothing happened? Tap here.</summary>' +
        '<p>Google Calendar can claim the link, and the app itself cannot ' +
        'subscribe to a calendar. This route always works:</p>' +
        '<ol>' +
          '<li>Tap <strong>' + COPY_LABEL + '</strong> on the tier you want.</li>' +
          '<li>Open <a href="https://calendar.google.com/calendar/u/0/r/settings/addbyurl" ' +
            'target="_blank" rel="noopener">Google Calendar’s add-by-URL page</a>.</li>' +
          '<li>Paste it in and tap <strong>Add calendar</strong>.</li>' +
        '</ol>');
    }

    // The feeds live at the site root, so the base is the origin, never the
    // current page's directory. Deriving it from location.href broke every
    // button on /calendars/ from 1.22.0 until 1.29.0: on that page the
    // "relative" base resolved to /calendars/gulf-coast-*.ics, which 404s.
    // Nobody reported it, which says more about the traffic than the bug.
    var base = location.origin + '/';
    var bare = base.replace(/^https?:\/\//, '');

    // Built as nodes rather than as an HTML string. Every address here is
    // derived from location.href, so string concatenation would be putting a
    // value nobody controls inside a quoted attribute. It is not reachable on
    // GitHub Pages, which 404s any path that is not a real file, but the whole
    // point of building it this way is that it stops depending on the host.
    function tierLink(className, href, text, newTab) {
      var a = document.createElement('a');
      a.className = className;
      a.href = href;
      a.textContent = text;
      if (newTab) { a.target = '_blank'; a.rel = 'noopener'; }
      return a;
    }

    // Named rather than inline, because the picker below re-renders one of
    // these boxes every time a checkbox moves.
    function renderActions(box) {
      var file = box.getAttribute('data-file');
      var feed = base + file;
      var webcal = 'webcal://' + bare + file;

      box.textContent = '';

      if (publicHost) {
        box.appendChild(tierLink('btn btn--primary',
          'https://calendar.google.com/calendar/u/0/r?cid=' + encodeURIComponent(webcal),
          'Add to Google Calendar', true));
        box.appendChild(tierLink('btn', webcal, 'Subscribe (Apple / Outlook)'));
      }

      var download = tierLink('btn' + (publicHost ? '' : ' btn--primary'),
                              feed, 'Download .ics');
      download.setAttribute('download', '');
      box.appendChild(download);

      var copy = document.createElement('button');
      copy.className = 'btn';
      copy.type = 'button';
      copy.setAttribute('data-url', feed);
      copy.textContent = COPY_LABEL;
      box.appendChild(copy);
    }

    document.querySelectorAll('.actions[data-file]').forEach(renderActions);

    // --- the picker -------------------------------------------------------
    // Mirrors combo_file() in build_calendars.py: the order is fixed, and one
    // ticked box resolves to that feed's own file rather than to a combination
    // of one. If those two ever disagree the picker hands out a 404, so they
    // are written to look alike on purpose.
    var PICKER_ORDER = ['must', 'should', 'above', 'monthly'];
    var PICKER_SINGLE = {
      must: 'gulf-coast-must-do.ics',
      should: 'gulf-coast-should-do.ics',
      above: 'gulf-coast-going-above.ics',
      monthly: 'gulf-coast-monthly-rounds.ics'
    };
    var PICKER_LABEL = {
      must: 'Must Do',
      should: 'Should Do',
      above: 'Going Above',
      monthly: 'Monthly Rounds'
    };
    var PICKER_COUNT = { must: 12, should: 12, above: 12, monthly: 84 };

    var picker = document.querySelector('.picker');
    if (picker) {
      var pickerBox = picker.querySelector('.actions');
      var pickerSummary = picker.querySelector('.picker-summary');

      function pickerUpdate() {
        var chosen = PICKER_ORDER.filter(function (key) {
          var input = picker.querySelector('input[value="' + key + '"]');
          return input && input.checked;
        });

        if (!chosen.length) {
          pickerBox.textContent = '';
          pickerSummary.textContent = 'Tick at least one to get a calendar.';
          return;
        }

        var file = chosen.length === 1
          ? PICKER_SINGLE[chosen[0]]
          : 'gulf-coast-' + chosen.join('-') + '.ics';

        var total = 0;
        chosen.forEach(function (key) { total += PICKER_COUNT[key]; });
        var names = chosen.map(function (key) { return PICKER_LABEL[key]; });

        pickerSummary.textContent = '';
        pickerSummary.appendChild(document.createTextNode('One calendar: '));
        var strong = document.createElement('strong');
        strong.textContent = names.join(', ');
        pickerSummary.appendChild(strong);
        pickerSummary.appendChild(document.createTextNode(
          '. About ' + total + ' reminders a year.'));

        pickerBox.setAttribute('data-file', file);
        renderActions(pickerBox);
      }

      picker.addEventListener('change', pickerUpdate);
      pickerUpdate();
    }

    // The two subscribe buttons only cover Google and apps that register the
    // webcal:// handler. Everything else (Outlook on the web, Thunderbird,
    // Proton) wants an https:// feed address pasted into a box, so hand it over
    // directly rather than making people dig it out of the download link.
    //
    // One delegated listener rather than one per button, so it keeps working no
    // matter how many tiers the page grows.
    calendars.addEventListener('click', function (event) {
      var btn = event.target.closest('button[data-url]');
      if (!btn) { return; }
      var url = btn.getAttribute('data-url');

      function done(ok) {
        btn.textContent = ok ? 'Copied' : 'Press Ctrl+C';
        btn.classList.add('btn--copied');
        // Clear any pending reset first: without this, a second click inherits
        // the first timer and the label snaps back early.
        clearTimeout(btn._resetTimer);
        btn._resetTimer = setTimeout(function () {
          btn.textContent = COPY_LABEL;
          btn.classList.remove('btn--copied');
        }, 2000);
      }

      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = url;
        ta.setAttribute('readonly', '');
        ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
        document.body.removeChild(ta);
        if (ok) { done(true); } else { window.prompt('Copy this feed address:', url); done(false); }
      }

      // navigator.clipboard needs a secure context and can still be refused by
      // permissions policy, so fall back to a selected textarea, and finally to
      // a prompt the user can copy out of by hand.
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { done(true); }, fallback);
      } else {
        fallback();
      }
    });
  })();
