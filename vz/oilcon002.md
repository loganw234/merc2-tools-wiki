---
title: OilCon002
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# OilCon002

## Overview
An Oil Company story contract built around the support-call character Ewan (registers `WifBios`
dossier entry `"BioEwan"` on activation). The player plants listening-post equipment at up to three hidden
locations (revealed through a minimap "hacking" minigame), then a VZ convoy kidnaps an OC executive in one
of four candidate vans; the player has to spot the van, hijack it (or catch up after killing its driver),
deliver the hostage to a rescue site, board a rescue helicopter ("Lucky Lady"), and transit back to a
PMC/Oil location for an epilogue. Extensive checkpoint/recovery logic lets the whole delivery phase resume
correctly after a save/reload, including recreating an in-progress mission timer.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxLayerManager`, `MrxOilCon002Delivery`, `MrxSupportData`, `MrxTimer`,
  `MrxGuiPda`, `MrxPlayer`, `MrxTransit`, `MrxTutorialManager`, `MrxUtil`, `DangerousBuilding`,
  `MrxFuelAirBomb`, `MrxPmc`, `MrxCinematic`, `MrxTaskObjectiveDestroy`, `WifBios`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Almost entirely bare (non-`local`) globals rather than `self`-scoped fields: location GUIDs
(`oPostLoc01`-`03`, `uRescueLoc`), the delivery-progress bookkeeping (`tCompletedLoc`, `tCompPosts`,
`nPartsComplete`, `nTotal`, `nReset`), the kidnap-van state (`uTargVan`, `uVZDriver`, `uVZShotgun`,
`uHostage`), and three network-event constants (`NETEVENT_STARTHACK`/`STOPHACK`/`MOVE_LUCKY_LADY`) used
with `Net.SendCustomEvent("OilCon002", ...)` to keep the minigame/vehicle-teleport in sync across coop
clients.

## Functions
### `Activated(self)` and the delivery/checkpoint branch
Sets up locations, van list, and per-post VO line sets, then branches three ways on saved flags:
`AllPostsPlaced` (delivery phase already finished before a checkpoint — reconstructs the mission timer
from the saved remaining seconds and re-spawns the listening posts), `PartPostsPlaced` (mid-delivery
checkpoint — `RecoverPostsStatus`), or neither (fresh start — `StartPostDeliveryObjective`). Also arms a
garage-machinegunner ambush trigger and a VZ helicopter pilot who spawns, boards, and starts patrolling once
the player nears the airport.

### `StartPostDeliveryObjective(self)` / `RecoveryObjective(self)` / `AddPostDelivery`/`ResetPostDelivery`
Builds the master 3-part delivery objective (`MrxTaskObjectiveDeliver` children, one per drop zone from
`MrxOilCon002Delivery.GetCurrentDropZones()`), each watched by a proximity pair
(`AddPostDelivery`/`ResetPostDelivery`) that grants/revokes an `"OilCon002_Delivery"` freebie support call
depending on whether a Listening Post is currently near that zone. `RecoveryObjective` is the
checkpoint-resume equivalent, seeded from `RecoverPostsStatus`'s decoded state.

### `SubDeliveryComplete(self, sLocation)` / `AllPostsCheck(self)` / `PartPostsCheck(self)` / `RecoverPostsStatus(self)`
The checkpoint math: each of the three drop zones is worth 100/10/1 respectively, summed into
`nPartsComplete` as a base-10-like status code (e.g. `110` = zones A and B done, C pending).
`PartPostsCheck`/`AllPostsCheck` save that code via `_SetFlag`; `RecoverPostsStatus` decodes it back with a
hardcoded 6-branch table (`100`/`10`/`1`/`110`/`11`/`101`) into "already-done" vs. "still-remaining" zone
lists on reload.

### `LoadVansLayer(self)` / `StartVansMoving(self)` / `HostageInVan` / `StartHijackObjective` / `StartRescueObjective` / `PlayerInVan` / `TransitStart`
The kidnap sequence proper: once all three posts are placed, extra objective layers load and the pending
delivery sub-objectives are cancelled (the delivery and kidnap phases are mutually exclusive in the UI even
though both objective sets exist in code). A random van from `tVanList` becomes the kidnap target;
`HostageInVan` spawns the hostage and puts them in it once the player is close. Killing the van's driver or
getting the player into the van both advance to the hijack objective; from there the flow chains through
rescue delivery, a "Lucky Lady" helicopter pickup, and `MrxTransit`-driven relocation to the epilogue.

### Hack minigame: `NetSafeStartHack`, `StartHack`, `HackVans`, `HackRand`, `StopHack`
Minimap/HUD-radar blip choreography revealing the three listening-post locations, then the van list, then a
recurring random single-van "ping." `NetSafeStartHack` is the network-safe half (blips without re-sending
the custom net event) used both by the normal path and by late-joining/recovering clients; `StartHack` is
the full version that also calls `Net.SendCustomEvent`. `HackRand`'s recursive re-blip uses an
ever-incrementing iteration number purely to give each blip a unique name, not for any counting logic.

### `GetHostageSeat(self, uTruck)`
Defined but never called — `HostageInVan` computes the shotgun's seat directly via
`Vehicle.GetSeatFromRider` instead. Dead code.

### `Cleanup(self)`
Removes the Lucky Lady helicopter (once hibernated), stops both hack blip sets, removes any lingering
Listening Posts, resets `MrxTransit`, removes four freebie support entries, marks three layers for removal
(one after a 0.75s delay), then calls `MrxTaskContract.Cleanup(self)`.

### `LoadAssets(self)`
Defined at the very end of the file (Lua doesn't require a function to be declared before its call site
within the same chunk) — adds the two base pristine/state layers.

## Events
`Event.ObjectProximity` (post/van/rescue/exit proximity triggers throughout — by far the most-used event
in this file), `Event.ObjectHealthLessThan` (kidnap van health floor triggers a timeout/cancel),
`Event.ObjectDeath` (van driver, hostage, garage), `Event.ObjectHibernation` (VZ pilot readiness, vehicle
wake gates), `Event.ObjectInSeat` (hostage exiting the van, player boarding the rescue helicopter),
`Event.TimerRelative` (banter delays, the reconstructed mission timer via `MrxTimer`).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- `AllPostsPlaced`/`PartPostsPlaced`'s base-10-digit encoding of "which of 3 things are done" into a single
  saved number is a compact checkpoint pattern worth recognizing elsewhere in this corpus, even though it
  doesn't scale gracefully past a handful of parts.
- The `NetSafe*` vs. full-version function pairing (`NetSafeStartHack` vs. `StartHack`) is a clean way to
  separate "do the visible thing" from "also tell other coop clients to do it," reusable anywhere a
  checkpoint-recovery path needs to replay a visual effect without re-triggering network sync.
