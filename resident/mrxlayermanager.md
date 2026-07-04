---
title: MrxLayerManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [layer management, world state]
verified: true
verified_note: read directly from source in full (mrxlayermanager.lua is only 360 lines) -- corrects the
  Instance pattern wording, documents the exact Mark/Process two-phase commit mechanism, a real confirmed
  parameter-passing bug in Remove(), and adds a categorized catalog of ~650 real layer names found across
  the corpus, built while investigating whether the Alamo/Dynasty-class ships' appearance is gated behind
  a layer. Retains the earlier confirmed note on _AddRequest's graceful culling of nonexistent layer names,
  found via the [Custom Contract deep dive](../deep-dives/custom-contract). Adds a second, independently-
  sourced boot-time layer manifest (170 static + 246 default-dynamic names) read directly, verbatim, from
  vz/xQ!L.lua's own literal _tStaticLayers/_tDefaultDynamicLayers tables -- found while investigating the
  Pg.Spawn coverage gap documented in the [World Inspector deep dive](../deep-dives/world-inspector).
---

# MrxLayerManager

*Module: mrxlayermanager.lua*

## Overview
`MrxLayerManager` is the mechanism behind every "the world changed because of something you did" moment in
this game -- a base gets destroyed, an outpost gets captured, a story chapter advances and a region's
geometry swaps to its next state, a one-time reveal happens after a specific mission completes. All of it
routes through this one module: named "layers" of level geometry get loaded or unloaded, and everything
else (missions, `WifMissionFlow`'s binding table, region-progression code) just tells this module which
named layers should exist right now.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxUtil`

## Instance pattern
**Singleton module with real process-wide state** — not stateless, and not per-`uGuid`. There's exactly one
copy of this module's four tracking tables for the whole running game:
- `_tRequests`: pending multi-layer operations, each tracking how many of its layers have finished
  (`nDone`/`nQuota`) so a batched callback fires only once every layer in that call is done.
- `_tOpQueue`: one entry per layer name currently being worked on, coalescing multiple requests that
  happen to touch the same layer into a single queued operation.
- `_tLoadedLayers`: every *dynamic* layer currently loaded, keyed by lowercased name. The value is a
  boolean, not just a presence flag — see `MarkForRemoval` below, it doubles as the "marked for removal"
  flag for that same layer.
- `_tLayersToBeAdded`: layers staged via `MarkForAddition`, not yet actually requested.
- `_knLayersToProcessCap` (`local`, = 10): a hard concurrency cap — genuinely `local`, not reachable or
  tunable from outside this file.

## Functions

### `Init()`
Stores `Sys.GetAssetRequestMax()` at startup (`_knOrigAssetRequestMax`) so it can be restored later once
the operation queue drains.

### `Add(vLayers, fCallback, tCallbackArgs, bCullDupes, bStatic, bClientNeedsLoadingScreen)`
The real, immediate "load this layer" entry point — thin wrapper over `_AddRequest(_knRequestTypeAdd, ...)`.
`vLayers` accepts either a single string or a table of strings. This is confirmed the correct function to
call when you want a layer to actually load *right now*, in contrast to `MarkForAddition` below, which only
stages a change.

### `Remove(vLayers, fCallback, tCallbackArgs, bClientNeedsLoadingScreen)`
The real, immediate "unload this layer" entry point.

**Confirmed bug, read directly from source:**
```lua
function Remove(vLayers, fCallback, tCallbackArgs, bClientNeedsLoadingScreen)
  _AddRequest(_knRequestTypeRemove, vLayers, fCallback, tCallbackArgs, bClientNeedsLoadingScreen)
end
```
`_AddRequest`'s real signature is `_AddRequest(nRequestType, vLayers, fCallback, tCallbackArgs, bCullDupes,
bStatic, bClientNeedsLoadingScreen)` — five parameters after `vLayers`, not four. `Remove` only supplies
four positional arguments after `vLayers`, so its own `bClientNeedsLoadingScreen` argument lands in
`_AddRequest`'s **`bCullDupes`** slot instead, and `_AddRequest`'s real `bClientNeedsLoadingScreen` parameter
is always `nil` for every `Remove` call, no matter what's passed. In practice this specific mix-up is inert
(`bCullDupes` is only ever checked when `nRequestType == _knRequestTypeAdd`, which a `Remove` call never
is), but the practical consequence is real: **`Remove` can never show a client loading screen, regardless of
what you pass as its fourth argument** — that parameter silently goes nowhere.

### `RemoveDynamicLayers(fCallback, tCallbackArgs)` / `RemoveAllLayers(tStaticLayers, fCallback, tCallbackArgs)`
Convenience wrappers: the first removes every currently-loaded dynamic layer (walks `_tLoadedLayers`); the
second does the same but also folds in a caller-supplied list of static layers to remove alongside them.

### `MarkForRemoval(vLayers)` / `MarkForAddition(vLayers)`
**These do not load or unload anything by themselves** — they only stage intent into the tracking tables,
lowercasing every name first. This is the single most important thing to know before using this module from
a mod: calling `MarkForAddition({"my_layer"})` alone changes nothing visible until `ProcessMarkedLayers()`
(below) is separately called.

```lua
function MarkForRemoval(vLayers)
  ...
  for i, sLayerName in ipairs(tLayers) do
    sLayerName = string.lower(sLayerName)
    if _tLoadedLayers[sLayerName] ~= nil then
      _tLoadedLayers[sLayerName] = true       -- true = "loaded, and marked for removal"
    end
    _tLayersToBeAdded[sLayerName] = nil        -- cancels a previously-staged addition of the same name
  end
end

function MarkForAddition(vLayers)
  ...
  for i, sLayerName in ipairs(tLayers) do
    sLayerName = string.lower(sLayerName)
    _tLayersToBeAdded[sLayerName] = true
    if _tLoadedLayers[sLayerName] == true then
      _tLoadedLayers[sLayerName] = false       -- cancels a previously-staged removal of the same name
    end
  end
end
```
The two functions are exact mirrors and cancel each other out for the same layer name — staging a removal
clears a pending addition and vice versa, before anything is actually requested.

### `RemoveMarkedLayers(fCallback, tCallbackArgs)`
Collects every layer name currently flagged `true` in `_tLoadedLayers` (i.e. marked for removal) and calls
the real `Remove()` on all of them at once.

### `ProcessMarkedLayers(fCallback, tCallbackArgs)`
**The function that actually commits everything staged by `MarkForRemoval`/`MarkForAddition`.** Two-phase,
strictly sequential — removals first, then additions, never both at once:
```lua
function ProcessMarkedLayers(fCallback, tCallbackArgs)
  local function _MarkedLayersAdded()
    _tLayersToBeAdded = {}
    MrxUtil.CallWithOptionalArgs(fCallback, tCallbackArgs)
  end
  local function _MarkedLayersRemoved()
    local tLayers = {}
    for sLayerName, _ in pairs(_tLayersToBeAdded) do
      table.insert(tLayers, sLayerName)
    end
    Add(tLayers, _MarkedLayersAdded)
  end
  RemoveMarkedLayers(_MarkedLayersRemoved)
end
```
Confirmed from real call sites (`vz/wifmissionflow.lua`) that most of the game's own mission-completion
handlers call `MarkForRemoval`/`MarkForAddition` *without* an adjacent `ProcessMarkedLayers()` call right
there — the actual commit is batched and happens elsewhere (a handful of call sites do call it directly,
e.g. inside `_ChangeOutpostStaging`, but only conditionally, under `MrxCheatBootstrap.IsSkipModeEnabled()`).
**Practical implication for modding: if you want a layer to appear/disappear immediately and reliably from
your own script, call `Add`/`Remove` directly — don't rely on `MarkForAddition`/`MarkForRemoval` alone**,
since you'd otherwise be depending on some other system's timing to eventually flush the staged change.

### `_AddRequest(nRequestType, vLayers, fCallback, tCallbackArgs, bCullDupes, bStatic, bClientNeedsLoadingScreen)`
The real entry point behind both `Add` and `Remove`. For every requested layer name (lowercased first):
- Culls it if `Sys.GetIgnoreLayers()` exists and lists that name (logged, not an error).
- Checks `Pg.AssetExists(sLayerName, "layer")` — **a nonexistent layer name is silently culled and logged,
  never an error or crash.** Confirmed: a name that doesn't correspond to a real compiled layer just logs
  `"Culling layer <name> from add request; layer does not exist"` via `Debug.Printf` and is dropped from
  the request. This is the same safety net already confirmed to make an auto-generated, never-real layer
  name harmless for a custom mission (see the [Custom Contract deep dive](../deep-dives/custom-contract)).
- Culls an add if `bCullDupes` is set and the layer's already loaded/static; culls a remove if the layer's
  already unloaded.
- What survives culling gets bundled into a `tRequest` (tracking `nDone`/`nQuota` for this specific batch)
  and merged into `_tOpQueue`, keyed by layer name — if two different callers both requested the same layer
  around the same time, their requests share one queued operation rather than double-processing it.
- If every layer in the call got culled, the callback still fires immediately, synchronously, with zero
  layers actually touched.

### `_ProcessOpQueue()`
The throttled worker loop. Only `_knLayersToProcessCap` (10) layer load/unload operations run concurrently —
once that many are in flight, this function just returns early on each call and relies on `_LayerStatusChange`
(below) to re-invoke it as operations complete, until the queue drains. Also temporarily raises
`Sys.SetAssetRequestMax()` to match the pending-operation count when needed, restoring the original value
once the queue empties. For each queued layer: `Pg.LoadLayer`/`Pg.ReloadLayer` for an add (reload instead of
load if the layer's already known and not static), `Pg.UnloadLayer` for a remove — all three are natives,
called with `_LayerStatusChange` as their completion callback.

### `_LayerStatusChange(sRequestType, sLayerName, sLayerType, bSuccess)`
The native completion callback. Updates `_tLoadedLayers` (adds get `false` — loaded, not marked for
removal; removes get cleared to `nil`), decrements the in-flight counter, tallies completion against every
`tRequest` that included this layer, and — only once a request's `nDone` reaches its `nQuota` (every layer
in that original `Add`/`Remove` call has finished) — queues that request's callback to fire. Then re-invokes
`_ProcessOpQueue()` to pick up more throttled work before finally firing any now-completed callbacks. A
failed load/unload hits `ASSERT`, not a silent failure.

### `SaveSingleton()` / `LoadSingleton(tSaveData, fCallback, tCallbackData)`
**This whole subsystem is save-game persisted.** `SaveSingleton` returns every currently-loaded dynamic
layer not marked for removal, plus anything staged-but-not-yet-loaded in `_tLayersToBeAdded`. `LoadSingleton`
diffs that saved list against whatever's actually loaded right now via `FindLayerIntersection` (below), then
does a single `Remove(toRemove, function() Add(toAdd, fCallback, tCallbackData) end)` to reconcile — meaning
a mod that force-adds a layer live (via `Add`/`MarkForAddition`+`ProcessMarkedLayers`) does **not** persist
across a save/reload by itself unless the mod also re-applies it every load (the same `OnLoad`-reapplies-every-level
pattern used throughout this wiki), since nothing here writes that choice into `tSaveData` on its own.

### `ResetState()`
Wipes all four tracking tables to empty — presumably called on a fresh game/level start.

### `FindLayerIntersection(tR, tA)`
A classic sorted two-pointer merge-diff between two layer-name lists (`tR` = currently loaded, `tA` = saved
target state): returns `(tRemoveList, tAddList)` — layers only in `tR` need removing, layers only in `tA`
need adding, layers in both stay untouched. Generic enough to reuse for any two layer-name-list reconciliation,
not `SaveSingleton`/`LoadSingleton`-specific.

## Events
Doesn't subscribe to any engine event directly — its "event handling" is `_LayerStatusChange`, a plain
callback function *passed to* `Pg.LoadLayer`/`Pg.ReloadLayer`/`Pg.UnloadLayer`, not something registered via
`Event.Create`.

## World-state layer catalog

Every real, in-use layer name found across the ~230 decompiled `.lua` files (`grep`-extracted, deduplicated
case-insensitively since `MrxLayerManager` lowercases every name it touches — **649 distinct layers**, found
while investigating what triggers the Alamo/Dynasty-class ships' appearance in Lake Maracaibo). This is
almost certainly not the *complete* set that exists in the compiled game (some layers may only ever be
referenced from compiled level-editor triggers rather than any `.lua` file), but it's everything reachable
from source, which is also everything a mod could plausibly reference or copy the naming convention from.

### The naming convention

Layer names follow `vz_state_<what>_<suffix>` (case is never significant — everything gets lowercased at
the API boundary). Two broad families:

**Mission-tied layers** — `vz_state_<factioncon|job><NNN>_<suffix>`, one small family of state variants per
mission, 516 of the 649 total. Confirmed suffix vocabulary and what each means, from reading real
`fConseq`/`Activated` bodies across many missions:

| Suffix | Meaning |
|---|---|
| *(none)* | The mission's own base/container layer — its own dedicated geometry, independent of state. |
| `pristine` | The undamaged/untouched starting state of whatever this mission's set-piece is. |
| `staging` | Pre-activation setup geometry/triggers for this mission, before it's actually live. |
| `defenses` | Hostile/enemy defensive setup for a stage of this mission. |
| `destroyed` / `ruined` | The post-destruction state, swapped in once the objective's target is destroyed. |
| `captured` | The post-capture state, for outpost/base-capture-type objectives specifically (as opposed to destroy-type, which uses `destroyed`). |
| `hostiles` | An active-enemies-present sub-state (seen paired with `pristine`/`destroyed` per sub-objective in `ChiCon002`). |
| `tg` | Seen paired 1:1 with many `Con050`/`051`/`052`/`053`-style contracts (both a bare `<id>_Tg` and a `<id>c_Tg` variant) — likely a target/trigger-marker layer; exact purpose not confirmed from source alone. |
| `post` | Rare (only 3 confirmed: `JetCon001`, `OilCon001`, `VzaCon001`) — a permanent world change that persists after this one specific mission, distinct from the region's own `act1`/`act2` progression. **This is the layer suspected (not proven — layer *contents* are compiled binary, invisible from Lua) to be what reveals the two additional Alamo-class ships after completing `OilCon001`.** |
| `a`/`b`/`c`.../`01`/`02`/`03`... | Sub-stage or sub-target letters/numbers for multi-part missions (job-type missions especially — `AllJob002`/`ChiJob005`/`GurJob011` etc. each have 5-10 numbered or lettered sub-stages, each with its own `pristine`/`staging`/`defenses`/`destroyed` set). |

**Regional/other layers** — 133 of the 649, not tied to a single mission ID. The load-bearing ones for
"change something bigger than one mission":

<details markdown="1">
<summary>Regional act-progression layers (confirmed region names, each with 2-3 chapter states)</summary>

`amazon` (act1/2), `angel_falls` (act1), `car_city` — Caracas (act1/act2all/act2chi/act3all/act3chi, plus an
`all`/`pristine` base), `car_dock` (act1), `car_estate` (act1), `car_shanty` (act1), `cumana`
(act1/act1all_n/act1all_s/act1chi/act2chi), `guanare` (act1), `gurhq` (act1), `jungle_mountain` (act1/2),
`mar_altagracia` — Maracaibo (act1/2), `mar_city` — Maracaibo (act1/act1_depot/act2/act3, plus
`pristine`/`ruined`), `mar_industrial` — Maracaibo (act1/act2/act3, plus `pristine` — **the region `OilCon001`
advances**), `mar_outskirt` (act1/2), `mar_village` (act1), `margarita` (act2, plus `crash`/`precrash`),
`merida` (act1/act1_helo/act1_staging/act2/act2_helo), `pmc` (act1, see PMC HQ interior below),
`solbunkerbase` (act1).

</details>

<details markdown="1">
<summary>PMC HQ interior state layers</summary>

`vz_state_pmc`, `vz_state_pmc_pristine`, `vz_state_pmc_livedin`, `vz_state_pmc_act1`,
`vz_state_pmcinterior`, `vz_state_pmcinterior_hel`, `vz_state_pmcinterior_jet`, `vz_state_pmcinterior_mec`,
`vz_state_pmcinterior_mecabsent`, `vz_state_pmc001_villawaveone`, `vz_state_pmc001_villawavetwo` — layers
tied to `WifPmcInterior`'s own HQ state; the `_hel`/`_jet`/`_mec` suffixes plausibly correspond to which
secondary hero (Ewan/Misha/Eva) is currently active, `_mecabsent` to Eva specifically not yet being present.

</details>

<details markdown="1">
<summary>Faction HQ / staging layers</summary>

`vz_state_all_hq_structures`, `vz_state_chi_hq_structures`, `vz_state_staging_all_hq`,
`vz_state_staging_chi_hq`, `vz_state_staging_oildepot`, `vz_state_staging_oilhq`,
`vz_state_staging_pirhq`, `vz_state_gurhq_act1`.

</details>

<details markdown="1">
<summary>Faction fuel/resource layers</summary>

`vz_state_all_fuel_amazon`, `vz_state_chi_fuel_amazon`, `vz_state_gur_fuel_junglemountains`,
`vz_state_oil_fuel_maroutskirts` — per-faction fuel-resource state, scoped per-region.

</details>

<details markdown="1">
<summary>Atmosphere / line-region markers</summary>

`vz_state_car_big_lineregion`, `vz_state_mar_big_lineregion`, `vz_state_mer_big_lineregion` — these
correspond to the `Graphics.Atmosphere.ChangeLineRegionSetting(Pg.GetGuidByName("rgn_atmo_..."), ...)`
pattern seen in mission scripts (e.g. `chicon002.lua`'s `"rgn_atmo_Maracaibo"` call) — weather/atmosphere
region markers, not gameplay content.

</details>

<details markdown="1">
<summary>Misc one-offs</summary>

`vz_state_cashpickups`, `vz_state_munitions_freeplay`, `vz_state_ocgate_dynamic`,
`vz_state_gua_upperclass_pristine`, `vz_state_mer_commercialpristine`, `vz_state_mer_oilrig_pristine`
(+`_tg`), `vz_state_sol_base_pristine`, `vz_state_sol_bunker` (+`_pmc004`),
`vz_state_solanobase_pmc004`, `vz_state_solbunkerbase_pmccon004`, `vz_state_oc_depot` (+`_pristine`),
`vz_state_temp_staging_gurcon002`.

</details>

<details markdown="1">
<summary>Full mission-ID → suffix table (87 mission/sub-mission IDs, all 516 mission-tied layers)</summary>

Read as: `<mission id>` has layers named `vz_state_<mission id>_<each suffix listed>` (plus, for entries
listing a bare number/letter with no trailing text, `vz_state_<mission id>_<that number/letter>` itself,
distinct from its own `_staging`/`_pristine`/etc. variants).

| Mission ID | Suffixes found |
|---|---|
| allcon001 | pristine |
| allcon002 | boats, mlrs, officers |
| allcon003 | and_chicon003_pristine, invasion, pristine |
| allcon050 / allcon050c | tg |
| allcon052 / allcon052c | tg |
| allcon053 / allcon053c | tg |
| alljob001 | 01_captured, 01_defenses, 01_pristine, 01_staging, 02_captured, 02_pristine, 03_captured, 03_defenses, 03_pristine, 03_staging2, 04_captured, 04_defenses, 04_pristine, 04_staging |
| alljob002 | 01-05, each with _defenses, _pristine, _staging |
| alljob005 | 01-05, each with (bare), _defenses, _destroyed, _staging |
| alljob009 | 01-05, each with (bare), _defenses, _destroyed, _pristine, _staging |
| alljob010 | 01-05, each with (bare, 01 only), _pristine (02-05), _staging |
| chicon001 | pristine |
| chicon002 | bridge_destroyed, bridge_hostiles, bridge_pristine, depot_destroyed, depot_hostiles, depot_pristine, hq_destroyed, hq_hostiles, hq_pristine, pristine, traffic |
| chicon003 | pristine |
| chicon005 / chicon006 | a_pristine, b_pristine, c_pristine |
| chicon008 | a |
| chicon050 / chicon050c | tg |
| chicon051 / chicon051c | tg |
| chicon053 / chicon053c | tg |
| chicon054 | pristine, staging |
| chijob001 | 01_captured/_defenses/_pristine/_staging, 02 same, 03_pristine/_staging, 04_captured/_defenses/_pristine/_staging |
| chijob002 | 01-05, each with (bare), _pristine, _staging |
| chijob005 | a-g, each with _defenses, _destroyed, _pristine, _staging |
| chijob006 | a-e, each with _defenses, _destroyed, _pristine, _staging |
| chijob009 | a_defenses/_destroyed/_pristine/_pristine_tg/_staging, b_pristine/_pristine_tg |
| chijob010 | 01-05, each with (bare, most), _pristine (01/02/04), _staging |
| gurcon001 | fortress, fortress_destroyed, outpost, outpost_pristine, pristine, staging |
| gurcon002 | pristine, tg, traffic |
| gurcon005 | airportdefbase, airportdefbase_staging |
| gurcon050 / gurcon050c | tg |
| gurcon052 / gurcon052c | tg |
| gurcon053 / gurcon053c | tg |
| gurjob002 | 01-05, each with _pristine, _staging |
| gurjob003 / gurjob005 | captured, defenses, pristine, staging |
| gurjob007 | 01-03, each with (bare), _defenses, _destroyed |
| gurjob008 | 01-02, each with _captured, _defenses, _pristine, _staging |
| gurjob011 | 01-10, each with _defenses, _destroyed |
| gurjob012 | 01-05, each with _pristine, _staging |
| jetcon001 | copterattack, cp01, post, pristine |
| oilcon001 | part1, post |
| oilcon002 | pristine |
| oilcon020 | deliveribles, mpdeliverables |
| oilcon021 | staging |
| oilcon050 / oilcon050c | tg |
| oilcon051 / oilcon051c | tg |
| oilcon052 / oilcon052c | tg |
| oiljob001 / oiljob002 / oiljob005 | captured, defenses, pristine, staging |
| oiljob008 | a-m (13 sub-stages), mix of _pristine/_staging/_defenses/_destroyed/_ruined per letter |
| oiljob011 | 01-05, each with (bare), _pristine, _staging |
| oiljob012 | 01-05, each with _pristine, _staging |
| pircon002 / pircon003 | deliverables, mp |
| pircon004 | pristine |
| pircon051 / pircon051c | tg |
| pircon052 / pircon052c | tg |
| pirjob002 | 01-03, each with _captured, _defenses, _pristine, _staging |
| pirjob007 | a/b/c/e/f/g, each with a mix of _defenses/_destroyed/_pristine/_staging |
| pirjob010 / pirjob011 | 01-03, each with (bare), _defenses, _destroyed |
| pirjob012 | 01-10, each with (bare), _pristine, _staging |
| pmccon001 | actionhijacktutorial, investigatevilla, villasoldiers |
| pmccon003 | bunkeraa, bunkerdefenses, getcarmona, pmcattack, pristine, solbunkerbase |
| pmccon004 | alliesnuked, chinanuked |
| pmccon013 | mp |
| pmccon015 / pmccon016 | a |
| pmccon018 | veh |
| pmccon033 | popdown, popup |
| vzacon001 | cp01, cp02, pregate1, pregate2, pristine, ruined |

</details>

## Boot-time layer manifest (`vz/xQ!L.lua`)

Found while investigating why hooking `Pg.Spawn` (see the
[World Inspector deep dive](../deep-dives/world-inspector)) only ever caught a tiny fraction of what
populates the open world during play — the answer turned out to be this file. `vz/xQ!L.lua` is the
level/game bootstrap script, and unlike the 649-name catalog above (recovered by grepping every
`MrxLayerManager.*` call site scattered across the whole corpus), these two tables are read directly,
verbatim, as literal string arrays hardcoded in that one file — no grep, no inference about what might
exist:

```lua
function _LoadLayers()
  if not _bStaticLayersLoaded then
    MrxLayerManager.Add(_tStaticLayers, _AttemptGameplaySetup, {"static"}, true, true)
  end
  ...
    MrxLayerManager.Add(_tDefaultDynamicLayers, _AttemptGameplaySetup, {"dynamic"})
  ...
end
```

Every real session loads both tables, unconditionally, as part of getting into gameplay at all — this is
the actual native bulk-population mechanism the rest of this page's catalog only ever reaches indirectly,
through individual mission scripts' own later `Add`/`Remove`/`MarkForAddition`/`MarkForRemoval` calls.

### `_tStaticLayers` (170 entries)

Permanent world geometry — terrain, roads, foliage, billboards, per-region "tiny" (presumably distant-LOD)
variants, and each faction's HQ. Notably, almost none of these follow the `vz_state_*` mission-suffix
convention documented above — they're not "state" layers at all, which is exactly why grepping
`MrxLayerManager.*` call sites elsewhere in the corpus never turned them up: nothing ever calls
`Add`/`Remove` on them again after this one boot-time load, so no mission script's own source ever
references them by name.

<details markdown="1">
<summary>Full list (170)</summary>

```
vz_All_Hq, vz_All_Job001_a, vz_All_Job001_b, vz_All_Job001_c, vz_All_Job001_d, vz_All_Job002_a,
vz_All_Job002_b, vz_All_Job002_c, vz_All_Job002_d, vz_All_Job002_e, vz_All_job005_a, vz_All_job005_e,
vz_All_job005_d, vz_All_Job010_a, vz_All_Job010_b, vz_All_Job010_c, vz_All_Job010_d, vz_All_Job010_e,
vz_amazon_base, vz_amazon_scrub, vz_amazon_road, vz_Amazon_foilage, vz_Amazon_billboard,
vz_Angel_Falls_Foilage, vz_angel_falls_road, vz_atmosphere_regions, vz_boundary_regions, vz_caracas_base,
vz_caracas_scrub, vz_car_city, vz_car_billboard, vz_car_city_roads, vz_car_estate, vz_caracas_foilage,
vz_car_shanty02, vz_car_shanty_roads, vz_Chi_Con005_d, vz_Chi_Con006_d, vz_Chi_Con054, vz_Chi_Job001_a,
vz_Chi_Job001_b, vz_Chi_Job001_c, vz_Chi_Job001_d, vz_Chi_Job002_a, vz_Chi_Job002_b, vz_Chi_Job002_c,
vz_Chi_Job002_d, vz_Chi_Job002_e, vz_Chi_Job006_a, vz_Chi_Job006_b, vz_Chi_Job006_c, vz_Chi_Job006_d,
vz_Chi_Job006_e, vz_Chi_Job010_a, vz_Chi_Job010_b, vz_Chi_Job010_c, vz_Chi_Job010_d, vz_Chi_Job010_e,
Vz_CommonLocations, vz_cum_city, vz_cum_billboard, vz_cum_margarita, vz_cum_outskirt, vz_cum_fortress,
vz_cum_roads, vz_cumana_scrub, vz_Cumana_foilage, vz_gua_upperclass, vz_gua_billboard, vz_guanare_road,
vz_Gua_vzbase, vz_Gur_base, vz_gur_base_mines, vz_Gur_HQ, vz_Gur_Job002_b, vz_Gur_Job002_c, vz_Gur_Job002_d,
vz_Gur_Job002_f, vz_Gur_job002_h, vz_Gur_job002_j, vz_Gur_Job003, vz_Gur_Job005, vz_Gur_Job008_a,
vz_Gur_Job008_b, vz_Gur_Job012_a, vz_Gur_Job012_g, vz_Gur_Job012_i, vz_Jet_Con001,
vz_jungle_mountain_billboard, vz_jungle_mountain_foilage, vz_jungle_mountain_road,
vz_jungle_mountain_scrub, vz_landingzone, vz_mar_altagracia, vz_mar_altagracia_roads, vz_mar_city,
vz_mar_fortress, vz_mar_roads, vz_mar_billboard, vz_mar_foilage, vz_mar_scrub, vz_mar_industrial,
vz_mar_industrial_roads, vz_mar_outskirt, vz_mar_outskirt_roads, vz_mar_village, vz_mar_village_roads,
vz_mer_commercial, vz_mer_billboard, vz_mer_dock, vz_mer_outskirt, vz_mer_residential, vz_mer_white,
vz_merida_foilage, vz_merida_roads, vz_merida_scrub, vz_Oil_Job001, vz_Oil_Job002, vz_Oil_Job005,
vz_Oil_Job008_d, vz_oil_job011_a, vz_oil_job011_c, vz_oil_job011_e, vz_oil_job011_h, vz_oil_job011_i,
vz_oil_job011_j, vz_oil_job011_f, vz_oil_job011_g, vz_PIR_HQ, vz_Pir_con003, vz_Pir_Job002_a,
vz_Pir_Job002_b, vz_Pir_Job002_c, vz_Pir_Job007_a, vz_Pir_Job012_a, vz_Pir_Job012_b, vz_Pir_Job012_c,
vz_Pir_Job012_d, vz_Pir_Job012_e, vz_Pir_Job012_f, vz_Pir_Job012_g, vz_Pir_Job012_h, vz_Pir_Job012_i,
vz_Pir_Job012_j, vz_Pirate_Isles_foilage, vz_Pirate_Isles_roads, vz_Pirate_Isles_scrub, vz_PMC,
vz_PMC_roads, vz_PMC_scrub, vz_PMC_foilage, vz_poi_lineregions, vz_rover_camera_test, vz_sfx_ambience,
vz_waterSounds, vz_sol_base, VZ_start_location, vz_teleporter, vz_LowResTerrain, VZ_terrain,
vz_caracas_tiny, vz_maracaibo_tiny, vz_amazon_tiny, vz_angel_falls_tiny, vz_jungle_mountain_tiny,
vz_merida_tiny, vz_guanare_tiny, vz_cumana_tiny, vz_pirate_isles_tiny, vz_pmc_tiny
```

</details>

### `_tDefaultDynamicLayers` (246 entries)

The default/starting ("pristine") state for essentially every region and mission-tied set piece in the
game, loaded up front so the world looks right before any contract has been touched. Unlike the static
list, most of these names *do* follow the `vz_state_*` convention and substantially overlap in spirit with
the mission-ID catalog above — this is likely where a large share of that catalog's own `_pristine`/
`_staging` entries actually get loaded from at runtime. No line-by-line cross-reference against the
existing 649-name catalog has been done here; treat this as a second, independently-sourced list, not a
verified diff against the first.

<details markdown="1">
<summary>Full list (246)</summary>

```
vz_state_car_city_pristine, vz_state_mar_city_pristine, vz_state_OC_Depot_pristine, vz_state_OC_Depot,
vz_state_mar_industrial_pristine, vz_state_mer_oilrig_pristine, vz_state_mer_oilrig_pristine_tg,
vz_State_Margarita_precrash, vz_State_AllCon001_pristine, vz_state_AllCon003_and_ChiCon003_Pristine,
vz_state_AllJob001_01_Pristine, Vz_State_AllJob001_01_Staging, vz_state_AllJob001_02_Pristine,
vz_state_AllJob001_03_Pristine, Vz_State_AllJob001_03_Staging2, vz_state_AllJob001_04_Pristine,
Vz_State_AllJob001_04_Staging, Vz_State_AllJob002_01_Pristine, Vz_State_AllJob002_02_Pristine,
Vz_State_AllJob002_03_Pristine, Vz_State_AllJob002_04_Pristine, Vz_State_AllJob002_05_Pristine,
Vz_State_AllJob002_01_Staging, Vz_State_AllJob002_02_Staging, Vz_State_AllJob002_03_Staging,
Vz_State_AllJob002_04_Staging, Vz_State_AllJob002_05_Staging, Vz_State_AllJob009_01_Pristine,
Vz_State_AllJob009_02_Pristine, Vz_State_AllJob009_03_Pristine, Vz_State_AllJob009_04_Pristine,
Vz_State_AllJob009_05_Pristine, Vz_State_AllJob010_02_Pristine, Vz_State_AllJob010_03_Pristine,
Vz_State_AllJob010_04_Pristine, Vz_State_AllJob010_05_Pristine, vz_state_amazon_act1,
vz_state_angel_falls_act1, Vz_State_Chi_HQ_Structures, Vz_State_ChiCon001_Pristine,
vz_State_ChiCon002_HQ_Pristine, vz_State_ChiCon002_Bridge_Pristine, vz_State_ChiCon002_Depot_Pristine,
vz_state_ChiCon054_Pristine, vz_state_ChiCon054_Staging, vz_state_ChiJob001_01_Pristine,
Vz_State_ChiJob001_01_Staging, vz_state_ChiJob001_02_Pristine, Vz_State_ChiJob001_02_Staging,
vz_state_ChiJob001_03_Pristine, Vz_State_ChiJob001_03_Staging, vz_state_ChiJob001_04_Pristine,
Vz_State_ChiJob001_04_Staging, Vz_State_ChiJob002_01_Pristine, Vz_State_ChiJob002_02_Pristine,
Vz_State_ChiJob002_03_Pristine, Vz_State_ChiJob002_04_Pristine, Vz_State_ChiJob002_05_Pristine,
Vz_State_ChiJob002_01_Staging, Vz_State_ChiJob002_02_Staging, Vz_State_ChiJob002_03_Staging,
Vz_State_ChiJob002_04_Staging, Vz_State_ChiJob002_05_Staging, Vz_State_ChiJob005_A_Pristine,
Vz_State_ChiJob005_B_Pristine, Vz_State_ChiJob005_C_Pristine, Vz_State_ChiJob005_D_Pristine,
Vz_State_ChiJob005_E_Pristine, Vz_State_ChiJob005_F_Pristine, Vz_State_ChiJob005_G_Pristine,
Vz_State_ChiJob006_A_Pristine, Vz_State_ChiJob006_B_Pristine, Vz_State_ChiJob006_C_Pristine,
Vz_State_ChiJob006_D_Pristine, Vz_State_ChiJob006_E_Pristine, Vz_State_ChiJob006_A_Staging,
Vz_State_ChiJob006_B_Staging, Vz_State_ChiJob006_C_Staging, Vz_State_ChiJob006_D_Staging,
Vz_State_ChiJob006_E_Staging, Vz_State_ChiJob009_A_Pristine, Vz_State_ChiJob009_A_Pristine_tg,
Vz_State_ChiJob009_B_Pristine, Vz_State_ChiJob009_B_Pristine_tg, Vz_State_ChiJob010_01_Pristine,
Vz_State_ChiJob010_02_Pristine, Vz_State_ChiJob010_04_Pristine, vz_state_guanare_act1,
vz_state_gua_upperclass_pristine, vz_state_gurcon001_pristine, vz_state_gurcon001_outpost_pristine,
vz_state_gurcon001_staging, vz_state_gurcon002_pristine, vz_state_GurHQ_act1,
Vz_State_GurJob002_01_Pristine, Vz_State_GurJob002_02_Pristine, Vz_State_GurJob002_03_Pristine,
Vz_State_GurJob002_04_Pristine, Vz_State_GurJob002_05_Pristine, Vz_State_GurJob002_01_Staging,
Vz_State_GurJob002_02_Staging, Vz_State_GurJob002_03_Staging, Vz_State_GurJob002_04_Staging,
Vz_State_GurJob002_05_Staging, vz_state_GurJob003_Pristine, Vz_State_GurJob003_Staging,
vz_state_GurJob005_Pristine, Vz_State_GurJob005_Staging, Vz_State_GurJob007_01, Vz_State_GurJob007_02,
Vz_State_GurJob007_03, vz_state_GurJob008_01_Pristine, Vz_State_GurJob008_01_Staging,
vz_state_GurJob008_02_Pristine, Vz_State_GurJob008_02_Staging, Vz_State_GurJob11_01, Vz_State_GurJob11_02,
Vz_State_GurJob11_03, Vz_State_GurJob11_04, Vz_State_GurJob11_05, Vz_State_GurJob11_06,
Vz_State_GurJob11_07, Vz_State_GurJob11_08, Vz_State_GurJob11_09, Vz_State_GurJob11_10,
Vz_State_GurJob012_01_Pristine, Vz_State_GurJob012_02_Pristine, Vz_State_GurJob012_03_Pristine,
Vz_State_GurJob012_04_Pristine, Vz_State_GurJob012_05_Pristine, Vz_State_GurJob012_01_Staging,
Vz_State_GurJob012_02_Staging, Vz_State_GurJob012_03_Staging, Vz_State_GurJob012_04_Staging,
Vz_State_GurJob012_05_Staging, vz_state_JetCon001_pristine, vz_state_jungle_mountain_act1,
vz_state_mar_altagracia_act1, vz_state_mar_big_lineregion, vz_state_mar_city_act1,
vz_state_mar_industrial_act1, vz_state_mar_outskirt_act1, vz_state_mar_village_act1,
vz_state_merida_act1, vz_state_merida_act1_helo, vz_state_merida_act1_staging,
vz_state_mer_big_lineregion, vz_state_mer_commercialpristine, vz_state_ocgate_dynamic,
vz_state_OilCon002_pristine, vz_state_OilCon021_staging, vz_state_OilJob001_Pristine,
vz_state_OilJob001_Staging, vz_state_OilJob002_Pristine, vz_state_OilJob002_Staging,
vz_state_OilJob005_Pristine, vz_state_OilJob005_Staging, Vz_State_OilJob008_A_Pristine,
Vz_State_OilJob008_A_Staging, Vz_State_OilJob008_B_Pristine, Vz_State_OilJob008_B_Staging,
Vz_State_OilJob008_C_Pristine, Vz_State_OilJob008_C_Staging, Vz_State_OilJob008_D_Pristine,
Vz_State_OilJob008_D_Staging, Vz_State_OilJob008_E_Pristine, Vz_State_OilJob008_E_Staging,
Vz_State_OilJob008_F_Pristine, Vz_State_OilJob008_F_Staging, Vz_State_OilJob008_G_Pristine,
Vz_State_OilJob008_G_Staging, Vz_State_OilJob008_H_Pristine, Vz_State_OilJob008_H_Staging,
Vz_State_OilJob008_I_Pristine, Vz_State_OilJob008_J_Pristine, Vz_State_OilJob008_J_Staging,
Vz_State_OilJob008_k_Pristine, Vz_State_OilJob008_k_Staging, Vz_State_OilJob008_l_Pristine,
Vz_State_OilJob008_l_Staging, Vz_State_OilJob008_m_Pristine, Vz_State_OilJob008_m_Staging,
Vz_State_OilJob011_01_Pristine, Vz_State_OilJob011_02_Pristine, Vz_State_OilJob011_03_Pristine,
Vz_State_OilJob011_04_Pristine, Vz_State_OilJob011_05_Pristine, Vz_State_OilJob011_01_Staging,
Vz_State_OilJob011_02_Staging, Vz_State_OilJob011_03_Staging, Vz_State_OilJob011_04_Staging,
Vz_State_OilJob011_05_Staging, Vz_State_OilJob012_01_Pristine, Vz_State_OilJob012_02_Pristine,
Vz_State_OilJob012_03_Pristine, Vz_State_OilJob012_04_Pristine, Vz_State_OilJob012_05_Pristine,
Vz_State_OilJob012_01_Staging, Vz_State_OilJob012_02_Staging, Vz_State_OilJob012_03_Staging,
Vz_State_OilJob012_04_Staging, Vz_State_OilJob012_05_Staging, vz_State_PirCon004_Pristine,
vz_state_PirJob002_01_Pristine, Vz_State_PirJob002_01_Staging, vz_state_PirJob002_02_Pristine,
Vz_State_PirJob002_02_Staging, vz_state_PirJob002_03_Pristine, Vz_State_PirJob002_03_Staging,
Vz_State_PirJob007_A_Pristine, Vz_State_PirJob007_B_Pristine, Vz_State_PirJob007_C_Pristine,
Vz_State_PirJob007_E_Pristine, Vz_State_PirJob007_F_Pristine, Vz_State_PirJob007_G_Pristine,
Vz_State_PirJob007_A_Staging, Vz_State_PirJob007_B_Staging, Vz_State_PirJob007_C_Staging,
Vz_State_PirJob007_E_Staging, Vz_State_PirJob007_F_Staging, Vz_State_PirJob007_G_Staging,
Vz_State_PirJob012_02_Pristine, Vz_State_PirJob012_05_Pristine, Vz_State_PirJob012_06_Pristine,
Vz_State_PirJob012_07_Pristine, Vz_State_PirJob012_08_Pristine, Vz_State_PirJob012_09_Pristine,
Vz_State_PirJob012_10_Pristine, Vz_State_PirJob012_05_Staging, Vz_State_PirJob012_06_Staging,
Vz_State_PirJob012_07_Staging, Vz_State_PirJob012_08_Staging, Vz_State_PirJob012_09_Staging,
Vz_State_PirJob012_10_Staging, VZ_State_Pmc_Pristine, vz_state_sol_base_pristine, vz_state_sol_bunker,
vz_state_staging_OilDepot, vz_state_staging_OilHQ, vz_state_staging_PirHQ, vz_state_VzaCon001_Pristine,
vz_state_vza_con001, vz_state_gurcon001_fortress, vz_state_PMC, vz_state_cashpickups,
vz_state_munitions_freeplay
```

</details>

### Why this matters for modding

- **This is a complete, safe candidate list** for any tool that wants to iterate over "every layer known
  to exist" without needing to enumerate them at runtime (no such enumeration function exists anywhere in
  `Pg` or in this module) or intercept the boot sequence to discover them.
- **It directly explains the `Pg.Spawn` gap** documented in the [World Inspector deep dive](../deep-dives/world-inspector):
  the overwhelming majority of what's "in the world" the moment a level finishes loading came from these
  ~416 layer loads, not from any runtime spawn call. Hooking `Pg.Spawn` alone was never going to catch it,
  because from Lua's perspective this content was never "spawned" — just loaded as part of a layer.
- **It still doesn't explain ambient traffic/pedestrians.** Nothing in either list reads as a
  population/traffic/density system by name — that remains a genuinely open question.

## Notes for modders

- **`MarkForAddition`/`MarkForRemoval` alone do nothing — you need `ProcessMarkedLayers()` too, or just call
  `Add`/`Remove` directly instead.** The most common mistake this module invites: staging a change and never
  seeing it, because nothing triggered the commit phase. If you want an immediate, reliable effect from your
  own script, prefer `MrxLayerManager.Add({"layer_name"})`/`Remove(...)` directly.
- **Nonexistent layer names are always safe to pass** — `Pg.AssetExists` culls them quietly (logged, not an
  error), confirmed both by reading `_AddRequest` and by live testing during the Custom Contract investigation.
  Feel free to probe a guessed layer name without fear of crashing anything.
- **`Remove`'s loading-screen argument is silently broken** — see the confirmed bug above. Don't rely on it.
- **Forced layer changes don't persist across a save/reload on their own** — `SaveSingleton` only persists
  whatever's already tracked in this module's own state; a mod that force-adds a layer needs to reapply that
  from `OnLoad` every level load, same as any other live, non-save-data mod state on this wiki.
- **The mission-ID suffix convention (`_pristine`/`_staging`/`_defenses`/`_destroyed`/`_captured`) is regular
  enough to guess.** For any mission ID not already in the catalog above, grepping that mission's own
  `vz/<id>.lua` file for `vz_state`/`Vz_State` will very likely turn up its own small state-layer family
  directly, following the same pattern.
- **The `_post` layers are the most interesting lead for "permanently change the world state."** Only three
  exist (`JetCon001`, `OilCon001`, `VzaCon001`) — each represents a lasting change tied to one specific
  mission's completion, as opposed to the broader region `act1`/`act2`/`act3` progression. Worth live-testing
  by force-adding one (e.g. `MrxLayerManager.Add({"vz_state_oilcon001_post"})`) to see what it actually
  contains, since layer *contents* are compiled binary and invisible from Lua source alone.
