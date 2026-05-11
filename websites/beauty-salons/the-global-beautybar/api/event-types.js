// GET /api/event-types
// Lists every Cal.com event type for the authenticated user. The
// frontend uses this to build a {slug -> id} map for /api/bookings.

import { calFetch, unwrap, API_VERSIONS, json, handleError } from "./_cal.js";

export default async function handler(req, res) {
  if (req.method !== "GET") return json(res, 405, { error: "method_not_allowed" });

  try {
    const raw = await calFetch("/event-types", { apiVersion: API_VERSIONS.eventTypes });
    const data = unwrap(raw);

    // Cal.com v2 returns either an array, or an object like
    // { eventTypeGroups: [{ eventTypes: [...] }, ...] }. Flatten defensively.
    let list = [];
    if (Array.isArray(data)) {
      list = data;
    } else if (Array.isArray(data?.eventTypes)) {
      list = data.eventTypes;
    } else if (Array.isArray(data?.eventTypeGroups)) {
      list = data.eventTypeGroups.flatMap((g) => g.eventTypes || []);
    }

    // Strip down to only what the frontend needs.
    const trimmed = list.map((et) => ({
      id: et.id,
      slug: et.slug,
      title: et.title,
      length: et.length || et.lengthInMinutes,
      price: et.price,
    }));

    return json(res, 200, trimmed);
  } catch (e) {
    return handleError(res, e);
  }
}
