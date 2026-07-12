---
title: WifBriefingData
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 18
inherits: none
tags: [data, cinematic]
verified: false
---

# WifBriefingData

*Module: wifbriefingdata.lua*

## Overview
`wifbriefingdata.lua` is 16,445 lines long and almost none of it is logic — confirmed by grep, the entire
file contains exactly two functions (`GetIntroIdByIndex`, `GetIntroIndexById`) and no `import()`/`inherit()`
at all. Everything else is a flat table of authored pre-mission cinematic direction: one entry per
flagship story contract (camera keyframes, face-anim sets, VO cue names, Scaleform overlay files), plus a
shared set of faction/PMC-recruit intro cutscenes. It has no behavior of its own — [`mrxbriefing`](../resident/mrxbriefing)
reads it to actually drive the briefing screen.

## Schema

### Top-level keys
16 in total: `Intros`, plus 15 per-contract entries, each keyed by the exact mission-ID string
[`mrxbriefing`](../resident/mrxbriefing) looks it up with.

| Key(s) | Covers |
|---|---|
| `Intros` | 5 faction/PMC-recruit intro cutscenes: `Gur`, `Pir`, `AllChi`, `Mec`, `Jet` |
| `AllCon001`, `AllCon002`, `AllCon003` | Allied Nation flagship contracts |
| `ChiCon001`, `ChiCon002`, `ChiCon003` | China flagship contracts |
| `GurCon001`, `GurCon002` | Guerrilla flagship contracts |
| `OilCon001`, `OilCon002`, `OilCon021` | Oil Company flagship contracts (`OilCon021` is the minimal stub, see below) |
| `PmcCon002`, `PmcCon003` | PMC flagship contracts |
| `JetCon001` | Jet (the pilot) PMC-recruit contract |
| `MecCon001` | Mec (the mechanic) PMC-recruit contract |

Every other contract/job in `src/vz/` (roughly 100 of the ~114 total) has **no entry here at all**.

Three more bare globals sit above `Intros` in the file, not inside any table: `knContact = 1`,
`knSimple = 2`, `knRecruit = 3`. Only `knSimple` is ever actually used as a value in this file — 5 of the 15
contract entries (`ChiCon001`, `GurCon001`, `PmcCon002`, `PmcCon003`, `OilCon021`) set `nType = knSimple`;
the other 10 leave `nType` unset entirely. `knContact`/`knRecruit` are exported (`WifBriefingData.knContact`/
`.knRecruit`) but never assigned to anything within this file's own data.

### `Intros`
Each of the 5 entries holds `tHq` (one or more HQ blip names), `sTitle` (a localization key), and
`tSequence` — an ordered array mixing VO lines, one Scaleform overlay step, and bare-number pauses.
`Gur`, trimmed:

```lua
Gur = {
  tHq = { "GurOutpost1" },
  sTitle = "[Briefing.Intro.Gur]",
  tSequence = {
    { sSpeaker = "Starter", sCue = "Fiona.Guerrilla.Intro01" },
    { sFlashFile = "POI_GR_Introduction", nTime = 35 },
    0.1,  -- bare number: a pause between steps, not confirmed further than that
    { sSpeaker = "Starter", sCue = "Fiona.Guerrilla.Intro02" },
    -- ...two more Starter lines...
    { sSpeaker = "Player1", sCue = { Mattias = "Mattias.Guerrilla01", Jennifer = "Jen.Guerrilla01", Chris = "Chris.Guerrilla01" } }
  }
}
```

`sCue` is either a plain string (a fixed line, usually spoken by `"Starter"`) or a table keyed
`Chris`/`Jennifer`/`Mattias` (a hero-dependent line, spoken by `"Player1"`). `Mec` and `Jet` are much
shorter — one `tSequence` entry each, a single `Starter` line (`Mec`: "Ewan.PMC.RecruitEva01"; `Jet`:
"Eva.PMC.RecruitMisha01") with no flash step and no player response — these are the PMC-boss recruitment
intros, not full faction-outpost intros like `Gur`/`Pir`/`AllChi`.

### Per-contract entries
A full entry can carry these fields (all confirmed present somewhere in the 15):

- `nType` — optional, see above.
- `tAssetPreload` — `{ soundbank = {...}, wavebank = {...} }`. The only field every one of the 15 entries has.
- `tActors` — optional, only on `AllCon001` and `AllCon003`. One extra named actor beyond the two speaking
  positions, e.g. `AllCon001`'s `HeroChair = { sTemplate = "_aloutpost_interior_herochair", sPosition = "hp_al01_player" }`.
- `tPositions` — always exactly two keys, `Player1` and `Starter` (hardpoint name strings), across all 14
  non-stub entries — confirmed by grep, no entry has more or fewer named speaking positions.
- `tFaceAnimSets` — `Player1` sub-keyed `Chris`/`Jennifer`/`Mattias`; `Starter` a single anim-set string.
- `tCinematic` — keyed `Chris`/`Jennifer`/`Mattias`, each an ordered array of keyframe steps, plus a sibling
  `tCameraEffects` sub-table (same three hero keys) of depth-of-field/field-of-view samples over time.
- `tConfirmCinematic` / `tDeclineCinematic` — same shape as `tCinematic` (including their own
  `tCameraEffects`), played instead of it when the player accepts/declines at the briefing screen — anim
  names confirm this (`"..._Yes_..."` / `"..._No_..."` variants of the same base animation).

A typical `tCinematic` step sequence for one hero (trimmed from `AllCon001.tCinematic.Chris`):

```lua
Chris = {
  { tAnims = { Player1 = "ALL01_Contract_Briefing_Chris", Starter = "ALL01_Contract_Briefing_Starter-Chris" },
    OnTime = 32.1333, OnComplete = "Player1" },
  { tFlash = { sFile = "AllCon001_briefing.gfx", nTime = 29.1 }, OnTime = 39.566696 },
  { tCamera = { bHold = true }, Stall = true }
}
```

— an anim/VO step, a Scaleform overlay step, then a hold-and-wait step. That 3-step shape (and the
matching `{ nTime, tDepthOfField = {...}, tFieldOfView = {...} }` shape of each `tCameraEffects` sample)
recurs across all 14 non-stub entries; `tDepthOfField = {bHold = true}`-style camera holds and `Stall = true`
markers alone appear 84 times in the file.

The floor and ceiling of entry size:
- **`OilCon021` is the smallest, and the only entry with no cinematic at all** — 10 lines, shown in full:
  ```lua
  OilCon021 = {
    nType = knSimple,
    tAssetPreload = {
      soundbank = { "vo_oilCon021" },
      wavebank = { "vo_oilCon021" }
    }
  }
  ```
  No `tPositions`, `tFaceAnimSets`, or `tCinematic` — just audio preload. Notably this one *does* set
  `nType = knSimple`, but so do four other entries that have full cinematics (see above) — `nType` doesn't
  by itself predict whether an entry has a cinematic.
- **The largest is actually `JetCon001` (~2,308 lines)**, not `AllCon002` — though `AllCon002` (~1,786
  lines) is a good second example. Neither adds any new field type over the shape above; the extra length
  is overwhelmingly more `tCameraEffects` samples tracking a longer VO track. Concretely: `AllCon001`'s
  entry (961 lines, ~32s Chris VO) has 46 `nTime = ` camera-effect keyframes total; `AllCon002` (1,786
  lines, ~92s Chris VO) has 86 — roughly double the keyframes for roughly double (or more) the spoken
  runtime, not a richer schema.

## Functions

### `GetIntroIdByIndex(nIntroIndex)` / `GetIntroIndexById(sId)`
Both are plain linear scans over `Intros` with `pairs()` — `GetIntroIdByIndex` walks until the Nth entry and
returns its key; `GetIntroIndexById` walks until it finds a matching key and returns its position. Neither
sorts or orders `Intros` itself; they just agree with each other and with whatever order `pairs()` happens
to produce in a given run.

Their real purpose, confirmed from [`mrxbriefing`](../resident/mrxbriefing): `_StartIntro` calls
`WifBriefingData.GetIntroIndexById(sName)` to turn an intro's string key into an integer before calling
`Net.SetBriefingCheapCinematic(CHEAP_INTRO, ...)`, and `NetSafePlayCheapCinematic` calls
`WifBriefingData.GetIntroIdByIndex(nIntroIndex)` on the receiving end to turn that integer back into the
string key for `_PlayIntro`. In other words, these two functions exist so "which intro is currently playing"
can be replicated over the network as a small integer instead of a string.

## Notes for modders
- **Pure data — nothing runs on load.** Confirmed no `import()`, no `inherit()`, and no function besides the
  two lookups above anywhere in the file. Safe to read from; there's no initialization order or side effect
  to worry about.
- **Only these 15 contracts get an authored cinematic briefing.** Every other mission's briefing config
  falls back to an empty table — confirmed in [`mrxbriefing`](../resident/mrxbriefing)'s `Start()`:
  `tMissionData.tConfig = WifBriefingData[sMissionName] or {}`. Every downstream `if tConfig.tXxx then`
  check in that file is written to be a safe no-op against that fallback, so a modded contract with no
  entry here just behaves like an ordinary job briefing — it doesn't error.
- **Confirmed real call sites**, all found by grep across the decompiled corpus:
  - [`mrxbriefing`](../resident/mrxbriefing) is the main consumer — reads `tActors`, `tPositions`,
    `tFaceAnimSets`, `tCinematic`, `tConfirmCinematic`, `tDeclineCinematic` for the selected mission, and
    checks `tConfig.nType == WifBriefingData.knSimple` (alongside `_oStarter:IsBoss()`) in
    `_AcceptOrDeclineMission` to decide whether to play this module's authored confirm/decline cinematic or
    fall back to a generic "cheap cinematic" instead. It also owns all `Intros` playback (`_PlayIntro`/
    `_StartIntro`) and the two lookup functions above.
  - [`MrxStarter`](../resident/mrxstarter)'s `Load` pulls `tActors` from a boss starter's *first* offered
    briefing to spawn the extra HQ-interior prop before the briefing UI opens.
  - `WifPmcInterior` (`src/vz/wifpmcinterior.lua` — no wiki page yet) reads `Intros[sIntro].tHq` in
    `_ExitComplete` to animate the matching HQ portal blip once a viewed intro finishes.
- **Adding a custom flagship-style cinematic briefing just means adding a new top-level key** matching your
  contract's exact mission-ID string — nothing here pattern-matches or registers keys elsewhere;
  [`mrxbriefing`](../resident/mrxbriefing) picks it up automatically through the plain
  `WifBriefingData[sMissionName]` lookup.
- **Two harmless on-disk naming mismatches**, confirmed by grep, worth knowing if you're hunting for assets
  by filename rather than by Lua key: `AllCon003`'s `tAssetPreload`/hardpoints reference `...004`-numbered
  assets (`vo_allCon004`, `hp_al04_player`/`hp_al04_starter`), and `ChiCon003` does the same
  (`vo_chinCon004`, `hp_ch04_player`/`hp_ch04_starter`) — both consistent with a cut or renumbered 4th
  entry in each series that never got its internal asset names updated. The Lua table key
  (`AllCon003`/`ChiCon003`) is what the game actually looks up by, so this doesn't affect anything at
  runtime.
- **The `tCameraEffects.tDepthOfField`/`tFieldOfView` arrays mix bare identifier tokens with real numbers.**
  Entries like `{ nDuration, nAngle, nStartNear, 0.096, 2.9907, nEndFar, nBlur }` have real authored values
  only at some positions; `nDuration`, `nAngle`, `nStartNear`, `nEndNear`, `nStartFar`, `nEndFar`, and
  `nBlur` are never assigned anywhere in this file (confirmed by grep for each name) — as bare global reads
  they evaluate to `nil` at runtime. This reads like a decompiler/authoring-tool artifact rather than
  intentional data; if you need to hand-edit a camera-effect value, treat each array as "the numeric
  literal at this position," not as named fields.
