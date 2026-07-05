---
title: MrxShootingGallery
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mission, player]
verified: true
verified_note: Events section was missing 3 real Event.* constants (ObjectHibernation, Boundary, WeaponEvent) actually referenced in source; expanded with accurate handle names and filter args, rest of page confirmed accurate.
---

# MrxShootingGallery

*Module: mrxshootinggallery.lua*

## Overview
The `MrxShootingGallery` module manages a shooting gallery mission scenario. It handles the removal and return of weapons for players, sets up boundary events to control player movement within a designated area, and manages firelock states to restrict weapon usage outside the boundary.

## Inheritance
- Inherits from: `none`
- Imports: `MrxSubtitle`, `MrxVoSequence`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but rather provides functions to manage player weapons and mission boundaries.

## Functions
### `RemoveWeapons(uPlayer)`
Removes all weapons from the specified player's inventory, disables their physics, and drops them at a slightly lower position. Returns a table of removed weapons.

### `ReturnWeapons(uPlayer, tWeapons)`
Returns the previously removed weapons to the specified player's inventory, re-enables weapon usage, and equips the weapons in the correct order.

### `ClearEvents()`
Deletes all registered events related to the shooting gallery mission, ensuring no lingering event handlers remain.

### `Reset()`
Resets the firelock states for both primary and secondary characters and clears any existing events. This function is called when resetting the mission state.

### `NetSafeSetupBorder(uBorderName)`
Sets up the border for the shooting gallery on the client side if the player is not local. It creates an event to call `SetupBorder` when the game state changes to "WaitForTether".

### `SetupClientBorder(uBorderName)`
Sets up boundary events for the secondary character on the client side. This function ensures that firelock states are managed correctly when the player exits or enters the designated area.

### `SetupBorder(uBorderName)`
Sets up the shooting gallery border on both server and client sides. It configures firelock states, creates boundary events, and handles player join events to ensure proper mission setup.

### `SteppedOut(uChar, uBorderName)`
Called when a character exits the designated boundary area. This function sets the firelock state to true for the character and starts a voice sequence warning about restricted weapon usage. Contains an empty `if Player.GetLocalCharacter() == uChar then end` block with no body — likely lost/stripped logic from decompilation, has no effect either way.

### `SteppedIn(uChar, uBorderName)`
Called when a character enters the designated boundary area. This function sets the firelock state to false for the character and re-creates boundary events to manage further transitions.

## Events
- `Event.GameStateChange` filtered on `"WaitForTether", "exit"` (via `NetSafeSetupBorder`, handle `_evNetSafeSetupBorder`) — re-runs `SetupBorder(uBorderName)` once the tether wait state exits, client-only (`Net.IsClient()` gate).
- `Event.ObjectHibernation` filtered on `"awake"` (via `SetupClientBorder`) — one-shot, waits for the secondary character to wake before wiring up `_BorderEventP2`.
- `Event.ScriptEvent` named `"mpPlayerJoin"` (persistent, via `SetupBorder`, handle `_evPlayerJoined`) — guarded to only fire when `Net.IsServer()` and the joining player is not local; calls `SetupClientBorder`.
- `Event.Boundary` (via `SetupBorder`/`SteppedOut`/`SteppedIn`, handles `_BorderEventP1`/`_BorderEventP2`) — fires on `"exit"`/`"enter"` of `uBorderName` for the primary/secondary character; `SteppedOut` and `SteppedIn` re-create each other's opposite-direction listener every time they fire, forming a ping-pong chain.
- `Event.WeaponEvent` filtered on `"FireLock"` for the primary weapon (via `SteppedOut`, handle `uFireLockVO`) — triggers `MrxVoSequence.Start` with the VO line `"Fiona-In-Mission-MinorContract-Pmc31-08"` when the locked weapon is fired.

## Notes for modders
- Ensure that `Reset()` is called appropriately to clear any existing mission state before starting a new shooting gallery mission.
- Use `RemoveWeapons` and `ReturnWeapons` to manage player weapons during the mission.
- Customize firelock states by setting appropriate values in the `Human.SetFireLock` function calls.
- Be aware of network synchronization issues when managing client-side events, especially in multiplayer scenarios.