---
title: China Contracts & Jobs
parent: VZ Modules
nav_order: 2
has_children: true
has_toc: false
---

# China Contracts & Jobs

China's story contracts (`chicon*.lua`) and side jobs (`chijob*.lua`) — 11 files total, each a native
`MrxTaskContract`/`MrxTaskContractOutpost`/`MrxTaskJob*` subclass rather than a
[Contract Framework](../contract-framework/) contract. See [VZ Modules](../vz/) for what that distinction
means and why it matters for modding.

## Modules in this category

- **[ChiCon001](chicon001)** — A China story contract: rescue a captured VIP ("PartyOfficial") from a hotel, subdue and release the prisoner, then escort them on foot to a dropoff point.
- **[ChiCon002](chicon002)** — A China story contract: a three-pronged siege of an Oil Company base near Maracaibo.
- **[ChiCon003](chicon003)** — A China story contract set in Caracas, structurally a mirror image of Allied Nation's [AllCon003](allcon003): verify (kill) a China-side high-value target (`ChiCon003_HVT`) and destroy five marked buildings, in any order, needing both done to complete.
- **[ChiCon008](chicon008)** — A China minor/side contract: spawn a locked "ZTZ98" tank and race it through roughly 20 checkpoints, optionally destroying 19 roadside barrels along the way for bonus time.
- **[ChiCon009](chicon009)** — A China minor/side contract: acquire a locked "ZBD2000" APC, rendezvous with the player's current position, then escort a spawned civilian ambulance (shown with a health bar) along a preset path to a dropoff — all under an overall countdown timer that fails the contract if it expires.
- **[ChiCon050](chicon050)** — A China outpost-capture side contract wrapping the `ChiJob001_01` outpost location.
- **[ChiCon051](chicon051)** — A China outpost-capture side contract wrapping the `ChiJob001_02` outpost location.
- **[ChiCon053](chicon053)** — A China outpost-capture side contract wrapping the `ChiJob001_04` outpost location.
- **[ChiJob002](chijob002)** — A China "verify" side job spanning ten targets across two location clusters — five `ChiJob002_Target_0X` sites and five `ChiJob010_Target_0X` sites — each with its own defense/pristine/ staging layer set and (for most targets) a proximity VO line.
- **[ChiJob003](chijob003)** — A minimal China side job: a generic bounty to destroy every object carrying the `"Allied"` label, restricted to hero characters.
- **[ChiJob020](chijob020)** — A China "destroy set" side job over eight pre-existing targets — seven `ChiJob005_A` through `_G` building targets plus one `ChiJob009_A` target (an oilrig demo object) — none of them `ChiJob020_`-named.
