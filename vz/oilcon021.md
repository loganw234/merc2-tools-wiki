---
title: OilCon021
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 6
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# OilCon021

## Overview
An Oil Company story contract to recover a named heavy vehicle nicknamed "the Devastator" (a truck object
internally called `MailTruck`). The player talks to a contact, then either finds the truck early
(triggering an alternate branch) or gets formally handed it, escorts it home while OC mercs mock whichever
co-op hero is driving through a multi-stage taunt dialogue, and wraps with a laughing-soldiers flourish at
the delivery point.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxVoSequence`, `DangerousBuilding`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Bare-global flags gate the two entry paths: `bEarlyFind` (player spotted the truck before finishing the
initial conversation), `bTalked` (conversation completed), `nAlreadyHeard` (mocking-dialogue encounter
counter). Character-specific VO line names (`sFoundVO`/`sMockVO1`-`5`/etc.) are picked via
`Object.HasLabel(uTalked, "Mattias"/"Jennifer"/"Chris")` throughout, since the escorting hero can be any of
the three co-op characters.

## Functions
### `Activated(self)`
Disables all `DangerousBuilding` spawns, makes a "psych" vehicle unusable, kills a pre-placed decoy truck
after 2s, and creates the initial "talk to the contact" `MrxTaskObjectiveAction`. Arms watchers for the
truck sinking/dying (`TruckLost`), the contact going hostile early (`CheckForHostile`, via
`SetupContactGuy`), spotting the truck up close before talking (`SpottedDevastator`), and a separate
"drop point destroyed" cancel trigger.

### `SetupContactGuy(self)` / `Seated(self)` / `Conversation(self, tPlayerTalker)` / `KeepFacing`/`Turn`/`Speak`
A small AI-choreography chain: the contact sits down, stands and faces the player when approached, and
holds that facing (re-arming itself every 4s) until the actual talk-to interaction fires `Speak`.
`CheckForHostile` polls (every 1s) whether the contact's feeling toward the local player has dropped below
-33 and, if so, aborts the conversation setup and cancels the contract early.

### `SetupDeliverTruck(self, uTalked)` / `EarlyFind(self)` / `DeliverTruckObjective(self)`
`SetupDeliverTruck` runs once talking completes normally: plays a character-specific "handoff" VO line,
has the contact perform an exit gesture/animation, then calls `DeliverTruckObjective`. `EarlyFind` is the
alternate path if `SpottedDevastator` fires before `bTalked` is set — it force-completes the talk objective
quietly (`bDsp = false`) and jumps straight to the same `DeliverTruckObjective`. `DeliverTruckObjective`
creates the actual delivery objective, cues special mission music on boarding, and arms a mocking-VO
trigger and a wrong-vehicle VO trigger (`FionaVOwrong`, if the player boards the decoy "psych" vehicle
instead).

### Mocking dialogue: `SpottedDevastator`, `OndaflyMocking`, `DotheMocking`, `Mocking`
A layered taunt system. `SpottedDevastator` plays a one-time three-line reaction the first time the truck
is seen close-up. `OndaflyMocking` polls every 12s for a living OC human near the truck and, once found,
hands off to `DotheMocking`, which picks distinct (character-specific) VO for the 1st, 2nd, 4th, and 6th
encounter and falls back to a random pool afterward — keyed by `nAlreadyHeard`. `Mocking` is a separate,
simpler proximity-triggered laughing-animation cue near a named laugh-point cluster.

### `Cleanup(self)`
Deletes the early-conversation-interrupt event if still armed, restores `DangerousBuilding` rarity to
default, then calls `MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectDeath` (truck lost, drop-point destroyed), `Event.ObjectPhysicsEvent`
(`"VehicleSinking"`, also routes to `TruckLost`), `Event.ObjectProximity` (contact approach, truck spotted,
mocking-trigger proximity, psych-vehicle boarding is via `ObjectInSeat` instead), `Event.ObjectInSeat`
(boarding the Devastator / the decoy vehicle), `Event.TimerRelative` (contact-hostile poll, facing
re-arms, mocking poll, animation delays).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The `Object.HasLabel(uGuid, "Mattias"/"Jennifer"/"Chris")` pattern used throughout to pick
  character-specific VO is the standard way this corpus handles "any of the co-op heroes could be doing
  this" dialogue — reuse it directly if your mod needs a line spoken by whichever hero triggers an event.
- `NetEventCallback` in this file is an empty stub even though `Net.SendCustomEvent("OilCon021", ...)` is
  called elsewhere — the send side is wired up but nothing consumes it on receipt. The same
  never-finished-net-hook pattern also appears in [OilCon001](oilcon001).
