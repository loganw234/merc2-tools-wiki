---
title: WifHqData
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 3
inherits: none
tags: [data]
verified: false
---

# WifHqData

## Overview
`WifHqData` is the static per-HQ/outpost configuration table for every faction base in the game —
interior template, portal/entrance points, PDA and radar icon sets, atmosphere, landing zone, and parking
lot — plus three small getter/index functions. It's the data `resident/mrxhqmanager.lua`,
`resident/mrxhq.lua`, `resident/mrxbriefing.lua`, and `resident/mrxmissionflow.lua` all read from to
actually construct and display an HQ.

## Inheritance
- Inherits from: none — base data module.
- Imports: none.

## Instance pattern
Stateless data module. `_tHqConfigs` (26 entries) never changes at runtime — unlike most of this batch,
there's no `SaveSingleton`/`LoadSingleton` pair here and no mutable state at all.

## The `_tHqConfigs` schema
Most outposts share this shape:

```lua
AllOutpost1 = {
  tInterior = {sTemplate = "_aloutpost_interior_job"},
  tPortal = {
    sEntrance = "Starter_All1_Entrance",
    sStart1 = "Starter_All1_Start1",
    sStart2 = "Starter_All1_Start2"
  },
  vBuildingName = "AllOutpost1",
  sPdaIcon = "icon_an_mc",
  sPdaIconLocked = "icon_an_locked_mc",
  sPdaIconNew = "icon_green_mc",
  sRadarIcon = "MiniMap_Icon_Faction_AN",
  sRadarIconLocked = "MiniMap_Icon_Faction_AN_locked",
  sRadarIconNew = "MiniMap_Icon_Faction_AN",
  sAtmosphere = "small",
  nLandingZone = 7,
  sLzUnlockStyle = "visit",
  sParkingLot = "07_all_hq_parking"
},
```

A main faction HQ looks the same but adds `sBlipLabel` and uses `nAltLandingZone` instead of
`nLandingZone`:

```lua
AllHq = {
  tInterior = {sTemplate = "AllHq_Interior"},
  tPortal = {sEntrance = "Starter_All0_Entrance", sStart1 = "Starter_All0_Start1", sStart2 = "Starter_All0_Start2"},
  vBuildingName = "AllHq",
  sPdaIcon = "icon_an_HQ_mc",
  sPdaIconLocked = "icon_an_HQ_locked_mc",
  sPdaIconNew = "icon_green_mc",
  sRadarIcon = "MiniMap_Icon_Faction_AN",
  sRadarIconLocked = "MiniMap_Icon_Faction_AN_locked",
  sRadarIconNew = "MiniMap_Icon_Faction_AN",
  sBlipLabel = "[poi.alliedhq]",
  sAtmosphere = "all",
  nAltLandingZone = 7,
  sParkingLot = "07_all_hq_parking"
},
```

The two "recruit companion" HQs (`JetHq` for Misha, `MecHq` for Eva) use a smaller, distinct schema: no
landing-zone fields at all, `sWorldIcon` instead, and — on `JetHq` specifically — `sPdaIconLocked` set to
the exact same texture as `sPdaIcon`, unlike every faction HQ/outpost where the locked variant is visually
distinct:

```lua
JetHq = {
  tInterior = {sTemplate = "_proutpost_interior_job"},
  tPortal = {sEntrance = "Starter_Jet_Entrance", sStart1 = "Starter_Jet_Start1", sStart2 = "Starter_Jet_Start2"},
  vBuildingName = "_village_bld_housestilts01 0x000f6257",
  sPdaIcon = "icon_misha_mc",
  sPdaIconLocked = "icon_misha_mc",
  sRadarIcon = "MiniMap_Icon_Misha",
  sWorldIcon = "HUD_PMC_Misha",
  sBlipLabel = "[Generic.HQ.JetHq]",
  sAtmosphere = "pir",
  sParkingLot = "08_pir_jet_parking"
},
```

Field notes:
- `vBuildingName` is usually a single string but is an **array** of 3 strings on `OilTalkbox`
  (`"intercom_dynamic"` plus two wall pieces) — whatever reads this field has to handle both shapes.
- `sLzUnlockStyle` is `"visit"` (main HQs/first outposts — must be physically reached once) or `"auto"`
  (later outposts — unlocks from story progression instead), on the entries that have a landing zone at
  all.
- One-off overrides layered onto the shared schema: `bWatchBuildingHealth = true` appears only on
  `ChiHq`; `nRotation = 180` only on `GurHq`; `nDrawDistance = 500` only on `OilTalkbox`.

## Functions
### `GetHqConfigFromId(sHqName)`
Plain `_tHqConfigs[sHqName]` lookup.

### `GetHqIndexFromId(sHqName)` / `GetHqIdFromIndex(nIndex)`
Same `pairs()`-iteration-order index scheme as [`WifMissionData`](wifmissiondata)'s mission-index
getters — see that page's gotcha on fragility; it applies here too, since the "index" isn't an authored
field, just position in one particular `pairs()` walk of `_tHqConfigs`.

## Events
None.

## Notes for modders
- **Decompiler/data note:** `OilTalkbox` sets `sAtmosphere` twice in its literal (`"small"`, then later
  `"oiljob"`) — Lua's last-key-wins rule means the effective value at runtime is `"oiljob"`; the first
  `"small"` is silently discarded, not merged.
- Read by `resident/mrxhqmanager.lua` (loads an HQ's config by name to build the runtime HQ object),
  `resident/mrxhq.lua` (portal blip add/remove, both by name and by the `pairs()`-order index),
  `resident/mrxbriefing.lua` (atmosphere lookup for a mission's starter HQ), and
  `resident/mrxmissionflow.lua` (portal entrance/start lookup). None of them write back to this table —
  it's read-only in practice even though nothing here enforces that.
- Same index-fragility gotcha as [`WifMissionData`](wifmissiondata): don't rely on
  `GetHqIndexFromId`/`GetHqIdFromIndex` returning stable numbers across a modified `_tHqConfigs`.
