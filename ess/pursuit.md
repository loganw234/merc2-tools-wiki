---
title: "Pursuit & Wanted System"
parent: Essentials (Ess)
nav_order: 19
---

# Pursuit & Wanted System

## Overview

`Ess.Pursuit` (`src/17_pursuit.lua`) wraps the engine's wanted/heat system — the `Pg.*Pursuit*` native family
documented at the raw-engine level on [Pg, "Pursuit/Wanted System"](../namespaces/pg#pursuitwanted-system).
New in **v0.3.1**, what `CHANGELOG.md` itself calls **"the 2026-07-22 bindings-pass harvest"** — a live-probe
mapping of the engine's never-called `luaL_Reg` bindings that landed in the wiki's `namespaces/` pages the
same day this wrapper was written against them. `Ess.Pursuit` is Core-tier only (no `Ess.Raw.Pursuit`, no
`Ess.Easy.Pursuit`); the one Easy-tier one-liner this release adds, `Ess.Easy.World.noPursuit`, lives in a
different file and namespace entirely — see [below](#esseasyworldnopursuitbon--the-one-liner).

Two things about this system are easy to get backwards, and both are pinned down by live testing rather than
by what the names suggest:

- **`.clear()` is the only real reset.** `.restrictAll()`, `.restrictFaction()`, and `.clearRestrictions()`
  read like they'd stop a chase. They don't — see
  [restrictAll, restrictFaction, clearRestrictions](#restrictall-restrictfaction-clearrestrictions--organic-heat-only-not-a-chase-stopper)
  below.
- **`.capLevel()` only ever ratchets down.** Once the level ceiling drops for the session, nothing short of a
  save-load or a full restart raises it again. See
  [capLevel(nLevel)](#caplevelnlevel--a-one-way-ratchet-not-a-tunable) below.

The source file's own header calls these its "two live-confirmed traps... encoded so nobody rediscovers
them." This page keeps that framing front and center rather than burying it in the function reference.

## Status

Verification happened in two layers, on the same day, and it's worth being precise about which claim comes
from which:

1. **The native layer.** `Pg.GetPursuitState`/`SetPursuit`/`ClearPursuitLock`/`SetMaxPursuitLevel`/
   `RestrictAllPursuit`/etc. were themselves live-probed on 2026-07-22 via the WebSocket lua-bridge, *before*
   this wrapper existed. That pass is what actually established the behavioral facts this page repeats — the
   ratchet, the restrict-vs-clear distinction, the idle-state shape — see
   [Pg, "Notes for modders"](../namespaces/pg#notes-for-modders). `17_pursuit.lua`'s own header cites that
   probe directly as its source.
2. **This wrapper layer.** Confirmed separately as part of `Ess` 0.3.1's own release verification. Offline
   first, as part of the whole-release gate (`checkpure` 10/10, `test_bundles` all green, the merged build's
   syntax/loadchecks clean) — though `Ess.Pursuit` itself is thin `pcall`-wrapped native calls with no pure
   Lua logic of its own, so those gates mostly confirm the file loads and parses cleanly rather than
   exercising its behavior. The behavior comes from what followed: **a full in-game pass on the release build
   (2026-07-22) — the whole smoke suite, 42/42 recipes PASS** — including a recipe written specifically for
   this namespace, `control_pursuit` (`samples/recipes/control_pursuit.lua`).

`control_pursuit` is the thorough check, not just a "didn't crash" smoke test: it reads `state()` idle, calls
`start("VZ", 1)` and asserts the resulting `state()` shows `Active` with `Level >= 1`, then calls `clear()`
and asserts `state()` is back to `Level == 0` — a real start → state-read → clear round-trip. (The same
recipe file also exercises the unrelated `Ess.Relations`/`Ess.Easy.Player.ghost` perceivability toggle in one
combined script; that half isn't part of this namespace.)

Two functions get a **lighter** confirmation than that round-trip, and it's worth not blurring the two
together. `CHANGELOG.md`'s targeted-probe notes say `Pursuit.restrict*` and `Easy.World.noPursuit`
**"execute clean"** during that same in-game pass — meaning they ran without erroring, not that this pass
independently re-verified their organic-only gating behavior. That behavioral confirmation — that
`restrictAll`/`restrictFaction` don't stop a running chase and don't block a scripted `.start()` — is the
native-layer finding from point 1 above, which this wrapper's own warnings quote almost verbatim rather than
re-deriving.

`.seconds()`, `.levelTimes()`, `.lock()`, `.custom()`, and `.clearRestrictions()` aren't individually named in
either the round-trip or the "execute clean" bullet — see each one's own confirmation level in
[Granular controls](#granular-controls-seconds-leveltimes-lock-custom) below; most rest on corpus call-site
evidence rather than a live probe of the wrapper call itself.

`.capLevel()` is the deliberate exception, and the omission is documented, not accidental —
`control_pursuit.lua`'s own header explains it outright:

> Deliberately NOT demonstrated: Ess.Pursuit.capLevel -- it is a live-confirmed ONE-WAY ratchet for the whole
> session (nothing raises the ceiling again until a save-load), so a smoke script must never call it.

The ratchet fact itself is still live-confirmed — just at the native layer (point 1 above, and see
[capLevel(nLevel)](#caplevelnlevel--a-one-way-ratchet-not-a-tunable) below). It's the wrapper call in a smoke
test that's correctly avoided, not the underlying finding that's in doubt.

## Ess.Pursuit

Source: `src/17_pursuit.lua`. Every function below wraps its native call in a bare `pcall` and returns a
plain boolean — `true` only means the call didn't error (and, where a `faction` argument is involved, that it
resolved). It is not by itself a semantic confirmation that the effect landed; `.state()`/`.level()` are the
only two calls that let you actually check.

| Function | Signature | Wraps |
|---|---|---|
| `state` | `Ess.Pursuit.state() -> t \| nil` | `Pg.GetPursuitState` |
| `level` | `Ess.Pursuit.level() -> n` | (shortcut on `state()`) |
| `start` | `Ess.Pursuit.start(faction, nLevel) -> ok` | `Pg.SetPursuit` |
| `clear` | `Ess.Pursuit.clear() -> ok` | `Pg.ClearPursuitLock` |
| `seconds` | `Ess.Pursuit.seconds(faction, n) -> ok` | `Pg.SetPursuitSeconds` |
| `levelTimes` | `Ess.Pursuit.levelTimes(n1, n2) -> ok` | `Pg.SetPursuitLevelTimes` |
| `lock` | `Ess.Pursuit.lock(faction, nLevel) -> ok` | `Pg.LockPursuit` |
| `custom` | `Ess.Pursuit.custom(faction, nDur, tSettings) -> ok` | `Pg.SetCustomPursuit` |
| `capLevel` | `Ess.Pursuit.capLevel(nLevel) -> ok` | `Pg.SetMaxPursuitLevel` |
| `restrictAll` | `Ess.Pursuit.restrictAll(bOn) -> ok` | `Pg.RestrictAllPursuit` |
| `restrictFaction` | `Ess.Pursuit.restrictFaction(faction, bOn) -> ok` | `Pg.RestrictPursuitFaction` |
| `clearRestrictions` | `Ess.Pursuit.clearRestrictions() -> ok` | `Pg.ClearPursuitRestrictions` |

**`faction`** (wherever it appears above) goes through a shared internal `factionOf()` helper: a string
resolves the normal way via [`Ess.Guid`](core#essguid--essname) (`"Allied"`, `"China"`, `"Guerilla"`, `"OC"`,
`"Pirate"`, `"VZ"` all work), and an already-resolved guid passes through untouched. Only `.start()` logs on
an unresolved faction (`"Pursuit.start: unknown faction " .. tostring(faction)`) before returning `false`;
`.seconds()`, `.lock()`, `.custom()`, and `.restrictFaction()` just return `false` silently, with no native
call attempted.

### `state()` and `level()` — the read channel

`Ess.Pursuit.state()` is a raw pass-through: `pcall(Pg.GetPursuitState)`, returning the table unmodified if
the call succeeded and actually produced a table, `nil` otherwise. Every field is the same shape
[Pg](../namespaces/pg#pursuitwanted-system) documents at the native level:

```
{ Level, Active, PlayerState, Faction, Locked, SecondsLeft, SecondsLeftInLevel, Duration }
```

Idle (no pursuit running): `Level = 0`, `Active = false`, `PlayerState = "Stopped"`, `Faction = 0xFFFFFFFF`.

`Ess.Pursuit.level()` is a one-line shortcut — `(t and t.Level) or 0` over `state()` — so it's always a plain
number, never `nil`, even before anything has started a pursuit this session.

### `start(faction, nLevel)` — begin a pursuit

Wraps `Pg.SetPursuit(f, nLevel or 1, true)`. `nLevel` defaults to `1`. This genuinely starts a pursuit — a
real countdown timer is seeded, scaling with level (per the native-level probe on
[Pg](../namespaces/pg#pursuitwanted-system): roughly 400s at level 3, ~210s at level 2) — but per the
source's own `NOTE`, **starting a pursuit alone spawns nothing to chase you**: `PlayerState` stays
`"Stopped"` on the `state()` table until faction units are actually nearby and engage. Don't expect visible
pursuers the instant `.start()` returns `true`.

### `clear()` — the one true reset

**This is the only thing that actually clears an active pursuit.** `Ess.Pursuit.clear()` wraps
`Pg.ClearPursuitLock(true)` — live-confirmed (2026-07-22) to drop `state()` straight back to `Level = 0`,
inactive. That's the real off switch.

Several other functions on this page sound like they should stop a chase and don't:
[`.restrictAll()`, `.restrictFaction()`, and `.clearRestrictions()`](#restrictall-restrictfaction-clearrestrictions--organic-heat-only-not-a-chase-stopper)
only gate *future organic* heat — an already-running pursuit keeps running right through all three. If the
actual goal is "make the chase stop right now," `.clear()` is the only call on this page that does it. It's
also the documented way to undo [`.lock()`](#granular-controls-seconds-leveltimes-lock-custom) — there's no
separate unlock call in this API.

### Granular controls: `seconds`, `levelTimes`, `lock`, `custom`

Four thinner wrappers for tuning a pursuit rather than starting or stopping one outright. Confirmation level
varies by function — this group is a mix of corpus-only and native-live-probed:

- **`seconds(faction, n)`** → `Pg.SetPursuitSeconds(f, n or 0, true)` — sets the remaining countdown
  directly. Corpus-confirmed shape only (`resident/mrxfactionmanager.lua`'s
  `Pg.SetPursuitSeconds(uFaction, 5, true)`), not part of the native-level live-probe batch. `n` defaults to
  `0` if omitted, which is **not** the same thing as `.clear()`: it sets the timer to zero rather than
  resetting `Level`/`Active` on the `state()` table.
- **`levelTimes(n1, n2)`** → `Pg.SetPursuitLevelTimes(n1 or 120, n2 or 300)` — corpus-confirmed only; the
  defaults here match the exact `120, 300` the decompiled corpus itself uses
  (`resident/mrxfactionmanager.lua`).
- **`lock(faction, nLevel)`** → `Pg.LockPursuit(f, nLevel or 1)` — corpus-confirmed only. Pins the pursuit at
  a level; `.clear()` is the documented way to undo it, per the source's own comment — there's no separate
  unlock call.
- **`custom(faction, nDur, tSettings)`** → `Pg.SetCustomPursuit(f, nDur or 60, tSettings or {})` — this one
  *is* in the native live-probe batch: per [Pg](../namespaces/pg#pursuitwanted-system), it executes cleanly
  with no error, but no visible effect was observable from an isolated test spot — like the rest of that
  group, it needs an actively engaged pursuit/skirmish to show what it actually changes.

### `capLevel(nLevel)` — a one-way ratchet, not a tunable

⚠ **Live-confirmed one-way session ratchet.** `Ess.Pursuit.capLevel(nLevel)` wraps
`Pg.SetMaxPursuitLevel(nLevel or 1)`. Live testing on 2026-07-22 found exactly one direction it moves: down,
for the rest of the running session. Per [Pg's own notes-for-modders callout](../namespaces/pg#notes-for-modders),
every attempt to raise the ceiling back up failed — a bigger `n` to the same call, a `(faction, n)` form,
`99`, `SetPursuitLevelTimes`, and `SetCustomPursuit` were all tried, and none of them undid it. Only a
save-load or a full restart resets the ceiling.

The wrapper won't let you forget it — every call logs a warning unconditionally, regardless of outcome:

```
Pursuit.capLevel(<n>): ONE-WAY for this session -- nothing raises the ceiling again until a save-load/restart (live-confirmed)
```

Treat `capLevel()` as a session-length commitment ("this mode never exceeds heat 2"), not a dial you turn
back up mid-session. It's the one `Ess.Pursuit` function the framework's own smoke recipe
(`control_pursuit.lua`) deliberately does not call, for exactly this reason — see [Status](#status) above.

### `restrictAll`, `restrictFaction`, `clearRestrictions` — organic heat only, not a chase stopper

**These gate organic heat generation. They do not clear an active chase.** That distinction is confirmed
independently at two levels, both dated 2026-07-22:

- **Native level** — [Pg's notes-for-modders callout](../namespaces/pg#notes-for-modders): `RestrictAllPursuit(false)`
  and `ClearPursuitRestrictions()` are both confirmed **not** to clear an already-active pursuit, and
  `RestrictAllPursuit`/`RestrictPursuitFaction` don't block a scripted `Pg.SetPursuit(...)` call either — both
  only gate the engine's own AI-driven escalation.
- **This wrapper level** — `17_pursuit.lua`'s own header states the identical finding as one of its two named
  traps:

  > `RestrictAllPursuit`/`RestrictPursuitFaction`/`ClearPursuitRestrictions` do NOT clear an active pursuit
  > (despite the names) and do NOT block a scripted `.start()` — they only gate ORGANIC (AI-driven)
  > escalation. The off switch for a live chase is `.clear()`, nothing else.

| Function | Signature | Wraps | Scope |
|---|---|---|---|
| `restrictAll` | `Ess.Pursuit.restrictAll(bOn) -> ok` | `Pg.RestrictAllPursuit` | Every faction (`bOn` defaults `true`) |
| `restrictFaction` | `Ess.Pursuit.restrictFaction(faction, bOn) -> ok` | `Pg.RestrictPursuitFaction` | One faction (`bOn` defaults `true`) |
| `clearRestrictions` | `Ess.Pursuit.clearRestrictions() -> ok` | `Pg.ClearPursuitRestrictions` | Drops every restriction the two above set |

If the actual goal is "stop the chase that's happening right now," that's
[`.clear()`](#clear--the-one-true-reset) — a completely different operation from anything in this section.

## `Ess.Easy.World.noPursuit(bOn)` — the one-liner

Not part of `Ess.Pursuit` itself. `Ess.Pursuit` has no parallel `Ess.Raw.Pursuit`/`Ess.Easy.Pursuit` pair — it
exposes a Core tier only ([the three tiers](index#the-three-tiers)). This one Easy-tier verb instead lives in
`src/94_easy_world.lua`, alongside the rest of `Ess.Easy.World`'s "make the world do X" one-liners
(`removeMapBoundary`, `clearWanted`, `tint`, `brightness`, `hellscape`, `resetAtmosphere` — see
[Ess.Easy](easy)), and it composes `Ess.Pursuit` directly rather than calling any native itself:

```lua
function Ess.Easy.World.noPursuit(bOn)
    if bOn == nil then bOn = true end
    if bOn then
        Ess.Pursuit.clear()
        Ess.Pursuit.restrictAll(true)
    else
        Ess.Pursuit.restrictAll(false)
    end
end
```

One call, two effects: stop whatever chase is currently running (`.clear()`) **and** keep new organic heat
from building back up (`.restrictAll(true)`) — exactly the combination the section above exists to warn you
neither half provides alone. `noPursuit(false)` only lifts the restriction; it does not (and cannot)
retroactively un-clear a pursuit, and — the same caveat as `.restrictAll()` itself —
[it never blocks a scripted `.start()` either way](#restrictall-restrictfaction-clearrestrictions--organic-heat-only-not-a-chase-stopper).

Per `CHANGELOG.md`'s targeted-probe notes, `Easy.World.noPursuit` **"execute[s] clean"** in the same 0.3.1
in-game pass as `Pursuit.restrict*` — confirming the composite call runs without erroring, the same lighter
bar described in [Status](#status) above, not a fresh behavioral re-confirmation of the "stays cold" effect
holding up over time.

### Not the same function as `clearWanted()`

`Ess.Easy.World` already had a pursuit one-liner before 0.3.1: [`clearWanted()`](easy), a one-shot
`Pg.ClearPursuitLock(true)` call with no ongoing restriction attached — the same native `.clear()` above
wraps, called directly and nothing else. **`noPursuit` is new in 0.3.1; `clearWanted` is untouched** — per
`CHANGELOG.md`'s own parenthetical confirming it wasn't touched by this release. The difference that matters:

| | `clearWanted()` | `noPursuit(true)` |
|---|---|---|
| Clears the current chase | Yes | Yes |
| Keeps new organic heat off afterward | No — heat can build right back up | Yes, via `restrictAll(true)` |
| Reversible in the same call family | N/A — one-shot | Yes — `noPursuit(false)` lifts the restriction |

Reach for `clearWanted()` for a single instant reset; reach for `noPursuit(true)` when a mod wants the player
to *stay* cold (a safe-zone hub, a cutscene) until it explicitly says otherwise.

## See also

- [Pg — Pursuit/Wanted System](../namespaces/pg#pursuitwanted-system) and its
  [Notes for modders](../namespaces/pg#notes-for-modders) — the native-level ground truth this whole
  namespace wraps, including the same-day live probes both traps above are built on.
- [Ess.Easy](easy) — the full one-liner catalog, including the pre-existing `clearWanted()`.
- [Core Primitives](core) — [`Ess.Guid`](core#essguid--essname) (faction name resolution) and
  [`Ess.Log`](core#esslog) (the `capLevel` warning and `start`'s unknown-faction log).
- [Essentials (Ess)](index#the-three-tiers) — "The three tiers," for why this namespace is Core-only with its
  one Easy verb parked in a different namespace instead of a parallel `Ess.Easy.Pursuit`.
- [Reactive Hooks & Hotkeys](reactive-hotkeys) — a sibling 0.3.x-vintage focused-namespace page with the same
  "confirmed live, feature by feature, precision over blanket claims" structure this page follows.
