---
title: Alarm
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [alarm, building]
verified: true
verified_note: import() failure outside a level with a real alarm object confirmed by live testing; rest of the module read directly from source
---

# Alarm

*Module: alarm.lua*

## Overview
The `Alarm` module manages the activation and deactivation of alarms for occupied buildings within a
100-meter radius. It triggers when any building is occupied, auto-checks every 8 seconds, and self-mutes
after 60 seconds if no buildings remain occupied.

**Not always-resident — `import("Alarm")` fails outside a level that has a real alarm object.** Despite
living in `resident/`, this is a per-object world-entity script (has `OnActivate(uGuid, iArg)`), not an
always-loaded core module like `MrxFactionManager` or `MrxPmc`. Confirmed by live testing: calling
`import("Alarm")` from a console/`OnLoad` script in a context with no alarm object currently loaded throws
`attempt to index global 'Alarm' (a nil value)`. This matters specifically because `Alarm` is the obvious,
tempting example to copy when hijacking `NetEventCallback` for custom networked events (it's short and its
own two real event IDs are `0`/`1`) — see the [networking deep dive](../deep-dives/networking) and the
[co-op chat feature](../deep-dives/coop-chat), both of which hit this exact error and switched to
`MrxFactionManager` as a safe, confirmed always-resident hijack target instead.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `DangerousBuilding`, `MrxTutorialManager`

## Instance pattern
This module does not follow the per-instance object pattern. It maintains global state in tables like
`tEvents` and `tLights`, keyed by the alarm object's `uGuid`.

## Functions
### `NetEventCallback(nEventType, tArgs)`
Handles network events for alarm activation and deactivation by calling `NetSafeAlarmActivated` or
`NetSafeAlarmDeactivated` based on the event type. Real event IDs: `NETEVENT_ALARMACTIVATE = 0`,
`NETEVENT_ALARMDEACTIVATE = 1` — see the [full `NETEVENT_` catalog](../deep-dives/networking#the-full-netevent_-catalog)
for how these fit alongside every other module's custom event IDs.

### `OnActivate(uGuid, iArg)`
Called when the alarm object is activated. Sets up initial state and schedules an event to call `Awake`
(inline, not a separate named function here) once the object leaves hibernation.

### `SendPlayerJoinEventsAlarm(uGuid)`
Sends a network event to activate the alarm if it was previously active — part of syncing state to a
player who joins mid-session.

### `OnDeath(uGuid)`
Calls `OnDeactivate` when the alarm object dies.

### `OnDeactivate(uGuid)`
Cleans up all events and state associated with the alarm object.

### `SetupActivationEvents(uGuid)`
Sets up the context action and events for activating the alarm, including handling player joins.

### `SetupDeactivationEvents(uGuid)`
Sets up the context action and event for deactivating the alarm.

### `OnUse(uGuid, bEnabled)`
Handles the use of the alarm by either activating or deactivating it based on the `bEnabled` flag.

### `MuteAlarm(uGuid)`
Stops the alarm sound after 60 seconds if no buildings are occupied.

### `AlarmActivated(uGuid)`
Activates the alarm: turns on nearby occupied buildings (`Pg.FastCollectBuildings(x, y, z, 100, "Occupied")`,
`DangerousBuilding.TurnOn`), plays sounds, flips the light/rotation vehicle parts, and sets up a recheck
event every 8 seconds.

### `CheckAlarm(uGuid)`
The 8-second recheck: looks for any occupied buildings within the radius. If none are found, deactivates
the alarm.

### `AlarmDeactivated(uGuid)`
Deactivates the alarm, stops sounds, and resets the alarm object's state.

### `NetSafeAlarmActivated(uGuid)` / `NetSafeAlarmDeactivated(uGuid)`
The receiving side of a network sync — waits for the object to be awake before replaying the
activate/deactivate visual and audio effects locally, without re-sending another network event (avoiding
an echo loop).

## Events
- Listens for `Event.ObjectHibernation` to run its awake-setup once the object leaves hibernation.
- Listens for custom event `mpPlayerJoin` to send player-join sync events.
- Listens for network events `NETEVENT_ALARMACTIVATE` and `NETEVENT_ALARMDEACTIVATE` (see `NetEventCallback`
  above).

## Notes for modders
- **Don't hijack this module's `NetEventCallback` for your own custom events** — see the callout above.
  Use `MrxFactionManager` instead; it's confirmed always-resident.
- `Pg.FastCollectBuildings(x, y, z, fRadius, sFilter)` (used here with `"Occupied"`) is a reusable pattern
  for "find buildings near a point" — see the [Pg namespace page](../namespaces/pg) for the wider
  `FastCollect*` family.
- The 100-meter search radius, 8-second recheck interval, and 60-second mute delay are all inline literals
  in the function bodies above (not named constants) — copy the relevant function if you want a modified
  version rather than trying to override just the numbers.
- Network sync here is a good real-world example of the "local effect immediately, sync to other players
  separately" pattern also used in [the co-op chat feature](../deep-dives/coop-chat) — `AlarmActivated`
  applies the effect on the activating machine directly, and `Net.SendCustomEvent` is purely to inform
  other players, who apply the same effect through `NetSafeAlarmActivated` instead of receiving it back
  themselves.
