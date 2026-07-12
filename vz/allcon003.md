---
title: AllCon003
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# AllCon003

## Overview
An Allied Nation story contract set during a China invasion of Caracas: the player verifies (kills) a
high-value target (`AllCon003_HVT`) and destroys four marked buildings, in any order, needing both done
to complete. Verifying/destroying triggers `GoHostile`, which drops China's relation with the PMC by 200
and stops China's faction reporting. The player is granted several `AL_CruiseMissile` and `Gunship`
support freebies for the fight, and the local atmosphere is switched to a "warzone" setting.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxCinematic`, `DangerousBuilding`, `Outpost`, `MrxSupportData`, `MrxFactionManager`,
  `MrxLayerManager`

## Instance pattern
A native `MrxTaskContract` subclass. Contract state is two module-level globals: `nCompleted` (counts
completed top-level objectives, 0-2) and `bHostile` (guards `GoHostile` from firing more than once).

## Functions
### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, resets `nCompleted`/`bHostile`, and waits for the local
character to wake before calling `Start`.

### `Start(self)`
Grants the `AL_CruiseMissile`/`Gunship` freebies, plays the opening VO, calls `SetupObjectives` and
`CaracasIsHell`, and adds the `vz_state_allcon003_invasion` layer.

### `SetupObjectives(self)`
Creates the `MrxTaskObjectiveVerify` child for the HVT and the `MrxTaskObjectiveDestroy` child for the
four marked buildings; both wire `GoHostile` (on first kill/part-destroyed) and `OneObjectiveDown` (on
full completion).

### `GoHostile(self)`
One-shot (guarded by `bHostile`): plays a VO sequence that drops China's PMC relation by 200 and stops
China's faction reporting.

### `OneObjectiveDown(self)`
Adds an AI infraction against China and increments `nCompleted`; completes the contract once both
objectives are done.

### `NukeItFromOrbit(self)`
Plays a VO line and calls in an autogunship flyby near the player. **No call site found anywhere in this
file.**

### `DecrementTimer(self)`
Subtracts 600 seconds from `oBonus._oTimer` and plays a one-time warning VO. **No call site found
anywhere in this file**, and `oBonus`/`bPlayedWarning` are never otherwise set here — this reads as
leftover scaffolding for an optional timed bonus objective that isn't actually wired up in this contract.

### `CaracasIsHell(self)`
Switches the `rgn_atmo_caracas` region's atmosphere setting to `"warzone"`.

### `BonusCancel(self)`
Plays a cancel VO line. **No call site found anywhere in this file** — same unwired-bonus-objective
pattern as `DecrementTimer`.

### `Cleanup(self)`
Restores the pre-invasion staging layer, removes the `AL_CruiseMissile` freebie, and calls the base
`MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectHibernation` — the local character waking fires `Start`.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Shared-template sibling**: [ChiCon003](chicon003) has the exact same shape — a hibernation-gated
  `Start`, a verify+destroy pair racing to 2 completions, a one-shot hostile-relation flip, the same
  `CaracasIsHell` atmosphere call, and the *same* unwired `BonusCancel`/`DecrementTimer` dead functions.
  The two were very likely cloned from a shared authoring template, with the optional timed-bonus-objective
  scaffolding copy-pasted but never actually hooked up in either file.
- `NukeItFromOrbit`, `DecrementTimer`, and `BonusCancel` all have no in-file call site — treat them as
  inert unless invoked externally (e.g. by a level-editor trigger volume calling a named script function),
  which this kind of engine does support and which wouldn't show up as a Lua call site here.
