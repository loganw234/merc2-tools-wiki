---
title: Hero
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [player, survival, tutorial]
verified: true
verified_note: confirmed all 26 top-level functions and all Event.* constants against 401-line source; noted SurvivalModeCallback is dead code (zero call sites anywhere in corpus, not the undefined-callback bug pattern); added untracked globals (uRiderEvent, nRiders, _uHideMessage, CueTable) to Instance pattern
---

# Hero

*Module: hero.lua*

## Overview
The `Hero` module is responsible for managing player-specific systems such as health regeneration, survival mode, inventory setup, and transfer system. It also handles tutorial messages and disables the grappling hook trigger.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxSound`, `MrxTutorialManager`, `MrxUtil`, `MrxVoSequence`, `MrxPmc`, `WifEquipmentData`, `MrxParkingLotManager`

## Instance pattern
This is a stateless manager/utility module — no `OnActivate`→`Awake`→`Create`/`setmetatable`/`tInstance`
registry anywhere in the file (`OnActivate` here calls `Activate` directly, not a class-factory `Create`).
Per-player state lives in plain `uGuid`/`uPlayer`-keyed globals instead:
- `tEvent`: `uGuid -> {FullHealth, Timer, HealthDropped, Cooldown, nTimeScale}` — event handles per player.
- `nInitialDelay`, `nSurvivalDelay`, `nHealingFactor`, `nVehicleFactor`, `nTic`, `nMinTic`: `local`
  constants (module-file-scoped, not global) for health regeneration and survival mode timing —
  `nHealingFactor`/`nSurvivalCooldown` get multiplied by 1.5 for higher-attitude players in `Activate`.
- `bSurvivalMode`: `uPlayer -> bool`, whether that player is currently in survival mode.
- `bSeeingRed`: declared as a `local` table but never read or written anywhere else in the file — appears
  to be dead/unused state.
- `nSurvivalThreshold`, `nSurvivalCooldown`, `nSurvivalAlpha`, `nMinTimeScale`, `nMaxTimeScale`: further
  `local` constants for survival mode thresholds and time scaling (`SetTimeScale`, which would consume
  `nMinTimeScale`/`nMaxTimeScale`, immediately `return`s before using them — see below).
- Additional untracked globals not in the previous version of this page: `nRiders` and `uRiderEvent`
  (transfer-system passenger count and its single shared `Event.CreatePersistent` handle — not
  per-player, genuinely global/singleton), `_uHideMessage` (tutorial-message event handle, doubles as a
  sentinel — can hold an event handle, `nil`, or the literal string `"InValid"`), and `CueTable`
  (assigned without `local` inside `DisableGrappleTriggered`, so it leaks as a true Lua global on every
  call — maps character identity strings to VO cue names for the grapple tutorial).

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
Empty-body stub. **Confirmed dead code** — grepped the entire decompiled corpus and found zero call sites
or references to this name anywhere outside its own definition. Not the same bug pattern as a missing
callback target (nothing calls it), just unused code.

### `EndSurvivalMode(uPlayer, uGuid, nTime)`
Ends the survival mode for the player. Fades out the screen and resets health clamping.

### `StartSurvivalMode(uPlayer, uGuid, bCallback)`
Starts the survival mode for the player. Fades in the screen to red and sets up a cooldown timer.

### `SurvivalCooldownEnded(uPlayer, uGuid)`
Handles the end of the survival cooldown. Sets the player invincible, clamps health, and starts healing.

### `SetTimeScale(uPlayer, uGuid)`
Opens with `do return end` — an unconditional early-exit that makes the rest of the function body
(computing a health-based time scale and calling `Sys.SetTimeScale`) permanently unreachable dead code.
Confirmed no other function in this file calls `SetTimeScale` either, so this is fully disabled/orphaned
in the current build.

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