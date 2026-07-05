---
title: MrxOilCon002Delivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDelivery
tags: [support, delivery]
verified: true
verified_note: 'spot-checked in deeper pass, confirmed accurate; cross-linked parent/designator, confirmed the mpPlayerJoin ScriptEvent + NETEVENT_SETDELIVERYLOCATIONS sync + 30m drop-zone gate against source, and clarified _tDeliveryLocations is a file-local (not a self field)'
---

# MrxOilCon002Delivery

*Module: mrxoilcon002delivery.lua*

## Overview
The `MrxOilCon002Delivery` module is a mission-specific supply drop: it delivers a "Listening Post" crate,
but only to one of a fixed set of predefined drop locations. It subclasses
[`MrxSupportDelivery`](mrxsupportdelivery) (inheriting the whole spawn/winch/drop sequence) and adds a custom
drop-zone validation that snaps the target to the nearest of three mission locations and rejects anything too
far. It also keeps the current set of enabled locations in sync across co-op clients.
[`MrxSupportData`](mrxsupportdata) wires it as the `OilCon002_Delivery` freebie.

## Inheritance
- Inherits from: [`MrxSupportDelivery`](mrxsupportdelivery)
- Imports: [`MrxSupportDesignator`](mrxsupportdesignator), `MrxSubtitle`, `MrxOilCon002Delivery`

## Instance pattern
**Same class-factory pattern as [`MrxSupportDelivery`](mrxsupportdelivery), not per-`uGuid`** —
`Create(oSelf, uOwnerGuid)` builds a new table via `setmetatable`/`__index`, exactly like its parent. No
`OnActivate`/`Awake`, no `tInstance` registry.

The mission's location state is **module-level, not per-instance**:
- `_tDeliveryLocations` — a **file-local** (`local`) list of the currently-enabled drop-zone names, defaulting
  to `oilcon002_loc_postA`/`postB`/`postC` (set by `ResetDropZones`). Shared across all instances; access it
  via `GetCurrentDropZones()`.
- `NETEVENT_SETDELIVERYLOCATIONS = 0` — the ID for this module's `Net.SendCustomEvent("MrxOilCon002Delivery",
  ...)` traffic that syncs which of the three zones are enabled (encoded as three 0/1 flags).
- `_ePlayerJoin` — a persistent `mpPlayerJoin` `Event.ScriptEvent` handle, created once, that re-sends the
  zone state to joining clients (server only).

## Functions
### `NetEventCallback(nEventType, tArgs)`
Called when a network event is received. If the event type matches `NETEVENT_SETDELIVERYLOCATIONS`, it resets the drop zones and removes any disabled ones based on the event arguments.

### `NetSendDropZones(bPlayerJoined)`
Sends the current state of delivery locations to all clients if the server is active. It encodes the enabled status of each location (A, B, C) into a network event.

### `ResetDropZones()`
Resets the drop zones to their default locations (`oilcon002_loc_postA`, `oilcon002_loc_postB`, `oilcon002_loc_postC`) and sends this state over the network.

### `AddSupport()`
Adds a "Listening Post Delivery" item to the support menu for all players. This item allows players to request a listening post delivery mission.

### `RemoveSupport()`
Removes the "Listening Post Delivery" item from the support menu for all players, effectively disabling the mission option.

### `Create(oSelf, uOwnerGuid)`
Creates a new instance of the support delivery mission. It sets up the cargo type, validation function, and network event listener for player joins.

### `_ValidateDropZone(fCallback, nX, nY, nZ, oSupport)`
Validates whether a proposed drop zone is within 30 meters of any active drop location. If valid, it adjusts the coordinates to the center of the nearest location and calls the callback with success; otherwise, it calls the callback with failure.

### `GetDistanceToObject(uObjectA, nX, nY, nZ, bIgnoreY)`
Calculates the distance between an object (`uObjectA`) and a specified point `(nX, nY, nZ)`. If `bIgnoreY` is true, it ignores the Y-axis difference.

### `GetDistanceBetween(uObjectA, uObjectB, bIgnoreY)`
Calculates the distance between two objects (`uObjectA` and `uObjectB`). If `bIgnoreY` is true, it ignores the Y-axis difference.

### `RemoveDropZone(nIndex)`
Removes a drop zone at the specified index from `_tDeliveryLocations` and sends the updated state over the network.

### `GetCurrentDropZones()`
Returns the current list of active drop zones.

## Events
- **`Event.ScriptEvent`** `"mpPlayerJoin"` (persistent, `_ePlayerJoin`, server + non-local joiner only) →
  `NetSendDropZones` re-broadcasts the current enabled zones to the new client.
- **`NetEventCallback(nEventType, tArgs)`** is the receiver for this module's `NETEVENT_SETDELIVERYLOCATIONS`
  custom net event — it resets the zones and removes any the flags mark disabled. Dispatched by module name,
  not via `Event.*`.

The actual delivery events (`Event.ObjectHibernation`, `Event.ObjectWinched`) are inherited from
[`MrxSupportDelivery`](mrxsupportdelivery).

## Notes for modders
- **Drop is location-locked**: `_ValidateDropZone` snaps the target to the nearest active
  `oilcon002_loc_post*` within `30`m and rejects anything farther (`"oilcon002_toofar"`, which
  [`MrxSupport.DenialMessage`](mrxsupport) turns into an "unclear" message + a Fiona VO). Change the `30`m
  gate or the `_tDeliveryLocations` names to retarget it.
- **Enabling/disabling zones**: `RemoveDropZone(nIndex)` drops one location and re-syncs; `ResetDropZones()`
  restores all three. Both call `NetSendDropZones` so co-op stays consistent.
- **`AddSupport`/`RemoveSupport`** add/remove the "[support.supply.listeningpost.name]" menu item for all
  players — this is a scripted mission support, not a purchasable catalog entry.