---
title: Barbell
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: spot-checked against source (3-line file), no changes needed.
---

# Barbell

*Module: barbell.lua*

## Overview
The `Barbell` module provides a utility function to detach the barbell from an object that is holding it. This is likely used in scenarios where a player or another entity releases the barbell.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance fields.

## Functions
### `UnUse(objectGuid, holdersGuid)`
Detaches the barbell identified by `objectGuid` from the object that is holding it, identified by `holdersGuid`. This function is called when the barbell is released or detached from its holder.

## Events
- Listens for: none — this module does not subscribe to any engine events

## Notes for modders
- Ensure that `UnUse` is called appropriately when the barbell needs to be detached from its holder.
- This function is a simple utility and does not have any additional side effects or dependencies.