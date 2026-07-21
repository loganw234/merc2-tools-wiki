/**
 * Mercenaries 2 wiki assistant -- Cloudflare Worker.
 *
 * Sits between the static chat page on GitHub Pages and DeepSeek. It exists for
 * three reasons:
 *   1. It holds the provider API key. A static site cannot.
 *   2. It holds the context pack, which is both the product and the cache prefix.
 *   3. It is the only place abuse controls can live.
 *
 * THE CACHE INVARIANT: DeepSeek bills cached prefix tokens at roughly 1% of the
 * uncached rate, and the pack is ~105k of the ~110k tokens in a typical request.
 * The cache only hits on an exact prefix match, so the system message must be
 * byte-identical on every request forever. Do not interpolate a date, a session
 * id, a user name, or anything else into it. If you need per-request context,
 * append it as a later message.
 *
 * Endpoints:
 *   POST /session  { turnstileToken }        -> { session, expiresAt }
 *   POST /chat     { session, messages[] }   -> text/event-stream (passthrough)
 */

import PACK from "../../pack/pack.txt";

// Frozen at module scope so it is provably identical across requests.
const SYSTEM_MESSAGE = { role: "system", content: PACK };

const enc = new TextEncoder();

export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin");

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(env, origin) });
    }
    if (request.method !== "POST") {
      return jsonError(405, "method_not_allowed", "Use POST.", env, origin);
    }
    // Reject cross-origin callers outright. This is not a security boundary on
    // its own (curl sends whatever Origin it likes) -- the rate limit and the
    // provider spend cap are. It just stops other sites embedding our endpoint.
    if (origin && origin !== env.ALLOWED_ORIGIN) {
      return jsonError(403, "forbidden_origin", "Not allowed from this origin.", env, origin);
    }

    const path = new URL(request.url).pathname;
    try {
      if (path === "/session") return await handleSession(request, env, origin);
      if (path === "/chat") return await handleChat(request, env, ctx, origin);
      return jsonError(404, "not_found", "Unknown endpoint.", env, origin);
    } catch (err) {
      // Never surface an upstream body to the client -- it can echo request
      // details. Log it, return something generic.
      console.error("unhandled", err && err.stack ? err.stack : String(err));
      return jsonError(500, "internal_error", "Something broke on our side.", env, origin);
    }
  },
};

/* ------------------------------------------------------------------ *
 * /session -- trade a Turnstile token for a short-lived signed session
 * ------------------------------------------------------------------ */

async function handleSession(request, env, origin) {
  const body = await readJson(request);
  if (!body || typeof body.turnstileToken !== "string") {
    return jsonError(400, "bad_request", "Missing turnstileToken.", env, origin);
  }

  const ip = clientIp(request);
  const form = new FormData();
  form.append("secret", env.TURNSTILE_SECRET);
  form.append("response", body.turnstileToken);
  if (ip) form.append("remoteip", ip);

  const verify = await fetch(
    "https://challenges.cloudflare.com/turnstile/v0/siteverify",
    { method: "POST", body: form }
  );
  const result = await verify.json();
  if (!result.success) {
    return jsonError(403, "turnstile_failed", "Verification failed. Reload and try again.",
      env, origin);
  }

  const ttl = int(env.SESSION_TTL_SECONDS, 7200);
  const expiresAt = Math.floor(Date.now() / 1000) + ttl;
  const session = await signSession(expiresAt, ip, env.SESSION_SECRET);
  return jsonOk({ session, expiresAt }, env, origin);
}

/* ------------------------------------------------------------------ *
 * /chat -- validate, rate-limit, proxy to DeepSeek, stream back
 * ------------------------------------------------------------------ */

async function handleChat(request, env, ctx, origin) {
  const body = await readJson(request);
  if (!body) return jsonError(400, "bad_request", "Expected a JSON body.", env, origin);

  const ip = clientIp(request);

  // 1. Session (proves a Turnstile pass happened recently, from this IP).
  const ok = await verifySession(body.session, ip, env.SESSION_SECRET);
  if (!ok) {
    return jsonError(401, "session_invalid",
      "Your session expired. Reload the page to continue.", env, origin);
  }

  // 2. Shape and size. These caps exist so a script cannot turn the endpoint
  //    into a general-purpose free LLM proxy by pasting a novel into it.
  const messages = Array.isArray(body.messages) ? body.messages : null;
  if (!messages || messages.length === 0) {
    return jsonError(400, "bad_request", "No messages.", env, origin);
  }
  if (messages.length > int(env.MAX_TURNS, 16)) {
    return jsonError(400, "too_many_turns",
      "This conversation is too long. Start a new one.", env, origin);
  }
  const maxPer = int(env.MAX_CHARS_PER_MESSAGE, 16000);
  let total = 0;
  for (const m of messages) {
    if (!m || (m.role !== "user" && m.role !== "assistant") || typeof m.content !== "string") {
      return jsonError(400, "bad_request", "Malformed message.", env, origin);
    }
    if (m.content.length > maxPer) {
      return jsonError(400, "message_too_long",
        `That message is ${m.content.length} characters; the limit is ${maxPer} ` +
        `(roughly ${Math.round(maxPer / 35)} lines of Lua). Paste the file that ` +
        `contains the problem rather than the whole mod.`,
        env, origin);
    }
    total += m.content.length;
  }
  if (total > int(env.MAX_CHARS_TOTAL, 40000)) {
    return jsonError(400, "conversation_too_long",
      "This conversation is too long. Start a new one.", env, origin);
  }
  if (messages[messages.length - 1].role !== "user") {
    return jsonError(400, "bad_request", "Last message must be from the user.", env, origin);
  }

  // 3. Rate limit. KV is eventually consistent and caps writes at ~1/sec/key,
  //    which is fine at this scale -- a determined attacker might squeeze a few
  //    extra requests through a race, and the provider spend cap catches that.
  const limited = await checkRateLimit(env, ip);
  if (limited) {
    return jsonError(429, "rate_limited", limited, env, origin);
  }

  // 4. Upstream. Pack goes first and alone in the system slot -- see the cache
  //    invariant at the top of this file.
  const upstream = await fetch(`${env.DEEPSEEK_BASE_URL}/chat/completions`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${env.DEEPSEEK_API_KEY}`,
    },
    body: JSON.stringify({
      model: env.DEEPSEEK_MODEL,
      messages: [SYSTEM_MESSAGE, ...messages],
      max_tokens: int(env.MAX_OUTPUT_TOKENS, 2000),
      stream: true,
      // Asks the provider to emit a final usage frame so we can confirm the
      // prefix cache is actually hitting. Without this the whole cost model is
      // unverifiable.
      stream_options: { include_usage: true },
    }),
  });

  if (!upstream.ok || !upstream.body) {
    const detail = await upstream.text().catch(() => "");
    console.error("upstream_error", upstream.status, detail.slice(0, 500));
    const msg = upstream.status === 429
      ? "The model provider is rate-limiting us. Try again in a moment."
      : "The model provider returned an error. Try again shortly.";
    return jsonError(502, "upstream_error", msg, env, origin);
  }

  return new Response(upstream.body.pipeThrough(usageLogger()), {
    headers: {
      ...corsHeaders(env, origin),
      "content-type": "text/event-stream; charset=utf-8",
      "cache-control": "no-cache, no-transform",
      connection: "keep-alive",
    },
  });
}

/**
 * Passes the SSE stream through untouched while watching for the final usage
 * frame. `prompt_cache_hit_tokens` is the number that matters: if it is not
 * roughly the pack size on a warm cache, something is breaking prefix stability
 * and every request is being billed at ~120x the cached rate.
 */
function usageLogger() {
  // Keep the last few RAW chunks and decode only at the end. Decoding every
  // chunk would burn Worker CPU proportional to response length, which matters
  // now that MAX_OUTPUT_TOKENS allows long answers. Per-chunk work here is a
  // push and an occasional shift.
  const recent = [];
  const KEEP = 8;
  return new TransformStream({
    transform(chunk, controller) {
      controller.enqueue(chunk);
      recent.push(chunk);
      if (recent.length > KEEP) recent.shift();
    },
    flush() {
      const decoder = new TextDecoder();
      let tail = "";
      for (const c of recent) tail += decoder.decode(c, { stream: true });
      const hit = /"prompt_cache_hit_tokens"\s*:\s*(\d+)/.exec(tail);
      const miss = /"prompt_cache_miss_tokens"\s*:\s*(\d+)/.exec(tail);
      const out = /"completion_tokens"\s*:\s*(\d+)/.exec(tail);
      if (hit || miss || out) {
        console.log(JSON.stringify({
          event: "usage",
          cache_hit_tokens: hit ? +hit[1] : null,
          cache_miss_tokens: miss ? +miss[1] : null,
          completion_tokens: out ? +out[1] : null,
        }));
      }
    },
  });
}

/* ------------------------------------------------------------------ *
 * rate limiting
 * ------------------------------------------------------------------ */

async function checkRateLimit(env, ip) {
  if (!env.RATE_LIMIT || !ip) return null;
  const now = Math.floor(Date.now() / 1000);
  const windows = [
    { key: `h:${ip}:${Math.floor(now / 3600)}`, ttl: 3600,
      max: int(env.MAX_MESSAGES_PER_HOUR, 25),
      msg: "You've hit the hourly limit. Try again in a little while." },
    { key: `d:${ip}:${Math.floor(now / 86400)}`, ttl: 86400,
      max: int(env.MAX_MESSAGES_PER_DAY, 80),
      msg: "You've hit the daily limit. Try again tomorrow." },
  ];
  for (const w of windows) {
    const current = int(await env.RATE_LIMIT.get(w.key), 0);
    if (current >= w.max) return w.msg;
    // expirationTtl keeps the namespace self-cleaning; no sweep job needed.
    await env.RATE_LIMIT.put(w.key, String(current + 1), { expirationTtl: w.ttl });
  }
  return null;
}

/* ------------------------------------------------------------------ *
 * session tokens (HMAC-SHA256 over "expiry.ip")
 * ------------------------------------------------------------------ */

async function hmacKey(secret) {
  return crypto.subtle.importKey(
    "raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
}

async function signSession(expiresAt, ip, secret) {
  const key = await hmacKey(secret);
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(`${expiresAt}.${ip || ""}`));
  return `${expiresAt}.${b64url(sig)}`;
}

async function verifySession(token, ip, secret) {
  if (typeof token !== "string" || !token.includes(".")) return false;
  const [expStr] = token.split(".", 1);
  const expiresAt = parseInt(expStr, 10);
  if (!Number.isFinite(expiresAt) || expiresAt < Math.floor(Date.now() / 1000)) return false;
  const expected = await signSession(expiresAt, ip, secret);
  return timingSafeEqual(token, expected);
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function b64url(buf) {
  const bytes = new Uint8Array(buf);
  let s = "";
  for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

/* ------------------------------------------------------------------ *
 * helpers
 * ------------------------------------------------------------------ */

function clientIp(request) {
  return request.headers.get("CF-Connecting-IP") || "";
}

function int(v, fallback) {
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : fallback;
}

async function readJson(request) {
  try {
    return await request.json();
  } catch {
    return null;
  }
}

function corsHeaders(env, origin) {
  return {
    "access-control-allow-origin": env.ALLOWED_ORIGIN,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    vary: "Origin",
  };
}

function jsonOk(obj, env, origin) {
  return new Response(JSON.stringify(obj), {
    status: 200,
    headers: { ...corsHeaders(env, origin), "content-type": "application/json" },
  });
}

function jsonError(status, code, message, env, origin) {
  return new Response(JSON.stringify({ error: code, message }), {
    status,
    headers: { ...corsHeaders(env, origin), "content-type": "application/json" },
  });
}
