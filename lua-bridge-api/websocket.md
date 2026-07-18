---
title: WebSocket Transport
parent: lua-bridge API
nav_order: 3
---

# WebSocket Transport

## Overview

Current version **v0.4.1**. The WebSocket transport was introduced in v0.4.0 and patched the same day in
v0.4.1 — both dated 2026-07-17 in `CHANGELOG.md`; git confirms the same-day cycle
(`199fa8e` v0.4.0 at 15:15, `1f40d7f` v0.4.1 at 19:32, both 2026-07-17).

It's a **hand-rolled RFC 6455 WebSocket server** — accepts inbound connections only, never opens outbound
ones. There is no vendored WebSocket library involved. It runs *inside* the existing raw-TCP REPL listener,
on the exact same socket and port (`127.0.0.1:27050` by default, from `lua_bridge_DEV.ini`'s `[repl]`
section — see [Getting Started](../getting-started#two-ways-to-run-code) for that protocol). There is no
separate, separately-configurable WS port. Each accepted connection is protocol-sniffed via `MSG_PEEK` on
the first bytes: if they read `"GET "`, the connection is treated as a WebSocket upgrade; anything else
falls through untouched to the pre-existing raw-TCP `<<<RUN>>>`/`<<<END>>>` line protocol. The only control
knob is an ini toggle, `websocket_enabled = 1|0` (default **1**, on) — set it to 0 to lock the listener to
raw-TCP only.

## Handshake

`ws_do_handshake` parses the HTTP GET request, locates the `Sec-WebSocket-Key` header (case-insensitive
substring scan, not a full header parser), and computes:

```
Sec-WebSocket-Accept = base64( sha1( Sec-WebSocket-Key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" ) )
```

using Windows **BCrypt** for SHA-1 (`BCryptOpenAlgorithmProvider`/`CreateHash`/`HashData`/`FinishHash` — the
three-call sequence, chosen because the one-shot `BCryptHash` helper isn't present in older MinGW
`bcrypt.h`) and **`CryptBinaryToStringA`** for base64. No third-party crypto library is linked in for this.
The GUID is the fixed RFC 6455 §1.3 constant. On success the server replies with a plain `101 Switching
Protocols` response carrying `Sec-WebSocket-Accept`; on any parse failure the connection is closed.

## Frame handling

`ws_recv_message` / `ws_send_frame` implement the framing needed for the wire contract below:

- Opcodes: `TEXT` (0x1), `BINARY` (0x2), `CLOSE` (0x8), `PING` (0x9), `PONG` (0xA), plus `CONTINUATION`
  (0x0) for fragment reassembly.
- Payload length uses the RFC 6455 §5.2 7/16/64-bit encoding (`<126` inline, `126` → 16-bit extended,
  `127` → 64-bit extended), on both send and receive.
- **Client frames must be masked** — per spec, the server rejects an unmasked client frame outright
  (`ws_recv_message` returns a protocol error) rather than silently accepting unmasked data.
- **Fragmented messages** are reassembled: the first data frame's opcode is remembered, subsequent
  fragments must be `CONTINUATION`, and the full message is only handed off once the `FIN` bit is set.
- **Ping is auto-ponged** and **close is echoed back** per §5.5.1, both handled inline even if they arrive
  interleaved with a fragmented data message.
- Message cap is `WS_MAX_MSG` = 1 MB, matching the raw-TCP `chunk_buf` cap so a WS client can send an
  equivalently large chunk.

## Concurrency

As of v0.4.1, each accepted WS connection gets its own worker thread (`WsClientThread`) and is tracked in
a shared client list, up to **`WS_MAX_CLIENTS` = 16** concurrent clients. A connection past the cap is
refused cleanly: `ws_add_client` fails, the socket is closed, and a log line records it —
`ws: refused client — %d clients already connected (WS_MAX_CLIENTS)`. Existing clients are unaffected by a
refusal. Raw TCP remains strictly single-client (its `<<<RUN>>>`/`<<<END>>>` protocol is inherently 1:1) —
unchanged and unaffected by any of this.

v0.4.0 shipped WS support as single-client only. v0.4.1's diff (`199fa8e`→`1f40d7f`) is what added the
`WS_MAX_CLIENTS` array/cap and raised the listener's `listen()` backlog from **1 to 8**, specifically so a
burst of near-simultaneous connection attempts doesn't get RST instead of queued.

## `Loader.WsSend` — the hidden channel

The only new Lua-callable function this transport adds:

```lua
Loader.WsSend(str, ...)
```

Same tab-joined variadic-string semantics as [`Loader.Printf`](loader) — every string argument is
concatenated with tabs, same as Lua's own `print()`. It broadcasts `{"type":"ws","line":"..."}` to *every*
currently-connected WS client. Unlike `Printf`, this never touches `lua_loader_printf.log` — it's a
WS-only, log-invisible channel. If no WS client is connected, it's a safe no-op (the broadcast loop simply
iterates zero clients).

`Loader.Printf`'s existing behavior gained a side effect in the same release: it still writes
`lua_loader_printf.log` exactly as before, but now **also** mirrors each call to every connected WS client
as `{"type":"log","line":"..."}`. This is the "live console feed" a browser client watches. Nothing about
raw-TCP or file-logging behavior changed — `Printf` never wrote to the raw-TCP output path in the first
place.

## Wire contract

One WS text-frame message is one request:

```
client -> bridge   {"id":"q17abc","code":"<lua source>"}
bridge -> client   {"type":"ack","id":"q17abc","status":"queued"}
bridge -> client   {"type":"log","line":"...a Loader.Printf line..."}
bridge -> client   {"type":"ws","line":"...a Loader.WsSend line..."}
```

The ack is sent immediately, synchronously, from the socket thread the moment the chunk is queued.
Log/ws lines arrive afterward, in real time, as the queued code actually executes on the game thread —
there is no guaranteed timing relationship between the ack and any particular log/ws line beyond "after."

`ws_parse_request` is a minimal, hand-rolled JSON reader scoped to exactly this contract — it looks up only
the `id` and `code` string keys (with standard backslash/`\uXXXX` unescaping) and otherwise skips whatever
else is present. It is **not** a general JSON library: nested objects/arrays inside the `code` string value
are fine, because at that point `code` is just a string being unescaped, not re-parsed. But it isn't a
document parser either — a full JSON body carrying nested objects/arrays as *other* top-level fields isn't
specially handled by the skip logic. In practice the wire contract only ever needs the two fields, so this
hasn't mattered, but don't assume it tolerates an arbitrary JSON body glued onto this shape.

## Threading model and result routing

The game's Lua VM is single-threaded and tick-driven — nothing changes that. A WS client's socket thread
**never touches Lua directly**. It only parses the incoming JSON, then pushes the extracted code string onto
the exact same cross-thread chunk queue that raw-TCP, `OnKey`, `OnLoad`, and `OnBoot` scripts already share
(tagged with a `from_ws` provenance bit on the queue node). That queue is drained on the main thread by the
same pump mechanism described in [Getting Started](../getting-started#two-ways-to-run-code) — a WS request
doesn't get a dedicated execution path, it rides the existing one.

Because a WS request has **no synchronous return path over the socket** — the ack only confirms
"queued," not "finished," let alone "here's the result" — result routing is handled **entirely by
client-side convention**, not by the bridge. The expected pattern is: the client wraps the Lua source it
submits so that, after doing its work, it calls `Loader.WsSend` with a nonce-tagged result string, then the
client watches the `{"type":"ws"}` stream itself and matches that tag back out. **The C side does no
request/response correlation whatsoever** — it doesn't know or track which `id` a given `WsSend` call
"belongs to." This is worth stating plainly because the wire contract's `{"id":...}` field makes it easy to
assume the bridge threads that id through to a matching response; it doesn't. The `id` only ever appears in
the immediate `{"type":"ack"}` reply — nothing downstream of that carries it.

## Cross-transport isolation

A WS-submitted chunk's result is kept out of the raw-TCP output buffer (`g_outBuf`) entirely — the
`from_ws` bit on the queue node makes the pump skip that fanout for WS-originated chunks, so a WS session
and a concurrent raw-TCP REPL session never see each other's output. This was, in fact, the specific bug
v0.4.1's "Fixed" entry addresses (`CHANGELOG.md`): previously every chunk's result was written to
`g_outBuf` regardless of origin, so a raw-TCP client connecting after a WS client had queued (and possibly
disconnected from) a chunk could see that chunk's stale result appear before its own `[queued]` ack.
v0.4.1 also clears `g_outBuf` at raw-TCP accept-time as a second layer against exactly this leakage.

## Status

Both v0.4.0 and v0.4.1's `CHANGELOG.md` entries are plain "Added"/"Changed"/"Fixed" sections — neither
carries a "Verification" section (the kind v0.3.0's entry has, citing stress-suite pass counts and measured
`IsKeyDown` throughput). So: this is **written and internally consistent on read, with no recorded
live-client verification** — no logged handshake against a real browser, no logged full
request-then-result round trip — as of this writing. Treat it accordingly; don't describe it as "confirmed
working" until that testing happens and gets recorded. There is also no sample `.lua` script anywhere in
this repo that exercises `Loader.WsSend` — the only referenced client is a JS reference client
(`tools/ess-bridge.js`) that lives in a separate repository, not this one.

## See also

- [Loader](loader) — `Loader.Printf`, whose tab-joined string-argument semantics `Loader.WsSend` reuses,
  and whose existing behavior now also mirrors to WS clients.
- [Getting Started](../getting-started#two-ways-to-run-code) — the raw-TCP REPL protocol and the
  queue/pump mechanism this transport's chunks are drained through.
- [Lua Web IDE](../live-tools/web-ide) — a browser-based client built on this transport.
- [Live Map](../live-tools/live-map) — another client consuming this transport.
