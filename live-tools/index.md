---
title: Live Tools
nav_order: 5
has_children: true
has_toc: false
---

# Live Tools

End-user **web apps** — normal pages in a normal browser tab — that connect live to a running copy of the
game. Distinct from a Lua *library* you build a mod on — [Essentials (Ess)](../ess/), or anything under
[Frameworks](../frameworks): a library ships as a `.lua` file you drop into your own mod, while a Live Tool
ships as a page you just open, with no Lua of your own to write.

The shared thread behind all three tools below: `lua-bridge` (repo `Merc2-Mods-Exp`, mod `lua-bridge-DEV`)
added a hand-rolled **WebSocket server** in v0.4.1, riding the same `127.0.0.1:27050` socket its raw-TCP REPL
already used — see [WebSocket Transport](../lua-bridge-api/websocket) for the wire protocol. That transport
turns the bridge into something a browser can talk to directly, with no Python relay or native install in
between. These three tools are its consumers: a live Lua IDE, a live player-position map, and a visual
node-graph editor that compiles to Lua. All run entirely client-side — a single self-contained HTML file —
and need nothing on top of the game itself and the bridge DLL to actually execute code, track a position, or
run a compiled graph live.

- **[Lua Web IDE](web-ide)** — a real, in-browser Lua editor: CodeMirror 6 with `Ess.*`-aware and
  native-engine-call autocomplete, a lint pass that catches beginner mistakes before they ever leave the
  page, a script library, an examples gallery, and a two-layer API reference, all baked into one shipped
  `index.html`. Hit Run and the code executes inside your actual running game over the WebSocket transport,
  with results and the live game log streamed straight back.
- **[Live Map](live-map)** — a Leaflet map of the game world that overlays any JSON file of world-space
  points as a toggleable layer (collectible toolboxes and teleport spots ship built in), and — optionally —
  opens the same WebSocket connection to track your live player position on the map in real time, with a
  working in-game teleport button once connected.
- **[Visual Editor](visual-editor)** — a node-graph editor (litegraph.js) for building an OnKey mod without
  writing Lua by hand: wire triggers to actions across 411 nodes (`Ess.*` calls, bare native calls, and flow
  control), hit Compile, and either download the generated `.lua` or send it straight into the running game
  over the same WebSocket transport. **Status: draft / proof of concept**, the repo's own words — young and
  small on purpose, not feature-complete.

All three are dual-mode: everything that doesn't need the game (browsing, editing, loading a layer, building
a graph) works with no connection at all, and each is hosted on its own domain and downloadable/runnable as
a single file with no build step.

Source: [mercs2-lua-web-ide](https://github.com/loganw234/mercs2-lua-web-ide) ·
[mercs2-webmap](https://github.com/loganw234/mercs2-webmap) ·
[mercs2-ess-visual](https://github.com/loganw234/mercs2-ess-visual).
