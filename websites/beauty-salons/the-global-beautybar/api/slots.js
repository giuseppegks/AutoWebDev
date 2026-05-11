// GET /api/slots?eventTypeId=123&startTime=2026-05-12T00:00:00Z&endTime=2026-05-13T00:00:00Z&timeZone=Europe/Amsterdam
// Returns available booking slots for the given event type on the given day.

import { calFetch, unwrap, API_VERSIONS, json, handleError } from "./_cal.js";

export default async function handler(req, res) {
  if (req.method !== "GET") return json(res, 405, { error: "method_not_allowed" });

  const url = new URL(req.url, `http://${req.headers.host}`);
  const eventTypeId = url.searchParams.get("eventTypeId");
  const startTime   = url.searchParams.get("startTime");
  const endTime     = url.searchParams.get("endTime");
  const timeZone    = url.searchParams.get("timeZone") || "Europe/Amsterdam";

  if (!eventTypeId || !startTime || !endTime) {
    return json(res, 400, { error: "missing_params", message: "eventTypeId, startTime, endTime zijn verplicht." });
  }

  try {
    const raw = await calFetch("/slots", {
      apiVersion: API_VERSIONS.slots,
      query: { eventTypeId, start: startTime, end: endTime, timeZone, format: "time" },
    });
    const data = unwrap(raw);

    // Normalize to a flat array of ISO strings regardless of shape.
    // Possible shapes:
    //   - { "2026-05-12": [{ time: "..." }, ...] }
    //   - { slots: { "2026-05-12": ["..."] } }
    //   - ["...", "..."]
    let slots = [];
    if (Array.isArray(data)) {
      slots = data;
    } else if (data && typeof data === "object") {
      const buckets = data.slots && typeof data.slots === "object" ? data.slots : data;
      for (const v of Object.values(buckets)) {
        if (Array.isArray(v)) {
          for (const entry of v) {
            if (typeof entry === "string") slots.push(entry);
            else if (entry && entry.time) slots.push(entry.time);
            else if (entry && entry.start) slots.push(entry.start);
          }
        }
      }
    }

    return json(res, 200, { slots });
  } catch (e) {
    return handleError(res, e);
  }
}
