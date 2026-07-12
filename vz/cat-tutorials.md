---
title: VZ Tutorials
parent: VZ Modules
nav_order: 8
has_children: true
has_toc: false
---

# VZ Tutorials

One page per contextual in-game tutorial trigger (`wiftutorial*.lua`) — 22 files total, e.g.
`wiftutorialboat.lua`, `wiftutorialc4.lua`, `wiftutorialhelicopter.lua`. Every file here inherits from the
native `MrxTutorial` engine class and follows the same small, uniform skeleton: activation/cancellation
criteria plus the message shown, occasionally a completion criterion. The most batchable, uniform
category in `src/vz/`.

## Modules in this category

- **[WifTutorialAirstrikeInterrupt](wiftutorialairstrikeinterrupt)** — Teaches the player that taking damage while calling in a satellite/airstrike targeting sequence interrupts it.
- **[WifTutorialAlarm](wiftutorialalarm)** — Shown when the player sets off a physical alarm object in the world.
- **[WifTutorialAlliesHonk](wiftutorialallieshonk)** — Teaches the player to honk their vehicle horn to attract allied NPCs.
- **[WifTutorialAPC](wiftutorialapc)** — Shown the first time the player mounts the driver seat of an APC.
- **[WifTutorialBoat](wiftutorialboat)** — Shown the first time the player mounts the driver seat of a boat.
- **[WifTutorialC4](wiftutorialc4)** — Teaches basic C4 usage.
- **[WifTutorialC4Switch](wiftutorialc4switch)** — A narrower, separate C4 tutorial about the detonator switch itself.
- **[WifTutorialCollateralDamage](wiftutorialcollateraldamage)** — Shown when the player deals collateral damage to a civilian or neutral.
- **[WifTutorialCollectibles](wiftutorialcollectibles)** — The most stateful tutorial in this category.
- **[WifTutorialCoopRevive](wiftutorialcooprevive)** — Presumably shown around reviving a downed co-op partner, per its message key and the manager catalog entry — per static source reading, this file only defines the message and a fixed completion timer; the actual trigger isn't in this file.
- **[WifTutorialCoopTether](wiftutorialcooptether)** — Presumably shown around the co-op "tether" mechanic that keeps two players from straying too far apart, per its message key and the manager catalog entry — per static source reading, this file only defines the message and a fixed completion timer; the actual trigger isn't in this file.
- **[WifTutorialGateHonk](wiftutorialgatehonk)** — Shown near one specific, hardcoded gate object while the player is using a vehicle disguise — presumably teaching that a disguised vehicle should honk to be let through a faction checkpoint.
- **[WifTutorialHelicopter](wiftutorialhelicopter)** — Shown the first time the player mounts the driver seat of a helicopter.
- **[WifTutorialHeliRepairPad](wiftutorialhelirepairpad)** — Presumably shown around landing on/using a helicopter repair pad, per its message key (`"[Tutorial.LandingZoneHealth]"`).
- **[WifTutorialLowFuel](wiftutoriallowfuel)** — Shown when the player's fuel drops to 10% of capacity or below.
- **[WifTutorialNoFuel](wiftutorialnofuel)** — Shown when the player runs out of fuel entirely.
- **[WifTutorialSwimming](wiftutorialswimming)** — Shown when the player's character enters a swimming state.
- **[WifTutorialTank](wiftutorialtank)** — Shown the first time the player mounts the driver seat of a tank (specifically excluding APCs).
- **[WifTutorialTankHijack](wiftutorialtankhijack)** — Shown near an enemy tank crewed by two or more gunners, teaching the tank-hijack mechanic.
- **[WifTutorialTrespass](wiftutorialtrespass)** — Shown when the player trespasses into hostile/restricted territory.
- **[WifTutorialVehicleDisguise](wiftutorialvehicledisguise)** — The other heavily stateful tutorial in this category, alongside [`WifTutorialCollectibles`](wiftutorialcollectibles).
- **[WifTutorialWheeledVehicleBasic](wiftutorialwheeledvehiclebasic)** — Shown the first time the player mounts the driver seat of a car.
