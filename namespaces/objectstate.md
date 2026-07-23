---
title: ObjectState
parent: Engine Namespaces
nav_order: 22
---

# ObjectState

## Overview

`ObjectState` is an **engine namespace**: implemented natively by the game engine, not by any decompiled
`.lua` module. There is no source file behind it, no `import()` needed — it is always globally available
from any script. What little is confirmed so far points to object-level messaging plus particle-emitter
control.

## Provenance

This page does not come from a live `pairs(ObjectState)` dump the way most pages in this section do —
that's a **different discovery method** from the one behind [`Sys`](sys), [`Camera`](camera),
[`Junk`](junk), and the other pairs()-enumerated namespaces. It comes from a newer research pass: a static
dump of all 973 `luaL_Reg` engine bindings compiled into the game executable, diffed against the 370-file
decompiled Lua corpus to find bindings that are registered but never called anywhere in that corpus. That
diff left several `luaL_Reg` binding tables unlabeled — a raw code address with no name attached. The
table at `0x007995B0` was one of them; it was resolved to the runtime global `ObjectState` by
cross-referencing which corpus call-prefixes matched its member functions, then confirmed live with a
`type(ObjectState) == "table"` check over lua-bridge's WebSocket transport against a running game.

That means the function list below is a **first, partial batch** — only the members that happened to turn
up as `ObjectState.*` call-prefixes during that cross-reference — not a complete `pairs()`-style
enumeration the way, e.g., [`Sys`](sys)'s 64 functions are. Only two member names came out of this pass,
and the same research pass flagged more members clustered around particle/effects work without naming
them individually (see Notes for modders below) — there is very likely more on this table than the two
named here.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SendMessage` | — | Name and table membership confirmed via the corpus call-prefix cross-reference described above; not itself live-probed for this page, and no call site with a concrete argument list was captured. Presumed by naming to send some message/signal to (or about) an object — plausibly `ObjectState.SendMessage(uGuid, ...)` by analogy with every other guid-taking namespace on this wiki, but that argument shape is a guess, not a confirmed signature. |
| `StartEmitter` | — | Name and table membership confirmed the same way; not live-probed, no captured argument list. Presumed by naming to start a particle emitter attached to an object — plausibly `ObjectState.StartEmitter(uGuid, ...)` — but again a guess from the name only. |

## Notes for modders

- The research pass that resolved this table's identity noted its members as "`SendMessage`, `StartEmitter`
  (+ the effects work)" — the parenthetical means more members clustered around particle/visual-effects
  work turned up in the same cross-reference pass without being individually named. If you're looking for
  a way to drive particle effects on an object from a mod, this namespace is the lead worth live-probing
  first, but don't assume `StartEmitter` is the only relevant entry point here.
- Missing or wrong arguments return `nil` silently on this engine — there is no `bad argument #N` error,
  because the engine inlines its own argument checks. That means a read-only-style probe is safe to make
  blind (a bad call just returns `nil` rather than crashing), but arity can't be discovered from an error
  message, only from a live probe with valid arguments — and for this namespace, no valid-argument probe
  has been done yet, including for `SendMessage`/`StartEmitter`'s likely-but-unconfirmed leading `uGuid`
  argument. Treat this page as a starting point for that probing, not a finished picture.
