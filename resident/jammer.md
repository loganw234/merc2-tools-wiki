---
title: Jammer
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, support]
verified: true
verified_note: "deeper pass: re-confirmed the duplicate-OnDeactivate bug and all 8 functions (one, OnDeactivate, defined twice — see Notes); surfaced the animation name (global_gpsjammer_anim), the two sound cues, the [ContextAction.UseAlarm] prompt, and the \"jammer\" anti-air tag as tunables; replaced vacuous Notes bullet"
---

# Jammer

*Module: jammer.lua*

## Overview
The `Jammer` module represents a context-toggle GPS jammer in the game. It manages the activation and deactivation of the jammer, including its animations, vehicle parts, and anti-air support effects.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxSupport`

## Instance pattern
Not the `Inheritable` rich-instance pattern — no `Create`/`setmetatable`/`tInstance` registry. State lives
in one module-level global `tEvents` (`tEvents = tEvents or {}`), keyed by `uGuid`; each entry holds up to
two `Event.ContextAction` handles, `.uActivate` and `.uDeactivate`, that are swapped as the jammer toggles
between off and on.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the object instance is activated. Initializes `tEvents[uGuid]` and sets up an event to call `SetupActivationEvents` once the object leaves hibernation.

### `OnDeactivate(uGuid)` — defined twice, second wins
**Confirmed in source, likely a bug.** This function name is defined **twice** in the file: once at
line 9 (clears `tEvents[uGuid].uActivate`/`.uDeactivate` handles and nils out `tEvents[uGuid]`) and
again at line 75 (just calls `MrxSupport.RemoveAntiAir(uGuid, "jammer")`). Lua has no function
overloading — the second `function OnDeactivate(uGuid)` silently replaces the first in the module's
global table. Only the line-75 body ever actually runs when the engine calls `OnDeactivate`; the
event-cleanup logic at lines 9-21 is dead code that can never execute. Practical effect: deactivating a
jammer never deletes its `tEvents[uGuid].uActivate`/`.uDeactivate` event handles or clears the
`tEvents[uGuid]` entry — only `OnDeath` and this second `OnDeactivate` remove anti-air status.

### `SetupActivationEvents(uGuid)`
Plays the material animation for the jammer, disables vehicle parts rotation, adds a context action for using the alarm, and sets up an event to handle the use of the alarm.

### `OnUse(uGuid)`
Called when the player uses the jammer. It deletes the activation event, plays the alarm activated animation, enables vehicle parts rotation, removes the context action, sets up deactivation events, and adds anti-air support.

### `AlarmActivated(uGuid)`
Plays the material animation for the jammer, enables vehicle parts rotation, removes the context action, sets up deactivation events, and adds anti-air support.

### `SetupDeactivationEvents(uGuid)`
Adds a context action for using the alarm and sets up an event to handle the deactivation of the alarm.

### `AlarmDeactivated(uGuid)`
Stops the sound associated with the jammer, plays a different sound cue, plays the material animation for the jammer, disables vehicle parts rotation, removes the context action, sets up activation events, deletes the deactivation event, and removes anti-air support.

### `OnDeath(uGuid)`
Called when the object instance dies. It removes anti-air support (`MrxSupport.RemoveAntiAir`).

## Events
- `Event.ObjectHibernation` — registered in `OnActivate` (`{uGuid, "awake"}`) to call `SetupActivationEvents`
  once the object leaves hibernation.
- `Event.ContextAction` — registered twice (via different handles, `tEvents[uGuid].uActivate` /
  `.uDeactivate`), both filtered on `{Player.GetAnyCharacter(), uGuid}`: one calls `OnUse` (turn on) while
  the jammer is off, the other calls `AlarmDeactivated` (turn off) while it's on. These pair with
  `Pg.AddContextAction`/`Pg.RemoveContextAction` prompts, not raw input events.

## Module constants & tunables
- **Material animation:** `"global_gpsjammer_anim"` — played via `Object.PlayMaterialAnimation` (last arg
  `true`/`false` toggles the on/off pose) in the activate/use/deactivate paths.
- **Sound cues** (in `AlarmDeactivated`): stops `"fol_alarm_bldg_01"` and cues `"fol_bldg_alarm_activate"`.
- **Context prompt:** `"[ContextAction.UseAlarm]"` — the localized on-screen "use" prompt.
- **Anti-air tag:** `"jammer"` — passed to [MrxSupport](mrxsupport)`.AddAntiAir`/`.RemoveAntiAir`; this is
  what actually creates/removes the jamming effect on the support system.
- **Vehicle part:** `"CtrlRotation"` — toggled on/off via `Vehicle.SetParts` to spin/stop the dish.

## Notes for modders
- **Be aware of the duplicate `OnDeactivate` definition** (see Functions above) — only the second one in
  file order (anti-air removal only) is reachable; the `tEvents` cleanup body earlier in the file never
  runs, so activate/deactivate event handles are never freed on deactivation (only on the toggle cycle).
- **Reskin/retime:** swap `"global_gpsjammer_anim"` for a different material animation, or change the two
  sound cues, to restyle the jammer. The `"jammer"` tag is the gameplay hook — change it to route the
  effect through a different [MrxSupport](mrxsupport) anti-air category.