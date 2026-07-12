---
title: Pirate Contracts & Jobs
parent: VZ Modules
nav_order: 5
has_children: true
has_toc: false
---

# Pirate Contracts & Jobs

The Pirate faction's story contracts (`pircon*.lua`) and side jobs (`pirjob*.lua`) — 9 files total, each
a native `MrxTaskContract`/`MrxTaskContractOutpost`/`MrxTaskJob*` subclass rather than a
[Contract Framework](../contract-framework/) contract. See [VZ Modules](../vz/) for what that distinction
means and why it matters for modding.

## Modules in this category

- **[PirCon001](pircon001)** — PirCon001 is a jetski race contract for the Pirate faction: the player (and, in co-op, a second player) races a jetski through roughly 30 waypoint checkpoints while a couple of rival pirate speedboats are scripted to converge on and block the course near a trigger point partway through.
- **[PirCon002](pircon002)** — PirCon002 is a smuggling-delivery contract: the player drives a truck carrying 24 jugs of rum ("RumJug" props on the truck bed) to a drop-off point while pursued by custom Oil Company (OC) vehicles.
- **[PirCon003](pircon003)** — PirCon003 is a follow-up smuggling-delivery contract in the same mold as PirCon002, this time hauling a truckload of 42 "bird" crates (`BirdBox` props, cargo value 1900 each) past a custom `VZ` pursuit and a pair of "Cliffy" ambush vehicles that path in to block the route.
- **[PirCon004](pircon004)** — PirCon004 is a large, co-op-capable physics cargo-delivery contract: the player hijacks a truck ("PirCon004_OrganTruck") whose bed is loaded with dozens of separately-spawned organ-transplant containers, then drives it cross-country to a delivery point while a `VZ` pursuit triggers past a distance threshold, scripted explosions go off near landmark buildings/pipes along the route, and an ambush truck is spawned near a marked goal.
- **[PirCon051](pircon051)** — PirCon051 is an outpost-capture contract: the player must clear and hold a single capture point at a Pirate outpost building.
- **[PirCon052](pircon052)** — PirCon052 is a second outpost-capture contract, structurally identical to [PirCon051](pircon051) — a single capture point at a different Pirate outpost building.
- **[PirJob001](pirjob001)** — PirJob001 is a minimal "destroy this type of target" side job: it tells the base `MrxTaskJobDestroyType` class to track anything labeled `"VZ"`, restricts progress to the hero's own kills (not AI companions or vehicle passengers), and starts running.
- **[PirJob012](pirjob012)** — PirJob012 is a "verify" (capture/subdue/confirm) side job against a fixed set of 10 named targets scattered around the map, each with its own defense/pristine/staging layers and a "you're getting near this one" VO cue.
- **[PirJob020](pirjob020)** — PirJob020 is a "destroy this fixed set of targets" side job spanning 10 named objectives, each with its own pristine/defense/destroyed (and sometimes staging) layers.
