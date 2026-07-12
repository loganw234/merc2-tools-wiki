---
title: OilCon020
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# OilCon020

## Overview
An Oil Company story contract: gun-running. The player picks up a weapons truck, drives it past several
scripted VZ roadblocks and a pursuit, and delivers it (cargo losses along the way reduce the payout). Woven
through the first act is an elaborate first-time PDA/GPS-beacon contextual tutorial — a full state machine
covering opening the PDA, setting a beacon in the correct target zone, and being nagged/re-prompted until
the player gets it right.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxLayerManager`, `MrxUtil`, `DangerousBuilding`, `MrxFactionManager`,
  `MrxTutorialManager`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Cargo state tracked as bare globals: `nGoods`/`nGoods1`/`nGoods2` (crate counts, split per-truck in coop),
`nCargoValue` (500/crate), a run of `nPlayedVOn` booleans gating one-shot threshold barks, plus one network
event constant, `NETEVENT_CLIENTSETUP`.

## Functions
### `Activated(self)` and cargo pickup
Disables faction-infraction reporting and all "dangerous building" spawns for the duration, makes a staged
getaway jeep unusable until needed, and creates the initial "get in the truck(s)" objective
(`MrxTaskObjectiveEnterVehicle`). Arms a run of proximity triggers along the approach to the truck that
gate the PDA tutorial sequence and an early-warning AI reaction (`AIReact`) once the player gets very close.

### PDA/GPS tutorial state machine: `GPSTuteStart`, `OpenPDA`, `DoTheNag`, `TuteInPDA`, `ValidationFunction`, `BeaconUsed`, `AskToClearBeacon`, `BeaconCleared`, `NowClosePDA`, `GPSTuteDone`
A dedicated first-time-use tutorial covering the PDA/map beacon feature: shows the message, nags with
random VO every several seconds until the PDA is opened, listens for `ScriptEvent("PDA Open"/"PDA Close")`
and `"GPS Beacon Set"/"Cleared"`, validates whether the beacon landed inside a hardcoded target rectangle
(`BeaconUsed`'s `2675 <= nX <= 2825, -500 <= nZ <= -350` check), and either confirms success or asks the
player to clear and retry. `GPSTuteDone` is the teardown that deletes every event handle this chain armed.

### `StageJeep(self)` / `AIReact(self)`
`StageJeep` makes the getaway jeep usable and either sends its AI driver down a path or, if no driver is
present, walks a nearby living VZ soldier over to get in first — recursing via its own callback until a
driver exists. `AIReact` arms a "player backs off" re-nag trigger and starts a boat gunner AI moving into
position.

### `ObjDeliverGoods(self)` / `CartelBlock`/`RoadBlockStop`/`NowBlockerExit`/`BlockerChase`
The delivery run: creates the actual delivery objective, arms proximity-triggered VO at three named
"CartelBlock" trucks, and starts a periodic cargo-loss poll (`DisplayGoodsLost`). The four `CartelBlock*`
functions choreograph a roadblock vehicle driving into position, stopping, then having its occupants bail
— except `BlockerChase` (a "give chase" variant), which has no visible call site anywhere in this file and
looks unused.

### `CheckGoodsLost(self)` / `DisplayGoodsLost(self)`
`CheckGoodsLost` (armed on a persistent 2s timer) checks whether either delivery truck is out of view of
all players and, if so, counts how many `"OilCon020gun"` crates remain on its hardpoint. `DisplayGoodsLost`
rewrites the HUD cash-estimate text every time goods drop and fires escalating one-shot VO barks at fixed
crate-count thresholds (35/25/18/12/9), cancelling the contract outright if the count ever hits 0.

### `ActivateDelivered(self)` / `CountDelivered(self)` / `IntercomResponse(self)`
The delivery-complete tail: an optional "hand off to a contact" beat in coop, then a final crate count at
the drop zone converted straight to cash (halved per player if netplay is active), followed by an intercom
VO reaction tiered by how many crates actually arrived (10+, 1+, or 0 which re-triggers the same cancel
message as running out mid-drive).

### `Cleanup(self)`
Clears the HUD tray slot, tells clients the mission ended (`NETEVENT_CLIENTSETUP2`), forces every player
out of their seat, clears the custom pursuit and re-enables infraction reporting, stops special music,
removes the MP deliverables layer if applicable, and force-closes any lingering PDA tutorial state before
calling `MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectProximity` is by far the dominant event here (tutorial triggers, roadblocks, pursuit
start/stop, AI reactions). Also: `Event.ScriptEvent` (`"PDA Open"/"Close"`, `"GPS Beacon Set"/"Cleared"`),
`Event.TimerRelative` (persistent cargo-loss poll, nag timers, delayed VO), `Event.ObjectHibernation`
(vehicle wake gates), `Event.ObjectDeath` (end-contact death cancel).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The PDA/GPS tutorial state machine here is the most fully-worked contextual-tutorial example in this
  batch — worth reading closely if you want to gate a custom mod objective behind "player must correctly
  use feature X first."
- `BlockerChase` appears to be dead/unused code, similar to the abandoned sub-systems noted in
  [GurCon001](gurcon001)/[GurCon002](gurcon002) — don't assume a defined function fires just because it's
  present.
