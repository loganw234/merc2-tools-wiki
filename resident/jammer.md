---
title: Jammer
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, support]
verified: true
verified_note: found duplicate OnDeactivate definition (second silently overrides first, shadowing the tEvents cleanup logic); OnDeath/OnDeactivate rely on MrxSupport.RemoveAntiAir, confirmed defined; events list confirmed against source.
---

# Jammer

*Module: jammer.lua*

## Overview
The `Jammer` module represents a context-toggle GPS jammer in the game. It manages the activation and deactivation of the jammer, including its animations, vehicle parts, and anti-air support effects.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxSupport`

## Instance pattern
This is a stateless manager utility module (no per-instance table). It tracks events associated with each jammer instance in the `tEvents` table.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the object instance is activated. Initializes `tEvents[uGuid]` and sets up an event to call `SetupActivationEvents` once the object leaves hibernation.

### `OnDeactivate(uGuid)` — defined twice, second wins
**Confirmed in source, likely a bug.** This function name is defined **twice** in the file: once at
line 9 (clears `tEvents[uGuid].uActivate`/`.uDeactivate` handles and nils out `tEvents[uGuid]`) and
again at line 75 (just calls `MrxSupport.RemoveAntiAir(uGuid, "jammer")`). Lua has no function
overloading — the second `function OnDeactivate(uGuid)` silently replaces the first in the module's
global table. Only the line-75 body ever actually runs when the engine calls `OnDeactivate`; the
event-cleanup logic at lines 9-21 is dead code that can never execute. Practical effect: deactivating a
jammer never deletes its `tEvents[uGuid].uActivate`/`.uDeactivate` event handles or clears the
`tEvents[uGuid]` entry — only `OnDeath` and this second `OnDeactivate` remove anti-air status.

### `SetupActivationEvents(uGuid)`
Plays the material animation for the jammer, disables vehicle parts rotation, adds a context action for using the alarm, and sets up an event to handle the use of the alarm.

### `OnUse(uGuid)`
Called when the player uses the jammer. It deletes the activation event, plays the alarm activated animation, enables vehicle parts rotation, removes the context action, sets up deactivation events, and adds anti-air support.

### `AlarmActivated(uGuid)`
Plays the material animation for the jammer, enables vehicle parts rotation, removes the context action, sets up deactivation events, and adds anti-air support.

### `SetupDeactivationEvents(uGuid)`
Adds a context action for using the alarm and sets up an event to handle the deactivation of the alarm.

### `AlarmDeactivated(uGuid)`
Stops the sound associated with the jammer, plays a different sound cue, plays the material animation for the jammer, disables vehicle parts rotation, removes the context action, sets up activation events, deletes the deactivation event, and removes anti-air support.

### `OnDeath(uGuid)`
Called when the object instance dies. It removes anti-air support (`MrxSupport.RemoveAntiAir`).

## Events
- Listens for `Event.ObjectHibernation` to call `SetupActivationEvents` when the object leaves hibernation.
- Listens for `Event.ContextAction` (twice, via different handles) to call `OnUse` when first designated as
  "in use", and later `AlarmDeactivated` once the alarm is active — both wired through
  `Pg.AddContextAction`/context-action prompts rather than a raw player-input event.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the jammer's lifecycle.
- **Be aware of the duplicate `OnDeactivate` definition** (see Functions above) — only the second one in
  file order (anti-air removal only) is reachable; the `tEvents` cleanup body earlier in the file never runs.
- Customize animations and vehicle parts behavior by modifying the animation names and part settings in the functions.
- Be aware that adding and removing anti-air support (`MrxSupport.AddAntiAir` and `MrxSupport.RemoveAntiAir`) may affect gameplay mechanics.