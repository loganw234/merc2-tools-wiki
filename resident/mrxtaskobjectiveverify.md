---
title: MrxTaskObjectiveVerify
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective, verification]
verified: true
verified_note: deeper pass — REPLACED a fabricated Events section (Event.HelicopterSpawned/Destroyed/Damaged/PilotKilled/Landed/TargetSubdued/TargetExtracted/NetEvent do NOT exist; heli states arrive via oSupport:SetHeli*CB callbacks) with the real events (ObjectDeath/ObjectProximity/HumanStateTransition/ObjectHibernation/ContextAction/ObjectInSeat/HumanActionComplete/TimerRelative/ScriptEvent/ObjectDelete + MrxFactionManager attitude event); corrected imports (7 modules, not "none"); trimmed non-existent instance fields
---

# MrxTaskObjectiveVerify

*Module: mrxtaskobjectiveverify.lua*

## Overview
The `MrxTaskObjectiveVerify` module is responsible for handling the verification process of a high-value target (HVT) in the game. It manages various events related to the HVT's state, such as being subdued, destroyed, or damaged, and coordinates the extraction process. The module also handles network synchronization for multiplayer scenarios and ensures that the correct voice-over sequences and visual effects are played during the verification process.

## Inheritance
- Inherits from: [`MrxTaskObjective`](mrxtaskobjective)
- Imports: `MrxUtil`, [`MrxSupportData`](mrxsupportdata), [`MrxTutorialManager`](mrxtutorialmanager),
  [`MrxVerifyManager`](mrxverifymanager), [`MrxVoSequence`](mrxvosequence),
  [`MrxFactionManager`](mrxfactionmanager), [`MrxSupportPickup`](mrxsupportpickup)

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page). Real per-instance fields:
- `self.nCurrHVTState` — the HVT state machine value (one of the `HVT*`/`HELI*` constants below).
- `self._bIsVerified` / `self._bIsDead` — has the target been verified / has it died.
- `self._nSupportCount` — reference count of extraction-support grants (drives the freebie on/off).
- `self._AttitudeChangeEvent` — handle for the faction-attitude event (from
  [`MrxFactionManager`](mrxfactionmanager)).

### Module-level constants & tables (NOT per-instance)
- `NETEVENT_VERIFY = 0` — custom-net event id.
- `HVTNORMAL=1, HVTSUBDUED=2, HELIDESTROYED=3, HELIDAMAGED=4, HELILANDED=5, HELIPILOTKILLED=6, HVTDEAD=7`
  — the target-state enum (these are `local` to the module).
- `tHasExtractionFreebie`, `tHVTDistanceEvents`, `tActiveHelicopters` — **module-level shared tables**
  (globals), not per-objective state — a second concurrent verify objective shares them.
- `_tSubduedVO` — per-faction voice-cue lists played when a target is subdued.

{: .note }
> The previous page listed `uCurrentHVT`, `sCurrentFaction`, `tTargetActions` as fields — **none exist** in
> the source; they've been removed.

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
Real `Event.*` subscriptions (created across `Activated`, `_SetupVerify`, `_TargetBashed`, `_TargetSubdued`,
`_TargetOnHibernate`, and the distance helpers):
- **`Event.ObjectDeath`** (persistent, on target filter) → `_TargetDestroyed`.
- **`Event.ObjectProximity`** — hero-within-10 → `HeroProximity`; and the HVT distance guard (>150 / <140)
  → `_OnHVTOutOfRange` / `_AddSupport`.
- **`Event.HumanStateTransition`** (persistent) — `→ "KnockedDown.Idle"` → `_TargetBashed`; `KnockedDown.*`
  → `Upright.*` → `_TargetOutOfSubdued`; `→ "Subdued.Idle"` → `_TargetSubdued`.
- **`Event.ObjectHibernation`** — `"awake"` → `_TargetOnAwake`, `"hibernated"` → `_TargetOnHibernate`
  (re-shows the correct tutorial hint when the target streams back in).
- **`Event.ContextAction`** (after death) → `_TargetActioned` (the "Verify" prompt).
- **`Event.ObjectInSeat`** (`"ExtractionHelicopter"`) → `_TargetExtracted` (subdued HVT stowed in the heli).
- **`Event.HumanActionComplete`** → `_TargetActionedComplete` (verify animation finished).
- **`Event.TimerRelative`** — the `3` s pre-verify delay, the flash animation timer, etc.
- **`Event.ScriptEvent`** (`"mpPlayerJoin"`) → `SendPlayerJoinEvents` (re-grant extraction freebie to a
  joining co-op player).
- **`Event.ObjectDelete`** → prunes a heli from `tActiveHelicopters`.
- **Faction attitude:** `MrxFactionManager.CreatePersistentAttitudeChangeEvent` / `CreateAttitudeChangeEvent`
  toggles extraction support as the faction's attitude to the PMC flips.

{: .warning }
> The previous page invented `Event.HelicopterSpawned` / `Destroyed` / `Damaged`, `Event.PilotKilled`,
> `Event.HelicopterLanded`, `Event.TargetSubdued` / `Extracted`, `Event.NetEvent`, and mis-spelled
> `Event.ObjectHibernate`. **None of the heli events exist** — helicopter state changes arrive through
> *callbacks* set on the support object (`oSupport.oSupport:SetHeliDestroyedCB(...)`,
> `SetHeliLandedCB`, `SetPilotKilledCB`, `SetHeliSpawnedCB`, `SetHeliDamagedCB`), which are not
> `Event.Create` subscriptions. `NetEventCallback` is the custom-net handler, not an event.

## Notes for modders
- **`sFactionId` (config) drives which extraction support is granted.** `_GetSupportByFaction` maps it:
  `All→Extraction_AL`, `Chi→_CH`, `Gur→_GR`, `Oil→_OC`, `Pmc→_PMC`, `Pir→_PR` (defaults to `Extraction_PMC`).
  Support is granted while the player stays within `150` m of the HVT and revoked past it.
- **Distances and the `3`-second verify delay are hardcoded**; the state machine (`HVT*`/`HELI*`) picks which
  `"[Tutorial.ObjectiveVerify.Key*]"` hint shows.
- **German SKU branch:** `Sys.IsGermanSKU()` skips the on-screen verify animation entirely and completes the
  part directly (`"CENSORED!!!!"` in the logs) — expect different flow on that SKU.
- Verify art overrides: radar `"objective_verify"`, world `"HUD_objective_verify"`, PDA
  `"icon_verify_1_mc"` / `"icon_verify_2_mc"`, inline `"[objverify]"` / `"[objverify2]"`;
  `_GetJust2DCheckNeeded()` returns `true` here (world blip uses a 2D distance check).