---
title: PmcCon013
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon013

## Overview
PmcCon013 is a helicopter-winch skill challenge: board one of two named copters, then hover a winched object steadily at a target altitude (which rises with each replay, capped at 7 units above a fixed baseline) within a small radius for several seconds straight, all inside a 5-minute time limit. It's built around the game's winch mechanic and ties directly into the winch tutorial message.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxGuiHudMessage`, `MrxMusic`, `MrxTimer`, `MrxUtil`, `MrxAchievements`, `MrxTutorialManager`

## Instance pattern
A native `MrxTaskContract` subclass. Uses `self.bStarted`/`self.nCopterDead` as real instance fields (an exception to this file's otherwise bare-global state, which includes the height-polling counters `nTicks`, `nPrevHeight`, `nTargetHeight`, `nRadius`, and the mission timer `oMissionTimer`).

## Functions
### `Activated(self)` / `Start(self)`
Waits for the local player to wake, then disables normal player-use on two named copters and creates a "board either copter" objective leading to `StartTheShallenge` (the misspelling — "Shallenge" for "Challenge" — is preserved as written in the source).

### `StartTheShallenge(self)`
Guards against double-starting via `self.bStarted`. Auto-completes the vehicle-enter objective after 0.5s, shows the winch tutorial message for 7s, arms a persistent watch for the copter's death, starts special music, computes `nTargetHeight` (`5 + completions`, capped at 7), starts a 5-minute mission timer, creates the actual height objective, begins polling height every 0.25s (`PollHeight`), and adds a HUD marker disc (replicated to clients if hosting).

### `PollHeight(uGuid)` / `DisplayProgress(...)`
Computes height above the baseline Y; requires the object to hold roughly steady at/above the target height, un-winched, and within `nRadius` (10 units) of the marker for several consecutive ticks (effectively ~3 seconds) before completing the objective. `DisplayProgress` colors the HUD text green once above target and shows an out-of-bounds warning otherwise.

### `Complete(self)` / `Cleanup(self)` / `CopterDestroyed(self)`
`Complete` grants `ACHIEVEMENT_BALLS_TO_THE_WALL` on the third completion before calling the base `Complete`. `Cleanup` stops music, clears HUD slots, removes the marker (with net replication), stops the mission timer, and removes the MP layer. `CopterDestroyed` tolerates the loss of one of the two co-op copters but cancels the contract if a second one is destroyed.

## Events
- `Event.ObjectHibernation` — waits for the local player to wake before starting.
- `Event.TimerRelative` — the auto-complete delay, tutorial-message timeout, and the 0.25s height-polling tick.
- `Event.ObjectDeath` — the persistent copter-destruction watch.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- `PollHeight`'s "stay steady near/above a target height, un-winched, within a radius, for N consecutive ticks" logic is a reusable pattern if you're building a similar hover/precision-based objective.
- No direct `MrxPmc` calls in this file — the challenge is purely about winch mechanics, not economy.
