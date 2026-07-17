---
title: "Camera, Bones & Spatial"
parent: Essentials (Ess)
nav_order: 7
---

# Camera, Bones & Spatial

## Overview

`Ess.Camera`, `Ess.Bones`, and `Ess.Points` cover everything spatial: taking over the camera for a
scripted shot, reading/attaching to any bone or hardpoint on a character or vehicle, and picking spawn
points out of a coordinate list. Neither `Ess.Camera` nor `Ess.Bones` needs a running mission — both work
against any live object guid — and `Ess.Points` is pure data transforms you can unit-test with the game
closed.

Part of [Essentials (Ess)](index). See [Ess.Easy](easy) for the beginner-tier one-liners each namespace
below also exposes.

## Ess.Camera

⚠ **Three native tables share the word "Camera" here, and `Ess.Camera` deliberately spans all three** —
because from a modder's chair they're all "camera/screen effects," even though they're different engine
tables with different argument shapes:

| Ess function(s) | Native table | Argument shape |
|---|---|---|
| everything except `fov`/`restoreFov`/`fade` | [`Camera`](../namespaces/camera) | a camera **guid** (from `Player.GetCamera`) |
| `fov`, `restoreFov` | `Graphics.Camera` (`SetFovParams`/`RestoreFovParams`) | a player **index**, not a guid |
| `fade` | `Graphics.Effect` (`CameraFade`) | no guid/index at all — a global fade |

This isn't an `Ess` design choice, it's a confirmed cross-namespace footgun in the engine itself (see
[Graphics](../namespaces/graphics)'s own "naming collision" warning) — `Ess.Camera` just keeps that footgun
from leaking into your own code by hiding which table each call actually hits.

### Screen & lens effects

| Function | Signature | What it does |
|---|---|---|
| `lookAtAnchor` | `Ess.Camera.lookAtAnchor(x, y, z, i) -> uAnchor \| nil` | Spawns a small anchor prop at `(x,y,z)` and binds `Camera.SetLookAt` to it. |
| `staleAxisDecay` | `Ess.Camera.staleAxisDecay(axes, timeoutMs) -> tracker` | Forces a controller axis back to 0 after it goes idle for `timeoutMs` (default 150). |
| `followHardpoint` | `Ess.Camera.followHardpoint(uGuid, hp, i, interval) -> stop()` | Repoints the camera at a moving hardpoint every `interval` s (default 0.05). |
| `shake` | `Ess.Camera.shake(i, sPreset, uSource, nAmplitude, nDuration)` | `Camera.Shake`; preset defaults to `"ShakeCameraMedium"`. |
| `stopShake` | `Ess.Camera.stopShake(i, uSource)` | Stops an ongoing `"ShakeCameraConstantlyRandom"` shake. |
| `fov` | `Ess.Camera.fov(i, nAngle, nDuration)` | `Graphics.Camera.SetFovParams(i, nAngle, nDuration)` — blends field of view. |
| `restoreFov` | `Ess.Camera.restoreFov(i, nDuration)` | `Graphics.Camera.RestoreFovParams(i, nDuration)`. |
| `fade` | `Ess.Camera.fade(nAmount)` | `Graphics.Effect.CameraFade(nAmount)` — 0 clear, 1 black. |

**`lookAtAnchor`** exists because of a confirmed engine quirk documented in the
[freecam deep dive](../deep-dives/freecam): `Camera.SetPosition` silently no-ops until an active
`Camera.SetLookAt` binding exists — not even a hardcoded, oversized teleport moves the camera without one.
The fix is spawning a tiny anchor prop and pointing `SetLookAt` at it once. It defaults to spawning
`"TinyGeometry"`, **not** `"Verification Camera"` — a directly-confirmed gotcha: `Pg.Spawn("Verification
Camera", ...)` into a *live, running* world triggers a support/camera call-in that fails and despawns it
almost immediately, so it's only safe as a paused-world anchor. `"TinyGeometry"` is confirmed safe
mid-gameplay instead (WaveDefense's own drop markers and airstrike anchors use it, live, repeatedly).

**`staleAxisDecay`** wraps another freecam-deep-dive gotcha: the engine's `ControllerInput` event omits an
axis field entirely once it goes idle, rather than sending one final 0 — naively "only update when present"
freezes a stick at its last nonzero reading forever. Call `tracker:update(tInput, now)` once per input
event (`now` = your own running wall-clock seconds); `tracker.values[name]` always reads the current,
possibly-decayed-to-0 value.

**`followHardpoint`** is the fallback for keeping a camera pointed at a moving hardpoint where the native
object+hardpoint camera form no-ops: it re-reads `Object.GetHardpointPosition` every tick and pushes the
result straight into `Camera.SetPosition`. It **requires** an active `SetLookAt` binding to already exist
(see `lookAtAnchor` above) — and it is explicitly **not** a fix for the vehicle gunning camera:
`Player.GetCamera` while seated in a turret is confirmed to not be the actual active camera object at all
(the [gunning-camera hard limit](../deep-dives/bone-manipulation#what-this-does-not-unlock-the-gunning-camera)) —
don't expect this helper to reach it.

**`shake`/`stopShake`** wrap `Camera.Shake` exactly as confirmed on the
[Camera namespace page](../namespaces/camera): `"ShakeCameraMedium"` is a one-shot (an explosion, an
impact), `"ShakeCameraConstantlyRandom"` is ongoing and needs the matching `stopShake` call or it runs
until the player leaves the level — `shake` defaults to the one-shot preset specifically because that's
the safe default for a single call.

**`fov`/`restoreFov`/`fade`** are included here because a modder looking for "any screen/camera effect"
looks under Camera — but check the table above again before using them, they're different native tables
taking a different argument shape than everything else on this page. `fade` exposes no duration argument:
every confirmed real call site (the hijack cinematic in `resident/mrxactionhijack.lua`) passes a bare `0`
or `1`, so none is guessed here.

`Ess.Easy.Camera.shake(i)` / `.fadeOut()` / `.fadeIn()` are zero-config presets over `shake`/`fade` — see
[Ess.Easy](easy).

### Cinematic take-over

⚠ **Steals mouse/look control from the player** until you call `endCinematic` (or the fire-blind
`panicRevert`). Always provide a way back.

The confirmed-live sequence this sub-API bakes in (distilled from `resident/mrxactionhijack.lua`):

```
Player.SetCinematicMode(p, true, true);  Camera.Blend(c, dur)
Camera.SetPosition(c, x, y, z, true)            -- fixed vantage
Camera.SetLookAt(c, uGuid, sBone)               -- object+bone form AUTO-TRACKS as it moves
Camera.Hold(c, true, false)
-- release:
Camera.Hold(c, false, false);  Camera.StopBlending(c);  Player.SetCinematicMode(p, false)
```

| Function | Signature | What it does |
|---|---|---|
| `beginCinematic` | `Ess.Camera.beginCinematic(i, nBlend) -> ok` | Enters cinematic mode and arms the blend. Records `{p, c}` per player index in `Ess.Camera._cine`. |
| `placeCamera` | `Ess.Camera.placeCamera(x, y, z, i)` | Fixed world vantage (`Camera.SetPosition`). |
| `blend` | `Ess.Camera.blend(i, nDur)` | Re-arms the blend time for the *next* `placeCamera` — for discrete moves only. |
| `lookAtObject` | `Ess.Camera.lookAtObject(uGuid, sBone, i)` | Locks onto an object (+ optional bone); auto-tracks as it moves. |
| `lookAtPoint` | `Ess.Camera.lookAtPoint(x, y, z, i)` | Locks onto a fixed world point. |
| `hold` | `Ess.Camera.hold(i)` | Pins the current framing (`Camera.Hold(c, true, false)`). |
| `endCinematic` | `Ess.Camera.endCinematic(i)` | Releases control back to the player and stops any active `watch`/`orbit` loop. |
| `panicRevert` | `Ess.Camera.panicRevert()` | Force-releases **every** active cinematic — the always-works escape hatch; the lua-bridge still accepts commands while control is locked, so this can be fired blind to recover. |

**The smoothness rule** (confirmed live against real orbit/cinematic scripts): a *moving* camera must enter
cinematic mode with `blend 0` — an instant blend. With the default 1 s blend, every per-tick `placeCamera`
restarts a 1-second interpolation and the camera rubber-bands (that's the "jitter"). With blend 0, per-tick
`placeCamera` plus a re-issued `lookAtObject`/`lookAtPoint` each tick is smooth instead. The object-attach
camera forms are a confirmed dead end — they don't bind, don't chase them. `blend(i, nDur)` exists
separately for *discrete* moves (one `placeCamera` per blend, e.g. swinging the camera out to a new fixed
spot) — a per-tick moving camera still wants blend 0.

Remaining accepted quirk: `watch`/`orbit` (below) read the target's position each tick, so a fast-moving
target (a heli at speed, a crate still falling) quantizes and jitters slightly; it smooths out as the
target slows.

`Ess.Easy.Camera.watch(uGuid, opts) -> stop()` and `Ess.Easy.Camera.orbit(uGuid, opts) -> stop()` are the
finished shots built on this sub-API — a locked-off tracking shot (or `opts.chase` to trail from a fixed
angle) and a smooth orbit, respectively. Both return the same `stop`, which is `endCinematic(i)`. One real
recipe from the sample catalog:

```lua
local stop = Ess.Easy.Camera.orbit(car, { radius = 10, height = 4, speed = 45 })
-- ...later:
stop()   -- or Ess.Camera.panicRevert() as the fire-blind escape hatch
```

Full option lists (`at`/`height`/`look`/`bone`/`chase`/`angle`/`dist`/`chaseHeight`/`radius`/`speed`/
`startAngle`) and the moving-vehicle look-at caveat — `SetLookAt`'s object-track works on *character*
bones, not vehicle hardpoints, so tracking a heli means pointing the look at its pilot
(`opts = { look = pilotGuid, bone = "Bone_Chest" }`), not the vehicle itself — are covered on
[Ess.Easy](easy).

## Ess.Bones

`Ess.Bones` is a thin wrapper around the exact recipes confirmed in
[Reading and Attaching to Any Bone](../deep-dives/bone-manipulation) — every function below maps directly
onto that page's confirmed [`Object`](../namespaces/object) calls, not new capability layered on top. The
names themselves ultimately came out of the hash-cracking effort in
[Cracking the Bone-Name Hashes](../deep-dives/name-cracking); this namespace is what you *do* with a name
once you have one.

| Function | Signature | What it does |
|---|---|---|
| `attachFX` | `Ess.Bones.attachFX(uGuid, bone, template) -> uFx \| nil` | Spawn an FX at a bone and glue it there. |
| `detachFX` | `Ess.Bones.detachFX(uGuid, uFx) -> ok` | Undo `attachFX`. |
| `waitForReady` | `Ess.Bones.waitForReady(uGuid, cb, maxTries)` | Poll until a freshly-spawned model's transform has initialized. |
| `aimVector` | `Ess.Bones.aimVector(uGuid, hpBase, hpTip) -> dx, dy, dz \| nil` | The axis between two hardpoints — a turret's barrel line. |
| `probeNames` | `Ess.Bones.probeNames(uGuid, prefixes, suffixes) -> hits, nTried` | Sweep prefix × suffix candidate names. |

**`attachFX(uGuid, bone, template)`** is exactly the deep dive's confirmed
[3-call attach recipe](../deep-dives/bone-manipulation#attaching-the-recipe), wrapped in one function: read
the bone's world position with `Object.GetHardpointPosition`, `Pg.Spawn` the template there, then
`Object.Attach` + `Object.SetTransformToObject` to glue it on and snap it exactly onto the bone before it
can drift a frame. It rejects a blank template up front (a blank string would CTD `Pg.Spawn`) and returns
`nil` if any pcall'd step fails — a bad bone name or a spawn failure. Any `hp_*` hardpoint or raw `bone_*`
skeleton joint works as `bone`, per the deep dive's central finding that both resolve through the same
hashed lookup.

**`detachFX(uGuid, uFx)`** is the deep dive's reverse recipe — `Object.Detach` then `Object.Remove` — and
is nil-safe: calling it with a `nil` `uFx` is a no-op, not an error, so cleanup code doesn't need its own
guard around it.

**`waitForReady(uGuid, cb, maxTries)`** exists for the deep dive's confirmed
[fresh-spawn gotcha](../deep-dives/bone-manipulation#gotcha-a-freshly-spawned-model-isn-t-ready-for-0-3-s):
a just-`Pg.Spawn`'d model's hardpoints read `nil` for a beat because its skeleton hasn't initialized yet.
Rather than a fixed `Event.Create(Event.TimerRelative, {0.3}, ...)` delay, this polls `Object.GetPosition`
every 0.1 s via `Ess.Loop` and calls `cb(uGuid)` as soon as it resolves — `maxTries` defaults to 6 (~0.6 s,
comfortably past the documented ~0.3 s window), and it gives up and calls `cb` anyway past that so a caller
is never left hanging on a guid that's genuinely broken. Note it checks the object's *overall* position,
not a specific bone, since it doesn't know which hardpoint the caller ultimately wants (a character and a
vehicle have entirely different bone names) — if you already have one exact bone name in mind, polling
`Object.GetHardpointPosition` on that name directly is a strictly stronger check; do that inline instead.

**`aimVector(uGuid, hpBase, hpTip)`** is the deep dive's
["Bonus: you can now read a turret's real aim direction"](../deep-dives/bone-manipulation#bonus-you-can-now-read-a-turret-s-real-aim-direction)
recipe, generalized: the vector between two hardpoints on the same object is the aim/facing axis of
whatever they mount. Confirmed live on the Allied Destroyer's cannon with `hpBase = "hp_seat_cannon"`
(breech) and `hpTip = "hp_barreltip_cannon"` (muzzle) — genuinely new capability the original destroyer
deep dive had said wasn't Lua-reachable, until the bone-probe work proved otherwise. Returns `nil` if
either hardpoint doesn't resolve.

**`probeNames(uGuid, prefixes, suffixes)`** generalizes the `DestroyerTool.ProbeHardpoints` sweep that the
[name-cracking effort](../deep-dives/name-cracking) itself grew out of: it builds every `prefix..suffix`
combination and pcall-probes `Object.GetHardpointPosition` for each, returning the hits plus how many
candidates were tried in total. **Carry the same hard caveat everywhere this is used**:
`GetHardpointPosition` is hash-keyed, so a garbage string can collide onto a real bone's hash and return
real, valid coordinates — a hit here proves the *string* is a valid handle for *some* real node, not that
it's that node's true dev name (exactly the collision problem the name-cracking page spends most of its
length on). This is a research/discovery tool, not something to build production logic on top of the
assumption that a hit means what its text suggests.

A real usage from the sample catalog — pinning an effect to your own head bone, and handling a fresh
vehicle spawn's startup delay:

```lua
local plume = Ess.Bones.attachFX(me, "Bone_Head", "global_particle_env_smokeplume_distance_tall")
...
local car = Ess.Object.spawn("Veyron", px + 10, py, pz)
if car then
    Ess.Bones.waitForReady(car, function(u)
        local x, y, z = Ess.Object.pos(u)
        -- car's transform is now confirmed initialized
    end)
end
...
Ess.Bones.detachFX(me, plume)
```

## Ess.Points

Pure spawn-point data transforms, ported from `WaveDefense.lua`'s `bucketArena`/`idealPoints` and
generalized beyond wave-defense. No live world touched — these operate on plain coordinate tables, so
they're testable offline/synthetically with no game running at all. A spawn point is a 4-tuple
`{x, y, z, r}` (matching MissionForge's arena export shape), where `r` is an optional radius-tier hint
(defaults to 3, infantry-tier, if omitted).

| Function | Signature | What it does |
|---|---|---|
| `bucket` | `Ess.Points.bucket(spawnList) -> { inf = {...}, veh = {...}, heli = {...} }` | Splits a point list into infantry/vehicle/heli tiers by radius. |
| `ideal` | `Ess.Points.ideal(pts, refX, refZ, opts) -> { p, ... }` | Nearest-first, distance-windowed point selection around a reference. `opts = {minDist=18, maxDist=80, maxCount=24}`. |

**`bucket`** sorts by radius: `r <= 5` → infantry, `r <= 15` → vehicle, `r > 15` → heli — matching
MissionForge's own radius-tier convention. If *no* point qualifies for the infantry tier, `.inf` falls
back to the full input list rather than an empty table (WaveDefense's own "any point can take infantry"
fallback), so a caller drawing from `.inf` is never left with zero options.

**`ideal`** scores every point by squared horizontal distance to `(refX, refZ)` — **Y is deliberately
ignored**, matching the source (arena spawn points are compared on the horizontal plane only) — then
applies a three-tier fallback so a caller never gets an empty result it has to special-case:

1. Points within `[opts.minDist, opts.maxDist]` (default 18/80), nearest first, capped at `opts.maxCount`
   (default 24).
2. If fewer than 4 came back, drop the `maxDist` ceiling (keep only the `minDist` floor) and retry.
3. If still zero, return every point unfiltered.

The 18/80/24 defaults are WaveDefense's own confirmed-working values ("use more spawn points → fewer
enemies per point").

## See also

- [Essentials (Ess)](index) — the framework index.
- [Ess.Easy](easy) — `Ess.Easy.Camera.watch`/`orbit`/`shake`, and every other namespace's one-liner tier.
- [Reading and Attaching to Any Bone](../deep-dives/bone-manipulation) — the confirmed research `Ess.Bones` wraps.
- [Cracking the Bone-Name Hashes](../deep-dives/name-cracking) — where the bone names themselves came from.
- [Freecam](../deep-dives/freecam) — the `SetPosition`-needs-`SetLookAt` and stale-axis gotchas `Ess.Camera` bakes in.
- [Camera](../namespaces/camera), [Graphics](../namespaces/graphics), [Object](../namespaces/object) — the raw engine namespaces underneath.
