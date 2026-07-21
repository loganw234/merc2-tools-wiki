---
title: Live Map
parent: Live Tools
nav_order: 2
---

# Live Map

## Overview

`mercs2-webmap` is an interactive top-down map of the Mercenaries 2 world, built on Leaflet with
`CRS.Simple` (a plain coordinate plane, not geo-projected) over the retail world map image. Live at
**https://map.mercs2.tools/** (confirmed reachable); source at
[github.com/loganw234/mercs2-webmap](https://github.com/loganw234/mercs2-webmap). Like the
[Lua Web IDE](web-ide), it's a single standalone HTML file — no build step to use it, no server, no external
requests — hosted on GitHub Pages or downloaded and opened straight off disk.

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

## Terrain: the heightmap layer

A new **heightmap layer** (`src/app/34_heightmap.js` + the generated `src/data/heightmap.js`) sits alongside
the point layers above, as a separate ground-height overlay. To be clear about what did and didn't change:
the `map.jpg` backdrop, the collectibles dataset, and the seeded teleport-spot data are all **unchanged** —
this is new data layered on top, not a redo of the existing ones.

The data itself is a dense, base64-packed grid: a row-major `Int16` array of ground heights (world units × 10,
`-32768` = never sampled) at a 16-unit cell size across the full 500×500-cell map, plus a parallel `Uint8`
"source tier" plane recording which gathering method won each cell (vehicle > foot > terrain-probe >
grid-probe > heli-sweep, most trustworthy first, per the repo's own tiering comment). It's built by
`tools/build_heightmap.py` from the raw position logs in `data/*.log` — ~870 KB of packed binary before the
base64 stretch — and committed as a generated, vendored-asset file the same way `map-image.js` is.

On top of that tensor:

- **`WM.heightAt(x, z)`** — bilinear-interpolated ground height at any world point, falling back to an
  inverse-distance blend near sparse edges — and **`WM.slopeAt(x, z)`** — terrain slope in degrees. Both
  return `null` for genuinely unscanned ground rather than guessing at it.
- A **canvas overlay**: a hypsometric color ramp split at the game's actual water surface (≈ -35, not 0) —
  blue bathymetry below, green-through-brown land above — with optional Horn hillshade and 25-unit contour
  lines, painted once into an offscreen canvas and shipped as a single Leaflet `imageOverlay` (so the full
  501×501 grid pans smoothly instead of one `L.rectangle` per cell). It renders in its own Leaflet pane
  (touches `src/app/10_map.js`, which now also gives the base map its own low pane) stacked above the map
  image but below the marker layers, so it never hides a marker under it.
- An **LZ finder** toggle that highlights ground that's flat (under 8°), dry, and fully scanned — a quick way
  to spot heli-landing or base-building spots.
- A two-click **elevation profile** tool (`WM.startProfile`): click a start and an end point and get a drawn
  cross-section with distance and low/high readouts, plus a **line-of-sight** check between the two points'
  standing eye height that flags where (and whether) the terrain in between blocks the view.

All of it is new panel controls under a "Heightmap" section in `src/app/40_ui.js`, hidden entirely if a build
has no heightmap data embedded.

**Where the tensor comes from.** A set of new in-game Lua scripts — `ingame/RoadLogger.lua`, `FootLogger.lua`,
`GridProbe.lua`, `HeliSweep.lua`, `HeliMap.lua`, `GroundStream.lua`, `TerrainProbe.lua` — each gather ground
samples by a different method (driving, walking, physics-drop probes, aerial sweeps) and broadcast every
sample over the same hidden `Loader.WsSend` WebSocket channel the live player overlay below already uses.
They're Lua data-gathering tools that feed this pipeline, not features of this map page itself — except
`RoadLogger.lua`, whose broadcasts the map also listens to directly (see "Mapping mode" below). A Python
pipeline in `tools/` then turns the accumulated logs into everything above and more: `build_heightmap.py`
builds the tensor, and a new `build_all.ps1` chains it through the rest of a 9-step build — the webmap
bundle, a 3D export (a display model and a game-exact raw model), an in-game height-oracle Lua file, a
printable STL, a raw tensor data drop, and a terrain "almanac" summary.

## Connecting to the game

**Connect to game** opens a WebSocket to `ws://127.0.0.1:27050` — see
[WebSocket Transport](../lua-bridge-api/websocket) for the wire protocol — and, on open, sends **one** setup
Lua chunk that starts an in-game [`Ess.Loop`](../ess/timing-input#essloop) ticking every 0.1s. Each tick
reads [`Ess.Player.pose(0)`](../ess/identity-query#essplayer) and pushes `x,y,z` out over the hidden
`Loader.WsSend` channel, tagged for pose updates. This is deliberately **not** per-frame polling from the
browser side — the old version called `run()` on a timer, which meant recompiling the whole wrapped chunk
in the game every tick; the current version compiles once and lets the game push. A green dot tracks the
local player in real time (~10 Hz, matching the 0.1s tick) on the map, and a **Follow player** option
recenters the view on every update. With the heightmap layer above loaded, the live coordinate readout also
shows an **AGL** figure (height above the ground under the player, via `WM.heightAt`) once it's more than a
few units — covering flying, falling, or standing on a roof — and flags **UNDERWATER** once the player's `y`
drops below the sea surface (`src/app/30_live.js`).

With that connection open, teleport spots gain a real, working **⇱ Teleport here** button (calls
`Ess.Player.teleport(x, y, z, yaw)` over the same bridge) and a **Save current spot** button that reads the
live pose to mint a new spot. Spots can also be added by pasting raw `[Ess][LOCATION]` log lines or JSON
directly into the import box. An **Export** action dumps all current spots (built-in + saved) as JSON to
paste back into the repo for everyone. Right-clicking **anywhere** on the map now opens that same teleport
action for an arbitrary point, snapped to the ground: it reads `WM.heightAt` there and lands you a couple of
units above the surface, just above the water line if the point is underwater, or high up with an explicit
"no height data" note if that spot hasn't been scanned yet (`src/app/26_teleport.js`).

**Tracks only the local player** — `Ess.Player.pose(0)`, one green dot. It does not track other players,
NPCs, or objects.

## Mapping mode

There's no UI toggle for this one — `src/app/36_mapping.js` just listens on the same hidden WebSocket channel
the live overlay uses. When the in-game `RoadLogger.lua` script (bound to F11) is running, it broadcasts
`<<ROADLOG>>START`, one `<<ROADLOG>>PT x,y,z,yaw` per logged point, and `<<ROADLOG>>STOP n` — alongside its
normal `[ROAD]` game-log lines — and `src/app/30_live.js`'s `onData` recognizes the tag and hands it off. The
map then:

- auto-draws an amber breadcrumb trail as the points arrive, breaking into a new segment across any jump
  bigger than 80 units so a teleport doesn't draw a line across the map,
- tallies a running sample count and distance,
- persists the session to `localStorage` so it survives a reload, and
- can export the samples as `[Ess] [ROAD] ...` lines — the same format `tools/build_heightmap.py` already
  parses — to drop into `data/` and fold into the next heightmap build.

(`GridProbe.lua`'s scattered probe points ride the same channel as a `DOT` variant, plotted as unconnected
dots rather than trail segments.) Because it's driven entirely by telemetry rather than a button, the
"Mapping" panel section itself stays hidden until a signal — or a restored session — actually exists.

## Teleport to all points

Every marker the generic layer loader places — not just the seeded teleport spots — now carries its world
position (`src/app/20_layers.js`). A persisted **Teleport to all points** toggle in the Teleport spots panel
injects a working **⇱ Teleport here** button into *any* marker's popup, not only teleport-kind ones. Turning
it on goes through a small confirmation dialog first — `src/app/28_modal.js`, a general-purpose modal built
for this — with a bit of tongue-in-cheek copy about it being "not *too* cheaty"; turning it back off needs no
ceremony. `src/app/26_teleport.js` wires the injected button into whichever popup is open, live-reflecting
whether a game connection currently exists.

## Fully opt-in

Every feature except the live overlay and its teleport actions works with **no game connection at all** —
loading layers, toggling visibility, collect-tracking, importing/exporting teleport spots by hand. The
heightmap layer (heights, hillshade, contours, the LZ finder, the elevation profile) is likewise fully
offline — it's baked into the build from committed logs, not streamed live. Mapping mode and the
ground-snapped right-click teleport both need a live connection like the rest of the live-overlay family; the
**Teleport to all points** toggle itself flips with no connection, but the buttons it adds only do anything
once connected. Connecting is purely additive.

## Where the map image comes from

The backdrop is **not generated from world geometry by this tool**. `tools/gen_map_image.py` downscales an
already-existing retail `map.jpg` (8204×8204) sourced from a sibling repo, `mercs2-tools`, into a base64
data URI embedded in `src/data/map-image.js`. Marker placement reuses the exact edge-driven world↔pixel
transform from `mercs2-tools/missionforge.html` verbatim (described in-repo as "confirmed pixel-perfect").
Because Leaflet's `CRS.Simple` coordinate space is the logical 8204-unit span rather than the embedded
picture's real pixel size, the picture can be downscaled for file size without touching the calibration.

## Status

Same posture as the [Lua Web IDE](web-ide) on the code itself: the WebSocket client (a copy of the same
`ess-bridge.js` — reconnect with backoff, nonce-tagged ack/result correlation, an 8s no-hang timeout) is
complete and non-trivial, not a stub.

Since this page was last written, the surrounding evidence changed a lot, though not quite enough to flip the
verdict below. The repo now carries `data/RoadMarkersSession1.log` plus 17 further logged sessions (the
`GroundStream (*).log` series, `TotalCoverage.log`, `RapidTest.log`, the `GridProbe`/`MixedProbe` sessions,
`RoadMarkersSession2.log`) — real captured game output, not synthetic fixtures: `RoadMarkersSession1.log`
opens with genuine `[Ess]` boot-banner lines (`Net: v0.2.1 ready`, `Contract: loaded`, and so on) followed by
real `[ROAD]` position samples, and the
heightmap tensor's own metadata reports 1,441,266 merged samples across all those logs. The commit history
over that same terrain effort describes several live-only failure modes found and fixed by iteration — e.g.
"GroundStream: use Ess.Camera wrappers (raw Camera.* was the crash)", "GroundStream: no teleport -- start the
camera where the player stands (fix load crash)", "HeliMap: never move the player mid-run -- ride the heli
(fixes load-loop crash)", and the final terrain commit's own description of a "streaming-stall zero-hold"
fix — the kind of bug you only find by actually running these scripts against a live game, repeatedly. Taken
together, that's substantially stronger circumstantial evidence than before that the underlying
lua-bridge/Ess connection works and was exercised heavily.

That still isn't the same thing as "the live map page's Connect-to-game overlay was confirmed end to end,"
and the gap matters here specifically. `RoadLogger.lua`'s own header notes that, besides broadcasting over
the WebSocket hidden channel, it *also* writes the identical `[ROAD]` lines straight to the game's own log
file as an offline fallback, explicitly so it "can map with or without the map open." Every piece of telemetry
above — the boot banners, the position samples, the iteration-fixed crashes — is fully consistent with the
Lua side having been driven and logged directly, with nothing ever reading it back over the WebSocket or
rendering it in a browser. No commit message, README line, or code comment anywhere states that the webmap
page itself was opened, **Connect to game** was clicked, and the dot or the mapping trail was actually watched
moving on the map. Treat the live overlay — and everything gated on it: the teleport buttons, the
ground-snapped right-click teleport, mapping mode's auto-draw, the AGL/underwater readout — as resting on much
stronger circumstantial evidence of a working connection than before, but **still not confirmed as working
end-to-end through this page's own UI.**

## See also

- [Lua Web IDE](web-ide) — the other WebSocket-transport client, running arbitrary code instead of a fixed
  pose-streaming loop.
- [WebSocket Transport](../lua-bridge-api/websocket) — the wire protocol the live overlay and the teleport
  actions both ride on.
- [Ess.Loop](../ess/timing-input#essloop) — the heartbeat the in-game setup chunk starts to stream pose
  updates.
- [Ess.Player](../ess/identity-query#essplayer) — `pose(0)` (streamed every tick) and `teleport(x,y,z,yaw)`
  (called by the Teleport-here button).
