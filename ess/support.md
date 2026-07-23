---
title: "Support & Call-ins"
parent: Essentials (Ess)
nav_order: 14
---

# Support & Call-ins

## Overview

`Ess.Support` (`58_support.lua`) lifts the combat call-ins — airstrikes, artillery, bombing runs, gunship
runs, reinforcements — out of [`Ess.Contract`](contract)'s support system (`82_contract_encounter.lua`'s
`SUPPORT_EFFECTS`, documented in full on [Support Effects & Triggers](../contract-framework/support-effects-and-triggers))
so any script can fire one **anywhere, standalone, with no contract running**. `Ess.Easy.Airstrike` is a
tiny beginner preset built on top of it.

Every call is **fire-and-forget**: it schedules its own timed ordnance spawn(s)/flyby(s) and returns
immediately. Per the source's own framing, the spawned shells and flyby vehicles are engine-managed
one-shots, so there's nothing to track or tear down — none of these functions return a handle.

All positions are world `(x, y, z)`. Every function takes an `opts` table (or `nil`) as the last argument;
an `opts.owner` field, where present, is a **faction NAME** (`"China"`, `"Allied"`, etc.), resolved
internally via [`Ess.Guid`](core#essguid--essname) to tag who "fired" the effect so the game attributes
damage/kills correctly — omit it for unattributed. Template/ammo/vehicle strings default to the exact
values `Ess.Contract`'s support system already uses.

A few implementation details worth knowing before the per-function breakdown:

- Every native call in this file is wrapped in a **bare `pcall`** — not `Ess.Safe.call`/`.quiet` (see
  [Ess.Safe](core#esssafe)) the way most of the rest of `Ess` is. Failures are silently swallowed, not
  logged.
- Staggered/delayed spawns go through a private `after(delay, fn)` helper — a bare
  `pcall(Event.Create, Event.TimerRelative, { delay }, fn)`, not registered on any
  [`Ess.Track`](tracking#esstrack) tracker or built via [`Ess.Event.on`](tracking#essevent). Consistent
  with the "nothing to clean up" framing above: these are one-shot timers with no cancel path, not
  something you'd ever need to cancel early.
- `Ess.Support.artillery`'s scatter uses one **module-level** [`Ess.RNG`](core#essrng) stream
  (`Ess.RNG.new()`, created once when `58_support.lua` loads, time-seeded) — shared across every
  `artillery` call for the rest of the session, not a fresh generator per call.

## Status

**Confirmed live as of 0.3.0.** `CHANGELOG.md`'s `[0.3.0]` entry — a dated, versioned verification record
(the maintainer's own first-party account, not a captured log/transcript) — is explicit: *"`Ess.Support` —
all 7 call-ins fired clean (`shell`, `artillery`, `airstrike`, `bombingrun`, `gunship`, `reinforce`,
`Easy.Airstrike.at`), with `reinforce` separately confirmed actually delivering units."* That supersedes this
namespace's prior `[Unreleased]`-era status ("not yet in-game smoke-run... test in a live game, then bump to
`0.3.0` to release") — the live pass happened, and that's what 0.3.0 shipped on.

This confirms the **wrapper layer itself**, not just the natives underneath it. The natives every function
here composes — `Airstrike.SpawnOrdnance`, `Airstrike.Flyby` (see [Airstrike](../namespaces/airstrike)), and
`MrxCopterDrop.Create` (see [MrxCopterDrop](../resident/mrxcopterdrop)) — were already independently confirmed
elsewhere in this wiki via `Ess.Contract`'s support-effects system; 0.3.0 is what extends that same live
confirmation to this standalone wrapper, closing the "confirmed by association only" gap that used to apply
here. That's separate from the `call_in_support` sample recipe (`samples/recipes/call_in_support.lua`)
exercising `airstrike`/`artillery`/`gunship` — its own automated smoke-check still only asserts
`type(Ess.Support.artillery) == "function"` etc. (API shape, not behavior); the live confirmation above comes
from the 0.3.0 verification pass itself, not from that recipe.

The `Ess.Safe.template` guard added to `Ess.Support.reinforce`'s copter path (see [Hardening](#hardening-the-copter-drop-guard)
below) is a narrower claim the 0.3.0 verification summary doesn't separately call out — `CHANGELOG.md` still
lists the guard's addition under its pre-release, **offline-only** hardening audit, distinct from the
live-verified list above. `reinforce` firing live and delivering units (above) confirms the function; it
doesn't by itself confirm this specific guard's blank-template safety net was the thing exercised.

## Ess.Support

| Function | Signature | opts |
|---|---|---|
| `shell` | `Ess.Support.shell(x, y, z, opts)` | `ammo` (default `"Gunship Shell"`), `dropHeight` (default `220`), `owner` |
| `artillery` | `Ess.Support.artillery(x, y, z, opts)` | `count` (default `5`), `radius` (default `14`), `stagger` (default `0.35`), plus `ammo`/`owner` (passed through to each `shell` call) |
| `airstrike` | `Ess.Support.airstrike(x, y, z, opts)` | `vehicle` (default `"Support Vehicle (Autogunship)"`), `altitude` (default `120`), `speed` (default `55`) |
| `bombingrun` | `Ess.Support.bombingrun(x, y, z, opts)` | `vehicle` (default `"Support Vehicle (A10)"`), `ammo` (default `"Bomb"`), `count` (default `3`), `altitude` (default `150`), `speed` (default `160`), `owner` |
| `gunship` | `Ess.Support.gunship(x, y, z, opts)` | `template` (default `"AH1Z"`), `count` (default `3`), `stagger` (default `1.6`), `spread` (default `45`), `altitude` (default `55`), `speed` (default `45`) |
| `reinforce` | `Ess.Support.reinforce(x, y, z, opts)` | `faction`, `units` (array of template strings), `deliver` (`"copter"` \| `"paradrop"` \| anything else/omitted = direct), `vehicle`/`altitude`/`speed` (paradrop transport pass only) |

### `shell(x, y, z, opts)`

One falling shell — composes a single `pcall(Airstrike.SpawnOrdnance, opts.ammo or "Gunship Shell", x, y +
(opts.dropHeight or 220), z, 0, -100, 0, "impact", 1, ownerGuid(opts.owner))`: spawned `dropHeight` units
above the target point with a straight-down (`-100`) velocity, impact-fused. The source header describes
this as "the primitive the rest build on," but that's only literally true of `artillery` below — `airstrike`,
`bombingrun`, `gunship`, and `reinforce` each compose different natives directly (`Airstrike.Flyby`,
`MrxCopterDrop.Create`, `Ess.Object.spawn`) rather than calling `shell` themselves.

There's no matching named effect in `Ess.Contract`'s `def.support` vocabulary — `shell` is new here, the
single-round primitive `artillery` used to build internally without exposing it on its own.

### `artillery(x, y, z, opts)`

`count` shells rain onto the area, each a separate `Ess.Support.shell(x + dx, y, z + dz, opts)` call
scheduled `stagger * (i - 1)` seconds apart via `after()` (so shell 1 fires immediately). `dx` and `dz` are
each drawn **independently** from the shared module-level RNG, uniform in `[-radius, radius]` — despite the
name, this scatters shells across a `2*radius`-wide **square**, not a circle of radius `radius`. `ammo` and
`owner` (if set in `opts`) are forwarded unchanged to every `shell` call.

Matches `def.support`'s `artillery` effect (see [Support Effects & Triggers](../contract-framework/support-effects-and-triggers))
one-for-one, including the ~0.35s stagger.

### `airstrike(x, y, z, opts)`

A single `pcall(Airstrike.Flyby, opts.vehicle or "Support Vehicle (Autogunship)", x - 50, z + 300, x, z, y +
(opts.altitude or 120), opts.speed or 55)` — **no drop callback**, so this is a pure visual pass with no
ordnance of its own (see [Airstrike](../namespaces/airstrike)'s `Flyby` row). The flight path is fixed
relative to the target regardless of player facing: it starts 50 units back on X and 300 units out on +Z,
then flies straight to `(x, z)`.

This is the `flyby` / `airstrike` effect from `def.support`, same defaults.

### `bombingrun(x, y, z, opts)`

An aircraft makes one pass and walks a stick of `count` bombs across the target. `pcall(Airstrike.Flyby,
vehicle, x - 350, z + 350, x, z, alt, speed, drop)` spawns the plane with a `drop` callback (`alt = y +
(opts.altitude or 150)`); if that `pcall` succeeds, the returned jet guid is captured as `uJet`. `drop()`
then schedules `count` bomb spawns `0.14s` apart via `after()`; each one re-reads the jet's **live** position
via `pcall(Object.GetPosition, uJet)` at fire time (falling back to the original static `x, alt, z` if that
read fails, e.g. `uJet` was never set), so the bomb stick actually follows the plane's real flight path
rather than a straight line computed up front. Each bomb: `pcall(Airstrike.SpawnOrdnance, opts.ammo or
"Bomb", jx, jy, jz, 0, -60, 0, "impact", 1, ownerGuid(opts.owner))`.

Matches the `bombingrun` effect in `def.support`, including the "re-reads live position each drop" behavior
already documented there.

### `gunship(x, y, z, opts)`

`count` helicopters pass over, fanned out in both position and timing. For each `i`, `off = (i - 1) *
opts.spread` (default spread `45`), scheduled `stagger * (i - 1)` seconds apart (default stagger `1.6`) via
`after()`: `pcall(Airstrike.Flyby, opts.template or "AH1Z", x - 60 - off, z + 300 + off, x + off, z, y +
(opts.altitude or 55), opts.speed or 45)` — no drop callback, a visual pass only, same as `airstrike`. The
growing `off` term shifts each subsequent helicopter's start point and destination so the wave doesn't spawn
into itself.

This corresponds to the `heli` effect in `def.support` — note the rename: the contract-framework effect key
is `heli`, the standalone function here is `Ess.Support.gunship`.

### `reinforce(x, y, z, opts)`

Units arrive, placed on a 3-wide, 4-unit-spaced grid around `(x, y, z)`
(`ox = ((i - 1) % 3 - 1) * 4, oz = math.floor((i - 1) / 3) * 4` for unit `i`). `opts.faction` is looked up
in a fixed 2-letter map (`{ Allied = "AL", China = "CH", Guerilla = "GR", OC = "OC", Pirate = "PR", VZ = "VZ" }`)
— used **only** by the `"copter"` delivery path below, since that's the code `MrxCopterDrop.Create` expects;
an unrecognized faction string passes through as-is (assumed to already be a valid code), and an omitted
one defaults to `"VZ"`.

Three delivery modes (`opts.deliver`):

- **`"copter"`** — every `opts.units[i]` spawns at once (no stagger) via `pcall(MrxCopterDrop.Create, fac,
  tmpl, x + ox, y, z + oz, false)`, guarded immediately beforehand by
  [`Ess.Safe.template(tmpl)`](core#esssafe) — see [Hardening](#hardening-the-copter-drop-guard) below.
- **`"paradrop"`** — first flies a transport over via `pcall(Airstrike.Flyby, opts.vehicle or "Support
  Vehicle (Paradrop_AL)", x - 350, z + 350, x, z, y + (opts.altitude or 180), opts.speed or 140)` (no drop
  callback), then spawns each unit after a `1.5 + 0.2 * i` second delay so it lands roughly under the
  passing transport. Despite the name, the actual per-unit spawn is the **same guarded direct spawn** as
  the branch below (just timed to the flyby) — there's no literal parachute/chute object attached to the
  unit.
- **anything else / omitted ("direct")** — every unit spawns immediately, no stagger, via
  [`Ess.Object.spawn(tmpl, x + ox, y, z + oz)`](identity-query#essobject) (blank-template-safe internally,
  no yaw specified).

Matches the `reinforce` effect in `def.support` one-for-one on the delivery-mode semantics.

### Hardening: the copter-drop guard

Per `CHANGELOG.md`'s `[0.3.0]` "Hardening" notes: `reinforce`'s `"copter"` path now validates the template
with [`Ess.Safe.template`](core#esssafe) before calling `MrxCopterDrop.Create` — the direct-spawn path was
already guarded (`Ess.Object.spawn` is blank-template-safe on its own), but the copter path wasn't, and
`MrxCopterDrop.Create` spawns internally the same way a raw `Pg.Spawn` does. **A blank template there can
hard-CTD past the surrounding `pcall`** — a native crash inside the engine's own spawn code isn't something
Lua's `pcall` can catch, the same footgun documented for `Pg.Spawn` elsewhere on this wiki. Guarding the
template string *before* the call is the only fix; there's no way to make the call itself safe after the
fact.

## Ess.Easy.Airstrike

Three one-tap presets — a jet pass plus a few shells — over `Ess.Support` above.

| Function | Signature | Does |
|---|---|---|
| `at` | `Ess.Easy.Airstrike.at(x, y, z)` | `Ess.Support.airstrike(x, y, z)` (all defaults) immediately followed by `Ess.Support.artillery(x, y, z, { count = 4, radius = 10 })` — one flyby plus 4 shells scattered in a 20×20-unit square. |
| `onTarget` | `Ess.Easy.Airstrike.onTarget(i)` | Resolves [`Ess.Player.targetUnderReticle(i or 0)`](identity-query#essplayer) for the guid, then separately re-reads its position via [`Ess.Object.pos(u)`](identity-query#essobject) (rather than using the `x, y, z` `targetUnderReticle` already returns) and calls `.at()` on it if that succeeds. |
| `onMe` | `Ess.Easy.Airstrike.onMe(i)` | Reads the player's own position via [`Ess.Player.pose(i or 0)`](identity-query#essplayer) and calls `.at()` on it — a deliberate danger-close self-strike; the source's own comment calls it "for the brave / the cinematic." |

All three no-op quietly if the position lookup fails (no target under the reticle, no character for player
slot `i`).

`.at()` is one of the 7 call-ins named in the 0.3.0 live-verification pass (see [Status](#status) above).
`.onTarget()`/`.onMe()` aren't separately named there — both are thin position-resolvers that hand off to
`.at()` internally, so the call-in itself is covered, but the reticle-lookup/player-position step wrapping it
hasn't been independently confirmed live.

## See also

- [Ess.Easy](easy) — `Ess.Easy.Spawn.airstrike(sRound)` is the simpler, older beginner-tier preset (a single
  shell dropped on your own head) that predates `Ess.Support`/`Ess.Easy.Airstrike`; still documented there,
  still current.
- [Encounter Toolkit](encounter-toolkit) — the sibling gameplay-scripting systems (`AIOrders`, `Relations`,
  `Triggers`, `Sandbox`, `Layers`) extracted from the same `Ess.Contract` internals.
- [Core Primitives](core) — [`Ess.Safe`](core#esssafe) (the `reinforce` copter-path guard), `Ess.RNG`
  (artillery's scatter), `Ess.Guid` (the `owner` resolution).
- [Identity & World Query](identity-query) — `Ess.Player`/`Ess.Object`, what `Ess.Easy.Airstrike.onTarget`/
  `.onMe` and `reinforce`'s direct-spawn path build on.
- [Contract Engine](contract) — `Ess.Contract`, the system these call-ins were lifted out of.
- [Support Effects & Triggers](../contract-framework/support-effects-and-triggers) — the original
  `def.support` vocabulary (`artillery`, `flyby`/`airstrike`, `bombingrun`, `heli`, `reinforce`) this
  namespace is a standalone lift of.
- [Airstrike](../namespaces/airstrike) — `Airstrike.SpawnOrdnance`/`Airstrike.Flyby`, the engine natives
  every function above except `reinforce`'s copter path is built on.
- [MrxCopterDrop](../resident/mrxcopterdrop) — the native module `reinforce`'s `"copter"` delivery path
  calls into (`MrxCopterDrop.Create`), including the hardcoded winch/drop-height details.
- [Support & Airstrikes](../resident/cat-support-airstrikes) — the full native resident-module family
  (`MrxArtillery`, `MrxBombingRun`, `MrxGunship`, `MrxCopterDrop`, `paradrop`, etc.) this namespace mirrors
  in standalone Lua.
