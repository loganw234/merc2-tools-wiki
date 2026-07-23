---
title: Encounter Toolkit
parent: Essentials (Ess)
nav_order: 9
---

# Encounter Toolkit

## Overview

`Ess.AIOrders`, `Ess.Relations`, `Ess.Triggers`, `Ess.Sandbox`, and `Ess.Layers` are the gameplay-scripting
machinery that originally lived inside `ContractFramework.lua` — grouped-unit AI commands, temporary faction
stances, the trigger/condition vocabulary, and save-clean ephemeral-mode isolation. All five have been
extracted into standalone `Ess.*` namespaces: **none of them need a running `Ess.Contract` instance
anymore.** `Ess.Contract` still uses them internally (a contract's `def.waypoints`/`def.relations`/
`def.support`/`def.triggers` are thin wrappers over exactly these namespaces), but a mod can now spawn a
squad, flip two factions to war, arm a proximity trigger, or run an isolated arena minigame with no contract
in play at all.

The underlying design — trigger condition types, AI order behaviors, relation stances — was worked out and
documented first against the standalone Contract Framework:

- [Units, AI Orders & Relations](../contract-framework/units-ai-and-relations) — the original `def.units`/
  `def.waypoints`/`def.relations` design `Ess.AIOrders`/`Ess.Relations` are a native port of.
- [Support Effects & Triggers](../contract-framework/support-effects-and-triggers) — the original
  `def.support`/`def.triggers` design `Ess.Triggers`' condition vocabulary is a native port of.

This page documents the current `Ess.*` API surface as it actually exists in source now, verified directly
against `60_aiorders*.lua` through `64_layers.lua` — some details have evolved from the standalone version
(most notably: **handles instead of ids** for `Ess.Relations`, and **scopes instead of a shared table** for
`Ess.Triggers`' named triggers/gates, both structural fixes for id-collision bugs the original single-table
designs had). Where this page's tables diverge from the two pages above, this page's source read is the
current source of truth.

Three-tier design applies selectively here: `AIOrders`, `Relations`, `Triggers`, and `Sandbox` all carry
`Raw`/Core/`Easy` tiers. `Layers` is single-tier (absorbed whole from the standalone Layer Framework
library) — reach for it directly, or through `Ess.Sandbox`'s `"layers"` provider.

## AIOrders

Command a spawned unit **group** — one call moves, attacks, patrols, or otherwise orders every guid in a
list at once. Built only on `Ai.Goal`/`Ai.Anchor`/`Ai.Deploy` primitives, exactly as `ContractFramework.lua`
already used them — nothing here is a new native capability.

### Raw

| Function | Signature | Notes |
|---|---|---|
| `pri` | `Ess.Raw.AIOrders.pri(p)` | Normalizes `"hi"`/`"high"`, `"med"`/`"medium"`, `"lo"`/`"low"` (case-insensitive) to the engine's `"HiPri"`/`"MedPri"`/`"LoPri"` strings. Anything unrecognized (including `nil`) falls back to `"HiPri"`. |
| `actor` | `Ess.Raw.AIOrders.actor(g)` | **The rule every behavior depends on**, ported from `ContractFramework.lua`'s `aiActor`: an AI goal must target the **driver** of a vehicle guid, not the vehicle hull — `Vehicle.GetDriver(g)` if that succeeds and returns something, else `g` itself. Ordering a vehicle guid directly silently does nothing without this. |
| `goal` | `Ess.Raw.AIOrders.goal(args)` | `pcall`-wrapped `Ai.Goal(args)` — returns the handle, or `false` on error. |
| `haste` | `Ess.Raw.AIOrders.haste(g, speed)` | `pcall`-wrapped `Ai.SetHaste(g, speed)` — no-op if `speed` is `nil`. |
| `priorityTarget` | `Ess.Raw.AIOrders.priorityTarget(g)` | `pcall`-wrapped `Ai.SetPriorityTarget(g)` — marks `g` as the priority target for hostile AI. Confirmed real (`resident/mrxsupport.lua`, `resident/outpost.lua`); the standalone primitive for a boss-fight or escort-defense scenario, outside the group `command()` dispatcher. |
| `enable` | `Ess.Raw.AIOrders.enable(g, bOn)` | `pcall`-wrapped `Ai.Enable(g, bOn)` — toggles whether the AI system drives `g` at all. Confirmed real (`resident/mrxactionhijack.lua`, `resident/mrxutil.lua`); freezes a subject in place for a scripted/cutscene beat, then hands control back. |

### Core

```lua
Ess.AIOrders.setGroup(name, guids)   -- register a named group
Ess.AIOrders.group(name) -> guids    -- read it back (empty table, never nil, for an unknown name)
Ess.AIOrders.command(guids, behavior, opts, tracker) -> ok
```

`setGroup`/`group` is a standalone stand-in for `ContractFramework`'s `inst.groups` — it lets `attack`/
`follow`/`enter` target **another** named group without needing a contract instance to hold the registry.

`command` dispatches to one of eleven built-in behaviors, `pcall`-wrapped (a bad behavior name or a runtime
error is logged and returns `false` rather than crashing the caller). `tracker`, if given (an `Ess.Track` —
see [Tracking & Cleanup](tracking)), receives any spawned anchor prop (`defend`) or scheduled follow-up
event (`follow`) for cleanup.

| `behavior` | Does |
|---|---|
| `move` | `Ai.Goal{Goal="MoveToPos"}` to `opts.at` — go there and stop. `Force=true`. |
| `face` | `Ai.Goal{Goal="Face"}` turning to face `opts.at` (`Position=true`) — no movement; staging/cutscene framing. `HiPri`. |
| `hold` | `Ai.Anchor{AnchorRadius=0}` + `Ai.Goal{Goal="Idle"}` — stand exactly where spawned, don't give chase. `HiPri`. |
| `defend` | Spawns an invisible `TinyGeometry` anchor at `opts.at` (registered on `tracker` if given), moves the group there, then `Ai.Anchor`s each member to that anchor with `opts.radius` (default 12) — holds an area, fighting anything that enters it. |
| `attack` | Hunts `opts.target` (the **first** guid of that named group, via `Ess.AIOrders.group`) if given, else the nearest local player (`Player.GetLocalCharacter`). Falls back to a plain `MoveToPos` toward `opts.at` if no target resolves at all. Default priority `"med"` (every other behavior defaults `"hi"`). |
| `patrol` | Walks `opts.points` in order via chained `MoveToPos` goals — each goal's `Callback` re-issues the next point on arrival. Loops unless `opts.loop == false`, or there's only one point (a single-point "patrol" quietly becomes a plain one-shot move instead of a wasteful one-point loop). |
| `follow` | Re-issues a `MoveTo` toward `opts.target`'s group (or the nearest player) every `opts.interval` seconds (default 4), via a self-rescheduling `Event.TimerRelative` — a simple re-issued tail, not a native follow behavior. **Reschedules forever** until cancelled — pass a `tracker` so the timer is cleaned up when the scene/mode ends, or it keeps ticking after the actor is no longer relevant. |
| `flee` | A single `MoveToPos` directly away from the nearest player, `opts.distance` units (default 120) — one-shot, doesn't keep re-fleeing on a timer. `HiPri`. |
| `enter` | Boards a vehicle: resolves `opts.target` as a group name first, falling back to `Pg.GetGuidByName`, then issues `Ai.Goal{Goal="Enter", Role=opts.role or "passenger"}` for each guid. `HiPri`, `Force=true`. |
| `deploy` | `Ai.Deploy{Role="Passenger"}` on each guid — `guids` here are expected to be the transport vehicles themselves; a transport disgorges its passengers. `HiPri`, `Force=true`. |
| `animate` | `Human.DoAction(g, opts.action or "Cower")` — plays a canned action pose. |

All behaviors route the acting guid through `Ess.Raw.AIOrders.actor()` first (see Raw tier above), and most
apply `opts.speed` via `haste()`. `opts.priority` (`"hi"`/`"med"`/`"lo"`) is honored by `move`/`defend`/
`attack`/`patrol`/`follow`.

### Easy

`Ess.Easy.AIOrders` covers the three most common orders as one-liners: `attack(guids, target)`,
`patrol(guids, points)`, and `guard(guids, at)` (the friendlier name for `"defend"`). See
[Ess.Easy](easy) for the full one-liner catalog.

### Example

From the shipped `command_a_squad.lua` recipe:

```lua
local squad = {}
for i = 1, 3 do
    local g = Ess.Object.spawn("VZ Soldier", px + 12, py, pz + 6 + i * 2)
    if g then squad[#squad + 1] = g end
end
Ess.AIOrders.command(squad, "move", { at = { x = px, y = py, z = pz } })
```

## Relations

Named, **handle-based** faction-pair stance sets, applied and restored as one unit. Unifies the same
snapshot → apply → restore pattern that existed independently twice (`ContractFramework.lua`'s
`def.relations`, and `WaveDefense.lua`'s own `setupRelations`/`restoreRelations`) into one implementation.

Handle-based specifically so two independent callers can never collide: an earlier id-keyed version shared
one flat module table, so two callers reusing a generic id like `"combat"` could restore/overwrite each
other's set. `apply()` now mints its own opaque handle carrying its own snapshot; `restore(handle)` undoes
exactly that one apply and nothing else. There's no global "restore everything," because there's no longer
any global registry to collide in — hold the handle yourself (a local var, an `Ess.Track`, or an instance
field) until you restore it.

### Raw

| Function | Signature | Notes |
|---|---|---|
| `snapshot` | `Ess.Raw.Relations.snapshot(ga, gb) -> {ok, val}` | `pcall`-wrapped `Ai.GetRelation(ga, gb)`. **`ok` is the load-bearing field**: it distinguishes "read a real value" from "the read itself failed." Collapsing those two (as `ContractFramework.lua`'s original `_applyRelations` did, `o1ok and o1`) loses the distinction between a genuine `0` (neutral) and "unknown" — Lua's `and` short-circuits to `false` the instant `ok` is false, silently skipping that direction's restore forever. |
| `set` | `Ess.Raw.Relations.set(ga, gb, val) -> ok` | `pcall`-wrapped `Ai.SetRelation(ga, gb, val)`. |
| `restore` | `Ess.Raw.Relations.restore(ga, gb, snap) -> ok` | Fix for the gap above (documented in source as "Known Bug #3"): if the original read failed (`snap.ok == false`), there is genuinely nothing to restore to — this **logs it honestly and returns `false`** instead of silently no-oping. If the read did succeed, always restores, even when the original value itself was `0` (neutral is a real, valid value to restore). |

### Core

```lua
Ess.Relations.apply(pairsList [, label]) -> handle
Ess.Relations.restore(handle)
Ess.Relations.isActive(handle) -> bool
Ess.Relations.getFeeling(uGuidA, uGuidB) -> n
Ess.Relations.setFeeling(uGuidA, uGuidB, n)
Ess.Relations.getPerceivability(uGuid) -> n, nFloor
Ess.Relations.setPerceivability(uGuid, n) -> ok
```

`pairsList` entries are `{a, b, set}` or `{a=, b=, set=}`. `set` is one of the stance names below
(case-insensitive) or a raw number:

| `set` value | Numeric | 
|---|---|
| `"friend"` / `"ally"` / `"allied"` | `100` |
| `"neutral"` | `0` |
| `"enemy"` / `"hostile"` | `-100` |

`apply` sets **both directions** (`a→b` and `b→a`) to the same value — a mutual stance, not a one-way read
— and snapshots both directions individually before doing so. When one side of a pair is `"PMC"` (the
player's own faction), it also calls `MrxFactionManager.SetAttitudeMutable` on the *other* faction's
abbreviation first (`Allied`→`"All"`, `China`→`"Chi"`, `Guerilla`→`"Gur"`, `OC`→`"Oil"`, `Pirate`→`"Pir"`,
`VZ`→`"VZ"`, `PMC`→`"Pmc"`) — the same call the story missions use to make a faction's attitude toward the
player actually able to change (a faction with `bDynamic = false` can't be moved regardless of what
`Ai.SetRelation` is told). An unresolvable faction name (`Pg.GetGuidByName` fails for either side) is
logged and that pair is skipped, not a hard error.

`restore(handle)` is idempotent — restoring an already-restored or `nil` handle is a safe no-op.
`isActive(handle)` reports whether it hasn't been restored yet.

`getFeeling`/`setFeeling` wrap `Ai.GetFeeling`/`Ai.SetFeeling` — an **individual-pair** relationship value,
distinct from the per-**faction** `apply`/`restore` above (confirmed real usage: `mrxfollow.lua` calls
`SetFeeling(uGuid, uTarget, 100)` to neutralize hostility on one specific subject before starting a scripted
"Follow" role, without touching that subject's whole faction's stance). No snapshot/restore needed for
these — they're thin direct wrappers.

**Live gotcha confirmed in source comments:** a freshly `Pg.Spawn`'d character's feeling reads back as a
stale `0` if queried in the same tick as the spawn — the same class of "needs a moment to settle" delay
documented elsewhere for bone/hardpoint reads. Wait at least one tick after spawning before calling
`getFeeling`/`setFeeling` on a target you just created.

`getPerceivability`/`setPerceivability` wrap `Ai.GetPerceivability`/`Ai.SetPerceivability` (see
[Ai](../namespaces/ai)) — yet another per-**individual** stat, but not a relationship between two subjects
like `getFeeling` above: it's one subject's own AI *detectability*. `getPerceivability(uGuid)` returns `n`
(the current value) and `nFloor` (that subject's own engine-side floor), or `nil` if the read failed;
`setPerceivability(uGuid, n)` drives it and returns whether the call itself succeeded.

Both are new in **v0.3.1** — the 2026-07-22 "bindings-pass harvest" (`CHANGELOG.md`'s `[0.3.1]` entry), the
same batch that mapped a set of the engine's never-called `luaL_Reg` bindings and shipped wrappers only over
live- or corpus-confirmed calls. Verified the same way the rest of that release was: offline first
(`checkpure` 10/10, `test_bundles` all green), then a full in-game pass on the 2026-07-22 release build.
**Confirmed live as of 0.3.1, and specifically reversible:** that pass drove a subject's perceivability
`90 → 30 → 90`, reading it back with `getPerceivability` between steps — the value actually moved and
round-tripped to its exact starting point, not just "the call executed without erroring." Same fresh-spawn
settle caveat as `getFeeling`/`setFeeling` above applies here too: wait at least one tick after spawning
before querying a target you just created.

### Easy

`Ess.Easy.Relations` tracks **one handle internally**, so only one easy-tier relation set can be active at a
time — deliberate: this tier is guardrails for the common single-encounter case, not the general
multi-handle tool (use `Ess.Relations` directly for that). Calling any of these again first restores
whatever the previous easy-tier call set, so it can't leak or stack: `makeHostile(factionList)` (every
listed faction becomes hostile to PMC), `makeAllies(factionList)` (every pair within the list becomes
mutually allied), `war(a, b)` (two factions fight each other, independent of the player — the case
`makeHostile` can't express), `sideWith(friend, foe)` (PMC allies `friend`, is hostile to `foe`, and
`friend`/`foe` go to war — one call for "I'm helping side A crush side B"), and `restore()`. See
[Ess.Easy](easy) for the full catalog.

A related one-liner lives in a different namespace, but it's built directly on `setPerceivability` above so
it's worth covering here too: **`Ess.Easy.Player.ghost(bOn, i)`** (`src/93_easy_unlocks.lua`) is the
Easy-tier stealth toggle. It floors player `i`'s (default `0`) own character detectability down to whatever
`getPerceivability` currently reports as that character's floor — call it again, or pass `false` explicitly,
to turn it back off; omit `bOn` entirely to just toggle. The detail worth stating plainly: turning it off
restores your **exact original** perceivability, not a hardcoded fallback value — the actual number
`getPerceivability` read back at the moment ghost switched on is what gets replayed, held in `Ess.State` so a
reload-safe `OnKey` re-run toggles instead of clobbering that saved value with a second floor.

New in the same **v0.3.1** "bindings-pass harvest" as `getPerceivability`/`setPerceivability` above.
`CHANGELOG.md` is explicit that it's "Registered in the Console + playground" — it's in
`Ess.Easy.Console`'s browsable one-liner registry and its `.play()` playground under the **Player** group
(see [Debug & Dev Tools](dev-tools#esseasyconsoleplay) for both). **Confirmed live as of 0.3.1:** the smoke suite's
new `control_pursuit` recipe explicitly exercises "ghost lowering perceivability then restoring the exact
original" as part of the release's 42/42-passing in-game run on the 2026-07-22 build — the exact-restore
behavior above is what was actually tested, not just what the source comments claim.

### Example

From the shipped `make_them_fight.lua` recipe:

```lua
local handle = Ess.Relations.apply({ { "China", "Allied", "hostile" } }, "recipe_war")
local snap = Ess.Raw.Relations.snapshot(Ess.Guid("China"), Ess.Guid("Allied"))
-- snap.val == -100
Ess.Relations.restore(handle)
```

## Triggers

The full condition vocabulary — extracted from `ContractFramework.lua`'s `armTrigger`, generalized away
from a running contract instance. This is the piece with the most moving parts in this group.

### Raw — the condition vocabulary

```lua
Ess.Raw.Triggers.arm(spec, onFire, tracker) -> cancel()
```

Stateless: fires `onFire()` once its condition is met, or immediately for the always-true specs.
`tracker` (an `Ess.Track`), if given, receives every scheduled `Event.Create` handle this trigger uses, for
cleanup. The returned `cancel()` stops the trigger from ever firing, even if its condition is later met.

| `spec =` | Fires when |
|---|---|
| `nil` or `"immediate"` (default if omitted) | Right away, synchronously, the instant `arm` is called. |
| `"once"` (shorthand for `{once = 3}`) or `{once = seconds}` | Once, after a fixed delay. |
| `"recurring"` (shorthand for `{recurring = 10}`) or `{recurring = interval, limit =, delay =}` | Every `interval` seconds, forever or up to `limit` times. First fire after `delay` seconds (default = `interval`). |
| `{proximity = radius, at = {x,y,z}}` | The local player gets within `radius` of a point — polled every 0.4s (`Player.GetLocalCharacter` + `Object.GetPosition`, flat XZ distance check). |
| `{onDestroy = "PlacedName"}` | A specific **named** placement (resolved via `Pg.GetGuidByName`) dies — watched with `Event.ObjectDeath`, no polling. Logs and gives up if the name doesn't resolve at all. |
| `{onDestroy = "nearest"}` or `{onDestroy = {at=, radius=, kind=}}` | Polls (every 1s, via `Ess.Probe.nearby`) the area for the nearest object matching `kind`, within `radius` (default 45) of `at` (falls back to `spec.at`) — once one is found, watches **that specific object** die. For a target that may not exist yet when the trigger arms (e.g. a spawned objective target). |
| `{onHealthBelow = {target=, pct=}}` | `target`'s health drops below `pct`% (default 50) of whatever it read as on the **first successful poll** (i.e. "at arm time," polled every 0.5s starting immediately) — not necessarily full/max health if the target was already damaged when the trigger armed. |
| `{onCleared = {at=, radius=, kind=, faction=}}` | An area (`radius`, default 45, via `Ess.Probe.nearby`) that had at least one matching object in it now has zero — a "wave wiped out" check. Only counts once something was actually observed there first (polled every 0.8s), so an already-empty area doesn't fire immediately. |

**Not ported:** `onObjComplete` (fires on a top-level *contract* objective index) — that concept only exists
inside a running `Ess.Contract` instance and is handled there locally rather than generalized into this
standalone file. For cross-trigger logic beyond a single condition, compose triggers through a scope's
`:gate` (below) instead.

An unrecognized spec logs `"Triggers.arm: spec table matched no known condition"` and returns a no-op
`cancel`.

### Core — named triggers and logic gates

```lua
Ess.Triggers.arm(spec, onFire, tracker) -> cancel()          -- passthrough to Ess.Raw.Triggers.arm
Ess.Triggers.scope() -> scope                                 -- an ISOLATED named-trigger/gate namespace
  scope:arm(spec, onFire, tracker) -> cancel()
  scope:armNamed(id, spec, onFire, tracker) -> cancel()
  scope:gate(inputs, need, onFire, tracker) -> cancel()
  scope:declare(id)
  scope:markFired(id)
```

`Ess.Triggers.arm` stays a bare top-level call because it's stateless — it never names anything or shares a
table. Named triggers and gates need to cross-reference each other **by name**, though, which requires
shared state — and an earlier version kept that state in one module-level pair of tables (`_known`/`_fired`)
shared by every caller in the game. Two independent systems both calling `armNamed("start", ...)` would
silently collide: one's trigger firing would satisfy the other's unrelated gate. `Ess.Triggers.scope()` is
the structural fix — each scope owns its own private `_known`/`_fired`, so two scopes can't interfere no
matter what ids they reuse; the collision is impossible by construction, not merely documented as a risk.
`Ess.Contract` gives each running contract instance its own scope; a direct caller should make one per
independent group of triggers.

- `scope:armNamed(id, spec, onFire, tracker)` — like `arm`, but registers `id` in *this* scope so a later
  `scope:gate` can name it as an input, and marks it fired the moment it fires.
- `scope:declare(id)` / `scope:markFired(id)` — for an id whose firing is driven by something other than
  `armNamed` (a custom poll, or a gate's own id needing to be referenceable by another gate). `declare`
  makes a gate's input-validation accept the id; `markFired` records that it fired — call it **before**
  running the id's own action, so a chained gate observes it as satisfied in the same tick.
- `scope:gate(inputs, need, onFire, tracker)` — fires once `need` (default: **all** of them) of the named
  `inputs` have fired in this scope. Validates every input against this scope's known ids and logs loudly
  on any that were never armed/declared (a gate that can never be satisfied) or an empty `inputs` list (a
  gate that polls forever) — it fails loud instead of silently never firing. Polls every 0.4s. Gates chain:
  a gate firing marks *itself* as fired too, so it can feed into another gate's `inputs`.

### Easy

`Ess.Easy.Triggers` covers the three single-purpose cases that cover most real usage, no spec-table syntax
required: `onPlayerNear(x, y, z, r, fn)`, `onDeath(uGuid, fn)`, `after(seconds, fn)`. See
[Ess.Easy](easy) for the full catalog.

## Sandbox

Begin/finish an ephemeral, **guaranteed-restored** mode across every registered provider at once, with
saves gated for the whole duration — the single biggest unifying idea in this group. Unifies the standalone
Layer Framework's begin/add/remove/swap/expect/finish pattern (snapshot → apply → guaranteed restore,
save-gated so a crash mid-mode just leaves the pre-mode vanilla state) with `WaveDefense.lua`'s
independently-built cash isolation into one implementation, one save-gate, four built-in providers.

### Raw

```lua
Ess.Raw.Sandbox.register(name, { apply = fn(id, opts), restore = fn(id) })
Ess.Raw.Sandbox.gateSaves() / .ungateSaves()
```

`register` adds a provider (a `{apply=, restore=}` table) under `name` for anything not covered by the four
built-ins. `gateSaves`/`ungateSaves` delegate to the one shared `Ess.Save` gate (see
[Tracking & Cleanup](tracking)) under a fixed generic holder key — this pair exists only for a Raw-tier
provider author who wants to gate saves by hand outside the full `Sandbox` lifecycle; `Ess.Sandbox.begin`/
`.finish` (below) don't use it, they hold `Ess.Save` keyed by each sandbox's own id instead, so concurrent
sandboxes gate independently.

### Core

```lua
Ess.Sandbox.begin(id, providerNames, opts) -> ok
Ess.Sandbox.finish(id)
Ess.Sandbox.isActive(id) -> bool
```

`begin` gates saves for this sandbox id, then calls each named provider's `apply(id, opts)` in order. A
provider that errors is logged and skipped — it's simply not added to this id's active-provider list, so
`finish()` won't try to restore something that never successfully applied. If **every** named provider was
unknown or failed (nothing was actually isolated), `begin` releases the save-gate holder it took and does
**not** mark the id active — so a `false` return truly means there's nothing to `finish()`, and no save-gate
holder is left stranded from a typo'd provider name.

`finish(id)` restores every provider that successfully applied, in order, then releases this sandbox's
save-gate holder — saves resume only once the **last** holder anywhere (any other sandbox, or `Ess.Layers`)
is also gone.

Four built-in providers:

| Provider | `apply(id, opts)` | `restore(id)` |
|---|---|---|
| `"relations"` | If `opts.relations` is given, `Ess.Relations.apply(opts.relations, "sandbox:"..id)` — the resulting handle is stashed by sandbox id. | `Ess.Relations.restore()` on that stashed handle. |
| `"economy"` | Reads the current campaign cash (`MrxPmc.GetCashQty`), saves it via `Ess.SaveVar`, then zeroes the wallet (`MrxPmc.AddCashQty(-cash, ...)`) — or sets it to `opts.startCash` instead if given. | Restores the saved cash exactly, by adding the delta between the saved value and whatever the current value drifted to. |
| `"supports"` | Snapshots the HUD support quick-select menu's current items (via `MrxGuiBase.GetWidgetByNameAndOwner("Support Menu", player)`), then clears it (`RemoveAll`). Existence-checked, not a hard failure — no-ops if the widget lookup fails (e.g. `MrxGuiBase` unavailable). | Clears the menu again, then re-adds every saved item via `Hud.SupportMenu:AddItem`. |
| `"layers"` | `Ess.Layers.begin(id)`. | `Ess.Layers.finish()`. |

The `"economy"` provider's persistence via `Ess.SaveVar` means a mid-session inspection can see the saved
amount, but — unlike `WaveDefense.lua`'s own single-global-key version — it does **not** auto-recover a
stranded deduction from a crashed prior session, since `Loader.SaveVar`/`LoadVar` has no key-enumeration API
to discover an arbitrary caller's sandbox id at boot. This is a documented, deliberate scope reduction, not
an oversight.

### Easy

`Ess.Easy.Sandbox.arena(id, opts)` turns on all four built-in providers at once — the "just isolate
everything for my arena/minigame" case, no provider list to think about. `Ess.Easy.Sandbox.done(id)` is
`finish(id)`. See [Ess.Easy](easy) for the full catalog.

### Example

From the shipped `an_arena.lua` recipe:

```lua
Ess.Easy.Sandbox.arena("recipe_arena")     -- isolation on, saving gated
-- ... minigame runs here; saves suppressed, state is scratch ...
Ess.Easy.Sandbox.done("recipe_arena")      -- restores layers/economy/relations, re-enables saving
```

## Layers

Safe, save-clean runtime manipulation of the `vz_state_*` dynamic layer system, for ephemeral modes
(arenas, minigames). Absorbed whole from the standalone `LayerFw.lua` (mercs2-layer-framework) — the last
of the four originally-separate frameworks to be absorbed into `Ess`, now native rather than an adopted
external dependency. Single-tier (no `Raw`/`Easy` split) — reach for it directly, or through
`Ess.Sandbox`'s `"layers"` provider, which is what most callers actually use.

Everything routes through `MrxLayerManager` — never raw `Pg.LoadLayer`/`UnloadLayer` — so its
`_tLoadedLayers` bookkeeping (the single source of truth the native save reads) stays authoritative and
consistent with the world at all times. **STATIC layers (terrain/geometry) are refused outright** — they
must never be touched mid-session. Layer changes apply for a mode's duration and are **always** restored on
`finish()`; saves are gated (no-op'd) the whole time via the shared `Ess.Save` gate, so a crash mid-mode
just leaves the pre-mode vanilla save on disk — nothing to recover.

| Function | Signature | Notes |
|---|---|---|
| `begin` | `Ess.Layers.begin(sId)` | Opens a mode: snapshots the current set of loaded dynamic layers as the baseline, gates saves. Returns `false` if a mode is already active — only one mode at a time. |
| `add` | `Ess.Layers.add(vLayers, fCb)` | Loads layer(s) (a string or a list); culls duplicates/nonexistent entries; refuses (logs, skips) any STATIC layer. |
| `remove` | `Ess.Layers.remove(vLayers, fCb)` | Unloads layer(s); same static-layer refusal. |
| `swap` | `Ess.Layers.swap(vRemove, vAdd, fCb)` | Remove-then-add, sequenced (`MrxLayerManager.Remove`'s callback chains into `.Add`) — the mission idiom. |
| `expect` | `Ess.Layers.expect{present=, absent=, cb=}` | Declarative convergence: diffs the declared set against what's actually currently loaded and issues only the minimal add/remove — fixes drift instead of blindly re-applying everything. |
| `composite` | `Ess.Layers.composite(fCb)` | Optional: forces a visible recomposite via `MrxState` (enters `STATE_WAITFORGAME` then `STATE_WAITFORSTREAMING`). Not needed if the mode also teleports/fast-travels the player (that composites for free). Best-effort — logs and no-ops if `MrxState` is unavailable. |
| `finish` | `Ess.Layers.finish(fCb)` | Restores **exactly** to baseline — diffs current state vs. the recorded baseline (not the tracked delta), so it's correct even if something else changed layers mid-mode — then un-gates saves. |
| `isActive` | `Ess.Layers.isActive()` | `true` while a mode is open. |
| `isLoaded` | `Ess.Layers.isLoaded(name)` | Reads `MrxLayerManager._tLoadedLayers` directly. |
| `snapshot` | `Ess.Layers.snapshot()` | The baseline set captured at `begin()`, as a list. |
| `current` | `Ess.Layers.current()` | The live, currently-loaded dynamic-layer set, as a list. |

Save-gating uses the shared `Ess.Save` gate under a fixed holder key (`"Ess.Layers"`) — safe as a fixed key
because only one `Layers` mode can ever be active at a time (`begin()` refuses a second). This is the same
mechanism `Ess.Sandbox` and `Ess.Raw.Sandbox.gateSaves()` use, structurally preventing either from ever
clobbering the other's gate.

## See also

- [Essentials (Ess)](index) — the framework index this page belongs to.
- [Units, AI Orders & Relations](../contract-framework/units-ai-and-relations) / [Support Effects & Triggers](../contract-framework/support-effects-and-triggers) — the original standalone-Contract-Framework design these namespaces are a native port of.
- [Cinematic](cinematic) — `Ess.Cinematic`'s `order`/`spawn`/`relations` steps drive `AIOrders`/`Relations` directly as cutscene timeline steps.
- [Contract Engine](contract) — `Ess.Contract`'s `def.waypoints`/`def.relations`/`def.support`/`def.triggers` are built on exactly these namespaces.
- [Tracking & Cleanup](tracking) — `Ess.Track` (the `tracker` argument throughout this page) and the shared `Ess.Save` gate.
- [Ess.Easy](easy) — the full one-liner catalog, including every `Easy` tier mentioned above.
- [Ai](../namespaces/ai) — the native `GetPerceivability`/`SetPerceivability` primitives `Ess.Relations` wraps.
- [Debug & Dev Tools](dev-tools#esseasyconsoleplay) — `Ess.Easy.Console`'s browsable reference and `.play()` playground, where `Ess.Easy.Player.ghost` is registered under the Player group.
