---
title: PirJob001
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTaskJobDestroyType
tags: [job]
verified: false
---

# PirJob001

## Overview
PirJob001 is a minimal "destroy this type of target" side job: it tells the base `MrxTaskJobDestroyType` class to track anything labeled `"VZ"`, restricts progress to the hero's own kills (not AI companions or vehicle passengers), and starts running. There is no mission-specific logic beyond that configuration — the whole file is one lifecycle override.

## Inheritance
- Inherits from: [`MrxTaskJobDestroyType`](../resident/mrxtaskjobdestroytype) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskJobDestroyType` subclass — `self`-based lifecycle override, no module-level state at all.

## Functions
### `Activated(self)`
Calls the base `MrxTaskJobDestroyType.Activated`, then configures the job: `self:_SetLabelFilter("VZ")` (only `VZ`-labeled targets count), `self:_SetHeroOnly(true)` (only the hero-controlled player's kills count, not squadmates/AI), and `self:_Go()` (starts the job running).

## Events
None registered directly in this file — target-destruction tracking is entirely handled by the base `MrxTaskJobDestroyType` class.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system (jobs included), not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- This is about as small as a job file gets in this corpus — a good minimal template if you're studying the `MrxTaskJobDestroyType` config surface (`_SetLabelFilter`, `_SetHeroOnly`, `_Go`).
- `_SetHeroOnly(true)` is the notable choice here: contrast with jobs that don't call it and so count any player/ally kill toward the total.
