---
title: Oil Company Contracts & Jobs
parent: VZ Modules
nav_order: 4
has_children: true
has_toc: false
---

# Oil Company Contracts & Jobs

Universal Petroleum/Oil Company's story contracts (`oilcon*.lua`) and side jobs (`oiljob*.lua`) — 12
files total, the largest faction category and home to the biggest "normal" story contract in the corpus
(`oilcon001.lua`, 2241 lines / 108 functions). Each is a native
`MrxTaskContract`/`MrxTaskContractOutpost`/`MrxTaskJob*` subclass rather than a
[Contract Framework](../contract-framework/) contract. See [VZ Modules](../vz/) for what that distinction
means and why it matters for modding.

## Modules in this category

- **[OilCon001](oilcon001)** — The largest "normal" story contract in the entire corpus (2241 lines, roughly 108 functions) — an extended warehouse heist and rescue for Universal Petroleum.
- **[OilCon002](oilcon002)** — An Oil Company story contract built around the support-call character Ewan (registers `WifBios` dossier entry `"BioEwan"` on activation).
- **[OilCon003](oilcon003)** — An Oil Company minor/side story contract (VO keys read `MinorContract-Oil03`): talk to an OC VIP, then deliver him by vehicle to a drop point within a shrinking time limit, chased by a `MrxFactionManager` custom pursuit that escalates with `GetNumCompletions()`.
- **[OilCon005](oilcon005)** — A straightforward Oil Company minor contract: a sports-car race.
- **[OilCon020](oilcon020)** — An Oil Company story contract: gun-running.
- **[OilCon021](oilcon021)** — An Oil Company story contract to recover a named heavy vehicle nicknamed "the Devastator" (a truck object internally called `MailTruck`).
- **[OilCon050](oilcon050)** — An Oil Company outpost-capture contract (internally `OilJob001`) with a custom `Activated` override that cross-references [GurCon053](gurcon053) via `WifMissionFlow` — the two files describe the same physical outpost from the two factions' contract numbering, and whichever activates first gets the "first discovery" VO while the other is skipped.
- **[OilCon051](oilcon051)** — An Oil Company outpost-capture contract, config-only (internally `OilJob002`) — no custom `Activated` override, unlike its sibling [OilCon050](oilcon050).
- **[OilCon052](oilcon052)** — An Oil Company outpost-capture contract, config-only (internally `OilJob005`) — the third of this batch's three near-identical Oil Company outposts, differing from [OilCon051](oilcon051) only in which building/ capture point it names.
- **[OilJob004](oiljob004)** — A 9-line Oil Company side job: destroy every object labeled `"Guerilla"`, hero-only.
- **[OilJob008](oiljob008)** — An Oil Company destroy-set side job spanning 11 targets across several differently-prefixed location series.
- **[OilJob011](oiljob011)** — An Oil Company "verify a set of targets" side job spanning two location series — `OilJob011_Target_01`–`05` and `OilJob012_Target_01`–`05`, ten targets total under one job.
