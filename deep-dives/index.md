---
title: Deep Dives
nav_order: 10
has_children: true
has_toc: false
---

# Deep Dives

Long-form technical writeups that don't fit the [Snippets](../snippets)/[Sample Scripts](../sample-scripts)
format — full investigations into a hard problem, including the wrong turns, the dead ends that were
still worth knowing about, and the final working result. Where [Recipes](../recipes) gives you a
building block, a Deep Dive gives you the reasoning that got there, so you can adapt the technique to a
different problem instead of just copy-pasting the end result.

## Available Deep Dives

- **[Building a Real Freecam](freecam)** — how to get genuine continuous analog stick and d-pad input
  into a Lua script (something no documented engine API provides), by hijacking the PDA widget's own
  input-handling event, and using it to drive a fully controllable detached flying camera.
- **[Overriding a Function](function-override)** — replacing a piece of the game's own logic instead of
  just reading/writing a value, worked through end to end: the original approach, three wrong turns, the
  fix that actually worked, and the general pattern for applying this technique elsewhere.
- **[Networking: A Lua-Only Restoration?](networking)** — *speculative, not live-tested* — what the `Net`
  namespace actually exposes: three distinct connection paths, a real direct-IP-connect primitive, the
  native callback-by-convention dispatch behind both server discovery and custom cross-player events, and
  a full catalog of every `NETEVENT_*` constant in the decompiled corpus.
- **[A Basic Co-op Text Chat](coop-chat)** — *speculative, not live-tested* — send and display are solved
  by reusing the networking page's hijacked-`NetEventCallback` pattern and the tutorial-hint popup from
  Snippets; input turned out to need a small lua-bridge-side addition (`Loader.GetKeyboardState()`)
  rather than anything achievable in game Lua alone — the one Deep Dive here that isn't pure-Lua.
