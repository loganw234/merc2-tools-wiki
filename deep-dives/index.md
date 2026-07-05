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
- **[Custom Networked Events](networking)** — *core dispatch confirmed live* — mod-authored Lua scripts
  really can exchange their own custom data across an already-connected co-op session (matchmaking/
  connection itself is out of scope, already solved elsewhere): the native callback-by-convention dispatch
  behind `Net.SendCustomEvent`/`NetEventCallback`, two real constraints discovered along the way (event IDs
  get masked to a small range, string arguments arrive unreadable), a ping-pong test, and a full catalog of
  every `NETEVENT_*` constant in the decompiled corpus.
- **[A Basic Co-op Text Chat](coop-chat)** — *confirmed working end-to-end across two real players* —
  input, send, and display all fire correctly together over a real network connection; input is backed by
  the [lua-bridge API](../lua-bridge-api/)'s `Loader` keyboard functions rather than anything achievable in
  game Lua alone — the one Deep Dive here that depends on lua-bridge itself (v0.1.6+), not just a script.
- **[Building a Chat/Log UI](coop-chat-ui)** — *confirmed working by live testing* — a real engine crash
  bug found in `MrxGuiTextBuffer`'s own documented constructor, a scope-sealing dead end while trying to
  patch around it, and the bug-free internal function that turned out to be the real fix — plus a
  confirmed static-source-vs-runtime discrepancy in `MrxGui` itself.
- **[Adding a Custom Contract](custom-contract)** — *research notes, currently broken* — registering a
  mission into `WifMissionData` and Fiona's briefing menu, confirmed working end to end exactly once
  (menu, accept, teleport-out, spawn/destroy/reward), plus two hard native-safety rules
  (`dynamic_import`/`dynamic_remove` unsafe to touch beyond normal use; never `return fOriginal(...)` in a
  wrapper) discovered the hard way — but the same script permanently breaks the lua bridge when a save
  spawns the player directly inside the PMC HQ, root cause not yet found.
- **[Building a World Inspector (WAILA)](world-inspector)** — *work in progress* — a menu-driven "what am
  I looking at" mode and bulk nearby-object dump, confirmed working live (cycling, in-world marker,
  detailed per-object dump), built around a low-radius `Pg.FastCollect*` sweep instead of an unconfirmed
  reticle-targeting native. Documents the hard ceiling hit while chasing a real spawn-template string out
  of an object (only a hashed localized name is ever reachable), plus three still-open threads it led to:
  `Pg.Spawn` only catching a tiny fraction of real world population, whether any deeper native hook exists
  for object creation (short answer: not a clean one — see the layer system instead), and an unbuilt
  "layer delamination" tool for extracting a per-layer object roster.
- **[Making the Destroyer Driveable](destroyer-vehicle)** — *partially working* — turning the "Chinese
  Destroyer"/"Allied Destroyer" set-dressing ships into a spawnable, boardable vehicle for both players in
  co-op, confirmed working for spawning and seat entry/exit. A systematic hardpoint-naming probe, a full
  `Vehicle.GetSeatParams` dump, and an extensive camera-recipe test matrix (built around the one confirmed
  live-gameplay camera lock anywhere in the corpus) all come up empty on the two open problems — physics
  (needs external tooling, not reachable from Lua) and the camera (very likely the same "no Lua touchpoint"
  category as turret firing itself, already confirmed elsewhere on this wiki).
