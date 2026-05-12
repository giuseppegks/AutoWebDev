/* Coffeeshop Ketama — 18+ Age Gate */
(function () {
  var STORAGE_KEY = 'ketama_age_confirmed';
  var REDIRECT_URL = 'https://www.google.com/';

  function hasConfirmed() {
    try { return localStorage.getItem(STORAGE_KEY) === 'yes'; }
    catch (e) { return false; }
  }

  function setConfirmed() {
    try { localStorage.setItem(STORAGE_KEY, 'yes'); } catch (e) {}
  }

  function buildGate() {
    var gate = document.createElement('div');
    gate.className = 'age-gate';
    gate.setAttribute('role', 'dialog');
    gate.setAttribute('aria-modal', 'true');
    gate.setAttribute('aria-labelledby', 'ageGateTitle');
    gate.innerHTML = ''
      + '<div class="age-gate__card">'
      +   '<span class="age-gate__eyebrow">18+ alleen</span>'
      +   '<h2 class="age-gate__title" id="ageGateTitle">Ben je 18 jaar of ouder?</h2>'
      +   '<p class="age-gate__body">Coffeeshop Ketama is alleen toegankelijk voor volwassenen van 18 jaar en ouder. Een geldig ID is verplicht in onze zaak.</p>'
      +   '<div class="age-gate__actions">'
      +     '<button type="button" class="age-gate__btn age-gate__btn--yes" data-age-yes>Ja, ik ben 18+</button>'
      +     '<button type="button" class="age-gate__btn age-gate__btn--no" data-age-no>Nee</button>'
      +   '</div>'
      +   '<p class="age-gate__note">Door op "Ja" te klikken bevestig je dat je 18 jaar of ouder bent.</p>'
      + '</div>';
    return gate;
  }

  function dismiss(gate) {
    setConfirmed();
    gate.classList.add('is-leaving');
    setTimeout(function () {
      if (gate && gate.parentNode) gate.parentNode.removeChild(gate);
      document.body.classList.remove('age-locked');
    }, 380);
  }

  function init() {
    if (hasConfirmed()) return;
    document.body.classList.add('age-locked');
    var gate = buildGate();
    document.body.appendChild(gate);
    gate.querySelector('[data-age-yes]').addEventListener('click', function () { dismiss(gate); });
    gate.querySelector('[data-age-no]').addEventListener('click', function () { window.location.href = REDIRECT_URL; });
    // Trap focus minimally
    var yesBtn = gate.querySelector('[data-age-yes]');
    if (yesBtn) yesBtn.focus();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
