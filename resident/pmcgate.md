---
title: Pmcgate
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [pmc, gate]
verified: true
verified_note: spot-checked against source (7 lines, 2 functions) — function list, event list, and inheritance claim all confirmed accurate, no changes needed
---

# Pmcgate

*Module: pmcgate.lua*

## Overview
The `Pmcgate` module is responsible for managing the activation and opening of PMC gates in the game world. It sets up a timer to open the gate after it has been activated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance tables or fields tracked.

## Functions
### `OnActivate(uGateGuid, args)`
Called when the PMC gate instance is activated. It sets up an event to call `OpenGate` once the object leaves hibernation.

### `OpenGate(uGateGuid)`
Creates a timer that triggers after 2 seconds, calling `Object.OpenGate` with the PMC gate's GUID to open it.

## Events
- Listens for `Event.ObjectHibernation` to call `OpenGate` when the object leaves hibernation.
- Listens for `Event.TimerRelative` to trigger the gate opening after a delay.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to manage the gate's activation lifecycle.
- The gate opens 2 seconds after it is activated. This delay can be adjusted by changing the timer duration in the `OpenGate` function.
- No additional customization options are provided for this module; it functions as a simple timer-based gate opener.