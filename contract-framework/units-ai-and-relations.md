---
title: "Units, AI Orders & Relations"
parent: Contract Framework
nav_order: 4
---

# Units, AI Orders & Relations

> **Status: new, in development.** Read directly from `ContractFramework.lua` (read in full). Behavior
> described here is what the code currently does, not yet independently confirmed by extended live play.

Beyond objectives and triggered [support effects](support-effects-and-triggers), a contract can spawn its
own **grouped units** and command them directly with AI orders, and can temporarily override **faction
relations** for the contract's duration.

## Grouped spawns (`def.units`)

```lua
def.units = {
    { spawn = "Chinese Elite Soldier", x = 100, y = 0, z = 200, yaw = 90, group = "A" },
    { spawn = { "VZ Soldier", "VZ Officer" }, x = 105, y = 0, z = 200, group = "A", chance = 0.5 },
}
```

Spawned once, at contract start (before any AI orders can run, so there's always something to command),
and tracked for cleanup like every other framework-owned object. Fields:

- `spawn` (or `template`, or a bare first array entry) — a `Pg.Spawn` template string, **or a list of
  strings**, in which case one is picked at random each time.
- `x, y, z, yaw` (or `at = {x,y,z}`) — spawn position/facing.
- `group` — a string bucket name (default `"A"`). Every unit sharing a `group` ends up in
  `inst.groups["A"] = { guid, guid, ... }`, which is what `def.waypoints` and `def.relations` address.
- `chance` — optional 0..1 probability; omit for an always-spawns entry.

## AI orders per group

```lua
def.waypoints = {
    { id = "patrol1", group = "A", behavior = "patrol", points = { {100,0,200}, {150,0,200}, {150,0,250} } },
    { id = "attack1", group = "A", behavior = "attack", trigger = { ref = "alarm_tripped" } },
}
```

Each entry commands a whole `group` at once, built only on the same `Ai.Goal`/`Ai.Anchor` primitives the
shipped missions themselves use — nothing here is a new native capability, just a friendlier wrapper
around calls already confirmed elsewhere on this wiki. Orders arm through the **identical**
`trigger`/`fires`/gate system [Support Effects & Triggers](support-effects-and-triggers) describes — the
only difference from a support entry is the default: with no `trigger` given, an order fires after a short
`{ once = 1.5 }` delay instead of truly immediately, so vehicle crews have a moment to actually get seated
before being ordered to move.

| `behavior` | Does |
|---|---|
| `move` | `MoveToPos` to `at` — go there and stop. |
| `patrol` | Walks a route through `points` in order, looping unless `loop = false`. A single-point "patrol" quietly becomes a plain `move` instead of a wasteful one-point loop. |
| `defend` | Moves to `at`, then `Ai.Anchor`s the group to a spawned invisible anchor at that point with `radius` — holds the area, fighting anything that enters it. |
| `attack` | Hunts `target` (another group's first guid) if given, else the nearest player. |
| `hold` | `Ai.Anchor` with radius 0 + `Idle` goal — stand exactly where spawned, don't give chase. |
| `face` | Turns to face a point — no movement, useful for staging/cutscene-style framing. |
| `follow` | Re-issues a `MoveTo` toward `target` (or the nearest player) every `interval` seconds (default 4) — a simple tail, not a native follow behavior. |
| `flee` | Runs directly away from the nearest player, `distance` units (default 120), once. |
| `enter` | Boards a vehicle (`target` = another group/name) in `role` (default `"passenger"`). |
| `deploy` | A transport group disgorges its passengers (`Ai.Deploy`). |
| `animate` | Plays a canned action (`Human.DoAction`), e.g. `action = "Cower"` for a surrender pose. |

All of these accept `priority` (`"hi"`/`"med"`/`"lo"`, default varies by behavior) and most accept `speed`
(`Ai.SetHaste`). One quirk worth knowing: every order targets the **driver** of a vehicle guid, not the
vehicle hull itself (`Vehicle.GetDriver`, falling back to the guid itself for non-vehicles) — mirroring how
the shipped missions' own vehicle-chase logic works.

## Temporary faction stances (`def.relations`)

```lua
def.relations = {
    { "Allied", "PMC", "friend" },
    { "VZ", "PMC", "enemy" },
    { "VZ", "Allied", "enemy" },
}
```

Each entry is `{ factionA, factionB, stance }` (`"friend"`/`"ally"` = 100, `"neutral"` = 0,
`"enemy"`/`"hostile"` = -100), applied **both directions** via `Ai.SetRelation` for a true mutual stance.
The *original* relation is recorded first and automatically restored the moment the contract ends (win,
lose, or abort) — a contract can safely flip factions hostile for its own duration without permanently
changing how they treat each other afterward.

When one side of a relation is `"PMC"` (the player's own faction), the framework also calls
`MrxFactionManager.SetAttitudeMutable` on the *other* faction first — the same call the story missions use
to make a faction's attitude toward the player actually able to change at all (see
[`resident/mrxfactionmanager`](../resident/mrxfactionmanager) — a faction with `bDynamic = false` can't be
moved regardless of what `Ai.SetRelation` is told).

## See also

- [Support Effects & Triggers](support-effects-and-triggers) — the trigger/`fires`/logic-gate system AI
  orders share.
- [Objectives Reference](objectives) — `Contract.Enter`/`Contract.Escort`/etc. can reference a `def.units`
  group by name via `target`, rather than spawning their own separate object.
- [`resident/mrxfactionmanager`](../resident/mrxfactionmanager) — `SetAttitudeMutable` and which factions
  are actually `bDynamic`.
