---
title: Laptop
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [pickup, support]
verified: true
verified_note: confirmed real per-uGuid instance pattern (Blippable -> Inheritable chain); added tMunitions/module-level fields, fixed Delete/OnDeath details; events list confirmed against source, no invented events found.
---

# Laptop

*Module: laptop.lua*

## Overview
The `Laptop` module represents a fixed support-munition pickup in the game world. It handles the creation, activation, and deletion of laptop objects, as well as managing their radar blips and player interactions.

## Inheritance
- Inherits from: `Blippable`
- Imports: `MrxGui`, `MrxPmc`, `MrxSupportData`, `MrxTutorialManager`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
**Confirmed real per-`uGuid` instance pattern.** `Awake` calls `oPrototype:Create(uGuid, nStock)`, where
`oPrototype` is `getfenv()` (this module's own table) and `Create` resolves up the inheritance chain
(`Blippable` -> `Inheritable`), which builds the instance table via `setmetatable`/`__index` and registers
it in `Inheritable`'s `tInstance` registry keyed by `uGuid`. Per-instance fields set in this file:
- `nStock`: The munition/resource index into the module-level `tMunitions` table, associated with this laptop.
- `TaggedMarker`: A reference to any tagged marker associated with the laptop (set/cleared elsewhere via `Blippable`; read and removed in `Delete`).
- `_uHideMessage`: An event handle for hiding messages (read and deleted in `Delete`; not set anywhere in this file — likely set by `Blippable` or another cooperating module).

Module-level (not per-instance) state:
- `_kDistance = 150`: blip visibility distance constant.
- `tMunitions`: an array of munition/resource templates (strings like `"artillery"`, `"moab"`, or
  tables like `{nFuel = 50}`, `{nCash = 100000}`) indexed by `nStock`.
- `_nTagged`: a running count of currently-tagged laptop markers, decremented in `Delete`.
- `_tStatusList`: initialized empty in `OnDeath` if `nil`; not otherwise read/written in this file.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, nStock)`
Called when the object instance is activated. It sets up an event to call `Awake` once the object leaves hibernation.

### `Awake(uGuid, nStock)`
Bails out early if `Object.GetHealth(uGuid) == 0`. Sets blip texture/color/flash/size and marker fields
on the module prototype (`oPrototype.sTexture`, `.tColor`, `.tFlash`, `.nSize`, `.tMarker`), then creates
the per-instance table via `oPrototype:Create(uGuid, nStock)`, calls `oInstance:SetBlipped()`, stores
`oInstance.nStock`, and registers an `Event.WeaponEvent` listener (`"hero", "pickup", "Laptop"`) that
calls `PickupMunitions` with this instance as its bound argument. Note: there's a dead `if not
tMunitions[nStock] then end` check with an empty body — it evaluates the condition but performs no
action either way.

### `Delete(oSelf)`
Tears down the per-instance table: clears the blip (`oSelf:ClearBlipped()`), and if `oSelf.TaggedMarker`
is set, removes the marker (`Marker.Remove`), tells other clients to remove the marker objective if this
is the server (`Net.SendEvent_RemoveMarkerObjective`), clears the field, and decrements `_nTagged`. Also
deletes `oSelf._uHideMessage` if set. Finally calls `Blippable.Delete(oSelf)` to run the base class's teardown.

### `OnDeath(uGuid)`
Called when the object instance dies. Ensures `_tStatusList` is initialized (`{}`) if it's `nil`, then
calls `Inheritable.OnDeath(uGuid)` directly (bypassing any `Blippable`-level override) to run the base
death handling.

### `PickupMunitions(oInstance)`
Handles the player interaction with the laptop. Looks up the local player's PDA widget via
`MrxGui.GetWidgetByNameAndOwner("PDA", Player.GetLocalPlayer())` (logs `"ERROR: No PDA found!"` and bails
if missing), posts a `"MunitionsPickup"` script event with `{vStock, uGuid}`, adds the stock via
`MrxPmc.AddSupportQty(vStock, 1, true)`, updates the PDA display (`oPda:UpdateSupport`), and plays a
random voice-over cue (`"Fiona.Support.Munitions02"` or `"Fiona.Support.Munitions03"`) via
`MrxVoSequence.Start`.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `WeaponEvent` with parameters `"hero", "pickup", "Laptop"` to trigger `PickupMunitions`.

## Notes for modders
- There is no `OnDeactivate` defined in this file — lifecycle here is just `OnActivate` -> `Awake` -> (eventually) `Delete`/`OnDeath`.
- Customize the stock types by modifying the `tMunitions` table (index corresponds to the `nStock` argument passed into `OnActivate`).
- Be aware of network synchronization: `Delete` only sends `Net.SendEvent_RemoveMarkerObjective` when `Net.IsServer()` is true.
- The `_kDistance` constant (150) is defined but not read anywhere in this file — likely consumed by `Blippable` or the radar/blip engine subsystem, not visible here.