---
title: FoodCart
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 2-line file, single stub Use function confirmed, no events/inheritance in source; page was already accurate
---

# FoodCart

*Module: foodcart.lua*

## Overview
The `FoodCart` module is a utility script designed to handle interactions with food carts in the game. It currently defines a single function, `Use`, which is intended to manage player interactions with food carts.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state or use the `uGuid` keying pattern.

## Functions
### `Use(aiguid, floatval)`
A placeholder function that currently does nothing (empty body). It takes two arguments, `aiguid` and `floatval`, but no implementation is provided. This is the only function defined in the file.

## Events
- none

## Notes for modders
- This module is currently a stub with no functionality. Any custom behavior related to food cart interactions should be implemented within the `Use` function.
- Be cautious when extending this module, as it does not follow the standard per-instance pattern used by other modules in the corpus.