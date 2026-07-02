---
title: Controller
parent: Engine Namespaces
nav_order: 13
---

# Controller

## Overview

`Controller` is an **engine namespace**: implemented natively by the game engine, not by any
decompiled `.lua` file in `resident/` or elsewhere. It's always available as a global table — no
`import()` required.

Unlike `Object` or `Event`, `Controller` contains **no functions at all**. `pairs(Controller)`
shows exactly 25 entries, all plain integer constants identifying gamepad buttons and stick/pad
directions (e.g. `L1`, `RPad_Down`, `LStick_Left`, `Use_Melee`). There is nothing to call — the
table exists purely so scripts can refer to a specific controller input by name instead of a raw
numeric ID.

The presumed purpose, consistent with where it's actually used (see Provenance below), is
identifying a controller button/direction for minigame prompts and similar input-facing logic
(e.g. telling the HUD which button icon to display, or checking which button a player pressed
during a quick-time-style sequence).

## Provenance

- The full list of 25 numeric IDs comes from a live `pairs(Controller)` enumeration in-game
  (ground truth for *what exists*). This table needed no further research — the constants and
  their values are complete and authoritative as given.
- Because every entry is a constant (not a function), there is no "argument shape" question to
  investigate the way there is for `Object` or `Event`. The only open question is *usage*: which
  of these 25 constants are actually referenced somewhere in the ~230 decompiled `.lua` files.
- A grep across the full decompiled source tree found real usage in exactly one file:
  `resident/mrxactionhijack.lua`, in the vehicle-hijack minigame logic. No other file references
  `Controller.*` anywhere in the corpus.

### Confirmed usage found

In `resident/mrxactionhijack.lua`:

- `Controller.RPad_Down` is used as both the `GRAPHIC` and `INPUT` value in a ragdoll/knockdown
  table (`tRagdoll`, line 46-47) — presumably telling the HUD which button icon to show and which
  physical input satisfies the prompt.
- In the hijack "alternate" minigame branch (lines 587-610), `self[...].miniGame.button` is
  compared against `Controller.Use_Melee` and `Controller.Use_Reload` to decide which pair of
  `Controller.*` constants (`RPad_Up`/`RPad_Right`, `RPad_Up`/`RPad_Left`, or
  `LStick_Left`/`LStick_Right`) gets passed as the button-pair argument to
  `Event.Create(Event.Minigame, {...})`. This confirms `Controller.*` constants are passed through
  as data into the `Event.Minigame` event type's argument table (see
  [`Event`](event#human--animation-events), where `Minigame` is listed as name-only/unconfirmed —
  this call site is itself the only evidence found for that event's argument shape too, though
  documenting `Event.Minigame` in full is out of scope here).

No other constant in the list of 25 was found referenced anywhere in the decompiled corpus.

## Reference table

| Constant | Value | Notes |
|---|---|---|
| `LPad_Up` | 1 | No confirmed call site. |
| `LPad_Down` | 2 | No confirmed call site. |
| `LPad_Left` | 3 | No confirmed call site. |
| `LPad_Right` | 4 | No confirmed call site. |
| `RPad_Up` | 5 | **Confirmed.** Used in `resident/mrxactionhijack.lua:592,600` as part of the button-pair passed to the hijack minigame. |
| `RPad_Down` | 6 | **Confirmed.** Used in `resident/mrxactionhijack.lua:46-47` (`tRagdoll.GRAPHIC` / `tRagdoll.INPUT`). |
| `RPad_Left` | 7 | **Confirmed.** Used in `resident/mrxactionhijack.lua:601` (paired with `RPad_Up` for the `Use_Reload` case). |
| `RPad_Right` | 8 | **Confirmed.** Used in `resident/mrxactionhijack.lua:593` (paired with `RPad_Up` for the `Use_Melee` case). |
| `LStick_Left` | 9 | **Confirmed.** Used in `resident/mrxactionhijack.lua:608` (default/else branch of the hijack minigame). |
| `LStick_Right` | 10 | **Confirmed.** Used in `resident/mrxactionhijack.lua:609` (paired with `LStick_Left`). |
| `LStick_Up` | 11 | No confirmed call site. |
| `LStick_Down` | 12 | No confirmed call site. |
| `RStick_Left` | 13 | No confirmed call site. |
| `RStick_Right` | 14 | No confirmed call site. |
| `RStick_Up` | 15 | No confirmed call site. |
| `RStick_Down` | 16 | No confirmed call site. |
| `L1` | 17 | No confirmed call site. |
| `L2` | 18 | No confirmed call site. |
| `L3` | 19 | No confirmed call site. |
| `R1` | 20 | No confirmed call site. |
| `R2` | 21 | No confirmed call site. |
| `R3` | 22 | No confirmed call site. |
| `Use_Melee` | 26 | **Confirmed.** Used in `resident/mrxactionhijack.lua:587` as a comparison value for `miniGame.button` to select the melee button-pair. |
| `Use_Reload` | 27 | **Confirmed.** Used in `resident/mrxactionhijack.lua:595` as a comparison value for `miniGame.button` to select the reload button-pair. |
| `LStick_LeftRight` | 25 | No confirmed call site. Presumably a combined/axis identifier distinct from the separate `LStick_Left`/`LStick_Right` constants, but this is not confirmed from source. |

Note the numbering isn't fully contiguous in the sense of "23/24 exist but weren't in the
enumeration" — the live dump lists exactly the 25 names/values shown here (23 and 24 are simply
not present as names in the table; there is no gap to explain, this is the complete set).

## Notes for modders

- As with [`Event`](event) (see its Notes for modders section), always reference these by name —
  `Controller.L1`, not the literal `17` — even though only a handful of names have confirmed real
  usage in the decompiled corpus. The values are stable within a given game build, but names
  self-document and survive if the underlying numbering ever changes.
- Only 8 of the 25 constants (`RPad_Up`, `RPad_Down`, `RPad_Left`, `RPad_Right`, `LStick_Left`,
  `LStick_Right`, `Use_Melee`, `Use_Reload`) were found actually referenced in the decompiled
  source, all within a single file (`resident/mrxactionhijack.lua`) implementing a vehicle-hijack
  minigame. The remaining 17 constants are confirmed to exist (via live enumeration) but have no
  known call site — treat their exact usage context (e.g. whether they're consumed by native
  input-remapping UI, or by Lua code outside this corpus) as unconfirmed.
- Given the very narrow observed usage, this namespace is likely consumed mostly by native
  engine/GUI code (e.g. control-scheme display, button-prompt icons) rather than by gameplay Lua
  scripts in general — `mrxactionhijack.lua`'s minigame is the one place gameplay Lua needed to
  name a specific physical button.
