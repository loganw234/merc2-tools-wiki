---
title: ChiCon003
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# ChiCon003

## Overview
A China story contract set in Caracas, structurally a mirror image of Allied Nation's
[AllCon003](allcon003): verify (kill) a China-side high-value target (`ChiCon003_HVT`) and destroy
five marked buildings, in any order, needing both done to complete. Here, progress triggers
`AlliesHateYou` (a -200 relation hit against the Allied faction) instead of a hit against China, and
completion grants a free `ChiCon003_Artillery` support plus four `CH_CruiseMissile` freebies. The five
target buildings are also flagged non-collapsing/reinforced via `DangerousBuilding.TurnOn` until
destroyed as an objective.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxCinematic`, `DangerousBuilding`, `Outpost`, `MrxSupportData`, `MrxFactionManager`

## Instance pattern
A native `MrxTaskContract` subclass. Module-level globals: `nCompleted` (0-2, counts completed
objectives), `bAlliesHateYou` (guards `AlliesHateYou` from firing twice), and `tBuildings` (the five
target names, also read by the `DangerousBuilding.TurnOn` loop).

## Functions
### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, resets `nCompleted`/`bAlliesHateYou`, and waits for the local
character to wake before calling `Start`.

### `Start(self)`
Calls `SetupObjectives` and `CaracasIsHell`.

### `SetupObjectives(self)`
Arms `CreateProxEvents`, plays the opening VO (which also grants the cruise-missile freebies partway
through the sequence), creates the `MrxTaskObjectiveVerify` child for the HVT and the
`MrxTaskObjectiveDestroy` child for the five buildings (wiring `AlliesHateYou`/`OneObjectiveDown` on
each), and flags all five buildings non-collapsing via `DangerousBuilding.TurnOn`.

### `CreateProxEvents(self)`
Arms a hibernation trigger on `AllJob001_02_Outpost` that plays a VO line once it wakes.

### `OneObjectiveDown(self)`
Increments `nCompleted`; completes the contract once both objectives are done.

### `BonusCancel(self)`
Plays a VO line and locks the Allied faction's pursuit for 3 (presumably minutes/units). **No call site
found anywhere in this file.**

### `DecrementTimer(self)`
Subtracts 600 seconds from `oBonus._oTimer` and plays a one-time warning VO. **No call site found
anywhere in this file**, and `oBonus`/`bPlayedWarning` are never otherwise set here — the same unwired
bonus-objective scaffolding seen in [AllCon003](allcon003).

### `AlliesHateYou(self)`
One-shot (guarded by `bAlliesHateYou`): plays a VO sequence that drops the Allied faction's PMC relation
by 200.

### `CaracasIsHell(self)`
Switches the `rgn_atmo_caracas` region's atmosphere setting to `"warzone"`.

### `SetBattlePathways(self)`
Disables fifteen named road lanes for AI pathing. **No call site found anywhere in this file.**

### `_MissionComplete(self)`
A one-line wrapper for `self.Complete(self)`. **No call site found anywhere in this file** — possibly
invoked externally by a level-editor trigger volume rather than from Lua.

### `Cleanup(self)`
Clears the Allied pursuit lock, removes the `CH_CruiseMissile` freebie, and calls the base
`MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectHibernation` — the local character waking fires `Start`; `AllJob001_02_Outpost` waking
  fires a VO line via `CreateProxEvents`.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Shared-template sibling**: [AllCon003](allcon003) has the exact same shape — hibernation-gated
  `Start`, a verify+destroy pair racing to 2 completions, a one-shot hostile-relation flip, the same
  `CaracasIsHell` atmosphere call, and the *same* unwired `BonusCancel`/`DecrementTimer` dead functions.
  The two were very likely cloned from a shared authoring template.
- `BonusCancel`, `DecrementTimer`, `SetBattlePathways`, and `_MissionComplete` all have no in-file call
  site — treat them as inert unless invoked externally (e.g. a level trigger calling a named script
  function by name, which this engine supports and which wouldn't appear as a Lua call site here).
