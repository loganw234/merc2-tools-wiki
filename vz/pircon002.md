---
title: PirCon002
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PirCon002

## Overview
PirCon002 is a smuggling-delivery contract: the player drives a truck carrying 24 jugs of rum ("RumJug" props on the truck bed) to a drop-off point while pursued by custom Oil Company (OC) vehicles. The mission fails if too many jugs fall off along the way — the minimum needed to succeed rises with each replay (5, then 9, then 16 of the 24), and OC's pursuit vehicles get correspondingly tougher. A full, untouched delivery pays a large flat bonus on top of the per-jug cash reward; co-op adds a second truck and doubles every count.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxFactionManager`

## Instance pattern
A native `MrxTaskContract` subclass. Nearly all state is bare module-level globals rather than fields on `self`: cargo counters (`nGoods`, `nGoods1`, `nGoods2`, `nCargoValue = 950`, `nRequired`), delivery bookkeeping (`nGoodsDelivered`), the pickup truck list (`tPickups`), and co-op flags (`bClientwasIn`).

## Functions
### `Activated(self)`
Sets up the cargo counters and, based on `self:GetNumCompletions()`, scales `nRequired` (5/9/16) and the intro banter lines. Calls `SetupMPGame` in co-op. Creates the "enter the truck" objective (`MrxTaskObjectiveEnterVehicle`), which leads to `DeliverObjective` on completion, and a proximity event that starts the cargo-loss watch (`StartCheckingCargo`).

### `StartCheckingCargo(self)`
Arms a persistent 2s timer that calls `CheckGoodsLost`.

### `DeliverObjective(self)`
Picks an OC custom-pursuit vehicle table scaled by completion count (progressively adding gun trucks and a helicopter), sets the HUD's required-cash text, and creates the actual `MrxTaskObjectiveDeliver` to the drop-off. Clears the pursuit lock and stops the special music once the truck is close to the destination.

### `CheckGoodsLost(self)`
Counts remaining "RumJug" props on the truck bed(s) via a hardpoint-area query and updates `nGoods`; calls `DisplayGoodsLost` whenever the count drops.

### `_PlayRandomVO(self, tVOs)`
A random-line-from-table VO helper. Not called anywhere else in this file — likely unused here.

### `DisplayGoodsLost(self)`
Refreshes the HUD cash estimate, plays milestone warning VO at 18/11/6 jugs remaining, and — if the count drops below `nRequired` — plays a "we lost the cargo" line and cancels the contract.

### `ActivateDelivered(self)` / `CountDelivered(self)`
Co-op-only "final talk" objective, then the real delivery tally: counts jugs actually present near the drop-off, awards `nGoodsDelivered * nCargoValue` split appropriately for solo/co-op, plus a flat 2,000,000 bonus for a perfect (all-24, or all-48 in co-op) delivery. Completes if at least one jug arrived, otherwise cancels.

### `SetupMPGame(self)`
Adds a second pickup truck, doubles the goods counters, and sets up a cancel-on-death watch plus an idle AI goal for the "end talk" NPC used by the co-op ending.

### `Cleanup(self)`
Clears the two HUD slots, tears down the MP layer if used, clears the custom pursuit, stops the music, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectProximity` — starts the cargo-loss timer near the truck; clears pursuit lock and stops music near the drop-off.
- `Event.TimerRelative` — the persistent 2s cargo-check tick (`CheckGoodsLost`), and one-shot cancel delays after a "lost the goods" VO line.
- `Event.ObjectDeath` — cancels the contract if the co-op "end talk" NPC dies before being reached.
- `Event.ObjectHibernation` — sets the co-op "end talk" NPC idle once it wakes.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Several cancel messages and VO lines in this file reference `[PirCon003.Terms.*]` / `[PirCon003.Objectives.*]` localization keys rather than `PirCon002`-prefixed ones (e.g. the `fOnCancel` handlers on both child objectives, and the required-cash HUD text). This looks like a copy-from-PirCon003 authoring artifact preserved faithfully from the original source rather than a decompiler error — the keys still resolve, they're just mislabeled.
- The rival faction here is the Oil Company (`OC`), not `VZ` — worth knowing if you're comparing pursuit-scaling patterns against other pirate contracts (PirCon003/004 use `VZ`).
- `nRequired` is a *floor*, not a total: cargo starts at 24 (48 in co-op) regardless of difficulty: only the minimum you're allowed to lose changes between replays.
