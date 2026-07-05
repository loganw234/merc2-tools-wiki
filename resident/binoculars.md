---
title: Binoculars
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: spot-checked against source, no changes needed.
---

# Binoculars

*Module: binoculars.lua*

## Overview
The `Binoculars` module is a utility script that handles the functionality of binoculars in the game. It provides a function to simulate using binoculars, which could include adjusting zoom levels or activating specific visual effects.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless utility module (no `uGuid`). It does not track any per-instance state.

## Functions
### `Use(aiguid, floatval)`
Simulates the use of binoculars. The function takes two arguments: `aiguid` (likely an AI or player GUID) and `floatval` (possibly a zoom level or other floating-point value). Currently, this function is empty and does not perform any actions.

## Events
This module does not subscribe to or fire any engine events.

## Notes for modders
- The `Use` function is currently a placeholder with no implementation. Modders should extend this function to add the desired functionality when binoculars are used.
- Ensure that any additional logic added to `Use` is compatible with the game's existing mechanics and does not introduce unintended behavior.