---
title: Danceradio
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [lifestyle prop, animation]
verified: true
verified_note: 'deeper pass: re-confirmed OnActivate is still a no-op bare return (module inert), the shared-global state, and the full Event.* list; added a Module constants section (animation "player_mattias_bare_technoviking", "Dance"/"hero" context action, "DanceRadio" channel, NETEVENT_STARTDANCING=0, 1s timer) and Human/networking cross-links'
---

# Danceradio

*Module: danceradio.lua*

## Overview
The `Danceradio` module is a lifestyle prop intended to let players perform a dance animation
(`player_mattias_bare_technoviking`), synchronized across the network. **As currently written, the module is
inert**: `OnActivate` is a bare `return` with no logic, so none of the setup code (`OnActivateOld`,
`SetupActivationEvents`, the context action, the network handler) is ever reached from a live object
activation. See Notes below.

## Inheritance
- Inherits from: `none` — no `inherit()` call in this file.
- Imports: `none`

## Instance pattern
Stateless in the "no per-`uGuid` table, no `Inheritable`/`Create` chain" sense — there's no `tInstance`
registry keyed by `uGuid`. But it is **not** stateless in the sense of holding no state at all: several
plain module-level globals persist across calls and are shared by every activation of the prop, not
scoped per-object:
- `tEvents`: table of event handles, initialized `tEvents[uGuid] = tEvents[uGuid] or {}` in `OnActivateOld`
  (dead code path — see Overview) but never actually populated or read anywhere else in the file.
- `bAssetLoaded`: boolean, set in `OnActivateOld`, read/cleared in `OnDeactivate`.
- `oEvent`: (not declared `local`) holds the `Event.ContextAction` handle from `SetupActivationEvents`.
- `iPlayer`: (not declared `local`) set in `OnUse` to `1` or `2` depending on which character used the radio.
- `uGuid`: (not declared `local`) reused as a genuine global in `NetEventCallback` to resolve the acting
  character's GUID before calling `OnUse` — shadows the parameter name used elsewhere in the file, which is
  confusing but not itself broken given Lua's runtime name resolution.

## Functions
### `OnActivate(uGuid, iArg)`
Immediately `return`s — no setup, no event registration. Note the 2-argument signature here vs. the
3-argument `OnActivate(uGuid, uRuntimeOwner, iArg)` convention seen in most other world-object scripts.
Because this is a no-op, the rest of the file's activation chain (below) is currently unreachable from a
real object spawn.

### `OnActivateOld(uGuid, iArg)`
Not called from anywhere in this file or referenced by any other file found in this corpus — orphaned/dead
code, presumably the previous activation handler before it was replaced by the no-op `OnActivate` above.
Loads the `player_mattias_bare_technoviking` animation asset, sets `bAssetLoaded = true`, initializes
`tEvents[uGuid]`, and registers `SetupActivationEvents` to run once the object leaves hibernation
(`Event.ObjectHibernation`, `"awake"`).

### `OnDeactivate(uGuid)`
Unloads the animation asset if `bAssetLoaded` is true, and deletes `oEvent` (setting it to `nil`). Reachable
via the engine's normal deactivation hook regardless of whether `OnActivateOld` ever ran, so this can run
against unset globals if the object never went through the (dead) activation path.

### `SetupActivationEvents(uGuid)`
Adds a `"Dance"` context action for the prop and registers `oEvent` as an `Event.ContextAction` listener
(triggered by `"hero"` on this `uGuid`) that calls `OnUse`. Only called from `OnActivateOld` (dead) and from
`Finished` (below) — so in the current build, never actually invoked.

### `OnUse(uCharacter, uGuid)`
Identifies which player used the radio (`Player.GetPrimaryCharacter()` -> `iPlayer = 1`,
`Player.GetSecondaryCharacter()` -> `iPlayer = 2`), and if `Net.IsServer()`, sends a custom network event
`Net.SendCustomEvent("DanceRadio", NETEVENT_STARTDANCING, {iPlayer, uGuid})`. Removes the context action,
disables the character's weapons, plays the raw animation, and schedules `Finished` to run one second after
an `Event.HumanStateTransition` reports `"complete"` for that character.

### `Finished(uGuid, uCharacter)`
Re-enables the character's weapons and calls `SetupActivationEvents(uGuid)` again to re-arm the context
action for the next use.

### `NetEventCallback(nEventType, tArgs)`
Handles incoming `NETEVENT_STARTDANCING` (`= 0`) network events: resolves the acting character from
`tArgs[1]` (`1` -> primary, `2` -> secondary character) into the global `uGuid`, then calls
`OnUse(uGuid, tArgs[2])` to replay the dance locally on the receiving client.

## Events
Actual `Event.*` constants referenced in this file:
- `Event.ObjectHibernation` — in `OnActivateOld` (dead path), to call `SetupActivationEvents` on "awake".
- `Event.ContextAction` — in `SetupActivationEvents`, to call `OnUse` when a hero triggers the `"Dance"` action.
- `Event.TimerRelative` — in `OnUse`, to delay registering the completion listener by 1 second.
- `Event.HumanStateTransition` — registered inside that timer callback, to call `Finished` when the
  animation reaches `"complete"`.

`"DanceRadio"` is **not** an `Event.*` constant — it's a channel-name string argument to
`Net.SendCustomEvent`/`NetEventCallback`, the engine's separate network-RPC mechanism.

## Module constants & tunables
- Animation asset/template: `"player_mattias_bare_technoviking"` — loaded via `Pg.LoadAsset(..., "animation")`
  (in the dead `OnActivateOld`) and played via `Human.PlayRawAnimation` in `OnUse`.
- Context action label: `"Dance"` (added via `Pg.AddContextAction(uGuid, "Dance", false)`).
- Context action actor filter: `"hero"` (only the hero can trigger the `Event.ContextAction`).
- Net channel string `"DanceRadio"` with the single event id `NETEVENT_STARTDANCING = 0`.
- Timer delay before arming the completion listener: `1` second (`Event.TimerRelative {1}`).
- Animation completion is detected via `Event.HumanStateTransition` with the transition tuple
  `{uCharacter, "*", "*", "complete"}`.

## Notes for modders
- `OnActivate` currently does nothing. To make this prop functional, it would need to be changed to do what
  `OnActivateOld` does (or call it directly) — as shipped, activating this object has no effect.
- Several fields here are plain globals (`oEvent`, `iPlayer`, `uGuid`) rather than `local`s or per-instance
  table fields — they're shared across every instance of this prop in the world, not scoped per-`uGuid`.
  Multiple simultaneous instances would stomp on each other's state.
- Be aware that network synchronization (`Net.SendCustomEvent`, `NetEventCallback`) affects multiplayer
  behavior — dance state is explicitly replicated via a custom net event, not the standard `Event.*` system.
  See the [networking deep dive](../deep-dives/networking) for the wider `NETEVENT_` custom-event pattern.
- The dance itself uses [`Human`](../namespaces/human)`.DisableWeapons` / `PlayRawAnimation` / `EnableWeapons`
  — that disable-play-reenable sequence is the reusable lever if you want a different one-shot player
  animation prop; swap the `"player_mattias_bare_technoviking"` template.