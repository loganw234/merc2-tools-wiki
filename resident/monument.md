---
title: Monument
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [structure]
verified: true
verified_note: spot-checked against source (entire file is a 3-line empty function stub), no changes needed.
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
- This module is a stub and does not implement any functionality. Any custom behavior related to monument interactions should be added by extending or replacing this module.
- Be cautious when modifying this module, as it may affect the game's behavior if other parts of the code rely on its presence or structure.