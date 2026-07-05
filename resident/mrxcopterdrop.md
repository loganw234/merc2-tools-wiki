---
title: MrxCopterDrop
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, delivery]
verified: true
verified_note: 'spot-checked in deeper pass, confirmed accurate; cross-linked MrxSupport, noted the hardcoded 0.5 Ai.Deliver drop height, and clarified this is the standalone coordinate-driven cousin of MrxSupportDelivery (not part of the catalog inheritance chain)'
---

# MrxCopterDrop

*Module: mrxcopterdrop.lua*

## Overview
The `MrxCopterDrop` module is responsible for managing the delivery of cargo using helicopters. It handles
the spawning of both the helicopter and the cargo, deploying the winch to attach the cargo, and ensuring the
delivery process completes successfully.

Unlike the catalog-driven [`MrxSupportDelivery`](mrxsupportdelivery) family, this is a **standalone,
function-call helper**: a mission script calls `MrxCopterDrop.Create(sFaction, sCargo, nDesX, nDesY, nDesZ,
...)` with explicit coordinates and gets back the spawned heli/cargo GUIDs. It runs the same winch-and-drop
sequence but has no designator, no cost/recruit gating, and no per-instance object — it borrows only
`GoHome` from [`MrxSupport`](mrxsupport).

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxSupport`](mrxsupport)

## Instance pattern
This is a stateless manager/utility module — no `OnActivate`/`Awake`/`tInstance`/`setmetatable` anywhere
in the file. It does carry a handful of module-level globals rather than a per-`uGuid` table:
- `nAltitude` = `25` **is** read inside `Create`, as the default height offset passed to
  `Pg.FindPointFromCamera(nSpawnDistance, nAltitude, 10)` and in the `nTargetY < nDesY + nAltitude`
  comparison, both only when the caller doesn't supply `nTargetX` explicitly.
- `sDeliveryVehicle` = `"UH1 Transport (PMC) (Driver)"`, `sCargoToDeliver` = `"box"`, and `uCargoToDeliver`
  (resolved once at load time via `Pg.GetGuidByName(sCargoToDeliver)`) are **not** referenced by any
  function body in this file — `Create` takes its own `sCargo`/`sFaction` arguments instead, so these
  three look like unused leftover defaults/dead config.
- `Create` builds a local `tCopterData` table mapping faction codes (`AL`, `CH`, `GR`, `OC`, `PR`, `VZ`,
  `VZH`, `VZHF`, `VZF`) to helicopter template names, falling back to `"Ka29b (Driver)"` if the faction
  isn't found.

## Functions
### `Create(sFaction, sCargo, nDesX, nDesY, nDesZ, bCareless, nTargetX, nTargetY, nTargetZ)`
Spawns a helicopter and cargo for delivery. It checks if the current client is the server, retrieves GUIDs for the cargo and helicopter templates based on the faction, spawns the objects at appropriate positions, and sets up events to handle the winch deployment and cargo attachment.

### `_DeployWinch(uHeli, uCargo, nDesX, nDesY, nDesZ, bCareless)`
Called when the helicopter is awake. It deploys the winch on the helicopter and sets up a timer event to wait for the cargo to become active before proceeding with further delivery steps.

### `_WaitCallback(uHeli, uCargo, nDesX, nDesY, nDesZ, bCareless)`
Called after the cargo becomes active. It aligns the cargo's yaw with the helicopter's, attaches the cargo
to the winch, and issues `Ai.Deliver(driver, nDesX, nDesY, nDesZ, 0.5, bCareless)`. **The drop height is
hardcoded to `0.5` here** (unlike [`MrxSupportDelivery`](mrxsupportdelivery), which stores it as
`self.nCargoDropHeight`) — there's no parameter to change it without editing this line.

### `DeliveryComplete(uHeli)`
Called when the delivery is complete. It detaches the cargo from the winch and calls a function from `MrxSupport` to return the helicopter home.

**Confirmed in source:** this function does `self = {}` with no `local` keyword, which assigns to the
*global* `self` rather than creating a function-local table. It then passes that table to
`MrxSupport.GoHome(self, uHeli)`. Functionally this still works (an empty table is a valid throwaway
first argument for `GoHome`), but it pollutes the global namespace with a `self` that any other file's
top-level code could read or clobber — likely a copy-paste artifact from a method body (where `self`
would normally arrive as an implicit parameter) rather than deliberate design.

## Events
- Listens for `Event.ObjectHibernation` to deploy the winch when the helicopter becomes active.
- Listens for `Event.TimerRelative` to wait for the cargo to become active before proceeding with further delivery steps.
- Listens for `Event.ObjectWinched` to detach the cargo from the winch after the delivery is complete.

## Notes for modders
- Ensure that the server is handling the creation of helicopter and cargo objects to maintain consistency across multiplayer sessions.
- Customize the faction and cargo types by modifying the local `tCopterData` table inside `Create`. The module-level `sDeliveryVehicle`/`sCargoToDeliver`/`uCargoToDeliver` globals are dead — not read by any function in this file — so editing them has no effect. `nAltitude` (25), by contrast, is live: it's the default vertical offset `Create` uses via `Pg.FindPointFromCamera` when the caller omits `nTargetX`, so changing it does change drop-point selection.
- Be aware that network synchronization (`Net.IsClient()`) may affect the behavior in multiplayer environments — `Create` returns immediately with no value on the client.
- The `_DeployWinch` and `_WaitCallback` functions are internal helpers and should not be called directly by modders.