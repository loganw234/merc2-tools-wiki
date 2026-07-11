---
title: UI Kit Scripts
parent: UI Kit
nav_order: 6
has_children: true
has_toc: false
---

# UI Kit Scripts

Complete, ready-to-drop-in scripts built on [UI Kit](../uilib/) — unlike
[Sample Scripts](../sample-scripts), which bundles many scripts per page behind collapsible entries, each
script here gets its own dedicated page.

- **[coopchat.lua](coopchat)** — a full co-op text chat: `UI.Chat` as the front end, a packed/chunked
  encoding to carry arbitrary text over `Net.SendCustomEvent`, sender identity, and a movement freeze while
  typing. The current, improved implementation of [A Basic Co-op Text Chat](../deep-dives/coop-chat).
- **[menudemo.lua](menudemo)** — `UI.Menu` end to end: nested categories, `ctx:spawn`, a live ON/OFF
  `:switch`, and composing with `UI.Confirm`/`UI.Input`/`UI.Board`/`UI.Chat` from inside a menu action.
- **[uidemo.lua](uidemo)** — the kit's own smoke test for every widget *other* than `UI.Menu`: a hand-driven
  `UI.List` drill-down, `UI.Panel` as a rolling log, `UI.Bar`, `UI.Toast`, and both `UI.Confirm`/`UI.Input`.
