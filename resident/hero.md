---
title: Hero
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [player, survival, tutorial]
---

# Hero

*Module: hero.lua*

## Overview
The `Hero` module is responsible for managing player-specific systems such as health regeneration, survival mode, inventory setup, and transfer system. It also handles tutorial messages and disables the grappling hook trigger.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxSound`, `MrxTutorialManager`, `MrxUtil`, `MrxVoSequence`, `MrxPmc`, `WifEquipmentData`, `MrxParkingLotManager`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `tEvent`: A table to store event handles for each player.
- `nInitialDelay`, `nSurvivalDelay`, `nHealingFactor`, `nVehicleFactor`, `nTic`, `nMinTic`: Constants for health regeneration and survival mode settings.
- `bSurvivalMode`: A boolean table indicating if the player is in survival mode.
- `bSeeingRed`: A boolean table indicating if the player is seeing red (likely related to health).
- `nSurvivalThreshold`, `nSurvivalCooldown`, `nSurvivalAlpha`, `nMinTimeScale`, `nMaxTimeScale`: Constants for survival mode thresholds and time scaling.

## Functions
### `Init()`
Initializes the parking lot manager by calling `MrxParkingLotManager.Setup()`.

### `Deinit()`
Cleans up the parking lot manager by calling `MrxParkingLotManager.Cleanup()`.

### `OnActivate(uGuid)`
Called when a world object instance is activated. It sets up an event to call `Activate` once the object leaves hibernation.

### `Activate(uGuid)`
Activates the hero system for the player controlled by the given `uGuid`. Sets up survival mode, inventory, and transfer system if the player is local. Also configures pickup markers.

### `OnDeath(uGuid)`
Handles the death event of a player-controlled object. Cleans up survival mode and ends it if necessary.

### `OnDeactivate(uGuid)`
Called when a world object instance is deactivated. Saves the inventory, cleans up survival mode, and transfer system for the local player.

### `SetupInventory(uGuid)`
Sets up the inventory for the player by ensuring all weapons have their maximum reserve ammo.

### `SaveOutInventory(uGuid)`
Saves the current state of the player's inventory (currently a placeholder function).

### `HealthDropped(uGuid)`
Handles the health drop event. Creates a heal timer and manages survival mode based on the player's health.

### `Heal(uGuid)`
Regenerates the player's health over time. Adjusts healing rate if the player is in a vehicle. Ends survival mode if the player's health reaches the threshold.

### `CreateHealTimer(uGuid, nNextPulse)`
Creates a timer to trigger the next heal event for the given player.

### `CreateDropEvent(uGuid)`
Sets up an event to handle further health drops by calling `HealthDropped`.

### `CleanupSurvival(uGuid)`
Cleans up all events related to survival mode and fades out the screen.

### `CleanEvents(events)`
Deletes all events in the provided table to prevent memory leaks.

### `SetupSurvivalSystem(uPlayer, uGuid, bKickStartEvents)`
Sets up the survival system for the player. Optionally starts health drop events if `bKickStartEvents` is true.

### `SurvivalModeCallback(uPlayer, uGuid, bCallback)`
A placeholder function for handling survival mode callbacks (currently does nothing).

### `EndSurvivalMode(uPlayer, uGuid, nTime)`
Ends the survival mode for the player. Fades out the screen and resets health clamping.

### `StartSurvivalMode(uPlayer, uGuid, bCallback)`
Starts the survival mode for the player. Fades in the screen to red and sets up a cooldown timer.

### `SurvivalCooldownEnded(uPlayer, uGuid)`
Handles the end of the survival cooldown. Sets the player invincible, clamps health, and starts healing.

### `SetTimeScale(uPlayer, uGuid)`
Adjusts the game time scale based on the player's health (currently disabled).

### `SetupTransferSystem(uGuid)`
Sets up the transfer system for the player to allow entering vehicles as passengers.

### `CleanupTransferSystem(uGuid)`
Cleans up the transfer system when no players are using it.

### `EnterPassengerCallback(uGuid, uVehicle, sSeatType, uSeat)`
Handles the event of a player entering a vehicle seat. Checks conditions and transfers the player if possible.

### `GetAttribute(uGuid, sAttribute)`
Retrieves an attribute level for the given player or character. Returns a default value if no matching attribute is found.

### `HideTutorialMessage()`
Hides a tutorial message after a delay.

### `TutorialCueCallback()`
Sets up a timer to hide a tutorial message after 5 seconds.

### `DisableGrappleTriggered(uPlayerGuid)`
Disables the grappling hook trigger and shows a tutorial message if the player does not have the grappling hook equipment.

## Events
- Listens for `Event.ObjectHibernation` to call `Activate` when the object leaves hibernation.
- Listens for `Event.ObjectHealth` to handle health drops and survival mode logic.
- Listens for `Event.TimerRelative` to manage heal timers and tutorial message delays.
- Posts custom events like `SurvivalMode`, `SurvivalCooldownEnded`.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage player-specific systems.
- Customize health regeneration settings by adjusting constants like `nHealingFactor` and `nVehicleFactor`.
- Use the transfer system to allow players to enter vehicles as passengers.
- Be aware of tutorial message handling and disable conditions for specific equipment.