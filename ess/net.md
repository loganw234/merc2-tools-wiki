---
title: Networking
parent: Essentials (Ess)
nav_order: 11
---

# Networking

> **Status: co-op delivery not independently re-confirmed.** `Ess.Net` is a faithful port of confirmed-working
> co-op code (real co-op wave-defense sessions on the standalone `ModNet.lua`), but full two-machine delivery
> hasn't been re-verified solo under this port — that needs a second machine. Treat the "confirmed" history
> below as inherited from `ModNet.lua`'s own live-test record, not independently re-tested for `Ess.Net`.

## Overview

`Ess.Net` (`70_net.lua` + `71_net_wire.lua`) is the native port of [`ModNet.lua`](../modnet) (`_G.ModNet`) —
the co-op data-sync layer built on `Net.SendCustomEvent`. The wire protocol itself (serialization,
chunking/reassembly, the last-writer-wins synced-state channel, the ready-gate handshake) is called out in
the source comments as a "FAITHFUL, byte-for-byte port" of confirmed-working production co-op code — see
[ModNet](../modnet) for the deep mechanics writeup (the TLV serialization tags, LWW tie-breaking, the
heartbeat's three jobs) this page doesn't repeat. What's genuinely new is the scaffolding around it:

- The callback hijack now goes through the general-purpose `Ess.Net.hijackCallback` (below), built on
  [`Ess.Override.wrap`](override), instead of a second hand-rolled copy of the same recipe.
- The heartbeat runs on `Ess.Loop` instead of a raw self-rescheduling `Event.Create`.
- Every wire packet now carries a magic marker that `ModNet.lua`'s own hijack didn't need (see below).
- A ready-gate handshake holds outgoing traffic until the peer confirms it has `Ess.Net` installed — not
  present in the standalone `ModNet.lua` documented on this wiki.

Same three layers as `ModNet` — use the highest one that fits.

## 1. Synced state — `Shared` / `Set` / `Get` / `Track`

```lua
local S = Ess.Net.Shared("mymod")   -- a table whose fields auto-sync (LWW)
S.score = 100                        -- write -> broadcast; read S.score anywhere

Ess.Net.Set("k", v)   -- shortcut: same idea, default namespace ("_")
Ess.Net.Get("k")

Ess.Net.Track("hp", function() return myHp end)   -- push a local var out on a heartbeat
```

- **`Ess.Net.Shared(ns) -> table`** — returns a table with `__index`/`__newindex` metamethods wired to the
  internal synced-state store; reading or writing a field *is* reading or writing synced state, no explicit
  send/receive call anywhere in your own code.
- **`Ess.Net.Set(key, value)`** / **`Ess.Net.Get(key)`** — shortcuts for `Shared("_")`, the default
  namespace.
- **`Ess.Net.Track(key, getter, ns)`** — polls `getter()` once per heartbeat (`Ess.Net.HB`, default 2s) and
  broadcasts only when its return value actually changed since the last check. **Idempotent**: calling
  `Track` again with the same `(ns, key)` just replaces the getter in place rather than adding a duplicate
  watcher — safe to call again on a reload.

A direct `Shared` write broadcasts *every time*, whether or not the value actually changed — unlike `Track`,
which only sends on a real diff. Guard a frequently-rewritten `Shared` field yourself with a plain equality
check if you don't want it spamming the wire (see [ModNet's writeup](../modnet#1-synced-state-simplest) for
the one-line pattern `WaveDefense.lua` uses).

## 2. Messages — `On` / `Send`

```lua
Ess.Net.On("chat", function(sender, text) ... end)   -- sender = 0/1 player id
Ess.Net.Send("chat", "hello")                          -- any value: str/num/bool/table
```

- **`Ess.Net.On(name, fn)`** — registers a receiver for channel `name`; `fn(sender, value)`.
- **`Ess.Net.Send(name, value, reliable)`** — serializes `value` (string/number/bool/nil/nested table) and
  sends it chunked over the wire. `reliable` defaults to `true` (pass `false` for an unreliable send).

`CoopChat.lua` (see `samples/OnKey/CoopChat.lua`) is the reference example — it sends `{ name = ..., text =
... }` tables over a `"chat"` channel and titles incoming lines with the sender's name, falling back to a
`P1`/`P2` label built from `sender` (`0`/`1`) if none was set.

## 3. Raw — `OnRaw` / `SendRaw`

```lua
Ess.Net.OnRaw("ch", function(sender, nums) ... end)
Ess.Net.SendRaw("ch", { 1, 2, 3 })
```

Bypasses serialization entirely — plain number arrays in, plain number arrays out. **`Send`/`On` and
`SendRaw`/`OnRaw` are separate pairs per channel** — the receiving side has to register with whichever one
the sender used, since that determines whether the incoming bytes get deserialized or handed back raw.

## Identity & authority

```lua
Ess.Net.Me()          -- this machine's player id (0/1)
Ess.Net.IsCoop()       -- in a live co-op session?
Ess.Net.IsHost()       -- true only on the host/authority, in co-op
Ess.Net.IsAuthority()  -- SP OR co-op host = "should I run the sim?"
```

Same semantics as `ModNet`'s [Identity & authority](../modnet#identity--authority): `IsHost()` alone is
**false in single-player** (`Net.IsServer()` reads falsy when there's no "server" role to hold with nobody
else connected), so `IsAuthority()` folds that in — true in single-player unconditionally, true in co-op only
for the host. Internally every native flag read is normalized through a small `T(x) = x == true or x == 1`
helper, since this engine's boolean-ish return values aren't consistently real Lua booleans.

Note that [`Ess.Contract.Accept`](contract) does **not** use `Ess.Net.IsAuthority()` for its own co-op gate —
it checks the native `Net.IsMultiplayer()`/`Net.IsClient()` functions directly instead, for a
confirmed-specific reason documented on that page.

## `Ess.Net.hijackCallback` — the collision-proof hijack, generalized

```lua
Ess.Net.hijackCallback(moduleTable, name, isMinePredicate, onMine) -> ok
```

Generalizes the exact fix `ModNet.lua` needed for a **confirmed real-world bug**: `MrxFactionManager.
NetEventCallback` is shared with the game's own faction traffic on the same custom-event id. An earlier,
naive hijack (`MrxFactionManager.NetEventCallback = function(...) handle it end`, ignoring anything not
recognized) unconditionally claimed *every* packet on that id, which silently swallowed the game's own co-op
join/faction-sync events — the real, shipped root cause of a co-op **black screen** on connection.

`hijackCallback` extracts the fix (mark → check → claim-mine-or-passthrough) as a reusable primitive for any
always-resident callback:

- `moduleTable` — the resident module table (e.g. `MrxFactionManager`), already `import()`'d by the caller —
  `import` is file-scoped, `Ess.Net` can't do it for you.
- `name` — the field name to hijack (e.g. `"NetEventCallback"`).
- `isMinePredicate(...) -> bool` — your marker check, called with whatever arguments the native callback
  itself receives (the shape varies per callback — this doesn't assume any particular one).
- `onMine(...)` — called (`pcall`-guarded) when `isMinePredicate` returns true; **the original is not called
  for a "mine" packet** — a marker-tagged packet is fully yours, not also forwarded to whatever used to
  handle that id.

Built on [`Ess.Override.wrap`](override) rather than hand-rolling a second copy of the tail-call-avoidance
machinery — and, per the source's own comment, arguably *safer* than `ModNet.lua`'s own literal code:
ModNet's own pass-through line is `return orig(evt, tArgs)`, itself a tail call (apparently fine in that
specific confirmed-working co-op-tested case, but this project's established rule is "never `return
fOriginal(...)`," full stop) — `hijackCallback` never tail-calls the original in either branch.

`Ess.Net` dogfoods this on itself: its own wire receiver is installed via

```lua
Ess.Net.hijackCallback(MrxFactionManager, "NetEventCallback",
    function(evt, tArgs) return evt == M.EV and tArgs ~= nil and tArgs[1] == M.MAGIC end,
    function(_, tArgs) wireRecv(tArgs) end)
```

— the general-purpose version of the exact recipe it was extracted from.

## Config

| Field | Default | What |
|---|---|---|
| `Ess.Net.EV` | `5` | The shared `SendCustomEvent` id every `Ess.Net` channel multiplexes over. Shared with the game's own faction events on this id — `MAGIC` (below) is what tells them apart. |
| `Ess.Net.MAGIC` | `5066564` (`"MOD"` / `0x4D4F44`) | Leads every `Ess.Net` packet (`tArgs[1]`) so the receiver only claims genuinely-ours traffic and passes the game's own events on the same id straight through. |
| `Ess.Net.SLOTS` | `5` | `tArgs` per send. 3 are header now (magic + mid/seq/total + sender/channel); the rest carry payload. |
| `Ess.Net.HB` | `2.0` | Heartbeat interval, seconds — `Track` polling, ready-gate retries, periodic full state reconcile, reassembly-buffer GC. |

## Constraints

Same as `ModNet`: numbers are 24-bit-safe (3 bytes each), this is a small-payload control plane (sync
*state*, not files — every send still costs one or more real `SendCustomEvent` calls), and
host-authoritative or single-writer keys converge cleanest under last-writer-wins.

## The ready-gate handshake

Traffic on the shared `SendCustomEvent` id is **held** (`wireSend` no-ops) while in a co-op session until
the peer's own `Ess.Net` has confirmed it's installed — except the two handshake channels themselves. A
freshly-loaded joiner (non-authority) announces readiness immediately on load and again every heartbeat tick
until acked, so nothing gets sent at a peer still on its load screen (whose `Ess.Net` isn't installed yet,
and whose native faction handler could otherwise choke on the traffic). Once the host acks, both sides push
a full state reconcile so nothing set before the handshake completed is lost. Local writes to `Shared`/`Set`
still update immediately regardless of gate state — only the wire send is held.

## Differences from `ModNet.lua`

| | `ModNet.lua` | `Ess.Net` |
|---|---|---|
| Callback hijack | Hand-rolled inline (`if evt == M.EV then M._recv(tArgs) elseif orig then orig(evt, tArgs) end`) | `Ess.Net.hijackCallback`, built on `Ess.Override.wrap` |
| Packet marking | None — claims every packet on `M.EV` | Every packet carries `M.MAGIC`; unmarked traffic on the same event id passes straight through |
| Heartbeat | Raw self-rescheduling `Event.Create` | `Ess.Loop.start("Ess.Net.heartbeat", ...)` — always returns `true` (never idles); `Ess.Loop`'s own generation guard supersedes any previous instance cleanly on a reload |
| Header layout | 2 header slots (mid/seq/total, sender+channel) | 3 header slots (adds the magic marker) |
| Ready-gate handshake | Not present | Present — see above |

Because of the added magic-marker header slot, `Ess.Net`'s wire format is **not** byte-compatible with the
standalone `ModNet.lua` — both co-op peers need to be running the same one. The `"ModNet$state"` /
`"ModNet$ready"` / `"ModNet$rack"` channel *names* are kept byte-identical between the two only so their hash
(`chash`) lines up if you're reasoning about either implementation side by side — it does not imply
cross-version wire compatibility given the header change.

## See also

- [ModNet](../modnet) — the standalone predecessor; the full mechanics writeup (TLV serialization, LWW
  tie-breaking, the heartbeat's three jobs, the `chash` channel-multiplexing scheme) this page builds on
  without repeating.
- [Meta: Override](override) — `Ess.Override.wrap`, the primitive `hijackCallback` is built on.
- [Contract Engine](contract) — why `Ess.Contract.Accept` deliberately does *not* use `Ess.Net.IsAuthority()`
  for its own co-op gate.
- [Essentials (Ess)](index) — the framework index.
