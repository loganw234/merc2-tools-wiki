---
title: lua-bridge API
nav_order: 5
has_children: true
has_toc: false
---

# lua-bridge API

Every other reference section on this wiki — [Resident Modules](../resident/), [Engine Namespaces](../namespaces/) —
documents things that are part of Mercenaries 2 itself: real game code, reachable because lua-bridge gives
a live Lua console into the running engine. This section is different. It documents globals that
**lua-bridge itself adds** to that environment — functions with no `.lua` file behind them and no engine
namespace to enumerate via `pairs()`, because the game never shipped them. They exist purely because
modding needed something the engine's own Lua surface didn't expose.

That distinction matters for one practical reason: everything in [Engine Namespaces](../namespaces/) is
guaranteed present in any copy of the game lua-bridge can attach to, regardless of which lua-bridge build
you're running. Everything here ships in the stock lua-bridge install — but make sure you're on
**lua-bridge v0.1.6 or later** before relying on anything in this section, since older installs predate
some of these additions.

## Available namespaces

- **[Loader](loader)** — logging, plus (as of this writing) the game's first real general-purpose
  keyboard input API: full keyboard-state snapshots, a single-key predicate, an edge-triggered keystroke
  queue, and foreground-focus detection. Added specifically to unblock the
  [co-op text chat](../deep-dives/coop-chat) idea, whose "Input" problem had no answer anywhere in the
  game's own Lua surface.

`Tcp.Send(host, port, msg)` (see the [lua-bridge README](https://github.com/loganw234/Mercenaries2)) is
also a lua-bridge-provided global, registered the same way — not yet written up as its own page here.
