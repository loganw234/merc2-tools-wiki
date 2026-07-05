---
title: Crate
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [winchable, blip]
verified: true
verified_note: 'deeper pass: re-confirmed the bare tGuids[uGuid] bookkeeping pattern and all four lifecycle functions; added the full Marker.AddBlip args (opaque white 255,255,255,255 + 0.5,16,20 tail) and cross-linked the Marker namespace — the earlier note undersold the blip colour/params'
---

# Crate

*Module: crate.lua*

## Overview
The `Crate` module represents a winchable crate object in the game world. It manages the crate's blip marker on the minimap and handles its winching state.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
plain module-level table, `tGuids[uGuid] = tGuids[uGuid] or {}`, with no `Create`/`Delete`/`setmetatable`
anywhere. Each activated crate gets a small sub-table entry in `tGuids`, not a full instance object with
inherited methods. It tracks:
- `tGuids[uGuid].Marker`: The GUID of the blip marker added to the minimap.
- `tGuids[uGuid].Winched`: An event handle for the crate's winching state.

## Functions
### `OnActivate(uGuid)`
Called when the crate instance is spawned/activated. Initializes the crate's state and sets up an event listener for its hibernation state.

### `Awake(uGuid)`
Handles the crate's awakening from hibernation. If the crate is not winched, it adds a blip marker to the minimap. If the crate is winched, it removes any existing blip marker.

### `OnDeactivate(uGuid)`
Called when the crate instance is being torn down (despawned/unloaded). Removes any existing blip marker and deletes all associated events.

### `OnDeath(uGuid)`
Called when the underlying object of the crate dies. Deactivates the crate instance by calling `OnDeactivate`.

## Events
- Listens for: `Event.ObjectHibernation` to handle the crate's awakening.
- Listens for: `Event.ObjectWinched` to update the blip marker based on the crate's winching state.

## Module constants & tunables
- Blip texture: `sTexture = "pickup_crate_2"` (the one module-level constant; swap to re-skin the minimap
  blip).
- Full blip call (in `Awake`):
  `Marker.AddBlip(uGuid, "pickup_crate_2", 48, 255, 255, 255, 255, 0.5, 16, 20)` — size `48`, colour
  `255,255,255,255` (opaque white RGBA), then `0.5, 16, 20` (the remaining `Marker.AddBlip` params — e.g.
  scale/range values). See [Marker](../namespaces/marker) for the full signature.

## Notes for modders
- The crate uses a blip marker with texture `"pickup_crate_2"` and size `48`, drawn opaque white.
- When the crate is winched (`Object.IsWinched(uGuid)`), its blip marker is removed from the minimap; the
  blip returns when it is un-winched, because `Awake` re-runs on each `Event.ObjectWinched`.
- `OnActivate`/`Awake`/`OnDeactivate`/`OnDeath` are engine-invoked — you don't call them yourself. The only
  real skin lever here is `sTexture`; everything else is bare bookkeeping.