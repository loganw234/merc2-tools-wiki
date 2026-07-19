---
title: Essentials (Ess)
parent: Frameworks
nav_order: 1
has_children: true
has_toc: false
---

# Essentials (Ess)

> **Status: this supersedes the other frameworks.** [UI Kit](../uilib/), [ModNet](../modnet), and the
> [Contract Framework](../contract-framework/) — plus the standalone Layer Framework — are now absorbed as
> native `Ess.*` code (`Ess.UI`, `Ess.Net`, `Ess.Contract`, `Ess.Layers`). Their pages remain as historical
> reference for the standalone predecessors, but new mods should build on `Ess`: it's one drop-in file, and
> the old standalones are no longer maintained or deployed. See [Migrating](#migrating-from-the-old-frameworks)
> for the one-to-one mapping.

`Ess` (`_G.Ess`) is the foundational Lua library for *Mercenaries 2* modding — safe, one-line wrappers
around every hard-won pattern this project has found, so a new modder doesn't rediscover them by crashing
the game first. It wraps the traps this wiki documents the hard way: the 32-bit-float RNG
degeneration, the tail-call crash when you override engine logic, the leak-prone
`Add.../Remove...` handle pairs, the [`FlashWidget` corner-coordinate bug](../uilib/), the freshly-spawned
model whose bones read nil for ~0.3s — each is a footgun somewhere else on this wiki, and each is a
one-liner here.

It began as four separate frameworks; those are now **one** file. Deploy `1_Ess.lua` and every other mod
just reads off the global `_G.Ess` table — nothing else required.

## Install

1. Copy the built `1_Ess.lua` into `scripts/OnLoad/` and give it a **low** load number so it runs before
   anything that uses it:
   ```ini
   [OnLoad]
   1_Ess.lua=5
   ```
2. Drop `data/vz-patch.wad` into the game's `data/` folder — it carries the `.gfx` movies `Ess.UI` renders
   through (menus, toasts, board, chat). It auto-loads; nothing else references it. (Skip this only if you
   never touch `Ess.UI`.)
3. Guard any consumer script so it fails clean if Ess isn't loaded:
   ```lua
   if not _G.Ess then Loader.Printf("load Ess first") return end
   ```

The **release zip** ships all of this in game-folder layout (`scripts/OnLoad/1_Ess.lua`, `data/vz-patch.wad`,
the bind-to-a-key demos under `scripts/OnKey/`, and the recipe catalog) — extract it over your install. See
[Where it lives](#where-it-lives).

## The three tiers

Most namespaces expose one or more of three parallel tiers. Reach for the highest one that fits:

- **`Ess.Easy.*`** — guardrails. Intent-named presets (`Ess.Easy.Mark.enemy(guid)`), smallest surface, hard
  to misconfigure. Where a beginner starts — see the dedicated [Ess.Easy](easy) drilldown.
- **`Ess.*`** (unqualified, "Core") — named parameters and sensible defaults, with full control when you want
  to override one.
- **`Ess.Raw.*`** — the primitives the other two are assembled from, for composing something Ess didn't
  anticipate. Not a "skip the safety" hatch — the actual building blocks.

Tiering is selective: only namespaces with a real beginner/advanced gap carry all three (Mark, AIOrders,
Relations, Triggers, Sandbox, Impulse). Simple ones (RNG, Time, Table) are single-tier.

### Instant one-liners

For a newcomer whose whole thought is "I want X to happen," these hide the import and the namespace — each is
one guessable call. The full catalog lives on the [Ess.Easy](easy) page; a taste:

| Verb | Does |
|---|---|
| `Ess.Easy.Vehicle.summon(template)` | spawn a vehicle in front + drop you in the driver seat |
| `Ess.Easy.Spawn.explosion(type)` / `.crate(type)` / `.weapon(name)` / `.airstrike(round)` | a boom in front / a supply drop / a weapon pickup / a shell on your own head |
| `Ess.Easy.World.removeMapBoundary()` / `.clearWanted()` | roam the whole map / lose all heat |
| `Ess.Easy.Player.giveGrapplingHook()` / `.unlockFastTravel()` / `.giveAllRewards()` / `.skin(code)` | the game's own cheat-menu unlocks + whole-figure skin swap, one call each |
| `Ess.Easy.Spawn.fx(t, x,y,z)` / `.fxOn(t, guid, bone)` | a particle effect at a point, on an object, or glued to a bone |
| `Ess.Easy.Fun.dance()` / `.fanfare(win)` | technoviking dance / victory-or-fail music sting |

All use confirmed template names and real engine functions. `Ess.Easy.Console.open()` browses the whole
`Ess.Easy.*` surface in-game, searchable.

## What's inside

Each row below is its own drilldown page — read [Ess.Easy](easy) first if you're new, then the Core-tier
page for whatever you're building. The framework's own
[`CAPABILITIES.md`](https://github.com/loganw234/mercs2-lua-essentials/blob/master/CAPABILITIES.md) and
[`FEATURE_SHEET.md`](https://github.com/loganw234/mercs2-lua-essentials/blob/master/FEATURE_SHEET.md) (the
*why*, and the full build history) remain the canonical upstream reference these pages are checked against.

| Page | Namespaces | What it covers |
|---|---|---|
| [Core Primitives](core) | `Safe`, `Table`, `Str`, `Color`, `Vec`, `Math`, `Guid`/`Name`, `Log`, `State`, `SaveVar`, `RNG` | The `pcall`-and-log idiom, string/color/vector/geometry helpers, reload-safe state, and the engine-safe RNG that sidesteps the 32-bit-float LCG trap. |
| [Identity & World Query](identity-query) | `Player`, `Object`, `Vehicle`, `Probe`, `Human`, `Impulse` | Character/camera/teleport, the everyday spawn/transform/health/label namespace, seats and riders, nearby-object collection, and mass-scaled launch/knockback. |
| [Timing & Input](timing-input) | `Time`, `Loop`, `Input`, `TextConsole` | Wall-clock timing that survives world-pause, the one shared heartbeat, correct key polling, a `.gfx`-free typed console. |
| [Tracking & Cleanup](tracking) | `Track`, `Event`, `Save` | One registry for every leak-prone Add/Remove pair, a logging `Event.Create` wrapper, and the shared save-suppression gate. |
| [Markers](mark) | `Mark` (`Raw`/Core/`Easy`) | Radar, PDA, ground ring, and floating icon — independent opts, tiered from four raw primitives up to one-call presets. |
| [Ess.UI](ui) | `UI.Menu/List/Panel/Bar/Toast/Confirm/Input/Chat/Board`, `Gfx`, `ScrollLog` | The nine-widget kit, native port of [UI Kit](../uilib/), on one input/focus/heartbeat engine. |
| [Camera, Bones & Spatial](camera-bones) | `Camera`, `Bones`, `Points` | Shake/fade/FOV, the full cinematic camera take-over, the confirmed bone/hardpoint recipes, arena spawn-point selection. |
| [Sound & HUD](sound-hud) | `Sound`, `Hud` | Cue/ambience/volume, native hint/banner/objective-tray/radio-subtitle popups. |
| [Encounter Toolkit](encounter-toolkit) | `AIOrders`, `Relations`, `Triggers`, `Sandbox`, `Layers` | The gameplay-scripting machinery extracted from the Contract Framework — usable standalone, without a running contract. All tiered. |
| [Cinematic](cinematic) | `Cinematic` | A declarative cutscene timeline (cuts/dollies/orbits, spawns, AI orders, narration, fades, music) — always restores control, always ESC-skippable. |
| [Networking](net) | `Net` | Co-op data sync, native port of [ModNet](../modnet): auto-syncing shared tables, named messages, authority model. |
| [Contract Engine](contract) | `Contract` | The full save-safe ephemeral-mission engine, native port of the [Contract Framework](../contract-framework/): 16 objective types plus relations/support/AI-order/trigger subsystems. |
| [Meta / Override](override) | `Override` | Change engine logic without the tail-call crash — the crashing shape is made structurally impossible to write. |
| [Support & Call-ins](support) | `Support`, `Easy.Airstrike` | Combat call-ins (shell/artillery/airstrike/bombing run/gunship/reinforce) lifted out of `Ess.Contract` so they're callable anywhere, fire-and-forget. **Unreleased** — composed from already-confirmed native calls, wrapper layer not yet independently smoke-run. |
| [Reactive Hooks & Hotkeys](reactive-hotkeys) | `On`, `Keys` | Intent-named reactive world hooks (death/area/health/hurt/vehicle/tick) and a multi-hotkey panel for one `OnKey` script. **Unreleased** — execute-verified offline, not yet in-game smoke-run. |
| [Objectives & Quests](objectives) | `Objective`, `Quest`, `Easy.Objective`, `Easy.Quest` | The middle tier between a bare `Ess.Hud.objective` line and a whole `Ess.Contract` — single goals and multi-step chains with reload-safe `id`-based construction. **Unreleased** — state machine execute-verified offline, not yet in-game smoke-run. |
| [Debug & Dev Tools](dev-tools) | `Easy.Debug`, `Easy.Console.play` | A live on-screen debug overlay (position, reticle target, health, nearby counts) and an in-game "run any Easy call and cycle its params" playground. **Unreleased** — construction/dispatch verified offline, on-screen rendering not yet in-game smoke-run. |
| **[Ess.Easy](easy)** | Every `Ess.Easy.*` namespace | The full beginner-tier one-liner surface in one place — spawning, unlocks, world tweaks, fun, and every other namespace's Easy preset. |

## A few worked examples

A drill-down menu wired to the one-liners:

```lua
Ess.UI.Menu("MY TOOLS")
  :entry("Summon a helicopter", function() Ess.Easy.Vehicle.summon("UH1 Transport") end)
  :entry("Boom", function() Ess.Easy.Spawn.explosion() end)
  :switch("Invincible", function() return _G.myGod end, function(on) _G.myGod = on end)
  :open()
```

A whole two-objective mission — ephemeral, never touches the save:

{% raw %}
```lua
Ess.Contract.Register{
  id = "raid", title = "Raid the Depot", reward = { cash = 20000, fuel = 60 },
  objectives = {
    Ess.Contract.Destroy{ desc = "Wreck the 2 trucks", spawns = {
      { "Veyron", x + 18, y, z + 6, 0 }, { "Veyron", x + 18, y, z - 6, 0 } } },
    Ess.Contract.Reach{ desc = "Reach extraction", at = { x, y, z }, radius = 12 },
  },
}
Ess.Contract.Accept("raid")
```
{% endraw %}

Take over the camera for a shot, then hand control back:

```lua
local stop = Ess.Easy.Camera.orbit(guid, { radius = 10, speed = 45 })
-- ...later:
stop()   -- or Ess.Camera.panicRevert() as a fire-blind escape hatch
```

## Migrating from the old frameworks

Each absorbed framework maps one-to-one onto a native `Ess.*` namespace. The APIs were kept deliberately
close, and `Ess.UI.Menu` is byte-for-byte compatible:

| Standalone (deprecated) | Now | Notes |
|---|---|---|
| [`uilib.lua`](../uilib/) (`_G.UI`) | [`Ess.UI`](ui) | Same nine widgets, same menu builder and `ctx:` helpers. |
| [`ModNet.lua`](../modnet) | [`Ess.Net`](net) | Shared tables, named messages, authority model. |
| [`ContractFramework.lua`](../contract-framework/) | [`Ess.Contract`](contract) | Same objective builders + support/trigger/relations/AI-order subsystems, now built on the standalone `Ess.AIOrders`/`Ess.Relations`/`Ess.Triggers`. |
| Layer Framework | `Ess.Layers` (usually via `Ess.Sandbox`) — see [Encounter Toolkit](encounter-toolkit) | Save-clean `vz_state_*` manipulation. |

You no longer deploy `uilib.lua` / `ModNet.lua` / `ContractFramework.lua` / `LayerFw.lua` alongside your mod —
just `1_Ess.lua`. [WaveDefense](../wave-defense) is the one exception that stays its own file (a gamemode, not a
framework); it will eventually *consume* `Ess.*` rather than be absorbed.

## Samples & the smoke test

The framework ships **25 recipes** — short "how do I X?" scripts that are each a living doc *and* a
self-verifying smoke test. `python tools/smoke.py` reloads the current build into the running game, runs
every recipe, and reports `PASS`/`FAIL` per recipe, so a change that breaks a public helper turns a recipe
red before release. There are also five bind-to-a-key demos (including the in-game MissionForge mission
author) under `scripts/OnKey/`.

## Where it lives

- **Repo:** [`github.com/loganw234/mercs2-lua-essentials`](https://github.com/loganw234/mercs2-lua-essentials)
  — source under `src/` (one file per namespace, merged into `dist/Ess.lua` by `build/merge.py`), the
  capability reference, and the samples.
- **Releases:** each version tag ships a ready-to-extract zip (the framework, the wad, the demos, the
  recipes) on the [Releases page](https://github.com/loganw234/mercs2-lua-essentials/releases). Start with
  the latest.

## Verification status

Everything above is built and live-tested against the running game, most with exact before/after value
confirmations. Two honest limits, both external rather than untested logic:

- **Co-op peer-to-peer delivery** (`Ess.Net`) — a faithful port of confirmed-working co-op code, but full
  two-machine delivery hasn't been re-verified solo (needs a second machine).
- **`Ess.Input.hijackController`** — its known bug is fixed, but it hasn't been driven with real controller
  input at an open PDA.

## See also

- [Frameworks](../frameworks) — the index this page belongs to.
- [UI Kit](../uilib/), [ModNet](../modnet), [Contract Framework](../contract-framework/) — the standalone
  predecessors, kept as historical reference.
- [WaveDefense](../wave-defense) — the worked example that glues the pieces together; the one framework file Ess
  doesn't absorb.
- [Building ForgeMenu](../deep-dives/forge-menu) and [Custom Contracts, a Save-Safe Approach](../deep-dives/custom-contract)
  — the deep dives whose reasoning `Ess.UI` and `Ess.Contract` are built on.
