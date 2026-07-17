---
title: Identity & World Query
parent: Essentials (Ess)
nav_order: 2
---

# Identity & World Query

## Overview

This page covers the [Ess](index) namespaces you reach for once you know *what* you want to touch: who the
player is, what a given object is doing, what's sitting in a vehicle's seats, what's nearby, what a
character is carrying, and how to shove any of it around. Six source files: `10_player.lua` (`Ess.Player`),
`11_object.lua` (`Ess.Object`), `12_vehicle.lua` (`Ess.Vehicle` + an inline `Ess.Easy.Vehicle.summon`),
`13_probe.lua` (`Ess.Probe`), `14_human.lua` (`Ess.Human` + an inline `Ess.Easy.Human.giveWeapon`), and
`16_impulse.lua` (the full three-tier `Ess.Raw.Impulse` / `Ess.Impulse` / `Ess.Easy.Impulse`).

Every function here is `uGuid`-first and `pcall`-wrapped — the whole point is that a bad or dead guid gets
you `nil`/`false` back, not a hard Lua error killing the rest of your script.

## Ess.Player

Player/character identity, without the 8-getter native sprawl (`GetLocalCharacter`/`GetPrimaryCharacter`/
`GetSecondaryCharacter`/`GetAnyCharacter`/`GetLocalPlayer`/`GetPrimaryPlayer`/`GetSecondaryPlayer`/
`GetCharacter(slot)`). Wraps the [`Player`](../namespaces/player) engine namespace. `Player.GetAnyCharacter()`
(native, "whichever character, don't care which") stays directly available for the rare case that actually
wants it — not worth wrapping.

| Function | Signature | Notes |
|---|---|---|
| `character` | `Ess.Player.character(i) -> uCharGuid \| nil` | `i = 0` or `nil` is `Player.GetLocalCharacter()` (this machine's own character, single-player-safe). `i = 1` is `Player.GetSecondaryCharacter()` — **confirmed nil outside co-op**, and that `nil` is returned as-is rather than silently coerced into something a downstream `Object.*` call would choke on. |
| `slot` | `Ess.Player.slot(i) -> uPlayerGuid \| nil` | The player-**slot** guid (what `Camera.*` and some `Ai.*` calls actually want), distinct from the character guid. |
| `camera` | `Ess.Player.camera(i) -> uCameraGuid \| nil` | Resolves an index straight to `Player.GetCamera(slot)` in one call. |
| `giveCash` | `Ess.Player.giveCash(n)` | Routes through `MrxPmc.AddCashQty(n, false, "[Ess]")` — **never** `Player.SetCash`/`AddCash`, which are confirmed to silently skip the HUD refresh. No player-index argument: cash is this machine's own campaign wallet. |
| `giveFuel` | `Ess.Player.giveFuel(n)` | Same idea via `MrxPmc.AddFuelQty(n)`. |
| `pose` | `Ess.Player.pose(i) -> x, y, z, yaw, uChar, uPlayerSlot` | One-stop "where is this player, facing which way." `yaw` defaults to 0 if unreadable; `x`/`y`/`z` are `nil` if there's no character at all (e.g. `i=1` outside co-op). |
| `targetUnderReticle` | `Ess.Player.targetUnderReticle(i) -> uGuid \| nil, x, y, z` | The native (`Player.GetTargetUnderReticle`) returns coordinates first and the guid last; this reorders so the guid is the primary return value, matching `Ess.Player`'s own convention elsewhere. |
| `removeBoundaries` | `Ess.Player.removeBoundaries() -> nCleared` | Clears every out-of-bounds volume currently active, for every connected player at once (iterates `Player.GetAllPlayers()`, so no `i` argument needed). Only clears what's active *right now* — doesn't disable the boundary system, so a mission/area transition can add a new one later. |
| `setInputEnabled` | `Ess.Player.setInputEnabled(bOn, i)` | Freeze (`false`)/restore (`true`) gameplay input via `Player.SetInputEnabled` on the player slot. Confirmed to leave the keyboard-event stream a Lua UI reads (`Loader.PopKeyEvents`) intact — it gates game control only, so a chat box can still type while the world is frozen underneath it. |
| `rumble` | `Ess.Player.rumble(i, fLength)` | Controller haptic feedback via `Pg.Rumble`. `fLength` defaults to 0.2 (real call sites use ~0.15s). |
| `teleport` | `Ess.Player.teleport(x, y, z, yaw, onDone)` | Warps **all** connected heroes to one spot (co-op safe) via the confirmed `MrxUtil.TeleportHeroesToLocations` idiom — deliberately *not* raw `Object.SetPosition`, which is unreliable on characters. `onDone` fires once the warp completes. For the co-op case where each hero needs a *different* spot, drop to `MrxUtil.TeleportHeroesToLocations` directly with a per-hero location list. |

Two caveats worth knowing before you rely on this namespace:

- **`Ess.Player.slot(1)` is not a co-op check.** Confirmed live (2026-07-16, single-player, PMC HQ):
  unlike `Ess.Player.character(1)`, which correctly returns `nil` outside co-op, `Player.GetSecondaryPlayer()`
  returns a real, distinct, non-nil player-slot guid even in single-player. Use `Ess.Player.character(1) ~=
  nil` to test for co-op, not `Ess.Player.slot(1) ~= nil`.
- **`teleport` and interior cells don't round-trip.** Confirmed live: teleporting *out* of the PMC HQ
  interior cell unloads that cell and drops the player into the open world — interior coordinates do not
  round-trip (teleport back to an interior Y and you land on open-world terrain below it and take fall
  damage instead). Fall damage on this engine is capped (~97) and never fatal on its own, but heal
  afterward (`Ess.Object.heal`) if you don't want the player left hurt.

## Ess.Object

The everyday object-manipulation namespace, wrapping [`Object`](../namespaces/object) — the biggest engine
namespace (87 functions) — with `pcall`-safety and one canonical name per concept, so a modder isn't
dropping to raw native calls (and hitting invalid-guid throws) for basic move/hurt/hide/label/launch.

A shared internal `truthy(v)` helper (`v == true or v == 1`) backs every boolean-returning wrapper below —
some engine getters return `1`/`0` rather than a real boolean, and `0` is truthy in Lua, so a naive `if
Ess.Object.alive(g)` could otherwise be fooled by a `0`.

### Transform

| Function | Signature | Notes |
|---|---|---|
| `pos` | `Ess.Object.pos(uGuid) -> x, y, z \| nil` | `pcall`-wrapped `Object.GetPosition` (it throws on an invalid/dead guid). |
| `setPos` | `Ess.Object.setPos(uGuid, x, y, z)` | Teleports an *object*. Confirmed unreliable on freshly-spawned/AI humans (streaming/physics can snap them back) — for the player use `Ess.Player.teleport`, for a dynamic ghost-follow use `Ess.Vehicle.followGhost`. Solid for props/vehicles and for placing a just-spawned object before it streams in. |
| `yaw` / `setYaw` | `Ess.Object.yaw(uGuid) -> n \| nil` / `Ess.Object.setYaw(uGuid, n)` | Unit (degrees vs. radians) is **unconfirmed** on this engine — the project's own sample scripts disagree with each other. Read-modify-write a yaw you got from `yaw()` and it's self-consistent regardless. |
| `faceToward` | `Ess.Object.faceToward(uGuid, x, y, z)` | Turns the object to face a world point (ground-plane yaw; `y` is accepted for call convenience but unused). Uses `Ess.Math.angleTo` so the convention matches the engine's own. |
| `faceObject` | `Ess.Object.faceObject(uGuid, uTarget)` | Same, but faces another object's *current* position. |
| `distance` | `Ess.Object.distance(uGuidA, uGuidBOrX, yOrIgnoreY, z, bIgnoreY) -> n \| nil` | Collapses `Object.GetDistanceFrom`'s two confirmed forms — object-to-object (`uGuidA, uGuidB, bIgnoreY`) and object-to-coordinates (`uGuidA, x, y, z, bIgnoreY`) — into one call, dispatching on whether the 2nd argument is a number. |

### Health & life

| Function | Signature | Notes |
|---|---|---|
| `health` / `setHealth` | `Ess.Object.health(uGuid) -> n \| nil` / `Ess.Object.setHealth(uGuid, n)` | |
| `maxHealth` | `Ess.Object.maxHealth(uGuid) -> n \| nil` | |
| `heal` | `Ess.Object.heal(uGuid)` | The confirmed "heal to full" idiom: `Object.SetHealth(uGuid, Object.GetMaxHealth(uGuid))`. |
| `damage` | `Ess.Object.damage(uGuid, nAmount) -> nNewHealth \| nil` | There is no native "damage" call on this engine (only Get/SetHealth/Kill) — this reads current health, subtracts, and applies; if the result would be `<= 0` it calls `Object.Kill` outright, since `SetHealth(uGuid, 0)` does **not** reliably register as death here. Returns the new health (0 if it killed), or `nil` if health couldn't be read. |
| `kill` / `remove` | `Ess.Object.kill(uGuid)` / `Ess.Object.remove(uGuid)` | Distinct verbs on purpose: `Kill` destroys (leaves a corpse/wreck), `Remove` deletes the object outright. **Confirmed: `Kill` is not instantaneous** — `alive(uGuid)` still reads `true` in the same tick as a kill (the death sequence has to begin first) and flips to `false` a moment later. Poll `alive()` over a couple ticks rather than checking it immediately after `kill()`. |
| `revive` | `Ess.Object.revive(uGuid, nDelay)` | `nDelay` is an optional, confirmed second argument to `Object.Revive`. |
| `alive` / `valid` | `Ess.Object.alive(uGuid) -> bool` / `Ess.Object.valid(uGuid) -> bool` | `Object.IsAlive`/`Object.IsValid`, `truthy()`-coerced. |
| `setInvincible` | `Ess.Object.setInvincible(uGuid, bOn, sReason)` | `sReason` is **required** here even though the native call allows omitting it — every real call site tags one ("Survival"/"Hijack"/"HQ"), and making it mandatory means you can't accidentally ship an untagged toggle some other system can't attribute later. An invalid/missing reason logs a warning and falls back to `"Ess"` rather than failing. |

### Visibility, labels, identity

| Function | Signature | Notes |
|---|---|---|
| `visible` / `setVisible` | `Ess.Object.visible(uGuid) -> bool` / `Ess.Object.setVisible(uGuid, bOn)` | `Object.IsVisible` is a real boolean-returning native here (distinct from the `FlashWidget` `GetVisible` footgun documented elsewhere in Ess). |
| `hasLabel` / `addLabel` / `removeLabel` | `Ess.Object.hasLabel(uGuid, sLabel) -> bool`, `.addLabel(uGuid, sLabel)`, `.removeLabel(uGuid, sLabel)` | Labels are free-form string tags the engine and other scripts read (e.g. `"PMC"`, `"Disposable"`, `"garage"`). |
| `displayName` | `Ess.Object.displayName(uGuid) -> s` | Localized, human-readable name (`Object.GetLocalizedName`) — for HUD/labels. Distinct from `Ess.Name(guid)` (see [Core Primitives](core)), which is the guid's hash string. |
| `playerControlled` | `Ess.Object.playerControlled(uGuid) -> bool` | **Live discovery:** despite the engine's own wiki page implying a boolean, `Object.IsPlayerControlled` actually returns the *controlling player's guid* (a userdata) when the object is player-controlled, and a falsy value otherwise — a plain `truthy()` check would wrongly report the real player as NOT controlled (a guid isn't `== true` or `== 1`). This wrapper instead checks "returned a real value" (`v ~= nil and v ~= false and v ~= 0`). |

### Physics

| Function | Signature | Notes |
|---|---|---|
| `enablePhysics` / `disablePhysics` | `Ess.Object.enablePhysics(uGuid)` / `Ess.Object.disablePhysics(uGuid)` | |
| `impulse` | `Ess.Object.impulse(uGuid, x, y, z, bLocal)` | `Object.ApplyImpulse` — the confirmed launch/knock-around primitive; real call sites scale the impulse by the object's mass (e.g. `Object.ApplyImpulse(u, 0, 10000, 6 * mass, true)`), so heavier things need a bigger push. `bLocal` defaults to `true` (impulse in the object's own space). This is the bare call — for mass-scaling + directional + `speedBoost`/`launch`/`knockback` presets, see [Ess.Impulse](#ess-impulse) below. |

### Spawn

The one *create* verb — spawning is `Pg.Spawn`, not `Object.*`, but a spawned thing is an object you then
drive with everything above, so it lives here. Both entry points carry a confirmed blank-template crash
guard: a blank/whitespace template string hard-crashes the engine and `pcall` cannot catch a native crash,
so it's validated *before* the call rather than relying on `pcall` to make it safe.

| Function | Signature | Notes |
|---|---|---|
| `spawn` | `Ess.Object.spawn(sTemplate, x, y, z, yaw) -> uGuid \| nil` | Refuses a blank/whitespace `sTemplate` outright (logs and returns `nil`). Sets `yaw` after spawn if given. |
| `spawnAhead` | `Ess.Object.spawnAhead(sTemplate, nDist, nHeight, i) -> uGuid \| nil` | Spawns `sTemplate` `nDist` units (default 18) in front of player `i` (default local), `nHeight` units up (default 0 — bump it for aircraft / a midair drop), facing the same way the player is. Hides the yaw→sin/cos "in front of me" trig via `Ess.Math.pointAhead` (see [Core Primitives](core)). |

Real usage, from the shipped `spawn_and_control` recipe:

```lua
local car = Ess.Object.spawnAhead("Veyron", 8)

local cx, cy, cz = Ess.Object.pos(car)                       -- where did it end up?
local px, _, pz  = Ess.Player.pose(0)
local dist = Ess.Math.dist2D(px, pz, cx, cz)                 -- horizontal distance to the player
Ess.Object.faceObject(car, Ess.Player.character(0))          -- turn it to face me
Ess.Object.heal(car)                                         -- set health to full
```

### Vehicle-entry watch

| Function | Signature | Notes |
|---|---|---|
| `vehicleOf` | `Ess.Object.vehicleOf(uChar) -> uVehicleGuid \| nil` | Unifies 4 overlapping entry points across 2 namespaces (`Object.InSeat`/`Object.InVehicle`/`Player.GetControlledObject`/`Vehicle.GetFromRider`) into the one confirmed idiom in the shipped source: `Vehicle.GetFromRider(char)` (driver or passenger). |
| `pollVehicleChange` | `Ess.Object.pollVehicleChange(uChar, onChange, interval) -> stop()` | Watches `uChar` for entering/exiting a vehicle by **polling** `Vehicle.GetFromRider` on a heartbeat (default interval 0.5s, built on the shared `Ess.Loop`) and firing `onChange(uVehicleOrNil, uPrevVehicleOrNil)` on the nil↔guid transition. Confirmed there is no native "entered a vehicle" event for an *unknown* target vehicle — the only Lua-reachable enter event needs a specific vehicle+seat known in advance, so this polls rather than hooks. Returns a `stop()` function to end the watch early. |

## Ess.Vehicle

Seat/rider queries plus the human-doesn't-`SetPosition` workaround, wrapping the
[`Vehicle`](../namespaces/vehicle) engine namespace.

| Function | Signature | Notes |
|---|---|---|
| `driver` | `Ess.Vehicle.driver(uVeh) -> uCharGuid \| nil` | |
| `riders` | `Ess.Vehicle.riders(uVeh) -> { uCharGuid, ... }` | Empty table if none/unreadable, never `nil`. |
| `seatOf` | `Ess.Vehicle.seatOf(uChar) -> sSeat \| nil` | Which seat `uChar` currently occupies, if any. Together with `driver`/`riders` this collapses a 7-getter overlap (`GetDriver`/`GetRiders`/`GetFromRider`/`GetSeatFromRider`/`GetRiderFromSeat`/`GetFromSeat`/`GetSeatByType`) down to the 3 shapes actually needed day to day — the raw namespace stays available for anything more exotic. |
| `enterBestSeat` | `Ess.Vehicle.enterBestSeat(uChar, uVeh) -> ok` | `pcall`-wrapped `MrxUtil.EnterBestAvailableSeat` — confirmed driver/gunner/passenger/cargo seat priority order. |
| `enterSeatExcluding` | `Ess.Vehicle.enterSeatExcluding(uChar, uVeh, excludeSeats) -> ok, sSeatTypeUsed` | For "board a vehicle but never take the driver seat" (e.g. a co-op partner boarding after the driver already has). Loops `{"d","g","p","c"}` in priority order via `Vehicle.GetSeatByType` + `Vehicle.EnterBySeatGuid`, skipping any type named in `excludeSeats`. Verified against the real, live-confirmed-working `DestroyerTool.lua` (see [Making the Destroyer Driveable](../deep-dives/destroyer-vehicle)) — its two boolean arguments are passed exactly as that reference does; their precise semantics beyond that call site aren't independently confirmed. |
| `exit` | `Ess.Vehicle.exit(uVeh, uChar) -> ok` | Confirmed signature+usage from the same `DestroyerTool.lua`: `Vehicle.Exit(uVehicle, uCharacter, true)`. |
| `flyTo` | `Ess.Vehicle.flyTo(uHeli, x, y, z, opts) -> cancel()` | Sends an AI helicopter to a world point. Wraps two gotchas: the flight command is `Ai.Deliver(driver, x, y, z, dropHeight, careless)` — **not** `Ai.Goal "MoveToPos"`, which does not fly a heli — and a freshly-spawned heli has no driver for a moment, so this polls `Ess.Vehicle.driver` until one exists before issuing the order. `opts.height` (drop height, default 0.5), `opts.careless` (bool), `opts.onReady(driver)` fires once the order is issued. Returns `cancel()` to stop the driver-wait early. |
| `orbitFlight` | `Ess.Vehicle.orbitFlight(uHeli, cx, cy, cz, opts) -> totalSeconds` | Flies a *crewed* heli (a "(Driver)"/"(Full)" template) a few circular laps around a centre point by chaining timed `flyTo` waypoints. `opts`: `radius`(90), `height`(45), `orbits`(2), `points`(6 per orbit), `secPerLeg`(2.2), `startAngle`(deg), `tracker` (an `Ess.Track`, for cleanup), `onDone`. The first leg starts above ground, so the heli climbs into the orbit with no separate takeoff order. |
| `followGhost` | `Ess.Vehicle.followGhost(template, x, y, z) -> ghost \| nil` | Spawns `template` and returns a `ghost` object (`ghost.guid`, `ghost:update(nx, ny, nz)`, `ghost:remove()`). Confirmed gotcha: `Object.SetPosition` silently does **not** move a spawned human (works fine on props/vehicles) — `:update()` tries `SetPosition` first, then re-reads the real position; if it's still off by more than ~3 units, it despawns and respawns the template at the new spot instead, updating `ghost.guid` so callers always read the current handle. |

**Caution, live-observed but not causally confirmed (2026-07-16, PMC HQ interior):** spawning a vehicle and
calling `enterBestSeat` from *inside* an interior cell was followed once by the next bridge chunk (even a
bare `return 1+1`) stalling Lua execution for 30+ seconds, recovered only by killing and relaunching the
process. Never confirmed the vehicle-entry was the actual cause — could be coincidental — but the source
flags it explicitly: avoid spawning + entering a vehicle from inside an interior cell without further
testing, and don't chain an immediate follow-up query in the same breath if you do.

### Ess.Easy.Vehicle

`12_vehicle.lua` also defines one inline Easy-tier preset:

```lua
Ess.Easy.Vehicle.summon(sTemplate, opts) -> uVeh | nil
```

Spawns `sTemplate` a short way in front of the local player (via `Ess.Object.spawnAhead`, no coordinate/yaw
math needed) and drops the player into the best seat (`Ess.Vehicle.enterBestSeat`). Midair by default —
`opts.dist` (18) / `opts.height` (10) override — so an aircraft hovers the instant you're piloting it and a
ground vehicle just settles. Returns `nil` if the template name was wrong. The full `Ess.Easy.*` catalog is
covered on [Ess.Easy](easy).

## Ess.Probe

Nearby-object queries and a safe "what is this guid" description.

| Function | Signature | Notes |
|---|---|---|
| `nearby` | `Ess.Probe.nearby(x, y, z, radius, kind, filter, includeSelf) -> { uGuid, ... }` | Collapses `Pg.FastCollectHumans`/`GroundVehicles`/`Buildings`/`Flying`/`Tanks`/`Helicopters` (11 separate "find nearby X" natives) into one dispatcher, deduped by guid across whichever families `kind` selects. `kind`: `"humans"` \| `"vehicles"` (ground + flying) \| `"buildings"` \| `nil`/`"any"` (humans + ground vehicles + flying). `filter`: optional `Object.HasLabel` string — only objects carrying that label are kept. `includeSelf`: **default `false`** — the native `FastCollect*` calls have no concept of "self," so a query whose radius covers the caller's own position would otherwise return the local player's own character(s) indistinguishable from any other result; pass `true` for the rare case that genuinely wants them (e.g. counting total zone occupants). |
| `nearest` | `Ess.Probe.nearest(x, y, z, radius, kind, filter, includeSelf) -> uGuid, nDist \| nil` | The single closest match from `nearby` (same args, same player-excluded-by-default behavior). Returns `nil` if nothing matched in range. |
| `getFaction` | `Ess.Probe.getFaction(uGuid) -> sAbbrev \| nil` | `MrxUtil.GetFaction` → `MrxFactionManager.GetFactionAbbrev` fallback chain. |
| `describeSafe` | `Ess.Probe.describeSafe(uGuid) -> sDescription` | A one-line "what is this" for logging/debugging — name, position, health, faction — every field individually `pcall`-guarded so one bad field can't blank out the whole description. |

**Confirmed real-world footgun (2026-07-16):** an ad hoc test query with a typo'd `kind` (e.g.
`"character"`, not a valid kind) silently fell through to the `"any"` default, and because `includeSelf`
defaults to excluding the player, that part was actually safe — but the incident that prompted the
`includeSelf` default in the first place was a query that *did* end up returning only the player's own guid,
and a destructive call on the result killed the player. Don't assume a `nearby`/`nearest` result is never
you unless you've confirmed `includeSelf` is doing what you think.

## Ess.Human

Weapon/inventory control and action/animation playback for a character guid, wrapping the `Human` engine
namespace plus the small `Weapon` namespace for ammo (since ammo operates on the weapon guids `Ess.Human`'s
own getters return — one home instead of a third tiny namespace).

| Function | Signature | Notes |
|---|---|---|
| `equipWeapon` | `Ess.Human.equipWeapon(uChar, uWeapon) -> ok` | `Human.Inventory.EquipWeapon` — the confirmed-working form. The top-level `Human.EquipWeapon` has zero real call sites anywhere in the decompiled corpus, so this deliberately does not expose that one. |
| `dropWeapon` | `Ess.Human.dropWeapon(uChar, uWeapon) -> ok` | `Human.Inventory.DropWeapon`. |
| `primaryWeapon` / `secondaryWeapon` | `Ess.Human.primaryWeapon(uChar) -> uGuid \| nil` / `.secondaryWeapon(uChar) -> uGuid \| nil` | `Human.Inventory.Get{Primary,Secondary}Weapon`. |
| `allWeapons` | `Ess.Human.allWeapons(uChar) -> { uGuid, ... }` | `Human.Inventory.GetAllWeapons` — never `nil`, an empty table if none. |
| `setAllWeapons` | `Ess.Human.setAllWeapons(uChar, tWeaponGuids) -> ok` | `Human.Inventory.SetAllWeapons`. |
| `reloadAll` | `Ess.Human.reloadAll(uChar)` | `Human.Inventory.ReloadAll(uChar, false)`. |
| `doAction` | `Ess.Human.doAction(uChar, sActionName)` | `Human.DoAction` — e.g. `"Cower"`/`"Stand"`/`"Proximity"`. No-ops on a blank/non-string action name. |
| `disableWeapons` / `enableWeapons` | `Ess.Human.disableWeapons(uChar)` / `.enableWeapons(uChar)` | |
| `knockdown` | `Ess.Human.knockdown(uChar, nDuration)` | `Human.Knockdown`; `nDuration` defaults to 0.5. |
| `ammo` / `setAmmo` / `maxAmmo` | `Ess.Human.ammo(uWeapon) -> n` / `.setAmmo(uWeapon, n)` / `.maxAmmo(uWeapon) -> n` | `Weapon.GetReserveAmmo`/`SetReserveAmmo`/`GetMaxReserveAmmo`. `ammo`/`maxAmmo` return 0 rather than `nil` on failure. |
| `refillAmmo` | `Ess.Human.refillAmmo(uWeapon)` | The confirmed "set to `GetMaxReserveAmmo`" one-liner, independently duplicated across `pmccon001.lua`/`vzacon001.lua`. |
| `setInfiniteAmmo` | `Ess.Human.setInfiniteAmmo(uChar, bOn)` | `Object.SetInfiniteAmmo` — note this one is actually on the `Object` namespace (a character guid), not `Human`/`Weapon`, but is kept here as squarely a "character ammo" concern. **Confirmed live-tested:** it keeps *reserve* ammo maxed forever; the magazine currently being fired still empties normally and still needs a reload (grenades: infinite reserve, still thrown one at a time). |

Real usage, from the shipped `give_weapons` recipe:

```lua
local char = Ess.Player.character(0)
local added = Ess.Easy.Human.giveWeapon(char, "Grenade Launcher")   -- add a weapon by template name
Ess.Human.setInfiniteAmmo(char, true)                               -- and never run dry
```

### Ess.Easy.Human

```lua
Ess.Easy.Human.giveWeapon(uChar, sTemplateName) -> ok
```

Live-confirmed: `Pg.GetGuidByName(sTemplateName)` resolves a weapon *template* name (e.g. `"Grenade
Launcher"`) to a real guid distinct from any weapon the character already carries, and
`Human.Inventory.EquipWeapon` on that guid genuinely adds a new weapon (verified via an exact before/after
`GetAllWeapons` count change, 2 → 3) — not just re-equipping something already held. No blank-template guard
needed the way `Pg.Spawn` needs one: `GetGuidByName` on an empty/bad name just returns `nil`/`false`, it
doesn't hard-crash the engine. See [Ess.Easy](easy) for the rest of the beginner-tier surface.

## Ess.Impulse

Launch/boost/knock objects around, the confirmed `Object.ApplyImpulse` way, with the fiddly bits handled.
This is the one namespace in this batch with a full three-tier waterfall: `Ess.Raw.Impulse` (bare natives) →
`Ess.Impulse` (mass-scaled directional push, hides the local-axis convention) → `Ess.Easy.Impulse`
(`speedBoost`/`launch`/`knockback` intent presets).

**Confirmed convention** (from `resident/spyhunter.lua`'s boost/jump mechanic — the speed-boost effect this
wraps): `Object.ApplyImpulse(uGuid, x, y, z, bLocal)` in *local* space is `(x = side, y = up, z = forward)`.
Real boosts scale the impulse by the object's mass — e.g. `ApplyImpulse(u, 0, 10000, 8*mass, true)` — because
an impulse is `mass * Δvelocity`, so changing *speed* by a consistent amount regardless of how heavy the
thing is means the impulse itself has to scale with mass. That mass bookkeeping (`Object.GetMass`, axis
order, local-vs-world) is exactly what makes the raw call awkward.

### Ess.Raw.Impulse

| Function | Signature | Notes |
|---|---|---|
| `apply` | `Ess.Raw.Impulse.apply(uGuid, x, y, z, bLocal)` | `Object.ApplyImpulse`, one `pcall`. Local space (`bLocal` true, the default) is `(x=side, y=up, z=forward)`; world space (`bLocal` false) is world x/y/z. Same underlying call as `Ess.Object.impulse`. |
| `applyAtPoint` | `Ess.Raw.Impulse.applyAtPoint(uGuid, ix, iy, iz, px, py, pz, bLocal)` | `Object.ApplyPointImpulse` — an impulse `(ix,iy,iz)` applied at an *offset* point `(px,py,pz)` rather than the center. An off-center push imparts spin (torque) — how `spyhunter.lua` does its barrel-roll flip. Defaults to local space. |
| `mass` | `Ess.Raw.Impulse.mass(uGuid) -> n \| nil` | `Object.GetMass`, `pcall`'d — the scaling factor the boosts use. |

### Ess.Impulse (Core)

| Function | Signature | Notes |
|---|---|---|
| `push` | `Ess.Impulse.push(uGuid, opts)` | `opts.forward`/`up`/`side` — local-space components (`forward` = the way it faces), omit any for 0. `opts.dir = {x,y,z}` — or a *world-space* direction, overrides forward/up/side (for knockback etc.). `opts.strength` scales `dir` (default 1); for the forward/up/side form, bake strength directly into those. `opts.scaleByMass` — **default `true`**: multiplies by the object's mass (falls back to a `DEFAULT_MASS` of 1000 if `GetMass` is unavailable) so the velocity change is the same on a light bike or a heavy tank. Pass `false` for a raw, mass-independent shove where you supply the full magnitude yourself. |
| `spin` | `Ess.Impulse.spin(uGuid, opts)` | An off-center impulse to make something roll/flip. `opts.forward`/`up`/`side` is the impulse (local); `opts.at = {x,y,z}` is the local offset it's applied at (the lever arm — further from center = more spin). `opts.scaleByMass` as in `push`. |
| `mass` | `Ess.Impulse.mass(uGuid) -> n \| nil` | The mass getter, surfaced at the Core tier too (same as `Ess.Raw.Impulse.mass`). |

### Ess.Easy.Impulse

Intent presets. Default target (when `uGuid` is omitted) is: the vehicle you're driving, or you on foot —
resolved via `Ess.Player.character(0)` then `Ess.Object.vehicleOf(char) or char`.

| Function | Signature | Notes |
|---|---|---|
| `speedBoost` | `Ess.Easy.Impulse.speedBoost(uGuid, strength)` | A forward speed boost — the Spy Hunter effect. Defaults to the vehicle you're driving. `strength` defaults to 8 (real usage: 6–8 for a strong boost); mass-scaled, so it feels the same in a bike or a tank. |
| `launch` | `Ess.Easy.Impulse.launch(uGuid, strength)` | Pops something straight up — a hop, or a big launch. `strength` defaults to 12. |
| `knockback` | `Ess.Easy.Impulse.knockback(uGuid, fromGuid, strength)` | Shoves `uGuid` directly away from `fromGuid` (default source: you) with a slight upward lift — "the blast sent them flying." World-direction, mass-scaled. `strength` defaults to 10. |

Real usage, from the shipped `speed_boost` recipe:

```lua
local car = Ess.Object.spawn("Veyron", px + 12, py, pz)
local _, y0 = Ess.Object.pos(car)
Ess.Easy.Impulse.launch(car, 10)                          -- pop it up
```

See [Ess.Easy](easy) for the full beginner-tier catalog across every namespace, not just Impulse.

## See also

- [Essentials (Ess)](index) — the framework index this page belongs to.
- [Core Primitives](core) — `Safe`, `Table`, `Math`, `Guid`/`Name`, `State`, `SaveVar`, `RNG`; the primitives
  this page's namespaces are built on.
- [Player](../namespaces/player), [Object](../namespaces/object), [Vehicle](../namespaces/vehicle) — the raw
  engine namespaces `Ess.Player`, `Ess.Object`, and `Ess.Vehicle` each wrap.
- [Making the Destroyer Driveable](../deep-dives/destroyer-vehicle) — the live-confirmed multi-seat boarding
  script `Ess.Vehicle.enterSeatExcluding`/`exit` are verified against.
- [Ess.Easy](easy) — the full one-liner surface, including `Ess.Easy.Vehicle.summon`,
  `Ess.Easy.Human.giveWeapon`, and `Ess.Easy.Impulse.*` covered briefly above.
