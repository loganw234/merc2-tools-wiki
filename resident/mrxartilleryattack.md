---
title: MrxArtilleryAttack
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, artillery]
verified: true
verified_note: "deeper pass: confirmed smoke-shell quirk and all defaults (5 shells, dist 10, Artillery Shell, 4s); documented the two-different-timer-bases (marker vs barrage) and Airstrike.SpawnOrdnance shape; added cross-links"
---

# MrxArtilleryAttack

*Module: mrxartilleryattack.lua*

## Overview
`MrxArtilleryAttack` is a small, self-contained helper that drops a staggered falling-ordnance strike onto an object's position — a plain function you call with a target `uGuid`, not a player-facing support type. It spawns several shells at randomized positions around the target to fake an artillery bombardment. Unlike [`MrxArtillery`](mrxartillery), it has no designator, no cost, no VO, and no inheritance — it's the raw "make N shells fall on this spot" primitive.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none` (calls the [Airstrike](../namespaces/airstrike) engine namespace directly)

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
Spawns a single falling round at the given coordinates via [`Airstrike.SpawnOrdnance`](../namespaces/airstrike):
```lua
Airstrike.SpawnOrdnance(sTemplate, x, y, z, 0, -100, 0, "impact", 1)
```
Downward velocity `-100`, `"impact"` detonation. Note it passes **no** `uOwner` (9-arg form), so kills from this strike aren't attributed to a player — a real difference from [`MrxArtillery.TriggerFallingMissile`](mrxartillery), which passes `self.uOwner`.

## Events
No event subscriptions. `Create` schedules each of the `nShells` rounds with [`Event.TimerRelative`](../namespaces/event) at `5 + i * (nTime / nShells)` seconds. The **marker** smoke shell is fired immediately (no timer), so the strike opens with an un-offset ranging round and the real barrage lands starting ~5 seconds later — two different time bases worth knowing when tuning `nTime`.

## Module constants & tunables
All are `Create` parameters with defaults, plus one hardcoded literal:
- `nShells = 5`, `nDistance = 10`, `sTemplate = "Artillery Shell"`, `nTime = 4` (defaults applied via `or`).
- Marker round: always `"Artillery Smoke Shell"`, un-offset, fired with no timer — **not** configurable (see the callout above).
- Drop height: `y + 250` (marker and barrage share the same computed Y).

## Notes for modders
- Call it with just `MrxArtilleryAttack.Create(uTarget)` for the defaults, or pass all five args to retune count/spread/template/duration.
- `sTemplate` accepts any [Airstrike template string](../namespaces/airstrike#confirmed-ordnance-template-name-strings) — swap `"Artillery Shell"` for something heavier to change the payload without touching the timing.
- If you don't want the tell-tale smoke ranging round, you'd have to override `Create` wholesale — the `"Artillery Smoke Shell"` shot is hardcoded, not parameterized.