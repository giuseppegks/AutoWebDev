/* =====================================================
   THE GLOBAL BEAUTYBAR — main.js
   Editorial nails salon, Nijmegen. Forked from the Aurora
   massage template; adapted to a single-artist nails studio
   with Cal.com booking.
   ===================================================== */

// ---------- CONFIG ---------------------------------------------------
const SHOP = {
  name: "The Global Beautybar",
  fullName: "The Global Beautybar Nijmegen",
  phone: "+31634565653",
  phoneDisplay: "06 34 56 56 53",
  whatsapp: "31634565653",
  email: "bichhao_pham@hotmail.com",
  address: "Zwanenveld 8403, 6538 TL Nijmegen",
  timezone: "Europe/Amsterdam",
  language: "nl",
  instagram: "https://www.instagram.com/theglobalbeautybar",
};

// 0 = Sun ... 6 = Sat. [openHour, closeHour] 24h local. Verified from
// Salonized site (May 2026). Sunday closed.
const SHOP_HOURS = {
  1: [12, 18],
  2: [10, 18],
  3: [10, 18],
  4: [10, 18],
  5: [10, 18],
  6: [10, 18],
};

const SLOT_STEP = 30;

// Service catalog. Keys MUST match Cal.com event-type slugs (see README).
// Verified from https://the-global-beautybar.salonized.com/services (May 2026).
const SERVICES = {
  // ---- Acryl
  "acryl-naturel-nieuw":     { label: "Acryl naturel roze · nieuwe set", cat: "Acryl",    duration: 60, price: 45 },
  "acryl-naturel-opvullen":  { label: "Acryl naturel roze · opvullen",   cat: "Acryl",    duration: 60, price: 40 },
  "acryl-gellak-nieuw":      { label: "Acryl met gellak · nieuwe set",   cat: "Acryl",    duration: 60, price: 50 },
  "acryl-gellak-opvullen":   { label: "Acryl met gellak · opvullen",     cat: "Acryl",    duration: 60, price: 45 },
  "acryl-babyboom-nieuw":    { label: "Acryl babyboom · nieuwe set",     cat: "Acryl",    duration: 60, price: 55 },
  "acryl-babyboom-opvullen": { label: "Acryl babyboom · opvullen",       cat: "Acryl",    duration: 60, price: 50 },
  "acryl-french-nieuw":      { label: "Acryl french · nieuwe set",       cat: "Acryl",    duration: 60, price: 55 },
  "acryl-french-opvullen":   { label: "Acryl french · opvullen",         cat: "Acryl",    duration: 60, price: 50 },
  // ---- BIAB
  "biab-naturel-nieuw":      { label: "BIAB naturel roze · nieuwe set",  cat: "BIAB",     duration: 60, price: 50 },
  "biab-naturel-opvullen":   { label: "BIAB naturel roze · opvullen",    cat: "BIAB",     duration: 60, price: 45 },
  "biab-gellak-nieuw":       { label: "BIAB met gellak · nieuwe set",    cat: "BIAB",     duration: 60, price: 55 },
  "biab-gellak-opvullen":    { label: "BIAB met gellak · opvullen",      cat: "BIAB",     duration: 60, price: 50 },
  "biab-french-nieuw":       { label: "BIAB french · nieuwe set",        cat: "BIAB",     duration: 60, price: 60 },
  "biab-french-opvullen":    { label: "BIAB french · opvullen",          cat: "BIAB",     duration: 60, price: 55 },
  // ---- Manicure
  "mani-knippen":            { label: "Knippen en vijlen",               cat: "Manicure", duration: 15, price: 10 },
  "mani-klassiek":           { label: "Manicure",                        cat: "Manicure", duration: 30, price: 15 },
  "mani-gellak":             { label: "Gellak",                          cat: "Manicure", duration: 30, price: 30 },
  "mani-gellak-french":      { label: "Gellak french",                   cat: "Manicure", duration: 45, price: 35 },
  "mani-gellak-met-verw":    { label: "Gellak met verwijderen",          cat: "Manicure", duration: 45, price: 32.5 },
  "mani-met-gellak":         { label: "Manicure met gellak",             cat: "Manicure", duration: 45, price: 35 },
  // ---- Pedicure
  "pedi-knippen":            { label: "Knippen en vijlen",               cat: "Pedicure", duration: 15, price: 10 },
  "pedi-spa":                { label: "Spa pedicure",                    cat: "Pedicure", duration: 30, price: 40 },
  "pedi-spa-gellak":         { label: "Spa pedicure met gellak",         cat: "Pedicure", duration: 60, price: 50 },
  "pedi-spa-french":         { label: "Spa pedicure met french",         cat: "Pedicure", duration: 60, price: 55 },
  "pedi-gellak":             { label: "Gellak",                          cat: "Pedicure", duration: 30, price: 30 },
  "pedi-gellak-french":      { label: "Gellak french",                   cat: "Pedicure", duration: 30, price: 35 },
  "pedi-gellak-met-verw":    { label: "Gellak verwijderen en gellak",    cat: "Pedicure", duration: 30, price: 32.5 },
  // ---- Extras
  "extra-reparatie":         { label: "Reparatie (vanaf)",               cat: "Extras",   duration: 15, price: 3 },
  "extra-nailart":           { label: "Nailart (vanaf, per nagel)",      cat: "Extras",   duration: 15, price: 2 },
  "extra-verw-gellak":       { label: "Verwijderen gellak",              cat: "Extras",   duration: 15, price: 10 },
  "extra-verw-biab":         { label: "Verwijderen BIAB / Acryl",        cat: "Extras",   duration: 30, price: 15 },
};

// Ordered category list — used by HTML grouping + step 1 of the modal.
const SERVICE_CATEGORIES = ["Acryl", "BIAB", "Manicure", "Pedicure", "Extras"];

// Booking variant: "cal" → POST /api/bookings (Cal.com proxy).
const BOOKING_MODE = "cal";
const BOOKING_ENDPOINT = "/api/bookings";

// How far ahead to allow booking (days)
const BOOKING_HORIZON_DAYS = 60;

// Cache-bust version. Bump when you replace an asset's contents at the
// same path — vercel.json sets immutable Cache-Control on .jpg/.mp4.
const CACHE_BUST = "v=1";
const cb = (u) => (u && !u.includes("?") ? `${u}?${CACHE_BUST}` : u);

// ---------- DOM HELPERS ---------------------------------------------
const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const on = (el, ev, fn, opts) => el && el.addEventListener(ev, fn, opts);
const fmtDate = (d) => d.toISOString().slice(0, 10);
const sameDay = (a, b) => a.toDateString() === b.toDateString();

// ---------- FOOTER YEAR ----------------------------------------------
$("#year") && ($("#year").textContent = new Date().getFullYear());

// ---------- NAV ------------------------------------------------------
const nav = $("#nav");
const onScroll = () => nav.classList.toggle("is-scrolled", window.scrollY > 8);
on(window, "scroll", onScroll, { passive: true });
onScroll();

const burger = $(".nav__burger");
on(burger, "click", () => {
  const open = nav.classList.toggle("is-open");
  burger.setAttribute("aria-expanded", open ? "true" : "false");
});
$$(".nav__links a").forEach((a) =>
  on(a, "click", () => {
    nav.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
  }),
);

// ---------- BACKGROUND-IMAGE HYDRATION -------------------------------
// Set backgroundImage directly — bulletproof. Some CSS interactions
// in the full page were swallowing the var(--img) approach.
// All URLs are cache-busted so replaced asset contents are picked up
// despite the immutable Cache-Control header in vercel.json.
$$("[data-img]").forEach((el) => {
  const src = el.getAttribute("data-img");
  if (!src) return;
  el.style.backgroundImage = `url("${cb(src)}")`;
  el.style.backgroundSize = "cover";
  el.style.backgroundPosition = "center";
  el.style.backgroundRepeat = "no-repeat";
});

// ---------- REVEAL ON SCROLL -----------------------------------------
// Soft fade-in for elements marked .reveal — premium feel without animation overload.
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -10% 0px" },
  );
  $$(".reveal").forEach((el) => io.observe(el));
} else {
  // Fallback: just show everything if IO isn't available
  $$(".reveal").forEach((el) => el.classList.add("is-in"));
}

// ---------- HERO VIDEO ROTATOR --------------------------------------
// Each clip plays through ONCE, then advances to the next.
// Robust pattern:
//   - All videos preload="metadata" so duration is known up-front.
//   - When a clip becomes active: set currentTime=0, call play().
//   - Advance trigger = ended event + a duration-based timeout fallback,
//     because ended doesn't fire reliably across all browsers/codecs.
const heroVideos = $$(".hero__video");
if (heroVideos.length) {
  heroVideos.forEach((v) => {
    const src = v.getAttribute("data-src");
    if (src) {
      v.src = cb(src);
      v.preload = "metadata";  // override any preload="none" so we know duration
      v.load();
    }
  });

  let idx = 0;
  let advanceTimer = null;

  const scheduleAdvanceFallback = (cur) => {
    clearTimeout(advanceTimer);
    // Optional cap: data-max-seconds="2" trims a clip to ≤ 2s before advancing.
    const cap = parseFloat(cur.getAttribute("data-max-seconds") || "0");
    const arm = () => {
      const natural = isFinite(cur.duration) && cur.duration > 0 ? cur.duration : 5;
      const target = cap > 0 ? Math.min(natural, cap) : natural;
      advanceTimer = setTimeout(next, (target + 0.15) * 1000);
    };
    if (cur.readyState >= 1 /* HAVE_METADATA */) arm();
    else cur.addEventListener("loadedmetadata", arm, { once: true });
  };

  const next = () => {
    clearTimeout(advanceTimer);
    const prev = heroVideos[idx];
    prev.classList.remove("is-active");
    prev.pause();

    idx = (idx + 1) % heroVideos.length;
    const cur = heroVideos[idx];
    cur.classList.add("is-active");
    try { cur.currentTime = 0; } catch (_) { /* may not be seekable yet */ }
    const p = cur.play();
    if (p && typeof p.catch === "function") p.catch(() => {});
    scheduleAdvanceFallback(cur);
  };

  // Advance on natural end of any clip
  heroVideos.forEach((v) => on(v, "ended", next));
  // Arm initial fallback for the first clip too
  scheduleAdvanceFallback(heroVideos[0]);
}

// ---------- BOOKING MODAL --------------------------------------------
const modal = $("#book-modal");
const stepsList = $$(".book__steps li", modal);
const stepSections = $$(".book__step", modal);
const btnNext = $("#book-next");
const btnBack = $("#book-back");
const btnSubmit = $("#book-submit");

// Single-artist nails studio — no suite picker, no masseuse picker.
// Kept as empty objects so the inherited suite/masseuse JS no-ops
// safely if the HTML containers are absent.
const SUITES = {};

const state = {
  step: 1, // 1..4 then "confirm"
  service: null,
  suite: "",     // unused in nails build
  masseuse: "",  // unused in nails build
  date: null,    // Date object
  time: null,    // "HH:MM"
  formData: null,
  eventTypes: null, // populated lazily from /api/event-types
};

// Accepts either a string (service slug) or an opts object:
//   openModal({ service: "acryl-french-nieuw" })
function openModal(serviceOrOpts) {
  const opts = typeof serviceOrOpts === "string"
    ? { service: serviceOrOpts }
    : (serviceOrOpts || {});

  state.service  = opts.service && SERVICES[opts.service] ? opts.service : null;
  state.suite    = (opts.suite && SUITES[opts.suite]) ? opts.suite : "";
  state.masseuse = (opts.masseuse && MASSEUSES_DATA[opts.masseuse]) ? opts.masseuse : "";
  state.date     = null;
  state.time     = null;
  // Always start at step 1 — even with prefill, the user may want to
  // adjust suite/masseuse before continuing.
  state.step     = 1;

  modal.hidden = false;
  document.body.style.overflow = "hidden";
  renderStep();
}

function closeModal() {
  modal.hidden = true;
  document.body.style.overflow = "";
  // reset state so a reopen starts fresh
  state.step = 1;
  state.service = null;
  state.suite = "";
  state.masseuse = "";
  state.date = null;
  state.time = null;
  $$(".book__service.is-selected", modal).forEach((b) => b.classList.remove("is-selected"));
  $$(".book__masseuse.is-selected", modal).forEach((b) => b.classList.remove("is-selected"));
  $$(".book__slot.is-selected", modal).forEach((b) => b.classList.remove("is-selected"));
  $$(".book__select[data-select='suite']", modal).forEach((sel) => setBookSelectValue(sel, ""));
  closeAllBookSelects();
  $("#book-form").reset();
}

$$("[data-open-book]").forEach((b) =>
  on(b, "click", () => openModal({
    service:  b.getAttribute("data-service")  || undefined,
    suite:    b.getAttribute("data-suite")    || undefined,
    masseuse: b.getAttribute("data-masseuse") || undefined,
  })),
);
$$("[data-close-book]").forEach((b) => on(b, "click", closeModal));
on(document, "keydown", (e) => {
  if (e.key === "Escape" && !modal.hidden) closeModal();
});

// Step 1: services
$$(".book__service").forEach((btn) =>
  on(btn, "click", () => {
    $$(".book__service").forEach((b) => b.classList.remove("is-selected"));
    btn.classList.add("is-selected");
    state.service = btn.getAttribute("data-service");
  }),
);

// Step 1: suites — custom dropdown (matches modal aesthetic; native
// <select> would inherit OS styling that breaks the dark theme).
function setBookSelectValue(sel, value) {
  const opts = $$(".book__select-option", sel);
  let label = "";
  opts.forEach((o) => {
    const match = (o.getAttribute("data-value") || "") === (value || "");
    o.classList.toggle("is-selected", match);
    if (match) label = o.textContent.trim();
  });
  const valueEl = $(".book__select-value", sel);
  if (valueEl && label) valueEl.textContent = label;
}
function closeAllBookSelects() {
  $$(".book__select.is-open").forEach((s) => {
    s.classList.remove("is-open");
    const t = $(".book__select-trigger", s);
    if (t) t.setAttribute("aria-expanded", "false");
  });
}
$$(".book__select").forEach((sel) => {
  const trigger = $(".book__select-trigger", sel);
  const which   = sel.getAttribute("data-select"); // "suite"

  on(trigger, "click", (e) => {
    e.stopPropagation();
    const wasOpen = sel.classList.contains("is-open");
    closeAllBookSelects();
    if (!wasOpen) {
      sel.classList.add("is-open");
      trigger.setAttribute("aria-expanded", "true");
    }
  });

  $$(".book__select-option", sel).forEach((opt) => {
    on(opt, "click", () => {
      const value = opt.getAttribute("data-value") || "";
      setBookSelectValue(sel, value);
      if (which === "suite") state.suite = value;
      closeAllBookSelects();
    });
  });
});
on(document, "click", (e) => {
  if (!e.target.closest(".book__select")) closeAllBookSelects();
});
on(document, "keydown", (e) => {
  if (e.key === "Escape") closeAllBookSelects();
});

// Step 2: calendar
function renderCalendar(monthOffset = 0) {
  const cal = $("#book-calendar");
  cal.innerHTML = "";

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const view = new Date(today.getFullYear(), today.getMonth() + monthOffset, 1);
  const month = view.toLocaleDateString("nl-NL", { month: "long", year: "numeric" });

  // header
  const head = document.createElement("div");
  head.className = "book__cal-head";
  head.innerHTML = `
    <button class="book__cal-nav" data-cal-prev aria-label="Vorige maand">‹</button>
    <span class="book__cal-title">${month}</span>
    <button class="book__cal-nav" data-cal-next aria-label="Volgende maand">›</button>
  `;
  cal.appendChild(head);

  // dow row (NL, Mon-first)
  ["Ma","Di","Wo","Do","Vr","Za","Zo"].forEach((d) => {
    const e = document.createElement("div");
    e.className = "book__cal-dow"; e.textContent = d;
    cal.appendChild(e);
  });

  // pad to Monday-first (Sunday=0 -> 6, Monday=1 -> 0, ..., Saturday=6 -> 5)
  const firstDow = (view.getDay() + 6) % 7;
  for (let i = 0; i < firstDow; i++) {
    const blank = document.createElement("div");
    cal.appendChild(blank);
  }

  const lastDay = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
  const horizon = new Date(today); horizon.setDate(horizon.getDate() + BOOKING_HORIZON_DAYS);

  for (let d = 1; d <= lastDay; d++) {
    const date = new Date(view.getFullYear(), view.getMonth(), d);
    const btn = document.createElement("button");
    btn.className = "book__day";
    btn.type = "button";
    btn.textContent = d;
    const isPast = date < today;
    const isClosed = !SHOP_HOURS[date.getDay()];
    const tooFar = date > horizon;
    if (isPast || isClosed || tooFar) btn.disabled = true;
    if (state.date && sameDay(date, state.date)) btn.classList.add("is-selected");
    on(btn, "click", () => {
      $$(".book__day.is-selected", cal).forEach((x) => x.classList.remove("is-selected"));
      btn.classList.add("is-selected");
      state.date = date;
    });
    cal.appendChild(btn);
  }

  on($("[data-cal-prev]", head), "click", () => {
    if (monthOffset > 0) renderCalendar(monthOffset - 1);
  });
  on($("[data-cal-next]", head), "click", () => renderCalendar(monthOffset + 1));
}

// Step 3: slots
function renderSlots() {
  const wrap = $("#book-slots");
  wrap.innerHTML = "";
  if (!state.date) {
    wrap.innerHTML = '<p class="book__hint">Kies eerst een datum.</p>';
    return;
  }
  const dow = state.date.getDay();
  const hours = SHOP_HOURS[dow];
  if (!hours) {
    wrap.innerHTML = '<p class="book__hint">Op deze dag zijn we gesloten.</p>';
    return;
  }
  const [start, end] = hours;
  // Saturday actually opens 10:30; bump to 11 for clean 30-min slots
  const startMin = (dow === 6 ? 11 : start) * 60;
  const endMin = end * 60;

  for (let m = startMin; m < endMin; m += SLOT_STEP) {
    const hh = String(Math.floor(m / 60)).padStart(2, "0");
    const mm = String(m % 60).padStart(2, "0");
    const t = `${hh}:${mm}`;
    const btn = document.createElement("button");
    btn.className = "book__slot"; btn.type = "button"; btn.textContent = t;
    if (state.time === t) btn.classList.add("is-selected");
    on(btn, "click", () => {
      $$(".book__slot.is-selected").forEach((x) => x.classList.remove("is-selected"));
      btn.classList.add("is-selected");
      state.time = t;
    });
    wrap.appendChild(btn);
  }
}

// Step navigation
function renderStep() {
  // pre-select service / suite / masseuse if openModal prefilled them
  if (state.service) {
    $$(".book__service").forEach((b) => {
      b.classList.toggle("is-selected", b.getAttribute("data-service") === state.service);
    });
  }
  $$(".book__select[data-select='suite']").forEach((sel) => setBookSelectValue(sel, state.suite));
  $$(".book__masseuse").forEach((b) => {
    b.classList.toggle("is-selected", (b.getAttribute("data-masseuse") || "") === state.masseuse);
  });

  // Update step indicators
  stepsList.forEach((li) => {
    const n = parseInt(li.getAttribute("data-step"), 10);
    li.classList.toggle("is-active", state.step === n);
    li.classList.toggle("is-done", state.step !== "confirm" && n < state.step);
  });

  // Show only active section
  stepSections.forEach((s) => {
    const k = s.getAttribute("data-step");
    s.classList.toggle("is-active", String(state.step) === String(k));
  });

  // Render dynamic content per step
  if (state.step === 2) renderCalendar();
  if (state.step === 3) renderSlots();

  // Footer button visibility
  const isConfirm = state.step === "confirm";
  btnBack.hidden = state.step === 1 || isConfirm;
  btnNext.hidden = isConfirm || state.step === 4;
  btnSubmit.hidden = state.step !== 4;
}

// Validate per step before advancing
function validateStep() {
  if (state.step === 1) {
    if (!state.service) { alert("Kies een behandeling."); return false; }
  } else if (state.step === 2) {
    if (!state.date) { alert("Kies een datum."); return false; }
  } else if (state.step === 3) {
    if (!state.time) { alert("Kies een tijd."); return false; }
  }
  return true;
}

on(btnNext, "click", () => {
  if (!validateStep()) return;
  state.step += 1;
  renderStep();
});
on(btnBack, "click", () => {
  if (state.step === "confirm") return;
  state.step -= 1;
  renderStep();
});

// Lazy-fetch Cal.com event types once per session. The map lets us
// translate our SERVICES slug → numeric eventTypeId expected by
// /api/bookings (Cal.com v2). Slugs MUST be created in Cal.com first;
// see README.
async function getEventTypes() {
  if (state.eventTypes) return state.eventTypes;
  try {
    const res = await fetch("/api/event-types");
    if (!res.ok) throw new Error("event-types " + res.status);
    const data = await res.json();
    const list = Array.isArray(data) ? data : (data.eventTypes || data.data || []);
    const map = {};
    list.forEach((et) => {
      if (et && et.slug) map[et.slug] = et.id;
    });
    state.eventTypes = map;
    return map;
  } catch (_) {
    state.eventTypes = {};
    return state.eventTypes;
  }
}

// Step 4 -> submit (Cal.com booking via /api/bookings proxy)
on(btnSubmit, "click", async () => {
  const form = $("#book-form");
  if (!form.reportValidity()) return;

  const svc = SERVICES[state.service];
  if (!svc) { alert("Kies eerst een behandeling."); return; }

  btnSubmit.disabled = true;
  btnSubmit.textContent = "Verzenden…";

  const eventTypes = await getEventTypes();
  const eventTypeId = eventTypes[state.service];

  const fd = new FormData(form);
  const [hh, mm] = state.time.split(":").map(Number);
  const startLocal = new Date(state.date);
  startLocal.setHours(hh, mm, 0, 0);

  const payload = {
    start: startLocal.toISOString(),
    eventTypeId: eventTypeId || null,
    serviceSlug: state.service,
    serviceLabel: svc.label,
    servicePrice: svc.price,
    serviceDuration: svc.duration,
    responses: {
      name: fd.get("name"),
      email: fd.get("email") || "",
      phone: fd.get("phone"),
      notes: fd.get("notes") || "",
    },
    metadata: {
      source: location.host,
      serviceCategory: svc.cat,
    },
    timeZone: SHOP.timezone,
    language: SHOP.language,
  };
  state.formData = payload;

  let serverOk = false;
  let serverMessage = "";
  try {
    const res = await fetch(BOOKING_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    serverOk = res.ok;
    if (!res.ok) {
      try { const j = await res.json(); serverMessage = j.message || j.error || ""; } catch (_) {}
    }
  } catch (_) {
    serverOk = false;
  }

  showConfirm(payload, serverOk, serverMessage);

  btnSubmit.disabled = false;
  btnSubmit.textContent = "Bevestig reservering";
});

// ---------- SINGLE-ARTIST STUDIO -------------------------------------
// The Global Beautybar has one nail tech. The artist profile lives
// statically in over-ons.html, so the dynamic chip/modal/roster modules
// from the parent template are intentionally empty here: the underlying
// logic still loads but binds to no elements.
const MASSEUSES_DATA = {};

const masseuseModal = $("#masseuse-modal");
if (masseuseModal) {
  const mPhoto       = $("#masseuse-modal-photo");
  const mThumbs      = $("#masseuse-modal-thumbs");
  const mCounter     = $("#masseuse-modal-counter");
  const mPrev        = $("#masseuse-modal-prev");
  const mNext        = $("#masseuse-modal-next");
  const mName        = $("#masseuse-modal-name");
  const mTagline     = $("#masseuse-modal-tagline");
  const mBio         = $("#masseuse-modal-bio");
  const mSpecialties = $("#masseuse-modal-specialties");
  const mDays        = $("#masseuse-modal-days");
  const mBookBtn     = $("#masseuse-modal-book");

  let galleryPhotos = [];
  let galleryIdx = 0;

  function showPhoto(i) {
    if (!galleryPhotos.length) return;
    galleryIdx = (i + galleryPhotos.length) % galleryPhotos.length;
    mPhoto.style.backgroundImage = `url("${cb(galleryPhotos[galleryIdx])}")`;
    if (mCounter) mCounter.textContent = `${galleryIdx + 1} / ${galleryPhotos.length}`;
    if (mThumbs) {
      $$(".masseuse-modal__thumb", mThumbs).forEach((t, n) =>
        t.classList.toggle("is-active", n === galleryIdx),
      );
    }
    const single = galleryPhotos.length <= 1;
    if (mPrev) mPrev.hidden = single;
    if (mNext) mNext.hidden = single;
    if (mCounter) mCounter.hidden = single;
  }

  function openMasseuse(slug) {
    const m = MASSEUSES_DATA[slug];
    if (!m) return;
    galleryPhotos = m.photos && m.photos.length ? m.photos : [m.photo].filter(Boolean);
    galleryIdx = 0;

    mName.textContent = m.name;
    mTagline.textContent = m.tagline || "";
    mBio.textContent = m.bio || "";
    mSpecialties.innerHTML = "";
    (m.specialties || []).forEach((s) => {
      const li = document.createElement("li");
      li.textContent = s;
      mSpecialties.appendChild(li);
    });
    mDays.textContent = m.days || "";
    mBookBtn.dataset.masseuseSlug = slug;

    if (mThumbs) {
      mThumbs.innerHTML = "";
      mThumbs.hidden = galleryPhotos.length <= 1;
      galleryPhotos.forEach((src, i) => {
        const t = document.createElement("button");
        t.type = "button";
        t.className = "masseuse-modal__thumb";
        t.style.backgroundImage = `url("${cb(src)}")`;
        t.setAttribute("aria-label", `Foto ${i + 1}`);
        on(t, "click", () => showPhoto(i));
        mThumbs.appendChild(t);
      });
    }
    showPhoto(0);

    masseuseModal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeMasseuse() {
    masseuseModal.hidden = true;
    document.body.style.overflow = "";
  }

  $$(".masseuse-card[data-masseuse]").forEach((btn) =>
    on(btn, "click", () => openMasseuse(btn.getAttribute("data-masseuse"))),
  );
  $$("[data-close-masseuse]").forEach((b) => on(b, "click", closeMasseuse));
  on(mPrev, "click", () => showPhoto(galleryIdx - 1));
  on(mNext, "click", () => showPhoto(galleryIdx + 1));
  on(document, "keydown", (e) => {
    if (masseuseModal.hidden) return;
    if (e.key === "Escape") closeMasseuse();
    else if (e.key === "ArrowLeft") showPhoto(galleryIdx - 1);
    else if (e.key === "ArrowRight") showPhoto(galleryIdx + 1);
  });

  // "Reserveer met deze masseuse" — close detail, open booking modal
  // with this masseuse pre-selected in step 1.
  on(mBookBtn, "click", () => {
    const slug = mBookBtn.dataset.masseuseSlug || "";
    closeMasseuse();
    if (typeof openModal === "function") openModal({ masseuse: slug });
  });
}

// ---------- BOOKING: MASSEUSE PICKER (chips in step 1) ---------------
// Built dynamically from MASSEUSES_DATA so we don't duplicate names
// across three pages. "Geen voorkeur" comes first and is selected
// by default.
(function buildBookMasseuseChips() {
  const wrap = $("#book-masseuses");
  if (!wrap) return;
  wrap.innerHTML = "";

  const any = document.createElement("button");
  any.type = "button";
  any.className = "book__masseuse book__masseuse--any is-selected";
  any.setAttribute("data-masseuse", "");
  any.setAttribute("data-label", "Geen voorkeur");
  any.innerHTML = `
    <span class="book__masseuse-photo book__masseuse-photo--any" aria-hidden="true">★</span>
    <span class="book__masseuse-name">Geen voorkeur</span>
  `;
  wrap.appendChild(any);

  Object.entries(MASSEUSES_DATA).forEach(([slug, m]) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "book__masseuse";
    btn.setAttribute("data-masseuse", slug);
    btn.setAttribute("data-label", m.name);
    const photoSrc = (m.photos && m.photos[0]) || "";
    btn.innerHTML = `
      <span class="book__masseuse-photo" style="background-image:url('${cb(photoSrc)}')"></span>
      <span class="book__masseuse-name">${m.name}</span>
    `;
    wrap.appendChild(btn);
  });

  // Wire up click handlers (delegation on the wrap)
  on(wrap, "click", (e) => {
    const chip = e.target.closest(".book__masseuse");
    if (!chip) return;
    $$(".book__masseuse", wrap).forEach((b) => b.classList.remove("is-selected"));
    chip.classList.add("is-selected");
    state.masseuse = chip.getAttribute("data-masseuse") || "";
  });
})();

// ---------- AMBIENT AUDIO (homepage spa loop) ------------------------
// Soft background audio. Off by default — browsers block autoplay-with-
// sound until a user gesture, and we don't want to surprise visitors.
// Click toggles; preference persists in localStorage so returning
// visitors hear it again (after their first interaction on the new visit
// the saved-on state will resume).
//
// Auto-pause: once playing, scrolling past the hero fades the track
// out. The Sfeer button stays — visitor can re-enable manually if they
// want music for the rest of the page. Only fires once per page load.
(function ambientAudio() {
  const btn   = $("#ambient-toggle");
  const audio = $("#ambient-audio");
  if (!btn || !audio) return;

  const BASE_VOLUME = 0.45; // calm background — bumped up slightly
  audio.volume = BASE_VOLUME;

  const STORAGE_KEY = "aurora-ambient";
  let unlocked = false;            // true after the first successful play()
  let autoPauseConsumed = false;   // scroll-fade only fires once per load

  function fadeOut(duration = 700) {
    const startVol = audio.volume;
    const start = performance.now();
    function tick(now) {
      const t = Math.min(1, (now - start) / duration);
      audio.volume = startVol * (1 - t);
      if (t < 1) requestAnimationFrame(tick);
      else {
        setPlaying(false);
        audio.volume = BASE_VOLUME; // reset for next manual play
      }
    }
    requestAnimationFrame(tick);
  }

  function setPlaying(playing, persist = true) {
    if (playing) {
      audio.volume = BASE_VOLUME;
      const p = audio.play();
      if (p && typeof p.then === "function") {
        p.then(() => {
          unlocked = true;
          btn.classList.add("is-playing");
          btn.setAttribute("aria-pressed", "true");
          if (persist) localStorage.setItem(STORAGE_KEY, "on");
        }).catch(() => {
          // autoplay blocked or audio file missing — stay silent
          btn.classList.remove("is-playing");
          btn.setAttribute("aria-pressed", "false");
        });
      }
    } else {
      audio.pause();
      btn.classList.remove("is-playing");
      btn.setAttribute("aria-pressed", "false");
      if (persist) localStorage.removeItem(STORAGE_KEY);
    }
  }

  on(btn, "click", () => setPlaying(!btn.classList.contains("is-playing")));

  // Scroll past ~70% of the viewport (i.e. past the hero) → fade out.
  function onScrollAutoPause() {
    if (autoPauseConsumed) return;
    if (!btn.classList.contains("is-playing")) return;
    if (window.scrollY > window.innerHeight * 0.7) {
      autoPauseConsumed = true;
      window.removeEventListener("scroll", onScrollAutoPause);
      fadeOut();
    }
  }
  window.addEventListener("scroll", onScrollAutoPause, { passive: true });

  // If the visitor previously enabled it, try to resume. The first call
  // may be silently rejected by the browser; the next user gesture will
  // succeed because setPlaying() runs again on click.
  if (localStorage.getItem(STORAGE_KEY) === "on") {
    setPlaying(true, false);
    const resume = () => {
      if (!unlocked && localStorage.getItem(STORAGE_KEY) === "on") {
        setPlaying(true, false);
      }
      document.removeEventListener("click", resume);
      document.removeEventListener("scroll", resume);
    };
    document.addEventListener("click", resume, { once: true });
    document.addEventListener("scroll", resume, { once: true, passive: true });
  }
})();

// ---------- HOMEPAGE: VANDAAG / MORGEN ROSTER ------------------------
// Renders into [data-roster] elements based on each masseuse's weekdays.
// We don't claim a hard "today" — bezetting wisselt — but a daily filter
// gives a representative list and matches what auroramassages.nl shows.
(function renderRoster() {
  const slots = $$("[data-roster]");
  if (!slots.length) return;

  const NL_WEEKDAY = ["zondag","maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag"];
  const NL_MONTH   = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"];

  const today = new Date();
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);

  function rosterFor(date) {
    const dow = date.getDay();
    const entries = Object.entries(MASSEUSES_DATA)
      .filter(([, m]) => Array.isArray(m.weekdays) && m.weekdays.includes(dow))
      .map(([slug, m]) => ({ slug, m }));
    // Deterministic shuffle by date so the order is stable but rotates daily.
    const seed = date.getFullYear() * 10000 + (date.getMonth() + 1) * 100 + date.getDate();
    let s = seed;
    const rand = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
    for (let i = entries.length - 1; i > 0; i--) {
      const j = Math.floor(rand() * (i + 1));
      [entries[i], entries[j]] = [entries[j], entries[i]];
    }
    return entries.slice(0, 8);
  }

  function dateLabel(d) {
    return `${NL_WEEKDAY[d.getDay()]} ${d.getDate()} ${NL_MONTH[d.getMonth()]}`;
  }

  slots.forEach((slot) => {
    const which = slot.getAttribute("data-roster"); // "today" | "tomorrow"
    const date  = which === "tomorrow" ? tomorrow : today;
    const list  = rosterFor(date);
    slot.innerHTML = "";

    const dateEl = slot.previousElementSibling
      && slot.previousElementSibling.classList.contains("roster__date")
      ? slot.previousElementSibling : null;
    if (dateEl) dateEl.textContent = dateLabel(date);

    if (!list.length) {
      const p = document.createElement("p");
      p.className = "roster__empty";
      p.textContent = "Bel ons voor de actuele bezetting.";
      slot.appendChild(p);
      return;
    }

    list.forEach(({ slug, m }) => {
      const card = document.createElement("a");
      card.className = "roster__card";
      card.href = `masseuses.html#${slug}`;
      card.innerHTML = `
        <span class="roster__photo" style="background-image:url('${cb((m.photos && m.photos[0]) || m.photo)}')"></span>
        <span class="roster__name">${m.name}</span>
      `;
      slot.appendChild(card);
    });
  });
})();

function showConfirm(p, serverOk, serverMessage) {
  state.step = "confirm";
  renderStep();

  const dateLabel = state.date.toLocaleDateString("nl-NL", {
    weekday: "long", day: "numeric", month: "long", year: "numeric",
  });
  const summaryParts = [p.serviceLabel, dateLabel, p.time];
  $("#book-summary").textContent = summaryParts.join(" · ");

  // Pre-filled WhatsApp deep link — useful for changes, cancellations,
  // or as a fallback contact channel when the booking proxy is down.
  const r = p.responses || {};
  const lines = [
    `Reservering ${SHOP.name}`,
    `Behandeling: ${p.serviceLabel}`,
    `Datum: ${dateLabel}`,
    `Tijd: ${p.time}`,
    `Naam: ${r.name || ""}`,
    `Telefoon: ${r.phone || ""}`,
  ];
  if (r.notes) lines.push(`Wensen: ${r.notes}`);
  const waText = encodeURIComponent(lines.join("\n"));
  const waLink = $("#book-wa");
  if (waLink) waLink.href = `https://wa.me/${SHOP.whatsapp}?text=${waText}`;

  if (!serverOk) {
    const hint = document.querySelector(".book__confirm .book__hint");
    if (hint) {
      const detail = serverMessage ? ` (${serverMessage})` : "";
      hint.innerHTML =
        `Het lukte ons niet om de reservering direct te bevestigen${detail}. ` +
        `Bel ons op <a href="tel:${SHOP.phone}">${SHOP.phoneDisplay}</a> ` +
        `of stuur een appje via de knop hierboven — we plannen je dan handmatig in.`;
    }
  }
}

// ---------- HERO: live open/closed status ------------------------------
// Reads SHOP_HOURS + current time; writes a dot + label into any
// [data-shop-status] element. Refreshes once per minute so a visitor
// who sits on the homepage right around opening time sees it tick over.
(function liveShopStatus() {
  const NL_WEEKDAY = ["zondag","maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag"];
  const els = $$("[data-shop-status]");
  if (!els.length) return;

  function fmt(hour) { return String(hour).padStart(2, "0") + ":00"; }

  function render() {
    const now = new Date();
    const dow = now.getDay();
    const hours = SHOP_HOURS[dow];
    let state = "closed";
    let html = "";

    if (hours) {
      const [open, close] = hours;
      const minutes = now.getHours() * 60 + now.getMinutes();
      const openMin = open * 60;
      const closeMin = close * 60;
      if (minutes >= openMin && minutes < closeMin) {
        state = "open";
        html = `<strong>Vandaag open</strong> · ${fmt(open)} – ${fmt(close)}`;
      } else if (minutes < openMin) {
        html = `<strong>Gesloten</strong> · vandaag open ${fmt(open)}`;
      } else {
        // After close → find next open day
        for (let i = 1; i <= 7; i++) {
          const c = (dow + i) % 7;
          if (SHOP_HOURS[c]) {
            html = `<strong>Gesloten</strong> · ${i === 1 ? "morgen" : NL_WEEKDAY[c]} weer open`;
            break;
          }
        }
      }
    } else {
      for (let i = 1; i <= 7; i++) {
        const c = (dow + i) % 7;
        if (SHOP_HOURS[c]) {
          const [open] = SHOP_HOURS[c];
          html = `<strong>Gesloten</strong> · ${i === 1 ? "morgen" : NL_WEEKDAY[c]} ${fmt(open)}`;
          break;
        }
      }
    }

    els.forEach((el) => {
      el.setAttribute("data-state", state);
      el.innerHTML = html;
    });
  }

  render();
  setInterval(render, 60 * 1000);
})();

// ---------- MOBILE STICKY CTA: show after scrolling past hero -----------
// CSS toggles display via body.is-scrolled-past-hero — we just set the
// class on the body when the user has scrolled "into" the page.
(function stickyCtaScrollState() {
  const threshold = 360; // px; roughly past the hero corner on phones
  function update() {
    document.body.classList.toggle("is-scrolled-past-hero", window.scrollY > threshold);
  }
  on(window, "scroll", update, { passive: true });
  update();
})();
