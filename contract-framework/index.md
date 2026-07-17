---
title: Contract Framework
parent: Frameworks
nav_order: 2
has_children: true
has_toc: false
---

# Contract Framework

> **Deprecated — superseded by [Essentials (Ess)](../ess).** This system is absorbed there as native
> `Ess.Contract` — the same objective builders plus the support / trigger / relations / AI-order
> subsystems — shipped in one drop-in `1_Ess.lua`. This page and its children stay as historical reference
> for the standalone predecessor; new mods should build on Ess.

> **Status: new, in development.** This documents a real, substantial system as currently written and
> read directly from source — not a proposal. It hasn't yet accumulated the kind of live-test history the
> rest of this wiki marks with "confirmed working" banners; treat code behavior as authoritative and expect
> this section to gain confirmation notes (and bugfixes) as more of it gets played.

A save-safe, ephemeral custom-mission system for Mercenaries 2 — built as a **framework for other modders
to build on**, not a one-off mod. It exists because the game's own native contract system
(`WifMissionData` + `MrxTask`) corrupts saves if you hook into it: it serializes task nodes *into* the save
file and drives missions through `dynamic_import` + `mrxbriefing` + the `MrxState` load gate. This
framework touches none of that — a contract is a plain runtime object built only from safe primitives
(`Pg.Spawn` / `Event.*` / `Object.*` / `MrxPmc`). It can't corrupt a save because it never writes to one;
the tradeoff is that an active contract doesn't survive a save/reload (it's simply re-offered next level
load).

## The four pieces

- **[`ContractFramework.lua`](register-and-lifecycle)** — the engine. A `Contract.Register({...})` table
  describes a whole mission: objectives, rewards, spawned units, AI orders, faction relations, triggered
  support call-ins. Runs entirely from `scripts/OnLoad/`.
- **MissionForge** — an in-game, Halo-Forge-style authoring tool (`scripts/OnKey/MissionForge.lua`): fly
  around, place things, capture a mission's shape directly in the world instead of guessing coordinates by
  hand. Built on the same input/camera lineage as [ForgeCam](../deep-dives/forgecam) — see the
  [MissionForge deep dive](../deep-dives/mission-forge) for how it got there, or the
  [reference page](mission-forge) for day-to-day use.
- **The web tool** (`missionforge.html`, in the companion `mercs2-tools` repo) — pastes what MissionForge
  captured, then walks a 9-step form (mission details, start position, objectives, units, relations,
  support call-ins, triggers, AI orders) and generates the final `Contract.Register({...})` Lua. This is
  the piece aimed squarely at **non-programmers** — no Lua required to build a working mission. See
  [The Web Tool](web-tool).
- **The Contract Board** (`scripts/OnKey/contracts.lua`) — the player-facing side: a category-grouped
  mission list, a details/rewards/objectives panel, and HUD tracker widgets, all built on the same
  gfxforge/gfx_tool Scaleform pipeline as [Custom UI](../deep-dives/custom-ui). Fully decoupled from the
  engine — it only ever calls `Contract.All/Accept/Abort/Status`, and runs in a demo mode with fake
  contracts if no framework is loaded, so the UI can be worked on standalone. See
  [The Contract Board](contract-board).

## Reference pages

- **[Contract.Register & Lifecycle](register-and-lifecycle)** — the modder API surface, why it's
  save-safe, `Accept`/`Status`/`Abort`, and the built-in demo contract.
- **[Objectives Reference](objectives)** — all 16 objective types, sequential vs. parallel execution,
  nesting, and how objectives source their targets.
- **[Support Effects & Triggers](support-effects-and-triggers)** — scripted call-ins (artillery, airstrikes,
  reinforcements, music/vfx/vo) and the condition system that fires them.
- **[Units, AI Orders & Relations](units-ai-and-relations)** — spawning grouped units, commanding them with
  AI behaviors, and temporarily overriding faction stances for a contract's duration.
- **[MissionForge](mission-forge)** — controls, catalog, and export workflow for the in-game authoring
  tool (see also the [deep dive](../deep-dives/mission-forge) for the design story).
- **[The Contract Board](contract-board)** — the player-facing UI, its four-function engine adapter, demo
  mode, and the tracker widgets.
- **[The Web Tool](web-tool)** — the 9-step wizard, round-trip re-editing, the flow graph, and the live
  map.
- **[End-to-End Walkthrough](first-contract)** — the whole pipeline, start to finish, with a concrete
  worked example.
- **[ContractFramework.lua](source)** — the engine's complete, current source, reproduced in full.
- **[WaveDefense](../wave-defense)** — a full gamemode built on the engine's `onBegin`/`hideTracker` escape
  hatch, using a contract as a bare launcher instead of the whole mission.

## Load order

`ContractFramework.lua` must load **before** any contract file that calls `Contract.Register`. Give it a
low `lua_loader.ini` `[OnLoad]` number:

```ini
[OnLoad]
ContractFramework.lua=5
MyContracts.lua=15
```

Every modder contract file checks `_G.Contract` on load and logs a clear warning (rather than erroring)
if the framework hasn't loaded yet — see [Contract.Register & Lifecycle](register-and-lifecycle) for why.
