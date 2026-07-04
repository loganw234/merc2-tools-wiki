---
title: Junk
parent: Engine Namespaces
nav_order: 16
---

# Junk

## Overview

`Junk` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it, no
`import()` call needed, and it's always globally available to every script. The name and the bulk of its
contents (`Dump*`, `Search`, `LoadScript`, `InstallToHDD`, `IsInstallable`, `UseExistingInstall`) suggest this
is a developer/debug-tools grab-bag rather than a coherent gameplay API — plausibly leftover dev-console or
debug-menu tooling that shipped in the final build alongside a handful of genuinely gameplay-relevant
functions (alarm activation, homing projectiles, AI path visualization). That reading is inference from the
namespace's name and contents, not a confirmed design intent.

## Provenance

This page's function list comes from a live `pairs(Junk)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 24 function
names below is complete and authoritative: every one of them really exists on the namespace. It does **not**
mean every entry is documented with confirmed arguments. Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in
that corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed.

## Functions

### Alarms & Gameplay

| Function | Signature (best-known) | Notes |
|---|---|---|
| `ToggleAlarm` | `Junk.ToggleAlarm(uGuid)` | Confirmed in `resident/alarm.lua` — wired up as the callback for the alarm's context-action event: `Event.Create(Event.ContextAction, {Player.GetAnyCharacter(), uGuid}, Junk.ToggleAlarm, {uGuid})`. This is the function that actually runs when a player interacts with an alarm object; the rest of that module (`AlarmActivated`/`AlarmDeactivated`) appears to be the surrounding state machine it toggles between. Genuinely gameplay-relevant despite the namespace name. |
| `ActivateAlarm` | `Junk.ActivateAlarm(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed one-directional counterpart to `ToggleAlarm`/`AlarmActivated` in `resident/alarm.lua`, but that module calls its own local `AlarmActivated`/`AlarmDeactivated` functions directly rather than this one, so the relationship is inferred from naming only. |
| `SpawnHomingProjectile` | `Junk.SpawnHomingProjectile(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. **Likely (but unconfirmed) candidate for the real mechanism behind [`AntiAir`](../resident/antiair)'s homing missiles**: `antiair.lua` never calls [`Airstrike`](airstrike) (the confirmed mechanism every other scripted ordnance in the corpus uses) anywhere — its `_HomingLaunched` only reacts to an already-fired missile for radar-blip bookkeeping. This function's name is the closest naming match found for what must be firing those missiles instead, but that's inference from the name, not a confirmed call chain. |
| `DrawPath` | `Junk.DrawPath(uPathGuid)` | Confirmed in `vz/meccon001.lua`, called as `Junk.DrawPath(uPath)` where `uPath` is a path-object GUID resolved via `Pg.GetGuidByName(sPathName)`, immediately before handing that same GUID to `Ai.Goal({Goal = "PathMove", Target = uPath, ...})`. Reads as a debug/visualization aid for AI path-following (e.g. drawing the path an AI driver is about to follow), not something with a mechanical gameplay effect. |
| `Subdue` | `Junk.Subdue(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Debug / Dev Tools

| Function | Signature (best-known) | Notes |
|---|---|---|
| `DumpMemory` | `Junk.DumpMemory(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DumpStats` | `Junk.DumpStats(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DumpAssets` | `Junk.DumpAssets(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DumpAssetsDiff` | `Junk.DumpAssetsDiff(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DumpAssetMemory` | `Junk.DumpAssetMemory(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DumpTextures` | `Junk.DumpTextures(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `InstallToHDD` | `Junk.InstallToHDD()` | Confirmed in `resident/mrxguishell.lua` (and its duplicate under `shell/`), called with no arguments from an install-options menu callback: `InstallCallback(iOption, oShell)` calls `Junk.InstallToHDD()` when `iOption == 1`. Console/disc-install tooling, not gameplay-relevant. |
| `UseExistingInstall` | `Junk.UseExistingInstall()` | Confirmed in the same `mrxguishell.lua` callback, called with no arguments when `iOption == 2` (the "Use Existing HDD Install" menu option). |
| `IsInstallable` | `b = Junk.IsInstallable()` | Confirmed in `mrxguishell.lua`, guarded defensively as `if Junk.IsInstallable and Junk.IsInstallable() then` — called with no arguments, returns a value used in a boolean context. |
| `LoadScript` | `Junk.LoadScript(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `LoadFunctions` | `Junk.LoadFunctions(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `LoadData` | `Junk.LoadData(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Search` | `Junk.Search(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetQGrey` | `Junk.SetQGrey(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `FormatTime` | `s = Junk.FormatTime(nTime [, bUseTenths])` | Confirmed in `resident/mrxtimer.lua` as `Junk.FormatTime(self._iCurrentTime, self.bUseTenths)` and in `resident/mrxstatsmanager.lua` as `Junk.FormatTime(nTime)` (single-argument form) feeding directly into a displayed stats string. Formats a numeric time value into a display string; the second boolean argument appears to control whether tenths-of-a-second are included. |
| `DescribeGuid` | `s = Junk.DescribeGuid(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. The name strongly suggests a debug helper that returns a human-readable description of a `uGuid` (type/name/state), which would be directly useful for this project's ongoing GUID/object-identification work — but this is unconfirmed and untested; treat as a lead to test live, not a documented API. |
| `CreateRegion` | `Junk.CreateRegion(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetModelBBoxExtents` | `Junk.GetModelBBoxExtents(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

## Notes for modders

- `ToggleAlarm` is confirmed as genuinely gameplay-relevant: it's the live context-action callback wired up in
  `resident/alarm.lua` for interacting with alarm objects. `ActivateAlarm`, by contrast, has no confirmed call
  sites — the alarm module's own activation/deactivation logic (`AlarmActivated`/`AlarmDeactivated`) is
  implemented locally in that file rather than delegating to `Junk.ActivateAlarm`, so don't assume the two
  `Junk` alarm functions are interchangeable.
- `DescribeGuid` has no confirmed call sites in the decompiled corpus, but its name makes it a promising
  candidate to test live for GUID/object-identification purposes (e.g. dumping a human-readable summary of an
  unknown `uGuid` at the console). Flagged here as unconfirmed but worth live-testing, not as documented
  behavior.
- The `Dump*`/`Install*`/`Load*` functions read as internal dev-console and disc/HDD-install tooling with
  little to no gameplay purpose — `InstallToHDD`, `UseExistingInstall`, and `IsInstallable` are confirmed
  call sites, but all three are console-install menu plumbing (`resident/mrxguishell.lua`), not anything a
  gameplay mod would call.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Junk)` dump) but their
  argument shape is a guess based on naming convention only — don't build mods around them without testing
  in-game first.
