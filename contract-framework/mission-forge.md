---
title: MissionForge
parent: Contract Framework
nav_order: 5
---

# MissionForge

> **Status: new, in development.** Read directly from `MissionForge.lua` (read in full). For the design
> story — why it departs from ForgeCam the way it does, and two concrete bugs found and fixed along the
> way — see the [MissionForge deep dive](../deep-dives/mission-forge).

MissionForge is an in-game, walk-around authoring tool: place units, objectives, support call-ins,
triggers, and AI orders directly in the world, then export a paste-ready dump for
[the web tool](web-tool) to turn into a finished `Contract.Register({...})`. It runs in the live, unpaused
world — there's no camera to fly, just your own character walking around.

## Controls

| Input | Action |
|---|---|
| **F7** | Toggle MissionForge on/off |
| Walk around | The drop point is always your character's feet (shown by a ring + floating marker) |
| **Up / Down** | Move the menu highlight |
| **Left / Right** | Back out of / open into a branch (a faction, OBJECTIVES, SUPPORT/TRIGGERS, AI ORDERS) |
| **P** or **Enter** | Place the current brush at your feet |
| **Backspace** | Undo the last placement (a whole squad at once, if the last thing placed was one) |
| **Delete** | Remove the placement nearest to you |
| **, / .** | Shrink / grow the current objective/zone radius (hold to keep changing it) |
| **T** | Cycle the active group tag (A, B, C, ...) |
| **End** | Export everything placed so far to `lua_loader_printf.log` |

There's deliberately no "clear everything" key — undo one at a time with Backspace instead, so a stray
keypress can't erase real progress.

## The catalog

Highlighting a leaf in the menu sets it as the active brush; pressing **P**/**Enter** drops it. The menu
is organized as:

- **One branch per faction** (Guerilla / Allied / China / OC / Pirate / VZ), each with Infantry / Vehicles /
  Helicopters / Boats (and Emplacements for Allied) sub-branches, plus a **SQUADS** branch — preset unit
  compositions (Fire Team, Rifle Squad, Armor Platoon, up to a 24-unit Battle Group) that drop as a whole
  grid formation in one placement, sharing one undo step.
- **PROPS / MISC** — cover objects and a couple of stray props.
- **OBJECTIVES** — one entry per [objective type](objectives) (Destroy, Reach, Defend, Collect, Escort,
  Hold, Interact, Verify, Extract, Race Checkpoint, Survive, Chase), plus **Player Spawn** for the
  teleport-on-accept point.
- **SUPPORT / TRIGGERS** — one entry per [support effect](support-effects-and-triggers) type
  (artillery, airstrike flyby, bombing run, heli wave, reinforcement, music cue, explosion/VFX, scripted
  damage, voice-over) plus a generic **Trigger Zone**.
- **AI ORDERS (per group)** — Move To, Patrol Point (drop several to build a route), Defend Area, Attack /
  Hunt, Hold Ground, Face Point — these command whichever group is currently active (cycle it with **T**
  first).
- **EXPORT PLACEMENTS** — dumps everything to the log (same as pressing **End**).

## Group tags

Units, objectives, support, triggers, and AI orders placed while the same group letter is active all share
that tag. This is what lets [the web tool](web-tool) auto-wire things on import — a trigger and a support
call-in placed under the same group arrive already connected, and an AI order placed under a group commands
whichever units share that same tag. Bump the group (**T**) when starting a new cluster; leave it alone to
keep adding to the current one.

## What gets placed vs. what gets recorded

Nothing MissionForge places is the real thing — every placement is an inert marker (a faction supply crate
for infantry, an empty vehicle for vehicles, the bare prop for props, or an invisible zone anchor for
objectives/support/triggers/orders). The **real** template name is recorded separately and is what actually
ends up in the export and the generated contract. See the
[deep dive](../deep-dives/mission-forge#the-bigger-departure-no-live-preview-at-all) for why.

## Exporting

Press **End** (or select EXPORT PLACEMENTS). A `MISSIONFORGE_EXPORT = { ... }` table prints to
`lua_loader_printf.log` — copy the whole block (from `MISSIONFORGE_EXPORT = {` to the matching closing
`}`) and paste it into [the web tool](web-tool)'s first step.

## Where to go next

- [The Web Tool](web-tool) — turn an export into a finished, deployable contract.
- [MissionForge deep dive](../deep-dives/mission-forge) — the full design story, including two real bugs
  found and fixed.
- [Objectives Reference](objectives) / [Support Effects & Triggers](support-effects-and-triggers) /
  [Units, AI Orders & Relations](units-ai-and-relations) — what each placed thing means once it reaches the
  actual framework.
