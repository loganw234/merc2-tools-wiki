---
title: Bench
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: spot-checked against source, no changes needed.
---

# Bench

*Module: bench.lua*

## Overview
The `Bench` module provides utility functions for querying repair actions and handling object interactions. It defines methods to determine specific use actions based on input values and includes placeholders for actual implementation of those actions.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module with no per-instance tables or fields.

## Functions
### `QueryRepair(intVal)`
Determines the repair action based on the input integer value. If `intVal` is 1, it returns "MakeUpright". Otherwise, it returns an empty string.

### `QueryActiveUse(intVal)`
Determines the active use action based on the input integer value. If `intVal` is 1, it returns "SuperUse". Otherwise, it returns an empty string.

### `SuperUse(floatval, aiguid)`
Placeholder function for handling the "SuperUse" action. Currently does nothing.

### `Use(aiguid, floatval)`
Placeholder function for handling general use actions. Currently does nothing.

### `MakeUpright(objectguid, aiguid)`
Placeholder function for making an object upright. Currently does nothing.

## Events
This module does not listen to or fire any engine events.

## Notes for modders
- The `QueryRepair` and `QueryActiveUse` functions can be used to determine specific actions based on input values.
- Implement the `SuperUse`, `Use`, and `MakeUpright` functions to define the actual behavior for these actions.