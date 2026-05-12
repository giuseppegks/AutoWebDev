// Coffeeshop Ketama — site interactions

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

// ---- Highlight today's row in opening hours ----
const todayMap = ['zo', 'ma', 'di', 'wo', 'do', 'vr', 'za'];
const today = todayMap[new Date().getDay()];
document.querySelectorAll(`.hours-row[data-day="${today}"]`).forEach((row) => {
  row.classList.add('is-today');
});

// ---- Today's hours in hero meta ----
// Hours: ma-za 10:00 — 01:00 (next day), zo 11:00 — 01:00 (next day)
(function todayHours() {
  const wrap = document.querySelector('[data-today]');
  if (!wrap) return;
  const label = wrap.querySelector('.t-label');
  const hours = wrap.querySelector('.t-hours');
  const day = new Date().getDay(); // 0=zo
  label.textContent = 'Vandaag open';
  if (day === 0) {
    hours.textContent = '11:00 — 01:00';
  } else {
    hours.textContent = '10:00 — 01:00';
  }
})();

// ---- Open status badge: are we open right now? ----
const statusBadge = document.querySelector('[data-open-status]');
if (statusBadge) {
  // Hours: ma–za 10:00 — 01:00 (next day), zo 11:00 — 01:00 (next day)
  const now = new Date();
  const day = now.getDay(); // 0=zo
  const minutesNow = now.getHours() * 60 + now.getMinutes();

  // Open if (today after open-time) OR (previous-day's session still running, i.e. before 01:00)
  const openToday = day === 0 ? 11 * 60 : 10 * 60;
  const closeEarly = 60; // 01:00
  // Yesterday's session always runs until 01:00 the next day
  const inLateNight = minutesNow < closeEarly; // 00:00-00:59 = still yesterday's session
  const inToday = minutesNow >= openToday && minutesNow <= 24 * 60 - 1;

  const isOpen = inLateNight || inToday;
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

// ---- Mailto reservation form (no backend, no storage) ----
document.querySelectorAll('[data-mailto-form]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const get = (n) => (form.elements[n]?.value || '').trim();
    const subject = `Reserveringsverzoek — ${get('naam')} (${get('personen')})`;
    const lines = [
      `Naam: ${get('naam')}`,
      `E-mail: ${get('email')}`,
      `Telefoon: ${get('telefoon') || '—'}`,
      `Datum & tijd: ${get('datum')}`,
      `Aantal personen: ${get('personen')}`,
      '',
      'Berichtje:',
      get('bericht') || '—',
      '',
      '— Verstuurd via billys.coffee'
    ];
    const body = lines.join('\n');
    const url = `mailto:info@billys.coffee?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = url;
  });
});

// ---- Menu slider + lightbox ----
(function initSlider() {
  const slider = document.querySelector('[data-slider]');
  if (!slider) return;

  const track = slider.querySelector('.slider__track');
  const slides = Array.from(track.querySelectorAll('.slider__slide'));
  const prevBtn = slider.querySelector('.slider__btn--prev');
  const nextBtn = slider.querySelector('.slider__btn--next');
  const dotsWrap = slider.parentElement.querySelector('.slider__dots');

  // Build dots
  const dots = slides.map((_, i) => {
    const b = document.createElement('button');
    b.className = 'slider__dot';
    b.type = 'button';
    b.setAttribute('aria-label', `Naar foto ${i + 1}`);
    b.addEventListener('click', () => goTo(i));
    dotsWrap.appendChild(b);
    return b;
  });

  let current = 0;

  function setActive(i) {
    current = i;
    dots.forEach((d, idx) => d.classList.toggle('is-active', idx === i));
  }
  setActive(0);

  function goTo(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    track.scrollTo({ left: slides[i].offsetLeft, behavior: 'smooth' });
  }

  prevBtn?.addEventListener('click', () => goTo(current - 1));
  nextBtn?.addEventListener('click', () => goTo(current + 1));

  // Sync dots with scroll
  let scrollTimer;
  track.addEventListener('scroll', () => {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => {
      const w = track.clientWidth;
      const i = Math.round(track.scrollLeft / w);
      setActive(i);
    }, 80);
  });

  // Lightbox
  const lightbox = document.getElementById('lightbox');
  if (!lightbox) return;
  const lbImg = lightbox.querySelector('.lightbox__img');
  const lbClose = lightbox.querySelector('.lightbox__close');
  const lbPrev = lightbox.querySelector('.lightbox__prev');
  const lbNext = lightbox.querySelector('.lightbox__next');
  const lbCounter = lightbox.querySelector('.lightbox__counter');
  let lbIdx = 0;

  const allImgs = slides.map((s) => s.querySelector('img'));

  function openLb(i) {
    lbIdx = i;
    showLb();
    lightbox.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    lbClose.focus();
  }
  function showLb() {
    const img = allImgs[lbIdx];
    lbImg.src = img.src;
    lbImg.alt = img.alt || '';
    lbCounter.textContent = `${lbIdx + 1} / ${allImgs.length}`;
  }
  function closeLb() {
    lightbox.classList.remove('is-open');
    document.body.style.overflow = '';
  }
  function next() { lbIdx = (lbIdx + 1) % allImgs.length; showLb(); }
  function prev() { lbIdx = (lbIdx - 1 + allImgs.length) % allImgs.length; showLb(); }

  slides.forEach((s, i) => {
    s.addEventListener('click', () => openLb(i));
    s.setAttribute('role', 'button');
    s.setAttribute('tabindex', '0');
    s.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(i); }
    });
  });

  lbClose.addEventListener('click', closeLb);
  lbPrev.addEventListener('click', prev);
  lbNext.addEventListener('click', next);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLb();
  });
  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('is-open')) return;
    if (e.key === 'Escape') closeLb();
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
  });
})();
