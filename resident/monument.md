---
title: Monument
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [structure]
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
A placeholder function that currently does nothing. It takes two parameters, `aiguid` and `floatval`, but no actions are performed with them.

## Events
- none

## Notes for modders
- This module is a stub and does not implement any functionality. Any custom behavior related to monument interactions should be added by extending or replacing this module.
- Be cautious when modifying this module, as it may affect the game's behavior if other parts of the code rely on its presence or structure.