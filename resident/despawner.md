---
title: Despawner
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: spot-checked against source (entire file is 2 lines, one empty function) — no changes needed beyond confirming no inherit/Event/other functions exist and no call sites found elsewhere in the corpus.
---

# Despawner

*Module: despawner.lua*

## Overview
The `Despawner` module is a utility script nominally for despawning game objects. The entire source file is
two lines — a single empty function. Whatever despawn logic this is meant to gate on is either stubbed out,
handled entirely by the engine based on the function existing (e.g. a native call site checks for the
presence of `Use` without needing it to do anything), or not yet implemented in this build.

## Inheritance
- Inherits from: none — no `inherit()` call in this file.
- Imports: none

## Instance pattern
Stateless manager/utility module — no per-instance tables, no `tInstance`, no module-level globals of any
kind. The file defines exactly one function and nothing else.

## Functions
### `Use(floatval, aiguid)`
Empty function body — takes two arguments (`floatval`, `aiguid`) and does nothing with them. No other
functions exist in this file. No call sites for `Despawner.Use` were found anywhere else in the decompiled
corpus, so its expected caller/trigger (and the real meaning of `floatval`/`aiguid`) can't be confirmed from
static reading alone — likely invoked directly by native/engine code rather than other Lua modules.

## Events
- None — no `Event.*` references anywhere in this file.

## Notes for modders
- This module currently does nothing; overriding `Use` is the only way to give it behavior.
- Because no in-corpus caller was found, the exact invocation contract for `Use(floatval, aiguid)` (when it's
  called, what `floatval`/`aiguid` represent) is unconfirmed — treat the parameter names as a hint, not a
  guarantee.