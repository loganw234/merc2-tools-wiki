---
title: Outhouse
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (2-line stub, one empty Use function, no imports/inherit/events); tightened the stub note and made the modder guidance actionable (Use is an overridable global hook).'
---

# Outhouse

*Module: outhouse.lua*

## Overview
The `Outhouse` module is a utility script that defines the behavior for using an outhouse in the game world. Currently, it only contains a placeholder function `Use`, which does not perform any actions.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance pattern or tracked fields.

## Functions
### `Use(aiguid, floatval)`
Empty function — the body does nothing. `aiguid` is the object handle of the outhouse; `floatval` is
unused. By naming convention this is the "use/interact" hook the engine calls when the player
activates the object, but as shipped it is a no-op (the outhouse is pure set dressing).

## Events
- none — no `Event.*` calls of any kind.

## Notes for modders
- `Use` is a plain global, so overriding it is the whole point of this file: drop your own `Use`
  implementation to make the outhouse do something on interaction. See
  [Function override](../deep-dives/function-override).
- Nothing else is wired up — no inherit, no imports, no state — so there is no lifecycle or cleanup to
  worry about.