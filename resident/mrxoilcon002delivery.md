---
title: MrxOilCon002Delivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDelivery
tags: [support, delivery]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxOilCon002Delivery

*Module: mrxoilcon002delivery.lua*

## Overview
The `MrxOilCon002Delivery` module manages the listening-post delivery support mission. It inherits from `MrxSupportDelivery` and handles the setup, validation, and network synchronization of drop zones for delivering listening posts to specific locations.

## Inheritance
- Inherits from: `MrxSupportDelivery`
- Imports: `MrxSupportDesignator`, `MrxSubtitle`, `MrxOilCon002Delivery`

## Instance pattern
**Same class-factory pattern as [`MrxSupportDelivery`](mrxsupportdelivery), not per-`uGuid`** —
`Create(oSelf, uOwnerGuid)` builds a new table via `setmetatable`/`__index`, exactly like its parent. No
`OnActivate`/`Awake`, no `tInstance` registry. It tracks the following key fields:
- `_tDeliveryLocations`: A table of current drop zone locations.
- `NETEVENT_SETDELIVERYLOCATIONS`: An event type constant for setting delivery locations.

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
- Listens for `Event.ScriptEvent` with `"mpPlayerJoin"` to call `NetSendDropZones` when a new player joins the server.
- Listens for custom event `NETEVENT_SETDELIVERYLOCATIONS` to update drop zone states based on network events.

## Notes for modders
- Ensure that `AddSupport` and `RemoveSupport` are called appropriately to manage the availability of the listening post delivery mission in the support menu.
- Customize drop zone locations by modifying `_tDeliveryLocations`.
- Be aware that network synchronization (`NetSendDropZones`) ensures consistent state across all clients.
- The validation function `_ValidateDropZone` can be extended or modified to change the criteria for valid drop zones.