---
title: Live Tools
nav_order: 16
has_children: true
has_toc: false
---

# Live Tools

End-user **web apps** — normal pages in a normal browser tab — that connect live to a running copy of the
game. Distinct from [Frameworks](../frameworks), which is for Lua *libraries* other mods build on (like
[Essentials (Ess)](../ess/)): a framework ships as a `.lua` file you drop into your own mod, while a Live
Tool ships as a page you just open, with no Lua of your own to write.

The shared thread behind both tools below: `lua-bridge` (repo `Merc2-Mods-Exp`, mod `lua-bridge-DEV`) added
a hand-rolled **WebSocket server** in v0.4.1, riding the same `127.0.0.1:27050` socket its raw-TCP REPL
already used — see [WebSocket Transport](../lua-bridge-api/websocket) for the wire protocol. That transport
turns the bridge into something a browser can talk to directly, with no Python relay or native install in
between. These two tools are its first real consumers: a live Lua IDE, and a live player-position map. Both
run entirely client-side — a single self-contained HTML file — and need nothing on top of the game itself
and the bridge DLL to actually execute code or track a position live.

- **[Lua Web IDE](web-ide)** — a real, in-browser Lua editor: CodeMirror 6 with `Ess.*`-aware and
  native-engine-call autocomplete, a lint pass that catches beginner mistakes before they ever leave the
  page, a script library, an examples gallery, and a two-layer API reference, all baked into one shipped
  `index.html`. Hit Run and the code executes inside your actual running game over the WebSocket transport,
  with results and the live game log streamed straight back.
- **[Live Map](live-map)** — a Leaflet map of the game world that overlays any JSON file of world-space
  points as a toggleable layer (collectible toolboxes and teleport spots ship built in), and — optionally —
  opens the same WebSocket connection to track your live player position on the map in real time, with a
  working in-game teleport button once connected.

Both are dual-mode: everything that doesn't need the game (browsing, editing, loading a layer) works with no
connection at all, and both are hosted, downloadable, and servable directly by the bridge itself.
