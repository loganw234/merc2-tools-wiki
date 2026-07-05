---
title: MrxCrateDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDelivery
tags: [support, delivery]
verified: true
verified_note: 'deeper pass: corrected the Events section (parent has no "Awake" function; the real chain is ObjectHibernation/ObjectWinched via MrxSupportDelivery), documented that this is the workhorse ground-crate subclass used by ~90 catalog items, and replaced boilerplate notes with the ground-drop-zone-validation + blue-smoke + AA-off specifics'
---

# MrxCrateDelivery

*Module: mrxcratedelivery.lua*

## Overview
`MrxCrateDelivery` is the ground-crate variant of the standard helicopter cargo delivery, and the workhorse
of the supply-drop economy — [`MrxSupportData`](mrxsupportdata) instantiates it for the overwhelming
majority of catalog items (every `Supply` crate, plus most `Light`/`Heavy`/`Civilian` vehicle drops that
arrive winched under a copter). Like [`MrxBoatDelivery`](mrxboatdelivery) it's a thin subclass of
[`MrxSupportDelivery`](mrxsupportdelivery): the whole file is one `Create`. All delivery logic is inherited;
this module only sets a **ground drop-zone validation** function on the designator, blue smoke, and disables
AA testing.

## Inheritance
- Inherits from: [`MrxSupportDelivery`](mrxsupportdelivery)
- Imports: [`MrxSupportDesignator`](mrxsupportdesignator)

## Instance pattern
**Same class-factory pattern as [`MrxSupportDelivery`](mrxsupportdelivery), not per-`uGuid`** —
`Create(oSelf, uOwnerGuid)` builds a new table via `setmetatable`/`__index`, exactly like its parent. No
`OnActivate`/`Awake`, no `tInstance` registry. It extends the functionality of `MrxSupportDelivery` without
adding new state fields. The instance primarily manages the delivery process, including setting up the
cargo and vehicle, configuring the designator, and handling specific validation logic.

## Functions
### `Create(oSelf, uOwnerGuid)`
The only function in the file. Calls `MrxSupportDelivery:Create(uOwnerGuid)` for the base object, then
copies the caller-prototype's cargo (`SetCargo(oSelf.sCargoToDeliver)`), delivery vehicle
(`SetDeliveryVehicle(oSelf.sDeliveryVehicle)`) and careless flag (`SetCareless(oSelf.bCareless)`) onto it.
It then reconfigures the **existing** designator (the blue-smoke one the parent already built — fetched via
`GetDesignator()`, not replaced): installs `MrxSupportDesignator.ValidateGroundDropZone` as the validation
function, sets smoke color `"blue"`, and AA test level `"none"`. Sets the module name and returns the object.

## Events
None of its own. The delivery sequence — `Event.ObjectHibernation` (heli wake, then cargo wake) and
`Event.ObjectWinched` (`"Detach"` → cargo dropped) — is entirely inherited from
[`MrxSupportDelivery`](mrxsupportdelivery)'s `_DesignatorCallback` → `_DeployWinch` → `_WaitCallback` →
`CargoDropped` chain. (There is no `Awake` function anywhere in the parent; an earlier version of this page
claimed one.)

## Notes for modders
- **Cargo/vehicle come from the caller's prototype**, not from fields you set on the returned object. The
  catalog ([`MrxSupportData`](mrxsupportdata)) configures `SetCargo(...)`, optionally
  `SetDeliveryVehicle("Mi26 (PMC) (Driver)")` for heavy vehicles, and `SetCareless(true)` for crates, all on
  the prototype before `Create` copies them across.
- **Ground drop-zone validation** (`MrxSupportDesignator.ValidateGroundDropZone`) is the crate-specific
  gate — a designation over water/invalid terrain is rejected. Swap or clear the validation function on the
  designator if you need to allow other terrain.
- **Drop mechanics live on the parent** — for drop height (and its documented `SetCargoDropHeight` bug),
  cargo random-selection from a list, and the winch/`Ai.Deliver` sequence, see
  [`MrxSupportDelivery`](mrxsupportdelivery).