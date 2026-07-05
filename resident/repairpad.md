---
title: Repairpad
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, repair]
verified: true
verified_note: fixed OnActivate description (callback is an inline anonymous function, not a named Awake — no Awake function exists in this file) and removed fabricated HideMarker event claim (not present in source)
---

# Repairpad

*Module: repairpad.lua*

## Overview
The `Repairpad` module manages the activation and deactivation of repair pads in the game world. It handles events related to the pad's lifecycle, such as when it is activated, deactivated, or destroyed. The module also controls the visual state of the repair pad by toggling its front light.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxTutorialManager`

## Instance pattern
This is a stateless manager/utility module with no per-instance tables. It tracks events associated with each repair pad using the `tEvents` table, keyed by `uGuid`.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the repair pad instance is activated. Registers `tEvents[uGuid].uActivate`, an
`Event.ObjectHibernation` handler for `{uGuid, "awake"}`. Unlike most `OnActivate` implementations in this
codebase, the handler is an **inline anonymous function** defined right at the call site, not a separate
named `Awake` — there is no `Awake` function anywhere in this file. That anonymous function turns off the
`LightFront` vehicle part (`Vehicle.SetParts(uGuid, "LightFront", false)`) and calls
`SetupActivationEvents(uGuid)`.

### `OnDeactivate(uGuid)`
Called when the repair pad instance is deactivated. Deletes all associated events and clears the entry in the `tEvents` table.

### `OnDeath(uGuid)`
Called when the repair pad's underlying object dies. Turns off the front light and calls `OnDeactivate`.

### `SetupActivationEvents(uGuid)`
Sets up activation events for the repair pad, including turning on the front light.

## Events
- `Event.ObjectHibernation` (in `OnActivate`) — fires the inline "awake" handler described above, keyed
  under `tEvents[uGuid].uActivate` so `OnDeactivate` can find and delete it later.
- No other `Event.*` calls exist in this file. (A previous revision of this page claimed a `HideMarker`
  custom event — that string does not appear anywhere in `repairpad.lua`; it was not present in source.)

## Notes for modders
- Ensure that `OnActivate`, `OnDeactivate`, and `OnDeath` are called appropriately to manage the repair pad's lifecycle.
- The front light of the repair pad can be controlled using `Vehicle.SetParts`.
- `OnDeactivate` iterates `tEvents[uGuid]` with `pairs` and calls `Event.Delete` on every entry, then clears the table — so any event you add for a given `uGuid` should be stored in that table to get cleaned up automatically.