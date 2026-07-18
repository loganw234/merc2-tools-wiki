---
title: Deprecated Frameworks
nav_order: 17
has_children: true
has_toc: false
---

# Deprecated Frameworks

Three standalone libraries, each fully absorbed into [Essentials (Ess)](ess/) as native code before any
mod had much chance to build on the standalone versions. They're kept here only as historical reference —
the reasoning and source on these pages is real and accurate, but none of the three is maintained, deployed,
or the thing to start a new mod on. If you're looking for the current equivalent, follow the `Ess.X` link
in each entry below.

- **[Contract Framework](contract-framework/)** → now `Ess.Contract` — a save-safe, ephemeral
  custom-mission system: objectives, triggers, support call-ins, AI orders, and a player-facing board — all
  built from primitives that never touch the game's save file, paired with an in-game Forge-style authoring
  tool and a web finisher for non-programmers.
- **[UI Kit](uilib/)** → now `Ess.UI` — nine reusable HUD widgets (menus, lists, dialogs, a chat log, a
  two-pane board) sharing one input/focus/heartbeat engine, so building custom UI never means solving
  "widget, input, drawing, lifecycle" from scratch.
- **[ModNet](modnet)** → now `Ess.Net` — a co-op data-sync library over `Net.SendCustomEvent`: synced
  state with last-writer-wins conflict resolution, named messages carrying arbitrary Lua values (not just
  numbers), and a raw escape hatch — the same chunked-transport technique
  [A Basic Co-op Text Chat](deep-dives/coop-chat) and its [current implementation](uilib/coopchat) solve
  once, generalized for anything a co-op mod needs to keep in sync.

[WaveDefense](wave-defense) — the worked example of gluing all three together into a real gamemode — stays
in [Frameworks](frameworks) rather than moving here: it's an example built *on* these libraries, not one of
the libraries itself, and its own page already notes plainly which now-deprecated pieces it depends on.
