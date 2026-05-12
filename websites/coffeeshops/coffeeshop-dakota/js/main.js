// Coffeeshop Dakota — site interactions

// ---- Sticky-header shadow on scroll ----
const header = document.querySelector('.site-header');
if (header) {
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 12);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

// ---- Mobile nav drawer ----
const toggle = document.querySelector('.nav__toggle');
const menu = document.querySelector('.nav__menu');

if (toggle && menu) {
  const setOpen = (open) => {
    menu.classList.toggle('is-open', open);
    toggle.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  };
  toggle.addEventListener('click', () => {
    const isOpen = menu.classList.contains('is-open');
    setOpen(!isOpen);
  });
  menu.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => setOpen(false));
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });
}

// Dakota hours: dagelijks 09:00 — 00:00
const OPEN_MIN = 9 * 60;       // 09:00
const CLOSE_MIN = 24 * 60;     // 24:00 (midnight)

// ---- Highlight today's row in opening hours ----
const todayMap = ['zo', 'ma', 'di', 'wo', 'do', 'vr', 'za'];
const today = todayMap[new Date().getDay()];
document.querySelectorAll(`.hours-row[data-day="${today}"]`).forEach((row) => {
  row.classList.add('is-today');
});

// ---- Today's hours in hero meta ----
(function todayHours() {
  const wrap = document.querySelector('[data-today]');
  if (!wrap) return;
  const label = wrap.querySelector('.t-label');
  const hours = wrap.querySelector('.t-hours');
  if (label) label.textContent = 'Vandaag open';
  if (hours) hours.textContent = '09:00 — 00:00';
})();

// ---- Open status badge ----
const statusBadge = document.querySelector('[data-open-status]');
if (statusBadge) {
  const now = new Date();
  const minutesNow = now.getHours() * 60 + now.getMinutes();
  const isOpen = minutesNow >= OPEN_MIN && minutesNow < CLOSE_MIN;
  const dot = statusBadge.querySelector('.dot');
  const txt = statusBadge.querySelector('.txt');
  if (txt && dot) {
    if (isOpen) {
      txt.textContent = 'Nu geopend';
      dot.style.background = '#4ade80';
      dot.style.boxShadow = '0 0 0 4px rgba(74,222,128,0.18)';
    } else {
      txt.textContent = 'Nu gesloten';
      dot.style.background = '#9ca3af';
      dot.style.boxShadow = '0 0 0 4px rgba(156,163,175,0.18)';
    }
  }
}

// ---- Reveal-on-scroll ----
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window && reveals.length) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('is-in'));
}

// ---- Year in footer ----
document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// ---- Mailto contact form (no backend, no storage) ----
document.querySelectorAll('[data-mailto-form]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const get = (n) => (form.elements[n]?.value || '').trim();
    const subject = `Bericht via website — ${get('naam')}`;
    const lines = [
      `Naam: ${get('naam')}`,
      `E-mail: ${get('email')}`,
      `Telefoon: ${get('telefoon') || '—'}`,
      '',
      'Bericht:',
      get('bericht') || '—',
      '',
      '— Verstuurd via coffeeshop-dakota.vercel.app'
    ];
    const body = lines.join('\n');
    const url = `mailto:info@coffeeshopdakota.nl?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = url;
  });
});
