---
title: Repairpad
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, repair]
verified: true
verified_note: 'deeper pass: re-confirmed all 4 functions + the single ObjectHibernation subscription; clarified the LightFront off→on sequence, noted MrxTutorialManager is imported-but-unused and bLightStart is a stray global; pruned vacuous modder bullets; cross-linked Vehicle/Event namespaces.'
---

# Repairpad

*Module: repairpad.lua*

## Overview
The `Repairpad` module is the tiny lifecycle script for a repair-pad object. Its whole observable
job is a light cue: when the pad wakes it briefly clears its `LightFront` vehicle part, then turns it
**on** to indicate the pad is live; on death/deactivate it clears the light again. It does not itself
implement the repairing — that is engine/vehicle behavior — it just manages the indicator light and
event cleanup.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: [`MrxTutorialManager`](mrxtutorialmanager) — imported but **not referenced** anywhere in
  this file (vestigial).

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
Turns **on** the front light (`Vehicle.SetParts(uGuid, "LightFront", true)`). Despite the name, it
registers no events — it is just the "light on" step called from the awake handler. The return is
stored in the stray global `bLightStart` (written here and in `OnActivate`, never read).

## Events
- `Event.ObjectHibernation` (in `OnActivate`) — fires the inline "awake" handler described above, keyed
  under `tEvents[uGuid].uActivate` so `OnDeactivate` can find and delete it later.
- No other `Event.*` calls exist in this file. (A previous revision of this page claimed a `HideMarker`
  custom event — that string does not appear anywhere in `repairpad.lua`; it was not present in source.)

## Notes for modders
- The visible lever here is the `"LightFront"` [`Vehicle.SetParts`](../namespaces/vehicle) part — that
  named part is the pad's indicator light. If your pad model names the light differently, this script
  won't toggle it.
- `OnDeactivate` iterates `tEvents[uGuid]` with `pairs` and `Event.Delete`s every entry, then clears
  the table — so any event you add for a given `uGuid` should be stored in that table to get cleaned up
  automatically.
- There is no repair logic, tunable, or timer in this file — it is purely the light/event-cleanup
  shell around the engine's repair-pad behavior.