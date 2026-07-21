---
title: What this game is (curated)
---

<!--
MAINTAINER NOTE — not sent to the model in this form; the builder strips this comment.

Lines tagged [VERIFY] are the ones written from general knowledge of the game rather
than from a wiki page. Everything else is sourced, with the page named inline.
Correct or delete the [VERIFY] lines, then remove the tag — an unverified claim in
this section is worse than a missing one, because the rest of the pack is trusted.
-->

Everything else in this pack is API reference. This section is what the words in it
*mean*. Use it to work out what a user is actually asking for, then answer from the
API sections.

## The game

*Mercenaries 2: World in Flames* (PC, Pandemic Studios). An open-world third-person
action game set in **Venezuela**, where the player is a mercenary who builds a
private military company and takes paid contracts from several mutually hostile
factions. The campaign is a revenge plot against **Solano**, the dictator who
double-crosses the player in the opening act.

The player is one of three selectable mercenaries — **Chris Jacobs**, **Jennifer
Mui**, or **Mattias Nilsson** (`vz/wifbios.md` lists `BioChris` / `BioJennifer` /
`BioMattias` among its 22 named dossier entries). Missions and jobs are taken as
**contracts** from faction handlers, run in the open world, and paid in cash.

The PMC's four support staff each unlock a mechanic, which is why they have
dedicated modules: **Fiona Taylor** (handler — briefings, the contract board),
**Ewan Devlin** (transport helicopter, winch extraction of fuel/cash crates),
**Eva Navarro** (garage/motor pool, `wifpmcgarage.lua`, plus the grappling hook),
and **Misha Milanich** (fixed-wing airstrikes).

Two players can play the whole game **co-op** — a first-class concern in this
codebase, not an afterthought. Much of the scripting complexity in `resident/` and
`vz/` exists to keep host and client in sync.

## PMC — read this before answering anything about factions

**PMC is the player's own outfit.** `vz/cat-pmc.md` calls `pmccon*.lua` "the
player's own PMC storyline contracts", and `vz/pmccon001.md` describes Solano's men
raiding "the player's own PMC headquarters villa".

So PMC means *you and your organisation*: the player character, the HQ villa with its
garage and interior, the economy, your equipment. It is **not** a troop faction with
rank-and-file soldiers you can spawn. Every `pmc`-prefixed entry in the template list
is a building or a prop (`_pmcoutpost_bld_hq`, `_pmcoutpost_beerA`). There is no
`"PMC Soldier"` template and asking for one is a category error — say so, and steer
to a faction that does have troop templates.

## The other factions

Six factions besides PMC. **The code name and the in-fiction name differ**, which is
the single most useful thing on this page when reading someone's question — a user
saying "the guerrillas" and the codebase saying `gur*` are the same faction:

| Code / prefix | In-fiction faction | Role |
|---|---|---|
| `VZ` | **Venezuelan Army** | Solano's regime. Permanently hostile; the campaign's main enemy |
| `gur`, "Guerilla" | **PLAV** (People's Liberation Army of Venezuela) | Left-wing insurgency against Solano, led by Marcela Acosta |
| `oil`, "Oil Company" | **Universal Petroleum (UP)** | Western oil corporation under Dr. Lorraine Rubin; largest contract category |
| `all`, "Allied" | **Allied Nations (AN)** | US-backed force under CIA agent Phillip Joyce; arrives late-game |
| `chi`, "China" | **PLA** | Chinese force under General Zhou Peng; arrives late-game |
| `pir`, "Pirate" | **The Pirates** (Balseros Crew) | Coastal smugglers and black-market arms |

`VZ` is permanently hostile. The other five have a **reputation** standing that rises
with completed contracts and falls when you kill their people or wreck their
property — which is what `Ai.SetRelation` / `Ai.SetFeeling` / `Ess.Relations`
manipulate at runtime.

**Solano** is the antagonist: his men raid the player's HQ (`vz/pmccon001.md`) and
later contracts assault his bunkers (`vz/pmccon003.md`, `pmccon004.md`).

**Solano** is the antagonist of the PMC storyline: his men raid the player's HQ
(`vz/pmccon001.md`), and later contracts cover assaulting his bunkers
(`vz/pmccon003.md`, `pmccon004.md`).

Factions are engine-side. There is no documented Lua call that creates a new one.
What *is* adjustable at runtime is the relationship between existing factions and
individual units' feelings toward each other — `Ai.SetRelation`, `Ai.SetFeeling`, and
the `Ess.Relations` wrapper. When a user asks for a "custom faction", that is almost
always what they actually want.

## The core loop and its vocabulary

These words appear hundreds of times across the API sections. What they refer to:

- **Contract / job** — a mission. Story contracts (`*con*.lua`) and side jobs
  (`*job*.lua`) per faction, dispensed from briefing screens at the HQ
  (`deep-dives/custom-contract.md` shows a briefing board listing "Universal
  Petroleum" and "Emplaced Weapons Challenge" entries).
- **HQ** — the player's base. Includes the villa, a **garage** (`wifpmcgarage.lua`)
  and an **interior** (`wifpmcinterior.lua`), with named gate and door objects that
  missions open and close.
- **Outpost** — a capturable/usable installation. Outposts recur constantly in the
  scripting layer and have their own transit/landing-zone machinery.
- **Support** — called-in assistance bought with cash/fuel: deliveries, vehicle
  drops, and **airstrikes**. `Ess.Support` wraps this; `namespaces/airstrike.md` is
  the engine surface.
- **Fuel** — a second currency alongside cash, spent on support call-ins.
  `MrxPmc.AddFuelQty` / `AddCashQty` are the HUD-updating economy calls.
- **PDA / briefing** — the in-game menu surface for contracts, dossiers and the map.
- **Hijacking** — commandeering an occupied vehicle, a signature mechanic with its
  own resident module (`mrxactionhijack.lua`).

## Mapping intent to mechanics

Common asks and where they actually land:

| The user wants | What they actually need |
|---|---|
| "NPCs under my command" | Spawn units from a faction with troop templates, then `Ess.AIOrders.command` for behaviour and `Ai.SetFeeling`/`Ess.Relations` to stop them being hostile |
| "a custom faction" | Relations/attitude manipulation between existing factions — you cannot create one |
| "PMC soldiers" | Does not exist; see above |
| "my own mission" | The Contract Framework / `Ess.Contract`, not the native `MrxTask*` classes the shipped `vz/` contracts use |
| "call in an airstrike" | The support system — `Ess.Support`, `namespaces/airstrike.md` |
| "give myself money" | `MrxPmc.AddCashQty` (HUD-updating), not `Player.SetCash` |
