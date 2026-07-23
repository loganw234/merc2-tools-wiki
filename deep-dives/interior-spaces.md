---
title: "Getting Into Interior Spaces"
parent: Deep Dives
nav_order: 17
---

# Deep Dive: Getting Into Interior Spaces

> **Status: confirmed working live (2026-07-23).** The PMC HQ mansion's enter/exit, all six faction
> landing-zone bases, and — the new find this pass turned up — all five factions' separate walkable HQ
> *offices* are all confirmed enterable with real, live-tested coordinates. The one real trap
> (`MrxUtil.SpawnActor` being asynchronous) is documented with the fix. Still open: exact briefing-room
> coordinates, and whether the smaller captured-outpost `interior_job` templates spawn the same way the HQ
> offices do.

## Three kinds of "interior" — easy to conflate, worth keeping separate

"Interior" turns out to mean three genuinely different things in this engine, and mixing them up is the
easiest way to waste time chasing the wrong mechanism:

1. **The PMC HQ mansion** — a true separate-region walkable interior: its own streamed layer
   (`Vz_State_PmcInterior`), living at an isolated, high, off-in-its-own-space coordinate,
   **(3794, 450, −3823)**. One dedicated native call gets you in and out.
2. **Faction HQ *bases*** (Allied/Oil/Guerrilla/Pirate/China) — **not separate interiors at all.** These are
   ordinary open-world military bases at their landing-zone coordinates — e.g. the Allied LZ streams in 93
   buildings and 59 props as normal world content. You reach them the same way you'd reach anywhere else on
   the map: teleport or fast-travel. No interior-mode flip needed beyond what any location gets.
3. **Faction HQ *offices*** — the newest find here. Each faction *also* has its own small, walkable HQ
   office interior (where its contract-giver/cutscene character actually lives) — and unlike (2), this one
   really is a separate region. It isn't a pre-existing streamed layer at all: it's a worldentity **template**
   (`AllHq_Interior` / `ChiHq_Interior` / `GurHq_Interior` / `OilHq_Interior`, per `wifhqdata.lua`'s
   `tInterior.sTemplate`) that gets *spawned on demand* onto one shared hidden coordinate island —
   **(3750, 450, −3840)**, right next door to the PMC mansion's own isolated spot. Because it's a live spawn
   rather than a layer stream, it comes with its own gotcha (below), and because every faction's office
   spawns onto the exact same slot, only one can exist at a time.

Categories (1) and (2) were already reachable by primitives the decompiled corpus itself uses all the time.
Category (3) is the new discovery this pass made, confirmed live on 2026-07-23.

## How an interior actually loads

Traced through the resident + `vz` scripts, the general mechanism behind category (1) and the streamed half
of category (2) is:

1. **Stream the layer(s)** — `MrxLayerManager.Add({"Vz_State_PmcInterior", ...}, onLoaded, nil, nil, nil, true)`
   (an async request queue; the trailing `true` is high priority). Interior geometry and props are type-6
   `layer` container assets living in `vz_state_*`/`layers_static` blocks.
2. **Flip interior mode** — `WifVzBoundary.SetInteriorMode(true)` plus `MrxHq.GlobalEnter(true)`: HUDs off,
   hero invincible, faction-reporting disabled, and the game switches to the `rgn_atmo_interior` atmosphere.
3. **Wait for the stream** — `MrxState.Enter(MrxState.STATE_WAITFORGAME, complete, ...)`.
4. **Place the player** — `MrxUtil.TeleportHeroesToLocations({loc1, loc2})`, where each `loc` is either a
   **marker name** (a string, resolved via `Pg.GetGuidByName` then `Object.GetPosition`/`GetYaw`) or a raw
   **`{x, y, z, yaw}`** table (`mrxutil.lua:142`).
5. **Exit** reverses it: `SetInteriorMode(false)`, `MrxHq.GlobalExit()`, unload the layers.

Category (3) — the spawned faction offices — swaps step 1 for a live `MrxUtil.SpawnActor` call instead of a
layer stream; see the gotcha section below for why that distinction matters in practice.

### Two naming levels, and why it matters which one you're using

- **Block/layer names** — what `MrxLayerManager.Add` actually loads, case-insensitive to the underlying
  block path: `Vz_State_PmcInterior`, `staging_oil_hq`, and so on.
- **Placement/marker names** — teleport targets, resolved by `Pg.GetGuidByName` *after* the layer has
  loaded: `PmcInterior_A1`, `01_pmc_hq_lz_playerone`, `HqInterior`. These are entities inside the
  `layers_static` placement data, not WAD block paths — you cannot `MrxLayerManager.Add` a marker name, and
  you cannot `Pg.GetGuidByName` a block name.

## Entry primitives

All of these are live-callable over the bridge or from an OnKey script:

| Call | What it does |
|---|---|
| `WifPmcInterior.Enter(true, nPortal)` | One-call entry to the PMC HQ interior. `nPortal` 1–4 (portals A/B/C/D → the same MainHall). Streams `Vz_State_PmcInterior`, sets interior mode, teleports heroes to `PmcInterior_<P>1`/`2`. |
| `_G.DebugTeleport(x, y, z)` | The cheat-bootstrap global — teleports all heroes to raw coordinates. The universal mover, usable for any of the three categories once you have real coordinates. |
| `Pg.GetAllLandingZones(1)` / `(2)` | Native — returns every transit destination for player 1/2, including the 6 faction-HQ landing zones. Source of `MrxTransit._tLandingZones`. |
| `MrxTransit.UnlockAllLandingZones()` | Cheat — unlocks every landing zone so you can fast-travel anywhere. |
| `MrxTransit.Transit(nLocation)` | Fast-travel (loading-screen warp) to landing-zone `nLocation`. `GetTransitPoint(n)` returns its coordinates. |
| `MrxLayerManager.Add(tLayers, cb, ...)` | Streams any layer list in; `cb` fires once loaded. |
| `MrxUtil.TeleportHeroesToLocations({marker \| {x,y,z,yaw}})` | Places heroes at a marker or raw coordinates. |
| `MrxUtil.TeleportHeroesToHardpoints({ {vObject=uGuid, sHardpoint=sName} })` | Places heroes at a named hardpoint on a specific object — how the spawned faction offices seat you correctly. |
| `MrxUtil.SpawnActor(sTemplate, sName, {x,y,z}, ..., fnCallback)` | Spawns a worldentity template and fires `fnCallback` once it's actually ready. **Asynchronous** — see the gotcha below. |
| `WifVzBoundary.SetInteriorMode(b)` | Interior render/boundary mode toggle. |

## Get-in recipes, one per category

**Category 1 — PMC HQ (trivial):**
```lua
WifPmcInterior.Enter(true, 1)   -- any of portals 1..4 land in MainHall
```

**Category 2 — a faction HQ base, via its landing zone:**
The six HQ landing-zone objects are `01_pmc_hq_lz_playerone`, `02_oil_hq_lz_playerone`,
`05_gur_hq_lz_playerone`, `07_all_hq_lz_playerone`, `08_pir_hq_lz_playerone`, `12_chi_hq_lz_playerone`.
Unlock and transit, or resolve the object directly and warp onto it:
```lua
local g = Pg.GetGuidByName("02_oil_hq_lz_playerone")
local x, y, z = Object.GetPosition(g)
DebugTeleport(x, y, z)
```

**Category 3 — a faction HQ office, spawned on demand:**
{% raw %}
```lua
_MODULES.mrxhq.GlobalEnter(false)
MrxUtil.SpawnActor("OilHq_Interior", "HqInterior", {3750, 450, -3840}, nil, 0, false, false, function()
  Graphics.Atmosphere.ChangeLineRegionSetting(Pg.GetGuidByName("rgn_atmo_interior"), "oil")
  MrxUtil.TeleportHeroesToHardpoints({{ vObject = Pg.GetGuidByName("HqInterior"), sHardpoint = "hp_playerA_enter" }})
end)
-- exit: _MODULES.mrxhq.GlobalExit() then DebugTeleport(x, y, z)
```
{% endraw %}
Swap `"OilHq_Interior"` for `"AllHq_Interior"`/`"ChiHq_Interior"`/`"GurHq_Interior"` for the other three; the
PMC office uses category 1's own dedicated call instead, not this generic path.

**Any interior layer, generically:**
```lua
MrxLayerManager.Add({"Vz_State_ChicOn002_Hq_Pristine"}, function()
  WifVzBoundary.SetInteriorMode(true)
  DebugTeleport(x, y, z)   -- see the contents reference below for known coordinates
end, nil, nil, nil, true)
```

## The gotcha: `SpawnActor` is asynchronous

This is the one real trap in category 3, and it's easy to hit without realizing why. `MrxUtil.SpawnActor`
returns before the spawned object's collision has actually finished streaming in. Teleport immediately
inside the naive version of its own callback and you land where the floor isn't there yet —
**confirmed live**: the player fell from the intended y≈451 down through y≈340 and kept going.

The reliable pattern is to **not** teleport inside the raw spawn callback at all: spawn without teleporting,
poll `Pg.GetGuidByName("HqInterior")` until it resolves to a valid guid (roughly another 1.5s beyond the
spawn callback firing, for collision to catch up), and only then call `TeleportHeroesToHardpoints`. Done
this way, all five faction offices were confirmed enterable, landing at y≈451 every time:

| Office | Confirmed landing coordinates |
|---|---|
| PMC | (3794, 450, −3823) |
| Oil | (3737, 450, −3826) |
| Guerrilla | (3754, 451, −3838) |
| Allied | (3750, 451, −3827) |
| China | (3750, 451, −3838) |

All five spawn onto the exact same slot, `{3750, 450, -3840}` — they're mutually exclusive. Despawn the
previous office's `HqInterior` actor (`Object.Remove`) before spawning the next one, or you'll end up with
two actors contesting the same space. The [snippet below](../snippets#warp-into-any-hq-interior-and-back-out)
packages this whole poll-then-teleport pattern as two reusable functions.

## Live-confirmed coordinates, all of it

**PMC HQ interior** — enter via `_MODULES.wifpmcinterior.Enter(true, 1)` (not a bare global — reach it via
`_MODULES.wifpmcinterior`/`_MODULES.mrxhq`, same as the faction offices), landing around **(3794, 450, −3823)**.
Confirmed markers once inside: `PmcInterior_A1` (3794, 450, −3823.4), `A2`, `B1` (3794, 450.8, −3911),
`MainHallToGarage1` (3768, 450, −3851.6). Exit reliably with
`_MODULES.mrxhq.GlobalExit(); WifVzBoundary.SetInteriorMode(false); DebugTeleport(2551, -14, -911)` — calling
the interior's own `Exit()` was found to stall, so this sequence is the confirmed-working alternative.

**Faction HQ bases** (landing-zone coordinates, from `Pg.GetAllLandingZones(1)`, 30 zones total, resolved by
name via `Pg.GetGuidByName`+`Object.GetPosition`): PMC (2632, 8, −887) · Oil (2515, −30, 1463) ·
Guerrilla (1583, 162, −2451) · Allied (261, −34, 225) · Pirate (2082, −28, 2619) · China (−2316, 16, 1081).

**Faction HQ offices** — see the table above.

## Interior contents reference

Companion to the mechanism above: what's actually *in* each interior layer, decoded from `vz.wad` directly
rather than from live testing. Method: `mercs2_smuggler --dump-block <idx>` against each type-6 `layer`
block (UCFX ECS: `COMP`/`info`/`schm`/`data`), then a raw string scan for spawn markers and placed entity
names. **Read the confidence level here honestly** — this is a byte-level string scan, not a decoded ECS
transform component, so exact per-entity coordinates aren't available this way (a live
`Object.GetPosition` on a resolved marker, once the layer is loaded, is the accurate source for that); some
`contents` entries below carry a few junk leading bytes picked up by the scan (e.g. a stray `$f`/`>(Oo`
prefix) rather than a clean asset name — kept as-is rather than silently cleaned up, since guessing at the
"real" name would be worse than showing the raw extraction.

This table covers **layer-block interiors only** — categories 1 and 2 above, plus the outpost/briefing/ruin
blocks below. The category-3 faction offices (`AllHq_Interior` etc.) aren't layer blocks at all — they're
worldentity templates, so they don't show up in a block dump; see the live-tested recipe above instead.

**Inventory, ~36 true cells total** (full list in `vz_wad_layer_list.txt`):
- **PMC HQ interior** (6 blocks) — `Vz_State_PmcInterior` plus state variants `_hel`/`_jet`/`_mec`/
  `_mecabsent` (helicopter/jet/mechanic present or absent), plus `pmc_interior`.
- **Faction HQ shells** (10 blocks) — `all_hq_structures`, `chi_hq_structures`, `gurhq_act1`,
  `staging_{all,chi,oil,pir}_hq`, `chicon002_hq_{pristine,hostiles,destroyed}`.
- **Outpost buildings** (5 blocks) — `pmcoutpost_bld_{hq,hqsuites,pool,dock,fueldepot}`.
- **Briefing rooms** (13 blocks) — `scaleform_{allcon,chicon,gurcon,jetcon,meccon,pmccon}...briefing`.
- **Reusable ruin interiors** (2 blocks) — `resident2-global_ruin_interior04`/`_08`.

**Per-block detail** (marker counts are spawn/teleport marker names found in that block; contents are a
sample of placed entities/props, not necessarily exhaustive):

| Interior | Block (size) | Spawn/teleport markers | Notable contents |
|---|---|---|---|
| PMC HQ interior | 667 (19647 B) | 28 — `EXIT`, `Exiting`, `HqInterior`, `MovementPortal`, `PmcInterior_A1`/`A2`/`A_Exit`, `_B1`/`B2`/`B_Exit`, `_C1`/`C2`/`C_Exit`, `_D1`/`D2`/`D_Exit`, `_F1`/`F2`, `_GarageToMainHall1`/`2` | 128 entries incl. `PmcInterior_StarterFiona_BriefingLoc(+_Hero1)`, `Sickbay Hero Respawn 1`/`2`, vehicles/props/foliage — see raw dump for the full, partly string-scan-garbled list |
| Allied HQ (structures) | 253 (25318 B) | 3 — `EXIT`, `Exiting`, `MovementPortal` | 68 entries — outpost buildings (`_aloutpost_bld_barracks02`, `_guardtowershort`, `_helipad`, `_largetent`), props, `bldg_bunker`/`glass`/`metal` |
| Allied HQ (staging) | 152 (17738 B) | 17 — incl. multiple `PathSpawner_AlliedHQ_*` (hill01-04, out01-04, prision02, tent02) + `PopulationSimpleSpawner` | 64 entries — same prop/building family, plus `hum_hero_chris`/`hum_hero_jen` |
| China HQ (structures) | 553 (12123 B) | 3 — `EXIT`, `Exiting`, `MovementPortal` | 64 entries |
| China HQ (captured/pristine) | 394 (12219 B) | 3 — `EXIT`, `Exiting`, `MovementPortal` | 65 entries incl. `_ocoutpost_bld_hq` |
| China HQ (staging) | 497 (19868 B) | 19 — incl. `PathSpawner_ChiHQ_PedList_*` (camp01/02, dock01-03, fortwalk01-04, hangar01-04, mechanic, tents) + `PopulationSimpleSpawner` | 65 entries incl. `_chinaoutpost_bld_helipad` |
| Guerrilla HQ (act1) | 317 (18480 B) | 8 — incl. `PathSpawner_GurHQ_PedList`/`VehList` + `PopulationSimpleSpawner` | 64 entries |
| Oil HQ (staging) | 742 (14423 B) | 4 — `EXIT`, `Exiting`, `MovementPortal`, `PopulationSimpleSpawner` | 64 entries |
| Pirate HQ (staging) | 225 (34738 B) | 8 — incl. `PathSpawner_Boat_PirateIsles_Act1_A` (×4) + `PopulationSimpleSpawner` | 64 entries |
| PMC outpost — HQ suites | 3484 (616746 B) | 0 — none found | 2 entries: `pmcoutpost_bld_hqsuites_{pristine,ruin}_lod` |
| Ruin interior 04 | 8196 (49284 B) | 0 — none found | 0 — none |
| Ruin interior 08 | 8256 (65732 B) | 0 — none found | 0 — none |

## Still open

- **Exact briefing-room coordinates.** The 13 `scaleform_*briefing` blocks are confirmed to exist as
  entities in the inventory above, but none of their placement coordinates have been captured yet — these
  are Scaleform cutscene contexts (see the `## Get-in recipes` generic-layer recipe as the starting point
  for testing one directly), not walkable spaces in the same sense as the other two categories.
- **Whether outpost `interior_job` templates spawn the same way the HQ offices do.** Smaller
  captured-outpost interiors use `_<faction>outpost_interior_job` templates (`al`/`china`/`gr`/`oc`/`pr`
  variants) — structurally similar to the category-3 discovery above (a template rather than a layer
  block), but not yet confirmed to use the same `SpawnActor`-plus-poll pattern. The OC office's own cutscene
  actor (`oc001_exec` / `characternameanimgroup_ochqexecphone`) is confirmed as the entity living inside
  that specific office once entered — a useful landmark if you're testing that office specifically.

## See also

- [Snippets: warp into any HQ interior and back out](../snippets#warp-into-any-hq-interior-and-back-out) —
  the packaged `GoInside`/`GoOutside` utility built on the category-3 recipe above.
- [Player](../namespaces/player) — the boundary functions (`AddBoundary`/`RemoveAllBoundary`) relevant to
  leaving the open world in the first place, if boundaries are blocking the route to a landing zone.
- [MrxLayerManager](../resident/mrxlayermanager) — the boot-time layer manifest and general layer-loading
  machinery `MrxLayerManager.Add` is part of.
