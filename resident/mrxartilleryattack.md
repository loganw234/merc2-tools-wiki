---
title: MrxArtilleryAttack
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, artillery]
verified: true
verified_note: re-verified previously-documented smoke-shell quirk against source, still accurate; no other gaps found
---

# MrxArtilleryAttack

*Module: mrxartilleryattack.lua*

## Overview
The `MrxArtilleryAttack` module is responsible for executing a staggered falling-ordnance strike. It spawns multiple shells at randomized positions around the target location, creating an artillery bombardment effect.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance table). It does not track any persistent state.

## Functions
### `Create(uGuid, nShells, nDistance, sTemplate, nTime)`
Spawns an artillery bombardment at the specified location (`uGuid`). Configures the number of shells (`nShells`), distance from the target (`nDistance`), shell template (`sTemplate`), and total time for the attack (`nTime`). Randomizes positions for each shell and schedules their deployment using timers.

**Not mentioned above but confirmed in source:** before scheduling any of the `nShells`, `Create` immediately
fires one extra shot at the raw (un-offset) target position using a hardcoded `"Artillery Smoke Shell"`
template — always, regardless of `sTemplate`, and not configurable via any parameter. This is likely a
marker/ranging round rather than a real hit.

### `TriggerFallingMissile(x, y, z, sTemplate)`
Spawns a single falling missile at the specified coordinates (`x`, `y`, `z`) using the provided template (`sTemplate`).

## Events
- Listens for custom event `Event.TimerRelative` to schedule each shell's deployment.

## Notes for modders
- Ensure that the correct parameters are passed to `Create` to achieve the desired artillery strike.
- Customize the number of shells, distance, and timing by adjusting the parameters when calling `Create`.
- The module uses randomization to spread out the shells around the target location, creating a more realistic artillery bombardment effect.