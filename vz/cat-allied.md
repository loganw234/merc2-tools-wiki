---
title: Allied Nation Contracts & Jobs
parent: VZ Modules
nav_order: 1
has_children: true
has_toc: false
---

# Allied Nation Contracts & Jobs

The Allied Nation faction's story contracts (`allcon*.lua`) and side jobs (`alljob*.lua`) — 10 files
total, each a native `MrxTaskContract`/`MrxTaskContractOutpost`/`MrxTaskJob*` subclass rather than a
[Contract Framework](../contract-framework/) contract. See [VZ Modules](../vz/) for what that distinction
means and why it matters for modding.

## Modules in this category

- **[AllCon001](allcon001)** — An Allied Nation story contract built around a downed plane and two captured VIPs.
- **[AllCon002](allcon002)** — A large Allied Nation story contract: the siege of Caracas's China-held MLRS/AA position.
- **[AllCon003](allcon003)** — An Allied Nation story contract set during a China invasion of Caracas: the player verifies (kills) a high-value target (`AllCon003_HVT`) and destroys four marked buildings, in any order, needing both done to complete.
- **[AllCon008](allcon008)** — An Allied Nation minor/side contract: a "Coanda Transport" helicopter race through roughly 35 checkpoints.
- **[AllCon050](allcon050)** — An Allied Nation outpost-capture side contract wrapping the `AllJob001_01` outpost location.
- **[AllCon052](allcon052)** — An Allied Nation outpost-capture side contract wrapping the `AllJob001_03` outpost location.
- **[AllCon053](allcon053)** — An Allied Nation outpost-capture side contract wrapping the `AllJob001_04` outpost location.
- **[AllJob002](alljob002)** — An Allied Nation "verify" side job spanning ten targets across two location clusters — five `AllJob002_0X_Target` sites and five `AllJob010_0X_Target` sites — each with its own defense/staging/ pristine/verified layer set and (for most targets) a proximity VO line.
- **[AllJob003](alljob003)** — A minimal Allied Nation side job: a generic bounty to destroy every object carrying the `"China"` label, restricted to hero characters.
- **[AllJob020](alljob020)** — An Allied Nation "destroy set" side job over 19 pre-existing targets — but every single target name it registers is prefixed `AllJob005_`, `AllJob009_`, or `ChiJob006_`, not `AllJob020_`.
