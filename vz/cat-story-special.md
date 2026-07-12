---
title: Story & Special Contracts
parent: VZ Modules
nav_order: 7
has_children: true
has_toc: false
---

# Story & Special Contracts

The handful of `vz/` files that don't fit a single-faction bucket: `jetcon001.lua` and `meccon001.lua`
(the recruitable Jet-pilot and Mechanic specialist storylines, plus `mecjob.lua`'s own locally-defined
job-template base class and its 3 subclasses), `vzacon001.lua` (the game's actual opening mission), and
`stagingact1.lua` (shared world-dressing/patrol setup, imported once by [`xQ!L`](../vz/xql)).

## Modules in this category

- **[JetCon001](jetcon001)** — `JetCon001` is the recruitment mission for the Jet-pilot specialist.
- **[MecCon001](meccon001)** — `MecCon001` is the recruitment mission for the Mechanic specialist: a monster-truck race against the clock (with an AI motorcycle opponent in co-op), delivering the truck back to the mechanic's garage at the end.
- **[MecJob](mecjob)** — `MecJob` is a **local base class defined in this corpus, not a native engine class** — it's `mecjob.lua`'s own shared template for "deliver a specific damaged vehicle to the mechanic's garage" side jobs, built on top of the native [`MrxTaskJob`](../resident/mrxtaskjob).
- **[MecJob001](mecjob001)** — `MecJob001` is the first of 3 thin [`MecJob`](mecjob) subclasses — a side job asking the player to deliver a damaged vehicle labeled `"rtr"` (displayed as reference image `global_polaroid_belmont`) to the mechanic's garage.
- **[MecJob002](mecjob002)** — `MecJob002` is the second of 3 thin [`MecJob`](mecjob) subclasses — delivers a damaged vehicle labeled `"m35"` (displayed as reference image `global_polaroid_cortez`) to the mechanic's garage.
- **[MecJob003](mecjob003)** — `MecJob003` is the third of 3 thin [`MecJob`](mecjob) subclasses — delivers a damaged vehicle labeled `"amx30"` (displayed as reference image `global_polaroid_calderone`) to the mechanic's garage.
- **[StagingAct1](stagingact1)** — `StagingAct1` is a stateless world-dressing module: a small library of AI patrol-setup functions for the Guerilla base (gate, trailer, road, earthmover, mover-arm, squad, and front patrols).
- **[VzaCon001](vzacon001)** — `VzaCon001` is the game's opening mission.
