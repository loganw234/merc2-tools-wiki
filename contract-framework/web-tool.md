---
title: The Web Tool
parent: Contract Framework
nav_order: 7
---

# The Web Tool

> **Status: new, in development.** Read directly from `missionforge.html` (read in full) and `flowgraph.js`
> (structure/purpose confirmed). Behavior described here is what the code currently does, not yet
> independently confirmed by extended live use.

`missionforge.html`, in the companion `mercs2-tools` web hub, is the piece aimed squarely at
**non-programmers**: paste what [MissionForge](mission-forge) captured in-game, fill in mission details
and fine-tuning through plain forms, and copy out a finished `Contract.Register({...})` — no Lua
authoring required. It's one tool among several on that hub site (a save-game editor and a cheat-menu
builder live there too, unrelated to contracts); this page covers only the MissionForge companion.

## Step 1 — Load

Paste **either**:

- A `MISSIONFORGE_EXPORT = { ... }` dump straight from `lua_loader_printf.log`, or
- An existing, previously-generated `Contract.Register({ ... })` file — to **re-open and edit** a mission
  you (or someone else) already finished and deployed.

Both are parsed by a small hand-written Lua-table reader built into the page (handles nested tables,
`Contract.Reach({...})`-style calls, comments, and captures whole `function ... end` bodies as opaque
text) — nothing is sent anywhere; the whole tool runs client-side in the browser. Two "Load ... demo"
buttons load sample exports (matching `grand_prix.lua`/`convoy_demo.lua`) if you just want to see the tool
work before making your own.

Re-importing a generated contract is a genuine **round trip**, not just a re-paste: it even reverses a
`fResolve` function body with a regex to pull `Pg.Spawn(...)` calls back out as editable "provided units,"
so a contract generated, tweaked by hand, and re-opened later doesn't lose that hand-editing.

## Steps 2–9 — the wizard

| Step | Covers |
|---|---|
| 2 · Mission details | `id`, `title`, `category`, `briefing`, `intro` radio line, reward cash/fuel, `mode`, `timeLimit`, fanfare message + style. |
| 3 · Player start | Which captured spawn point(s) become `def.start` (or none). |
| 4 · Objectives | One card per placed objective — description, per-type fields, optional/bonus. |
| 5 · Units | Every placed unit, auto-classified as a **destroy target**, a **single target** (verify/escort), or **provided** (spawned at accept, not tied to any one objective). |
| 6 · Relations | Faction ↔ faction stances (friend/neutral/enemy), including **PMC** (the player). |
| 7 · Support call-ins | One card per placed support zone — effect type, position, and that effect's specific fields (ordnance/aircraft/music cue/particle/etc., each from a curated pick-list with a "custom…" free-text escape hatch). |
| 8 · Triggers | Generic named triggers, including the `all`/`count` logic gates, and which supports/orders each one `fires`. |
| 9 · AI Orders | Per-group behavior (move/patrol/defend/attack/hold/face/follow/flee/enter/deploy/animate) and its own trigger condition. |

Every field here maps directly onto the shapes documented in
[Objectives Reference](objectives) / [Support Effects & Triggers](support-effects-and-triggers) /
[Units, AI Orders & Relations](units-ai-and-relations) — the generator (`genLua()`) produces exactly the
`Contract.Register({...})` Lua those pages describe.

## Auto-wiring by group

Anything MissionForge tagged with the same [group letter](mission-forge#group-tags) arrives **pre-wired**:
a trigger and a support call-in placed under the same group are automatically connected
(`trigMode = "ref"`), and an AI order automatically commands the units sharing its group. Nothing stops you
from rewiring any of it afterward, either through the forms or the flow graph below.

## The flow graph

The **⛓ Flow graph** button opens a small, dependency-free node-graph editor (`flowgraph.js`) — drag to
wire a trigger to the support call-ins/AI orders it should fire, double-click a node to jump straight to
its full form card for the finer-grained fields. It edits the **exact same fields** the forms do
(`trigMode`, `ref`, `fires`), so the graph and the forms never fall out of sync — pick whichever is faster
for a given edit. Its own header describes it as reusable for a differently-shaped node relationship in the
future (e.g. objective ordering), decoupled from the rest of the page behind a small `init({state, onChange,
create, locate})` hook interface.

## The live map

A calibrated, pannable, zoomable top-down map (scroll to zoom, drag to pan) plots every placed unit,
objective, support zone, trigger, and AI waypoint over the actual world map image, color-coded by kind.
World coordinates map to image pixels **1:1** once calibrated (`0,0` = image center, the shipped image
spans ±4102 world units each way) — useful for sanity-checking that a "reinforcements arrive here" zone
isn't, say, on the wrong side of a river from the objective it's meant to threaten.

## Output

The right-hand pane always shows the current generated Lua, live, as you edit — **Copy** or
**Download .lua** it, save it into `scripts/OnLoad/` with a higher `lua_loader.ini` number than
`ContractFramework.lua`, and it's ready to play. See
[the end-to-end walkthrough](first-contract) for the complete path from an empty level to a playable
contract.

## See also

- [MissionForge](mission-forge) — the in-game tool this one receives an export from.
- [Contract.Register & Lifecycle](register-and-lifecycle) — the exact shape the generated Lua targets.
- [End-to-End Walkthrough](first-contract) — the full pipeline, start to finish.
