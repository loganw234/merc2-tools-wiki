---
title: Munitions
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [munition, pickup, support]
verified: true
verified_note: 'deeper pass: added the full tMunitions table (21 stock entries incl. fuel 50/500/5000 and cash 100000 pickup values), the exact blip/marker textures + sizes per stock type, _kDistance/_nBlippedVOCoolDownTime constants, VO cue strings and the NETEVENT_* codes; re-confirmed all functions + the GetMunitionsCount bug; cross-linked Blippable/MrxPmc/MrxSupportData/namespaces.'
---

# Munitions

*Module: munitions.lua*

## Overview
The `Munitions` module manages the behavior and interactions of munition objects in the game world. It handles various aspects such as blipping, tagging, picking up, and network synchronization for different types of munitions (support, fuel, cash). The module also manages tutorial messages and voice-over (VO) cues related to these interactions.

## Inheritance
- Inherits from: [`Blippable`](blippable) (→ [`Inheritable`](inheritable))
- Imports: [`MrxGui`](mrxgui), [`MrxPlayState`](mrxplaystate), [`MrxPmc`](mrxpmc),
  [`MrxSupportData`](mrxsupportdata), [`MrxTutorialManager`](mrxtutorialmanager), [`MrxUtil`](mrxutil),
  [`MrxVoSequence`](mrxvosequence), [`MrxMunitionsPickup`](mrxmunitionspickup)

Blipping/marker/objective behavior (`self:SetBlipped()`, `self:AddObjective()`,
`self:RemoveObjective()`, `Delete`→`Blippable.Delete`) is inherited from [`Blippable`](blippable);
this module only sets the blip *appearance* fields and drives the tag/pickup logic.

## Instance pattern
This is a genuine per-instance object module (keyed by `uGuid`) — confirmed via `OnActivate`/`Awake`/`tInstance` and `oPrototype:Create(uGuid, nStock)` (line 49), inherited from `Blippable`/`Inheritable`. Per-instance fields set directly on `oInstance`/`self`:
- `nStock`: The type of munition (support, fuel, or cash) — index into the module-level `tMunitions` table.
- `bTagged`: Indicates whether the munition has been tagged (context action performed).
- `bPickedUp`: Indicates whether the munition has been picked up.
- `bActive`: Inherited from `Blippable` (not a field this file sets directly) — tracks whether the instance is currently blipped; toggled by `Blippable.SetBlipped`/`ClearBlipped`, which this module calls via `self:SetBlipped()`/`self:ClearBlipped()`. The wiki previously called this `bBlipped`; that name does not appear in either `munitions.lua` or `blippable.lua`.
- `TagEvent`, `VehicleEnterEvent`, `VehicleExitEvent`, `NearnessEvent`, `FarnessEvent`: Individual event handles for the context action, vehicle enter/exit, and radar proximity events, each deleted in `Delete(self)`. There is no `tContextActions` table anywhere in the source — context actions are registered directly via `Pg.AddContextAction`, not stored in a table on the instance.
- `sTexture`, `tColor`, `tFlash`, `nSize`, `tMarker`: Radar blip/marker appearance, set in `Awake` based on stock type (support/fuel/cash each get distinct texture and marker constants).

## Functions

### OnActivate(uGuid, uRuntimeOwner, nStock)
- **Description**: Called when the world object instance is spawned/activated.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
  - `uRuntimeOwner`: Runtime owner of the object.
  - `nStock`: Stock type of the munition.
- **Behavior**: Creates an event to call `Awake` when the object leaves hibernation.

### Awake(uGuid, nStock)
- **Description**: Initializes the instance and sets up blip/marker textures, adds context actions, and registers proximity-near events.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
  - `nStock`: Stock type of the munition.
- **Behavior**: Sets various properties based on the stock type (support, fuel, or cash), adds a context action, and sets up nearness events.

### OnDeactivate(uGuid)
- **Description**: Called when the instance is being torn down.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
- **Behavior**: Handles immediate pickup of hibernated munitions if necessary, then calls `Blippable.OnDeactivate(uGuid)`. Note: `Blippable` itself does not define `OnDeactivate` — this call resolves through the inheritance chain to `Inheritable.OnDeactivate` (`Blippable` does `inherit("Inheritable")`). Works correctly via metatable fallback, just not literally defined where the call site implies.

### HideTutorialMessage(uGuid)
- **Description**: Hides a tutorial message and deletes the associated event.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.

### SetAllowBlippedVO(bAllow)
- **Description**: Sets whether blipped VO messages are allowed.
- **Parameters**:
  - `bAllow`: Boolean flag to allow or disallow blipped VO messages.

### PlayBlippedVO(nStock)
- **Description**: Plays a blipped VO message based on the stock type and current state.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Behavior**: Checks conditions and plays the appropriate VO cue, sets cooldown timers, and updates played hint flags.

### Near(self)
- **Description**: Called when the player enters the near proximity of the object.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Plays a blipped VO message if in free play mode, sets the object as blipped, sends a network event, and registers farness events.

### Far(self)
- **Description**: Called when the player exits the near proximity of the object.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Clears the blipped state, unregisters farness events, and registers nearness events again.

### AddContextAction(self)
- **Description**: Adds a context action to the object for tagging purposes.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Adds a context action based on the stock type and whether the object is in a vehicle. Handles vehicle-specific events as well.

### CanActionTarget(uGuid, uHero, nStock)
- **Description**: Checks if the munition can be targeted by the player.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
  - `uHero`: Player character GUID.
  - `nStock`: Stock type of the munition.
- **Behavior**: Enforces various conditions such as taggable status, fuel capacity, and support stock limits. Shows tutorial messages if necessary.

### Actioned(self, uHero)
- **Description**: Called when a context action is performed on the object.
- **Parameters**:
  - `self`: The instance table.
  - `uHero`: Player character GUID.
- **Behavior**: Checks if the munition can be targeted and calls `ActionTarget` if conditions are met.

### ActionTarget(uGuid)
- **Description**: Handles the successful action on the object, updating various states and playing VO cues.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
- **Behavior**: Updates context actions, changes marker colors, pulses markers, sends network events, marks the munition as tagged, and plays VO sequences.

### HumanControlled(self, uCharacter)
- **Description**: Handles when a human character takes control of the object (e.g., entering a vehicle).
- **Parameters**:
  - `self`: The instance table.
  - `uCharacter`: Character GUID.
- **Behavior**: Deletes the current instance and sets up events for exiting the vehicle.

### Delete(self)
- **Description**: Tears down the per-instance table, unregistering from various events and updating states.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Removes context actions, clears blipped state, deletes events, updates tagged counters, and posts relevant events.

### OnDeath(uGuid)
- **Description**: Called when the object's underlying object dies.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
- **Behavior**: Calls `Inheritable.OnDeath` and removes context actions if on the client side.

### IsCash(nStock)
- **Description**: Checks if the stock type is cash.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Returns**: Boolean indicating if the stock type is cash.

### IsFuel(nStock)
- **Description**: Checks if the stock type is fuel.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Returns**: Boolean indicating if the stock type is fuel.

### IsSupport(nStock)
- **Description**: Checks if the stock type is support.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Returns**: Boolean indicating if the stock type is support.

### SetMunitionsTaggable(bTaggable)
- **Description**: Sets whether munitions are taggable and refreshes relevant states.
- **Parameters**:
  - `bTaggable`: Boolean flag to set munitions as taggable or not.
- **Behavior**: Updates the taggable state, sends network events if necessary, and refreshes context actions.

### AreMunitionsTaggable()
- **Description**: Checks if munitions are currently taggable.
- **Returns**: Boolean indicating if munitions are taggable.

### RefreshMunitions()
- **Description**: Refreshes context actions for all untagged and unpicked up munitions.
- **Behavior**: Iterates through instances, updates context actions based on stock type, and handles non-taggable states.

### SaveSingleton()
- **Description**: Saves the current state of various module-level variables.
- **Returns**: A table containing the saved state.

### LoadSingleton(tSaveData)
Loads saved data for the munitions module. If `tSaveData` is a table, it sets the munitions to be taggable or not based on `bMunitionsTaggable`, and updates various hint flags (`_bPlayedCashHint1`, `_bPlayedFuelHint1`, etc.) from the save data.

### PickupAllMunitions()
Iterates over all instances of munitions in `tInstance` and calls `PickupMunitions(uGuid)` for each one to pick up all munitions.

### PickupMunitions(uGuid)
Handles the pickup logic for a specific munition instance. It checks if the PDA widget is available, retrieves the munition instance from `tInstance`, and processes it based on its type (support, fuel, or cash). If valid, it updates the player's PMC stats, posts an event, sends a custom network event if on the server, marks the munition as picked up, deactivates it, and fades it out if not winched.

### GetTaggedMunition()
Returns the GUID of the first tagged munition found in `tInstance`. If no tagged munition is found, returns `nil`.

### IsMunitionTagged(uMunition)
Checks if a specific munition (identified by its GUID) is tagged. Returns `true` if tagged, otherwise `false`.

### ClientTagAndBlip(uGuid)
Tags and blips a specific munition on the client side. It updates the color of the objective and marker for the munition instance and pulses the marker.

### GetMunitionsCount()
**Confirmed bug in source (line 635).** Checks `_nTagged > 0`, but the return statement reads a *different*, never-assigned global `nTagged` (missing the leading underscore) instead of `_nTagged`:
```lua
function GetMunitionsCount()
  if _nTagged > 0 then
    return nTagged        -- bug: should be _nTagged; nTagged is never declared/assigned anywhere in this file
  else
    return false, "nomunitions"
  end
end
```
In practice this means: whenever at least one munition is tagged, the function returns `nil` (Lua's default value for an unset global) instead of the actual tagged count. The "no munitions tagged" branch (`false, "nomunitions"`) is unaffected and works as documented.

### NetEventCallback(nType, tArgs)
Handles network events related to munitions. It processes different event types such as setting munitions taggable, client stockpile queries and acknowledgments, pickup events, marker pulses, and checking if a munition is tagged.

### OnPlayerJoined()
Called when a player joins the game. If on the server, it sends a custom network event to set whether munitions are taggable based on the current state.

## Events

The following `Event.*` constants are the ones actually referenced in this file (a previous version of this page listed `Event.PlayerNear`, `Event.PlayerFar`, `Event.ObjectDeath`, and `Event.PlayerJoined` — none of those appear anywhere in `munitions.lua`; `OnDeath` and `OnPlayerJoined` are lifecycle callback names the engine/inheritance chain calls directly, not events this file wires up itself):

- **Event.ObjectHibernation**: Wired in `OnActivate` to call `Awake` when the object leaves hibernation.
- **Event.ObjectProximity**: Used twice, for proximity-based blip near/far detection — `Near`/`Far` register each other via `Event.Create(Event.ObjectProximity, {uGuid, Player.GetLocalCharacter(), "<"/">"​, _kDistance}, ...)`.
- **Event.ContextAction**: Wired in `AddContextAction` (`self.TagEvent`) to call `Actioned` when the player performs the tag context action.
- **Event.ObjectInSeat**: Used in `AddContextAction` (vehicle exit, one-shot) and as a persistent vehicle-enter listener (`self.VehicleEnterEvent`) calling `HumanControlled`.
- **Event.TimerRelative**: Used for the blipped-VO cooldown (`PlayBlippedVO`/`SetAllowBlippedVO`) and for hiding tutorial messages after a delay (`HideTutorialMessage`, via `_tHideEvents`).

## Module constants & tunables

The `nStock` field is a 1-based index into the module-level `tMunitions` table, which is the single
source of truth for what each pickup contains:

- **Indices 1–17 (support)** — string names: `"artillery"`, `"bombingrun"`, `"bunkerbuster"`,
  `"carpetbomb"`, `"clusterbomb"`, `"combatairpatrol"`, `"cruisemissile"`, `"daisycutter"`,
  `"fuelairbomb"`, `"harm"`, `"laserguidedbomb"`, `"moab"`, `"rocketartillery"`, `"smartbomb"`,
  `"strategicmissile"`, `"surgicalstrike"`, `"tankbuster"`. Each grants 1 of that support (via
  `MrxPmc.AddSupportQty`), capped at `MrxSupportData.tSupportData[name].nMaxStock`.
- **Indices 18–20 (fuel)** — `{nFuel = 50}`, `{nFuel = 500}`, `{nFuel = 5000}`. Adds fuel via
  `MrxPmc.AddFuelQty`; refused when fuel is already at capacity.
- **Index 21 (cash)** — `{nCash = 100000}`. Adds cash via `MrxPmc.AddCashQty(..., "[Generic.Pickups]")`.

Change these values to retune pickup rewards. `IsSupport`/`IsFuel`/`IsCash` classify a stock by the
shape of its `tMunitions` entry (string vs. `nFuel` table vs. `nCash` table).

**Blip & marker appearance** (set in `Awake`, per stock type):

| Stock   | Radar texture (`sTexture`) | Marker texture (`tMarker.sTexture`) |
|---------|----------------------------|-------------------------------------|
| Support | `radar_Munition`           | `pickup_munitions`                  |
| Fuel    | `radar_Oil`                | `pickup_fuel_2`                     |
| Cash    | `radar_Money`              | `pickup_cash_2`                     |

All three share radar `tColor = {51,102,51}`, `tFlash = {255,255,255}`, radar `nSize = 8`, and marker
`tColor = {153,255,153}`, marker `nSize = 40`, `nNearDist = 5`, `nFarDist = 100`. On tag, the color
flips to green `{0,255,0}` and the marker pulses (`Marker.Pulse(uGuid, 0, 255, 0)`).

**Other tunables**
- `_kDistance = 175` — radar near/far proximity threshold (`Event.ObjectProximity` distance for
  `Near`/`Far`).
- `_nBlippedVOCoolDownTime = 30` — cooldown (seconds) between "blipped" hint VO lines. There is also a
  hard-coded 10s initial gate before the first blipped VO is allowed.
- **VO cues** (see `PlayBlippedVO`/`ActionTarget`/`PickupMunitions`): hint lines like
  `"Fiona.Misc.Cash01/02"`, `"Fiona.Misc.Fuel01/02"`, `"Fiona.Misc.Munition01/02"`; tag lines
  `"Fiona.Support.Munitions02/03"` plus character variants; first-fuel-pickup line
  `"Fiona-In-Mission-Freeplay-None-25"`. All play at `MrxVoSequence.knPriorityFreeplay`.
- **Net event codes**: `NETEVENT_SETTAGGABLE=0`, `NETEVENT_CLIENTSTOCKPILEQUERY=1`,
  `NETEVENT_CLIENTSTOCKPILEACK=2`, `NETEVENT_PICKUP=3`, `NETEVENT_MARKERPULSE=4`,
  `NETEVENT_ISMUNITIONTAGGED=5` — all sent over the `"Munitions"` custom-event channel.

## Notes for modders
- **Retune reward amounts** by editing `tMunitions` (fuel 50/500/5000, cash 100000). To add a new
  support type to pickups, add its `MrxSupportData` name string to the list.
- **Swap blip/pickup icons** via the texture strings above — the `pickup_*` markers and `radar_*`
  radar icons are the visual knobs.
- `GetMunitionsCount` is **broken** (see above): the "count" branch returns `nil`. If you rely on it,
  read `_nTagged` directly instead.
- Munitions inside a vehicle are handled specially: the tag context action is deferred until the
  vehicle is exited (`AddContextAction`/`HumanControlled` via `Event.ObjectInSeat`), and the instance
  is torn down and re-activated across enter/exit. Don't assume a munition's instance persists while
  it's being driven around.
- `SetMunitionsTaggable(false)` greys out the tag prompt (prefixes the context action with `[neut]`)
  and is server-authoritative — it re-broadcasts via `NETEVENT_SETTAGGABLE`. This is the intended
  lever for gating munitions behind "get a pilot first".
- Pickup progress is server-authoritative; clients are queried via `CanActionTarget` →
  `NETEVENT_CLIENTSTOCKPILEQUERY`/`ACK` before a tag is confirmed. See [`Net`](../namespaces/net).