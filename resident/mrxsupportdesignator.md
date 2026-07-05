---
title: MrxSupportDesignator
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, economy]
verified: true
verified_note: "deeper pass: confirmed all functions/tables against source; cross-linked the 5 subtypes + Airstrike.EquipDesignator; documented the per-type field matrix (sDesignationType/sAATestLevel/validation/GetType) so the variants read as a family"
---

# MrxSupportDesignator

*Module: mrxsupportdesignator.lua*

## Overview
`MrxSupportDesignator` is the base class for the five things a player throws/places to mark a strike target: a [beacon](mrxsupportdesignatorbeacon), a [flare](mrxsupportdesignatorflare), a [laser](mrxsupportdesignatorlaser) painter, a [satellite](mrxsupportdesignatorsatellite) mini-game mark, or [smoke](mrxsupportdesignatorsmoke). It owns the shared machinery — target coordinates, the completion-callback list, drop-zone/landing-zone validation, and equipping the physical designator weapon — while each subtype overrides `Create`/`GetType` and (some) `Commence` to add its own behavior. A [`MrxSupport`](mrxsupport) strike holds one designator instance and fires its `DesignationCallback` when the designator completes.

## The five subtypes at a glance
Every subclass just re-runs `Create` to stamp a fixed set of fields, then overrides `GetType`. The differences that matter:

| Subtype | `sDesignationType` | `sAATestLevel` | `fValidationFunction` | Notable extra |
|---|---|---|---|---|
| [Beacon](mrxsupportdesignatorbeacon) | `"Beacon Designator"` | `"jammer"` | `nil` | `bDesignateOnDeath = false` |
| [Flare](mrxsupportdesignatorflare) | `"Flare Designator"` | `"none"` | `ValidateWaterDropZone` | spawns `"Flare Projectile Stage 2"` on complete |
| [Laser](mrxsupportdesignatorlaser) | `"Laser Designator"` | `"medium"` | (inherited) | custom `Commence` + `LaserFinished` (fuel/recruit checks) |
| [Satellite](mrxsupportdesignatorsatellite) | `"Satellite Designator"` | (per-support) | (inherited) | PDA-map mini-game, cost, zoom |
| [Smoke](mrxsupportdesignatorsmoke) | `"Smoke Designator"` | `"basic"` | `ValidateGroundDropZone` | colored smoke emitter, 10s lifetime, net-synced |

## Inheritance
- Inherits from: none — base/utility module
- Imports: none (calls the [Airstrike](../namespaces/airstrike) engine namespace for `EquipDesignator`)

## Instance pattern
**Not per-`uGuid` — same class-factory pattern as [`MrxSupport`](mrxsupport)**: `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, no `tInstance` registry anywhere in source. This is the
base class its 5 designator subtypes (Beacon/Flare/Laser/Satellite/Smoke) all inherit the pattern from.
Key fields:
- `uOwner`: The GUID of the player or entity that owns the designator.
- `bDesignationComplete`: A boolean indicating whether the designation process is complete.
- `sDesignationType`: The type of designation being used.
- `sAATestLevel`: The AA test level for the designation.
- `fValidationFunction`: A function to validate the drop zone.
- `tCallbackList`: A list of callbacks to be called when designation is complete.
- `tVOCues`: A table for voice-over cues related to designation.
- `nX`, `nY`, `nZ`: The coordinates of the designated location.
- `uGuid`: The GUID of the designator object.
- `oParentSupport`: The parent support object that owns this designator.

## Functions
### `GetTarget(self)`
Returns the target coordinates and GUID once the designation is complete. Returns `nil` if the designation is not complete.

### `RemoveBeacon(self)`
Removes a beacon associated with the designator if it exists.

### `Create(self, oNewDesignator)`
Creates a new instance of the designator by copying properties from an existing one. If no new designator is provided, it creates a default instance.

### `SetOwner(self, uPlayerGuid)`
Sets the owner of the designator to the specified player GUID.

### `AddCompleteCallback(self, fCallback, tCallbackData)`
Adds a callback function to be called when the designation is complete. The callback data can be passed as an optional table.

### `RemoveCompleteCallback(self, fCallback)`
Removes a previously added callback function from the list of callbacks.

### `SetCompleteCallback(self, fCallback, tCallbackData)`
Sets a callback function and its associated data to be called when the designation is complete. The callback must be a function, and the data must be a table if provided.

### `CompleteDesignation(self)`
**Not documented above but this is what actually fires everything `AddCompleteCallback`/`SetCompleteCallback`
registered.** Sets `bDesignationComplete = true`, calls every function in `tCallbackList` with its stored
data (`fFunction(unpack(tData))`), then posts an `"Airstrike"` event with `sStage = "DesignationComplete"`,
`sType = "None"` (subclasses override `GetType` to post a more specific `sType`). Nothing in this base class
calls `CompleteDesignation` itself — it's meant to be invoked by whatever confirms a valid target was
reached, e.g. a designator subclass's own drop-zone/landing-zone validation success.

### `SetDesignationType(self, sTemplateName)`
Sets the type of designation template to use for the designator. The template name should be a string or `nil`.

### `SetValidationFunction(self, fFunction)`
Sets the validation function to be used for validating the drop zone. The function must be a function or `nil`.

### `ValidateGroundDropZone(fCallback, nX, nY, nZ, oSupport, bWater)` / `ValidateWaterDropZone(fCallback, nX, nY, nZ, oSupport)` / `ValidateLandingZone(fCallback, nX, nY, nZ, oSupport)`
**Not previously documented on this page — the actual drop-zone/landing-zone validation logic the Overview
refers to**, and the shape of function `SetValidationFunction` expects (note: these three all take
`fCallback` as their *first* argument, not `self` — plain functions, not methods, despite living in this
module). All three wrap `Ai.TestDropZone`, looking up per-cargo/per-vehicle radius and height-tolerance
data from two local tables (`_cargoTemplateData`, `_heliTemplateData`, keyed by template hash string, falling
back to a `.default` entry) and calling `fCallback` themselves with `(false, "nodrop")` or `(false, "noland")`
if `Ai.TestDropZone` couldn't even register the test. `ValidateWaterDropZone` is just
`ValidateGroundDropZone` with `bWater` forced to `true`.

### `SetTargetValidationRequired(self, bRequireValidation)`
Sets whether target validation is required before completing the designation.

### `SetAATestLevel(self, sAATestLevel)`
Sets the AA test level for the designation.

### `SetTargetLocation(self, nX, nY, nZ)`
Sets the target location coordinates for the designator. The coordinates must be numbers.

### `SetDesignationParameters(self, nNewX, nNewY, nNewZ, uGuid, uTarget)`
**Not previously documented — this, not `SetTargetLocation`, is the setter that actually populates what
`GetTarget` later returns**, including the two fields `SetTargetLocation` doesn't touch at all (`uGuid`,
`uTarget`). Each argument is individually type-checked and falls back to keeping the existing value if the
type doesn't match (`"number"` for the coordinates, `"userdata"` for the two guids) rather than rejecting
the whole call.

### `OnDeny(self, uGuid)`
Called when the designation is denied. Currently does nothing.

### `SetParentSupport(self, oSupport)`
Sets the parent support object that owns this designator.

### `GetParentSupport(self)`
Returns the parent support object that owns this designator.

### `Configure(self, tOptions)`
Configures the designator with options provided in a table. If an option is not present in the table, it retains its current value.

### `Commence(self, bFireImmediately)`
Starts the designation process. Calls `Airstrike.EquipDesignator(self.uOwner, self.sDesignationType, nil, nil, bFireImmediately)` to give the player the physical designator item, then `Weapon.SetReserveAmmo(self.uWeaponGuid, 1)` so it's a single-use throw. Returns the equipped weapon guid, or `false` if `uOwner` isn't a `userdata` handle. The [Laser](mrxsupportdesignatorlaser) and [Satellite](mrxsupportdesignatorsatellite) subtypes override this to pass their own completion callback into `EquipDesignator` instead of `nil`.

{: .note }
> `Airstrike.EquipDesignator` is a real engine call used by every designator subtype but is **not yet documented on the [Airstrike](../namespaces/airstrike) namespace page** (that page enumerates only `SpawnOrdnance`/`SpawnTargettedOrdnance` from grepped call sites). Confirmed signature from usage: `uWeaponGuid = Airstrike.EquipDesignator(uOwner, sDesignationType, fCompleteCallback, tCallbackData, bFireImmediately)`.

### `GetType(self)`
Returns the type of the designator, which is "none" in this base class.

## Events
- Listens for custom events related to designation completion and validation.

## Notes for modders
- Ensure that the designator's owner is set correctly using `SetOwner`.
- Use `AddCompleteCallback` and `RemoveCompleteCallback` to manage callbacks for when the designation is complete.
- Customize the designator by setting various parameters such as type, validation function, and target location using the provided setter functions.
- Be aware that the designator's behavior can be influenced by the parent support object set with `SetParentSupport`.
- The module uses predefined templates (`_cargoTemplateData` and `_heliTemplateData`) for validating drop zones. These templates can be extended or modified as needed.