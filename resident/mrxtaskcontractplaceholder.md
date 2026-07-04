---
title: MrxTaskContractPlaceholder
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskContract
tags: [task, contract]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskContract](mrxtaskcontract) for the general mechanism.
---

# MrxTaskContractPlaceholder

*Module: mrxtaskcontractplaceholder.lua*

## Overview
The `MrxTaskContractPlaceholder` module is a stub implementation of a task contract. It provides a placeholder sequence to indicate that the contract is not yet implemented, and automatically completes upon activation.

## Inheritance
- Inherits from: `MrxTaskContract`
- Imports: `MrxCinematic`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskContract`](mrxtaskcontract)'s class-factory pattern** (itself
inherited from [`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general
mechanism), identified by name/lineage rather than a world-object GUID. It does not track any additional
state beyond what is inherited from `MrxTaskContract`.

## Functions
### `Activated(self)`
Called when the task contract instance is activated. It first calls the base class's `Activated` method and then triggers a placeholder cinematic sequence with a message indicating that the contract is not yet implemented. The sequence automatically completes the contract.

## Events
- Listens for none, as it does not subscribe to any engine events.

## Notes for modders
- This module is intended as a placeholder and should be replaced with a fully functional task contract implementation.
- Ensure that `OnActivate` is called appropriately to trigger the placeholder sequence.
- The placeholder sequence automatically completes the contract, so there are no additional steps required beyond activation.