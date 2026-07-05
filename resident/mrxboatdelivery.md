---
title: MrxBoatDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDelivery, MrxSupportDesignatorFlare
tags: [support, delivery, boat]
verified: true
verified_note: 'deeper pass: confirmed this is a thin 12-line subclass of MrxSupportDelivery -- only override is a flare designator with AA test "none"; replaced vacuous "ensure Create is called" notes with the real inherited-behavior + cross-links, and documented the SetCargo-from-caller-prototype pattern'
---

# MrxBoatDelivery

*Module: mrxboatdelivery.lua*

## Overview
`MrxBoatDelivery` is the water-drop variant of the standard helicopter cargo delivery. It's a very thin
subclass of [`MrxSupportDelivery`](mrxsupportdelivery) — the entire file is one `Create` function. All the
real work (spawn cargo, spawn heli, winch, fly to target, drop) is inherited from
[`MrxSupportDelivery`](mrxsupportdelivery); the only thing this module changes is swapping the smoke
designator for a **flare** designator with anti-air testing disabled, which suits a marker dropped over open
water. [`MrxSupportData`](mrxsupportdata) uses it for every `Boat`-type catalog item (jetskis, speedboats,
the PMC patrol boat, etc.).

{: .note }
> The `inherit("MrxSupportDesignatorFlare")` line is effectively unused: `Create` creates the flare
> designator explicitly via `MrxSupportDesignatorFlare:Create()`, it doesn't inherit designator *methods*.
> Behaviorally this is a `MrxSupportDelivery` with a flare designator bolted on.

## Inheritance
- Inherits from: [`MrxSupportDelivery`](mrxsupportdelivery), [`MrxSupportDesignatorFlare`](mrxsupportdesignatorflare)
- Imports: none

## Instance pattern
**Same class-factory pattern as [`MrxSupportDelivery`](mrxsupportdelivery)/[`MrxSupportDesignatorFlare`](mrxsupportdesignatorflare),
not per-`uGuid`** — `Create(oSelf, uOwnerGuid)` builds a new table via `setmetatable`/`__index`, exactly
like its parents. No `OnActivate`/`Awake`, no `tInstance` registry. It tracks the following key fields:
- `sCargoToDeliver`: The type of cargo to be delivered.
- `oDesignator`: The designator used for marking the drop zone.

## Functions
### `Create(oSelf, uOwnerGuid)`
The only function in the file. Calls `MrxSupportDelivery:Create(uOwnerGuid)` to build the base delivery
object, then: copies the caller-prototype's `sCargoToDeliver` via `SetCargo(oSelf.sCargoToDeliver)`, sets
the module name to `"MrxBoatDelivery"`, creates a [`MrxSupportDesignatorFlare`](mrxsupportdesignatorflare)
with `SetAATestLevel("none")`, and installs it as the designator (replacing the blue-smoke one the parent
`Create` set up). Returns the new support object.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

`oSelf.sCargoToDeliver` reads the cargo name off the *prototype table* the catalog set up (e.g.
`oSupport:SetCargo({"Dinghy", ...})` in [`MrxSupportData`](mrxsupportdata)), and `SetCargo` here copies it
onto the freshly built instance. That's why the boat items in the catalog configure cargo on the object
*before* it ever runs — the value is read back out at `Create` time.

</details>

## Events
None of its own — every event subscription (`Event.ObjectHibernation` for the heli/cargo wake, and
`Event.ObjectWinched` for the drop) comes from [`MrxSupportDelivery`](mrxsupportdelivery)'s
`_DesignatorCallback` → `_DeployWinch` → `_WaitCallback` → `CargoDropped` chain. See that page for the full
delivery sequence.

## Notes for modders
- **What to change lives on the parent, not here.** Drop height, the delivery helicopter template, cargo
  picking, and the actual winch sequence are all on [`MrxSupportDelivery`](mrxsupportdelivery) — this file
  only chooses a flare designator with AA disabled.
- **Cargo is set by the caller's prototype.** The catalog (`[MrxSupportData](mrxsupportdata)`) sets
  `SetCargo(...)` and `SetCareless(true)` on the prototype; `Create` copies the cargo across. To change what
  a boat item delivers, change the catalog entry's cargo (or set `sCargoToDeliver` on the prototype before
  `Create`), not a field on the returned instance.
- **Flare vs. smoke over water**: the flare designator + `SetAATestLevel("none")` is the water-specific
  choice. If you clone this for a land drop you'd typically want smoke and a ground-drop-zone validation
  function instead — see [`MrxCrateDelivery`](mrxcratedelivery) for that shape.