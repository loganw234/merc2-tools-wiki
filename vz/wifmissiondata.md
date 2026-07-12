---
title: WifMissionData
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 1
inherits: none
tags: [data]
verified: false
---

# WifMissionData

## Overview
`WifMissionData` is the game's native mission/contract registry — a single large table (`tMissionData`)
with one entry per contract or job across every faction (69 entries total), giving each a stable
identity, unlock/starter wiring, a critical-path flag, milestone thresholds for repeatable "job" types,
and PDA/journal display metadata. A thin getter API sits on top, and `Init()` derives one additional
field (`bContract`) at load time by parsing each mission id's own name.

## Inheritance
- Inherits from: none — base data module.
- Imports: `MrxUtil` (used once, in `Init`, to parse mission ids), [`WifMissionFlow`](wifmissionflow)
  (used once, in `GetNumCompletedContracts`).

## Instance pattern
Not stateless in the strictest sense: `tMissionData` is a static, hand-authored table, but `Init()`
mutates every entry in place the first time it runs, stamping on a derived `bContract` boolean. After
that, every other function only reads the table — there's no per-`uGuid` instance store, just this one
shared table plus an init pass.

## The `tMissionData` schema
Fields seen across entries (not all appear on every one):

| Field | Meaning |
|---|---|
| `sModuleName` | Repeats the entry's own key; present on every entry. |
| `sFactionId` | Owning faction (`"All"`, `"Chi"`, `"Gur"`, `"Oil"`, `"Pmc"`, `"Pir"`, `"Vza"`) — see gotcha below, this doesn't always match the id's own prefix. |
| `sStarter` | Which `MrxStarterManager` starter spawns/tracks this mission in the world. |
| `tMaterielScale` | Faction id → multiplier, e.g. `{Chi = 1}` — scales another faction's materiel/reinforcements for this mission. |
| `bCriticalPathMission` | Marks a main-story mission. |
| `tLayers` | Array of world-state "layer" names tied to this mission (consumed by `MrxLayerManager` elsewhere, e.g. in [`WifMissionFlow`](wifmissionflow)). |
| `bRepeatable` / `nLevels` | Repeatable side content with N difficulty levels. |
| `tMilestones` | Array of `{nMilestone, sKey}` — completion-count thresholds and their unlock/text keys, on repeatable "Job" type content. |
| `sTitle` | Present on ~15 entries — see the `GetMissionTitle` note below, this field looks vestigial. |
| `bCompletable` / `bCompleteable` | Inconsistent spelling across entries — see gotcha below. |
| `sPdaTexture`, `nPdaSortOrder` | PDA/journal listing icon and sort bucket (see the `knPdaSortOrder*` constants). |
| `tStartLocations` | Array of candidate teleport points, read via `GetMissionStartLocations` (inherited on `WifMissionFlow`, not defined in this file). |
| `bPlayerVisibleMission` | Flags a handful of story missions (`VzaCon001`, `PmcCon001`-`004`, `MecCon001`, `JetCon001`). |
| `bSkipInitialNotifications`, `bSuppressPdaDisplay` | Used by `PmcJob001`/`PmcJob002` — background stat-tracking "jobs" with no PDA presence. |
| `bContract` | **Not authored** — written by `Init()` (see below), not present in the literal source. |

Three representative entries, verbatim:

```lua
AllCon001 = {
  sModuleName = "AllCon001",
  sFactionId = "All",
  tMaterielScale = {Chi = 1},
  sStarter = "AllStarter0",
  bCriticalPathMission = true
},
```

```lua
AllJob003 = {
  sModuleName = "AllJob003",
  sFactionId = "All",
  bCompletable = false,
  tMilestones = {
    {nMilestone = 3, sKey = "AllJob003_Milestone1"},
    {nMilestone = 10, sKey = "AllJob003_Milestone2"},
    {nMilestone = 25, sKey = "AllJob003_Milestone3"},
    {nMilestone = 50, sKey = "AllJob003_Milestone4"}
  },
  sPdaTexture = "icon_destroy_2_mc",
  nPdaSortOrder = knPdaSortOrderStandingBty
},
```

```lua
AllCon052 = {
  sModuleName = "AllCon052",
  sFactionId = "All",
  sStarter = "AllStarter2",
  sTitle = "[AllCon052.Title]"
},
```

Top-of-file constants `knPdaSortOrderActiveContract` (1) through `knPdaSortOrderBillboards` (7) define
the seven PDA sort buckets referenced by `nPdaSortOrder`.

## Functions
### `Init()`
One-time pass over every `tMissionData` entry: calls `MrxUtil.ExplodeMissionName(sMissionId)` (splits a
mission id into a 3-char faction code, a 3-char type code `"Con"`/`"Job"`, and a numeric suffix) and
stamps `tMissionConfig.bContract = true` for `"Con"` missions, `false` for `"Job"` missions. Must run
before any function that reads `bContract` (see Notes).

### `IsMissionAContract(sMissionId)` / `IsMissionAJob(sMissionId)`
Guarded reads of the derived `bContract` field (return `nil` if `sMissionId` is unknown).

### `IsMissionOnCriticalPath(sMissionId)`
Guarded read of `bCriticalPathMission`.

### `GetMissionTitle(sMissionId)`
Does **not** read `tMissionData` at all — always returns the literal string
`"[" .. sMissionId .. ".Title]"`. See the `sTitle` gotcha below.

### `GetMissionFaction(sMissionId)` / `GetMissionStarter(sMissionId)`
Unguarded reads of `sFactionId` / `sStarter` — see gotcha below, these will error on an unknown id rather
than returning `nil`.

### `GetMissionIndexFromId(sMissionId)` / `GetMissionIdFromIndex(nIndex)`
Derive/resolve a 1-based numeric index purely from `pairs(tMissionData)` iteration order — see gotcha
below.

### `SetMissionData(tNewMissionData)`
Wholesale-replaces the entire `tMissionData` table (not a merge). Returns `nil` if passed `nil`, `true`
otherwise.

### `GetMissionMilestoneData(sMissionId)` / `GetMissionRepeatable(sMissionId)` / `GetMissionLevels(sMissionId)` / `IsMissionSuppressedInPda(sMissionId)` / `GetMissionPdaTexture(sMissionId)` / `GetPdaSortOrder(sMissionId)`
All guarded (`if sMissionId and tMissionData[sMissionId] then ...`) reads of `tMilestones` /
`bRepeatable` / `nLevels` / `bSuppressPdaDisplay` / `sPdaTexture` / `nPdaSortOrder` respectively.

### `GetIsCompleteable(sMissionId)`
Reads `tMissionData[sMissionId].bCompleteable` — note the spelling — and defaults to `true` if that
field is absent. See gotcha below.

### `GetNumCompletedContracts()`
Asks `WifMissionFlow.GetMissionStates()` (a method [`WifMissionFlow`](wifmissionflow) inherits from its
own native base class — not defined in that file's own source) for a list of `{sMissionId, sState}`
pairs, and counts the ones that are both a contract and `"complete"`.

### `GetNumContracts()`
Counts every `tMissionData` entry for which `IsMissionAContract` is true.

## Events
None — pure data-plus-getter module, no `Event.*` calls anywhere in this file.

## Notes for modders
This is the native mission registry that `ContractFramework.lua`/[Contract Framework](../contract-framework/)
was built to avoid hooking into directly — see
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why a save-safe,
ephemeral system was built instead of extending this one.

- **Call `Init()` first.** `bContract` doesn't exist on any entry until `Init()` has run once — until
  then, `IsMissionAContract`/`IsMissionAJob`/`GetNumContracts`/`GetNumCompletedContracts` all read as
  false/zero.
- **Gotcha — `bCompletable` vs `bCompleteable`:** `AllJob003`, `ChiJob003`, and `OilJob004` all set
  `bCompletable = false` (correct spelling), but `GurJob001` is the only entry that sets
  `bCompleteable = false` (extra "e") — and `GetIsCompleteable()` only ever reads the `bCompleteable`
  spelling. So for `AllJob003`/`ChiJob003`/`OilJob004`, the getter finds nothing, falls through its `nil`
  check, and returns `true` — as far as this getter is concerned, those three "not completable" jobs
  actually read as completable. Whether any other code reads `bCompletable` directly, bypassing the
  getter, wasn't checked here.
- **Gotcha — unguarded getters:** `GetMissionFaction`, `GetMissionStarter`, and `GetIsCompleteable` index
  `tMissionData[sMissionId]` with no existence check, unlike most of the getters in this file — pass an
  unknown id and they error instead of returning `nil`.
- **Gotcha — fragile numeric indices:** `GetMissionIndexFromId`/`GetMissionIdFromIndex` number missions
  purely by `pairs()` iteration order over `tMissionData`, not by any authored field. That's consistent
  within one run against an unmodified table, but adding, removing, or reordering entries (e.g. from a
  mod) can silently renumber every mission after the change.
- `sFactionId` doesn't always match the id's own prefix: `OilCon020`'s `sFactionId` is `"Pmc"`, not
  `"Oil"` — don't assume faction from the id string alone.
- `sTitle`, where present, is always exactly the same string `GetMissionTitle()` synthesizes from the id
  anyway (`"[<id>.Title]"`). No call site found in this corpus reads `tMissionData[id].sTitle` directly —
  the confirmed title lookups (e.g. in `resident/mrxhq.lua`) all go through `GetMissionTitle()` instead —
  so the field looks vestigial from this getter's perspective.
- `SetMissionData()` replaces the whole registry at once; there's no merge/patch entry point here, so
  adding missions via this API means building a full replacement table rather than adding one entry.
