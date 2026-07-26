---
title: Visual Editor
parent: Live Tools
nav_order: 3
---

# Visual Editor

## Overview

`mercs2-ess-visual` is a node-graph editor for scripting *Mercenaries 2* Ess mods visually: wire up a
trigger and a sequence of actions, hit **Compile**, and get a real `scripts/OnKey/*.lua` file out. It's
built on [litegraph.js](https://github.com/jagenjo/litegraph.js) — "the same engine ComfyUI's own node
canvas runs on," per the repo's own README — vendored here unmodified (MIT) rather than pulled in as a live
dependency. Live at **[visual.mercs2.tools](https://visual.mercs2.tools)**; source at
[github.com/loganw234/mercs2-ess-visual](https://github.com/loganw234/mercs2-ess-visual). Like the
[Lua Web IDE](web-ide), there's no build step and no dependencies to run locally either: `python -m
http.server` in the repo folder, or just open `index.html` directly in a browser.

**Status: draft / proof of concept.** That's the repo's own words, not a hedge added here — the live page's
own `<title>` tag calls it "a node-graph draft for scripting Ess mods." Small on purpose; see
[What's not here yet](#whats-not-here-yet) below before extending it. "Draft" doesn't mean idle, though: it's
under active, incremental development — branching, captured return values, Function Blocks, save/load,
undo/redo, autosave, a full Native tier, and Connect + Run have all landed as separate, working commits
rather than one big-bang rewrite.

## The three node tiers

**411 node types** (40 sidebar categories, confirmed against the live tool's own node-library count), split
across three tiers:

- **Ess (201)** — one node per real `Ess.*` call. Every `Ess.Easy.*` function has one, plus a wide slice of
  the Core tier for the namespaces modders touch most: Object, Human, Vehicle, Player, Camera, Markers,
  Relations, AI Orders, Followers, Squad, Hud, Sound, Missions, Cinematic, Loop, Keys, Triggers.
- **Native (193)** — bare engine calls (`Object.SetName`, `Marker.AddDisc`, `Camera.SetPitch`) for
  capability Ess doesn't wrap yet: animation, winch/cargo, attachment, vehicle doors/turrets/hijacking, raw
  markers, HUD fanfares, the dynamic music system, and player costumes/disguise/satellite-scan. These are
  colored warm and bucketed under their own "Native: X" sidebar categories, deliberately separate from the
  Ess tier, so a graph never quietly mixes "goes through Ess's safety net" with "doesn't."
- **Flow Control (17)** — `Branch (If)`, `Compare`/`And`/`Or`/`Not`, arithmetic, `Set Local`, `Log`,
  `Custom Code`, and the **Function Start / Function Return / Call** trio for reusable, parameterized
  functions compiled into real `local function name(...) end` blocks.

Plus one dynamically-generated **Call: name** node per function you define.

**This is a different three-way split from [Ess's own three tiers](../ess/#the-three-tiers)**
(`Easy`/`Core`/`Raw`), worth keeping distinct rather than conflating: Ess's tiers describe how much of Ess's
*own* safety net a given call opts into, all inside the `Ess.*` namespace. The editor's tiers are a
different axis — which of the *editor's* node categories a call lives in, and, specifically for Native,
whether it goes through Ess at all. An Ess-tier node here can wrap either an `Ess.Easy.*` preset or a
Core-tier call — both share the same 201-node Ess bucket — while every Native node bypasses Ess entirely and
talks straight to the engine, which is exactly why it gets its own warm color and its own sidebar section
instead of blending in with everything else.

## Workflow

1. **Pick a starting point.** The tool opens on **Spawn & Control** (spawn a car ahead, capture its guid,
   face it at you, heal it, log where it landed, clean it up). Nine more live under **Load a boilerplate
   sample** (top right), each adapted from a real, smoke-tested script in
   [mercs2-lua-essentials](https://github.com/loganw234/mercs2-lua-essentials)'s own `samples/`:

   | Sample | Demonstrates |
   |---|---|
   | Spawn & Control | the default: spawn → capture guid → act, with the guid **wired** into both consumers |
   | Command a Squad | a captured **guid list** feeding straight into `AI Orders: Attack`, no per-unit bookkeeping |
   | Direct the Camera | capturing a **closure** (`Camera: Orbit`'s `stop`) and calling it later from `Custom Code` |
   | Command a Helicopter | the "(Full)" crewed-template and `Vehicle: Fly To` gotchas baked in |
   | Trailer Hitch | the one **Native**-tier sample — two spawns, two captured guids, welded together with `Object.Attach` |

   Five more share the same picker — Mark & Notify, A Quick Mission, Call In Support, World Tweaks, and
   Timers & Loop — rounding out all ten. Every sample compiles to runnable Lua with no edits first (see
   [Status](#status)).
2. **Edit it.** Click a node in the left sidebar to drop it on the canvas, or double-click empty canvas to
   search all 411 of them by name. Drag from a node's dot to wire it.
3. **Set your hotkey** on the **On Key Press** node — the bright green one, where every script starts.
4. **Hit Compile.** The generated Lua appears on the right. The status line reports how many lines came out
   and warns about any node that isn't connected to a trigger — those compile to nothing.
5. **Name it, download the `.lua`, and install it**: drop it in your game folder's `scripts/OnKey/`, load a
   save, press the key.

Or skip the manual install: with the game running and lua-bridge listening, hit **Connect** then **Run in
game** to send the compiled script straight over and watch the exec chain light up on canvas as it fires.
This rides the exact same lua-bridge WebSocket transport as the [Lua Web IDE](web-ide) and
[Live Map](live-map) — see [WebSocket Transport](../lua-bridge-api/websocket) for the wire protocol — so all
three Live Tools now share one connection mechanism to the running game, just for different jobs: editing
text, tracking a position, or running a compiled graph.

## Working with a graph

- **Fit to View** — frames the whole graph on screen. Shortcut `F`. Runs automatically on load and whenever
  you switch samples.
- **Save / Load Graph** — round-trips the whole graph as a portable `.json` file.
- **Autosave** — saves to the browser as you work and picks up where you left off next time, no prompt, no
  lost work. A banner offers a sample instead if the canvas is empty, and can hand your graph back if you
  take it.
- **Undo / Redo** — `Ctrl+Z` / `Ctrl+Y`, or the toolbar buttons. Up to 50 steps.
- **Copy / Paste / Select All / Delete** — `Ctrl+C` / `Ctrl+V` / `Ctrl+A` / `Del`, litegraph's own; paste-then-nudge is how you duplicate a node.
- **New Group** — select some nodes, click it, give it a title: a labeled, colored box around exactly what
  you selected. Right-click a group → **Edit Group** to rename, recolor, or resize it afterward.

## Extending the node library

Every node follows the same three-part shape: exec-in/exec-out pins wire it into the sequence, an
`addInput`/`addProperty`/`addWidget` triple per value slot (a pin with a widget fallback), and an `onAction`
that resolves its inputs, emits a line of Lua text, and fires its own `then` output. A pure-data node with no
exec pins at all (like `Random Number`) skips `onAction` entirely and just implements `onExecute` calling
`setOutputData` with Lua expression text.

**Where a signature comes from.** The repo's [DESIGN.md](https://github.com/loganw234/mercs2-ess-visual/blob/master/DESIGN.md)
lays out a strict trust order for anything a node emits, highest first:

1. **The decompiled game source and the loader's own implementation** — e.g. the valid `KEYVAL` key names
   on `On Key Press` are transcribed straight from `ResolveKeyName()` in the lua-bridge loader's C source,
   the actual code that turns a string into a key binding. Anything it doesn't recognize resolves to no
   binding at all, silently.
2. **Ess itself** (`mercs2-lua-essentials/src/*.lua`), which builds directly on that source — every `Ess.*`
   node's argument shape and return value is checked against the real function. Ess and the loader don't
   always agree: the loader accepts `"alt"` as a key name, Ess's own `NAMES` table in `25_keys.lua` doesn't,
   so `On Key Press` and `Keys: On` deliberately offer different lists.
3. **This wiki**, last, and only for the Native tier. That ordering is deliberate: this wiki is itself
   reverse-engineered from decompiled scripts and still being built, so it's one level removed from the
   source in the same way this very page is — trusting it first would mean building a node on a guess about
   a guess. Every Native candidate was checked against this wiki's own per-function confidence notes
   ("Confirmed in real scripts," "Live-confirmed via WebSocket lua-bridge probe," or "no call sites found —
   unconfirmed"); anything flagged with a bare, unclear `(...)` signature was left out entirely, and an
   unconfirmed-but-simple call says so plainly in its own `.desc`.

**A footgun worth knowing before you add one.** litegraph shares one index space across every `addInput`
call on a node, assigned in call order — an `"exec"` input added first claims slot 0, so the next `addInput`
is slot 1, not 0:

```js
this.addInput("exec", LiteGraph.ACTION);    // slot 0
this.addInput("someValue", "number");       // slot 1 -- not 0
// ...
var v = CodeGen.resolveInput(this, 1, "someValue");   // must match the real slot index
```

`CodeGen.resolveInput`'s slot argument has to match that real position. Get it wrong and the node doesn't
throw an error — it silently falls back to its widget's default value instead of reading the wire that's
actually connected, with nothing on screen to flag it. The documented advice is blunt: always compile and
read the output.

## New in Ess v0.4.2: a machine-verified node dataset

Ess's own [CHANGELOG](https://github.com/loganw234/mercs2-lua-essentials/blob/master/CHANGELOG.md) adds a
second thread here, entirely on the framework side. Its **0.4.2** entry describes this editor's hand-written
Ess-tier nodes plainly: "~200 nodes... hand-written against `src/*.lua` — accurate, but maintained by
memory" (that figure lines up with the editor's own 201 Ess-tier nodes above; 0.4.2's generated dataset only
concerns `Ess.*` calls, not the separate Native or Flow Control tiers).

0.4.2 generates an alternative dataset instead of hand-writing it: `build/nodes.py` merges `dist/ess.json`
(derived straight from `src/`, so it can't drift out of sync) with a hand-authored `api/nodes.overlay.json`
— the human-written half that supplies what a bare signature can't: what a parameter is *for*, what units
it's in, and which of them silently do nothing. The overlay is validated at build time and, in the
changelog's own words, "cannot invent anything": an entry naming a function that doesn't exist, or giving a
real function a parameter it doesn't have, fails the build outright. The result is a second, larger catalog —
**486 nodes**, all **896 parameters** carrying a confirmed type, a working default, and a hand-written
explanation, plus 62 functions deliberately skipped with a written reason each (93 of the 486 are the
`Ess.Easy.*` beginner tier; 138 are pure getters). 0.4.2 also ships `dist/ess-nodes.generated.js`, a working
litegraph consumer proving the generated data holds together end to end — but that file lives in the Ess
repo, not this editor's, registered under its own `essgen/` type prefix specifically so it can coexist with
this editor's existing `ess/` nodes without a load-order collision.

State this precisely, in the changelog's own words, because it's easy to over-read: **"Tooling only — the
framework itself is unchanged."** This release produces the *data*. **"Nothing in the editor's own repo is
touched."** Adopting the generated dataset into this editor's actual node library — replacing or
supplementing the hand-written nodes above with the generated ones the tooling already produces — is a
separate step that hasn't happened yet.

## What's not here yet

Straight from the README's own accounting, plainly:

- **Only one compile target** (an OnKey script). An OnLoad target and an "HTML tool button" target are both
  natural next steps — same node library, different compiler backends.
- **No real topological sort for data-node-to-data-node chains.** The compiler's pre-pass runs every data
  node once, in whatever order the graph's own node list returns (creation order, not dependency order) — so
  chaining Flow Control's `Compare`/`And`/`Or`/arithmetic nodes into each other works whenever the upstream
  one happens to land earlier in that list, but isn't guaranteed. Keep those chains shallow.
- **List/table-shaped parameters are raw text widgets, not a real list-building UI.** A "guids" or "spawns"
  parameter is a string widget whose text IS a Lua table literal — you type `{ Ess.Guid('some_unit') }` by
  hand. `Combine List (4)` covers the fixed-four case; a real variable-arity list-builder would be nicer.
- **An already-placed Call node doesn't resize when you edit its function's signature.** litegraph has no
  live pin migration for an existing instance when its type re-registers. Delete and re-drop it.

## Credit and license

`lib/litegraph.js` / `lib/litegraph.css` are vendored, unmodified, from
[jagenjo/litegraph.js](https://github.com/jagenjo/litegraph.js) (MIT). `lib/tokens.css` and
`lib/bridge-client.js` are vendored from this ecosystem's own
[mercs2-tools-shared](https://github.com/loganw234/mercs2-tools-shared). Everything else in the repo is MIT.

## Status

The repo states its own status plainly, and this page has kept that framing throughout rather than softening
it: **draft / proof of concept**, small on purpose.

That's not the same as untested. Confirmed directly against the live tool for this page: loading the default
Spawn & Control sample fresh and hitting Compile with no edits produced working Lua on the first try —

```lua
local __spawn1 = Ess.Object.spawnAhead('Veyron', 8)
Ess.Object.faceObject(__spawn1, Ess.Player.character(0))
Ess.Object.heal(__spawn1)
local cx, cy, cz = Ess.Object.pos(__spawn1)
Ess.Log(string.format('[graph] spawn_and_control: car @ %.1f,%.1f,%.1f', cx or 0, cy or 0, cz or 0))
local __trigger1 = Ess.Easy.Triggers.after(6, function() Ess.Object.remove(__spawn1) end)
```

— matching the README's own claim that every one of the ten samples "compiles to runnable Lua with no edits
first," each one's Ess calls, parameter shapes, and cleanup timing translated node-for-node from the real
recipe wherever node coverage allows.

`DESIGN.md` separately documents two real bugs its own persistence system shipped with, both found, in its
own words, "by actually testing it, not just reading the code": a two-pass restore ordering gap that could
leave a saved Call node as a dead placeholder, and a widget-sync bug in Function Start/Return's `onConfigure`
that silently destroyed a function's restored wires on load — a Save → Load round trip looked fine right up
until you compiled it and got `nil` where a real value used to be. Both are fixed; the point is that this
tool's persistence layer has genuine test-caught-a-real-bug history behind it, not just code that reads
correctly.

Connect + Run itself rides the same lua-bridge WebSocket transport the Lua Web IDE and Live Map both use —
see [WebSocket Transport](../lua-bridge-api/websocket)'s own Status section for that transport's
separately-recorded live-client evidence. Nothing in this repo's own docs makes an independent
"confirmed live in-game" claim for Connect + Run beyond describing it as shipped, working functionality —
so treat it as resting on that shared transport's own evidence rather than as separately re-verified here.

## See also

- [Lua Web IDE](web-ide) — the other browser tool built on the same lua-bridge WebSocket transport; both
  ultimately ride `Loader.WsSend`.
- [Live Map](live-map) — the third client on that same transport, tracking a live player position instead of
  running a compiled script.
- [WebSocket Transport](../lua-bridge-api/websocket) — the wire protocol all three Live Tools' round trips
  ride on.
- [Essentials (Ess)](../ess/) — the framework this editor's Ess-tier nodes wrap one-for-one; see
  [The three tiers](../ess/#the-three-tiers) for Ess's own Easy/Core/Raw split, a different axis from this
  editor's own Ess/Native/Flow Control tiers.
