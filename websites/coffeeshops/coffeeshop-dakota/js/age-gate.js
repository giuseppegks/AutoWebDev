// Dakota — 18+ age gate
// Toont op eerste pageload, slaat keuze op in localStorage.
(function ageGate() {
  var KEY = 'dakota-age-verified';
  try {
    if (localStorage.getItem(KEY) === 'yes') return;
  } catch (e) { /* private mode — show gate */ }

  function build() {
    var overlay = document.createElement('div');
    overlay.className = 'age-gate';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'ageGateTitle');
    overlay.innerHTML = [
      '<div class="age-gate__card">',
        '<div class="age-gate__badge">18+</div>',
        '<h2 class="age-gate__title" id="ageGateTitle">Welkom bij <em>Dakota</em>.</h2>',
        '<p class="age-gate__text">Onze deuren staan open voor bezoekers van <strong>18 jaar of ouder</strong>. Voordat je verder gaat, vragen we je je leeftijd te bevestigen.</p>',
        '<div class="age-gate__actions">',
          '<button type="button" class="btn btn--primary" data-age-yes>Ja, ik ben 18 of ouder</button>',
          '<button type="button" class="btn btn--ghost" data-age-no>Nee</button>',
        '</div>',
        '<p class="age-gate__fine">Identificatie verplicht bij bezoek aan de coffeeshop. Door verder te gaan ga je akkoord met onze huisregels.</p>',
      '</div>'
    ].join('');
    document.body.appendChild(overlay);
    document.body.classList.add('age-locked');

    var yes = overlay.querySelector('[data-age-yes]');
    var no = overlay.querySelector('[data-age-no]');

    yes.addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'yes'); } catch (e) { /* ignore */ }
      overlay.remove();
      document.body.classList.remove('age-locked');
    });

    no.addEventListener('click', function () {
      overlay.classList.add('is-denied');
      overlay.querySelector('.age-gate__card').innerHTML = [
        '<div class="age-gate__badge">18+</div>',
        '<h2 class="age-gate__title">Sorry — <em>te jong.</em></h2>',
        '<p class="age-gate__text">Deze website is alleen toegankelijk voor bezoekers van 18 jaar of ouder. Kom gerust later nog eens terug.</p>',
        '<div class="age-gate__actions">',
          '<a class="btn btn--ghost" href="https://www.google.com">Verlaat de site</a>',
        '</div>'
      ].join('');
    });

    yes.focus();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
