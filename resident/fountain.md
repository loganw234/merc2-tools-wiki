---
title: Fountain
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: all 4 functions confirmed against source (QueryActiveUse, Use, SuperUse, QueryRepair); no events, no inheritance; page was already accurate
---

# Fountain

*Module: fountain.lua*

## Overview
The `Fountain` module provides utility functions for querying and handling interactions with fountains in the game world. It includes methods to determine active uses, handle use actions, and query repair states.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state.

## Functions
### `QueryActiveUse(intVal)`
Determines the active use type based on the input integer value. If `intVal` is 1, it returns `"SuperUse"`. Otherwise, it returns an empty string.

### `Use(floatval, aiguid)`
Handles the general use action for the fountain. Empty body — takes both arguments but does nothing with them.

### `SuperUse(floatval, aiguid)`
Handles the super use action for the fountain. Empty body, same as `Use`.

### `QueryRepair(intVal)`
Queries the repair state based on the input integer value. Ignores `intVal` entirely and always returns an empty string.

## Events
This module does not listen for or fire any engine events.

## Notes for modders
- The `Use` and `SuperUse` functions are currently placeholders without implementation. Modders should extend these functions to add desired behavior.
- The `QueryActiveUse` function can be used to determine the type of use action being performed on a fountain.
- The `QueryRepair` function is always empty, indicating no repair functionality by default.