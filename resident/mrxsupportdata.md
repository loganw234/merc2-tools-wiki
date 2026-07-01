---
title: MrxSupportData
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, supply, delivery, data-reference]
---

# MrxSupportData

*Module: mrxsupportdata.lua*

## Overview

`MrxSupportData` owns the catalog of every purchasable support item in the game — supply drops,
vehicles, and airstrikes — plus per-faction unlock/freebie/recruit-requirement tracking. The catalog
itself (`tSupportData`) is what [`MrxCheatBootstrap`](mrxcheatbootstrap)'s "Add support" dialog and
"The Works!" both iterate over.

## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxUtil`, `MrxPmc`, and the individual support-delivery modules (`mrxcratedelivery`,
  `mrxartillery`, `mrxsupportcopterdelivery`, etc.) referenced while building each catalog entry.

## Instance pattern

Stateless manager module — no `Create`/`uGuid` pattern. Module-level tables hold shared, global state
instead of per-object instances:

- `tSupportData` — the full support-item catalog (see below). Starts as an **empty table literal** in
  source and is populated by dozens of individual `tSupportData.<key> = {...}` assignments and
  `AddSupportData(...)` calls scattered through the file — there's no single place in source that shows
  the finished catalog, which is why the table below was captured by dumping it live in-game instead of
  reading source.
- `tFreebieData` — tracks mission-granted free uses of support items.
- `tRequirementsObtained` / `tRequirementStrings` — recruit-requirement state and their display strings.
- `_kMaxStock` — the max-stock constant, `99` (matches every entry in the catalog below).

## Support item catalog

**Captured by live runtime dump**, not read from source — see [Recipes](../recipes) for the `DumpTable`
tool this was captured with. 134 items across 7 types. "Loc key" is the untranslated localization string
key (e.g. `[vehicle.ah1z]`) `sName` actually holds — this wiki doesn't have the string-table lookup, so
these are shown as-is rather than resolved to display text; most are still readable enough to identify
the item. Every entry has `nMaxStock = 99`, so that column is omitted from context below where obvious.

Each type's items are sorted by cash cost, cheapest first.

### Supply (21 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `Support` | `[support.supply.Support.name]` | 5,000 | 40 | 99 |
| `blanco` | `[support.supply.blanco.name]` | 5,000 | 40 | 99 |
| `cqb` | `[support.supply.cqb.name]` | 5,000 | 40 | 99 |
| `fiona` | `[support.supply.fiona.name]` | 5,000 | 40 | 99 |
| `gr` | `[support.supply.gr.name]` | 5,000 | 40 | 99 |
| `lightmg` | `[support.supply.lightmg.name]` | 5,000 | 40 | 99 |
| `oc` | `[support.supply.oc.name]` | 5,000 | 40 | 99 |
| `pr` | `[support.supply.pr.name]` | 5,000 | 40 | 99 |
| `al` | `[support.supply.al.name]` | 10,000 | 40 | 99 |
| `c4` | `[support.supply.c4.name]` | 10,000 | 40 | 99 |
| `ch` | `[support.supply.ch.name]` | 10,000 | 40 | 99 |
| `covert` | `[support.supply.covert.name]` | 10,000 | 40 | 99 |
| `gl` | `[support.supply.gl.name]` | 10,000 | 40 | 99 |
| `rpg` | `[support.supply.rpg.name]` | 10,000 | 40 | 99 |
| `sniperch` | `[support.supply.sniperch.name]` | 10,000 | 40 | 99 |
| `sniperru` | `[support.supply.sniperru.name]` | 10,000 | 40 | 99 |
| `aa` | `[support.supply.aa.name]` | 15,000 | 40 | 99 |
| `amal` | `[support.supply.amal.name]` | 15,000 | 40 | 99 |
| `amch` | `[support.supply.amch.name]` | 15,000 | 40 | 99 |
| `atal` | `[support.supply.atal.name]` | 15,000 | 40 | 99 |
| `atch` | `[support.supply.atch.name]` | 15,000 | 40 | 99 |

### Airstrike (20 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `bombingrun` | `[support.airstrike.bombingrun.name]` | 75,000 | 140 | 99 |
| `clusterbomb` | `[support.airstrike.clusterbomb.name]` | 75,000 | 220 | 99 |
| `tankbuster` | `[support.airstrike.tankbuster.name]` | 100,000 | 200 | 99 |
| `artillery` | `[support.airstrike.artillery.name]` | 150,000 | 140 | 99 |
| `combatairpatrol` | `[support.airstrike.combatairpatrol.name]` | 150,000 | 280 | 99 |
| `bunkerbuster` | `[support.airstrike.bunkerbuster.name]` | 200,000 | 300 | 99 |
| `fuelairbomb` | `[support.airstrike.fuelairbomb.name]` | 200,000 | 900 | 99 |
| `laserguidedbomb` | `[support.airstrike.laserguidedbomb.name]` | 200,000 | 460 | 99 |
| `carpetbomb` | `[support.airstrike.carpetbomb.name]` | 250,000 | 280 | 99 |
| `daisycutter` | `[support.airstrike.daisycutter.name]` | 250,000 | 300 | 99 |
| `smartbomb` | `[support.airstrike.smartbomb.name]` | 300,000 | 200 | 99 |
| `rocketartillery` | `[support.airstrike.rocketartillery.name]` | 350,000 | 280 | 99 |
| `surgicalstrike` | `[support.airstrike.surgicalstrike.name]` | 350,000 | 280 | 99 |
| `uptankbuster` | `[support.airstrike.uptankbuster.name]` | 350,000 | 180 | 99 |
| `cruisemissile` | `[support.airstrike.cruisemissile.name]` | 400,000 | 160 | 99 |
| `strategicmissile` | `[support.airstrike.strategicmissile.name]` | 400,000 | 220 | 99 |
| `upcombatairpatrol` | `[support.airstrike.upcap.name]` | 400,000 | 200 | 99 |
| `moab` | `[support.airstrike.moab.name]` | 500,000 | 400 | 99 |
| `upclusterbomb` | `[support.airstrike.upclusterbomb.name]` | 500,000 | 180 | 99 |
| `nuke` | `[AllCon003.Terms.Reward]` | 1,000,000 | 500 | 99 |

### Heli (21 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `ka29b` | `[vehicle.ka29b]` | 40,000 | 160 | 99 |
| `uh1transportgr` | `[vehicle.uh1transportgr]` | 40,000 | 80 | 99 |
| `endriagoattack` | `[vehicle.endriagoattack]` | 45,000 | 140 | 99 |
| `alouette3transportpr` | `[vehicle.alouette3transportpr]` | 50,000 | 100 | 99 |
| `alouette3transportvz` | `[vehicle.alouette3transportvz]` | 50,000 | 100 | 99 |
| `coandatransport` | `[vehicle.coandatransport]` | 50,000 | 60 | 99 |
| `mh53j` | `[vehicle.mh53j]` | 50,000 | 140 | 99 |
| `mi26ch` | `[vehicle.mi26ch]` | 50,000 | 140 | 99 |
| `mi26vz` | `[vehicle.mi26vz]` | 50,000 | 140 | 99 |
| `endriagoelite` | `[vehicle.endriagoelite]` | 60,000 | 140 | 99 |
| `alouette3attackpr` | `[vehicle.alouette3attackpr]` | 75,000 | 140 | 99 |
| `alouette3attackvz` | `[vehicle.alouette3attackvz]` | 75,000 | 140 | 99 |
| `coandaattack` | `[vehicle.coandaattack]` | 75,000 | 100 | 99 |
| `coandasuperiority` | `[vehicle.coandasuperiority]` | 75,000 | 100 | 99 |
| `endriagosuperiority` | `[vehicle.endriagosuperiority]` | 75,000 | 140 | 99 |
| `alouette3elite` | `[vehicle.alouette3elite]` | 100,000 | 140 | 99 |
| `coandagunship` | `[vehicle.coandagunship]` | 100,000 | 100 | 99 |
| `alouette3superiority` | `[vehicle.alouette3superiority]` | 125,000 | 140 | 99 |
| `ah1z` | `[vehicle.ah1z]` | 200,000 | 180 | 99 |
| `mi35` | `[vehicle.mi35]` | 250,000 | 200 | 99 |
| `wz10` | `[vehicle.wz10]` | 350,000 | 200 | 99 |

### Light (30 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `m15150calgr` | `[vehicle.m15150calgr]` | 15,000 | 60 | 99 |
| `m15150calvz` | `[vehicle.m15150calvz]` | 15,000 | 60 | 99 |
| `m35guntruckgr` | `[vehicle.m35guntruckgr]` | 15,000 | 60 | 99 |
| `ext` | `[vehicle.ext]` | 20,000 | 60 | 99 |
| `extgl` | `[vehicle.extgl]` | 20,000 | 60 | 99 |
| `guntruckoc` | `[vehicle.guntruckoc]` | 20,000 | 100 | 99 |
| `hmmwvarmored50cal` | `[vehicle.hmmwvarmored50cal]` | 20,000 | 120 | 99 |
| `laviii50cal` | `[vehicle.laviii50cal]` | 20,000 | 140 | 99 |
| `m35guntruckvz` | `[vehicle.m35guntruckvz]` | 20,000 | 60 | 99 |
| `t300m60` | `[vehicle.t300m60]` | 20,000 | 60 | 99 |
| `buggypr` | `[vehicle.buggypr]` | 25,000 | 60 | 99 |
| `hmmwvarmoredgl` | `[vehicle.hmmwvarmoredgl]` | 25,000 | 120 | 99 |
| `laviii25mm` | `[vehicle.laviii25mm]` | 25,000 | 140 | 99 |
| `m35aagr` | `[vehicle.m35aagr]` | 25,000 | 80 | 99 |
| `laviiiad` | `[vehicle.laviiiad]` | 30,000 | 140 | 99 |
| `laviiiat` | `[vehicle.laviiiat]` | 30,000 | 140 | 99 |
| `laviiimewss` | `[vehicle.laviiimewss]` | 30,000 | 140 | 99 |
| `m35aavz` | `[vehicle.m35aavz]` | 30,000 | 80 | 99 |
| `hmmwvarmoredtow` | `[vehicle.hmmwvarmoredtow]` | 35,000 | 120 | 99 |
| `nglv50cal` | `[vehicle.nglv50cal]` | 35,000 | 80 | 99 |
| `laviiimgs` | `[vehicle.laviiimgs]` | 40,000 | 160 | 99 |
| `hmmwvavenger` | `[vehicle.hmmwvavenger]` | 45,000 | 120 | 99 |
| `nglvgl` | `[vehicle.nglvgl]` | 45,000 | 80 | 99 |
| `sidecarmotorcycle` | `[vehicle.sidecarmotorcycle]` | 50,000 | 40 | 99 |
| `sx2150mlrs` | `[vehicle.sx2150mlrs]` | 60,000 | 120 | 99 |
| `buggyhellfire` | `[vehicle.buggyhellfire]` | 150,000 | 60 | 99 |
| `dsvscoutvehicle` | `[vehicle.dsvscoutvehicle]` | 150,000 | 60 | 99 |
| `panhardassault` | `[vehicle.panhardassault]` | 400,000 | 60 | 99 |
| `tankbike` | `[vehicle.tankbike]` | 750,000 | 60 | 99 |
| `veyronassault` | `[vehicle.veyronassault]` | 1,000,000 | 60 | 99 |

### Heavy (20 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `m113gr` | `[vehicle.m113gr]` | 30,000 | 100 | 99 |
| `m113aagr` | `[vehicle.m113aagr]` | 35,000 | 100 | 99 |
| `m113vz` | `[vehicle.m113vz]` | 35,000 | 100 | 99 |
| `m113aavz` | `[vehicle.m113aavz]` | 40,000 | 100 | 99 |
| `m113jammervz` | `[vehicle.m113jammervz]` | 40,000 | 100 | 99 |
| `m551` | `[vehicle.m551]` | 45,000 | 140 | 99 |
| `stingrayii` | `[vehicle.stingrayii]` | 50,000 | 140 | 99 |
| `wz551` | `[vehicle.wz551]` | 70,000 | 160 | 99 |
| `scorpion90` | `[vehicle.scorpion90]` | 75,000 | 140 | 99 |
| `zbd2000` | `[vehicle.zbd2000]` | 85,000 | 160 | 99 |
| `amx30` | `[vehicle.amx30]` | 100,000 | 160 | 99 |
| `plz45` | `[vehicle.plz45]` | 100,000 | 160 | 99 |
| `ztz63a` | `[vehicle.ztz63a]` | 100,000 | 180 | 99 |
| `amx30aa` | `[vehicle.amx30aa]` | 125,000 | 160 | 99 |
| `amx30elite` | `[vehicle.amx30elite]` | 150,000 | 160 | 99 |
| `m2a3` | `[vehicle.m2a3]` | 150,000 | 160 | 99 |
| `pgz95` | `[vehicle.pgz95]` | 150,000 | 160 | 99 |
| `pgz95command` | `[vehicle.pgz95command]` | 165,000 | 160 | 99 |
| `m1a2` | `[vehicle.m1a2]` | 425,000 | 240 | 99 |
| `ztz98` | `[vehicle.ztz98]` | 425,000 | 220 | 99 |

### Boat (9 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `jetskiciv` | `[vehicle.jetskiciv]` | 5,000 | 40 | 99 |
| `turbosquidgr` | `[vehicle.turbosquidgr]` | 5,000 | 40 | 99 |
| `turbosquidoc` | `[vehicle.turbosquidoc]` | 5,000 | 40 | 99 |
| `speedboat` | `[vehicle.speedboat]` | 10,000 | 60 | 99 |
| `dinghy` | `[vehicle.dinghy]` | 15,000 | 60 | 99 |
| `omen` | `[vehicle.omen]` | 25,000 | 60 | 99 |
| `piranha` | `[vehicle.piranha]` | 45,000 | 60 | 99 |
| `patrolboatvz` | `[vehicle.patrolboatvz]` | 75,000 | 80 | 99 |
| `patrolboatpmc` | `[vehicle.patrolboatpmc]` | 500,000 | 60 | 99 |

### Civilian (13 items)

| Key | Loc key | Cash | Fuel | Max stock |
|---|---|---:|---:|---:|
| `junkers` | `[vehicle.junkers]` | 5,000 | 60 | 99 |
| `bike` | `[vehicle.bike]` | 10,000 | 60 | 99 |
| `m151softtopgr` | `[vehicle.m151softtopgr]` | 10,000 | 60 | 99 |
| `m151softtopvz` | `[vehicle.m151softtopvz]` | 10,000 | 60 | 99 |
| `civilian` | `[vehicle.civilian]` | 15,000 | 60 | 99 |
| `hmmwvsofttop` | `[vehicle.hmmwvsofttop]` | 15,000 | 120 | 99 |
| `monster` | `[vehicle.monster]` | 20,000 | 60 | 99 |
| `sports` | `[vehicle.sports]` | 20,000 | 60 | 99 |
| `utility` | `[vehicle.utility]` | 20,000 | 60 | 99 |
| `luxury` | `[vehicle.luxury]` | 25,000 | 60 | 99 |
| `mattiaschopper` | `[vehicle.mattiaschopper]` | 25,000 | 40 | 99 |
| `monstertruck` | `[vehicle.monstertruck]` | 40,000 | 60 | 99 |
| `valiantpython` | `[vehicle.valiantpython]` | 50,000 | 60 | 99 |

## Overriding catalog values from your own mod

Since `tSupportData` is just a plain Lua table, changing an entry's price, fuel cost, or stock cap from
your own script is as simple as it sounds:

```lua
import("MrxSupportData")
MrxSupportData.tSupportData.moab.nCashCost = 1        -- MOAB airstrike now costs $1
MrxSupportData.tSupportData.tankbike.nMaxStock = 999   -- stock cap raised from 99 to 999
```

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

`MrxSupportData.tSupportData.moab` is a table (one catalog entry), and `.nCashCost` is one of its
fields — so `MrxSupportData.tSupportData.moab.nCashCost = 1` is just "reach into this table, then that
table, then set this field," the same `.` chaining you've seen everywhere else in this wiki. Nothing
about *modifying* a table is different from *reading* one — if you can write `d.nCashCost` to read a
value (as the catalog-dump script above does), you can write `d.nCashCost = 1` to change it.

</details>

**Timing matters here, and this is unconfirmed — worth testing if you try it:** `tSupportData` starts
empty and gets built up by `mrxsupportdata.lua`'s own module-level code, which (like all `resident/`
module-level code) runs once, the first time something imports that module. If your override script runs
*before* that population happens, your change would get silently clobbered the moment
`MrxSupportData`'s own init code assigns over that same key afterward. An `OnLoad` script is the safer
bet — by the time a level has fully loaded, essentially everything has already been imported at least
once by the game's own systems — whereas `OnBoot` runs so early there's a real risk of firing before
`MrxSupportData` itself has been touched yet. If you test this (either folder), we'd like to know: does
an `OnBoot`-time override to `tSupportData` actually stick, or does it get reset back to the original
value?

## Functions

### `IsSupportEquippable(sKey)`
Checks if a support item is equippable based on its key (`sKey`). Considers whether the recruit
requirement has been met and any additional optional requirements. Returns a boolean, plus an optional
string describing why the item is not equippable (missing recruit/requirement).

### `SetHeliPilotRecruited(bRecruited)` / `SetMechanicRecruited(bRecruited)` / `SetJetPilotRecruited(bRecruited)`
Sets the recruitment status of the named recruit type.

### `SetRequirement(sRequirement, bObtained)`
Sets the status of a specific requirement.

### `SynchNetRecruits(tRecruits)`
Synchronizes recruitment status across the network — sends an event if this is the server, otherwise
updates local state from received data.

### `SetIgnoreRequirements(bIgnore)`
Globally ignores (or stops ignoring) recruit requirements. **Confirmed working by live testing** — see
[MrxCheatBootstrap](mrxcheatbootstrap)'s "The Works!" snippet, which uses this.

### `Init()`
Initializes module-level state (`tRequirementsObtained`, `tRequirementStrings`) and builds the support
catalog described above.

### `GetFreebie(sSupportName)`
Retrieves the freebie data for a given support name.

### `AddAllFreebies()`
Adds all freebies to the player's inventory.

### `GetLocalRemote(vPlayers)`
Returns two booleans: whether there are local and/or remote players among `vPlayers`.

### `_AddFreebie(sSupportName, nQty, bAddingAllFreebies, nMaxQty)` / `AddFreebie(sSupportName, nQty, vPlayers, bAddingAllFreebies, nMaxQty)`
Adds a quantity of a freebie to the player's inventory, handling network sync and HUD updates. `Add*`
(no underscore) wraps the internal version with network-sync handling for a player list.

### `_RemoveFreebie(sSupportName)` / `RemoveFreebie(sSupportName, vPlayers)`
Removes a freebie from the player's inventory, updates the HUD, handles network sync.

### `GetFreebieStringIndex(uStringHash)` / `GetSupportStringIndex(uStringHash)`
Resolve a string hash back to its support name.

### `NetEventCallback(nEventId, tArgs)`
Handles network events related to adding/removing freebies.

### `Add(tSupport, sFaction)`
Adds support items to the player's inventory for a given faction, updating unlock status and checking
for achievements.

### `IsItemUnlocked(sSupportId, sFaction)` / `IsItemNew(sSupportId, sFaction)` / `SetItemViewed(sSupportId, sFaction)`
Per-faction unlock/new/viewed status tracking for catalog items.

### `SaveSingleton()` / `LoadSingleton(tSaveData)`
Serialize/restore this module's state to/from a save table.

### `AddSupportData(tSupportDataToAdd, sKey)`
Adds a new entry to `tSupportData`. Returns `true` on success, `nil` otherwise. This is what the ~130
individual catalog entries are built with internally.

### `GetMaxQuantity()`
Returns the max stock quantity for freebies.

### `GetPlayerVisibleName(sSupportId)` / `GetFreebieName(sSupportId)`
Resolve a support/freebie ID to its player-visible name.

## Events

- **`Event.PlayerJoined(uGuid)`** / **`Event.PlayerLeft(uGuid)`** — update recruitment status as players
  join/leave the session.
- **`Event.NetworkRecruitSync(tRecruits)`** — synchronizes recruit status across players.

## Notes for modders

- **Call-order requirements**: `Init()` sets up the tables this module depends on — see the timing
  discussion above if you're modifying `tSupportData` from your own script.
- **Pitfalls**: modifying recruitment status or freebie quantities affects player progression/game
  balance — know what you're changing before you ship it to anyone else.
- **Tunables**: `_kMaxStock = 99` is the ceiling every catalog entry currently uses; nothing stops a
  single entry's `nMaxStock` from being set higher (see the override example above).
