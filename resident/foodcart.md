---
title: FoodCart
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: re-confirmed the 1-line source; clarified Use is an intentionally-empty engine hook (not an Event.* subscription), cross-linked sibling stub props, and trimmed generic Notes'
---

# FoodCart

*Module: foodcart.lua*

## Overview
The entire `foodcart.lua` is a single empty `Use(aiguid, floatval)` hook. The engine calls it when the food
cart is used, but this file scripts no behaviour — it exists so the prop has a valid `Use` entry point (the
same minimal-prop shape as [Binoculars](binoculars) and [Dropoff](dropoff)'s sibling stubs).

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state or use the `uGuid` keying pattern.

## Functions
### `Use(aiguid, floatval)`
The engine-invoked "use" hook. Arguments `aiguid` and `floatval` are declared but unused, and the body is
empty, so doing nothing on use is the intended behaviour. This is the only function in the file.

## Events
- Subscribes to: none. `Use` is an engine callback, not an `Event.Create` listener.

## Notes for modders
- There is no existing behaviour to preserve — the hook is empty by design. Fill in `Use` if you want the
  food cart to do something when used.