---
title: MrxSupport
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, economy]
verified: true
verified_note: 'deeper pass: re-confirmed the class-factory pattern, the o-global decompiler artifact, and the corrected Events list; added a module constants/tunables block (default vehicle/bomb templates, 60%-health damage-abort, 60s Copter cooldown, GetSpawnHeight 250/50, per-faction GoHome landing zones) and cross-linked the subclasses'
---

# MrxSupport

*Module: mrxsupport.lua*

## Overview
`MrxSupport` is the shared base every airstrike/supply-drop/vehicle-delivery type in the
[Support & Airstrikes](index) category builds on — designating targets, handling fuel/cash/stockpile
costs, anti-air interaction, and player feedback are all defined once here rather than per support type.
If you want to add a new support type, this (and [`MrxSupportDelivery`](mrxsupportdelivery) for anything
delivered by a helicopter) is where to start.

**Not the `Inheritable`/per-`uGuid` world-object pattern** — there's no `OnActivate`/`Awake` anywhere in
this file. `MrxSupport` uses a plain Lua class-factory pattern instead: a support-type module (e.g.
`MrxCombatAirPatrol`) calls `MrxSupport:Create(uPlayerGuid)` (or, from a further subclass,
`ParentModule.Create(self, uPlayerGuid)`), which does `setmetatable(oNewSupport, self); self.__index =
self` and hands back a fresh object that falls back to whichever module actually called `Create` for
everything it doesn't set itself. There's no `tInstance`-style registry keyed by GUID — a support object's
identity comes from being held onto directly by whatever created it, not looked up later by a world-object
GUID.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSupportDesignator`, `MrxSupportManager`, `MrxGui`, `MrxPmc`, `MrxGuiHudMessage`, `AntiAir`,
  `MrxAchievements`, `MrxUtil`, `MrxVoSequence`, `MrxFactionManager`

## Instance pattern
Class-style object, not per-`uGuid` — see the callout above. Fields set per-object by `Create`/the
various `Set*` functions:
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
Confirmed directly from source — not a general subscription list, these are specific to particular
functions:
- **`Event.ObjectHibernation`** — used in `BlipAircraft` (auto-remove a blip once the aircraft hibernates)
  and `Land`/`GoHome` (remove a landed helicopter/winched object once it hibernates). Not about the support
  object's own lifecycle.
- **`Event.ObjectDeath`** — used in `BlipAircraft` (remove blip on death) and `SetupPilotKilledEvent` (calls
  `Abandon` if the pilot dies).
- **`Event.TimerRelative`** — used for cooldowns/delays in various support-sequence functions.

`Event.PlayerJoined`/`Event.PlayerLeft`/`Event.NetAction` do **not** appear anywhere in this file — an
earlier version of this page listed them incorrectly. `SynchNetAction`/`SynchNetAddItem`/
`SynchNetRemoveItem` are plain functions, dispatched to by naming convention (the same pattern documented
on the [networking deep dive](../deep-dives/networking)), not registered engine event listeners.

## Notes for modders

1. **This is a class-factory object, not a per-`uGuid` world object** — see the Overview callout. Don't
   look for `OnActivate`/`Awake` here; a new support-type module built on this calls
   `MrxSupport:Create(uPlayerGuid)` (or the equivalent through its own parent) to get an instance, then
   configures it via `Configure(tOptions)` or the individual `Set*` functions before calling
   `Commence`/`BeginSupportSequence`.
2. **Pitfalls**:
   - `RefundCosts` refunds exactly what `BeginSupportSequence` recorded consuming (`nFuelConsumed`/
     `sStockpileConsumed`/`sFreebieConsumed`) and nils each after — it's idempotent, but only refunds if
     those fields are still set, so call it before anything else clears them.
   - Per-support-sequence event listeners (aircraft hibernation/death in `BlipAircraft`, pilot death in
     `SetupPilotKilledEvent`, the 60%-health abort in `SetupDamageEvent`) are keyed to a specific heli GUID
     and are **not** auto-released — clean them up (or let `GoHome`/`Abort` do it) or they leak.
3. **Tunables & constants** (file scope unless noted):
   - Default templates: `sDeliveryVehicle = "Support Vehicle (Mig27)"`, `sBomb = "Dumb Bomb Projectile"`,
     `sRecruit = "Arachnid Guy"` — subclasses override these via `Set*`.
   - **Damage-abort threshold**: `SetupDamageEvent` aborts the support if the heli's health drops below
     **60%** (`Object.GetHealth(uHeli) * 0.6`).
   - **Copter cooldown**: `BeginSupportSequence` starts a **60**-second cooldown on the `"Copter"` recruit
     after use (`MrxSupportManager.StartRecruitCooldown("Copter", 60)`).
   - **Spawn height**: `GetSpawnHeight()` returns **250** if a co-op secondary character is present, else
     **50** — this is the vertical offset most subclasses use when spawning the delivery aircraft.
   - **Return landing zones**: `GoHome` sends the heli to a per-faction HQ LZ (`tLocs`: PMC→
     `01_pmc_hq_lz_playerone`, Allied→`07_all…`, China→`12_chi…`, Guerilla→`05_gur…`, OC→`02_oil…`,
     Pirate→`08_pir…`), falling back to a random camera-relative point if the LZ isn't found.
   - Costs (`SetFuelCost`/`SetCashCost`) and VO cues (`SetVOCues`/`PlayRandomVOCue`) are the economy/immersion
     levers.
4. **Decompiler artifact worth knowing about**: `Create(self, uPlayerGuid)` references a bare global `o`
   (`local oNewSupport = o or {}`) that's never defined anywhere in this file — almost certainly a lost
   local-variable name from decompilation. Harmless in practice (`o` is always `nil`/falsy at runtime, so
   this always evaluates to a fresh `{}`), unlike the genuinely crashing version of this same class of bug
   documented on [`MrxGuiTextBuffer`](mrxguitextbuffer) — but worth recognizing as the same pattern if you
   ever see it elsewhere.