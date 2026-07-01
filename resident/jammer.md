---
title: Jammer
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, support]
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
Called when the object instance is activated. It sets up an event to call `SetupActivationEvents` once the object leaves hibernation.

### `OnDeactivate(uGuid)`
Called when the object instance is deactivated. It cleans up any registered events and removes anti-air support.

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
Called when the object instance dies. It removes anti-air support.

## Events
- Listens for `Event.ObjectHibernation` to call `SetupActivationEvents` when the object leaves hibernation.
- Listens for `Event.ContextAction` to handle the use of the alarm and trigger either `AlarmActivated` or `AlarmDeactivated`.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the jammer's lifecycle.
- Customize animations and vehicle parts behavior by modifying the animation names and part settings in the functions.
- Be aware that adding and removing anti-air support (`MrxSupport.AddAntiAir` and `MrxSupport.RemoveAntiAir`) may affect gameplay mechanics.