---
title: ObjectFilter
parent: Engine Namespaces
nav_order: 23
---

# ObjectFilter

## Overview

`ObjectFilter` is an **engine namespace**: implemented natively by the game engine, not by any decompiled
`.lua` module. There is no source file behind it, no `import()` needed — it is always globally available
from any script. Of the four namespaces newly identified in this research pass, this one has the fullest
confirmed member list — six names — and their shape reads as a coherent filter/query-builder pattern; see
**Notes for modders** below for that reading, clearly labeled as inference rather than confirmed behavior.

## Provenance

This page does not come from a live `pairs(ObjectFilter)` dump the way most pages in this section do —
that's a **different discovery method** from the one behind [`Sys`](sys), [`Camera`](camera),
[`Junk`](junk), and the other pairs()-enumerated namespaces. It comes from a newer research pass: a static
dump of all 973 `luaL_Reg` engine bindings compiled into the game executable, diffed against the 370-file
decompiled Lua corpus to find bindings that are registered but never called anywhere in that corpus. That
diff left several `luaL_Reg` binding tables unlabeled — a raw code address with no name attached. The
table at `0x00798770` was one of them; it was resolved to the runtime global `ObjectFilter` by
cross-referencing which corpus call-prefixes matched its member functions, then confirmed live with a
`type(ObjectFilter) == "table"` check over lua-bridge's WebSocket transport against a running game.

That means the function list below is a **first, partial batch** — only the members that happened to turn
up as `ObjectFilter.*` call-prefixes during that cross-reference — not a complete `pairs()`-style
enumeration the way, e.g., [`Sys`](sys)'s 64 functions are. Six names came out of this pass — a fuller
picture than the other three namespaces from the same research pass — but there could still be more on
this table that simply had no call-prefix to cross-reference against.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Create` | — | Name and table membership confirmed via the corpus call-prefix cross-reference described above; not itself live-probed for this page, no captured argument list. Presumed by naming to construct a new filter object/handle — see **Notes for modders** for the inferred builder-pattern reading. Signature unconfirmed. |
| `AddObject` | — | Confirmed the same way. Presumed by naming to add a specific object (by guid) into a filter's candidate set. Signature unconfirmed. |
| `SetFilter` | — | Confirmed the same way. Presumed by naming to set some filter predicate/criteria on a filter handle. Signature unconfirmed. |
| `SetRelation` | — | Confirmed the same way. Presumed by naming to set a relational condition (e.g. combining multiple filter criteria, or a spatial/faction relation) on a filter handle. Signature unconfirmed. |
| `Eval` | — | Confirmed the same way. Presumed by naming to evaluate a configured filter and return its matching result. Signature unconfirmed. |
| `GetCoopPlayerGuid` | — | Confirmed the same way. Doesn't obviously fit the `Create`/`AddObject`/`SetFilter`/`SetRelation`/`Eval` builder-pattern reading below — plausibly a convenience getter used to feed a co-op player's guid into a filter (e.g. as an `AddObject`/`SetRelation` argument), but that's speculation; its relationship to the other five is not confirmed. |

## Notes for modders

- **Inference, not confirmed behavior:** the shape of these six names reads like a filter/query-builder
  pattern — `Create` a filter handle, configure it with `AddObject`/`SetFilter`/`SetRelation`, then `Eval`
  it to get a result (presumably a matching object or set of objects, by analogy with `Pg`'s
  `FastCollect*` family — see [Pg](pg)). That reading comes purely from how the five names sit together,
  not from any call site, disassembly, or live probe of the actual argument/return behavior — treat it as
  a reasonable starting hypothesis to test, not a documented fact.
- `GetCoopPlayerGuid` is confirmed to exist on this table but doesn't obviously fit that builder-pattern
  reading; see the Functions table above.
- Missing or wrong arguments return `nil` silently on this engine — there is no `bad argument #N` error,
  because the engine inlines its own argument checks. That makes a read-only-style call like `Eval` or
  `GetCoopPlayerGuid` safe to probe blind (a bad call just returns `nil` rather than crashing), but arity
  can't be discovered from an error message, only from a live probe with valid arguments — and none of
  the six functions above have had that probe done yet. Treat this page as a starting point for that
  probing, not a finished picture.
