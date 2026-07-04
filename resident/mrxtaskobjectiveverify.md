---
title: MrxTaskObjectiveVerify
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective, verification]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskObjective](mrxtaskobjective) for the general mechanism.
---

# MrxTaskObjectiveVerify

*Module: mrxtaskobjectiveverify.lua*

## Overview
The `MrxTaskObjectiveVerify` module is responsible for handling the verification process of a high-value target (HVT) in the game. It manages various events related to the HVT's state, such as being subdued, destroyed, or damaged, and coordinates the extraction process. The module also handles network synchronization for multiplayer scenarios and ensures that the correct voice-over sequences and visual effects are played during the verification process.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `none`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields:
- **NETEVENT_VERIFY**: A constant representing the network event type for verification.
- **HVTNORMAL, HVTSUBDUED, HELIDESTROYED, HELIDAMAGED, HELILANDED, HELIPILOTKILLED, HVTDEAD**: Constants representing different states of a target (High Value Target).
- **tHasExtractionFreebie**: A table to track extraction freebies.
- **tHVTDistanceEvents**: A table to manage distance events related to the High Value Targets.
- **tActiveHelicopters**: A table to keep track of active helicopters.
- **bIsVerified**: Indicates whether the target has been verified.
- **uCurrentHVT**: The GUID of the current HVT being tracked.
- **sCurrentFaction**: The faction associated with the current HVT.
- **nSupportCount**: The number of support units for the current HVT.
- **tTargetActions**: A table to manage target actions and their states.

## Functions

### Activated(self)
Initializes the module when activated. Sets up various event listeners for target death, proximity, and state transitions. Also handles support pickup callbacks and initializes the current HVT state.

### Cleanup(self)
Cleans up resources when the module is deactivated. Removes support pickups and calls cleanup on the base class.

### _HelicopterSpawnedCallback(oSupport, uHeli)
Handles the callback for a helicopter being spawned. Adds it to the active helicopters table and sets up an event to remove it when deleted.

### _TargetIntoSubdued(self)
Updates the current HVT state to subdued if not already verified or in certain states. Shows a tutorial message if not on German SKU.

### _HelicopterDestroyedCallback(self)
Updates the current HVT state to destroyed and shows a tutorial message.

### _HelicopterDamagedCallback(self)
Updates the current HVT state to damaged and shows a tutorial message.

### _PilotKilledCallback(self)
Updates the current HVT state to pilot killed and shows a tutorial message.

### _HelicopterLandedCallback(self)
Updates the current HVT state to landed and shows a tutorial message.

### _TargetOutOfSubdued(self)
Resets the current HVT state to normal if not verified or dead, and shows a tutorial message.

### HeroProximity(self, uGuid, uHero)
Handles proximity events for heroes. Plays voice-over sequences based on the faction and updates AI states and actions accordingly.

### _TargetOnHibernate(self, uGuid)
Sets up an event listener for when the target wakes up from hibernation.

### _TargetOnAwake(self, uGuid)
Handles the target waking up from hibernation by updating its state and setting up further event listeners.

### _TargetDestroyed(self, uGuid)
Handles the destruction of a target. Processes callbacks, removes proximity events, and sets up verification if not on German SKU.

### _SetupVerify(self, uGuid)
Sets up the verification process for a destroyed target. Adds context actions and creates an event listener for the action being completed.

### NetEventCallback(nEventType, tArgs)
Handles network events. For `NETEVENT_VERIFY`, it calls `NetSafeTargetActioned`.

### _TargetActioned(self, uActioner, uGuid)
Sends a custom network event for target actioning and calls the non-network safe version.

### DoVerifyAnimation(uActioner, uGuid)
Performs the verification animation by setting positions, rotations, and disabling player input. Spawns a camera and starts an action.

### Abort(self, uActioner, FlashEvent)
Deletes the flash event to abort the verification process.

### flashAnimation()
Plays a sound cue and spawns a visual effect for the verification animation.

### NetSafeTargetActioned(uActioner, uGuid)
Performs the network-safe version of target actioning by calling `DoVerifyAnimation` and setting up an event listener for completion.

### NonNetSafeTargetActioned(self, uActioner, uGuid)
Performs the non-network safe version of target actioning by calling `DoVerifyAnimation`, removing context actions, and setting up an event listener for completion.

### _TargetActionedComplete(self, uGuid, uActioner, uCamera, nOldHealth)
Completes the target actioning process. Updates verification status, processes callbacks, and cleans up resources.

### NetSafeTargetActionedComplete(uActioner, uCamera, nOldHealth)
Handles the network-safe completion of target actioning by cleaning up resources.

### _TargetBashed(self, uGuid)
Handles the bashing of a target. Updates its state, shows a tutorial message, and sets up an event listener for subduing.

### _tSubduedVO
A table containing voice-over sequences for different factions when a target is subdued.

### `_TargetSubdued(self, uGuid)`
Handles the event when a target is subdued. It performs several actions:
- Marks the target as subdued.
- Removes any context action associated with the target.
- Retrieves and processes the faction of the target.
- Adds an infraction to the player's primary and secondary characters if they exist.
- Checks if the game SKU is German and, if so, censors a message and proceeds to extract the target.
- Otherwise, adds a context action for carrying the target and sets up support extraction events.
- Processes any callback functions defined in the configuration for when a target is subdued.

### `_TargetExtracted(self, uGuid)`
Handles the event when a target is extracted. It performs several actions:
- Marks the objective as verified.
- Clears the current HVT state.
- Hides any tutorial messages.
- Updates the verification manager with the extraction status of the target.
- Removes the target if it's a userdata type.
- Deletes any stow events associated with the target and removes support.
- Completes the part of the objective.
- Fades out the target object.

### `_SetHostileAttitudeChangeEvent(self, uGuid, sFaction)`
Sets up an event to handle changes in hostile attitude towards the PMC faction. It performs several actions:
- Iterates through active helicopters and sends them home.
- Removes any freebie support for the current faction.
- Deletes any existing attitude change event.
- Creates a new persistent attitude change event that triggers when the faction's attitude towards the PMC becomes non-hostile, adding support and setting up a non-hostile attitude change event.

### `_SetNonHostileAttitudeChangeEvent(self, uGuid, sFaction)`
Sets up an event to handle changes in non-hostile attitude towards the PMC faction. It performs several actions:
- Adds freebie support for the current faction.
- Deletes any existing attitude change event.
- Creates a new persistent attitude change event that triggers when the faction's attitude towards the PMC becomes hostile, removing support and setting up a hostile attitude change event.

### `_AddSupport(self, uGuid)`
Adds support for a target. It performs several actions:
- Increments the support count.
- Deletes any existing distance events associated with the target.
- If this is the first support being added, it adds freebie support for the current faction and creates a distance event for the target.

### `_RemoveSupport(self, uGuid)`
Removes support for a target. It performs several actions:
- Decrements the support count to a minimum of 0.
- Deletes any existing distance events associated with the target.
- If all support has been removed, it deletes any attitude change event, sends active helicopters home, removes freebie support for the current faction, and clears the extraction freebie flag.

### `_GetSupportByFaction(sFaction)`
Retrieves the support type based on the faction. It returns a predefined support type or defaults to "Extraction_PMC" if the faction is not recognized.

### `SendPlayerJoinEvents()`
Sends player join events for factions that have extraction support. It performs several actions:
- Checks if the current session is a server.
- Iterates through factions with extraction support and adds freebie support for each faction.

### `_GetShortDescription()`
Returns a short description of the objective, which is "[Generic.ObjectiveVerify]".

### `GetInlineIcon(self)`
Retrieves the inline icon for the objective based on whether it's optional or not. It returns either "[objverify2]" for optional objectives or "[objverify]" for mandatory ones.

### `_GetJust2DCheckNeeded()`
Returns a boolean indicating whether just a 2D check is needed, which is always `true`.

### `_GetTargetRadarIcon()`
Retrieves the radar icon for the target, which is "objective_verify".

### `_GetTargetPdaIcon(bOptional)`
Retrieves the PDA icon for the target based on whether it's optional or not. It returns either "icon_verify_2_mc" for optional targets or "icon_verify_1_mc" for mandatory ones.

### `_GetTargetGameSpaceIcon()`
Retrieves the game space icon for the target, which is "HUD_objective_verify".

### `_IsValidTarget(uGuid)`
Checks if a given GUID represents a valid target. It returns `true` if the GUID matches any player character or if the object is alive.

### `_CreateDistanceEvent(self, uGuid)`
Creates a distance event for a target to monitor proximity. It sets up an event that triggers when the player gets too far from the target.

### `_OnHVTOutOfRange(self, uGuid)`
Handles the event when the player gets too far from the HVT. It performs several actions:
- Removes support for the target.
- Creates a new distance event that triggers when the player gets closer to the target, adding support again.

## Events

- **`Event.ObjectDeath`**: Listens for the death of an object and calls `_TargetDestroyed`.
- **`Event.ObjectProximity`**: Listens for proximity events with heroes and calls `HeroProximity`.
- **`Event.ObjectHibernate`**: Listens for objects waking up from hibernation and calls `_TargetOnAwake`.
- **`Event.HelicopterSpawned`**: Listens for helicopters being spawned and calls `_HelicopterSpawnedCallback`.
- **`Event.HelicopterDestroyed`**: Listens for helicopters being destroyed and calls `_HelicopterDestroyedCallback`.
- **`Event.HelicopterDamaged`**: Listens for helicopters taking damage and calls `_HelicopterDamagedCallback`.
- **`Event.PilotKilled`**: Listens for helicopter pilots being killed and calls `_PilotKilledCallback`.
- **`Event.HelicopterLanded`**: Listens for helicopters landing and calls `_HelicopterLandedCallback`.
- **`Event.TargetSubdued`**: Listens for targets being subdued and calls `_TargetSubdued`.
- **`Event.TargetExtracted`**: Listens for targets being extracted and calls `_TargetExtracted`.
- **`Event.NetEvent`**: Listens for network events and calls `NetEventCallback`.

## Notes for modders

- **Call-order requirements**: Ensure that the module is properly activated before any other operations are performed. The `Activated` function sets up necessary event listeners.
  
- **Pitfalls**: Be cautious with modifying the state of active helicopters or targets, as it can affect gameplay balance and objectives.

- **Tunables**: There are no tunable parameters exposed in this module. All behavior is hardcoded.

- **Decompiler artifacts**: The decompiler may produce unused locals or redundant operator groupings. These should be ignored unless they affect the logic of the code.