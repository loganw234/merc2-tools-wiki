---
title: PMC Contracts & Jobs
parent: VZ Modules
nav_order: 6
has_children: true
has_toc: false
---

# PMC Contracts & Jobs

The player's own PMC storyline contracts (`pmccon*.lua`) and side jobs (`pmcjob*.lua`) — 13 files total,
the largest single-faction category. Each is a native
`MrxTaskContract`/`MrxTaskContractOutpost`/`MrxTaskJob*` subclass rather than a
[Contract Framework](../contract-framework/) contract. See [VZ Modules](../vz/) for what that distinction
means and why it matters for modding.

## Modules in this category

- **[PmcCon001](pmccon001)** — PmcCon001 is the story contract where Solano's men raid the player's own PMC headquarters villa.
- **[PmcCon002](pmccon002)** — PmcCon002 sends the player to an oil rig to find an informant, "Blanco," hiding in the rig office.
- **[PmcCon003](pmccon003)** — PmcCon003 is a large, multi-phase story contract covering the assault on Solano's bunker and the immediate PMC counter-attack that follows: fly out by taxi helicopter, deploy a Bunker Buster strike on the bunker, race back to base against a helicopter-wave pursuit, defend the PMC compound from an armored assault (with an optional second tank wave), then track down and extract the target "Carmona" as he flees by jeep and helicopter.
- **[PmcCon004](pmccon004)** — PmcCon004 is the story contract covering the destruction of Solano's second bunker and the hijack of his escape helicopter.
- **[PmcCon013](pmccon013)** — PmcCon013 is a helicopter-winch skill challenge: board one of two named copters, then hover a winched object steadily at a target altitude (which rises with each replay, capped at 7 units above a fixed baseline) within a small radius for several seconds straight, all inside a 5-minute time limit.
- **[PmcCon015](pmccon015)** — PmcCon015 is a short "Phoenix" street-race contract: spawn a race car (or two, one per player, in co-op) and run a course of roughly 17 checkpoints against a shrinking timer that tightens with each replay (45s down to 25s).
- **[PmcCon016](pmccon016)** — PmcCon016 is a race contract (a Panhard in solo, a Buggy in co-op) around a longer course of roughly 27 checkpoints, with a secondary parallel objective to shoot down 6 destructible pylons along the way for bonus time.
- **[PmcCon018](pmccon018)** — PmcCon018 ("Burnout") is a fixed-position shooting-gallery minigame: both players' real weapons are stripped and stashed on the ground, aim mode is disabled, and each is given a "Practice Laser" freebie weapon instead.
- **[PmcCon031](pmccon031)** — PmcCon031 is a multi-stage shooting-gallery contract at the PMC compound: move to a firing point, destroy a set of decorative statues (first with an emplaced machine gun, then a recoilless rifle, then a grenade launcher), then finish with a car-launch gauntlet where vehicles fling in from fixed points and must be destroyed within a 9-second window each (up to 4 misses trigger negative hero VO).
- **[PmcCon032](pmccon032)** — PmcCon032 is an "easy" shooting-gallery course: armed with an infinite-ammo Grenade Launcher, the player moves through 5 firing points, destroying 3 targets at each of the first three, 21 sniper statues at the fourth, and 6 more at the fifth, all against a displayed time-to-beat (2:30/1:20/1:00 depending on replay count).
- **[PmcCon033](pmccon033)** — PmcCon033 is a "pop-up target" shooting-gallery course: armed with an infinite-ammo silver Pistol, the player clears four fixed firing points (3 targets each, framed in-HUD as "Portaits" — a typo preserved from the source), then a final wave of four painting-style targets that physically pop up by opening like a hinged door (`Vehicle.OpenDoor`/`CloseDoor` reused as a pop-up mechanism) before being destroyed.
- **[PmcCon034](pmccon034)** — PmcCon034 is a shooting-gallery course armed with an infinite-ammo Anti-Material Rifle: destroy 19 named sniper statues while two independent bonus side-targets keep appearing — a truck-and-statue pair that drives along a path every 43 seconds, and a bust statue winched beneath a helicopter — each granting a 5-second timer-pause bonus if destroyed before it's cleared away.
- **[PmcJob001](pmcjob001)** — PmcJob001 is a "collect this type of item" side job: gather 100 `"SpareParts"`-labeled pickups scattered around the map.
