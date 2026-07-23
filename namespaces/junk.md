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
| `ActivateAlarm` | `Junk.ActivateAlarm(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed one-directional counterpart to `ToggleAlarm`/`AlarmActivated` in `resident/alarm.lua`, but that module calls its own local `AlarmActivated`/`AlarmDeactivated` functions directly rather than this one, so the relationship is inferred from naming only. Independently corroborated on 2026-07-22 as a genuine native binding: a static dump of the compiled engine's `luaL_Reg` registration table shows it really is a member of the table backing `Junk` (address `0x00799E28`) — a second, independent confirmation method beyond the live `pairs()` dump, but one that only proves table membership, not argument shape; still name-only for calling purposes. |
| `SpawnHomingProjectile` | `Junk.SpawnHomingProjectile(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. **Likely (but unconfirmed) candidate for the real mechanism behind [`AntiAir`](../resident/antiair)'s homing missiles**: `antiair.lua` never calls [`Airstrike`](airstrike) (the confirmed mechanism every other scripted ordnance in the corpus uses) anywhere — its `_HomingLaunched` only reacts to an already-fired missile for radar-blip bookkeeping. This function's name is the closest naming match found for what must be firing those missiles instead, but that's inference from the name, not a confirmed call chain. Independently corroborated on 2026-07-22 as a genuine native binding via the same static `luaL_Reg` registration-table audit noted on `ActivateAlarm` above (same table, address `0x00799E28`) — membership only, no argument shape recovered. |
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
| `SpawnWithModel` | `Junk.SpawnWithModel(name1, name2, x, y, z)` (**DISASM-SOLID**) | No call sites in the decompiled corpus, but unlike the rest of this table it's been fully investigated rather than left as a bare name — chased as a possible additive-model-spawning route and confirmed a dead end. See **Junk.SpawnWithModel — a fully investigated dead end** below for the complete writeup. |

### Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `FormatTime` | `s = Junk.FormatTime(nTime [, bUseTenths])` | Confirmed in `resident/mrxtimer.lua` as `Junk.FormatTime(self._iCurrentTime, self.bUseTenths)` and in `resident/mrxstatsmanager.lua` as `Junk.FormatTime(nTime)` (single-argument form) feeding directly into a displayed stats string. Formats a numeric time value into a display string; the second boolean argument appears to control whether tenths-of-a-second are included. |
| `DescribeGuid` | `s = Junk.DescribeGuid(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. The name strongly suggests a debug helper that returns a human-readable description of a `uGuid` (type/name/state), which would be directly useful for this project's ongoing GUID/object-identification work — but this is unconfirmed and untested; treat as a lead to test live, not a documented API. |
| `CreateRegion` | `Junk.CreateRegion(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Independently corroborated on 2026-07-22 as a genuine native binding via the same static `luaL_Reg` registration-table audit noted on `ActivateAlarm`/`SpawnHomingProjectile` above (same table, address `0x00799E28`) — membership only, no argument shape recovered. |
| `GetModelBBoxExtents` | `ex, ey, ez = Junk.GetModelBBoxExtents(uGuid)` | **CONFIRMED LIVE** (2026-07-22, live-probed over lua-bridge's WebSocket transport against a running game) — a stronger confirmation tier than the rest of this table's "exists per live `pairs()` enumeration" entries, which confirm only the name. Takes a **`uGuid`**, not a name string — worth flagging plainly, since a model-lookup function like this is easy to assume wants a template/model name the way `Pg.Spawn` does; instead it wants the same object handle every `Object.*`/`Vehicle.*` call uses. Returns three numbers — the model's bounding-box extents along each axis. Real example from the probe: a boat measured `19.98, 18.74, 22.71`. Still no call sites in the decompiled corpus; this signature comes entirely from live probing, not source. |

## Junk.SpawnWithModel — a fully investigated dead end

`Junk.SpawnWithModel` doesn't get a one-line table entry above because it earned a full investigation
instead of one. A 2026-07-22 research pass chased it specifically as a possible way to spawn additive
models **without a guidmap entry** — a route around the same wall that blocks `Pg.Spawn` and everything
else on this wiki that needs a name the engine already recognizes. It surfaced by diffing a static dump
of all 973 registered `luaL_Reg` engine bindings against the decompiled Lua corpus to find functions that
are real but never called anywhere in it, then live-probing the survivors over lua-bridge's WebSocket
transport against a running game. The result is a dead end — but a completely characterized one, not an
abandoned lead.

### Signature — DISASM-SOLID

`SpawnWithModel(name1, name2, x, y, z)` — two name strings followed by three coordinate floats. This
comes from reading the disassembly, not a call site (there are none in the decompiled corpus to read
argument shape off of), because the engine inlines its own argument checks and never raises a Lua-level
`bad argument #N` error to reveal arity that way. A single-string call no-ops to `nil`: the second name is
required, not optional.

### The shared name registry — DISASM-SOLID architecture, LIVE-CONFIRMED results

`name1` and `name2` resolve through two *different* native functions — `name1` via a resolver at
`0x672f60`, `name2` via a separate one at `0x649180` — but both share the same critical section
(`0xedbaa4`), the same freelist global (`0xedbac0`), and the same pair of iterators
(`0x649a80`/`0x649b90`). That's one shared registry addressed by two entry points, not two independent
namespaces — recovered by reading the disassembly, not by probing.

That registry is confirmed **not** the same one `Pg.GetGuidByName` resolves against — its resolver sits at
a different address, `0x59ff50` — but live testing showed it answers to the **same template-name
namespace**: real spawn templates like `Veyron`, `L300`, and `Explosion (Grenade)` resolve to a guid
through it, exactly as they would through `Pg.GetGuidByName`. Outfit codes (`pmc_hum_*`) and raw
model-asset names (`global_deliverycrate`, model-hash userdata) both come back `nil`. So this isn't a back
door into some other, more permissive set of spawnable names — it's the exact same already-registered
template list, addressed from a second angle.

### What it actually builds — CONFIRMED LIVE

Called with a resolving name pair and real coordinates, `SpawnWithModel` genuinely does produce a valid
object at `(x, y, z)` with health. But its model bounding box measures roughly **1e-16** — checked with
`Junk.GetModelBBoxExtents` above — which is empty geometry in every practical sense: an invisible
placeholder, not a visible model. Its visible-mesh path is inactive in retail; it lives in the dev `Junk`
table for a reason. Even setting the registry question aside entirely, this alone is why it was never
going to be a viable additive-spawn route: a successful call still renders nothing.

### Crash-safety — CONFIRMED LIVE, and the wider `Pg.Spawn` gotcha

The one point genuinely in `SpawnWithModel`'s favor: **it's crash-safe on any name.** Feed it garbage for
`name1`/`name2` and it resolves cleanly to `nil` instead of taking the game down — its disassembly shows a
clean not-found return path, and live testing with non-resolving names confirms the game keeps running.

That is *not* how `Pg.Spawn` behaves, and it's worth flagging as a general rule independent of
`SpawnWithModel` entirely: **`Pg.Spawn` (and other name-resolution calls, such as
`SetOutfit`/`SetModelName`) hard-crash the game on an unresolved name, with no soft failure.** This is
confirmed live — the game CTD'd outright on `Pg.Spawn('Austin (CIV)', ...)`, a name that simply didn't
resolve.
There's no `pcall` to catch here; it's a hard crash to desktop, not a Lua-level error. **Always gate any
name-based spawn behind `Pg.GetGuidByName(name) ~= nil` first** — see [`Pg`'s Spawning
section](pg#spawning) and [Object Lookup by Name section](pg#object-lookup-by-name). `SpawnWithModel`'s
crash-safety above is a concrete, useful illustration of the contrast: given the exact same kind of
unresolved name, `Pg.Spawn` crashes and `SpawnWithModel` doesn't — even though `SpawnWithModel` is a dead
end for the reasons above, "doesn't crash on bad input" is a genuinely better property than the thing
every other spawn path on this wiki has to be gated so carefully around.

### Verdict: closed from both directions, with one documented next step

`SpawnWithModel` needs an already-registered name — the same guidmap wall as everything else on this wiki
— **and** renders nothing even on success. As an additive-spawning route it's closed off both ways at
once: no new names to reach, and nothing to see if you somehow found one.

The only remaining way to learn what *could* populate that `0x672f60`/`0x649180` registry — whether
anything beyond the standard template list is ever added to it, and by what mechanism — is **runtime
instrumentation**: an ASI hook on `0x672f60`, logging every name it receives live and whether it resolves.
Both the resolver and `SpawnWithModel`'s own constructor (`0x674660`) are SecuROM-obfuscated, so static
reverse-engineering stops here — there's nothing further to recover by reading more disassembly. **This
hasn't been done.** It's a documented next step for whoever picks this thread up, not a claim that the
registry is somehow permanently unreachable.

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
- **Spawn/name-resolution crash gotcha, live-confirmed:** `Pg.Spawn` (and other name-resolving calls like
  `SetOutfit`/`SetModelName`) hard-crash the game outright on an unresolved name — no `pcall`-catchable
  error, just a crash to desktop. Always gate behind `Pg.GetGuidByName(name) ~= nil` first — see [`Pg`'s
  Spawning section](pg#spawning). See **Junk.SpawnWithModel — a fully investigated dead end** above for the
  concrete contrast: `SpawnWithModel` resolves that exact same kind of unresolved-name failure to a clean
  `nil` instead of crashing.
