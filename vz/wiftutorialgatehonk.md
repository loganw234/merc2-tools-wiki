---
title: WifTutorialGateHonk
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 12
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialGateHonk

## Overview
Shown near one specific, hardcoded gate object while the player is using a vehicle disguise —
presumably teaching that a disguised vehicle should honk to be let through a faction checkpoint.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: `MrxTutorialManager`, `MrxFactionManager` — **both declared, neither referenced anywhere in
  this file's body.** The strongest instance of this pattern in the category (compare
  [`WifTutorialAlliesHonk`](wiftutorialallieshonk), which also has one unused import each).

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. No module-level or per-instance state
beyond what the base class itself tracks (`_tEvents`).

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.GateHonk]"`.

### SetupActivationCriteria(self)
Resolves a hardcoded gate object via `Sys.StringToGuid("0x000f9a64")`, then registers a **persistent**
`Event.ObjectProximity` (gate, player, within 20 units) that calls `ShowMessage`.

### ShowMessage(self)
Checks `Player.GetVehicleDisguiseState({Player = Player.GetLocalCharacter()})`. If
`tostring(bDisguiseState) == "true"`, calls the bare global `ActivateTutorial(self, true)` — resolves
through inheritance to `MrxTutorial.ActivateTutorial` since this file doesn't define its own.

## Events
- `Event.ObjectProximity` — persistent, hardcoded gate object, 20-unit radius. Being persistent, it
  keeps re-checking every time the player re-enters the radius rather than firing only once.

## Notes for modders
- Trigger key: `"GateHonk"`. Self-arms via a persistent proximity event.
- The gate's object GUID is hardcoded (`0x000f9a64`, resolved via `Sys.StringToGuid`) rather than
  resolved by label — tied to one specific placed gate in the level.
- `ShowMessage` compares `tostring(bDisguiseState) == "true"` rather than a plain truthy check — the same
  "stringify before comparing" idiom seen in [`WifTutorialVehicleDisguise`](wiftutorialvehicledisguise),
  likely because `Player.GetVehicleDisguiseState` can return a non-boolean/`nil` sentinel the author
  wanted to exclude from matching real `true`.
- Both imports (`MrxTutorialManager`, `MrxFactionManager`) are declared but never referenced anywhere in
  this file — likely vestigial, possibly copy-pasted from a similar tutorial.
- No `SetupCancellationCriteria` or `SetupCompletionCriteria` override — completes via the inherited
  **20-second** timer, not the 10-second pattern common elsewhere in this category.
