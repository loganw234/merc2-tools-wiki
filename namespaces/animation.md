---
title: Animation
parent: Engine Namespaces
nav_order: 21
---

# Animation

## Overview

`Animation` is an **engine namespace**: implemented natively by the game engine, not by any decompiled
`.lua` module. There is no source file behind it, no `import()` needed — it is always globally available
from any script. What little is confirmed so far points to facial animation and stance/action-driven
animation lookup.

Note: this is a different table from the animation-related functions already documented under
[`Object`](object#animation) (`PlayAnimation`, `StopAnimation`, `StopAnimationChannel`,
`StopAllAnimation`, `PlayMaterialAnimation`, `StopMaterialAnimation`) — those operate on a specific
object's skeletal/material animation via its `uGuid` and are a separate, already-confirmed family. This
page's `Animation` is its own top-level namespace; whether or how it relates internally to `Object`'s
animation calls is not known from anything in hand.

## Provenance

This page does not come from a live `pairs(Animation)` dump the way most pages in this section do — that's
a **different discovery method** from the one behind [`Sys`](sys), [`Camera`](camera), [`Junk`](junk), and
the other pairs()-enumerated namespaces. It comes from a newer research pass: a static dump of all 973
`luaL_Reg` engine bindings compiled into the game executable, diffed against the 370-file decompiled Lua
corpus to find bindings that are registered but never called anywhere in that corpus. That diff left
several `luaL_Reg` binding tables unlabeled — a raw code address with no name attached. The table at
`0x0079A88C` was one of them; it was resolved to the runtime global `Animation` by cross-referencing which
corpus call-prefixes matched its member functions, then confirmed live with a `type(Animation) == "table"`
check over lua-bridge's WebSocket transport against a running game.

That means the function list below is a **first, partial batch** — only the members that happened to turn
up as `Animation.*` call-prefixes during that cross-reference — not a complete `pairs()`-style enumeration
the way, e.g., [`Sys`](sys)'s 64 functions are. Only two member names came out of this pass, and there is
very likely more on this table than that.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `PlayFaceAnim` | — | Name and table membership confirmed via the corpus call-prefix cross-reference described above; not itself live-probed for this page, and no call site with a concrete argument list was captured. Presumed to play a facial animation/expression on a character by naming; signature unconfirmed. |
| `GetTranslationForStanceAndAction` | — | Name and table membership confirmed the same way; not live-probed, no captured argument list. Presumed by naming to look up some translation/offset value keyed by a stance and an action (plausibly for animation blending or root-motion offsetting), but that's a reading of the name only — signature and even the general behavior are unconfirmed. |

## Notes for modders

- Only the name and table membership are confirmed for both functions above — not argument count, argument
  types, or return values. Nothing about "stance" or "action" as engine concepts is confirmed from any
  other source in this wiki; treat `GetTranslationForStanceAndAction`'s purpose as a guess from its name.
- Missing or wrong arguments return `nil` silently on this engine — there is no `bad argument #N` error,
  because the engine inlines its own argument checks. That means a read-only getter like
  `GetTranslationForStanceAndAction` is safe to probe blind (a bad call just returns `nil` rather than
  crashing), but arity can't be discovered from an error message, only from a live probe with valid
  arguments — and for this namespace, no valid-argument probe has been done yet. Treat this page as a
  starting point for that probing, not a finished picture.
