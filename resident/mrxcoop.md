---
title: MrxCoop
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [co-op, player management]
verified: true
verified_note: 'deeper pass: spot-checked against source, confirmed accurate; noted the 38.5 boundary radius
  and squared-distance tether comparison, and flagged the PlayerAddMessage arg-count mismatch in
  _TetherInsideMin (passes the message string as the uPlayerGuid) as a harmless debug-only decompiler quirk.'
---

# MrxCoop

*Module: mrxcoop.lua*

## Overview
The `MrxCoop` module manages co-op gameplay mechanics, specifically the tethering system that keeps players within a certain distance of each other. It handles setting up and destroying tethers, adding new players to the game session, determining respawn origins, and managing player proximity events.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui`, `MrxPlayer`

## Instance pattern
No `OnActivate`/`Awake`/`tInstance`/`setmetatable` — not a per-`uGuid` instance module. It's a singleton
manager that keeps its working state in a handful of module-level globals instead (all set with no
`local`, so they're visible/shared across the whole module rather than tied to a discrete object):
- `_tEvents`: table of active `Event.ObjectProximity` handles, keyed by `"<secondaryCharTostring>_in"` /
  `"_out"` / `"_btw"`.
- `_primaryChar`: the first player's character GUID, set once by the first `AddPlayer` call.
- `iTetherMin` / `iTetherMax`: tether distance thresholds, set by `SetupTether`.

## Functions
### `SetupTether(aTetherMin, aTetherMax)`
Sets up the tethering system with specified minimum and maximum distances. It destroys any existing tethers and initializes event handles. The tether boundary radius is set to 38.5 units.

### `DestroyTether()`
Destroys all active tethers by removing proximity events and disabling out-of-boundary settings for players.

### `AddPlayer(newPlayer)`
Adds a new player to the co-op session. If no primary character is set, it assigns the new player as the primary. For subsequent players, it calculates their distance from the primary character and sets up appropriate tethering events based on proximity.

### `GetRespawnOrigin()`
Determines the respawn origin for players. It checks if any alive player characters exist and uses their position and yaw. If no alive players are found, it defaults to a predefined respawn point named "loc_playerStart".

### `_TetherInsideMin(primary, secondary)`
Handles the case where a player is inside the minimum tether distance from the primary character. It sets up events to monitor proximity for transitioning between distances. (Decompiler quirk: its debug
`PlayerAddMessage("INSIDE: " .. idx)` call passes only one argument, so the message string lands in the
`uPlayerGuid` slot and `sMsg` is `nil` — a harmless bug since these are diagnostic messages only. The sibling
handlers call it correctly with `(secondaryPlayer, "...")`.)

### `_TetherBetweenMinAndMax(primary, secondary)`
Handles the case where a player is between the minimum and maximum tether distances. It sets up events to monitor proximity for transitioning outside the maximum distance or inside the minimum distance.

### `_TetherOutsideMax(primary, secondary)`
Handles the case where a player is outside the maximum tether distance from the primary character. It sets up events to monitor proximity for transitioning back within the maximum distance.

### `GetSquaredDistance(obj1, obj2)`
Calculates the squared distance between two objects based on their positions.

### `PlayerAddMessage(uPlayerGuid, sMsg)`
Adds a message to a player's message box widget in the GUI. If the widget is not found, it does nothing.

## Events
- Listens for proximity events (`Event.ObjectProximity`) to manage player tethering states.
- Does not fire any custom engine events directly.

## Notes for modders
- **`SetupTether(min, max)` takes two distances** and also hard-sets the engine boundary radius to `38.5`
  (`Pg.SetBoundaryRadius`). `min`/`max` are stored in `iTetherMin`/`iTetherMax` (module globals) and drive
  the three-band proximity state machine (inside-min / between / outside-max). Only the *secondary* player is
  tethered; the first `AddPlayer` becomes `_primaryChar`.
- **Comparison note:** the initial band pick in `AddPlayer` compares **squared** distances
  (`GetSquaredDistance` vs. `iTetherMin*iTetherMin`), but the `Event.ObjectProximity` thresholds use the raw
  `iTetherMin`/`iTetherMax`. Same effective distances, two different representations — don't "fix" one to
  match the other.
- `GetRespawnOrigin` returns the first alive player's position/yaw, falling back to the level marker
  `"loc_playerStart"` if nobody's alive — that marker must exist in the level or respawn origin is invalid.
- The `_tEvents` keys are `"<secondaryCharTostring>_in"/"_out"/"_btw"`, so the tether bookkeeping is keyed by
  the secondary character's handle-string; only one secondary is really supported at a time.