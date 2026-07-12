---
title: PirCon003
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PirCon003

## Overview
PirCon003 is a follow-up smuggling-delivery contract in the same mold as PirCon002, this time hauling a truckload of 42 "bird" crates (`BirdBox` props, cargo value 1900 each) past a custom `VZ` pursuit and a pair of "Cliffy" ambush vehicles that path in to block the route. A comedic caged-parrot NPC ("Parrot") provides reactive commentary keyed to the truck's speed and damage state throughout the drive. As with PirCon002, the minimum cargo needed to succeed rises with replays (7/15/25 of the 42), and a perfect delivery pays a large flat bonus.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxTimer`, `MrxFactionManager`

## Instance pattern
A native `MrxTaskContract` subclass, state kept in bare module-level globals: cargo counters (`nGoods`, `nGoods1`, `nGoods2`, `nCargoValue = 1900`, `nRequired`), truck health/speed tracking for the Parrot commentary (`nTruckHealth`, `bParrotVOon`), and co-op flags (`bClientwasIn`).

## Functions
### `Activated(self)`
Scales `nRequired` (7/15/25) and intro VO by completion count, sets up the "enter the truck" objective (leads to `DeliverTruck`), a proximity-triggered `BirdTalk` near the truck, and starts the cargo-loss watch after 3s.

### `StartCheckingBirds(self)`
Arms a persistent 1.5s timer calling `CheckGoodsLost`.

### `BirdTalk(self)`
Plays one of several completion-count-dependent banter sequences (a mix of hero banter and Parrot VO), ending in `ParrotVO`.

### `DeliverTruck(self)`
Picks a `VZ` custom-pursuit table via `DaCustomPursuit` based on difficulty, updates the HUD, and creates the delivery objective to `loc_DeliverySpot`. Also arms `CliffyA` (an ambush trigger) and pursuit-clear/music-stop proximity events near the destination.

### `ParrotVO(self)` / `DamageVO(self)` / `SpeedVO(self)` / `ParrotLostVO(self)` / `ParrotCooldown(self)`
The Parrot commentary system: `ParrotVO` starts polling loops for speeding (`SpeedVO`, re-checks every 5-20s) and truck damage (`DamageVO`, re-checks every 5-15s), each picking a random line from a pool when triggered. `ParrotLostVO` reacts to cargo loss with its own cooldown (`ParrotChat`/`ParrotCooldown`) so lines don't overlap.

### `CliffyA(self)`
Sends two named "Cliffy" vehicles' drivers on delayed `PathMove` goals to block the route.

### `CheckGoodsLost(self)`
Counts remaining `BirdBox` props on the truck bed(s) via a hardpoint-area query; on a drop, calls both `ParrotLostVO` and `DisplayGoodsLost`.

### `DisplayGoodsLost(self)`
Refreshes the HUD estimate and, if goods fall below `nRequired`, cancels via a nested helper `_TooManyBirdsLost` that this function (re)defines as a *global* every time it runs (see Notes).

### `ActivateDelivered(self)` / `CountDelivered(self)`
Co-op "final talk" objective, then the delivery tally and reward split, matching PirCon002's pattern but with the 42/84-count perfect-delivery bonus.

### `SetupMPGame(self)`
Adds the second truck, doubles goods counters, and sets up the co-op "end talk" NPC's cancel-on-death and idle-on-wake events.

### `Cleanup(self)`
Clears HUD slots, tears down the MP layer, clears custom pursuit, stops music, calls base `MrxTaskContract.Cleanup`.

### `DaCustomPursuit(self, nLevel)`
Builds one of three escalating `VZ` pursuit-vehicle tables (`nLevel` 0/1/2, matched to completion count in `DeliverTruck`) and applies it via `MrxFactionManager.SetCustomPursuit`.

## Events
- `Event.ObjectProximity` — near the truck triggers `BirdTalk`; past/near key waypoints triggers `DaCustomPursuit`, pursuit-clear, and `CliffyA`.
- `Event.TimerRelative` — drives the Parrot VO polling loops, the 1.5s cargo-check tick, and staged banter delays.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- `DisplayGoodsLost` declares `function _TooManyBirdsLost(...)` *inside itself* rather than at file scope — since it's a bare (global) function definition, each call to `DisplayGoodsLost` re-creates that global. It's harmless in practice (Lua allows redefining globals freely) but is a real oddity worth knowing if you're tracing control flow rather than a decompiler mis-render.
- Rival faction here is `VZ` (contrast PirCon002's `OC`); `DaCustomPursuit`'s three tables are worth a look if you want a template for scaling pursuit difficulty by replay count.
- Same cargo-floor pattern as PirCon002: total cargo is always 42 (84 co-op); only the minimum you're allowed to lose changes between replays.
