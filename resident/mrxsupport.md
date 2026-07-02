---
title: MrxSupport
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, economy]
---

# MrxSupport

*Module: mrxsupport.lua*

## Overview
The `MrxSupport` module is responsible for managing various support operations in the game, including designating targets, handling costs, and coordinating with other systems like anti-air defenses. It provides functionality to create, configure, and execute support actions while ensuring proper resource management and player feedback.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSupportDesignator`, `MrxSupportManager`, `MrxGui`, `MrxPmc`, and others

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator object associated with the support.
- `sDeliveryVehicle` and `uDeliveryVehicle`: Strings and GUIDs representing the delivery vehicle template name and its corresponding GUID.
- `sBomb` and `uBomb`: Strings and GUIDs representing the bomb template name and its corresponding GUID.
- `uOwner`: The GUID of the owner of the support.
- `nAircraftBlip`: A counter for aircraft blips.
- `tEvents`, `tAA`, `tVOCues`, `tLocalNetObjects`, `tRemoteNetObjects`: Tables used to manage various states, including events, anti-air systems, voice cues, and network objects.

## Functions

### Create(self, uPlayerGuid)
- **Description**: Creates a new support instance with the specified player GUID.
- **Parameters**:
  - `self`: The current support object.
  - `uPlayerGuid`: The GUID of the player who owns the support.
- **Returns**: A new support instance.

### DesignationCallback(self)
- **Description**: Placeholder function for handling designation callbacks. Currently does nothing.

### GetDesignator(self)
- **Description**: Retrieves the designator associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The designator object.

### SetDesignator(self, oDesignator)
- **Description**: Sets the designator for the support and updates its parent support reference if applicable.
- **Parameters**:
  - `self`: The current support object.
  - `oDesignator`: The new designator object to set.

### SetModuleName(self, sModuleName)
- **Description**: Sets the module name for the support.
- **Parameters**:
  - `self`: The current support object.
  - `sModuleName`: The name of the module.

### GetModuleName(self)
- **Description**: Retrieves the module name associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The module name.

### SetOwner(self, uGuid)
- **Description**: Sets the owner GUID for the support and updates the designator's owner if applicable.
- **Parameters**:
  - `self`: The current support object.
  - `uGuid`: The new owner GUID to set.

### SetFaction(self, sFactionId)
- **Description**: Sets the faction ID for the support.
- **Parameters**:
  - `self`: The current support object.
  - `sFactionId`: The faction ID to set.

### GetFaction(self)
- **Description**: Retrieves the faction ID associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The faction ID.

### GetDenialCondition(self)
- **Description**: Determines if there is a denial condition for using the support, such as AA test level or hostile faction status.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: A denial condition string if applicable, otherwise `nil`.

### GetOwner(self, uGuid)
- **Description**: Retrieves the owner GUID of the support.
- **Parameters**:
  - `self`: The current support object.
  - `uGuid`: The GUID to check (not used in the function).
- **Returns**: The owner GUID.

### SetRecruit(self, sRecruit)
- **Description**: Sets the recruit type for the support.
- **Parameters**:
  - `self`: The current support object.
  - `sRecruit`: The recruit type to set.

### GetRecruit(self)
- **Description**: Retrieves the recruit type associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The recruit type.

### GetElapsedCooldownTime(self)
- **Description**: Retrieves the elapsed cooldown time for the support's recruit if it is in a denial condition related to rearming.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The elapsed cooldown time or `nil` if not applicable.

### SetSupportName(self, sSupportName)
- **Description**: Sets the name of the support.
- **Parameters**:
  - `self`: The current support object.
  - `sSupportName`: The name to set.

### GetSupportName(self)
- **Description**: Retrieves the name of the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The support name.

### SetFuelCost(self, nFuelCost)
- **Description**: Sets the fuel cost for using the support.
- **Parameters**:
  - `self`: The current support object.
  - `nFuelCost`: The fuel cost to set.

### GetFuelCost(self)
- **Description**: Retrieves the fuel cost associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The fuel cost.

### SetCashCost(self, nCashCost)
- **Description**: Sets the cash cost for using the support.
- **Parameters**:
  - `self`: The current support object.
  - `nCashCost`: The cash cost to set.

### GetCashCost(self)
- **Description**: Retrieves the cash cost associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The cash cost.

### ShouldSuppressIconAnimationOnDirectUse(self)
- **Description**: Determines if the icon animation should be suppressed when using the support directly.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: A boolean indicating whether to suppress the icon animation.

### SetVOCues(self, tVOCues)
- **Description**: Sets the voice cues for the support.
- **Parameters**:
  - `self`: The current support object.
  - `tVOCues`: A table of voice cue names.

### GetVOCues(self)
- **Description**: Retrieves the voice cues associated with the support.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The table of voice cues.

### PlayRandomVOCue(tVOCues, bSendNetEvent)
- **Description**: Plays a random voice cue from the provided list and optionally sends a network event.
- **Parameters**:
  - `tVOCues`: A table of voice cue names.
  - `bSendNetEvent`: A boolean indicating whether to send a network event.

### BeginSupportSequence(self)
- **Description**: Initiates the support sequence, consuming fuel, cash, or freebies as necessary and sending relevant events.
- **Parameters**:
  - `self`: The current support object.
- **Returns**: The result of the designation callback.

### Configure(self, tOptions)
- **Description**: Configures the support with the provided options, updating fields if they exist.
- **Parameters**:
  - `self`: The current support object.
  - `tOptions`: A table of configuration options.

### Commence(self, bFireImmediately)
- **Description**: Commences the support action, checking for necessary conditions and starting the sequence if applicable.
- **Parameters**:
  - `self`: The current support object.
  - `bFireImmediately`: A boolean indicating whether to fire immediately.
- **Returns**: A boolean indicating success or failure.

### BlipAircraft(uAircraft, tColor, bSticky, sTexture)
- **Description**: Adds a radar blip for an aircraft with the specified color, stickiness, and texture.
- **Parameters**:
  - `uAircraft`: The GUID of the aircraft to blip.
  - `tColor`: A table representing the RGB color values.
  - `bSticky`: A boolean indicating whether the blip should be sticky.
  - `sTexture`: The texture name for the blip.

### _RemoveBlipCallback(sBlipName, bDelete)
- **Description**: Removes a radar blip and optionally deletes the associated object if applicable.
- **Parameters**:
  - `sBlipName`: The name of the blip to remove.
  - `bDelete`: A boolean indicating whether to delete the associated object.

### AddAntiAir(uGuid, sLevel)
- **Description**: Adds an anti-air system with the specified GUID and level.
- **Parameters**:
  - `uGuid`: The GUID of the anti-air system.
  - `sLevel`: The level of the anti-air system (e.g., "basic", "medium").

### RemoveAntiAir(uGuid)
- **Description**: Removes an anti-air system with the specified GUID.
- **Parameters**:
  - `uGuid`: The GUID of the anti-air system to remove.

### TestAALevel(sLevel)
- **Description**: Tests if there is an active anti-air system at the specified level or higher.
- **Parameters**:
  - `sLevel`: The level to test (e.g., "basic", "medium").
- **Returns**: The level of the active anti-air system or `nil` if none are found.

### DenialMessage(sReason)
- **Description**: Displays a denial message based on the specified reason and plays a corresponding voice cue.
- **Parameters**:
  - `sReason`: The reason for the denial (e.g., "aa", "jammer").

### SynchNetImportModule(sModule)
- **Description**: Dynamically imports a network module.
- **Parameters**:
  - `sModule`: The name of the module to import.

### SynchNetAction(oModule, uModule, fX, fY, fZ, uDesignatorGuid, uTarget, uOwnerGuid, uCargo, uFinalDestination, uDeliveryVehicle, uSetBomb, bEventPost)
- **Description**: Synchronizes a network action for the support, setting various parameters and posting events if applicable.
- **Parameters**:
  - `oModule`: The module object.
  - `uModule`: The GUID of the module.
  - `fX`, `fY`, `fZ`: Coordinates for the designation.
  - `uDesignatorGuid`: The GUID of the designator.
  - `uTarget`: The target GUID.
  - `uOwnerGuid`: The owner's GUID.
  - `uCargo`: The cargo GUID.
  - `uFinalDestination`: The final destination GUID.
  - `uDeliveryVehicle`: The delivery vehicle GUID.
  - `uSetBomb`: The bomb GUID to set.
  - `bEventPost`: A boolean indicating whether to post an event.

### SynchNetAddItem(oModule, uModule, aName, aIcon, aLitIcon)
- **Description**: Adds an item to the support menu via the network, creating a local object if necessary and opening the menu.
- **Parameters**:
  - `oModule`: The module object.
  - `uModule`: The GUID of the module.
  - `aName`: The name of the item.
  - `aIcon`: The icon for the item.
  - `aLitIcon`: The lit icon for the item.

### SynchNetRemoveItem(aName)
- **Description**: Removes an item from the support menu via the network.
- **Parameters**:
  - `aName`: The name of the item to remove.

### SetDeliveryVehicle(self, sVehicleTemplateName)
- **Description**: Sets the delivery vehicle template for the support.
- **Parameters**:
  - `self`: The current support object.
  - `sVehicleTemplateName`: The name of the vehicle template.

### SetBomb(self, sBombTemplateName)
- **Description**: Sets the bomb template for the support.
- **Parameters**:
  - `self`: The current support object.
  - `sBombTemplateName`: The name of the bomb template.

### RefundCosts(self)
Refunds the costs associated with a support operation. If fuel, stockpile, or freebie resources were consumed during the operation, they are added back to the player's inventory.

### SetupDamageEvent(self, uHeli, bCompleted)
Sets up an event listener for damage on the specified helicopter (`uHeli`). If the recruit type is "Copter", it listens for a "RecruitAvailable" event and triggers a fade-out if the recruit becomes available. It also sets up an event to abort support if the helicopter's health drops below 60%.

### Abort(self, uHeli, sReason)
Aborts the support operation for the specified helicopter (`uHeli`). If no reason is provided and the support was not completed, it displays a message box indicating that the copter was damaged. If the reason is "NoMunitions", it displays a different message box. It then plays a random voice-over cue based on the faction of the helicopter and applies a penalty to the player's cash if the faction is PMC. Finally, it calls `GoHome` to return the helicopter home.

### SetupPilotKilledEvent(self, uHeli, bCompleted)
Sets up an event listener for the death of the pilot of the specified helicopter (`uHeli`). When the pilot dies or is hijacked, it triggers the `Abandon` function.

### Abandon(self, uHeli)
Handles the abandonment of a support operation when the pilot of the specified helicopter (`uHeli`) is killed or hijacked. It detaches any cargo from the winch and marks the support as complete. If the faction is PMC, it calculates a penalty to the player's cash. Finally, it makes the recruit available again.

### GoHome(self, uGuid, uWinchedGuid)
Handles the return of the specified helicopter (`uGuid`) home after a support operation. It detaches any cargo from the winch and marks the support as complete. It then determines the landing zone based on the faction of the helicopter and sets up an AI goal for the driver to move there. If the landing zone is not found, it falls back to a random location. Once the helicopter reaches its target, it calls `Land` to land the helicopter.

### Land(self, uGuid, nTargetX, nTargetY, nTargetZ, uWinchedGuid)
Handles the landing of the specified helicopter (`uGuid`) at the target coordinates (`nTargetX`, `nTargetY`, `nTargetZ`). If there is a winched object (`uWinchedGuid`), it fades out the winched object. It then sets up an AI goal for the driver to land the helicopter and calls `FadeOut` when the landing is complete.

### FadeOut(uGuid, nState)
Fades out the specified helicopter (`uGuid`) and its driver if they are not marked as "Hero". It detaches any cargo from the winch, deploys the vehicle as a passenger, and fades out both the helicopter and its driver.

### PlayAirstrikeVO(uJet, sMisha)
Plays a voice-over cue for an incoming airstrike based on the faction of the specified jet (`uJet`). The voice-over cue is selected randomly from a predefined list for each faction. If no cue is found for the faction, it logs a debug message.

### GetSpawnHeight()
Returns the spawn height for a support operation. If the player has a secondary character, the height is set to 250; otherwise, it is set to 50.

## Events

- **Event.ObjectHibernation**: Listens for this event to wake up and initialize the support instance.
- **Event.ObjectDeath**: Listens for this event to handle the death of a support-related object (e.g., helicopter).
- **Event.PlayerJoined / Event.PlayerLeft**: Listens for these events to manage player-specific state or resources.
- **Event.TimerRelative**: Used for various timed actions, such as cooldowns or delays in support operations.
- **Event.NetAction**: Listens for network actions related to support operations and synchronizes them across clients.

## Notes for modders

1. **Call-order requirements**:
   - Ensure that `OnActivate` is called before any other lifecycle functions like `Awake`, `OnDeactivate`, etc., as it sets up the initial state of the support instance.
   - The sequence of events (e.g., `BeginSupportSequence`, `Commence`) should be respected to maintain proper operation flow.

2. **Pitfalls**:
   - Be cautious with resource management functions like `RefundCosts` and `Abort` to avoid unintended consequences, such as over-refunding or excessive penalties.
   - Ensure that event listeners are properly removed when they are no longer needed to prevent memory leaks or unexpected behavior.

3. **Tunables**:
   - The fuel cost (`SetFuelCost`), cash cost (`SetCashCost`), and other resource costs can be adjusted to balance the game economy.
   - Voice-over cues (`SetVOCues`, `PlayRandomVOCue`) can be customized to enhance immersion or localization.

4. **Decompiler artifacts**:
   - Unused local variables like `oDesignator` in `Create(self, uPlayerGuid)` are decompiler artifacts and should not affect the functionality of the module.
   - Duplicate table keys in literals (e.g., `tEvents`, `tAA`) are handled correctly by Lua but may appear redundant in the decompiled code.