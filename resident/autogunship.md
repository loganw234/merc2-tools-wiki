---
title: Autogunship
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [vehicle, ai]
---

# Autogunship

*Module: autogunship.lua*

## Overview
The `Autogunship` module represents an AI-controlled gunship that targets and attacks ground vehicles. It manages the gunship's blip on the radar, its targeting logic, and missile firing behavior.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tColor`: The color of the radar blip based on faction relation.
- `uLastTarget`: The last target selected for missile salvo.

## Functions
### `OnActivate(uGuid)`
Called when the gunship instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Creates a new per-instance table for the gunship using the module's prototype. It determines the faction relation of the gunship and sets its blip color accordingly. If the gunship has the "PMC" label, it makes it unkillable. It then adds a radar blip and schedules the first missile salvo after 3 seconds.

### `Salvo(uGuid)`
Handles the logic for launching a salvo of missiles. It collects ground vehicles within a 200m radius around the player's position, selects a valid target based on faction labels, and fires 4 missiles at 0.25-second intervals. After each salvo, it schedules the next one after another 3 seconds.

### `LaunchMissile(uGuid, uTarget)`
Fires a single missile towards the specified target. It calculates the normalized direction vector from the gunship to the target with ±5 aim scatter, plays sound and particle effects, and spawns the missile with a speed of 100.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for custom event `Salvo` to handle missile salvo logic.
- Listens for custom event `LaunchMissile` to fire individual missiles.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the gunship's lifecycle.
- Customize blip colors by modifying the `tColorAlly`, `tColorNeutral`, and `tColorEnemy` fields.
- Adjust the missile salvo interval and target selection logic as needed for different gameplay scenarios.
- Be aware that making the gunship unkillable (`Object.SetUnkillable`) may affect player experience.