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
| `Ess.Raw.Mark.pda(uGuid, tex, sLabel)` | `pda(uGuid, tex, sLabel) -> sName \| nil` | `Pda.Map:AddBlip(...)`. `tex` defaults to `"icon_action_1_mc"`; `sLabel` defaults to the guid string. Sort order `2`. Both defaults exist because omitting either makes the blip look like the call never happened — see [Why the PDA blips were never visible](#why-the-pda-blips-were-never-visible). |
| `Ess.Raw.Mark.removePda(sName)` | `removePda(sName)` | `Pda.Map:RemoveBlip({sName=sName})`. |
| `Ess.Raw.Mark.world(uGuid, tex, rgb, size, dist)` | `world(uGuid, tex, rgb, size, dist) -> handle \| nil` | The floating in-world icon — `Marker.AddBlip`. Returns a real handle, **not** a name. `tex` defaults to `"HUD_objective_action"`, `size` (on-screen icon size) defaults to `32`, `dist` (draw distance) defaults to `175` — real shipped call sites vary that between roughly `175` and `220`, so both are exposed rather than hardcoded. |
| `Ess.Raw.Mark.removeWorld(handle)` | `removeWorld(handle)` | `Marker.Remove(handle)`. Also used to remove a `worldDisc` handle (both are `Marker.Remove`-compatible). |
| `Ess.Raw.Mark.worldDisc(uGuid, radius, rgb, alpha)` | `worldDisc(uGuid, radius, rgb, alpha) -> handle \| nil` | A ground ring — `Marker.AddDisc`. Distinct from a floating icon: the "go here" zone marker. `radius` defaults to `15`, `alpha` defaults to `0.15`. |
| `Ess.Raw.Mark.pulse(uGuid, rgb)` | `pulse(uGuid, rgb)` | Flashes/pulses an object's **existing** marker in a color — `Marker.Pulse`. Confirmed (`mrxfactionmanager.lua`) to take the object's own `uGuid` directly, **not** a marker handle, unlike every other function in this file. |
| `Ess.Raw.Mark.haltPulse(uGuid)` | `haltPulse(uGuid)` | `Marker.HaltPulse(uGuid)` — same "takes the object guid" rule as `pulse`. |
| `Ess.Raw.Mark.showPlayerMarkers(bOn)` | `showPlayerMarkers(bOn)` | `Gui.EnablePlayerMarkers(bOn)` — a **global** on/off toggle for whether *other players'* HUD markers render at all, not per-guid like everything else here. Confirmed (`mrxbriefing.lua`): hide during a cutscene/briefing, restore after. |

`rgb` throughout is a plain `{r, g, b}` table; when omitted every function falls back to the same default
color, `{255, 200, 0}` (amber). It does **not** reach the PDA layer —
see [Color reaches two of the three layers](#color-reaches-two-of-the-three-layers).

### Why the PDA blips were never visible

**`icon_yellow_mc` draws nothing.** It is a registered icon name that resolves to no art. Confirmed live
(2026-07-26) with four otherwise-identical blips side by side: `icon_action_1_mc` and
`icon_deliverable_1_mc` rendered, while `icon_yellow_mc` and a blip with *no* texture at all were both
blank.

That matters more than one bad name in a list, because `icon_yellow_mc` is the engine's own last-resort
fallback — the render path is `tBlip.sTexture or tMissionData.sDefaultBlipTexture or "icon_yellow_mc"`. Any
blip that falls all the way through that chain is invisible by construction, so passing nothing is exactly
as blank as passing the fallback. (`mrxutil.lua`'s `tObjPdaMarker` lists the name twice, first and last, and
also carries an empty string; it is in the engine's own vocabulary, it simply has no art behind it.)

It was also Ess's own default in three places — two of them on this page (`Ess.Raw.Mark.pda`'s `tex`
default and the `generic` kind's PDA leg; the third is `Ess.Pda.blip`'s `sTexture` default). That, not
anything about the call itself, is the real reason `Ess.Mark`'s PDA blips were never visible.

**An earlier pass diagnosed this as a missing label, and that was only half the story.** The label half is
real: a blip with no `sLabel` displays its *texture name*, because the render path's label slot is
`tBlip.sLabel or tMissionData.sDefaultBlipLabel` and with no label and no owning mission that goes nil, at
which point the movie shows the texture instead (confirmed live). But the text `icon_yellow_mc` people saw
on screen was the label fallback naming an icon that was never rendering in the first place — the blip was
not "an unlabelled dot," it was no dot at all. Both halves are fixed by the two defaults above: a texture
that actually draws, and a label that at least identifies the object.

## Ess.Mark (Core)

One call per "thing," with every surface an independent opt. `Ess.Mark.object` targets an existing object's
`uGuid`; `Ess.Mark.zone` marks a bare world point by spawning its own invisible anchor prop first.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Mark.object(uGuid, opts)` | `object(uGuid, opts) -> handle` | Marks an existing object. Returns a compound handle table (`{uGuid, radarName?, pdaName?, worldHandle?, discHandle?}`) covering whichever surfaces were drawn. |
| `Ess.Mark.zone(x, y, z, radius, opts)` | `zone(x, y, z, radius, opts) -> handle \| nil` | Spawns a `TinyGeometry` anchor at `(x, y, z)` via `Ess.Object.spawn` (see [Identity & World Query](identity-query)) and marks it. Returns `nil` if the anchor fails to spawn. The zone **owns** its anchor — `Ess.Mark.clear` removes the prop for you. |
| `Ess.Mark.clear(handle)` | `clear(handle)` | Tears down every surface a handle actually used, plus the zone anchor prop if there was one. Safe on a partial handle — any missing/nil field is just skipped. |

### Kinds: one name, three icons

The three surfaces do **not** share an icon namespace. The same objective is `HUD_objective_destroy` in the
world, `objective_destroy` on the radar and `icon_destroy_1_mc` on the PDA, and each name is validated
against a different fixed table in `mrxutil.lua` — `tObjWorldMarkers`, `tObjRadarMaker`, `tObjPdaMarker` —
by a different lookup function. Nothing in the engine relates the three; the correspondence is purely a
naming convention, which is why it has to be written down somewhere at all.

The table `Ess.Mark` inherited from the Contract Framework named only **two** of the three and hardcoded
the PDA leg — the call was literally `Ess.Raw.Mark.pda(uGuid, "icon_yellow_mc")` — so every kind disagreed
with itself: a `destroy` objective drew a destroy icon in the world, a destroy icon on the radar, and
nothing you could see on the map, because [that texture draws no art at
all](#why-the-pda-blips-were-never-visible). `Ess.Mark.KINDS` now names all three for every
kind — it is the public, iterable vocabulary, so `Ess.Mark.KINDS.destroy.pda` is a legal answer to "what
icon does a destroy objective use on the map," and iterating it beats guessing what kinds exist.

| `kind` | Radar (`rdr`) | World (`wld`) | PDA (`pda`) |
|---|---|---|---|
| `action` | `objective_action` | `HUD_objective_action` | `icon_action_1_mc` |
| `destroy` | `objective_destroy` | `HUD_objective_destroy` | `icon_destroy_1_mc` |
| `defend` | `objective_defend` | `HUD_objective_defend` | `icon_defend_1_mc` |
| `verify` | `objective_verify` | `HUD_objective_verify` | `icon_verify_1_mc` |
| `deliverable` | `objective_deliverable` | `HUD_objective_deliverable` | `icon_deliverable_1_mc` |
| `outpost` | `objective_outpost` | `HUD_objective_outpost` | `icon_outpost_1_mc` |
| `generic` | `MiniMap_Icon_Symbol_Yellow` | `MiniMap_Icon_Symbol_Yellow` | `icon_action_1_mc` |

Every name above is confirmed present in the `mrxutil.lua` table for **its own** layer — the radar column
in `tObjRadarMaker`, the world column in `tObjWorldMarkers`, the PDA column in `tObjPdaMarker` — so none of
these kinds leaves a layer without a texture. Being in the table is a *naming* check, not a promise of art:
`icon_yellow_mc` is in `tObjPdaMarker` and still [draws nothing](#why-the-pda-blips-were-never-visible).
Two notes on the odd ones out:

- **`destination` is an alias for `deliverable`** — the same table, not a copy. It predates the three-layer
  rewrite and is `Ess.Mark.zone`'s default kind, so it stayed rather than being renamed, and it picked up
  the PDA leg for free.
- **`generic` is the one kind that is not a naming set.** `MiniMap_Icon_Symbol_Yellow` is in both the world
  and radar tables, so those two line up despite the naming. The PDA leg deliberately does *not* use
  `icon_yellow_mc`, its apparent counterpart, because [that name draws
  nothing](#why-the-pda-blips-were-never-visible) — pairing it here would make `generic` the one kind that
  silently vanishes on the map. It uses `icon_action_1_mc` instead.

Seven faction kinds line up the same way, named `faction_<code>`:

| `kind` | Radar (`rdr`) | World (`wld`) | PDA (`pda`) |
|---|---|---|---|
| `faction_gr` | `MiniMap_Icon_Faction_GR` | `HUD_faction_GR` | `icon_gr_mc` |
| `faction_oc` | `MiniMap_Icon_Faction_OC` | `HUD_faction_OC` | `icon_oc_mc` |
| `faction_pr` | `MiniMap_Icon_Faction_PR` | `HUD_faction_PR` | `icon_pr_mc` |
| `faction_an` | `MiniMap_Icon_Faction_AN` | `HUD_faction_AN` | `icon_an_mc` |
| `faction_ch` | `MiniMap_Icon_Faction_CH` | `HUD_faction_CH` | `icon_ch_mc` |
| `faction_pmc` | `MiniMap_Icon_Faction_PMC` | `HUD_HQ_PMC` | `icon_pmc_mc` |
| `faction_vz` | `MiniMap_Icon_Faction_VZ` | *(none)* | `icon_vz_mc` |

The world layer is the incomplete one, confirmed against `tObjWorldMarkers`: there is no `HUD_faction_PMC`
(PMC borrows its HQ icon) and no `HUD_faction_VZ` at all. Radar and PDA have all seven. `faction_vz`
therefore carries no world texture, and the world layer falls through to `Ess.Raw.Mark.world`'s own default
— `HUD_objective_action`, a plain objective icon, not a VZ one. It is the one kind that half-resolves, and
it does so on the world layer only.

### Color reaches two of the three layers

This asymmetry is the thing here most likely to be mistaken for a bug. `opts.rgb` tints the **radar** dot
(`Hud.Radar:AddObjective` takes `nR`/`nG`/`nB`) and the **world** icon and ring (`Marker.AddBlip`/`AddDisc`
take `r, g, b`), and arbitrary colors work on both — verified live 2026-07-26 with three markers identical
but for `rgb`, which rendered red, green and blue on the minimap and in the world.

**The PDA map has no color parameter at all.** `AddMapBlip` takes thirteen arguments and not one of them is
rgb, so those same three markers were visually identical on the map. A PDA blip's only color axis is which
texture you pick — which is exactly why the faction kinds matter: on the map, `faction_gr` *is* the color.

A `kind` is a default, not a straitjacket. `opts.radarIcon` / `opts.pdaIcon` / `opts.worldIcon` each
override one layer and leave the rest of the kind intact, so you can color the PDA leg on its own
(confirmed live: `kind = "destroy"` with `pdaIcon = "icon_gr_mc"` shows a destroy icon on the radar and in
the world, and the guerrilla icon on the map):

```lua
Ess.Mark.object(uGuid, { kind = "destroy", pdaIcon = "icon_gr_mc" })
```

An override is only honoured if it is a non-empty string; anything else falls back to the kind's own icon.

### The opts, in full — and a naming gotcha

`object()`'s opts default **opt-out** (radar/pda/world all `true`) matching the Contract Framework's
"mark everything" convention — pass `radar=true, pda=true, world=false` to match WaveDefense's convention
instead:

- `opts.radar` (default `true`), `opts.pda` (default `true`) — same as the raw calls.
- `opts.world` (default `true`) — **the floating in-world icon.**
- `opts.disc` (default `false`) — **a ground ring** around the object (`opts.radius` default `15`,
  `opts.discAlpha` its fill).
- `opts.kind` (default `"action"`) — picks all three icons at once, from
  [`Ess.Mark.KINDS`](#kinds-one-name-three-icons).
- `opts.radarIcon` / `opts.pdaIcon` / `opts.worldIcon` — override one layer's texture without disturbing
  the other two.
- `opts.label` — the PDA blip's label; defaults to the guid string.
- `opts.rgb` — tints the radar dot, the floating icon and the ring, but
  [not the PDA blip](#color-reaches-two-of-the-three-layers).
- `opts.size` / `opts.dist` — the floating icon's on-screen size and draw distance.

`zone()`'s opts:

- `opts.world` (default `true`) — **the ground ring** (`Marker.AddDisc`; `opts.discAlpha`, or `opts.alpha`,
  its fill).
- `opts.radar` / `opts.pda` (default `true` each) — the round-radar/PDA blip on the same anchor.
- `opts.icon` (default `false`) — **also** drops a floating in-world icon on the anchor.
- `opts.kind` (default `"destination"`) picks the icon set for all three layers — the radar blip, the PDA
  blip and the floating icon. `opts.radarIcon`/`pdaIcon`/`worldIcon`, `opts.label`, `opts.rgb` and
  `opts.size`/`opts.dist` behave exactly as on `object()`.

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

Kind `"action"` resolves on the PDA as well (`icon_action_1_mc`), so `enemy` and `objective` put a real icon
on the map and not just on the radar and in the world. Neither preset passes a label, so their blips are
labelled with the object's guid string — drop to `Ess.Mark.object` with `opts.label` if the blip should read
as something a player recognises.

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
