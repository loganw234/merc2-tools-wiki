---
title: Engine Namespaces
nav_order: 9
has_children: true
has_toc: false
---

# Engine Namespaces

Everything in [Resident Modules](../resident/) is backed by a real, readable `.lua` file — a genuine
decompiled module we can quote and cross-check. **Engine namespaces** are different: things like
`Object`, `Vehicle`, `Event`, and `Pg` are global tables implemented natively inside the game engine
itself. There is no `.lua` source file behind them, no `import()` needed to reach them — they're just
always there, on every script, from the moment it runs.

That also means we can't read their implementation the way we can read a `resident/` module. Everything
documented on these pages comes from one of two places:

- **Live introspection** — running `pairs(SomeNamespace)` in-game via a Lua console/REPL and printing
  every key. This gives a complete, authoritative list of every real function that exists on the
  namespace. See [Snippets: Dump every engine namespace at once](../snippets#dump-every-engine-namespace-at-once)
  for the exact script used to do this.
- **Static usage in the decompiled corpus** — grepping the ~230 decompiled `.lua` files for real call
  sites, to recover argument shapes and usage patterns for whichever of those functions actually get
  called somewhere.

## Why this is worth doing

Static source reading has a real blind spot: a function can genuinely exist on an engine namespace and
still have **zero call sites** anywhere in the entire decompiled corpus, simply because none of the
~230 scripts we have happened to use it. Grepping for it finds nothing, and a wiki built only from
source reading would (wrongly) conclude the function doesn't exist.

This actually happened here. Early in this project, "how do I find what object the player is currently
aiming at" was investigated by grepping for every plausible function name (`GetAimTarget`,
`GetTargetedObject`, `GetLookAt`, `LineOfSight`, and a dozen other guesses) across the whole source
tree — all came back empty, and the honest conclusion at the time was "not possible from what we have."
Running `pairs(Player)` live in-game turned up `Player.GetTargetUnderReticle` immediately — a real,
callable engine function that simply has no caller anywhere in the decompiled scripts. Static analysis
alone could never have found it; live enumeration did, on the first try.

That's the case for treating this as its own reference section rather than folding it into existing
pages: it's a fundamentally different (and more complete) source of truth than everything else in this
wiki, and it deserves to be labeled as such rather than quietly mixed in.

## How to read these pages

Every namespace page follows the same shape:

- **Overview** — what the namespace is for, in plain terms.
- **Provenance** — which parts of the page are backed by real call-site evidence versus name-only
  live enumeration. This section exists because these pages mix two very different confidence levels,
  and it matters which one applies to any given function.
- **Functions** — grouped tables, not the per-function prose used on `resident/` pages. A namespace
  function typically gives us a name and (if we're lucky) a real argument pattern from source — that's
  much less to say than a `resident/` module's full logic, so a table fits the actual amount of
  confirmed information better than prose would.

A function marked "no call sites found in the decompiled corpus" is not a weaker claim about whether it
exists — the live enumeration already settled that. It's a weaker claim about *how to call it correctly*.
Treat those as real leads worth live-testing, not documentation gaps to be papered over with guesses.

## Namespaces mapped so far

| Namespace | Functions | Notes |
|---|---|---|
| [Object](object) | 87 | Position/transform, health, physics, animation, winches, labels — the namespace almost everything else operates on via `uGuid`. |
| [Vehicle](vehicle) | 40 | Seats/riders, doors/turrets, the hijacking state machine, vehicle-specific physics. |
| [Event](event) | 48 (44 event-type IDs + 4 functions) | The callback-registration pattern (`Event.Create`) used throughout `resident/`. |
| [Pg](pg) | 80 | Spawning, proximity-based collection (`FastCollect*`), GUID-by-name lookup, the pursuit/wanted system, contracts, achievements, asset streaming. |

## What's left

A full `pairs(_G)` scan (see [Snippets](../snippets#dump-every-engine-namespace-at-once)) turned up
roughly two dozen more real engine namespaces beyond the four above — `Ai`, `Net`, `Sound`, `Sys`,
`Human`, `Gui`, `Hud`, `Controller`, `Camera`, `Graphics`, `Junk`, `Marker`, and others, ranging from a
single entry up to `Player` itself at 107. Those haven't been mapped into dedicated pages yet. If you've
run the full dump yourself and want to contribute a page for one of them, following the same
Overview/Provenance/Functions shape as the four above is the right template to copy.
