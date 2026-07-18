---
title: Core Primitives
parent: Essentials (Ess)
nav_order: 1
---

# Core Primitives

## Overview

This page covers the bottom of the [Ess](index) stack: the pieces every other namespace is built out of,
rather than the ones you'd reach for to move an object or spawn a vehicle. Seven source files:
`00_core.lua` (`Ess.Log`, `Ess.Safe`, `Ess.Table`, `Ess.Guid`/`Ess.Name`), `01_math.lua` (`Ess.Math`),
`02_str.lua` (`Ess.Str`), `03_color.lua` (`Ess.Color`), `04_vec.lua` (`Ess.Vec`), `22_state.lua`
(`Ess.State`, `Ess.SaveVar`), and `53_rng.lua` (`Ess.RNG`). `00_core.lua` loads first (the `00_` prefix is
deliberate) and has zero dependencies on the rest of Ess — literally everything else in the framework
depends on it.

`Ess.Str`, `Ess.Color`, and `Ess.Vec` are pure Lua — no engine calls, no dependencies on the rest of
`Ess` — so unlike most of this framework they can be (and are) execute-verified offline, without the game
running, via `tools/checkpure.py` (a [lupa](https://pypi.org/project/lupa/)-embedded-Lua test harness that
loads the real `src/*.lua` files and asserts against them). Where this page says a function is
"execute-verified offline," that's the method: real source, run outside the game, not a claim of a live
in-game test.

None of these namespaces carry a three-tier `Raw`/Core/`Easy` split — they're small, single-purpose
utilities where a beginner/advanced gap doesn't really exist. You just call them.

## Ess.Log

```lua
Ess.Log(msg)
```

Every `Ess.*` message goes through this so log lines are consistently prefixed (`"[Ess] " .. tostring(msg)`)
and easy to grep out of `lua_loader_printf.log`. It routes through `Loader.Printf`, and is guarded so a
missing `Loader` global can't make `Ess.Log` itself throw.

## Ess.Safe

The single most duplicated shape in the whole project is `local ok, r = pcall(...); if not ok then
Loader.Printf(...) end`. `Ess.Safe` fixes it in one place. It's fixed-arity — up to 4 return values — rather
than a generic table-pack/unpack dance: plenty for every native call in this corpus, and much easier to read.

| Function | Signature | Notes |
|---|---|---|
| `call` | `Ess.Safe.call(fn, ...) -> ok, a, b, c, d` | Wraps any engine call — a function reference plus its args, or a zero-arg closure for a multi-statement body. Logs once via `Ess.Log` on failure. |
| `quiet` | `Ess.Safe.quiet(fn, ...) -> ok, a, b, c, d` | Same shape, but never logs — for calls expected to fail sometimes as part of normal control flow (e.g. probing whether an object has a label), where a log line on every failure would just be noise. |
| `string` | `Ess.Safe.string(ok, val, fallback) -> s` | Only trust a native return as a string if it really is one — some calls return an unexpected type (bare userdata) on edge cases. Pass `Ess.Safe.call`'s own `(ok, val)` straight through: `Ess.Safe.string(Ess.Safe.call(Object.GetName, u))`. `fallback` defaults to `"?"`. |
| `template` | `Ess.Safe.template(sTemplate) -> bool` | The canonical "is this actually a spawnable template name" guard: `true` only for a non-empty, non-whitespace string. |

`Ess.Safe.template` exists because a blank/whitespace/non-string template name makes `Pg.Spawn` (and
everything built on it) hard-CTD the engine in native C++ — and `pcall` cannot catch a native crash, only a
Lua error, so the check has to happen *before* the call. That exact guard used to be re-inlined by hand in
roughly six places (`Object.spawn`, `Vehicle.followGhost`, `Bones.attachFX`, `UI.Menu`'s `ctx:spawn`,
`Contract._safeSpawn`), and two spawn paths — the original `Contract` `Pg.Spawn` gap and, more recently, the
copter path in `Ess.Support.reinforce` — missed it by hand before this existed. `Ess.Safe.template` is one
call instead of re-deriving the guard: see [Ess.Support](support) for the `reinforce` consumer. The guard
itself is execute-verified offline via `tools/checkpure.py`; existing inline copies aren't required to
migrate, just new code.

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

Note this is distinct from `Ess.Object.displayName(uGuid)` (covered on [Identity & World
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
via live testing — with one exception, see below.

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
hard-launched car. See [Ess.Camera](camera-bones#ess-camera) for the full write-up; `Ess.Vec.lerp` itself
stays in the offline-verified bucket above.

## Ess.Math

Geometry/number helpers this project kept re-deriving file after file — spawn-ahead forward trig, camera
orbit/dolly lerps, grid placement, distance checks. One confirmed-correct home for each, loaded right after
`00_core` (pure functions, no other `Ess` dependencies).

**Engine convention (load-bearing, live-calibrated):** Y is up; the horizontal plane is X/Z. A yaw's FORWARD
vector is `(-sin(yaw), +cos(yaw))` in `(x, z)` — the exact projection `Ess.Object.spawnAhead` was calibrated
against in-engine, accurate to about 4 degrees (the parallax between the character's facing and the
third-person camera). `angleTo`/`pointAhead` below are consistent with it: a yaw from `angleTo` fed to
`Object.SetYaw` faces the way you'd expect, and `pointAhead` matches `spawnAhead`'s own projection exactly.

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

Real usage, from the shipped `random_selection` recipe:

```lua
local rng = Ess.RNG.new(1234)                                  -- reproducible; Ess.RNG.new() = time-seeded

local d6   = rng:int(6)                                        -- an integer in [1, 6]
local coin = rng:chance(0.5)                                   -- true ~half the time
local pick = rng:pick({ "AH1Z", "Mi35", "WZ10" })              -- one element of a list (uniform here;
                                                                -- pass {w=} weights on table entries for weighted)
```

## See also

- [Essentials (Ess)](index) — the framework index this page belongs to.
- [Identity & World Query](identity-query) — `Player`, `Object`, `Vehicle`, `Probe`, `Human`, `Impulse`; the
  next tier up, built on these primitives (`Ess.Object.faceToward` uses `Ess.Math.angleTo`, `Ess.Impulse`
  uses `Ess.Player`/`Ess.Object`, and so on).
- [Ess.Easy](easy) — the beginner-tier one-liner presets built on top of all of this.
