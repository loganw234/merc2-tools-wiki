---
title: MrxBoatDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDelivery, MrxSupportDesignatorFlare
tags: [support, delivery, boat]
---

# MrxBoatDelivery

*Module: mrxboatdelivery.lua*

## Overview
The `MrxBoatDelivery` module is a specialized support delivery system for water-based operations. It inherits from both `MrxSupportDelivery` and `MrxSupportDesignatorFlare`, providing functionality to deliver cargo using a boat and a flare designator.

## Inheritance
- Inherits from: `MrxSupportDelivery`, `MrxSupportDesignatorFlare`
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `sCargoToDeliver`: The type of cargo to be delivered.
- `oDesignator`: The designator used for marking the drop zone.

## Functions
### `Create(oSelf, uOwnerGuid)`
Constructs a new per-instance table for the boat delivery support system. It initializes the base delivery system with the owner's GUID, sets the cargo type, module name, and configures the flare designator with no AA test level.

## Events
- Listens for engine events inherited from `MrxSupportDelivery` and `MrxSupportDesignatorFlare`.

## Notes for modders
- Ensure that the `Create` function is called appropriately to initialize the boat delivery system.
- Customize the cargo type by setting the `sCargoToDeliver` field.
- The flare designator is configured with no AA test level, which may affect how it interacts with enemy anti-aircraft systems.