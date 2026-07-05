---
title: DangerousBuilding
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, world entity]
verified: true
verified_note: 'deeper pass: fixed the Events section (removed a non-existent RemoveDangerousBuilding *listener*; documented the real Event.ObjectHibernation + Event.ObjectHealth subscriptions and the outgoing Net.SendEvent_* calls); added a full Module constants section (radar textures/colours temp_radar_icon_db grey 170s vs temp_radar_icon_dbactive red 250,0,0, nMaxDBs=8, rarity magic strings, VZ Tower spawn tuning, reward toast); replaced vacuous Notes with SetProperties keys + the inverted-rarity gotcha; bare tDBs[uGuid] pattern re-confirmed'
---

# DangerousBuilding

*Module: dangerousbuilding.lua*

## Overview
The `DangerousBuilding` module manages dangerous buildings in the game. It handles the activation, deactivation, and state changes of these buildings, including their radar blips, health monitoring, and attached spawners. The module also supports setting properties such as rarity and reward for these buildings.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxGui`](mrxgui) (kill-reward toast), [`MrxPmc`](mrxpmc) (cash payout),
  [`MrxUtil`](mrxutil) (`CallWithOptionalArgs` for the optional wakeup function)

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
plain module-level table, `tDBs[uGuid] = tDBs[uGuid] or {}`, with no `Create`/`Delete`/`setmetatable`
anywhere. Each activated building gets a small sub-table entry in `tDBs`, not a full instance object with
inherited methods. It tracks the following key fields:
- `tDBs`: A table storing data for each dangerous building instance.
- `nDBCount`: The current count of active dangerous buildings.
- `nMaxDBs`: The maximum number of active dangerous buildings allowed.
- `nDefaultRarity`: The default rarity value for dangerous buildings.
- `nGlobalRarity`: The global rarity value that affects the activation probability.
- `nDefaultCashReward`: The default cash reward for destroying a dangerous building.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Handles the initialization of the dangerous building instance. If the building is occupied, it calls `SetupOccupied`. Otherwise, it rolls a random chance based on rarity and activates a random dangerous building if conditions are met.

### `SetupOccupied(uGuid, bForceOnClient)`
Sets up an occupied dangerous building by adding a grey radar blip and monitoring its health. If the building is permanently occupied, it sends a network event to update the server.

### `TurnOn(uGuid, bRadar, bPermanent, bForceOnClient)`
Activates the dangerous building by turning on attached spawners and changing the radar blip to red active. It also animates the blip size and sends a network event if necessary.

### `OccupiedBuildingSpawnCallback(uGuid)`
Animates the radar blip alpha for an occupied dangerous building when it spawns.

### `TurnOnRandomDB(uGuid, bForceOnClient)`
Activates a random dangerous building by turning on attached spawners with specific settings and sending a network event if necessary.

### `OnDeactivate(uGuid)`
Called when the object instance is deactivated. It removes the dangerous building if it's not permanent and deletes associated events.

### `Delete(oSelf)`
Calls `RemoveDB(oSelf.uGuid)`. Note the `oSelf.uGuid` access is the `Inheritable`-style calling convention,
but this module has no `Create`/`setmetatable` factory — so `Delete` is only meaningful if something external
passes it a table with a `.uGuid` field; it is not wired to the bare `tDBs[uGuid]` lifecycle used elsewhere
in this file.

### `OnDeath(uGuid)`
Handles the death of a dangerous building by removing it and rewarding the player if applicable.

### `ClearProperties(uGuid)`
Clears properties for the specified dangerous building by calling `RemoveDB`.

### `RemoveDB(uGuid, bKilled, bForceOnClient)`
Removes the specified dangerous building, updates radar blips, turns off attached spawners, and sends network events as necessary. If the building is killed, it rewards the player.

### `RemoveAllDBs()`
Removes all active dangerous buildings by calling `RemoveDB` for each one.

### `GetAllDBs()`
Prints debug information about all currently active dangerous buildings.

### `GetRarity(uGuid)`
Returns the rarity value of the specified dangerous building or the global rarity if none is set.

### `SetProperties(uGuid, tProps)`
Sets properties for the specified dangerous building, including density, faction, reward, and spawner settings.

### `_Process(tTable, data)`
Processes and inserts data into a table, converting names to GUIDs if necessary.

### `ConvertToTableOfGuids(tData)`
Converts input data into a table of GUIDs.

### `ProcessProperties(uGuid, tProps)`
Processes properties for the specified dangerous building, updating density, faction, reward, and spawner settings as needed.

### `SetFaction(uGuid, sFaction)`
Sets the faction for the specified dangerous building and updates attached spawners accordingly.

### `SetWakeupFunction(uGuid, fFunction)`
Sets a wakeup function for the specified dangerous building.

### `SetRarity(uGuid, iRarity)`
Sets the rarity value for the specified dangerous building or updates the global rarity if applicable.

### `SetDBFaction(uGuid, sFaction, tProps)`
Updates the faction settings for attached spawners of the specified dangerous building.

## Events
- **Creates** `Event.ObjectHibernation` (`OnActivate`) to call `Start` when the object leaves hibernation.
  The handle is stored as `tDBs[uGuid].WakeEvent`.
- **Creates** `Event.ObjectHealth` (`SetupOccupied`, server only) with comparator `"<"` against the
  building's current health, so `TurnOn` fires when the occupied building takes any damage. Stored as
  `tDBs[uGuid].HealthEvent`.
- `OnActivate`/`OnDeactivate`/`OnDeath`/`Delete`/`ClearProperties` are engine lifecycle callbacks, not
  `Event.*` subscriptions.

{: .note }
> The `Net.SendEvent_AddDangerousBuilding` / `Net.SendEvent_RemoveDangerousBuilding` /
> `Net.SendEvent_AddRandomDangerousBuilding` / `Net.SendEvent_SetOccupiedDangerousBuilding` calls are
> **outgoing** engine net-events (server → clients), not `Event.Create` subscriptions this module listens
> for. (A previous version of this page incorrectly listed a `RemoveDangerousBuilding` *listener* — there is
> none; only the send exists.)

## Module constants & tunables
- Caps/tuning: `nMaxDBs = 8` (max simultaneously-active random DBs), `nDefaultRarity = 16`,
  `nGlobalRarity` (starts at `nDefaultRarity`), `nDefaultCashReward = 0`, `nDBCount` (live counter).
- Inactive/occupied radar blip: texture `"temp_radar_icon_db"`, colour `170,170,170` (grey), size `8x8`,
  `nSortOrder = 3`, `bSticky = false`.
- Active radar blip: texture `"temp_radar_icon_dbactive"`, colour `250,0,0` (red), size `8x8`, then pulsed via
  `Hud.Radar:AnimateObjectiveSize` (`nDuration = 5`, width/height oscillating `4`–`12`).
- Blip name key: `"db_" .. tostring(uGuid)`.
- Random-DB spawner tweak (`TurnOnRandomDB`): `SpawnerType = "Once"`, `RadiusType = "RADIUS_PLAYER_2D"`,
  `ActiveRadius = 100`, `SkipPercentChange = 100`, `SpawnList = "Spawnlist (VZ Tower)"`; also turns the
  `"ground"` spawner group off.
- Kill reward message: `"[green]Occupied building destroyed! +$" .. nReward` (4s), paid via
  `MrxPmc.AddCashQty(nReward, true)` — only when `nReward > 0`.
- `SetRarity` magic strings: `"never"` → `-1` (never activates), `"always"` → `0`, `"default"` →
  `nDefaultRarity`; and `uGuid` of `"default"`/`"all"`/`"global"` sets `nGlobalRarity` instead of a per-object
  rarity.

## Notes for modders
- `SetProperties(uGuid, tProps)` is the main authoring lever — recognized keys include `Density` (0–100,
  converted to `ChanceNotActive`/`SkipPercentChance`), `Faction`, `Reward`, `Rarity`, `WakeupFunction`,
  `Group`, and any spawner fields passed straight to [`Ai`](../namespaces/ai)`.TweakAttachedSpawners`.
- Activation is probabilistic: `Start` rolls `math.randf() * nMaxDBs * iRarity` and only turns the building
  on if that is `< nMaxDBs`, so **larger `Rarity` means *less* likely** (and `< 0` / `"never"` disables it).
- Cash rewards flow through [`MrxPmc`](mrxpmc)`.AddCashQty` and the on-screen toast through
  [`MrxGui`](mrxgui)`.AddMessage`; the default reward is `0`, so buildings pay nothing unless a per-object
  `Reward` is set via `SetProperties`.
- `Permanent` buildings survive `OnDeactivate` (early return) — set via `TurnOn(..., bPermanent=true)`.
- This is the module [Alarm](alarm) calls into: `DangerousBuilding.TurnOn(tBuildings, true, false, true)`
  activates every occupied building near a tripped alarm.
- Debug helpers `GetAllDBs()` and `GetRarity(uGuid)` are handy from the console for inspecting live state.