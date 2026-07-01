---
title: FriendlyGate
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [ai, gate]
---

# FriendlyGate

*Module: friendlygate.lua*

## Overview
The `FriendlyGate` module manages the behavior of gates that open based on proximity to friendly or allied vehicles. It checks for nearby valid candidates (hero or faction-vehicles) and opens if any are present and not locked, with attitude-gated conditions for the player. The gate also has a far-edge re-check at 40m.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxFactionManager`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tLockedGates`: A table to store locked gate GUIDs.
- `_tGates`: A table to manage gate-specific data, including proximity events, attitude change events, candidate vehicles, and filter settings.

## Functions
### `Init()`
Initializes the module. Currently does nothing.

### `Deinit()`
Deinitializes the module. Currently does nothing.

### `LockGate(uGateGuid, bLock)`
Sets or clears a gate's lock state in `_tLockedGates`. If the gate is already registered, it evaluates candidates again.

### `IsGateLocked(uGateGuid)`
Checks if a gate is locked by looking up its GUID in `_tLockedGates`.

### `OnActivate(uGateGuid)`
Called when the gate instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGateGuid)`
Initializes the gate's behavior, including setting lights and creating proximity and attitude change events. It also registers death events for specific parts of the gate.

### `OnDeath(uGateGuid, uNodeGuid)`
Handles the gate's death by calling `OnDeactivate`.

### `OnDeactivate(uGateGuid)`
Cleans up all events and data associated with the gate when it is deactivated.

### `CreateProxEvent(uFilter, uGateGuid)`
Creates a proximity event for the gate to detect nearby vehicles within 20m.

### `_EvaluateCandidates(uGateGuid, bApproaching, vObjects)`
Evaluates candidate vehicles approaching or leaving the gate's proximity. It updates the list of candidates and opens/closes the gate based on conditions.

### `_RemoveCandidate(uGateGuid, uGuid)`
Removes a vehicle from the list of candidates by deleting associated events.

### `_ChangeState(uGateGuid, bOpen)`
Changes the open state of the gate, playing a voice-over if it opens for the first time and updating lights accordingly.

### `_TestAttitude(sGateFaction, uPlayerCharGuid)`
Tests the attitude between the gate's faction and the player character to determine if the gate should open.

### `SaveSingleton()`
Saves the current state of locked gates.

### `LoadSingleton(tLockedGates)`
Loads the saved state of locked gates.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the gate leaves hibernation.
- Listens for proximity events (`Event.ObjectProximity`) to evaluate candidates approaching or leaving the gate's radius.
- Listens for attitude change events (`MrxFactionManager.CreatePersistentAttitudeChangeEvent`) to re-evaluate candidates based on faction attitudes.
- Listens for death events (`Event.ObjectDeath`) to remove dead vehicles from candidate lists.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage gate lifecycle.
- Use `LockGate` to control the lock state of gates.
- Customize faction behavior by modifying the `_tFactions` table or adjusting attitude checks in `_TestAttitude`.
- Be aware that network synchronization may affect multiplayer behavior, especially with attitude changes and proximity events.