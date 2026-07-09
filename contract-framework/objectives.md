---
title: Objectives Reference
parent: Contract Framework
nav_order: 2
---

# Objectives Reference

> **Status: new, in development.** Read directly from `ContractFramework.lua` (read in full). Behavior
> described here is what the code currently does, not yet independently confirmed by extended live play.
> A block of these is explicitly marked in the source as **draft, untested** (noted per-type below).

## Sequential vs. parallel

`def.objectives` is a plain array built from the builder functions below. By default (`def.mode` unset or
`"sequential"`) they run **one at a time, in order** — the next one only starts once the previous calls
its completion. Set `def.mode = "parallel"` to run the whole list **at once** instead; the contract
completes once every non-`optional` objective in the list has completed, and fails the instant any
non-`optional` one fails. Mark an objective `optional = true` (every builder accepts it) to make it not
block completion either way — pair it with `bonus = <cash>` to pay out extra reward only if it happens to
finish successfully.

Nesting is free: `Contract.Group{ mode = "parallel", objectives = { ... } }` runs its own nested list in
whichever mode you give it, and can itself sit inside a sequential (or parallel) outer list — the same
runner function powers both the top-level list and every `Group`.

## Where an objective's targets come from

Three ways to source the guids an objective acts on, all supported (in different combinations) by the
`destroy`/`chase` builders and several others:

- **Spawned** (`spawns = { {"TemplateName", x, y, z, yaw}, ... }`) — the framework spawns them itself via
  `Pg.Spawn` and tracks them for cleanup when the objective (or the whole contract) ends.
- **Named** (`objects = { "PlacedObjectName", ... }`) — resolved via `Pg.GetGuidByName` against objects
  already placed in the level. **Not** tracked for removal — they're real level content, not the
  framework's to delete.
- **Live-queried** (`where = { area = {x,y,z,r}, kind = "humans"|"vehicles"|"buildings", faction = "...",
  label = "..." }`) — a live `Pg.FastCollect*` sweep of the given area, optionally filtered by faction/label
  (checked via `Object.HasLabel`). Whatever matches *right now* becomes the target set.

## The 15 objective types

| Builder | Objective type | Completes when |
|---|---|---|
| `Contract.Destroy{desc, spawns, objects, where, quota}` | `destroy` | `quota` (default: all) of the sourced targets are killed. |
| `Contract.Reach{desc, at, radius}` | `reach` | The player enters a radius around a point (marked as a "destination" on radar/PDA/world). |
| `Contract.Defend{desc, time, target}` | `defend` | `time` seconds elapse; fails immediately if the named `target` dies first. |
| `Contract.Collect{desc, items, quota, radius}` | `collect` | The player walks within `radius` of `quota` (default: all) spawned pickup items. |
| `Contract.Escort{desc, spawn, to, radius}` | `escort` | A spawned unit/vehicle reaches the `to` zone; fails if it dies first. Its actual movement/follow behavior is the modder's responsibility (a drivable vehicle, or a unit with its own follow AI). |
| `Contract.Enter{desc, target, spawn, seat}` | `enter` | The player boards the named or spawned vehicle's `seat` (default `"d"`, the driver's seat). |
| `Contract.Hold{desc, at, radius, time}` | `hold` | The player accumulates `time` seconds *total* inside the zone (capture-point style — leaving and returning keeps prior progress). |
| `Contract.Group{desc, mode, objectives}` | `group` | Its own nested objective list resolves, in `mode` ("sequential"/"parallel") — full tree nesting for free. |
| `Contract.Interact{desc, target, spawn, at, radius, time}` | `interact` | The player stays within `radius` of a target/point for `time` seconds (default 0 = instant on approach) — one primitive standing in for talk/plant/hack/sabotage/free-prisoner, the flavor being just the `desc` text. Leaving the radius resets progress (must "stay" to use it). |
| `Contract.Verify{desc, target, spawn, capture, captureHealth, radius}` | `verify` | An HVT bounty: completes on kill, or (if `capture = true`) when the player is within `radius` while the target's health is at or below `captureHealth` — an approximation, since real subdue state isn't reachable from Lua yet. |
| `Contract.Extract{desc, at, radius, boardTime, heli}` | `extract` | `boardTime <= 0` (default): reaching the LZ *is* extraction, instantly. `boardTime > 0`: hold the LZ that many seconds (optionally spawning `heli` as a visual); leaving resets progress. |
| `Contract.Race{desc, checkpoints, radius, time}` | `race` | Every checkpoint in `checkpoints` (an ordered list of points) is reached in order; only the *current* checkpoint is ever marked. Reports the run time on completion. |
| `Contract.Survive{desc, time, target}` | `survive` | `time` seconds elapse (drawing its own countdown on the HUD); fails immediately if the optional protected `target` dies first. |
| `Contract.Chase{desc, spawns, objects, where, escapeAt, escapeRadius, time, haste}` | `chase` | The **inverse** of `destroy` — sourced targets are ordered to flee toward `escapeAt` (`Ai.SetHaste` applied); completes when all are killed, **fails** the instant any one reaches the escape zone, and can also time out via `time`. |
| `Contract.Protect{desc, target, spawn}` | `protect` | *(fail-condition only — put it in `def.fail`, not `def.objectives`.)* Never completes anything; only ever fails the whole contract if the named/spawned target dies. |
| `Contract.StayInArea{desc, at, radius}` | `stay` | *(fail-condition only — put it in `def.fail`.)* Fails the contract if the player ever leaves the radius. |

Everything from `collect` through `race` above (barring the always-safe `group`) is explicitly marked in
`ContractFramework.lua`'s own source as a **draft objective type — untested, but built to the same shape**
as the earlier, more battle-tested ones (`destroy`/`reach`/`defend`/`chase`). Same API, just newer.

## Marking objectives in the world

Every objective that has a physical target or location gets marked on **three surfaces at once**, the same
way the base game's own missions do: the round radar (`Hud.Radar:AddObjective`), the PDA map
(`Pda.Map:AddBlip`), and an in-world marker (`Marker.AddBlip`). Five icon kinds exist —
`destroy`/`verify`/`defend`/`action`/`destination` — each pulled straight from the base game's own
`MrxTaskObjective` icon family, so a custom contract's markers look identical to a shipped mission's.

## Example: a nested, mixed-mode objective list

```lua
Contract.Register{
    id = "warehouse_raid", title = "Warehouse Raid",
    objectives = {
        Contract.Group{
            desc = "Clear the warehouse",
            mode = "parallel",
            objectives = {
                Contract.Destroy{ desc = "Destroy the guards", where = { area = { 100, 0, 200, 40 }, kind = "humans" } },
                Contract.Interact{ desc = "Plant the charge", at = { 105, 0, 210 }, time = 5, optional = true, bonus = 10000 },
            },
        },
        Contract.Extract{ desc = "Get to the LZ", at = { 40, 0, 40 }, boardTime = 5 },
    },
}
```

The outer list is sequential (default): the whole `Group` must resolve before `Extract` starts. Inside the
group, both children run in parallel — the guards must all die (required), while planting the charge is
optional and pays a bonus if it happens.

## See also

- [Contract.Register & Lifecycle](register-and-lifecycle) — how `def.objectives` fits into the rest of a
  contract definition, and the runner that drives sequential/parallel execution.
- [Support Effects & Triggers](support-effects-and-triggers) — `def.fail` conditions run through the same
  trigger machinery support call-ins use.
