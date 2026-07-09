---
title: Support Effects & Triggers
parent: Contract Framework
nav_order: 3
---

# Support Effects & Triggers

> **Status: new, in development.** Read directly from `ContractFramework.lua` (read in full). Behavior
> described here is what the code currently does, not yet independently confirmed by extended live play.

`def.support` is a list of scripted, triggered actions — an artillery barrage, a wave of reinforcements, a
music swell, a line of dialogue — layered on top of the objective list. Each entry names an **effect**
(what happens) and a **trigger** (when it fires). This is the same mechanism [MissionForge](mission-forge)
and [the web tool](web-tool) expose through their own "Support call-ins" / "Triggers" steps.

```lua
def.support = {
    { id = "arty1", effect = "artillery", at = { 100, 0, 200 }, radius = 20, count = 6,
      trigger = { proximity = 40 } },
}
```

## Effect types (`effect = "..."`)

| Effect | Params | What happens |
|---|---|---|
| `artillery` | `at`, `radius`, `count`, `ammo` (default `"Gunship Shell"`), `owner` | `count` shells rain onto a spread area around `at`, staggered ~0.35s apart, via `Airstrike.SpawnOrdnance`. |
| `flyby` / `airstrike` | `at`, `vehicle` (default `"Support Vehicle (Autogunship)"`), `altitude`, `speed` | A support vehicle streaks over the point via `Airstrike.Flyby` — a visual pass, no ordnance of its own. |
| `bombingrun` | `at`, `vehicle` (default `"Support Vehicle (A10)"`), `ammo` (default `"Bomb"`), `altitude`, `speed`, `count`, `owner` | An aircraft makes a pass and walks a stick of `count` bombs onto the zone, re-reading the aircraft's live position each drop so the stick actually follows its flight path. |
| `heli` | `at`, `template` (default `"AH1Z"`), `count`, `stagger`, `spread`, `altitude`, `speed` | A wave of `count` helicopters passes over, fanned out in both position and timing so they never spawn into each other. |
| `reinforce` | `at`, `faction`, `spawns` (a list of templates), `deliver` = `"copter"` \| `"paradrop"` \| direct | Units arrive: `"paradrop"` flies a transport over first and drops troops under it; `"copter"` uses `MrxCopterDrop.Create`; otherwise units spawn directly. |
| `custom` | `fn` | Calls `fn(ev, task)` yourself — the escape hatch for anything not covered above. |
| `say` | `text`, `hold` | A one-shot radio line via the HUD objective tray (auto-clears after `hold` seconds, default 5). |
| `music` | `cue`, or `stop = true` / `cue = "stop"` | Swells (or stops) the special mission music — see [cue names](../sound-music-effects#music-cues). |
| `vfx` | `at`, `particle`, `count`, `radius`, `up` | Cosmetic (no damage) explosion/fire/smoke particles via `Airstrike.SpawnDirectedObject` — see [particle names](../sound-music-effects#explosions--particle-effects). |
| `damage` | `target` (a group name, faction, or area), `pct` (default 25) or `kill = true` | Scripted damage/kill on a target set, via `Object.SetHealth`/`Object.Kill`. |
| `vo` | `lines` (a string or list of VO keys), `gap` | Plays a voice-over line sequence via `MrxVoSequence.Start` — no-op if VO isn't loaded. See [VO key reference](../sound-music-effects#voice-over-lines). |

`music`/`vfx`/`vo` are exactly the three effects [Sound, Music & Effects](../sound-music-effects) exists to
give you real cue/particle/VO-key names for — that page is this one's companion reference, not a separate
system.

## Fanfare

Contract completion always plays the native completion sting — the music cue plus a HUD banner, via
`Hud.EventFanfare:Commence`. The style **must** be one of a fixed set of shipped `EventFanfare` types or
the native call crashes on its own PDA-log concatenation, so the framework clamps it:

```
contact · support · stockpile · landingzone · hvtcapture · hvtkill · bounty · outfit · highscore
```

Set `def.fanfareType` to any of those (default: `"highscore"`, which reads as a generic win) and
`def.fanfare` for the banner text (default: `"<title> complete"`).

## Triggers — when an effect fires

Every support entry (and every [AI order](units-ai-and-relations#ai-orders-per-group)) has a `trigger`.
Conditions:

| `trigger =` | Fires when |
|---|---|
| `"immediate"` (default if omitted) | Right away, as soon as the contract's background setup runs. |
| `{ once = seconds }` (or the string `"once"`, using `ev.delay`/default 3) | A one-time delay. |
| `{ recurring = interval, limit = n }` (or `"recurring"`, using `ev.interval`/default 10) | Repeatedly, every `interval` seconds, forever or up to `limit` times. |
| `{ proximity = radius, at = {x,y,z} }` | The player enters `radius` of a point (defaults to the effect's own `at` if omitted). |
| `{ onDestroy = "nearest" \| "PlacedName" }` | A named placement dies, or (with `"nearest"`) the closest matching object in an area dies — polled until one exists, then watched. |
| `{ onHealthBelow = { pct =, target = } }` | A tracked target's health drops below `pct`% of whatever it was when first observed. |
| `{ onObjComplete = N }` | Top-level objective #N is marked done. |
| `{ onCleared = { radius =, faction =, kind = } }` | An area that had matching objects in it now has zero — a "wave wiped out" check, only counted once something was actually there first. |

## Named triggers, `fires`, and logic gates

Anything above can also be authored as a standalone entry in `def.triggers` (with an `id`, and `kind`
instead of the inline shape — e.g. `kind = "proximity"`, `kind = "onDestroy"`) so multiple support entries
or AI orders can be gated on the **same** condition without duplicating it. A support/order entry opts into
this by setting `trigger = { ref = "thatTriggerId" }` instead of its own condition — it then stays dormant
until the named trigger fires.

A named trigger's own `fires = { "id1", "id2", ... }` lets one condition kick off several support entries
and/or AI orders at once by id.

Two special `kind`s act as **logic gates** over other triggers' fired-state rather than any world
condition:

- `kind = "all"`, `inputs = { id1, id2, ... }` — fires once *every* listed trigger has fired.
- `kind = "count"`, `inputs = { ... }`, `need = N` — fires once *any* `N` of the listed triggers have
  fired.

Gates can chain — a gate firing marks itself as fired too, so it can feed into another gate's `inputs`.

## Example: a reinforcement wave gated on two conditions

```lua
def.support = {
    { id = "wave_dead",  effect = "custom", fn = function() end, trigger = { onCleared = { radius = 50 }, at = { 0,0,0 } } },
    { id = "obj1_done",  effect = "custom", fn = function() end, trigger = { onObjComplete = 1 } },
    { id = "gate", kind = "all", inputs = { "wave_dead", "obj1_done" } },  -- goes in def.triggers, not def.support
}
def.triggers = {
    { id = "gate", kind = "all", inputs = { "wave_dead", "obj1_done" }, fires = { "reinforcements" } },
}
def.support[#def.support + 1] = { id = "reinforcements", effect = "reinforce",
    at = { 0, 0, 0 }, faction = "VZ", spawns = { "VZ Soldier", "VZ Soldier" },
    trigger = { ref = "gate" } }
```

(Split across two tables above only for clarity — `gate` really belongs in `def.triggers`, not
`def.support`.) Reinforcements arrive only once the first wave is cleared **and** objective 1 is complete,
whichever order those two things happen in.

## See also

- [Sound, Music & Effects](../sound-music-effects) — the full cue/particle/VO-key reference for the
  `music`/`vfx`/`vo` effects above.
- [Objectives Reference](objectives) — `def.fail` conditions (`Contract.Protect`/`Contract.StayInArea`) run
  through this same trigger machinery.
- [Units, AI Orders & Relations](units-ai-and-relations) — AI orders (`def.waypoints`) use the identical
  `trigger`/`fires` shape described here.
