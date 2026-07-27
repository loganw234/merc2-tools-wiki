---
title: Frameworks
nav_order: 15
has_children: true
has_toc: false
---

# Frameworks

Reusable systems built to be built on — each one abstracts a hard, general problem once so a modder using
it never has to solve that problem themselves. Distinct from [Deep Dives](deep-dives/), which document a
single investigation end to end; a framework here is an ongoing library with its own API surface, likely
to keep growing.

> **Looking for Essentials (Ess)?** It now has its own top-level section — see
> **[Essentials (Ess)](ess/)**. It outgrew this category: it's no longer one framework among several, it's
> the recommended starting point for any new mod, and it absorbed three of the standalone libraries this
> page used to list. Everything below is what remains here — an example gamemode, and a guide to writing
> your own library.

- **[WaveDefense](wave-defense)** — not a library but the worked example of gluing three of those
  predecessors together: a wave-survival gamemode where a Contract Framework contract is only the launcher,
  ModNet's authority model decides which machine runs the simulation, and UI Kit draws the entire HUD and
  setup menu itself.
- **[Building Your Own Framework](building-a-framework)** — not a library either, but the tutorial for
  writing one: OnLoad load order, registering a global safely, and the safe/unsafe patterns Ess itself
  follows, ending in a basic skeleton to build from.

Looking for `Ess`'s now-superseded predecessors? See [Deprecated Frameworks](deprecated-frameworks) —
Contract Framework, UI Kit, and ModNet are still documented in full, just no longer where new mods should
start.
