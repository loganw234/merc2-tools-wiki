---
title: Guerilla Contracts & Jobs
parent: VZ Modules
nav_order: 3
has_children: true
has_toc: false
---

# Guerilla Contracts & Jobs

The Guerilla faction's story contracts (`gurcon*.lua`) and side jobs (`gurjob*.lua`) — 11 files total,
each a native `MrxTaskContract`/`MrxTaskContractOutpost`/`MrxTaskJob*` subclass rather than a
[Contract Framework](../contract-framework/) contract. See [VZ Modules](../vz/) for what that distinction
means and why it matters for modding.

## Modules in this category

- **[GurCon001](gurcon001)** — A Guerilla story contract centered on an assault against a VZ-held island fortress complex.
- **[GurCon002](gurcon002)** — A Guerilla story contract set around a town plaza in Merida.
- **[GurCon003](gurcon003)** — A Guerilla minor/side story contract (its VO keys all read `MinorContract-Gur03`) — deliver a "Piranha" speedboat down a river course while being chased by a scaling Oil-Company-flagged pursuit, with a contextual tutorial for the boat's boost button on the player's first run.
- **[GurCon005](gurcon005)** — A short Guerilla minor contract: assassinate four named Universal Petroleum targets scattered around a single location.
- **[GurCon050](gurcon050)** — A Guerilla outpost-capture contract.
- **[GurCon052](gurcon052)** — A Guerilla outpost-capture contract, config-only like [GurCon050](gurcon050).
- **[GurCon053](gurcon053)** — A Guerilla outpost-capture contract (internally `GurJob008_02`), notable for being one of only two outpost files in this batch with a custom `Activated` override on top of the config.
- **[GurJob001](gurjob001)** — A tiny Guerilla side job: destroy every object labeled `"Billboard"` (VZ propaganda billboards, going by the label), restricted to the hero characters.
- **[GurJob002](gurjob002)** — A Guerilla "verify a set of targets" side job spanning two differently-numbered location series — `GurJob002_01`–`05` and `GurJob012_01`–`05`, ten targets total under one job.
- **[GurJob006](gurjob006)** — An 8-line Guerilla side job: destroy every object labeled `"OC"` (Oil Company), hero-only.
- **[GurJob020](gurjob020)** — The largest Guerilla side job in this batch: a destroy-set covering 13 buildings across two location series (`GurJob007_Target01`–`03` and `GurJob011a`–`j`_Target), with `DangerousBuilding`-tuned AI spawners armed on each one and a VO table that scales its line selection by how many targets remain, not just a flat weight.
