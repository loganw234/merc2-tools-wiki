---
title: Cinematic
parent: Essentials (Ess)
nav_order: 10
---

# Cinematic

## Overview

`Ess.Cinematic` is a declarative **cutscene timeline** runtime: hand it an ordered list of steps — camera
cuts/dollies/orbits/chases, waits, spawns, actor facing, AI orders, helicopter fly-ins, narration (banner /
subtitle / hint / VO), fades, shakes, music/sound cues, teleports, faction relations — and it plays them in
order, pacing each with a per-step `hold` duration.

It is an **orchestrator, not new engine spelunking** — every step handler is built entirely on primitives
documented elsewhere on this wiki that are already confirmed live: `Ess.Camera`'s cinematic take-over
(`beginCinematic`/`placeCamera`/`lookAtObject`-auto-track/`fade`), `Ess.Object.spawn`, `Ess.AIOrders.command`
(see [Encounter Toolkit](encounter-toolkit)), `Ess.Vehicle.flyTo`, `Ess.Hud`, `Ess.Sound`/VO, and
`Ess.Player.teleport`. See [Camera, Bones & Spatial](camera-bones) for the camera primitives `Cinematic`
drives underneath every `camera`/`orbit`/`chase` step.

This is the engine a full "cinematic suite" for mission building sits on: MissionForge captures the
**spatial** steps in-game (camera vantages, look-at points, action markers), a companion web tool authors
the **sequencing** (order/durations/params), and both just emit a `steps` list this runtime plays.
`Ess.Contract` plays one as a mission intro via `def.cinematic` (see [Contract Engine](contract)).

## `Ess.Cinematic.play(steps, opts)`

```lua
Ess.Cinematic.play(steps, opts) -> seq | nil
```

`steps` is a list of `{type=, <params>, hold=}` tables — see the step vocabulary table below for every
`type` and its params. `opts`:

| `opts.` | Default | Meaning |
|---|---|---|
| `camera` | `true` | Take over the screen via `Ess.Camera.beginCinematic`/`endCinematic`. Set `false` to run the timeline (spawns, orders, HUD, etc.) without any camera takeover at all. |
| `blend` | `0` | Camera blend passed to `beginCinematic` — `0` is instant cuts, matching the confirmed rule that a *moving* camera (dolly/orbit/chase) needs Blend 0 to stay smooth. |
| `skippable` | `true` | Whether the skip key fast-forwards the timeline. |
| `skipKey` | `0x1B` (ESC) | The virtual-key code polled via `Ess.Input.poll()` each tick to trigger a skip. |
| `startFade` | `false` | If `true`, opens on a black screen (`Ess.Camera.fade(1)`) — fade back in via a `fade` step. |
| `i` | `0` | Player index (co-op seat) the cinematic plays for. |
| `onDone` | — | `fn(ctx)` called after the sequence finishes (naturally, by skip, or by `stop()`) — fires **after** control/camera are already fully restored. |

**Timing model:** steps fire strictly in order. After firing a step, the timeline advances `hold` seconds
before firing the next one — `hold` omitted or `0` means the *next* step fires the **same tick**, which is
how several actions (e.g. a `spawn` + a `subtitle`) start together. A `{type="wait"}` step does nothing but
occupy a hold — read its duration from `time`/`seconds` if `hold` itself is omitted.

**Step context (`ctx`), shared across every step in one sequence:**
- `ctx.named[name] = guid` — a `spawn` step with `name=` registers here; `camera look=`/`order target=`/
  `fly target=` and other refs resolve names against this table (plus the special refs `"player"`/`"hero"`
  and `"partner"`/`"player2"`, and a raw guid passed through as-is, and finally `Ess.Guid(ref)` as a
  world-object-name fallback).
- `ctx.groups[grp] = {guids}` — a `spawn` step with `group=` buckets into here **and** registers the group
  with `Ess.AIOrders.setGroup`, so an `order` step (or any other `Ess.AIOrders` call) can command it.
- `ctx.track` — an `Ess.Track`. A `spawn` marked `ephemeral=true` is cleaned up when the cutscene ends; by
  default a `spawn` **persists** into the mission (mission actors are meant to outlive the cutscene that
  introduced them).

**Guarantee: a cutscene can never strand the player.** Camera and control are **always** restored on
finish, skip, or `stop()` — this isn't opt-in behavior, it's unconditional in the `finish()` internals (see
Guarantees below).

**ESC-skippable:** pressing the skip key fast-forwards — every remaining step still **fires** (so any
mission actor the cutscene spawns or positions ends up in the right place), just with every remaining
`hold` collapsed to zero.

## Step type vocabulary

| `type` | Params | What it does |
|---|---|---|
| `wait` | `time=` / `seconds=` | Pure pause — no handler logic, the `hold` alone does the work. |
| `camera` | `at={x,y,z}`, `look=<ref>`, `lookAt={x,y,z}`, `bone=`, `to={x,y,z}` | Cuts the camera to `at`, framing either a world point (`lookAt`) or an object it then **auto-tracks** as it moves (`look`, optionally a specific `bone` — e.g. `look="heli", bone="Bone_Chest"` tracks a pilot). Give `to` for a **dolly**: the camera lerps `at`→`to` across this step's `hold`. Point-look (`lookAt`) is routed through a reusable `TinyGeometry` anchor object rather than the coordinate form of `SetLookAt`, working around a confirmed engine quirk: `Camera.SetPosition` no-ops until an active *object-form* `SetLookAt` binding exists, and the coordinate form never creates that binding — a fixed shot framing a bare point would otherwise leave the camera stuck on the player. See [Camera, Bones & Spatial](camera-bones). |
| `orbit` | `target=<ref>`, `radius=`, `height=`, `speed=`, `startAngle=`, `look=<ref>`, `bone=` | Camera smoothly orbits `target`, re-reading its live position every tick — the showcase shot for a spawned object. `look` defaults to `target` itself if omitted. |
| `chase` | `target=<ref>`, `angle=`, `dist=`, `height=`, `look=<ref>`, `bone=` | Camera follows a moving `target` from a **fixed world angle** (a clean trailing shot; a fixed angle avoids the velocity-heading jitter of an auto-trail). Tracking a moving vehicle: point `look=` at its pilot with `bone="Bone_Chest"` — `SetLookAt` object-tracking works on character bones, not vehicle hardpoints. |
| `face` | `who=`/`target=<ref>`, `at={x,y,z}` **or** `toward=<ref>` | A direct action (not a camera move): turns a spawned actor to face a world point, or another named actor. |
| `spawn` | `template=`, `at={x,y,z}`, `yaw=`, `name=`, `group=`, `ephemeral=`, `invincible=` | Spawns one object (`Ess.Object.spawn`'s blank-template guard applies). `name=` registers it in `ctx.named`; `group=` buckets it in `ctx.groups` and registers the group with `Ess.AIOrders`. Persists by default — `ephemeral=true` marks it for cleanup on `ctx.track` when the cutscene ends. `invincible=true` calls `Ess.Object.setInvincible`. |
| `order` | `group=`/`target=`, `behavior=`, `at=`, `points=`, `radius=`, `speed=`, `loop=`, `attackTarget=` | Commands a spawned group (or a single named/resolved `target`) with any `Ess.AIOrders` behavior — see [Encounter Toolkit](encounter-toolkit) for the full behavior list (move/patrol/attack/defend/hold/face/follow/flee/enter/deploy/animate). Runs through `Ess.AIOrders.command(guids, behavior, opts, ctx.track)`. |
| `fly` | `target=<heli ref>`, `at={x,y,z}`, `height=` | Sends an AI helicopter to a point via `Ess.Vehicle.flyTo` (`Ai.Deliver` underneath). |
| `say` / `banner` | `text=`/`msg=` | A clean centered narration banner (`Ess.Hud.banner`). `banner` is a plain alias for `say`. |
| `subtitle` | `text=`/`msg=`, `hold=` | A lower-third radio-style caption (`Ess.Hud.radio`) — the better fit for cutscene dialogue than the big centered banner. Stays up for `hold` seconds (default 5), then clears itself. |
| `hint` | `text=`/`msg=`, `id=` | The persistent tutorial-style HUD popup (`Ess.Hud.hint`) — stays until explicitly hidden or the cutscene ends (the running `id`, default `"ess_cinematic"`, is auto-hidden in `finish()`). |
| `vo` | `lines=`/`text=`, `gap=` | A voice-over line sequence via `MrxVoSequence.Start`, with `gap` seconds between lines (default 1). A no-op if VO isn't loaded on this install (`pcall`-guarded, checked for presence first). |
| `music` | `cue=` or `stop=true` | Starts (or stops) the special mission music via `MrxMusic`. `cue=""` or `cue="stop"` is equivalent to `stop=true`. Default cue if none given: `"mu_pmc_panicloop_01"`. |
| `sound` | `cue=`, `on=<ref>` | A one-shot sound *effect* (`Ess.Sound.cue`), distinct from music/VO. `on=` attaches it to an object (positional — an alarm, an impact); omit for a plain UI/HUD one-shot. |
| `fade` | `to=0\|1` or `out=true` | Full-screen fade (`0` clear, `1` black) via `Ess.Camera.fade`. Pair two steps for a fade-out-then-in transition. |
| `shake` | `preset=`, `amplitude=`, `duration=` | Camera shake for impacts, via `Ess.Camera.shake`. |
| `teleport` | `at={x,y,z}`, `yaw=` | Warps the hero(es) via `Ess.Player.teleport` — co-op safe. |
| `relations` | {% raw %}`pairs={{a,b,set}, ...}`{% endraw %} | Sets a faction stance for the scene via `Ess.Relations.apply`. **Not auto-restored** — a mission's relations are meant to persist past its intro; use `Ess.Relations` directly (holding the handle) if you need this scoped/reverted instead. |
| `func` / `custom` | `fn=function(ctx, seq) ... end` | Arbitrary code — the escape hatch for anything not covered above (also the web tool's own "custom" step type). |

Every step handler is `pcall`-wrapped individually (`fireStep`): a bad or erroring step is logged and the
**timeline carries on** rather than aborting the whole cutscene.

## Reusable cutscenes: `define` / `playNamed`

```lua
Ess.Cinematic.define(id, steps, opts)          -- register a reusable cutscene under a name
Ess.Cinematic.playNamed(id, extraOpts) -> seq | nil
```

`define` registers a `steps`/`opts` pair under a string `id` (logged; re-defining under the same load is
fine — the registry resets fresh every script load). `playNamed` plays a previously defined cutscene;
`extraOpts`, if given, is shallow-merged **over** the defined `opts` (so the same cutscene can be replayed
with, say, a different `onDone` callback each time) rather than replacing them outright.

Per the source's own header comment, a defined cutscene is meant to be referenced either directly via
`playNamed`, from a contract's `def.cinematic = "id"`, or from a trigger's own cinematic support effect
(`{effect="cinematic", cinematic="id"}`) — the contract-side wiring for the latter two lives in
`Ess.Contract`'s own source, which is outside what this page verifies; treat that specific integration as
documented-in-comment rather than independently confirmed here.

## Control API

```lua
Ess.Cinematic.skip()             -- fast-forward the active cutscene (remaining steps fire, holds collapse to 0)
Ess.Cinematic.stop(seq)          -- end it now, restore control, run onDone (defaults to the active sequence)
Ess.Cinematic.isPlaying() -> bool
Ess.Cinematic.active() -> seq | nil
```

Only one cutscene plays at a time — calling `play()` while one is already active calls `stop()` on it first
(the new one supersedes, it doesn't queue or error).

## Guarantees

- **Camera/control are always restored.** `finish()` unconditionally calls `Ess.Camera.endCinematic` (unless
  `opts.camera == false`, since then it never took control) and `Ess.Camera.fade(0)` — the screen can never
  be left stuck faded to black, even if the sequence ends mid-fade.
- **A persistent `hint` step is always cleared** on finish, via `Ess.Hud.hideHint`.
- **Only `ephemeral=true` spawns are cleaned up** at the end (`ctx.track:closeAll()`) — everything else a
  cutscene spawns is left in the world by design, since mission actors are meant to outlive their intro.
  `ephemeral` spawns and `follow`-behavior timers (via `AIOrders`) both ride on the same `ctx.track`.
  `onDone` fires *after* this cleanup and after the "done" log line, so a callback's own logging reads in
  the correct order.
- **ESC-skippable by default**, configurable via `opts.skippable`/`opts.skipKey`; the key that launched the
  cutscene itself is discarded (`Ess.Input.clear()`) so triggering play doesn't also instantly skip it.
- **A single bad step never aborts the timeline** — each step handler is individually `pcall`-wrapped and
  logged on error, then the sequence continues to the next step.
- A reload resets `Ess.Cinematic._active` to `nil` unconditionally — a sequence in flight when the world
  reloads is simply gone, never resumed as a stale handle.

## Easy tier

`Ess.Easy.Cinematic` is the zero-opts entry point: `play(steps, onDone)` (skippable, camera takeover, no
other options to think about) and `shot(at, lookAt, seconds) -> step` — sugar that builds one static
`{type="camera", ...}` step, so a hand-authored list can read as a storyboard: `{ shot(a,b,4), shot(c,d,3),
... }`. See [Ess.Easy](easy) for the full one-liner catalog.

## Example

From the shipped `a_cutscene.lua` recipe — a two-shot cutscene with a named ephemeral actor:

```lua
local steps = {
    { type = "spawn",    template = "Veyron", at = { px + 14, py, pz }, name = "hero_car", ephemeral = true },
    { type = "camera",   at = { px + 22, py + 4, pz + 6 }, look = "hero_car", hold = 1.2 },
    { type = "subtitle", text = "Recipe: a two-shot cutscene.", hold = 0 },
    { type = "orbit",    target = "hero_car", radius = 9, height = 4, speed = 60, hold = 1.2 },
}

Ess.Cinematic.play(steps, {
    skippable = true,
    onDone = function()
        -- fires after the last step AND after control is fully restored
    end,
})
```

## See also

- [Camera, Bones & Spatial](camera-bones) — `Ess.Camera`'s cinematic take-over, `SetLookAt` object-vs-point
  quirk, and the bone/hardpoint tracking `camera`/`orbit`/`chase` steps drive.
- [Encounter Toolkit](encounter-toolkit) — `Ess.AIOrders` (the `order` step) and `Ess.Relations` (the
  `relations` step), documented in full there.
- [Sound & HUD](sound-hud) — `Ess.Hud.banner`/`.radio`/`.hint` and `Ess.Sound.cue`, the narration steps.
- [Contract Engine](contract) — `def.cinematic` plays one of these as a mission intro.
- [Essentials (Ess)](index) — the framework index this page belongs to.
