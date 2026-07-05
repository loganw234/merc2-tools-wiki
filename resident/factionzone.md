---
title: FactionZone
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [faction, radar]
verified: true
verified_note: 'deeper pass: re-confirmed every function/event against source; added a Module constants section (dark-red 64,0,0,160 region colour + the full hash-keyed faction abbreviation map) and Inheritable/MrxGui/Hud/Ai cross-links; prior fixes (hash-keyed _tAssociationMap, inherited OnDeactivate/OnDeath, BoundaryCallback condition) still hold'
---

# FactionZone

*Module: factionzone.lua*

## Overview
The `FactionZone` module adds a colored line region to the radar and PDA map for specific faction zones. It also sends `TrespassStateChange` GUI events (via `MrxGui.SendEvent`) when players enter or exit these zones.

## Inheritance
- Inherits from: [`Inheritable`](inheritable)
- Imports: [`MrxGui`](mrxgui) (sends the `TrespassStateChange` GUI event)

## Instance pattern
Per-instance object module (keyed by `uGuid`), created via the standard `OnActivate` → `Awake`-equivalent → `Create` idiom (here `OnActivate` calls `oPrototype:Create(uGuid, uRuntimeOwner)` directly, with no separate `Awake`/hibernation wait — unlike `Inheritable`'s documented `OnActivate`/`Awake` split, this file's own `OnActivate` skips straight to `Create`). Tracks the following key fields:
- `uFaction`: The GUID of the faction associated with the zone (`Ai.GetFactionGuid(oSelf.uGuid)`).
- `sFaction`: The short faction abbreviation (e.g. `"All"`, `"Pmc"`), copied from `_tAssociationMap`.
- `bActive`: Indicates whether the zone's visual and event triggers are active (set in `Enable`, cleared in `Disable`).
- `bTrespassing`: Tracks if a player is currently trespassing in the zone.
- `BoundaryEvent`: Persistent event handle for the boundary listener, set in `Enable`, deleted in `Disable`.

## Functions
### `Init()`
Initializes the module-level global `_tAssociationMap`, keyed by `String.GetHash(<faction name>)` (not the plain name string) — e.g. `[String.GetHash("Allied")] = {sFaction = "All"}`. Covers `Allied`, `China`, `Civ`, `Guerilla`, `OC`, `Pirate`, `PMC`, `VZ`.

### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. Immediately creates a new per-instance table via `oPrototype:Create(uGuid, uRuntimeOwner)` — note `iArg` is accepted but not forwarded to `Create` (only `uGuid`/`uRuntimeOwner` are passed).

### `Create(oPrototype, uGuid, uRuntimeOwner)`
Calls `Inheritable.Create(oPrototype, uGuid, uRuntimeOwner)`, then sets `oSelf.uFaction` from `Ai.GetFactionGuid`, looks up `Object.GetName(oSelf.uFaction)` (a hash) in `_tAssociationMap`, and copies every key/value from the matched entry onto `oSelf` (currently just `sFaction`). Calls `oSelf:Enable()` if `bActive` is not already set. If the faction name's hash isn't a key in `_tAssociationMap`, this indexes a nil table in the `pairs(...)` call and would error — no fallback/default entry exists.

### `Delete(oSelf)`
Tears down the per-instance table by calling `oSelf:Disable()` if `bActive`, then `Inheritable.Delete(oSelf)`. This file defines no `OnDeactivate`/`OnDeath`; teardown is invoked via `Inheritable.OnDeactivate`/`Inheritable.OnDeath`, both inherited, which call `oInstance:Delete()`.

### `BoundaryCallback(oSelf, uObjectGuid, uBoundaryGuid, sAction)`
Callback for `Event.Boundary`. Fires the `TrespassStateChange` GUI event and flips `oSelf.bTrespassing` only when the state actually changes: on `sAction == "enter"` while not already trespassing, or `sAction == "exit"` while currently trespassing (guarded by `if not (sAction ~= "enter" or oSelf.bTrespassing) or sAction == "exit" and oSelf.bTrespassing then`) — repeated "enter" events while already trespassing (or "exit" while not) are no-ops.

### `Enable(oSelf)`
Enables the faction zone by calling `Hud.Radar:AddLineRegion` and `Pda.Map:AddLineRegion` with a dark-red region (`nRed=64, nGreen=0, nBlue=0, nAlpha=160`) keyed by `uGuid`. Sets up a persistent `Event.Boundary` listener (`Player.GetLocalCharacter()`, `oSelf.uGuid`, `"any"`, `false`) calling `BoundaryCallback`, and sets `bActive = true`.

### `Disable(oSelf)`
Disables the faction zone by calling `Hud.Radar:RemoveLineRegion`/`Pda.Map:RemoveLineRegion` (keyed by `uGuid` only), deletes `BoundaryEvent`, sends a final `TrespassStateChange` (`bTrespassing = false`) event if `bTrespassing` was set, and clears `bActive` (sets it to `nil`, not `false`).

## Events
- Listens for `Event.Boundary` (via `Event.CreatePersistent`) to call `BoundaryCallback` when a player enters or exits the faction zone boundary.
- Sends `TrespassStateChange` as a GUI event payload via `MrxGui.SendEvent` (not an `Event.*` engine constant) on state changes in `BoundaryCallback` and on forced-false in `Disable`.

## Module constants & tunables
- Region colour (radar + PDA line region): `nRed = 64, nGreen = 0, nBlue = 0, nAlpha = 160` — a translucent
  dark red. Change these in `Enable`'s `tRegionParam` to recolour the zone outline.
- Faction association map (`_tAssociationMap`, hash-keyed): `Allied`→`All`, `China`→`Chi`, `Civ`→`Civ`,
  `Guerilla`→`Gur`, `OC`→`Oil`, `Pirate`→`Pir`, `PMC`→`Pmc`, `VZ`→`Vz`. The short code becomes `oSelf.sFaction`
  and is the payload of the `TrespassStateChange` event.

## Notes for modders
- `OnActivate`/`Create` happen synchronously here — there's no hibernation-wait step in this file's own `OnActivate`, unlike the more common `OnActivate` → `Event.Create(Event.ObjectHibernation, ...)` → `Awake` pattern seen elsewhere in `resident/`.
- The zone draws through [`Hud`](../namespaces/hud)`.Radar:AddLineRegion` and `Pda.Map:AddLineRegion`, and
  its faction is resolved via [`Ai`](../namespaces/ai)`.GetFactionGuid` — those are the primitives to reach
  for if you build a similar map-region prop.
- Customize the faction association by modifying `_tAssociationMap` in `Init`; remember the map is keyed by `String.GetHash(name)`, not the raw name string.
- `OnDeactivate`/`OnDeath` are not defined in this file — they come from `Inheritable`, which calls this file's `Delete` override.
- Be aware that enabling/disabling the zone affects both radar and PDA map visualizations, and that `Enable`/`Disable` are idempotent-guarded via `bActive` at the call site (`Create`/`Delete`), not inside `Enable`/`Disable` themselves.