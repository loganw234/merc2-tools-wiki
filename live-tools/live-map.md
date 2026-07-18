---
title: Live Map
parent: Live Tools
nav_order: 2
---

# Live Map

## Overview

`mercs2-webmap` is an interactive top-down map of the Mercenaries 2 world, built on Leaflet with
`CRS.Simple` (a plain coordinate plane, not geo-projected) over the retail world map image. Live at
**https://map.mercs2.tools/** (confirmed reachable). Like the [Lua Web IDE](web-ide), it's a single
standalone HTML file — no build step to use it, no server, no external requests — hosted on GitHub Pages,
downloadable, or served by the game's own `lua-bridge` at `http://127.0.0.1:27050/`.

## Layers, and why they're generic

Two layers ship built in:

- **~99 collectible toolboxes**, split into two color-coded batches (`batch_1C` / `batch_1D`).
- A **seeded Teleport spots** layer (see below).

But the real design point is that a user can drag in **any JSON file** of `{position:{x,y,z}}` points — or
a `{name, kind, groupBy, colors, points:[...]}` wrapper — and it becomes a new toggleable layer through the
exact same loader the built-in collectibles use. The collectibles are just the first shipped dataset, not
the point of the tool.

Collected-toolbox state persists in `localStorage` (keyed by each point's `entity_id`), with a `done/total`
counter per layer, a **Hide collected** toggle, and a **Reset ticks** control.

## Connecting to the game

**Connect to game** opens a WebSocket to `ws://127.0.0.1:27050` — see
[WebSocket Transport](../lua-bridge-api/websocket) for the wire protocol — and, on open, sends **one** setup
Lua chunk that starts an in-game [`Ess.Loop`](../ess/timing-input#ess-loop) ticking every 0.1s. Each tick
reads [`Ess.Player.pose(0)`](../ess/identity-query#ess-player) and pushes `x,y,z` out over the hidden
`Loader.WsSend` channel, tagged for pose updates. This is deliberately **not** per-frame polling from the
browser side — the old version called `run()` on a timer, which meant recompiling the whole wrapped chunk
in the game every tick; the current version compiles once and lets the game push. A green dot tracks the
local player in real time (~10 Hz, matching the 0.1s tick) on the map, and a **Follow player** option
recenters the view on every update.

With that connection open, teleport spots gain a real, working **⇱ Teleport here** button (calls
`Ess.Player.teleport(x, y, z, yaw)` over the same bridge) and a **Save current spot** button that reads the
live pose to mint a new spot. Spots can also be added by pasting raw `[Ess][LOCATION]` log lines or JSON
directly into the import box. An **Export** action dumps all current spots (built-in + saved) as JSON to
paste back into the repo for everyone.

**Tracks only the local player** — `Ess.Player.pose(0)`, one green dot. It does not track other players,
NPCs, or objects.

## Fully opt-in

Every feature except the live overlay and its teleport actions works with **no game connection at all** —
loading layers, toggling visibility, collect-tracking, importing/exporting teleport spots by hand. Connecting
is purely additive.

## Where the map image comes from

The backdrop is **not generated from world geometry by this tool**. `tools/gen_map_image.py` downscales an
already-existing retail `map.jpg` (8204×8204) sourced from a sibling repo, `mercs2-tools`, into a base64
data URI embedded in `src/data/map-image.js`. Marker placement reuses the exact edge-driven world↔pixel
transform from `mercs2-tools/missionforge.html` verbatim (described in-repo as "confirmed pixel-perfect").
Because Leaflet's `CRS.Simple` coordinate space is the logical 8204-unit span rather than the embedded
picture's real pixel size, the picture can be downscaled for file size without touching the calibration.

## Status

Same posture as the [Lua Web IDE](web-ide): the WebSocket client code (a copy of the same `ess-bridge.js` —
reconnect with backoff, nonce-tagged ack/result correlation, an 8s no-hang timeout) is complete and
non-trivial, not a stub. But there is no recorded evidence in this repo of an actual live "Connect to game"
session against a real running game. Treat it as **written and internally consistent, not yet confirmed via
live testing.**

## See also

- [Lua Web IDE](web-ide) — the other WebSocket-transport client, running arbitrary code instead of a fixed
  pose-streaming loop.
- [WebSocket Transport](../lua-bridge-api/websocket) — the wire protocol the live overlay and the teleport
  actions both ride on.
- [Ess.Loop](../ess/timing-input#ess-loop) — the heartbeat the in-game setup chunk starts to stream pose
  updates.
- [Ess.Player](../ess/identity-query#ess-player) — `pose(0)` (streamed every tick) and `teleport(x,y,z,yaw)`
  (called by the Teleport-here button).
