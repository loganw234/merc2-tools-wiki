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

- **[Contract Framework](contract-framework/)** — a save-safe, ephemeral custom-mission system: objectives,
  triggers, support call-ins, AI orders, and a player-facing board — all built from primitives that never
  touch the game's save file, paired with an in-game Forge-style authoring tool and a web finisher for
  non-programmers.
- **[UI Kit](uilib/)** — nine reusable HUD widgets (menus, lists, dialogs, a chat log, a two-pane board)
  sharing one input/focus/heartbeat engine, so building custom UI never means solving "widget, input,
  drawing, lifecycle" from scratch.
- **[ModNet](modnet)** — a co-op data-sync library over `Net.SendCustomEvent`: synced state with
  last-writer-wins conflict resolution, named messages carrying arbitrary Lua values (not just numbers),
  and a raw escape hatch — the same chunked-transport technique [A Basic Co-op Text Chat](deep-dives/coop-chat)
  and its [current implementation](uilib/coopchat) solve once, generalized for anything a co-op mod needs
  to keep in sync.
- **[WaveDefense](wave-defense)** — not a library but the worked example of gluing the other three
  together: a wave-survival gamemode where a Contract Framework contract is only the launcher, ModNet's
  authority model decides which machine runs the simulation, and UI Kit draws the entire HUD and setup
  menu itself.
