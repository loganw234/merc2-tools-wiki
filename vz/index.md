---
title: VZ Modules
nav_order: 8
has_children: true
has_toc: false
---

# VZ Modules

Reference pages for `src/vz/` — mission and contract scripts: per-faction story/side contracts and jobs,
in-game contextual tutorials, and the core mission-flow/save-data modules that tie a level together.
Distinct from [Resident Modules](../resident/) (the engine's reusable library/world-object code) and
[Shell Modules](../shell/) (the front-end menu system).

> **Status: new, first pass from static source reading only.** Every page here reflects what the
> decompiled Lua actually says, not confirmed by playing the game yet — treat function/behavior claims as
> a starting point, not a guarantee, until a page's own wording says otherwise.

There are 114 of these, split into categories:

- **[Allied Nation Contracts & Jobs](cat-allied)**
- **[China Contracts & Jobs](cat-china)**
- **[Guerilla Contracts & Jobs](cat-guerilla)**
- **[Oil Company Contracts & Jobs](cat-oil-company)**
- **[Pirate Contracts & Jobs](cat-pirate)**
- **[PMC Contracts & Jobs](cat-pmc)**
- **[Story & Special Contracts](cat-story-special)** — the two recruitable-specialist storylines (Jet the
  pilot, Mec the mechanic), the opening VZ mission, and shared world-dressing.
- **[VZ Tutorials](cat-tutorials)** — one page per contextual in-game tutorial trigger.
- **[World & Mission Flow](cat-world-mission-flow)** — save/load, briefing data, HQ/garage state, and the
  boot-time session conductor that ties everything else together.

## A different module shape than Resident Modules

Nothing here uses [Resident Modules](../resident/)' `Inheritable`/per-`uGuid` object pattern. Instead,
nearly every contract/job/tutorial file `inherit()`s from a **native task-framework base class** —
[`MrxTaskContract`](../resident/mrxtaskcontract), [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost),
one of the `MrxTaskJob*` family, or [`MrxTutorial`](../resident/mrxtutorial). Unlike most of the engine's
other native globals (`Object`/`Event`/`Player` and friends, which have no decompiled source at all),
these particular base classes *do* have their own `resident/` module and wiki page — each `vz/` page's
Inheritance section links straight to its actual parent's documentation. Lifecycle methods are
`self`-based overrides with an explicit "super" call to the parent, not `OnActivate`/`Awake`/`Create`
keyed by `uGuid`:

```lua
inherit("MrxTaskJobDestroyType")
import("MrxVoSequence")

function Activated(self)
  MrxTaskJobDestroyType.Activated(self)   -- explicit "super" call
  self:_SetLabelFilter("VZ")
  self:_SetHeroOnly(true)
  self:_Go()
end
```

**This is also the *old*, native contract/mission system.** Confirmed by grep across the whole
directory: zero files here call `Contract.Register` or reference `_G.Contract`. It's exactly the
`WifMissionData`/`MrxTask` system
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) describes as corrupting
saves if a mod hooks into it directly — which is why [`ContractFramework.lua`](../contract-framework/) was
built as an ephemeral, save-safe alternative instead. Reading these pages is useful for understanding how
the shipped game's own missions work, but **don't build a mod contract this way** — use
[Contract Framework](../contract-framework/) instead.

A handful of files (the `wif*` data/utility modules, `stagingact1.lua`, `xQ!L.lua`) have no `inherit()` at
all and are stateless utilities or singleton-state managers instead — each page's own "Instance pattern"
section says which kind it is.
