---
title: Markers
parent: Essentials (Ess)
nav_order: 5
---

# Markers

## Overview

`Ess.Mark` is, per its own source header, "the motivating example for the whole tiered design." There are
four independent ways to draw attention to something on this engine — a round-radar objective, a PDA map
blip, a floating in-world icon, and a ground ring — each with its own `Add.../Remove...` pair and its own
argument shape. The real lesson the framework's source draws from two existing call sites (the Contract
Framework marks all three surfaces unconditionally; WaveDefense deliberately marks radar+PDA only, skipping
the world icon so not every enemy clutters the world with a floating icon) is that the correct primitive
isn't "always mark all three" — it's **three independent opt-out toggles**, so one call covers any
combination without ever having to hand-assemble a multi-surface marker from raw pieces.

- **`Ess.Raw.Mark`** — the four marking surfaces as fully independent calls.
- **`Ess.Mark`** — one call per "thing" (`object` or `zone`), each surface an opt.
- **`Ess.Easy.Mark`** — three intent-named presets matching the two real conventions above, plus a
  zone-only ring.

## Ess.Raw.Mark

Each surface is a separate pair of calls. Radar and PDA registrations are keyed by name (`sName`, derived
from the guid) because their native `Remove...` calls remove by name, not by handle; the floating world
icon and the ground ring are keyed by a real `Marker.Add*` handle instead.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Raw.Mark.radar(uGuid, tex, rgb)` | `radar(uGuid, tex, rgb) -> sName \| nil` | `Hud.Radar:AddObjective(...)`. `tex` defaults to `"objective_action"`; `rgb` defaults to `{255, 200, 0}`. Fixed icon size (`10.667 x 10.667`) and sort order `5`. |
| `Ess.Raw.Mark.removeRadar(sName)` | `removeRadar(sName)` | `Hud.Radar:RemoveObjective({sName=sName})`. |
| `Ess.Raw.Mark.pda(uGuid, tex)` | `pda(uGuid, tex) -> sName \| nil` | `Pda.Map:AddBlip(...)`. `tex` defaults to `"icon_yellow_mc"`. Sort order `2`. |
| `Ess.Raw.Mark.removePda(sName)` | `removePda(sName)` | `Pda.Map:RemoveBlip({sName=sName})`. |
| `Ess.Raw.Mark.world(uGuid, tex, rgb, size, dist)` | `world(uGuid, tex, rgb, size, dist) -> handle \| nil` | The floating in-world icon — `Marker.AddBlip`. Returns a real handle, **not** a name. `tex` defaults to `"HUD_objective_action"`, `size` (on-screen icon size) defaults to `32`, `dist` (draw distance) defaults to `175` — real shipped call sites vary that between roughly `175` and `220`, so both are exposed rather than hardcoded. |
| `Ess.Raw.Mark.removeWorld(handle)` | `removeWorld(handle)` | `Marker.Remove(handle)`. Also used to remove a `worldDisc` handle (both are `Marker.Remove`-compatible). |
| `Ess.Raw.Mark.worldDisc(uGuid, radius, rgb, alpha)` | `worldDisc(uGuid, radius, rgb, alpha) -> handle \| nil` | A ground ring — `Marker.AddDisc`. Distinct from a floating icon: the "go here" zone marker. `radius` defaults to `15`, `alpha` defaults to `0.15`. |
| `Ess.Raw.Mark.pulse(uGuid, rgb)` | `pulse(uGuid, rgb)` | Flashes/pulses an object's **existing** marker in a color — `Marker.Pulse`. Confirmed (`mrxfactionmanager.lua`) to take the object's own `uGuid` directly, **not** a marker handle, unlike every other function in this file. |
| `Ess.Raw.Mark.haltPulse(uGuid)` | `haltPulse(uGuid)` | `Marker.HaltPulse(uGuid)` — same "takes the object guid" rule as `pulse`. |
| `Ess.Raw.Mark.showPlayerMarkers(bOn)` | `showPlayerMarkers(bOn)` | `Gui.EnablePlayerMarkers(bOn)` — a **global** on/off toggle for whether *other players'* HUD markers render at all, not per-guid like everything else here. Confirmed (`mrxbriefing.lua`): hide during a cutscene/briefing, restore after. |

`rgb` throughout is a plain `{r, g, b}` table; when omitted every function falls back to the same default
color, `{255, 200, 0}` (amber).

## Ess.Mark (Core)

One call per "thing," with every surface an independent opt. `Ess.Mark.object` targets an existing object's
`uGuid`; `Ess.Mark.zone` marks a bare world point by spawning its own invisible anchor prop first.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Mark.object(uGuid, opts)` | `object(uGuid, opts) -> handle` | Marks an existing object. Returns a compound handle table (`{uGuid, radarName?, pdaName?, worldHandle?, discHandle?}`) covering whichever surfaces were drawn. |
| `Ess.Mark.zone(x, y, z, radius, opts)` | `zone(x, y, z, radius, opts) -> handle \| nil` | Spawns a `TinyGeometry` anchor at `(x, y, z)` via `Ess.Object.spawn` (see [Identity & World Query](identity-query)) and marks it. Returns `nil` if the anchor fails to spawn. The zone **owns** its anchor — `Ess.Mark.clear` removes the prop for you. |
| `Ess.Mark.clear(handle)` | `clear(handle)` | Tears down every surface a handle actually used, plus the zone anchor prop if there was one. Safe on a partial handle — any missing/nil field is just skipped. |

`opts.kind` picks an icon set on both `object` and `zone`, from a fixed table (`OBJ_ICONS`, ported straight
from the Contract Framework's own `OBJ_ICONS` — the base game's `MrxTaskObjective` family):

| `kind` | Radar texture | World texture |
|---|---|---|
| `destroy` | `objective_destroy` | `HUD_objective_destroy` |
| `verify` | `objective_verify` | `HUD_objective_verify` |
| `defend` | `objective_defend` | `HUD_objective_defend` |
| `action` | `objective_action` | `HUD_objective_action` |
| `destination` | `objective_deliverable` | `HUD_objective_deliverable` |

### The opts, in full — and a naming gotcha

`object()`'s opts default **opt-out** (radar/pda/world all `true`) matching the Contract Framework's
"mark everything" convention — pass `radar=true, pda=true, world=false` to match WaveDefense's convention
instead:

- `opts.radar` (default `true`), `opts.pda` (default `true`) — same as the raw calls.
- `opts.world` (default `true`) — **the floating in-world icon.**
- `opts.disc` (default `false`) — **a ground ring** around the object (`opts.radius` default `15`,
  `opts.discAlpha` its fill).
- `opts.kind` (default `"action"`), `opts.rgb`, `opts.size`/`opts.dist` — passed through to the floating
  icon.

`zone()`'s opts:

- `opts.world` (default `true`) — **the ground ring** (`Marker.AddDisc`, `opts.discAlpha` its fill).
- `opts.radar` / `opts.pda` (default `true` each) — the round-radar/PDA blip on the same anchor.
- `opts.icon` (default `false`) — **also** drops a floating in-world icon on the anchor.
- `opts.kind` (default `"destination"`) picks the icon set for both the radar blip and the floating icon;
  `opts.size`/`opts.dist` tune the floating icon.

**The word `world` means opposite things on the two functions** — this is a genuine gotcha worth reading
twice, not a typo: on `object()`, `opts.world` is the *floating icon* and the ground ring is the separate
`opts.disc`. On `zone()`, `opts.world` is the *ground ring* and the floating icon is the separate
`opts.icon`. The asymmetry traces straight back to each function's real motivating call site — an object
usually wants its floating icon by default, a zone usually wants its ground ring by default — but it means
you cannot copy an `opts` table between `Ess.Mark.object` and `Ess.Mark.zone` and expect it to mean the same
thing.

## Ess.Easy.Mark

Three presets, matching the two real conventions the Core tier's opts were built to cover, plus a
zone-only ring. Small enough to read in full — this is the complete `31_mark_easy.lua` source, 21 lines,
sitting directly on top of `Ess.Mark`:

```lua
-- radar+PDA, no world icon -- matches WaveDefense's real convention (don't clutter the world with icons
-- for every enemy).
function Ess.Easy.Mark.enemy(uGuid)
    return Ess.Mark.object(uGuid, { radar = true, pda = true, world = false, kind = "action" })
end

-- all three surfaces -- matches ContractFramework's convention for a real mission objective.
function Ess.Easy.Mark.objective(uGuid)
    return Ess.Mark.object(uGuid, { radar = true, pda = true, world = true, kind = "action" })
end

-- world ring only -- the ground-disc "go here" case, no radar/PDA clutter.
function Ess.Easy.Mark.zone(x, y, z, r)
    return Ess.Mark.zone(x, y, z, r, { radar = false, pda = false, world = true })
end
```

| Function | Signature | Preset |
|---|---|---|
| `Ess.Easy.Mark.enemy(uGuid)` | `enemy(uGuid) -> handle` | Radar + PDA, **no** floating world icon. Kind `"action"`. |
| `Ess.Easy.Mark.objective(uGuid)` | `objective(uGuid) -> handle` | All three surfaces (radar, PDA, floating icon). Kind `"action"`. |
| `Ess.Easy.Mark.zone(x, y, z, r)` | `zone(x, y, z, r) -> handle \| nil` | Ground ring only — no radar/PDA clutter. (Remember: on `zone()`, `world = true` *is* the ring.) |

## Worked example

The real, confirmed recipe (`samples/recipes/mark_things.lua`) — an objective marker on the player's own
character plus a "go here" ground ring nearby, held for a few seconds, then torn down in two calls:

```lua
-- mark the player's own character as an objective (radar + PDA + floating icon).
local mObj = Ess.Easy.Mark.objective(Ess.Player.character(0))

-- drop a "go here" ground ring 10 units away (zone spawns its own anchor, no guid needed).
local px, py, pz = Ess.Player.pose(0)
local mZone = px and Ess.Easy.Mark.zone(px + 10, py, pz + 10, 8) or nil

-- ... later, one call each tears down every surface it drew (plus the zone's own anchor prop):
Ess.Mark.clear(mObj)
Ess.Mark.clear(mZone)
```

## Combining with Ess.Track

`Ess.Mark`'s handles are compound tables, not a single `Marker.Add*` handle — they don't plug directly into
an `Ess.Track` tracker's `:marker()` (which expects a raw handle). To fold a mark into a batch of tracked
cleanup, wrap it with the tracker's generic `:add()` escape hatch instead:

```lua
local tr = Ess.Track.new()
local m = Ess.Easy.Mark.enemy(uGuid)
tr:add(function() Ess.Mark.clear(m) end)   -- register the mark's teardown in the same batch
```

See [Tracking & Cleanup](tracking) for the full `Ess.Track` API and its worked example.

## See also

- [Essentials (Ess)](index) — the framework index.
- [Tracking & Cleanup](tracking) — the leak-prone `Add.../Remove...` pattern `Ess.Mark` is one instance of,
  and how to fold a mark handle into a tracker's batch.
- [Identity & World Query](identity-query) — `Ess.Object.spawn`, what `Ess.Mark.zone` uses to create its
  anchor prop.
