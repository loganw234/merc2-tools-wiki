---
title: Hackybench
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Bench
tags: [hack, bench]
verified: true
verified_note: "deeper pass: re-confirmed the 4-line source (inherit(\"Bench\") + empty Use override) and cross-checked Bench.lua; both stateless, zero Event.* references; added Bench cross-link, no other changes needed"
---

# Hackybench

*Module: hackybench.lua*

## Overview
The `Hackybench` module is a thin 4-line specialization of the [Bench](bench) module. It inherits from
`Bench` via `inherit("Bench")` and redefines `Use` as an empty stub — the file body is literally just the
`inherit()` call plus one empty function.

## Inheritance
- Inherits from: `Bench`
- Imports: none

## Instance pattern
**Neither `Hackybench` nor `Bench` follows the per-instance/`uGuid` pattern.** `Bench.lua` (checked
directly) defines only `QueryRepair`, `QueryActiveUse`, `SuperUse`, `Use`, and `MakeUpright` — five plain
functions, no `OnActivate`, no `Awake`, no `Create`, no `setmetatable`, no `tInstance` registry, and no
`inherit()` of its own. `Hackybench` adds nothing on top except overriding `Use`. Both modules are
stateless — there is no per-instance state to track at all.

## Functions
### `Use(aiguid, floatval)`
Overrides `Bench.Use`. Empty body in both `Hackybench` and `Bench` — this override doesn't actually
change behavior, since the base implementation was already a no-op.

Inherited from `Bench` (not redefined here): `QueryRepair(intVal)` (returns `"MakeUpright"` if `intVal ==
1`, else `""`), `QueryActiveUse(intVal)` (returns `"SuperUse"` if `intVal == 1`, else `""`), `SuperUse
(floatval, aiguid)` (empty stub), and `MakeUpright(objectguid, aiguid)` (empty stub).

## Events
**No events at all.** Neither `Hackybench.lua` nor `Bench.lua` contains a single `Event.*` reference —
no `Event.Create`, no `Event.ObjectHibernation`, nothing. The previous version of this page claimed
`Event.ObjectHibernation`/`OnUse` wiring "inherited from Bench," but `Bench` has no such wiring to
inherit; that claim did not check out against source.

## Notes for modders
- This module is a placeholder/template — every function it defines or inherits from `Bench` is either an
  empty stub or a trivial string lookup. There is no observed engine hookup (activation, hibernation, or
  use-trigger event) anywhere in this two-file chain.
- To extend this module, override `Use` with custom logic; be aware you're starting from nothing; the
  base classes provide no scaffolding to build on.
- `QueryActiveUse`/`QueryRepair` string returns (`"SuperUse"`, `"MakeUpright"`) look like they're meant to
  be read by an external/native dispatcher (likely by name, to decide which function to call next), but
  no call site for that dispatch was found in the decompiled corpus — can't confirm the mechanism from
  static reading alone.