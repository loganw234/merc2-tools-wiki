---
title: Ess.Easy
parent: Essentials (Ess)
nav_order: 18
---

# Ess.Easy

The beginner tier of every namespace in [Essentials (Ess)](index), collected in one place. The whole
design idea: a newcomer's thought is never "which namespace has the function I need, and what are its
twelve options" — it's "I want a helicopter" or "make that guy hostile." `Ess.Easy.*` hides the import,
hides the namespace, and hides every option that isn't the common case, so that thought becomes exactly
one guessable call. Every function on this page is a thin wrapper over a Core-tier (or occasionally
Raw-tier) call documented in more depth on its own namespace page — this page exists to answer "what can
I do in one line," not "how does it work underneath."

Not every namespace has an Easy tier — only ones with a real beginner/advanced gap do (per
[the three tiers](index#the-three-tiers)). Simple single-tier namespaces (`Ess.RNG`, `Ess.Track`, `Ess.Hud`…)
don't need one and aren't repeated here; see their own pages.

## The in-game reference: `Ess.Easy.Console`

You don't have to keep this page open in a browser tab. `Ess.Easy.Console.open()` opens an in-game,
browsable, searchable list of everything below (plus a handful of standout Core-tier one-liners), built on
[`Ess.UI.Board`](ui#essuiboard) with [`Ess.TextConsole`](timing-input#esstextconsole) driving the search box:

| Call | Does |
|---|---|
| `Ess.Easy.Console.open()` | Browse the full registry, grouped by namespace, in a list+detail board. |
| `Ess.Easy.Console.play()` | Opens the interactive Playground: drill into a category, run a curated demo function live, and cycle its parameters to see exactly what each one does in-game. Also reachable from the pinned `[ Playground... ]` row inside the board itself. See [Debug & Dev Tools](dev-tools) for the full writeup. |
| `Ess.Easy.Console.search()` | Opens a typed prompt; filters the registry by substring match against name/usage/description and reopens the board with just the matches. Also reachable from the pinned `[ Search... ]` row inside the board itself. |
| `Ess.Easy.Console.close()` | Closes whichever of the board, the Playground, and the search prompt are currently open. |

Picking a row logs its exact usage string to `lua_loader_printf.log` and toasts a confirmation — a quick
way to get a call's exact spelling without alt-tabbing. The registry itself is intentionally curated to
genuinely one-line-callable functions (a quick-reference cheat sheet), not an exhaustive dump — this page
mirrors it, organized by task instead of alphabetically, with full real signatures.

## Marking — `Ess.Easy.Mark`

Radar/PDA/world-ring presets over [`Ess.Mark`](mark) — each opt is independent, these three just cover the
common combinations.

| Call | Surfaces | Matches the convention of |
|---|---|---|
| `Ess.Easy.Mark.enemy(uGuid)` | radar + PDA, no world icon | WaveDefense (don't clutter the world with an icon per enemy) |
| `Ess.Easy.Mark.objective(uGuid)` | radar + PDA + world | ContractFramework's real mission objectives |
| `Ess.Easy.Mark.zone(x, y, z, r)` | world ring only | the ground-disc "go here" case, no radar/PDA clutter |

## Spawning — `Ess.Easy.Spawn`

One-line "make something cool appear near me," all routed through [`Ess.Object.spawn`/`.spawnAhead`](identity-query#essobject)
(blank-template crash guard and in-front math already handled), using confirmed real template-name strings.

| Call | Does |
|---|---|
| `Ess.Easy.Spawn.explosion(sType)` | A boom ~10 units in front of you. Default `"Explosion (Grenade)"`; also confirmed: `"Explosion (C4)"`, `"Explosion (MOAB)"`, `"Explosion (Rocket Artillery)"`, `"fx_Explosion_Huge"`. **Real, damaging — don't stand in it.** |
| `Ess.Easy.Spawn.crate(sType)` | A supply drop that parachutes in front of you. Default `"Supply Drop (Light MG)"`; also `"Supply Drop (Blueprints)"`, `"Supply Drop (Treasure)"`. Spawned high so the chute deploys, matching the game's own bounty crates. |
| `Ess.Easy.Spawn.weapon(sName)` | A weapon **pickup** on the ground in front of you (walk over it to grab it). Default `"RPG"`; also `"Sniper Rifle"`, `"Assault Rifle"`, `"Minigun"`, `"Shotgun"`, `"Grenade Launcher"`, `"C4"`, `"Anti-Material Rifle"`, `"Pistol"`. For straight-into-your-hands instead, see [`Ess.Easy.Human.giveWeapon`](#human--combat--esseasyhuman) below. |
| `Ess.Easy.Spawn.airstrike(sRound)` | Calls a shell down on your own head — the classic sandbox gag. Real `Airstrike.SpawnOrdnance` call, impact-fused, 250 units up with downward velocity. Default `"Artillery Shell"`; also `"Gunship Shell"`, `"Cluster Bomb Projectile"`, `"Cruise Missile Projectile"`, `"Bomb"`. **Real, lethal ordnance.** |
| `Ess.Easy.Spawn.fx(sTemplate, x, y, z)` | A particle/FX at a world location — a plain [`Ess.Object.spawn`](identity-query#essobject). |
| `Ess.Easy.Spawn.fxOn(sTemplate, uGuid, sBone)` | An FX on an object. With `sBone`, it's **glued** to that bone via [`Ess.Bones.attachFX`](camera-bones#essbones) and follows the object as it animates; without one, it's a one-shot at the object's current position. Remove a bone-bound one with `Ess.Bones.detachFX(uGuid, handle)`. Only real character/vehicle bone names bind — see [Ess.Bones](camera-bones#essbones) for where those come from. |
| `Ess.Easy.Spawn.enemies(nCount, opts)` | Drops `nCount` (default 3) hostiles a short distance in front of you and — unless `opts.attack` is `false` — immediately orders them to attack `opts.target` (default: you) via [`Ess.Easy.AIOrders.attack`](#ai-orders--esseasyaiorders): an instant firefight in one line. `opts`: `template` (default `"VZ Soldier"`), `dist` (14, how far ahead), `spread` (3, spacing between spawn slots), `attack` (default `true`), `target`. Returns the spawned guids so you can order/track them further. |
| [`Ess.Object.spawn(sTemplate, x, y, z, yaw)`](identity-query#essobject) | Not actually `Ess.Easy` — this is the plain Core-tier call every preset above is built on — but it's the natural next thing a beginner on this page reaches for the moment they want a template that isn't one of the curated presets above (there are thousands: vehicles, characters, props, anything with a spawn template). Blank-template crash guard included; returns the new guid, or `nil` if the template name was wrong. [`Ess.Object.spawnAhead(sTemplate, nDist, nHeight, i)`](identity-query#essobject) is the "in front of the player" version every preset above actually uses (`nDist` default 18, `nHeight` default 0) — it hides the yaw/trig math a beginner has no way to know. |

Confirmed FX/particle templates beyond the explosion family: `"fx_Explosion_Huge"`,
`"global_particle_explosion_c4"`, `"global_particle_env_smokeplume_distance_tall"`. One-shot FX
self-destruct on their own; ambient ones (a smoke plume) persist until you `Ess.Object.remove` them.

The real confirmed recipe (`samples/recipes/instant_firefight.lua`) is exactly one line — the attack order
happens automatically inside `enemies()`, no separate `Ess.Easy.AIOrders.attack` call needed:

```lua
Ess.Easy.Spawn.enemies(4)   -- 4 hostiles ahead, already ordered to attack you
```

## Support call-ins — `Ess.Easy.Airstrike`

One-tap presets over [`Ess.Support`](support)'s call-in primitives (shell/artillery/airstrike/bombingrun/
gunship/reinforce) — a jet flyby plus a few artillery shells, aimed at a point, your reticle target, or your
own position. See [Support & Call-ins](support) for the underlying mechanics this composes.

| Call | Does |
|---|---|
| `Ess.Easy.Airstrike.at(x, y, z)` | A jet flyby plus 4 artillery shells (10-unit scatter radius) on a world point — the one-tap barrage. |
| `Ess.Easy.Airstrike.onTarget(i)` | Same barrage, centered on whatever player `i` (default 0) currently has under their reticle. No-ops if nothing's targeted. |
| `Ess.Easy.Airstrike.onMe(i)` | Same barrage, centered on player `i`'s own position — the "call it in on yourself" gag. |

## Vehicles — `Ess.Easy.Vehicle`

| Call | Does |
|---|---|
| `Ess.Easy.Vehicle.summon(sTemplate, opts)` | The "I want a `<vehicle>`" one-liner: spawns `sTemplate` a short distance in front of you (`opts.dist`, default 18) at height (`opts.height`, default 10 — midair by default so an aircraft hovers the instant you're in it, a ground vehicle just settles) via `Ess.Object.spawnAhead`, then puts you in the best available seat (driver-first) via [`Ess.Vehicle.enterBestSeat`](identity-query#essvehicle). Returns the vehicle guid, or `nil` if the template name was wrong (spawn logs which). `opts.useView = true` places it along your view yaw instead of your body yaw — see [Core Primitives](core#essmath) for why those two differ. |

```lua
Ess.Easy.Vehicle.summon("UH1 Transport")
```

## Human & combat — `Ess.Easy.Human`

| Call | Does |
|---|---|
| `Ess.Easy.Human.giveWeapon(uChar, sTemplateName)` | Gives a character a weapon **by template name** (e.g. `"Grenade Launcher"`) with no spawning step. Resolves the template to a guid via `Pg.GetGuidByName` and equips it with [`Ess.Human.equipWeapon`](identity-query#esshuman). Live-confirmed to genuinely add a new weapon (an exact before/after `GetAllWeapons` count change, 2→3), not just re-equip something already held. `Pg.GetGuidByName` on a bad name just returns `nil` — no blank-template crash guard needed here the way `Pg.Spawn` needs one. |

## Impulse — `Ess.Easy.Impulse`

Mass-scaled launch/boost/knockback over [`Ess.Impulse.push`](identity-query#essimpulse) — a bike and a tank
feel the same push because the underlying impulse scales by `Object.GetMass`.

| Call | Does |
|---|---|
| `Ess.Easy.Impulse.speedBoost(uGuid, strength)` | A forward speed boost — the *Spy Hunter* effect this whole namespace is modeled on. Defaults to the vehicle you're driving if `uGuid` is omitted. `strength` defaults to 8 (the confirmed real recipe used 6–8). |
| `Ess.Easy.Impulse.launch(uGuid, strength)` | Pops something straight up — a hop, or a big launch. `strength` defaults to 12. |
| `Ess.Easy.Impulse.knockback(uGuid, fromGuid, strength)` | Shoves `uGuid` directly away from `fromGuid` (default source: you) with a slight upward lift — the "the blast sent them flying" feel. World-direction, mass-scaled. `strength` defaults to 10. |

## Player unlocks — `Ess.Easy.Player`

One-line wrappers around the game's own cheat-menu functions (most are exactly what
`MrxCheatBootstrap`/`mrxcheatbootstrap.lua` itself calls) — safe, confirmed toggles, not guesses.

| Call | Does |
|---|---|
| `Ess.Easy.Player.giveGrapplingHook()` | Unlocks the grappling hook (`MrxPmc.AddEquipment("GrapplingHook")`). |
| `Ess.Easy.Player.unlockFastTravel()` | Unlocks every landing zone (`MrxTransit.UnlockAllLandingZones`). |
| `Ess.Easy.Player.unlockAllHQs()` | Unlocks every HQ/outpost (`MrxHqManager.UnlockAllHq`). |
| `Ess.Easy.Player.giveAllRewards()` | Dispenses every unlock reward at once (`MrxRewardData.DispenseAllRewards`). |
| `Ess.Easy.Player.freeSupport(bOn)` | Ignores all airstrike/support stock + unlock requirements so any support call-in is free (`MrxSupportData.SetIgnoreRequirements`). `bOn` defaults to `true`; pass `false` to turn it back off. |
| `Ess.Easy.Player.ghost(bOn)` | **New in 0.3.1.** Floors your own AI detectability (`Ess.Relations.setPerceivability`, wrapping native `Ai.SetPerceivability`) so hostiles are far less likely to notice you; toggling back off restores your **exact original** value rather than a hardcoded default. Live-confirmed round-trip (90 → 30 → 90) via the `control_pursuit` smoke recipe. See [Encounter Toolkit](encounter-toolkit#relations) for the underlying `Ess.Relations` calls. |
| `Ess.Easy.Player.skin(sCode, i)` | Swaps player `i`'s whole-figure costume/skin via `Player.SetOutfit` — only a full `"*_hum_*"` model works, individual body parts don't. Confirmed codes include `"pmc_hum_fiona"`, `"pmc_hum_eva"`, `"pmc_hum_diablo"`, `"vz_hum_solano"`, `"al_hum_boss"`, `"ch_hum_boss"`, `"gr_hum_boss"`, `"civ_hum_beachfemale_a"`, `"police_hum_officer_b"` (~30 more in `sample-scripts-onload`). A reload restores your normal look. **A skin swap re-inits the model — its bones aren't ready for ~0.3s**, so wait a beat before attaching bone FX ([`Ess.Easy.Spawn.fxOn`](#spawning--esseasyspawn)) to a just-skinned character; see the [fresh-spawn readiness gotcha](camera-bones#essbones). |

## Fun — `Ess.Easy.Fun`

Pure for-the-lulz effects, both confirmed real functions:

| Call | Does |
|---|---|
| `Ess.Easy.Fun.dance()` | Your character does the "technoviking" dance (loads `player_mattias_bare_technoviking` and plays it via `Human.PlayRawAnimation`). Pure easter egg. |
| `Ess.Easy.Fun.fanfare(bWin)` | Plays the mission-success (or, with `bWin = false`, mission-fail) music sting via `MrxMusic.PlayFanfare` — the same call `mrxtaskcontract.lua` uses. Defaults to the win sting. |

## World — `Ess.Easy.World`

"Make the world do X" verbs. `.tint`/`.brightness`/`.hellscape` are **persistent by default**: crossing
into a new map zone re-applies that zone's own atmosphere and would otherwise silently overwrite your
custom look, so a lightweight `Ess.Loop` keeper watches `Graphics.Atmosphere.GetCurrentSetting` and snaps
your look back the instant a zone swaps it out. `resetAtmosphere()` stops the keeper for good.

| Call | Does |
|---|---|
| `Ess.Easy.World.removeMapBoundary()` | Drops the single "world boundary" fencing you into the story-unlocked map (`WifVzBoundary.RemoveWorldBoundary`, a real corpus call site) — including the Fiona-voiced warning + static. **Caveat: this is host/server-authoritative** — works in single-player and for the co-op host, but no-ops on a co-op *client*, and it only clears whichever main boundary is currently active. For a client-safe full unlock, use [`Ess.Player.removeBoundaries()`](identity-query#essplayer) instead (the confirmed-live per-player `Player.RemoveAllBoundary` loop) — kept as a separate verb here because it targets the *story* boundary system specifically, which is what a single-player roamer usually means. No clean restore. |
| `Ess.Easy.World.clearWanted()` | Instantly drops all pursuit/wanted heat (`Pg.ClearPursuitLock(true)`, a global — no import needed). One-shot only — heat can build right back up afterward. |
| `Ess.Easy.World.noPursuit(bOn)` | **New in 0.3.1.** Clears the current chase **and** keeps new organic heat from building back up, in one call (composes [`Ess.Pursuit.clear()` + `.restrictAll(true)`](pursuit#esseasyworldnopursuitbon--the-one-liner)) — reach for this over `clearWanted()` when a mod wants the player to *stay* cold (a safe-zone hub, a cutscene) rather than just reset once. `bOn` defaults to `true`; `noPursuit(false)` lifts the restriction only, it doesn't retroactively restart a cleared chase. |
| `Ess.Easy.World.tint(r, g, b)` | Washes the world in an ambient color, 0–255 each. Defaults to a deep red (220, 30, 30). |
| `Ess.Easy.World.brightness(n)` | Overall light level: ~0.05 is near-black, 1 is normal, above 1 blows out. |
| `Ess.Easy.World.hellscape()` | The confirmed dark + deep-red preset in one call (`brightness(0.08)` + the default red tint), and it sticks across zones like the other two. |
| `Ess.Easy.World.resetAtmosphere()` | Stops the zone-change keeper and calls `Graphics.Atmosphere.Restore` to let the natural look return. |

Built on the confirmed-live `Graphics.Atmosphere.Begin()`/`SetValue("fLightIntensity", n)`/
`SetColorValue("uiAmbientColor", r,g,b,255)`/`End(dur)` sequence — deliberately *not* the global
`SetTime`/`SetSky`/`SetTimeSpeed` setters, which were confirmed inert in live play.

## Camera — `Ess.Easy.Camera`

Zero-config presets over [`Ess.Camera`](camera-bones#esscamera), including two that take over the camera
entirely.

| Call | Does |
|---|---|
| `Ess.Easy.Camera.shake(i)` | Shakes player `i`'s camera with a medium preset (`"ShakeCameraMedium"`, amplitude 6, duration 5) — no preset name to remember. |
| `Ess.Easy.Camera.fadeOut()` / `.fadeIn()` | Full-screen fade to black / back in — named presets for `Ess.Camera.fade(1)` / `fade(0)`, no 0/1 to remember. |
| `Ess.Easy.Camera.watch(uGuid, opts)` | **Takes over the camera** for a cinematic shot of a target (e.g. a helicopter you just spawned). Default: a locked-off tracking shot — camera placed once, native `SetLookAt` panning to keep the target framed as it moves. `opts.chase = true` instead follows the target from a fixed angle around it (`opts.angle`); a *fixed* angle avoids the velocity-heading jitter an auto-trailing cam gets. Returns `stop()` — call it (or `Ess.Camera.panicRevert()` as a fire-blind escape hatch) to hand control back. **⚠ Tracking a moving vehicle:** point the look at whoever's riding it — `SetLookAt`'s object-track works on *character* bones, not vehicle hardpoints, so pass `opts = { look = pilotGuid, bone = "Bone_Chest" }`. |
| `Ess.Easy.Camera.orbit(uGuid, opts)` | **Takes over the camera** and smoothly orbits a target — per-tick position around a circle plus a re-issued `SetLookAt` every tick. `opts`: `radius` (12), `height` (4), `speed` in degrees/sec (40), `startAngle` (0), `look` (defaults to `uGuid`), `bone`, `i`. Returns `stop()`. |

```lua
local stop = Ess.Easy.Camera.orbit(spawnedGuid, { radius = 10, speed = 45 })
-- ...later:
stop()
```

Both `.watch` and `.orbit` steal camera control until stopped — always keep the returned `stop()` (or fall
back to `Ess.Camera.panicRevert()`). Note `Camera` here means the chase-cam/look-at/position/shake
namespace, distinct from `Graphics.Camera` (LOD/FOV/near-far) — see [Camera, Bones & Spatial](camera-bones)
for the full split.

## Time — `Ess.Easy.Time`

| Call | Does |
|---|---|
| `Ess.Easy.Time.slowmo(n, seconds)` | Zero-config slow-motion for the "explosion-impact/finisher-moment" case: applies [`Ess.Time.scale(n)`](timing-input#esstime) immediately (default `n = 0.2`) and schedules a single `Ess.Time.restoreScale()` after `seconds` (default 2) of **real** time via `Ess.Loop` — timed off `Ess.Time.stamp()`, deliberately not the scaled clock, or the restore would take `seconds / n` to actually fire. |

## Sound — `Ess.Easy.Sound`

| Call | Does |
|---|---|
| `Ess.Easy.Sound.play(sCueName)` | A plain UI one-shot sound cue, no guid/opts to think about — `Ess.Sound.cue(nil, sCueName)`. |

## UI — `Ess.Easy.Toast` / `.Confirm` / `.Menu`

The handful of single-call UI cases that don't need the full [`Ess.UI`](ui) widget-object API. `Ess.Gfx` is
the Raw tier under the UI kit; `Ess.UI` itself is already fairly friendly Core-tier, so most UI work doesn't
need an Easy tier at all — this is the thin sliver that does.

| Call | Does |
|---|---|
| `Ess.Easy.Toast(msg)` | Fire-and-forget notification — `Ess.UI.Toast(tostring(msg))`, no opts table. |
| `Ess.Easy.Confirm(text, onYes, onNo)` | A yes/no dialog with positional callbacks instead of an opts table; `onNo` is optional (default: do nothing). |
| `Ess.Easy.Menu(title, entries)` | Opens a **flat** one-level menu immediately — no `:category` nesting (use [`Ess.UI.Menu`](ui#essuimenu) directly if you need that, or `:switch`). `entries` accepts either an ordered array of `{label, fn}` pairs or a `{[label] = fn}` map (order not guaranteed for the map form, since it goes through `pairs()`). Each action receives the same `ctx` as the full builder (`ctx:hint/toast/confirm/ask/spawn/close`). |

```lua
Ess.Easy.Menu("MY TOOLS", {
  { "Heal me", function(ctx) Ess.Object.heal(Ess.Player.character(0)); ctx:toast("healed") end },
  { "Spawn a car", function(ctx) ctx:spawn("Veyron") end },
})
```

## Relations — `Ess.Easy.Relations`

The two genuinely common presets over [`Ess.Relations`](encounter-toolkit#relations), no
`{faction, faction, stance}` tuple vocabulary to learn. **Tracks exactly one internal handle** — calling
any of `makeHostile`/`makeAllies`/`war`/`sideWith` again first restores whatever the previous Easy-tier
call set, so it can't leak or stack. This is deliberate: guardrails for the common single-encounter case,
not the general multi-handle tool — use `Ess.Relations.apply` directly if you need more than one relation
set active at once.

| Call | Does |
|---|---|
| `Ess.Easy.Relations.makeHostile(factionList)` | Every faction in the list becomes hostile to PMC (you). |
| `Ess.Easy.Relations.makeAllies(factionList)` | Every pair *within* the list becomes mutually allied. |
| `Ess.Easy.Relations.war(a, b)` | Makes two factions fight **each other**, independent of the player — the faction-vs-faction case `makeHostile` can't express (`makeHostile` only ever means "hostile to PMC"). |
| `Ess.Easy.Relations.sideWith(friend, foe)` | You (PMC) join `friend` against `foe` in one call: PMC allies `friend`, PMC is hostile to `foe`, and `friend` is at war with `foe` — the whole stance for "I'm helping side A crush side B" (e.g. `sideWith("China", "Allied")`). |
| `Ess.Easy.Relations.restore()` | Undoes whatever the last Easy.Relations call set. Called automatically at the start of each of the four setters above. |

## Triggers — `Ess.Easy.Triggers`

The handful of single-purpose cases that cover most real usage over [`Ess.Triggers.arm`](encounter-toolkit#triggers),
no condition-spec table syntax to learn.

| Call | Does |
|---|---|
| `Ess.Easy.Triggers.onPlayerNear(x, y, z, r, fn)` | Calls `fn()` once the player gets within `r` of a point. |
| `Ess.Easy.Triggers.onDeath(uGuid, fn)` | Calls `fn()` when a specific object dies. |
| `Ess.Easy.Triggers.after(seconds, fn)` | Calls `fn()` once, after a delay. |

## AI orders — `Ess.Easy.AIOrders`

Named calls hiding the `opts` table, for the three most common orders over [`Ess.AIOrders.command`](encounter-toolkit#aiorders).

| Call | Does |
|---|---|
| `Ess.Easy.AIOrders.attack(guids, target)` | Orders a group of spawned units to attack a target guid. |
| `Ess.Easy.AIOrders.patrol(guids, points)` | Orders a group to patrol a list of `{x,y,z}` points. |
| `Ess.Easy.AIOrders.guard(guids, at)` | Orders a group to hold and defend a position — the friendlier name for the underlying `"defend"` behavior. |

## Sandbox — `Ess.Easy.Sandbox`

Begins with every built-in provider on, no provider list to think about — the "just isolate everything for
my arena/minigame" case, over [`Ess.Sandbox.begin`](encounter-toolkit#sandbox).

| Call | Does |
|---|---|
| `Ess.Easy.Sandbox.arena(id, opts)` | `Ess.Sandbox.begin(id, {"layers","economy","supports","relations"}, opts)` — all four providers isolated at once. |
| `Ess.Easy.Sandbox.done(id)` | `Ess.Sandbox.finish(id)` — restores everything `.arena` isolated. |

## Cinematic — `Ess.Easy.Cinematic`

| Call | Does |
|---|---|
| `Ess.Easy.Cinematic.play(steps, onDone)` | The zero-opts entry into [`Ess.Cinematic.play`](cinematic) — an ordered list of camera/spawn/say/fly/fade steps, skippable with ESC. |
| `Ess.Easy.Cinematic.shot(at, lookAt, seconds)` | Builds one static camera step (`{type="camera", at=, lookAt=, hold=seconds}`) — storyboard sugar so a hand-authored steps list reads as `{ shot(a,b,4), shot(c,d,3), ... }`. `seconds` defaults to 3. |

## Objectives & quests — `Ess.Easy.Objective` / `.Quest`

One-line goal tracking over [`Ess.Objective`/`Ess.Quest`](objectives) — a stateful HUD goal (or an ordered
sequence of them) already wired to a world event, no manual event glue on your side. See
[Objectives & Quests](objectives) for the underlying classes and step-definition shapes.

| Call | Does |
|---|---|
| `Ess.Easy.Objective(label, target, onComplete)` | A manual counted goal on the HUD objective line — advance it yourself with `:advance()`. Callable table, not a `.new{}` constructor. |
| `Ess.Easy.Objective.reach(x, y, z, r, label, onDone)` | Completes the instant the player steps within `r` (default 8) of a point; drops a "go here" ground ring. |
| `Ess.Easy.Objective.destroy(uGuid, label, onDone)` | Completes when that object dies; marks it on radar/PDA/world. |
| `Ess.Easy.Objective.clear(x, y, z, r, faction, label, onDone)` | Completes once every `faction` unit in the radius (default 40) is dead — shows "N left" on the HUD, polled once a second. |
| `Ess.Easy.Objective.survive(seconds, label, onDone, onFail)` | A live countdown goal; fails if the player dies before `seconds` elapses. |
| `Ess.Easy.Quest(steps, onComplete)` | A whole linear mission in one table — an ordered list of `reach`/`destroy`/`clear`/manual steps, each auto-wired and self-marking. |

## Missions — `Ess.Easy.Contract`

The one Core-tier namespace that had **no** Easy tier at all until this was added — previously a beginner
had to learn `Register`/`def.id`/`Accept` just to get "kill these guys" or "go here" working. Both
register **and accept** a single-objective contract in one call, over [`Ess.Contract`](contract).

| Call | Does |
|---|---|
| `Ess.Easy.Contract.destroy(sTitle, tSpawns, tOpts)` | A one-objective "destroy these" contract. `tSpawns = { {template, x, y, z, yaw?}, ... }` — same shape as the Core `Destroy` builder's `spawns`. |
| `Ess.Easy.Contract.reach(sTitle, at, radius, tOpts)` | A one-objective "go here" contract. `at = {x, y, z}`. |

Both take `tOpts = { desc =, reward = {cash=, fuel=} }` and return the generated contract id (`"easy1"`,
`"easy2"`, …, auto-incrementing per call).

```lua
Ess.Easy.Contract.destroy("Raid the Depot", {
  { "Veyron", x + 18, y, z + 6, 0 },
  { "Veyron", x + 18, y, z - 6, 0 },
}, { reward = { cash = 20000, fuel = 60 } })
```

## Debug — `Ess.Easy.Debug`

A live on-screen dev panel for mod authors — position, aim target, vehicle/health, nearby counts — built on
[`Ess.UI.Panel`](ui#essuipanel). See [Debug & Dev Tools](dev-tools) for the full writeup. **Live-verified as
of 0.3.0** — the CHANGELOG's dated verification entry confirms the overlay renders in-game.

| Call | Does |
|---|---|
| `Ess.Easy.Debug.overlay(opts)` | Toggles the panel on/off (call again to hide); returns the panel, or `nil` when toggled off. `opts` (all optional): `x`, `y` (screen position), `interval` (refresh seconds, default 0.2), `radius` (nearby-scan radius, default 40), `i` (player index). |
| `Ess.Easy.Debug.hide()` | Forces it off. |
| `Ess.Easy.Debug.isOn()` | Returns whether it's currently on. |

## See also

- [Essentials (Ess)](index) — the framework index, including the three-tier model this page is the top of.
- Every section above links sideways to its own Core-tier drilldown page for the full parameter set, the
  Raw-tier primitives, and anything the one-liner deliberately doesn't expose.
- [Debug & Dev Tools](dev-tools) — `Ess.Easy.Debug`'s live dev overlay and `Ess.Easy.Console.play()`'s
  interactive playground, in full.
- `Ess.Easy.Console.open()` — the same content as this page, live and searchable, in-game.
