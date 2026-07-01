---
title: MrxCrateDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDelivery
tags: [support, delivery]
---

# MrxCrateDelivery

*Module: mrxcratedelivery.lua*

## Overview
The `MrxCrateDelivery` module is a specialized support delivery system for ground-based cargo drops. It inherits from the base `MrxSupportDelivery` class and adds specific behaviors such as ground drop-zone validation, blue smoke markers, and disabling anti-aircraft (AA) tests.

## Inheritance
- Inherits from: `MrxSupportDelivery`
- Imports: `MrxSupportDesignator`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It extends the functionality of `MrxSupportDelivery` without adding new state fields. The instance primarily manages the delivery process, including setting up the cargo and vehicle, configuring the designator, and handling specific validation logic.

## Functions
### `Create(oSelf, uOwnerGuid)`
Constructs a new per-instance table for the crate delivery system. It initializes the base support delivery with the specified owner GUID, sets the cargo to deliver, configures the delivery vehicle, and applies specific settings such as ground drop-zone validation, blue smoke markers, and disabling AA tests.

## Events
- Listens for `Event.ObjectHibernation` (inherited from `MrxSupportDelivery`) to call `Awake` when the object leaves hibernation.
- Inherits other event handling functions from `MrxSupportDelivery`.

## Notes for modders
- Ensure that the `Create` function is called with the appropriate owner GUID to properly initialize the delivery system.
- Customize the cargo and vehicle by setting the `sCargoToDeliver` and `sDeliveryVehicle` fields before calling `Create`.
- The ground drop-zone validation ensures that the drop location is suitable for a ground-based delivery. Modders should be aware of this behavior if they need to override or extend it.
- Blue smoke markers are used during the delivery process, which can be useful for visual feedback in the game world.
- Disabling AA tests means that anti-aircraft defenses will not interfere with the delivery process, which is specific to ground-based deliveries.