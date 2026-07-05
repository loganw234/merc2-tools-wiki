---
title: Monument
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [structure]
verified: true
verified_note: "deeper pass: re-confirmed the entire file is one empty Use(aiguid, floatval) stub — no state, no events, no imports; replaced the cautionary boilerplate Notes with the concrete override lever"
---

# Monument

*Module: monument.lua*

## Overview
The `Monument` module is a placeholder or stub for handling interactions with monument structures in the game world. Currently, it only defines a single function `Use`, which does not perform any actions.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module (no per-instance tables or fields).

## Functions
### `Use(aiguid, floatval)`
The entire body of this function is empty — it takes two parameters, `aiguid` and `floatval`, but the
function does nothing at all (no statements between `function` and `end`). This is the only function
defined in the file. Likely an engine-invoked "use" callback (naming convention matches other `Use`
handlers in this codebase) left unimplemented for monuments.

## Events
- none

## Notes for modders
- **Override lever:** `Use` is a plain global with an empty body, so it's a ready hook — redefine it to make
  monuments do something on "use" (e.g. play a sound, award cash, spawn an effect). Its signature
  `(aiguid, floatval)` matches the other resident `Use` handlers (the same identically-empty pattern as
  [Hackybench](hackybench)'s `Use` override).
- There is nothing else here — no state, no events, no imports. Whatever calls `Use` is engine-side.