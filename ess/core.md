---
title: Core Primitives
parent: Essentials (Ess)
nav_order: 1
---

# Core Primitives

## Overview

This page covers the bottom of the [Ess](index) stack: the pieces every other namespace is built out of,
rather than the ones you'd reach for to move an object or spawn a vehicle. Ten source files:
`00_core.lua` (`Ess.Log`, `Ess.DEBUG`, `Ess.Safe`, `Ess.lastError`, `Ess.Table`, `Ess.Guid`/`Ess.Name`),
`01_math.lua` (`Ess.Math`), `02_str.lua` (`Ess.Str`), `03_color.lua` (`Ess.Color`), `04_vec.lua` (`Ess.Vec`),
`05_sys.lua` (`Ess.Sys`), `06_atmosphere.lua` (`Ess.Atmosphere`), `22_state.lua` (`Ess.State`,
`Ess.SaveVar`), `53_rng.lua` (`Ess.RNG`), and `98_stop.lua` (`Ess.stop`/`Ess.stopAll`/`Ess.Track:any`,
covered [below](#essstop)). `00_core.lua` loads first (the `00_` prefix is deliberate) and has zero
dependencies on the rest of Ess — literally everything else in the framework depends on it; `98_stop.lua`
is the last file in the whole build, for reasons covered in its own section below.

`Ess.Safe`'s diagnostic layer (`Ess.DEBUG`, `Ess.Safe.reject`/`.named`, `Ess.lastError`,
`Ess.Safe.stats`/`.reset`) and the universal teardown `Ess.stop`/`Ess.stopAll`/`Ess.Track:any` are both new
in **v0.4.0**, which `CHANGELOG.md` headlines as **"the diagnosability pass."** 0.4.1 was a pure packaging
fix for 0.4.0's release zip — no framework code changed, so if you only ever installed 0.4.0's `1_Ess.lua`,
nothing on this page is different. 0.4.2 is unrelated tooling: it generates node definitions for a new
visual node-editor from the API surface, again with no framework-code change, and isn't covered on this
page.

**v0.5.0** adds two whole namespaces to this page — [`Ess.Sys`](#esssys) and
[`Ess.Atmosphere`](#essatmosphere), neither of which existed in 0.4.2 — and substantially widens the
`Ess.DEBUG` guard-rejection channel across the whole framework (see [below](#essdebug--two-channels-of-silence)).
0.5.1 and 0.5.2 change nothing here: 0.5.1 is a data-only release (a field added to `api/natives.json` for
downstream tooling) and 0.5.2 ships the UI kit's missing `ess_ui.gfx` movie in `vz-patch.wad`. Confirmed
against the repo: the only change to `src/` between 0.5.1 and 0.5.2 is the version string itself.

`Ess.Str`, `Ess.Color`, and `Ess.Vec` are pure Lua — no engine calls, no dependencies on the rest of
`Ess` — so unlike most of this framework they can be (and are) execute-verified offline, without the game
running, via `tools/checkpure.py` (a [lupa](https://pypi.org/project/lupa/)-embedded-Lua test harness that
loads the real `src/*.lua` files and asserts against them). Where this page says a function is
"execute-verified offline," that's the method: real source, run outside the game, not a claim of a live
in-game test.

Almost none of these namespaces carry a three-tier `Raw`/Core/`Easy` split — they're small, single-purpose
utilities where a beginner/advanced gap doesn't really exist. You just call them. The one exception is
[`Ess.Atmosphere`](#essatmosphere), which genuinely is the Core tier beneath a handful of `Ess.Easy.World`
one-liners; there is still no `Raw` tier under it.

## Ess.Log

```lua
Ess.Log(msg)
```

Every `Ess.*` message goes through this so log lines are consistently prefixed (`"[Ess] " .. tostring(msg)`)
and easy to grep out of `lua_loader_printf.log`. It routes through `Loader.Printf`, and is guarded so a
missing `Loader` global can't make `Ess.Log` itself throw.

## Ess.Safe

The single most duplicated shape in the whole project is `local ok, r = pcall(...); if not ok then
Loader.Printf(...) end`. `Ess.Safe` fixes it in one place — and as of **v0.4.0**, it's also the mechanism the
whole diagnostic layer below runs through. That's a correction, not a new design: `Ess.Safe` had been
documented since 0.1.0 as this project's most duplicated shape, but the framework's own code only actually
routed through it **once** — an oversight, not a decision — until 0.4.0 made it the load-bearing mechanism it
always should have been.

It's fixed-arity — **up to 6 return values as of v0.4.0, up from 4** — rather than a generic
table-pack/unpack dance, and still allocates nothing: these calls sit inside per-frame heartbeats, where a
throwaway table per engine call would be a real cost. The widest native return anywhere in this corpus is 4
values (`Player.GetTargetUnderReticle`'s x, y, z, guid — see
[`Ess.Player.targetUnderReticle`](identity-query#essplayer)), so 6 is headroom rather than a fix for a
known-truncated case — confirmed live at 6 values through the game's own VM.

| Function | Signature | Notes |
|---|---|---|
| `call` | `Ess.Safe.call(fn, ...) -> ok, a, b, c, d, e, f` | Wraps any engine call — a function reference plus its args, or a zero-arg closure for a multi-statement body. Logs once via `Ess.Log` on failure, `Ess.DEBUG` or not — for a call whose failure is genuinely abnormal. |
| `quiet` | `Ess.Safe.quiet(fn, ...) -> ok, a, b, c, d, e, f` | Same shape, for calls expected to fail sometimes as part of normal control flow (e.g. probing whether an object has a label, reading a dead guid's position). **As of v0.4.0 this means "quiet unless you asked to hear it," not "invisible"** — previously these failures were unconditionally undiagnosable; now the failure is always counted, and logs once `Ess.DEBUG` is on. |
| `named` | `Ess.Safe.named(sLabel, fn, ...) -> ok, a, b, c, d, e, f` | New in v0.4.0. `.quiet` with the label supplied up front — the only way to attribute a **closure's** failure, since a closure is a fresh function object every call and can never appear in the reverse name-map `.call`/`.quiet` use to label a failure automatically (see `Ess.DEBUG` below). |
| `reject` | `Ess.Safe.reject(sLabel, sReason) -> nil` | New in v0.4.0. Records a **guard rejection** (see `Ess.DEBUG` below) instead of a thrown failure — call it where an Ess wrapper gives up on its own arguments, before the engine is ever touched: `if not uGuid then return Ess.Safe.reject("Ess.Object.heal", "no guid") end`. Always returns `nil`, so that stays one line. Because Ess is the one deciding, the logged reason is specific ("no guid") rather than a generic engine error string. |
| `string` | `Ess.Safe.string(ok, val, fallback) -> s` | Only trust a native return as a string if it really is one — some calls return an unexpected type (bare userdata) on edge cases. Pass `Ess.Safe.call`'s own `(ok, val)` straight through: `Ess.Safe.string(Ess.Safe.call(Object.GetName, u))`. `fallback` defaults to `"?"`. |
| `template` | `Ess.Safe.template(sTemplate) -> bool` | The canonical "is this actually a spawnable template name" guard: `true` only for a non-empty, non-whitespace string. Unaffected by anything else on this page — unchanged since 0.3.0. |

`Ess.Safe.template` exists because a blank/whitespace/non-string template name makes `Pg.Spawn` (and
everything built on it) hard-CTD the engine in native C++ — and `pcall` cannot catch a native crash, only a
Lua error, so the check has to happen *before* the call. That exact guard used to be re-inlined by hand in
roughly six places (`Object.spawn`, `Vehicle.followGhost`, `Bones.attachFX`, `UI.Menu`'s `ctx:spawn`,
`Contract._safeSpawn`), and two spawn paths — the original `Contract` `Pg.Spawn` gap and, more recently, the
copter path in `Ess.Support.reinforce` — missed it by hand before this existed. `Ess.Safe.template` is one
call instead of re-deriving the guard: see [Ess.Support](support) for the `reinforce` consumer. Confirmed
live in the 0.3.0 release pass, on top of its own offline coverage via `tools/checkpure.py`; existing inline copies aren't required to
migrate, just new code.

### Ess.DEBUG — two channels of silence

```lua
Ess.DEBUG = false   -- default; flip true from a script, or live over the bridge
```

New in **v0.4.0**. Ess's oldest structural weakness is that it fails *silently* on purpose — a wrapper's
whole job is to return `nil` instead of propagating a problem, so a call with a stale guid or a `nil`
argument produces no log line, no error, and no visible effect. That's the single most common "why isn't my
mod doing anything" wall. `Ess.DEBUG` opens it up: flip it true and everything Ess quietly gave up on starts
reporting itself. It's read at call time, not captured, so flipping it mid-session takes effect immediately,
and it survives a level reload.

There are two separate channels, because there are two genuinely different silences:

- **Thrown failures** — an engine call raised a Lua error and a `pcall` swallowed it. Recorded by
  `Ess.Safe.call`/`.quiet`/`.named` above.
- **Guard rejections** — Ess looked at the arguments, decided the call couldn't work, and returned early
  *without ever calling the engine* (a `nil` guid, a blank spawn template, an order with no destination).
  Recorded by `Ess.Safe.reject()` above.

**CONFIRMED LIVE 2026-07-25:** 14 deliberately-malformed native calls — nil/garbage/stale guids across
`Object`, `Player`, `Vehicle`, `Human`, `Ai`, `Marker`, `Camera`, `Sys`, and `Pg` — threw **zero** Lua errors.
They fail safe, returning `nil` or, for a stale guid, stale values. That's the important framing point: the
*guard-rejection* channel is what actually answers a beginner's "nothing happened," since a diagnostic built
only on caught errors would have been silent in exactly the case it exists for.

This is **not** a reason to drop the `pcall` guards, and none were dropped: the crash cases documented
elsewhere on this wiki and in `CONTRIBUTING.md` were recorded defensively — any observed crash written down
as a fact, deliberate breadth over pinpoint reproduction — so a rare throw in some other location or game
state stays entirely plausible. Both channels are load-bearing; only their relative frequency is now known.

**v0.5.0 widened the guard-rejection channel a great deal.** `CHANGELOG.md` records it in a single line —
"several silent-failure paths now report on the `Ess.DEBUG` channel instead of returning a bare `false`" —
but the scale is worth stating, because it changes how much of the framework `Ess.DEBUG` can actually
explain. Counted against the real `src/`, `Ess.Safe.reject` call sites went from **18 across 7 files** in
0.4.2 to **87 across 16 files** in 0.5.2. Nothing about the two-channel model changed; there is simply far
more reaching the guard-rejection channel than there was.

Most of the growth is in the HUD/UI-facing namespaces 0.5.0 built out — `Ess.Hud` (20 rejection sites),
`Ess.Pda` (16), `Ess.Sound` (9), `Ess.Minimap` (8), `Ess.Shop` (5). Only `Ess.Pda`, `Ess.Minimap` and
`Ess.Shop` are *new* files in 0.5.0; `Ess.Hud` and `Ess.Sound` already existed in 0.4.2 and carried **zero**
rejection sites between them, so those 29 are growth inside existing namespaces. Older namespaces gained
them too: [`Ess.On`](reactive-hotkeys) went 5 → 8 and `Ess.Raw.Mark` ([Markers](mark)) 0 → 5. Two related
sweeps land in the same release:

- **Bare `pcall` around engine calls was converted to `Ess.Safe.*`.** The sweep found 45 bare-`pcall` sites
  in that release's own code and converted the **26** that wrapped an *engine* call. A bare `pcall` swallows
  the failure completely: no counter, no `Ess.lastError`, nothing under `Ess.DEBUG`. The 19 it deliberately
  left are all `pcall(userCallback, ...)`, wrapping a **mod author's own callback** — a bug in your code is
  not an `Ess` failure, and recording it would make `Ess.Safe.stats()` blame the framework for it.
- **37 closures that were being passed to `Ess.Safe.quiet` moved to `Ess.Safe.named`.** This is the subtle
  one, because the old form looks correct. A closure is a fresh function object on every call, so it can
  never appear in the reverse name map and every one of them tallied as an undifferentiated `"closure"` —
  recorded, but nearly as undiagnosable as not recorded. This matters most for the colon-called natives
  (the entire `Hud`/`Pda` surface), which cannot be passed as a function reference at all.

**The sweep is not total, and the wiki should not imply it is.** Checked against current `src/`, several
older files still wrap *engine* calls in a bare `pcall` — `21_input.lua`'s PDA-widget calls and
`30_track.lua`'s `Hud.Radar:RemoveObjective`/`Pda.Map:RemoveBlip` teardowns among them. A failure in one of
those is still invisible to `Ess.DEBUG`, exactly as it was before 0.4.0.

A worked example of what a rejection buys you is [`Ess.Human.setState`](identity-query#esshuman), added in
the same release: the native reports nothing for a valid posture *and* nothing for garbage, so the
wrapper's whitelist rejection is the only place in the entire chain where a misspelled posture can ever
surface.

### Reading it back: Ess.lastError, Ess.Safe.stats, Ess.Safe.reset

| Function | Signature | Notes |
|---|---|---|
| `Ess.lastError` | `Ess.lastError() -> { msg, label, count, rejected } \| nil` | The most recent swallowed failure, thrown or rejected (`rejected` is only present and `true` for a guard rejection). This is how you read the message a failed `Ess.Safe.call`/`.quiet`/`.named` deliberately doesn't hand back — see the compatibility note below. |
| `Ess.Safe.stats` | `Ess.Safe.stats() -> tArray, nTotal` | Per-callsite tallies, worst first — but only for failures recorded while `Ess.DEBUG` was on. The second return is the *unconditional* session total, counted regardless of `Ess.DEBUG`, so a short (or empty) array next to a large total means "plenty failed, but before you turned DEBUG on." Throws and rejections share one tally on purpose, so it reads as a single "what's going wrong" list rather than two separate ones. |
| `Ess.Safe.reset` | `Ess.Safe.reset()` | Clears the tally, the session total, and the last error. Also drops the cached function-name map described below, so it rebuilds from scratch. |

The reverse name map (`function reference -> "Namespace.FnName"`, used to label a *thrown* failure when no
explicit label was given) is a snapshot of whatever engine globals existed at first use — built lazily, on
the first failure while `Ess.DEBUG` is on, so it costs nothing when debug is off. **CONFIRMED LIVE:** 1,889
functions mapped, correct on 4/4 spot checks (`Object.GetPosition`, `Player.GetLocalCharacter`, `Ai.Goal`,
`Pg.Spawn`), including one-level-deep nested tables like `Graphics.Camera`. A closure can never appear in
this map — it's a fresh function object every call — which is exactly why `Ess.Safe.named` exists above: the
only way to attribute one. **CONFIRMED LIVE:** `type(_G.debug)` is `nil` on this engine — the `debug` library
is absent outright (zero occurrences anywhere in the decompiled corpus, not merely unused), so a
`debug.getinfo` fallback for naming closures was confirmed dead code and removed rather than kept looking
like it might work. `Ess.Safe.reset()` drops the map for exactly this reason: it's a snapshot taken once, so
a namespace that populates after the snapshot (e.g. late in a level load) would otherwise read as an
unhelpful `"closure"`-style miss forever.

**Fully backwards compatible.** `Ess.Safe.call`/`.quiet` keep returning a bare `false` on failure —
deliberately *not* `pcall`'s own `false, errMessage` shape. Handing the error string back in the slot every
caller reads as "the value" would turn a clean nil-on-failure into a garbage-on-failure footgun. Read the
message via `Ess.lastError()` instead.

## Ess.Table

```lua
Ess.Table.compact(t) -> t
```

Rebuilds a numeric array densely, mutating `t` in place (and also returning it, for chaining). This fixes a
real bug: `t[#t] = nil` to "pop" the last element leaves a `nil` HOLE, and Lua's `#` operator is undefined on
a table with a hole — that desyncs `#`/`ipairs`/`table.insert` and can silently drop or duplicate entries
downstream. Prefer `table.remove` in new code (it never leaves a hole); reach for `compact` when a hole
already happened — someone else's code, or a sparse table you're about to treat as a dense array — and you
need it fixed before continuing. Non-numeric keys in `t` are left untouched.

Beyond `compact`, `Ess.Table` also carries the basic collection helpers the Lua 5.1 stdlib omits — pure
Lua, no dependencies, execute-verified offline via `tools/checkpure.py`. `map`/`filter`/`find`/`indexOf`
work on the **array part** only (`ipairs`); `keys`/`values`/`count`/`isEmpty`/`contains`/`copy`/`merge`
walk the **whole table** (`pairs`), since `#t` only ever sees the array part and would silently miss
map-style keys. All of them are non-mutating except `merge` (and `compact` above).

| Function | Signature | Notes |
|---|---|---|
| `keys` | `Ess.Table.keys(t) -> { k, ... }` | Every key in `t`, array or not, order unspecified. |
| `values` | `Ess.Table.values(t) -> { v, ... }` | Every value in `t`, order unspecified. |
| `count` | `Ess.Table.count(t) -> n` | Total number of entries via `pairs` — unlike `#t`, correct even with non-array keys or holes. |
| `isEmpty` | `Ess.Table.isEmpty(t) -> bool` | `next(t) == nil`. |
| `contains` | `Ess.Table.contains(t, val) -> bool` | Is `val` any value in `t` (`pairs`, so array or keyed)? |
| `indexOf` | `Ess.Table.indexOf(t, val) -> i \| nil` | First array index (`ipairs`) whose value equals `val`. |
| `map` | `Ess.Table.map(t, fn) -> { ... }` | New array: `fn(v, i)` for each array element. |
| `filter` | `Ess.Table.filter(t, fn) -> { ... }` | New array of elements where `fn(v, i)` is truthy — densely packed, never a hole. |
| `find` | `Ess.Table.find(t, fn) -> v, i \| nil` | First array element (and its index) where `fn(v, i)` is truthy. |
| `reduce` | `Ess.Table.reduce(t, fn, init) -> acc` | Folds the array to one value: `acc = fn(acc, v, i)` starting from `init`. |
| `slice` | `Ess.Table.slice(t, i, j) -> { ... }` | New array of `t[i..j]`, 1-based inclusive. `i`/`j` default to `1`/`#t` and are clamped into range. |
| `reverse` | `Ess.Table.reverse(t) -> { ... }` | New array with element order flipped. |
| `copy` | `Ess.Table.copy(t) -> { ... }` | Shallow copy — nested tables are shared, not cloned. |
| `merge` | `Ess.Table.merge(dst, src) -> dst` | Shallow-copies `src`'s keys onto `dst` (`src` wins on conflicts), **mutating and returning `dst`**. `src == nil` is a no-op. |

## Ess.Guid / Ess.Name

`Pg.GetGuidByName` and `Sys.GuidToString` each have both a namespaced form and a bare-global alias on this
engine — a confusing duplicate surface. Use these instead of remembering which:

| Function | Signature | Notes |
|---|---|---|
| `Ess.Guid` | `Ess.Guid(name) -> uGuid \| nil` | `pcall`-wrapped `Pg.GetGuidByName`. |
| `Ess.Name` | `Ess.Name(uGuid) -> sHash \| nil` | `pcall`-wrapped `Sys.GuidToString` — **confirmed to throw outright on at least one real object**, hence the wrap. |

`Ess` has no wrapper for the inverse direction — reach for the raw native, [`Sys.StringToGuid`](../namespaces/sys),
directly.

**A `uGuid` is Lua `userdata`, not a number or a string** — worth stating plainly since it trips people up.
`tostring(uGuid)` gives an opaque, non-reusable `"userdata: 0x...."` that cannot be turned back into a
working guid; there is no Lua literal syntax for userdata, so a guid can never be hand-written into a
script. The only confirmed, portable way to carry a guid across a round trip (e.g. out of a game session and
back into one, or between two systems that can't share a live reference) is through its string form:
`Ess.Name(uGuid)` out to a `"0x0012B69E"`-style string, and `Sys.StringToGuid("0x0012B69E")` back to an
identical, working handle — confirmed live (per `mercs2-lua-web-ide`'s object-inspector work) by reading the
same object's health through both the original guid and the round-tripped one and getting the same value.

Note `Ess.Name` is distinct from `Ess.Object.displayName(uGuid)` (covered on [Identity & World
Query](identity-query)), which returns the localized, human-readable name — `Ess.Name` returns the guid's
hash string.

## Ess.Str

`02_str.lua` — the everyday string helpers Lua 5.1's thin `string` library leaves you to hand-roll. Pure
Lua, no engine calls, no `Ess` dependencies. Execute-verified offline via `tools/checkpure.py`, not yet
confirmed via live testing (there's no engine surface to test against — it's plain string manipulation).

**Every separator/needle is LITERAL text, not a Lua pattern.** This is the real footgun the source itself
calls out: `split(s, ".")` splits on an actual dot, it does *not* treat `.` as "any character" the way
`string.gmatch`/`string.find` would. Every function below that takes a separator or needle matches it
plainly (`string.find(..., true)`) — reach for the stdlib directly if you actually want pattern matching.

| Function | Signature | Notes |
|---|---|---|
| `trim` | `Ess.Str.trim(s) -> s` | Strips leading/trailing whitespace. |
| `startsWith` | `Ess.Str.startsWith(s, prefix) -> bool` | |
| `endsWith` | `Ess.Str.endsWith(s, suffix) -> bool` | An empty `suffix` always matches. |
| `contains` | `Ess.Str.contains(s, needle) -> bool` | Literal substring test. |
| `count` | `Ess.Str.count(s, needle) -> n` | Non-overlapping literal occurrences (an empty `needle` counts as 0). |
| `split` | `Ess.Str.split(s, sep) -> { piece, ... }` | Splits on a literal `sep` (default `","`). `sep = ""` splits into one entry per character. A `sep` that never matches returns `{ s }`. |
| `join` | `Ess.Str.join(list, sep) -> s` | The inverse of `split`; `sep` defaults to `""`. |
| `padLeft` | `Ess.Str.padLeft(s, width, ch) -> s` | Pads on the left to `width` with `ch` (default `" "`, only its first character is used). No-op if `s` is already `width` or longer. |
| `padRight` | `Ess.Str.padRight(s, width, ch) -> s` | Same, padding on the right. |
| `capitalize` | `Ess.Str.capitalize(s) -> s` | Upper-cases the first letter only; the rest of the string is untouched. |
| `title` | `Ess.Str.title(s) -> s` | Capitalizes each word ("a b" -> "A B"). |
| `lines` | `Ess.Str.lines(s) -> { line, ... }` | Splits on `\n` (a trailing `\r` on each line is dropped); a single trailing newline doesn't manufacture a spurious empty final entry. |
| `truncate` | `Ess.Str.truncate(s, n [, ellipsis]) -> s` | Clips to `n` characters, appending `"..."` (or your own `ellipsis`) if it actually had to clip. |

## Ess.Color

`03_color.lua` — RGB helpers for the many `rgb = { r, g, b }` parameters across `Ess` (`Ess.Mark`,
`Ess.UI`, objective marker tints). Pure Lua, no engine calls, no `Ess` dependencies, all in **0-255 space**
to match what those consumers expect. Execute-verified offline via `tools/checkpure.py`, not yet confirmed
via live testing.

Every color function returns **three values** (`r, g, b`), which is exactly what an `rgb = { ... }` table
needs when it's the sole element of the constructor — `Ess.Mark.object(g, { rgb = { Ess.Color.hex("#ff8800") } })`
captures all three at once. `Ess.Color.NAMES` is a table of ready-made `{ r, g, b }` presets for the same
slots.

| Function | Signature | Notes |
|---|---|---|
| `hex` | `Ess.Color.hex(s) -> r, g, b \| nil` | Parses `"#RRGGBB"`, `"RRGGBB"`, or the short form `"#RGB"`/`"RGB"` (each digit doubled). Case-insensitive. Returns `nil` on anything else (wrong length, non-hex digits). |
| `hsv` | `Ess.Color.hsv(h, s, v) -> r, g, b` | `h` in `[0, 360)` (wraps), `s`/`v` in `[0, 1]` (clamped). Standard HSV-to-RGB — rainbows, evenly-spaced team tints. |
| `lerp` | `Ess.Color.lerp(c1, c2, t) -> r, g, b` | Blends two colors, each a `{ r, g, b }` table (or one with `.r`/`.g`/`.b` keys) — e.g. a health-bar gradient. `t` clamped to `[0, 1]`. |
| `of` | `Ess.Color.of(name) -> r, g, b \| nil` | Looks up a preset in `Ess.Color.NAMES` by name (case-insensitive). `nil` if the name isn't a preset. |

`Ess.Color.NAMES` currently has: `red`, `green`, `blue`, `yellow`, `orange`, `cyan`, `magenta`, `purple`,
`pink`, `lime`, `teal`, `white`, `black`, `gray`/`grey`, `brown` — each a `{ r, g, b }` table usable
directly as an `rgb` param.

## Ess.Vec

`04_vec.lua` — 3D vector helpers on flat `x, y, z` values: the spatial math that spawn/aim/knockback/camera
code kept open-coding (normalize a direction, step a point toward a target, lerp two positions). Pure Lua,
no engine calls, no `Ess` dependencies. Execute-verified offline via `tools/checkpure.py`, not yet confirmed
via live testing — with two exceptions, see below.

Everything takes and **returns flat components** (three separate values), not a table — matching how the
rest of `Ess` passes positions (`Ess.Object.pos` returns `x, y, z`; `Ess.Object.setPos` takes `x, y, z`) and
`Ess.Color`'s own three-value convention. Results drop straight into those calls:

```lua
Ess.Object.setPos(u, Ess.Vec.toward(px, py, pz, tx, ty, tz, 5))    -- move it 5 units toward the target
local dx, dy, dz = Ess.Vec.dir(fx, fy, fz, tx, ty, tz)             -- ...or shove it that way:
Ess.Object.impulse(u, Ess.Vec.scale(dx, dy, dz, 8000))
```

| Function | Signature | Notes |
|---|---|---|
| `length` | `Ess.Vec.length(x, y, z) -> n` | |
| `normalize` | `Ess.Vec.normalize(x, y, z) -> nx, ny, nz` | Unit vector; a zero-length input returns `0, 0, 0` rather than `NaN`. |
| `scale` | `Ess.Vec.scale(x, y, z, s) -> x, y, z` | |
| `add` | `Ess.Vec.add(x1, y1, z1, x2, y2, z2) -> x, y, z` | |
| `sub` | `Ess.Vec.sub(x1, y1, z1, x2, y2, z2) -> x, y, z` | `a - b`, i.e. the vector from `b` to `a`. |
| `dot` | `Ess.Vec.dot(x1, y1, z1, x2, y2, z2) -> n` | |
| `cross` | `Ess.Vec.cross(ax, ay, az, bx, by, bz) -> cx, cy, cz` | The cross product — dot's missing sibling, added in 0.3.1: perpendicular to both inputs, for camera-right from forward+up, a surface normal from two edges, or "is B left or right of A" from the sign of the vertical component. See below for its live-verification status and its distinction from the engine's own native `Math.CrossProduct`. |
| `dir` | `Ess.Vec.dir(fromX, fromY, fromZ, toX, toY, toZ) -> nx, ny, nz` | Unit direction from A to B (`normalize(sub(B, A))`). |
| `toward` | `Ess.Vec.toward(fromX, fromY, fromZ, toX, toY, toZ, dist) -> x, y, z` | The point `dist` units from A toward B. |
| `lerp` | `Ess.Vec.lerp(x1, y1, z1, x2, y2, z2, t) -> x, y, z` | Interpolates between two positions. |

(`Ess.Math`, next section below, holds the 2D/ground-plane and angle helpers — `angleTo`, `pointAhead`,
`dist2D`, `within2D`. `Ess.Vec` is the full-3D companion to those.)

**Multi-return caveat (real, and a genuine footgun):** Lua truncates a multi-value call to exactly ONE
value unless that call is the LAST item in an argument list. A `Ess.Vec` call expands to all three
components fine when it's the final argument of an engine call (`setPos`/`impulse` above), but nesting two
`Ess.Vec` calls does **not** work the way it looks like it should — `scale(dir(...), s)` silently passes
only `dir`'s `x` component as `scale`'s `x`, dropping `y`/`z` entirely. Capture the inner call's results into
locals first:

```lua
-- WRONG: dir(...) truncates to one value here, s lands in Vec.scale's y-slot
Ess.Object.impulse(u, Ess.Vec.scale(Ess.Vec.dir(fx, fy, fz, tx, ty, tz), 8000))

-- RIGHT: capture the inner call to locals, then pass all three through
local dx, dy, dz = Ess.Vec.dir(fx, fy, fz, tx, ty, tz)
Ess.Object.impulse(u, Ess.Vec.scale(dx, dy, dz, 8000))
```

**This exact mechanism is also what powers `Ess.Easy.Camera.orbit`/`.watch(chase=true)`'s follow-damping**
(release 0.2.1): both ease the camera toward its target position each tick via `Ess.Vec.lerp` rather than
snapping straight to it, low-passing the per-tick position jitter a fast-moving subject would otherwise
cause. `smooth` defaults to `true`, `smoothFactor` defaults to `0.2` (0..1; higher = snappier/less lag,
lower = glassier/more lag). Unlike the rest of this section, that *consumer* of `Ess.Vec.lerp` is
**confirmed working live** — the source itself records a live test against an orbit around a heli and a
hard-launched car. See [Ess.Camera](camera-bones#esscamera) for the full write-up; `Ess.Vec.lerp` itself
stays in the offline-verified bucket above.

**`Ess.Vec.cross`, added in 0.3.1 (the 2026-07-22 "bindings-pass harvest"), is this section's other
exception — and a more direct one than `lerp` above.** Per `CHANGELOG.md`'s `[0.3.1]` entry, `cross` itself
— not just a consumer built on top of it — was one of the targeted live probes run during that release's
in-game pass, and it returned `(0, 0, 1)`. It's pure Lua, no engine call, exactly like the rest of this
table: a **separate, independently-implemented** function from the native engine's own
[`Math.CrossProduct`](../namespaces/math), which computes the same cross-product math but through an actual
engine binding, not this framework. Same underlying math, two unrelated call paths — don't confuse the two.

## Ess.Math

Geometry/number helpers this project kept re-deriving file after file — spawn-ahead forward trig, camera
orbit/dolly lerps, grid placement, distance checks. One confirmed-correct home for each, loaded right after
`00_core` (pure functions, no other `Ess` dependencies).

**Engine convention (load-bearing, live-calibrated 2026-07-19):** Y is up; the horizontal plane is X/Z. A
yaw's FORWARD vector is `(+sin(yaw), +cos(yaw))` in `(x, z)`. `angleTo`/`pointAhead` below are exact inverses
of each other — if this convention is ever revisited, both must change together, as a pair.

**This was mirrored (wrong X sign) until 2026-07-19** — recorded here because it hid for a long time and
could otherwise get "re-fixed" back to the broken version. The old formula was `(-sin, +cos)`, with
`angleTo` computing `atan2(-dx, dz)`. Proven wrong by an A/B marker test: two rings placed from the same
body yaw, one per convention — facing **east** the correct `(+sin)` ring was dead ahead and the old `(-sin)`
ring was 180° behind; facing **north** the two rings coincided (`sin(0) = 0`), which is exactly why the bug
hid — the error is invisible at yaw 0/180 and maximal at yaw ±90. **Always calibrate facing east/west, never
north**, or a mirror bug like this one can pass a spot-check and hide again. This affected anything that
placed or aimed something relative to a yaw: `Ess.Object.spawnAhead`, `Ess.Easy.Vehicle.summon`, the UI
kit's `ctx:spawn`, and `Ess.Object.faceToward`/`faceObject` — all live-verified working correctly since the
fix. If you wrote code that compensated for the old (backwards) behavior, remove the compensation.

A *separate* issue, easy to conflate with the above but not the same thing: `Object.GetYaw`/a character's
own yaw is its **chest/body** orientation, not where the player is *looking* — stand still and swing the
mouse and the view rotates while the body doesn't (measured up to 111° apart; running forward re-aligns
them). `angleTo`/`pointAhead` are correct either way; which yaw you feed them is the separate question. See
[`Ess.Player.viewYaw`](identity-query#essplayer) for the view-relative yaw, and the `useView` opt-in on
`spawnAhead`/`Ess.Easy.Vehicle.summon`/`ctx:spawn` below.

| Function | Signature | Notes |
|---|---|---|
| `clamp` | `Ess.Math.clamp(v, lo, hi) -> n` | |
| `lerp` | `Ess.Math.lerp(a, b, t) -> n` | |
| `sign` | `Ess.Math.sign(v) -> -1\|0\|1` | |
| `round` | `Ess.Math.round(v [, decimals]) -> n` | `decimals` defaults to 0 (nearest integer). |
| `approach` | `Ess.Math.approach(cur, target, maxStep) -> n` | Moves `cur` toward `target` by at most `maxStep` — a frame-rate-independent ease when `maxStep = speed * dt`. |
| `dist2D` | `Ess.Math.dist2D(x1, z1, x2, z2) -> n` | Horizontal (X/Z-plane) distance — "how far away is it on the ground," ignoring height. |
| `dist3D` | `Ess.Math.dist3D(x1, y1, z1, x2, y2, z2) -> n` | Includes the Y term. |
| `angleTo` | `Ess.Math.angleTo(fromX, fromZ, toX, toZ) -> yawDegrees` | The yaw that faces from `(fromX,fromZ)` toward `(toX,toZ)`, in the engine's own convention. Returns 0 if the two points coincide. |
| `pointAhead` | `Ess.Math.pointAhead(x, z, yawDeg, dist) -> x2, z2` | The point `dist` units in front of `(x, z)` when facing `yawDeg` — exactly `Ess.Object.spawnAhead`'s projection, exposed for reuse (place something ahead of an NPC, aim a dolly, offset a marker). Y is unchanged; the caller keeps it. |
| `rotateOffset` | `Ess.Math.rotateOffset(x, z, yawDeg, localX, localZ) -> x2, z2` | Places a *local* offset (`localX` = right+, `localZ` = forward+) into world space around `(x, z)` for something facing `yawDeg` — "5 right and 10 ahead of me." `pointAhead` is this function's `localX = 0` special case. Exists so nobody hand-rolls a rotation matrix again — that's exactly how the mirror-sign bug above got re-derived into MissionForge's squad-grid placement before this existed. |
| `normDeg` | `Ess.Math.normDeg(deg) -> n in [-180, 180)` | Normalizes an angle so a difference of two yaws reads as the shortest turn (350 and 10 differ by 20, not 340). Handy for "am I roughly facing this" checks and smooth turn easing. |
| `clamp01` | `Ess.Math.clamp01(v) -> n` | Clamps to the unit range `[0, 1]` — the common case for a lerp/ease parameter. |
| `remap` | `Ess.Math.remap(v, inLo, inHi, outLo, outHi) -> n` | Linear rescale of `v` from `[inLo, inHi]` onto `[outLo, outHi]` — "a 0..maxHealth into a 0..1 bar," "a distance into an alpha." A degenerate input range (`inLo == inHi`) returns `outLo` instead of dividing by zero. Does **not** clamp the output — a `v` outside `[inLo, inHi]` extrapolates past `[outLo, outHi]`. |
| `smoothstep` | `Ess.Math.smoothstep(t) -> n` | Eases a `0..1 t` to `0..1` with zero slope at both ends (`3t² - 2t³`). Clamps `t` first. Feed it to `lerp` for an ease-in-out: `Ess.Math.lerp(a, b, Ess.Math.smoothstep(t))`. |
| `lerpAngle` | `Ess.Math.lerpAngle(a, b, t) -> deg` | Interpolates angle `a -> b` (degrees) the *shortest* way, so 350 -> 10 eases +20 through zero rather than -340 the long way round. `t` in `[0, 1]`; result normalized to `[-180, 180)`. The correct lerp for a turning yaw. |
| `wrap` | `Ess.Math.wrap(v, lo, hi) -> n` | Wraps `v` into the half-open range `[lo, hi)` — keep an index, an angle, or a cursor in-band. `hi <= lo` returns `lo`. |
| `dist2DSq` | `Ess.Math.dist2DSq(x1, z1, x2, z2) -> n` | `dist2D` without the `sqrt` — use when you only need to *compare* distances ("which is closer"). |
| `dist3DSq` | `Ess.Math.dist3DSq(x1, y1, z1, x2, y2, z2) -> n` | Same, including the Y term. |
| `within2D` | `Ess.Math.within2D(x1, z1, x2, z2, r) -> bool` | Is the second point within radius `r` of the first, on the ground plane? The `dx*dx + dz*dz <= r*r` range test, named — no `sqrt`, no chance to fumble the squaring. This is the check every proximity trigger / "reached the zone" poll open-codes; here once. |
| `within3D` | `Ess.Math.within3D(x1, y1, z1, x2, y2, z2, r) -> bool` | Same, including the height term. |

## Ess.Sys

New in **v0.5.0** (`05_sys.lua`). The "what game am I running in, and how is it configured?" namespace. The
engine's [`Sys`](../namespaces/sys) namespace is 64 functions of thoroughly mixed concerns — timing,
autosave, asset streaming, save versioning, and a large pile of environment/settings getters. `Ess` already
covered the timing half ([`Ess.Time`](timing-input#esstime), over `Sys.RealTimeStamp`/`MainTimeStamp`/
`TimeStampMark`) and the autosave half ([`Ess.Save`](tracking#esssave)); `Ess.Sys` is the **environment**
half: level identity, build identity, and the player's own option settings. All of it previously meant
dropping to raw natives.

**Everything here is read-only and side-effect free.** The `Sys` *mutators* (`RequestGameState`,
`SetLevelName`, `StartSingleplayer`, `AddStringDb`, …) are deliberately excluded — several of them drive the
game's own state machine — and are recorded in the framework's own `docs/deferred-setters.md` instead.

| Function | Signature | Notes |
|---|---|---|
| `level` | `Ess.Sys.level() -> sLevel, sMasterScript` | **Two values.** Both read `"vz"` in freeplay. At the bare shell menu they can come back as **empty strings rather than `nil`**, so test with `~= ""` and not just for nil-ness. |
| `version` | `Ess.Sys.version() -> sCode, sData` | **Two values, not one** — a build code *and* a data version. The corpus reads it as `local sCode, sData = Sys.GetVersion()`; taking only the first is a common misread. Both come back `"100000"` on this build. |
| `platform` | `Ess.Sys.platform() -> n \| nil` | The engine's own platform **enum**, not a string (`3` on this PC build). Deliberately left raw rather than mapped to a name: only the one value has ever been observed, and inventing labels for the rest would be fiction. |
| `language` | `Ess.Sys.language() -> s \| nil` | `"English"` here. Worth branching on in any script that puts text on screen. |
| `uptime` | `Ess.Sys.uptime() -> n` | Seconds of **main-loop** time since the process started (`Sys.MainTime` — 1354.7 in a session that had been up a while). `05_sys.lua`'s rationale for wrapping it is that it's the game's own clock and so doesn't advance while paused or loading, which would make it the right base for "how long has the player actually been *playing*" — but note that [Sys](../namespaces/sys) records `Sys.MainTime`'s pause/time-scale behaviour as **presumed, not confirmed**, so treat that as the reason it was chosen rather than a measured fact. Returns `0` rather than `nil` if unreadable. |
| `isLoading` | `Ess.Sys.isLoading() -> bool` | Is the engine loading or streaming right now? Wait on it before spawning into a world mid-stream. The shipped scripts pair it with a character check — `not Player.GetLocalCharacter() or Sys.IsLoadingOrStreaming()` — as their "world isn't ready yet" test; that idiom is worth copying rather than using this flag alone. |
| `settings` | `Ess.Sys.settings() -> t` | The player's own option settings, in one table (below). |
| `build` | `Ess.Sys.build() -> t` | What *kind* of build this is (below). |

`settings()` returns six booleans in one table. They're grouped rather than exposed as six predicates
because they're read together far more often than singly:

| Key | Meaning |
|---|---|
| `tutorials` | Tutorial hints are enabled. |
| `subtitles` | Subtitles are on — **respect this one.** A mod that shows custom dialogue and ignores it is a bug. |
| `rumble` | Controller rumble is enabled. |
| `invertY` | The player inverts the Y axis. |
| `confirmOnCircle` | Confirm is bound to circle rather than cross — it changes how you should word a prompt. |
| `noHud` | The HUD is hidden, so don't draw HUD-anchored UI. |

`build()` returns five booleans: `demo` (demo mode), `german` (the censored German SKU, which has different
gore/content rules), `finalConfig` (a release build rather than a dev one), `hasProfile` (an active player
profile is loaded), and `autoLoad` (the auto-load-last-save path is armed). Several of these are called
*defensively* in the shipped scripts — `Sys.IsDemoMode and Sys.IsDemoMode()` — i.e. Pandemic did not trust
them to exist in every build. `Ess.Safe.quiet` makes that moot (a missing binding yields `false` instead of
throwing), but it's a standing hint that these vary by build: branch on them, don't assert them.

The specific values quoted above (`3`, `"English"`, `"100000"`, the 1354.7 uptime) are recorded in
`05_sys.lua` as observations from the 0.5.0 live-probe pass against a running game, not derived from the
decompiled corpus. They describe **this** PC build; treat them as example readings rather than constants.

## Ess.Atmosphere

New in **v0.5.0** (`06_atmosphere.lua`). Sky, light and time-of-day — and an honest account of the region
system that keeps overwriting them. This is the *Core* tier underneath the `Ess.Easy.World` one-liners
(`tint`/`brightness`/`hellscape`, covered on [Ess.Easy](easy#world--esseasyworld)), which sit on the same
native [`Graphics.Atmosphere`](../namespaces/graphics#graphicsatmosphere) surface: the transaction model,
the value vocabulary, and the reasons an atmosphere change doesn't stick. All of it was **established by
live measurement on 2026-07-26**; the source is explicit that none of it is guessable from the native names.

**A note on where this lives.** `Ess.Atmosphere` is the odd entry on this page: it isn't a primitive the
rest of `Ess` is built out of, it's an engine-facing world-control namespace. It's documented here because
it loads in the same low-numbered core block (`06_`, immediately after `Ess.Sys`) and because this wiki has
no world/environment page yet. If one is ever added, this section belongs there.

### The three things that make this namespace confusing

**1. It is transactional.** `Graphics.Atmosphere.GetValue` returns `nil` outside a `Begin()`/`End()` pair —
not an error, just `nil`. The one call site in the decompiled corpus reads like an ordinary standalone
getter, so copying it verbatim silently returns nothing. Every function below opens and closes the
transaction for you, which is most of the reason the file exists.

**2. Value keys are not validated.** A nonsense key raises no error and returns no failure signal — inside a
transaction it simply reads `0`. Since `0` is a legitimate value for several *real* keys, you cannot use
that to test whether a key exists: a typo is a silent no-op forever. Worse, **the engine's own spelling
contains a mistake you have to reproduce** — it is `fBloomContastMultiplier` and `fBloomContastLimit`
(*Contast*, not *Contrast*). Spell it correctly and it silently does nothing. Use `Ess.Atmosphere.KEYS`
rather than typing any of these by hand; the aliases map to the misspelled engine strings deliberately.

**3. The region system owns the atmosphere, not you.** The map is divided into named atmosphere regions
(`rgn_atmo_caracas`, `rgn_atmo_Maracaibo`, `rgn_atmo_interior`, …). **There are forty-odd of them, not the
six the script corpus happens to name** — the full set lives in the *level* data (`layers_static`), which is
why an earlier pass concluded the other 34 "cannot be addressed." They can: 20 were checked live against
`Pg.GetGuidByName` and every one resolved, with a deliberately bogus name in the same batch as the control.
Name lookup is **case-insensitive**.

On the exact count, the wiki can only report what's checkable. `06_atmosphere.lua`'s header says "41 strings
for 40 regions," the extra string being a case-duplicate (`rgn_atmo_caracas` / `rgn_atmo_Caracas`) — but
only the lowercase spelling is actually in the exported `REGIONS` table, and its 41 entries are all distinct
even compared case-insensitively. **41 names is the verified figure**; the "40 regions" reduction is the
source's own, and this page does not stand behind it.

Crossing into a region starts an **interpolated blend**, roughly a second long, from wherever the atmosphere
currently is toward that region's own settings. So a manual change isn't so much "overwritten" as used as
the *starting point* of a blend the engine is driving somewhere else. Measured across one crossing:
`fLightIntensity` 1.15 → 1.02 → 1.0 and `fAtmosphereForce` 1.0 → 2.30 → 2.5, settling over about a second,
with a night sky fading back to daylight over the same interval.

### The surface

| Function | Signature | Notes |
|---|---|---|
| `get` | `Ess.Atmosphere.get(sKey) -> n \| nil` | Reads one float, opening and closing the transaction around it (without which the native returns `nil`). Accepts either a raw engine key (`"fLightIntensity"`) or a `KEYS` alias (`"lightIntensity"`). `nil` for a non-string key. |
| `set` | `Ess.Atmosphere.set(tKeyToValue, nFadeSeconds) -> bool` | Sets one or many values in **one** transaction — which matters, because the fade duration is a property of `End()`, so separate transactions mean separate fades and a visibly staggered result. `nFadeSeconds` defaults to **0.5**. Keys may be aliases or raw engine names. **The return says the transaction completed, not that the keys were real** — the engine never reports an unknown key. |
| `setColor` | `Ess.Atmosphere.setColor(sKey, r, g, b, a, nFadeSeconds) -> bool` | Color channels are **0–255**; each of `r`/`g`/`b`/`a` defaults to `255` and `nFadeSeconds` to `0.5`, matching every corpus call site. `sKey` may be a `COLOR_KEYS` alias. |
| `setTime` | `Ess.Atmosphere.setTime(n) -> bool` | Time of day as **0..1**; `0.95` is night. Not a `SetValue` key — it has its own native and takes no part in the `Begin`/`End` transaction. Pair it with `setTimeSpeed(0)` or the cycle carries on from wherever you put it. |
| `setTimeSpeed` | `Ess.Atmosphere.setTimeSpeed(n) -> bool` | The rate of the day/night cycle; `0` freezes it. There is **no** `GetTimeSpeed`, so the original rate cannot be read back or restored — record it yourself if you intend to put it back. |
| `blending` | `Ess.Atmosphere.blending() -> bool` | Is a region blend running *right now*? The same guard the shipped scripts use (`bSafeToBegin = not Graphics.Atmosphere.IsInterpolating()`) before beginning their own changes. **Read the same-frame trap below before using it.** |
| `setting` | `Ess.Atmosphere.setting() -> uSetting \| nil` | A handle for the currently-active atmosphere setting; compare handles with `==` to detect a transition. The native returns **two** userdata values and only the first changes on a region crossing, so this returns that one. Do **not** `tostring()` the raw native result — `tostring()` with two arguments returns a *function* on this build, which is an easy way to convince yourself a stored handle has changed into something else. |
| `region` | `Ess.Atmosphere.region(sName) -> uGuid \| nil` | Resolves an `rgn_atmo_*` name to its guid (it's [`Ess.Guid`](#essguid--essname) with a type check). Provided for future `ChangeLineRegionSetting` work — as of 0.5.2 there is nothing else in `Ess` to do with the guid. |

Three exported vocabularies exist so that nothing has to be typed by hand:

- **`Ess.Atmosphere.KEYS`** — 13 float keys under readable aliases: `lightIntensity`, `atmosphereForce`,
  `atmosphereLimit`, `timeRestore`, `bloomAmount`, `bloomMultiplier`, `bloomThreshold`, `bloomBlurRadius`,
  `bloomTargetLuminance`, `bloomContrastMultiplier`, `bloomContrastLimit`,
  `bloomAdaptiveLuminanceScale`, `bloomAdaptiveLuminancePct`. Note the two `bloomContrast*` aliases are
  spelled *correctly* and map to the engine's misspelled `fBloomContast*` strings — that's the whole point
  of the table.
- **`Ess.Atmosphere.COLOR_KEYS`** — `ambient` (`uiAmbientColor`), `rim` (`uiRimColor`), and `ambientCube`,
  which is a **table of six** key names rather than a single string. `setColor` guards against being handed
  that table alias and returns `false` rather than doing something surprising with it.
- **`Ess.Atmosphere.REGIONS`** — the 41 extracted region-name strings described above.

```lua
Ess.Atmosphere.set({ lightIntensity = 0.2, bloomAmount = 2 }, 1.5)   -- both keys, one 1.5s fade
local lit = Ess.Atmosphere.get("lightIntensity")                     -- alias or "fLightIntensity"
```

**The `blending()` same-frame trap (measured, and a real footgun).** `get`/`set`/`setColor` all open a
transaction, and *a transaction leaves the interpolating flag set for the remainder of that frame* — it does
not clear until the next one. Measured: a bare call reads `false`, the same call immediately after a `get()`
reads `true`, and a bare call one chunk later reads `false` again. So this always takes the wrong branch:

```lua
local v = Ess.Atmosphere.get("lightIntensity")
if not Ess.Atmosphere.blending() then ... end     -- ALWAYS false, every time
```

Sample `blending()` **first**, before touching anything else, or sample it on a later tick — an
[`Ess.Loop`](timing-input#essloop) heartbeat is the natural place, since that's where you'd be waiting for a
blend to finish anyway.

**Correction to an earlier finding on this wiki.** [Ess.Easy](easy) states that the global
`SetTime`/`SetSky`/`SetTimeSpeed` setters were "confirmed inert in live play." The 2026-07-26 measurement
says that is **wrong for `SetTime` and `SetTimeSpeed`**, and the error mattered — it steered work away from
the only interface that actually moves the sky. `Graphics.Atmosphere.SetTime(0.95)` visibly turns the sky to
night (confirmed on screen by a human, and confirmed again by watching it fade back over ~1s on a zone
crossing), and `SetTimeSpeed(0)` freezes the cycle. What *is* true is that neither is a `SetValue` key and
neither takes part in the `Begin`/`End` transaction, so they need their own keeper. `SetSky` remains
untested and **is** one of the 61 no-op stubs in the verified EXE audit, so that part of the old claim may
well hold.

**Time and region atmosphere are separate systems, so pinning the time is not map-wide.** Measured
2026-07-26 with a keeper confirmed ticking 1,299 times at 10 Hz and the lock holding at `0.95` throughout —
and the sky still full daylight on one side of a region boundary. A region's authored atmosphere preset
paints the sky *directly*; it is not derived from the time-of-day clock, so `SetTime` moves a clock that any
region with its own preset simply overrides, and re-asserting faster cannot win because the clock is not the
thing being contested. Where a time lock *does* hold: the gaps **between** atmosphere regions (a large part
of the map, where the engine falls back to a global default the clock does drive), and regions whose preset
follows the clock rather than overriding it. That's a property of the engine's data, not a bug.

**`Graphics.Atmosphere.ChangeLineRegionSetting` is deliberately not wrapped.** Reconfiguring what a region
*applies* is the obviously nicer mechanism — crossing the boundary would then do the right thing unaided —
and the call does work on the region you're standing in. It's held back for reasons that survived testing:
the second argument is an **authored preset name**, not a value you control, and there is no way to
enumerate or create one; and six calls batched into one chunk caused a **measured 13-second engine stall**,
so a blanket apply across every region would have to be paced out over seconds and would still leave the region-less
gaps untouched. Preset names attested in the decompiled corpus include `"default"`, `"pmc"`,
`"day"`, `"warzone"`, `"warzonemar"` and `"WarzoneSolano"` (see
[Graphics](../namespaces/graphics#graphicsatmosphere)); `"night"` is attested on exactly one region and
reads as late evening rather than true night. `Ess.Atmosphere.region()` exists so that work can start from
resolved guids rather than guesses.

## Ess.State

```lua
Ess.State(name, defaults) -> persistent table
```

The `_G.X = _G.X or {defaults}` idiom, done field-by-field. Every stateful `OnKey`/`OnLoad` script needs
this — a script re-executes fully on each keypress/reload; only `_G` survives between runs — but it merges
key-by-key instead of a blind top-level `or`.

**Confirmed real bug this fixes:** `_G.S = _G.S or {a=1,b=2}` silently drops a newly-added field. Say you
add `c=3` to `defaults` in a later edit — if `_G.S` already exists from an earlier run in the same session,
the `or` short-circuits on the whole table the instant it sees `_G.S` is non-nil, so the new key is never
even considered. `Ess.State` merges field by field instead: adding a field to `defaults` later always takes
effect on the next run, even if the table already exists. Internally it's keyed as `_G["_Ess_state_" ..
name]`, so pick a `name` your script owns.

## Ess.SaveVar

`Loader.SaveVar`/`LoadVar` is a flat namespace shared by every mod (numbers/strings/booleans only, persists
across game restarts in `lua_loader_data.ini`) — every mod ends up hand-rolling its own prefixed get/set +
unlock-flag idiom over it (directly confirmed duplicated in `WaveDefense.lua`). `Ess.SaveVar` is one
namespaced wrapper instead.

```lua
local sv = Ess.SaveVar.ns("MyMod")
```

| Method | Signature | Notes |
|---|---|---|
| `ns` | `Ess.SaveVar.ns(prefix) -> ns object` | Every key gets stored as `<prefix>_<key>`, so two mods' saved values can never collide. |
| `:get` | `sv:get(key, default) -> v` | Returns `default` if the key was never set. |
| `:set` | `sv:set(key, value)` | |
| `:flag` | `sv:flag(key) -> bool` | A `:get` specialized for booleans (default `false`). |
| `:setFlag` | `sv:setFlag(key, bOn)` | |

Real usage, from the shipped `persistent_vars` recipe (remembering a value across save/reload — XP, unlock
flags, high scores, a run counter):

```lua
local sv = Ess.SaveVar.ns("RecipeDemo")        -- namespace your vars

local before = sv:get("runs", 0)               -- read with a default (0 the very first time)
sv:set("runs", before + 1)                     -- write it back (persists)

sv:setFlag("said_hello", true)                 -- flags are the boolean flavor
local flagged = sv:flag("said_hello")
```

Unlike `Ess.State` (per-session, lives only in `_G`), `Ess.SaveVar` values survive a save/reload — use it
for anything the player should keep between play sessions.

## Ess.RNG

An engine-safe random number generator plus weighted pick — the namespace exists to paper over a real,
confirmed engine gotcha.

**The gotcha:** this engine's Lua numbers are 32-bit float (single precision), not the usual 64-bit double —
integers are only exact up to 2^24 (16,777,216). The obvious PRNG choice, a Park-Miller/MINSTD LCG (`state =
state*16807 mod 2^31`), silently degenerates on this engine: `state*16807` blows past 2^24 almost
immediately and starts rounding, and the generator can get stuck outputting the same value on every call.
**Confirmed:** this happened for real in `WaveDefense.lua` — every weighted crate/unit roll came out
identical for an entire play session before it was diagnosed. The engine's built-in `math.random` is
confirmed dead/unusable here too.

**The fix:** a small ZX-Spectrum-style LCG whose entire arithmetic stays under 2^23 no matter what — `state
= (state * 75) % 65537`. Full period 65536, verified well-distributed. Any hot integer math you do yourself
should stay under roughly 2^23 too, for the same reason — it's the engine's whole number type, not just this
generator.

Each `Ess.RNG.new()` is its own independent stream (seeded from the wall clock by default), so two mods
drawing from `Ess.RNG` in the same tick don't perturb each other's sequence the way one shared global
generator would.

| Method | Signature | Notes |
|---|---|---|
| `Ess.RNG.new` | `Ess.RNG.new(seed) -> generator` | Omit `seed` for a time-seeded stream (via `Sys.RealTime`); pass one for a reproducible sequence. |
| `:next` | `gen:next() -> n in [0, 1)` | |
| `:int` | `gen:int(n) -> integer in [1, n]` | |
| `:chance` | `gen:chance(p) -> bool` | `true` with probability `p` (0..1); omit `p` for a coin flip. |
| `:pick` | `gen:pick(list, weightKey) -> element of list` | Weighted by each entry's `[weightKey]` field (default `"w"`), falling back to weight 1 for entries missing it. Collapses an accumulator-loop weighted-pick that `WaveDefense.lua` had written three separate times (same logic, copy-pasted) into one implementation. |
| `:shuffle` | `gen:shuffle(list) -> list` | In-place Fisher–Yates shuffle of the array part (mutates and returns the same list, for chaining) — the engine-safe way to randomize order, since a random-comparator `table.sort` is biased and can even error on some Lua builds. |
| `:pickN` | `gen:pickN(list, n) -> {...}` | `n` distinct random elements (sample without replacement), order randomized. `n >= #list` returns a shuffled copy of the whole list; `n <= 0` returns `{}`. Never mutates `list`. |

Real usage, from the shipped `random_selection` recipe:

```lua
local rng = Ess.RNG.new(1234)                                  -- reproducible; Ess.RNG.new() = time-seeded

local d6   = rng:int(6)                                        -- an integer in [1, 6]
local coin = rng:chance(0.5)                                   -- true ~half the time
local pick = rng:pick({ "AH1Z", "Mi35", "WZ10" })              -- one element of a list (uniform here;
                                                                -- pass {w=} weights on table entries for weighted)
```

## Ess.stop

New in **v0.4.0** (`98_stop.lua` — the last file in the build, loading after every namespace it might need to
dispatch to, [`Ess.Track`](tracking#esstrack) included). One teardown verb for whatever handle shape you're
already holding, regardless of which namespace produced it.

**The problem it solves:** Ess grew **27 distinct teardown verbs** across **five** structurally different
disposal idioms, because each namespace picked whichever word read best locally — there was no learnable
single answer to "how do I turn this off":

| Shape | Construction | Its own teardown |
|---|---|---|
| A closure to call | `Ess.On.death(g, fn)` | the `stop()` it returns |
| An opaque handle table | `Ess.Mark.object(g, {...})` | `Ess.Mark.clear(handle)` |
| A caller-supplied id string | `Ess.Loop.start("id", ...)` | `Ess.Loop.stop("id")` |
| An object with a method | `Ess.Objective.new{...}` | `:cancel()` |
| A tracker registry | `Ess.Track.new()` | `:closeAll()` |

**None of this is deprecated.** All 27 verbs still work, and each is still the most precise way to say what
you mean inside its own namespace. `Ess.stop` is an *additional* convenience, not a replacement for any of
them — reach for it when you're just holding a handle and want it gone, or for a teaching example that
shouldn't need a detour into which namespace spells teardown which way.

| Function | Signature | Notes |
|---|---|---|
| `Ess.stop` | `Ess.stop(x) -> bool` | Tears down whatever `x` is — closure, handle table, id string, or object with a method — and returns whether it actually did. `nil` or anything unrecognized is a safe no-op returning `false`; teardown never throws. |
| `Ess.stopAll` | `Ess.stopAll(t) -> nCount` | Runs `Ess.stop` over a **dense** array of handles, in **reverse order** (mirroring `Ess.Track:closeAll`, since later setup usually depends on earlier setup), returning how many actually tore down. |
| `Ess.Track:any` | `tracker:any(x) -> x` | `Ess.Track`'s own integration point for the same dispatch: hand a tracker any of the five shapes above and its `:closeAll()` tears it down along with everything else. Returns `x` unchanged, so it chains: `local h = tracker:any(Ess.Easy.Mark.enemy(g))`. See [Tracking & Cleanup](tracking#esstrack) for `Ess.Track` itself — this is just its dispatch hook, not a replacement for its typed registrars (`:event`/`:guid`/`:marker`/...), which stay the better choice whenever you already know what you have. |

`Ess.stop` dispatches by duck-typing `x`, in this order: a `function` goes straight through
`Ess.Safe.named`; a `string` id is resolved by *asking* `Ess.Loop`/`Ess.Sandbox` which one (if either) is
currently running/active with that id, rather than guessing from the string itself; for a table, real
methods (`:closeAll`/`:cancel`/`:stop`) are checked before any field shape, so an object that happens to also
carry a matching field can't be misrouted; only then does it fall back to the same field-shape checks
`Ess.Mark.clear`/`Ess.Relations.restore` already use internally to recognize their own handles — so these
aren't new guesses, they're the discriminators those functions already relied on.

`Ess.stopAll` walks `#tHandles`, so — like anything else in this framework that trusts `#` — the array must
be dense. Individual `nil` entries inside it are skipped safely, but the *length* can silently lie on a
holed table; if you built the list by nil-ing entries out as you went, run it through
[`Ess.Table.compact`](#esstable) first.

## See also

- [Essentials (Ess)](index) — the framework index this page belongs to.
- [Identity & World Query](identity-query) — `Player`, `Object`, `Vehicle`, `Probe`, `Human`, `Impulse`; the
  next tier up, built on these primitives (`Ess.Object.faceToward` uses `Ess.Math.angleTo`, `Ess.Impulse`
  uses `Ess.Player`/`Ess.Object`, and so on).
- [Ess.Easy](easy) — the beginner-tier one-liner presets built on top of all of this.
- [Tracking & Cleanup](tracking) — `Ess.Track`'s full registrar surface and `:closeAll`, which
  `Ess.Track:any` (above) plugs into; also `Ess.Mark`/`Ess.Relations`, two of the handle shapes `Ess.stop`
  recognizes by field shape. `Ess.Save` (the savegame gate) lives there too — the other half of the engine
  `Sys` namespace that [`Ess.Sys`](#esssys) deliberately doesn't cover.
- [Sys](../namespaces/sys) and [Graphics](../namespaces/graphics) — the raw engine namespaces `Ess.Sys` and
  `Ess.Atmosphere` wrap, including the natives neither wrapper exposes.
