---
title: Laptop
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [pickup, support]
verified: true
verified_note: "deeper pass: re-confirmed the per-uGuid Blippable->Inheritable instance pattern and all 5 functions; surfaced the exact blip/marker constants set in Awake (radar_Munition/pickup_munitions textures, colors, sizes 8/48) and the full 21-entry tMunitions table shape; VO cues and the WeaponEvent filter re-confirmed"
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
- `tMunitions`: a 21-entry array indexed by `nStock`. Entries 1–17 are support-type strings (`"artillery"`,
  `"bombingrun"`, `"bunkerbuster"`, `"carpetbomb"`, `"clusterbomb"`, `"combatairpatrol"`, `"cruisemissile"`,
  `"daisycutter"`, `"fuelairbomb"`, `"harm"`, `"laserguidedbomb"`, `"moab"`, `"rocketartillery"`,
  `"smartbomb"`, `"strategicmissile"`, `"surgicalstrike"`, `"tankbuster"`); entries 18–21 are resource
  tables (`{nFuel = 50}`, `{nFuel = 500}`, `{nFuel = 5000}`, `{nCash = 100000}`). `Awake` receives `nStock`
  and this is the value handed to `MrxPmc.AddSupportQty` on pickup.
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

## Module constants & tunables
Set on the prototype in `Awake` (so every laptop shares them):
- **Radar blip:** `sTexture = "radar_Munition"`, `tColor = {51, 102, 51}` (dark green),
  `tFlash = {255, 255, 255}` (white), `nSize = 8`.
- **Map marker** (`tMarker`): `sTexture = "pickup_munitions"`, `tColor = {153, 255, 153}` (light green),
  `nSize = 48`.
- **Pickup VO:** one of `"Fiona.Support.Munitions02"` / `"Fiona.Support.Munitions03"`, chosen at random.
- **Pickup trigger:** `Event.WeaponEvent` filtered `{"hero", "pickup", "Laptop"}`.

## Notes for modders
- **What it gives you:** the payout is `tMunitions[nStock]` — either a support type (added via
  [MrxPmc](mrxpmc)`.AddSupportQty`) or a `{nFuel=...}`/`{nCash=...}` resource. Change the `tMunitions`
  entry (or the `nStock` passed into `OnActivate`) to change the reward. This is a great "free supplies"
  mod lever.
- **Restyle the blip/marker:** edit the `sTexture`/`tColor`/`nSize` and `tMarker` values in `Awake`.
- No `OnDeactivate` in this file — lifecycle is `OnActivate` → `Awake` → (eventually) `Delete`/`OnDeath`.
- Network: `Delete` only sends `Net.SendEvent_RemoveMarkerObjective` when `Net.IsServer()` is true.
- The `_kDistance` constant (150) is defined but not read anywhere in this file — likely consumed by
  [Blippable](blippable) or the radar/blip engine subsystem, not visible here.