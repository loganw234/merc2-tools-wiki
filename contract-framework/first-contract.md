---
title: End-to-End Walkthrough
parent: Contract Framework
nav_order: 8
---

# End-to-End Walkthrough

> **Status: new, in development.** This walks through the pipeline as each piece's own source documents
> it. The full chain — Forge placement through a played, completed contract — hasn't been independently
> re-confirmed as one continuous live session in this writeup; treat each individual step as accurate to
> the code, and the walkthrough's shape as the intended path.

Everything on the other pages in this section, tied together: from an empty level to a contract you can
actually accept and play, without writing any Lua by hand.

## 1. Deploy the framework

Two files, in `scripts/OnLoad/` and `scripts/OnKey/` respectively, with `ContractFramework.lua` loading
**before** any contract file:

```ini
[OnLoad]
ContractFramework.lua=5
```

`contracts.lua` (the [Contract Board](contract-board)) goes in `scripts/OnKey/` — its `KEYVAL` (`f5`)
auto-binds, no `.ini` entry needed. It also needs `contracts.gfx`, `cpanel.gfx`, and `cbar.gfx` alongside
it. At this point, pressing **F5** already shows a working board — in **demo mode**, with three fake
contracts, since nothing real has been registered yet.

## 2. Place a mission with MissionForge

Drop `MissionForge.lua` into `scripts/OnKey/` (`F7` auto-binds). Load into a level, walk to where you want
the mission to start, and press **F7**.

A small, concrete example — three vehicles to destroy, then reach an extraction point:

1. Open the menu into a faction's Vehicles branch, highlight one, walk to a spot, press **P** three times
   at three different spots (each drop is a separate placement, no group needed for a simple `destroy` —
   see [Objectives Reference](objectives) for how "destroy" sources targets from a live area query when
   nothing was explicitly grouped).
2. Open **OBJECTIVES → Reach / Go To**, walk to where extraction should be, press **P**.
3. Press **End** to export.

Check `lua_loader_printf.log` for the `MISSIONFORGE_EXPORT = { ... }` block — copy it, from
`MISSIONFORGE_EXPORT = {` through the matching closing `}`.

## 3. Finish it in the web tool

Open `missionforge.html`. Paste the export into **1 · Load / import**, click **Load**. The editor populates
from your placements:

- **2 · Mission details** — give it an `id`, a `title`, a `briefing`, a reward.
- **4 · Objectives** — the destroy objective and the reach objective are both already there; adjust
  descriptions, add a quota, whatever the mission needs.
- **5 · Units** — the three vehicles should show up here, auto-classified.
- Skip 3/6/7/8/9 entirely for this simple example — none of them are required.

The right-hand pane shows the generated `Contract.Register({...})` Lua updating live as you edit. Click
**Download .lua** (or **Copy** and paste into a new file yourself).

## 4. Deploy the generated contract

Save the downloaded file into `scripts/OnLoad/`, with a number **higher** than `ContractFramework.lua`'s:

```ini
[OnLoad]
ContractFramework.lua=5
MyFirstContract.lua=15
```

Every generated file already guards against the framework not being loaded yet — if you see
`"... Contract framework not loaded - give ContractFramework.lua a LOWER [OnLoad] number"` in your log,
that's exactly what it's telling you to check.

## 5. Play it

Load into a level. Press **F5** to open the Contract Board — your new contract now appears in the list
(under whatever `category` you gave it), no longer in demo mode. Select it, press **Enter** twice (the
double-press is a deliberate guard against accidentally starting the wrong contract), and the board closes,
teleporting you if a start point was set and beginning the objectives.

A tracker panel stays up in the corner while you play, showing each objective's checkbox state. Finishing
(or failing) plays the native completion fanfare and tears the tracker down automatically — see
[The Contract Board](contract-board#finishing-in-sync-with-the-native-fanfare) for exactly how that
handoff works.

## Where each piece is documented in depth

- [Contract.Register & Lifecycle](register-and-lifecycle) — what actually happens on accept, and the full
  `def` field reference.
- [Objectives Reference](objectives) / [Support Effects & Triggers](support-effects-and-triggers) /
  [Units, AI Orders & Relations](units-ai-and-relations) — everything a contract definition can do, beyond
  this walkthrough's simple destroy-then-reach example.
- [MissionForge](mission-forge) ([deep dive](../deep-dives/mission-forge)) — the full in-game authoring
  controls and design story.
- [The Web Tool](web-tool) — every wizard step, the flow graph, and the live map.
- [The Contract Board](contract-board) — demo mode, the accept/cancel state machine, and the tracker
  widgets.
