---
title: Frameworks
nav_order: 13
has_children: true
has_toc: false
---

# Frameworks

Reusable systems built to be built on — each one abstracts a hard, general problem once so a modder using
it never has to solve that problem themselves. Distinct from [Deep Dives](deep-dives/), which document a
single investigation end to end; a framework here is an ongoing library with its own API surface, likely
to keep growing.

- **[Essentials (Ess)](ess/)** — the foundational library that now underpins everything: safe, one-line
  wrappers around every hard-won engine pattern, shipped as one drop-in `1_Ess.lua`. It **absorbs three
  earlier standalone libraries** as native code (`Ess.UI`, `Ess.Net`, `Ess.Contract`) — see
  [Deprecated Frameworks](deprecated-frameworks) for those predecessors — new mods start here.
- **[WaveDefense](wave-defense)** — not a library but the worked example of gluing three of those
  predecessors together: a wave-survival gamemode where a Contract Framework contract is only the launcher,
  ModNet's authority model decides which machine runs the simulation, and UI Kit draws the entire HUD and
  setup menu itself.

Looking for `Ess`'s now-superseded predecessors? See [Deprecated Frameworks](deprecated-frameworks) —
Contract Framework, UI Kit, and ModNet are still documented in full, just no longer where new mods should
start.
