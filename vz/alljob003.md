---
title: AllJob003
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTaskJobDestroyType
tags: [job]
verified: false
---

# AllJob003

## Overview
A minimal Allied Nation side job: a generic bounty to destroy every object carrying the `"China"` label,
restricted to hero characters. The whole file is eight lines — it sets the base class's label filter and
hero-only flag, then starts the job. All actual target-finding/tracking logic lives in the
`MrxTaskJobDestroyType` base class, not in this file.

## Inheritance
- Inherits from: [`MrxTaskJobDestroyType`](../resident/mrxtaskjobdestroytype) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskJobDestroyType` subclass with no data or state of its own — this file only configures
the base class.

## Functions
### `Activated(self)`
Calls the base `MrxTaskJobDestroyType.Activated`, sets the label filter to `"China"`, restricts the job
to hero characters (`_SetHeroOnly(true)`), and starts it with `_Go`.

## Events
None registered directly in this file — target discovery/tracking is entirely handled inside the native
`MrxTaskJobDestroyType` base class.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- This is the minimal possible `MrxTaskJobDestroyType` subclass — a good reference shape for a "destroy
  every labeled X" bounty job that needs no custom data.
- **Mirror pair**: [ChiJob003](chijob003) is the exact same file with the label filter flipped to
  `"Allied"` — each faction offers a side job to hunt down the other faction's labeled assets.
