// POST /api/bookings
// Creates a booking via Cal.com v2. The frontend POSTs:
// {
//   start: ISO string,
//   eventTypeId: number,
//   serviceSlug, serviceLabel, servicePrice, serviceDuration,
//   responses: { name, email, phone, notes },
//   metadata: { ... },
//   timeZone, language
// }

import { calFetch, API_VERSIONS, json, handleError } from "./_cal.js";

async function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let buf = "";
    req.on("data", (chunk) => { buf += chunk; });
    req.on("end", () => {
      try { resolve(buf ? JSON.parse(buf) : {}); }
      catch (e) { reject(e); }
    });
    req.on("error", reject);
  });
}

export default async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { error: "method_not_allowed" });

  let payload;
  try { payload = await readJsonBody(req); }
  catch (_) { return json(res, 400, { error: "bad_json" }); }

  const {
    start,
    eventTypeId,
    responses = {},
    metadata = {},
    timeZone = "Europe/Amsterdam",
    language = "nl",
    serviceLabel,
  } = payload;

  if (!start || !eventTypeId) {
    return json(res, 400, {
      error: "missing_params",
      message: !eventTypeId
        ? "Deze behandeling is nog niet als event type aangemaakt in Cal.com."
        : "Start tijd ontbreekt.",
    });
  }
  if (!responses.name || !responses.phone) {
    return json(res, 400, { error: "missing_attendee", message: "Naam en telefoonnummer zijn verplicht." });
  }

  // Cal.com v2 booking payload shape (cal-api-version: 2024-08-13).
  const calBody = {
    start,
    eventTypeId: Number(eventTypeId),
    attendee: {
      name: responses.name,
      email: responses.email || `noreply+${Date.now()}@theglobalbeautybar.nl`,
      timeZone,
      language,
      phoneNumber: responses.phone,
    },
    bookingFieldsResponses: {
      ...(responses.notes ? { notes: responses.notes } : {}),
      ...(responses.phone ? { phone: responses.phone } : {}),
    },
    metadata: {
      ...metadata,
      ...(serviceLabel ? { serviceLabel } : {}),
    },
  };

  try {
    const data = await calFetch("/bookings", {
      method: "POST",
      apiVersion: API_VERSIONS.bookings,
      body: calBody,
    });
    return json(res, 200, { ok: true, booking: data });
  } catch (e) {
    return handleError(res, e);
  }
}
