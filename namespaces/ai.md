---
title: Ai
parent: Engine Namespaces
nav_order: 6
---

# Ai

## Overview

`Ai` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it, no
`import()` call needed, and it's always globally available to every script. Its functions govern NPC
behavior: registering and unregistering "subjects" (NPCs the AI system tracks), the goal/planning system
that drives moment-to-moment AI actions (`Goal`, `Plan*`), faction relations at the primitive level
(`GetRelation`/`SetRelation`/`ChangeRelation`), road/pedestrian traffic density and spawn-list management,
and squad- and vehicle-level behaviors (`Squad`, helicopter drop-zone/land/takeoff logic, `Anchor`,
`Water`).

## Provenance

This page's function list comes from a live `pairs(Ai)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 66
function names below is complete and authoritative: every one of them really exists on the namespace. It
does **not** mean every entry is documented with confirmed arguments. Where a function is actually called
somewhere in the ~230 decompiled `.lua` scripts, we can show a real argument pattern (usually a single
options table, sometimes positional `uGuid` arguments). Where it isn't called anywhere in that corpus, we
only know the name — arguments, return values, and behavior for those are unconfirmed and not guessed
beyond conventions that hold across the rest of this namespace.

Several `Ai.*` calls are wrapped by `resident/mrxai.lua`, a thin resident module that gates `Ai.Goal`,
`Ai.DefaultGoal`, `Ai.RemoveGoal`, `Ai.Deploy`, and `Ai.Role` behind an `Event.ObjectHibernation`/`"awake"`
check (i.e. it defers the raw `Ai.*` call until the target object is confirmed awake). That module is the
best available reference for how these table-shaped calls are normally issued in production code.

## Functions

### Subjects & State

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AddSubject` | `Ai.AddSubject(uGuid)` | Confirmed in `resident/mrxplayer.lua`, e.g. `Ai.AddSubject(uCharacterGuid)` — called when a player's character joins, registering it with the AI subject system. |
| `RemoveSubject` | `Ai.RemoveSubject(uGuid)` | Confirmed in `resident/mrxplayer.lua` as the counterpart to `AddSubject`, e.g. `Ai.RemoveSubject(uCharacterGuid)`. |
| `RemoveAllSubjects` | `Ai.RemoveAllSubjects()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetSubjectData` | `Ai.GetSubjectData(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetState` | `b = Ai.GetState({AIGuid = uGuid, State = sStateName})` | Confirmed in `resident/outpost.lua`, e.g. `Ai.GetState({AIGuid = uRusher, State = "NoCapture"})` — table-shaped call, mirrors `SetState`'s argument shape. |
| `SetState` | `Ai.SetState({AIGuid = uGuid, State = sStateName, Value = ...})` | Confirmed across several `resident/` and `vz/` scripts, e.g. `Ai.SetState({AIGuid = uGuid, State = "Pacifist", Value = true})` in `resident/mrxtaskobjectiveverify.lua`. |
| `Enable` | `Ai.Enable(uGuid, bEnabled)` | Confirmed in `resident/mrxactionhijack.lua` and `resident/mrxutil.lua`, e.g. `Ai.Enable(self._hijackee, false)` / `Ai.Enable(uGuid, true)` — toggles whether the AI system drives a given object at all. |
| `LivingWorld` | `Ai.LivingWorld({AIGuid = uGuid, Attrib = sAttribName, State = ...})` | Confirmed in `resident/mrxfollow.lua`, e.g. `Ai.LivingWorld({AIGuid = uGuid, Attrib = "LivingWorldBehaviour", State = false})` — disables the ambient "living world" behavior layer for a subject, typically before scripting custom behavior (e.g. `Follow`) on top. |
| `GetAttrib` | `Ai.GetAttrib(uGuid, sAttribName)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumably the getter counterpart of the `Attrib` field seen in `LivingWorld`, but that pairing is inferred from naming only. |
| `Temp` | `Ai.Temp(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments completely unconfirmed, including argument count. |

### Goals & Planning

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Goal` | `h = Ai.Goal({AIGuid = uGuid, Goal = sGoalName, Target = ..., Priority = sPriority, ...})` | Extremely common across `vz/` mission scripts and `resident/` modules — dozens of call sites. Table keys observed in real usage include `AIGuid`, `Goal` (e.g. `"PathMove"`), `Target`, `Priority` (`"lowPri"`, `"hiPri"`), `Mode` (`"Oneway"`), `Start` (`"Nearest"`), `Haste`, `Callback`, `CallbackData`. Returns a handle in several call sites (e.g. `local h = Ai.Goal(...)`, `self.curAiGoal = Ai.Goal(...)`) later passed to `RemoveGoal`. The exact set of valid `Goal` names and per-goal keys is not enumerated anywhere in the corpus — only the keys actually seen are confirmed. |
| `DefaultGoal` | `Ai.DefaultGoal(tParameters)` | No direct call sites in `vz`/`resident` mission scripts, but `resident/mrxai.lua` wraps it 1:1 with `Ai.Goal`'s calling convention (same `tParameters` table, same hibernation-gating pattern), strongly suggesting an identical table shape to `Goal`. Treat the table shape as inferred-by-analogy, not independently confirmed. |
| `RemoveGoal` | `Ai.RemoveGoal({AIGuid = uGuid, Handle = hHandle})` or `Ai.RemoveGoal(uGuid, hHandle)` | Confirmed in both shapes: table form is common (e.g. `Ai.RemoveGoal({AIGuid = uRocketMan, Handle = 0})` in `vz/allcon002.lua`), and a positional two-argument form appears in `resident/outpost.lua` (`Ai.RemoveGoal(uRusher, tRusherData.uMoveGoal)`) and `vz/meccon001.lua` (`Ai.RemoveGoal(self.curAiGoal)` — passing a stored handle value directly). Both forms coexist in the corpus; which one a given engine build actually expects is not resolvable from source alone. |
| `Plan` | `Ai.Plan(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `PlanClear` | `Ai.PlanClear(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `PlanIterate` | `Ai.PlanIterate(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `PlanSetConditions` | `Ai.PlanSetConditions(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `PlanSetGoal` | `Ai.PlanSetGoal(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Role` | `h = Ai.Role({AIGuid = uGuid, Role = sRoleName, ...})` | Confirmed across several `resident/` modules, e.g. `resident/mrxfollow.lua`: `Ai.Role({AIGuid = uGuid, Role = "Follow", Target = uTarget, MinDistance = 2, MaxDistance = kMaxFollowDistance, MoveDistance = 4, Priority = "hiPri", HardPriority = true, Callback = ..., CallbackData = {self}})` and `Ai.Role({AIGuid = uGuid, Role = "Idle", Priority = "hiPri", Callback = nil, CallbackData = nil})`. Returns a handle. A distinct concept from `Goal` — appears to assign a standing behavioral role (`"Follow"`, `"Idle"`) rather than a one-shot task. |
| `Deploy` | `Ai.Deploy({Vehicle = uGuid, Role = sRole, Force = bForce, ...})` | Confirmed in `vz/gurcon002.lua`: `Ai.Deploy({Vehicle = uHeli, Role = "Passenger", Force = true, MaintainRotorSpeed = true, Callback = ...})`. Also wrapped by `resident/mrxai.lua` with the same hibernation-gating pattern as `Goal`. Used for deploying/ejecting occupants from vehicles under AI control. |

### Faction Relations

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetRelation` | `n = Ai.GetRelation(uGuidA, uGuidB)` | **This is the literal primitive underneath `resident/mrxfactionmanager.lua`'s `GetRelation` wrapper** — see `resident/mrxfactionmanager.lua:517`: `return Ai.GetRelation(_tFactions[sSubjectAbbrev].uGuid, _tFactions[sObjectAbbrev].uGuid)`. Also called directly in several `vz/` and `resident/` scripts, e.g. `Ai.GetRelation(Pg.GetGuidByName(sFaction), Pg.GetGuidByName("PMC"))`. Takes two faction/subject `uGuid`s, returns a numeric relation value (`MrxFactionManager` treats this range as roughly -100 to 100). See the [MrxFactionManager](../resident/mrxfactionmanager) wiki page for the higher-level attitude/meter system built on top of this primitive — don't duplicate that logic here, use `Ai.GetRelation`/`Ai.SetRelation` directly only if you need to bypass `MrxFactionManager`'s bookkeeping (HUD meters, mutability checks, net sync). |
| `SetRelation` | `Ai.SetRelation(uGuidA, uGuidB, nRelation)` | **Also the literal primitive underneath `resident/mrxfactionmanager.lua`'s `SetRelation`** — see line 561: `Ai.SetRelation(_tFactions[sSubjectAbbrev].uGuid, _tFactions[sObjectAbbrev].uGuid, nRelation)`. Confirmed directly in many `vz/` mission scripts too, e.g. `Ai.SetRelation(GetGuidByName("China"), Pg.GetGuidByName("Civ_VIP_1"), 100)` and `Ai.SetRelation(Pg.GetGuidByName("VZ"), Pg.GetGuidByName("PMC"), -100)`. Same cross-link caveat as `GetRelation` applies — calling this directly skips `MrxFactionManager`'s HUD-meter and net-sync side effects. |
| `ChangeRelation` | `Ai.ChangeRelation(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Given the confirmed `GetRelation`/`SetRelation` pair, this is presumably a relative/delta adjustment rather than an absolute set, but that is a naming-based guess, not confirmed. |
| `SetAttitude` | `Ai.SetAttitude(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. `MrxFactionManager` implements its own attitude-label system (`GetAttitudeLevel`/`GetAttitudeLabel`) entirely on top of `Ai.GetRelation`/numeric thresholds, without calling `Ai.SetAttitude` anywhere in the corpus — so whether this function overlaps with or bypasses that resident-side system is unconfirmed. |
| `GetFeeling` | `n = Ai.GetFeeling(uGuidA, uGuidB)` | Confirmed in `resident/mrxfollow.lua` (`local aiFeeling = Ai.GetFeeling(uGuid, uTarget)`) and `vz/oilcon021.lua` (`Ai.GetFeeling(Pg.GetGuidByName("MailTalk"), Player.GetLocalCharacter())`). Returns a numeric value; `mrxfollow.lua` treats negative values as hostile (checks `aiFeeling < 0`). Appears to be a per-pair value distinct from faction-level `GetRelation`, possibly per-individual rather than per-faction, but that distinction is inferred from usage, not documented anywhere. |
| `SetFeeling` | `Ai.SetFeeling(uGuidA, uGuidB, nValue)` | Confirmed in `resident/mrxfollow.lua`: `Ai.SetFeeling(uGuid, uTarget, 100)`, used to neutralize hostility before starting a scripted "Follow" role. |
| `GetFactionGuid` | `uFactionGuid = Ai.GetFactionGuid(uGuid)` | Confirmed in `resident/factionzone.lua` (`oSelf.uFaction = Ai.GetFactionGuid(oSelf.uGuid)`) and `resident/outpost.lua` (`local uFaction = Ai.GetFactionGuid(uRusher)`) — resolves an individual subject's owning faction `uGuid`, for use with `GetRelation`/`SetRelation`/etc. |
| `AddInfraction` | `Ai.AddInfraction(uCharacterGuid, uFactionGuid, nAmount)` | Confirmed in several `resident/` modules, e.g. `Ai.AddInfraction(Player.GetPrimaryCharacter(), uFaction, 5)` and `Ai.AddInfraction(Player.GetLocalCharacter(), Pg.GetGuidByName("China"), 100)`. Adds to a running "infraction" tally against a faction, presumably feeding into relation decay — see `SetInfractionMultiplier` below. |
| `SetInfractionMultiplier` | `Ai.SetInfractionMultiplier(uFactionGuid, nMultiplier)` | Confirmed, e.g. `Ai.SetInfractionMultiplier(GetGuidByName("Guerilla"), 0)` / `(..., 1)` in `vz/gurcon002.lua`, and `Ai.SetInfractionMultiplier(Pg.GetGuidByName(sFactionTemplate), 0.2)` in `resident/mrxtaskcontract.lua`. Used to temporarily suppress (`0`) or restore (`1`) infraction accrual for a faction during scripted sequences, and to scale it down (e.g. `0.2`, `0.1`) for softer factions. |

### Traffic & Spawn Lists

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetRoadSpawning` | `Ai.SetRoadSpawning(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSidewalkSpawning` | `Ai.SetSidewalkSpawning(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetTrafficSpawning` | `Ai.SetTrafficSpawning(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetSpawnList` | `Ai.GetSpawnList(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSpawnList` | `Ai.SetSpawnList(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ResetAllSpawnLists` | `Ai.ResetAllSpawnLists()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ClearSpawnListChanges` | `Ai.ClearSpawnListChanges(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetSpawnListChangeInfo` | `Ai.GetSpawnListChangeInfo(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `TweakAttachedSpawners` | `Ai.TweakAttachedSpawners(uBuildingGuid, {SpawnerState = "on"/"off", SecondsPerCycle = n, SpawnList = sList, ...})` | Very common in `resident/dangerousbuilding.lua`, `resident/outpost.lua`, and several `vz/` mission scripts. Confirmed keys across call sites: `SpawnerState` (`"on"`/`"off"`), `SecondsPerCycle` (numeric spawn-cycle delay), `SpawnList` (string). Operates on all spawners attached to a given building/object `uGuid`. |
| `TweakAttachedSpawnersInGroup` | `Ai.TweakAttachedSpawnersInGroup(uBuildingGuid, sGroupName, {SpawnerState = ..., ...})` | Confirmed alongside `TweakAttachedSpawners` in the same modules, e.g. `Ai.TweakAttachedSpawnersInGroup(TallCommBuild, "Ground", {...})`, `Ai.TweakAttachedSpawnersInGroup(uGuid, "ground", {SpawnerState = "off"})`. Group names observed: `"Ground"`, `"Balcony"`, `"Rooftop"` — scopes the tweak to spawners tagged with that group instead of all spawners on the object. |
| `ShowObjectSpawners` | `Ai.ShowObjectSpawners(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumably a debug-visualization toggle given the name, but that is a guess. |
| `SetLaneActive` | `Ai.SetLaneActive(uRoadGuid, nLaneIndex, bActive)` | Confirmed, e.g. `Ai.SetLaneActive(Pg.GetGuidByName(road), 1, false)` in `vz/chicon003.lua` and `Ai.SetLaneActive(Pg.GetGuidByName("Road 0x000a7417"), 1, false)` in `vz/pmccon001.lua` — disables/enables a specific numbered lane on a road object for traffic spawning/routing. |
| `SetDriveThroughMassRatio` | `Ai.SetDriveThroughMassRatio(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `AddRoadException` | `Ai.AddRoadException(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RemoveRoadException` | `Ai.RemoveRoadException(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetExclusionZone` | `Ai.SetExclusionZone(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RemoveExclusionZone` | `Ai.RemoveExclusionZone()` | Confirmed called with zero arguments in `vz/gurcon002.lua` and `vz/oilcon001.lua` (`Ai.RemoveExclusionZone()`) — clears whatever exclusion zone is currently active; the counterpart `SetExclusionZone` has no call sites, so the zone's shape/parameters are unconfirmed. |

### Vehicle/Squad Behaviors

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Squad` | `t = Ai.Squad({SquadGuid = uSquad, Action = sAction, ...})` | Confirmed across `vz/oilcon001.lua` and `resident/mrxapcdrop.lua`. Observed `Action` value: `"GetUnits"` (e.g. `local tSquad = Ai.Squad({SquadGuid = uSquad, Action = "GetUnits"})`, returning what call sites treat as a table of unit guids). Other call sites build squads from scratch (e.g. `local tVZsquad = Ai.Squad({...})`) with additional unconfirmed keys — only `SquadGuid`/`Action`/`"GetUnits"` are solidly confirmed. |
| `Anchor` | `Ai.Anchor({AIGuid = uGuid, AnchorRadius = n, ...})` | Confirmed in `vz/allcon002.lua` and `vz/oilcon001.lua`/`vz/oilcon002.lua`, e.g. `Ai.Anchor({AIGuid = uRocketMan, AnchorRadius = 0})`. Pins a subject to its current position/area; `AnchorRadius = 0` appears to mean "don't wander at all." |
| `Water` | `Ai.Water(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `HeliDropZoneInfo` | `Ai.HeliDropZoneInfo(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `HeliLand` | `Ai.HeliLand(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `HeliTakeoff` | `Ai.HeliTakeoff(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `TestDropZone` | `b = Ai.TestDropZone({Callback = fCallback, Location = {nX, nY, nZ}, InnerRadius = n, InnerHeightTolerance = n, OuterRadius = n, OuterHeightTolerance = n, HeightMax = n, SearchRadius = n, Water = bAllowWater})` | Confirmed identically across `resident/mrxgunship.lua`, `resident/mrxsupportdesignator.lua`, `resident/mrxtankbuster.lua`, and `resident/pursuitcopter.lua` — all use the same full table shape shown here. Returns a boolean; `false` is treated by callers as "no valid landing spot found" (`if not bDropZoneAdded then fCallback(false, "noland") end`). The best-documented table-shaped call on this entire namespace. |
| `Deliver` | `Ai.Deliver(uDriverGuid, nX, nY, nZ, nDropHeight, bCareless)` | Confirmed in `resident/mrxcopterdrop.lua` and `resident/mrxsupportdelivery.lua`, e.g. `Ai.Deliver(Vehicle.GetDriver(uHeli), nDesX, nDesY, nDesZ, 0.5, bCareless)` — commands a helicopter's AI driver to cargo-drop at a coordinate, with a drop-height parameter and a "careless" boolean (likely relaxes precision/safety checks). |
| `SetHaste` | `Ai.SetHaste(uGuid, nHaste)` | Confirmed repeatedly, e.g. `Ai.SetHaste(uBoatCapn, 1)`, `Ai.SetHaste(uDriver, iCurSpeed * 0.5)`, `Ai.SetHaste(uCartelDriver, 1)` — a numeric multiplier controlling how urgently/fast a driven subject moves; `1` appears to be normal/default speed. |
| `SetPriorityTarget` | `Ai.SetPriorityTarget(uGuid)` | Confirmed in `resident/mrxsupport.lua` (`Ai.SetPriorityTarget(uHeli)`) and `resident/outpost.lua` (`Ai.SetPriorityTarget(uRunnerGuid)`) — marks a subject as the priority target for hostile AI, single `uGuid` argument. |
| `SetFacing` | `Ai.SetFacing(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `EveryoneOut` | `Ai.EveryoneOut(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Name suggests forcing all occupants out of a vehicle, analogous to `Object`/`Vehicle` seat functions, but that is a guess. |
| `GoIn` | `Ai.GoIn(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetPerceivability` | `Ai.GetPerceivability(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetPerceivability` | `Ai.SetPerceivability(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ThreatPerception` | `Ai.ThreatPerception(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Admire` | `Ai.Admire(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Rest` | `Ai.Rest(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Talk` | `Ai.Talk(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Feed` | `Ai.Feed(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

## Notes for modders

- The single biggest pattern on this namespace is the **options-table call convention**: `Goal`, `Role`,
  `Deploy`, `SetState`, `GetState`, `LivingWorld`, `Squad`, `Anchor`, and `TestDropZone` all take one Lua
  table as their sole argument, keyed by field names like `AIGuid`, `Target`, `Priority`, `Callback`. There
  is no in-corpus enumeration of every valid key for every goal/role name — only the keys actually observed
  at real call sites are confirmed here. Don't assume a key is invalid just because it isn't listed; assume
  it's merely untested.
- `Ai.GetRelation`/`Ai.SetRelation` are confirmed as the literal primitives underneath
  [`MrxFactionManager`](../resident/mrxfactionmanager)'s `GetRelation`/`SetRelation` wrappers (see
  `resident/mrxfactionmanager.lua` lines 517 and 561). If you need faction-relation changes to show up
  correctly in the HUD meter and stay synced over the network, go through `MrxFactionManager`, not `Ai`
  directly — calling `Ai.SetRelation` directly bypasses `MrxFactionManager`'s mutability checks
  (`IsAttitudeMutable`) and its `Hud.FactionDisplay`/`Net.SendCustomEvent` side effects.
- `resident/mrxai.lua` is worth reading directly if you're scripting `Goal`/`DefaultGoal`/`RemoveGoal`/
  `Deploy`/`Role` calls against subjects that might be hibernating — it defers the raw `Ai.*` call behind
  an `Event.ObjectHibernation`/`"awake"` gate rather than calling straight through, which avoids issuing
  AI commands to an object the engine hasn't fully woken up yet.
- `RemoveGoal` is confirmed with two different call shapes in the corpus (a `{AIGuid=, Handle=}` table,
  and a positional `(uGuid, handle)` form). Both appear in real, presumably-shipped scripts — which one is
  "correct" for a given engine build isn't resolvable from source alone, so if one form doesn't work,
  try the other.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Ai)` dump) but their
  argument shape is a guess based on naming convention only, or entirely unknown — don't build mods around
  them without testing in-game first.
