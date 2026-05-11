// Internal helper for /api/* proxies — never exposed directly to the
// browser. Centralizes Bearer auth, cal-api-version pinning, and
// defensive response handling so each route handler stays small.

const CAL_BASE = "https://api.cal.com/v2";

// Pinned API versions per booking-system skill. Bump these in tandem
// if Cal.com publishes a breaking change.
export const API_VERSIONS = {
  eventTypes: "2024-06-14",
  slots: "2024-09-04",
  bookings: "2024-08-13",
};

function authHeader() {
  const key = process.env.CALCOM_API_KEY;
  if (!key) {
    const err = new Error("CALCOM_API_KEY env var is missing");
    err.code = "missing_key";
    throw err;
  }
  return `Bearer ${key}`;
}

export async function calFetch(path, { method = "GET", body, apiVersion, query } = {}) {
  const url = new URL(`${CAL_BASE}${path}`);
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, String(v));
    }
  }

  const headers = {
    "Authorization": authHeader(),
    "Accept": "application/json",
  };
  if (apiVersion) headers["cal-api-version"] = apiVersion;
  if (body !== undefined) headers["Content-Type"] = "application/json";

  const res = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (_) { /* non-JSON */ }

  if (!res.ok) {
    const message = (data && (data.error?.message || data.message)) || text || `Cal.com ${res.status}`;
    const err = new Error(message);
    err.status = res.status;
    err.body = data;
    throw err;
  }
  return data;
}

// Cal.com v2 sometimes wraps in { status, data }, sometimes returns raw arrays
// depending on the endpoint version. Always unwrap to the inner payload.
export function unwrap(data) {
  if (data && typeof data === "object" && "data" in data) return data.data;
  return data;
}

// Standard JSON response helper for Vercel Node functions
export function json(res, status, payload) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(payload));
}

export function handleError(res, e) {
  if (e?.code === "missing_key") {
    return json(res, 500, { error: "config", message: "Server is niet correct geconfigureerd (CALCOM_API_KEY ontbreekt)." });
  }
  return json(res, e?.status || 500, {
    error: "upstream",
    message: e?.message || "Onverwachte fout bij Cal.com.",
    detail: e?.body || null,
  });
}
