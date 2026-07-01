---
title: Hackybench
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Bench
tags: [hack, bench]
---

# Hackybench

*Module: hackybench.lua*

## Overview
The `Hackybench` module is a specialized version of the `Bench` module. It inherits from `Bench` and overrides its `Use` function to provide custom behavior when interacted with by players.

## Inheritance
- Inherits from: `Bench`
- Imports: none

## Instance pattern
This module follows the per-instance object pattern (keyed by `uGuid`) inherited from `Bench`. It does not introduce any additional state fields beyond those defined in `Bench`.

## Functions
### `Use(aiguid, floatval)`
Overrides the `Use` function from the `Bench` module. Currently, this function is empty and does nothing when called.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation (inherited from `Bench`).
- Listens for `OnUse` to trigger the `Use` function when the player interacts with the object (inherited from `Bench`).

## Notes for modders
- This module is a placeholder or template that extends the functionality of `Bench`. The current implementation of the `Use` function does nothing.
- To extend this module, you can override the `Use` function with custom logic to provide specific behavior when players interact with the object.
- Ensure that any modifications to the `Use` function do not interfere with other interactions or game mechanics.