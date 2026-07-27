---
title: Essentials (Ess)
nav_order: 4
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
   through. It auto-loads; nothing else references it. (Skip this only if you never touch `Ess.UI` — but
   note there is no fallback path: without the wad `Ess.UI` is inert, not degraded.)

   **If you are on Ess 0.5.1, update to 0.5.2 or later before anything else.** Since the 0.5.0 rewrite the
   whole UI kit draws through **one** runtime movie inside that wad, `ess_ui.gfx` — and **the wad 0.5.1
   shipped did not contain it.** On a clean 0.5.1 install every menu, panel, toast, board and chat, plus
   `Ess.UI.Theme` and `Ess.UI.setScale`, did nothing at all. It failed **silently**: the widget host
   constructs successfully whether or not the named asset resolves, so nothing errored and nothing reached
   the log. The symptom is "my menu key does nothing," with a clean log — which is why it belongs here and
   not only on the UI page. 0.5.2 ships the corrected wad (12 assets) plus a build gate that parses the
   wad's own asset table instead of trusting that the file exists, so it cannot ship again. Full
   per-version breakdown: [Install warning for the UI wad](ui#install-warning-for-the-ui-wad).
3. Guard any consumer script so it fails clean if Ess isn't loaded:
   ```lua
   if not _G.Ess then Loader.Printf("load Ess first") return end
   ```

The **release zip** extracts straight over your install: `scripts/OnLoad/1_Ess.lua` and `data/vz-patch.wad`
land where they belong, and that is *all* it deploys. The recipe catalog, the bind-to-a-key demos and the
top-level guides ride along as reference only, under `Ess-samples/` and `Ess-*.md` — nothing is written into
`scripts/OnKey/`, and no `lua_loader.ini` is bundled, because extracting one over a real install would
clobber your existing loader config (your lua-bridge line included). The exact `[OnLoad]` line to *merge* in
is in `Ess-README.txt`. See [Where it lives](#where-it-lives).

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
| `Ess.Easy.World.removeMapBoundary()` / `.clearWanted()` / `.noPursuit(true)` | roam the whole map / lose all heat once / lose all heat **and stay cold** |
| `Ess.Easy.Player.giveGrapplingHook()` / `.unlockFastTravel()` / `.giveAllRewards()` / `.skin(code)` | the game's own cheat-menu unlocks + whole-figure skin swap, one call each |
| `Ess.Easy.Spawn.fx(t, x,y,z)` / `.fxOn(t, guid, bone)` | a particle effect at a point, on an object, or glued to a bone |
| `Ess.Easy.Fun.dance()` / `.fanfare(win)` | technoviking dance / victory-or-fail music sting |

All use confirmed template names and real engine functions. `Ess.Easy.Console.open()` browses the whole
`Ess.Easy.*` surface in-game, searchable.

## What's inside

Each row below is its own drilldown page — read [Ess.Easy](easy) first if you're new, then the Core-tier
page for whatever you're building. As of **0.5.2** the framework is **720 public functions across 87
namespaces** (`dist/ess.json`'s own generated counts), up from 434 — all of that growth landed in **0.5.0**
(0.5.1 is data-only and 0.5.2 is a wad fix, neither adding a public function), and most of it came out of
live probing against a running game rather than out of the decompiled scripts. The framework's own
[`CAPABILITIES.md`](https://github.com/loganw234/mercs2-lua-essentials/blob/master/CAPABILITIES.md) and
[`FEATURE_SHEET.md`](https://github.com/loganw234/mercs2-lua-essentials/blob/master/FEATURE_SHEET.md) (the
*why*, and the full build history) remain the canonical upstream reference these pages are checked against.
Hit an install or mod-authoring snag first?
[`TROUBLESHOOTING.md`](https://github.com/loganw234/mercs2-lua-essentials/blob/master/TROUBLESHOOTING.md)
(new in **0.3.2**) is a symptom-first fix list for the common failure points, before digging into any page
below.

| Page | Namespaces | What it covers |
|---|---|---|
| [Core Primitives](core) | `Safe`, `Table`, `Str`, `Color`, `Vec`, `Math`, `Guid`/`Name`, `Log`, `State`, `SaveVar`, `RNG`, `Sys`, `Atmosphere` | The `pcall`-and-log idiom, string/color/vector/geometry helpers, reload-safe state, and the engine-safe RNG that sidesteps the 32-bit-float LCG trap. **`Ess.DEBUG`/`Ess.Safe.reject`/`.stats`/`.reset`/`Ess.lastError` (0.4.0)** open up this framework's on-purpose silent failures on demand; **`Ess.stop`/`.stopAll` (0.4.0)** add one teardown verb for any of the 27 handle shapes across Ess without deprecating any of them. **New in 0.5.0:** [`Ess.Sys`](core#esssys) — the read-only environment half of the engine's `Sys` namespace (level and build identity, the player's own option settings; every mutator deliberately excluded) — and [`Ess.Atmosphere`](core#essatmosphere), sky/light/time-of-day plus an honest account of the region system that keeps overwriting them. |
| [Identity & World Query](identity-query) | `Player`, `Object`, `Vehicle`, `Probe`, `Human`, `Impulse` | Character/camera/teleport, the everyday spawn/transform/health/label namespace, seats and riders, nearby-object collection, and mass-scaled launch/knockback. **0.5.0** adds `Ess.Object.angularImpulse` — whose default coordinate space was *world* while `.impulse`'s is local, under a comment promising "same argument shape", now aligned — and `Ess.Human.setState`, which validates the posture string in the wrapper because the native reports nothing for a valid state *and* for garbage. |
| [Timing & Input](timing-input) | `Time`, `Loop`, `Input`, `TextConsole` | Wall-clock timing that survives world-pause, the one shared heartbeat, correct key polling, a `.gfx`-free typed console. `Loop.stats`/`.list` (added **0.3.3**) add per-loop tick-cost introspection, purely additive. |
| [Tracking & Cleanup](tracking) | `Track`, `Event`, `Save` | One registry for every leak-prone Add/Remove pair, a logging `Event.Create` wrapper, and the shared save-suppression gate. |
| [Markers](mark) | `Mark` (`Raw`/Core/`Easy`) | Radar, PDA, ground ring, and floating icon — independent opts, tiered from four raw primitives up to one-call presets. **0.5.0 fixed the reason [PDA blips were never visible](mark#why-the-pda-blips-were-never-visible)**: the default icon `icon_yellow_mc` is a registered name with *no art* (the engine's own last-resort fallback), and it was Ess's default in three places. In the same pass `Ess.Mark.KINDS` started naming [an icon for all three layers](mark#kinds-one-name-three-icons) — world, radar and PDA don't share an icon namespace, and the kind table had only ever named two of them. |
| [Ess.UI](ui) | `UI.Menu/List/Panel/Bar/Toast/Confirm/Input/Chat/Board`, `UI.Theme`, `Gfx`, `ScrollLog` | The nine-widget kit, native port of [UI Kit](../uilib/), on one input/focus/heartbeat engine. **Rewritten in 0.5.0** to draw at runtime from theme data: one movie replaces eight, so the [8-line panel / 3-toast / 5-chat-line caps are gone](ui#the-hard-caps-are-gone), and [`Ess.UI.Theme`](ui#essuitheme) restyles the whole kit from 34 plain values with seven presets. That one movie was **missing from the wad Ess 0.5.1 shipped** — see the [install warning](ui#install-warning-for-the-ui-wad) and step 2 above before you debug a UI that does nothing. |
| [Camera, Bones & Spatial](camera-bones) | `Camera`, `Bones`, `Points` | Shake/fade/FOV, the full cinematic camera take-over, the confirmed bone/hardpoint recipes, arena spawn-point selection. |
| [Sound & HUD](sound-hud) | `Sound`, `Hud`, `Hud.Faction` | Cue/ambience/volume, native hint/banner/objective-tray/radio-subtitle popups. **Substantially extended in 0.5.0**: [cue validation](sound-hud#cue-validation) (`duration`/`isCue`/`isLooping` — a mistyped cue is otherwise completely silent) and the category mixer; `Ess.Hud` gained `title`, `location`, `message` (a negative duration means permanent), `tutorial`, `image` and the cash/fuel readouts — display-only, they move the number on screen and not the money; and [`Ess.Hud.Faction`](sound-hud#esshudfaction) adds the faction meters, the pursuit gauge, and `timer()`, the only on-screen countdown the game exposes. Note `Ess.Hud.Faction.levels` is **globally destructive** — it replaces the game's own faction mood names for every faction until the level reloads, and `restoreLevels()` is what undoes it. |
| [Player Screens & Map Surfaces](screens) | `Pda`, `Minimap`, `Gps`, `Shop` | **All four new in 0.5.0.** The mission log, dossier and statistics screen plus the map layer underneath `Ess.Mark`'s blips; the minimap *widget*, which no `Hud.*` function reaches and where a plain `range()` call is overwritten within moments because the game recomputes range from player speed every update ([`lockRange()`](screens#range-vs-lockrange--why-a-naive-zoom-appears-to-do-nothing) owns the handler instead); the map beacon; and the game's own full-screen purchase UI filled with your own items. Live-confirmed on screen on 2026-07-26 — but with a **weaker evidence profile than its neighbours**: no `samples/recipes/` script exercises any of the four, so nothing re-runs these checks. See the page's [Status](screens#status). |
| [Encounter Toolkit](encounter-toolkit) | `AIOrders`, `Relations`, `Triggers`, `Sandbox`, `Layers` | The gameplay-scripting machinery extracted from the Contract Framework — usable standalone, without a running contract. All tiered. `Relations.getPerceivability`/`.setPerceivability` added in **0.3.1**, live-confirmed reversible. **`AIOrders`'s `follow` behavior was fundamentally rewritten in 0.3.3** (native `Ai.Role` instead of a re-issued-`MoveTo` timer) plus five more live-confirmed bug fixes across `move`/`attack`/`face`/`hold`/`enter` in 0.3.3-0.3.4 — see the page for exactly what changed. |
| [Followers Roster](followers) | `Followers` | A lifecycle-aware "who's currently assigned to me" roster on top of stateless `AIOrders` — recruit/dismiss/order the whole roster at once, per-follower markers, natural-completion auto-resume-follow. **New in 0.3.3**, substantially extended in **0.3.4** (vehicle-aware follow, `orderEnter`, and a Follow-role-drift fix that supersedes 0.3.4's own first-cut vehicle-only version — see the page's dated Status section). |
| [Squad — Team & Tactics Layer](squad) | `Squad` | Named teams/roles, a per-scope-safe `orderTeam`, an async multi-step `queue` with a per-step timeout watchdog, role-aware vehicle `Tactics.mountUp`/`.dismountAndSecure`, and on-foot `setFormation` — all built on `Followers` with no new native calls. **New in 0.3.4**, "visual sugar" formations explicitly not a precision tactical system — confirmed live for team-order isolation, vehicle mounting/dismounting, and a 4-unit wedge/diamond formation. |
| [Pursuit & Wanted System](pursuit) | `Pursuit` | The wanted/heat system: start/read/clear a pursuit, the one-way `capLevel` ratchet, and why `restrictAll`/`restrictFaction` gate organic heat only rather than stopping a chase. **New in 0.3.1**, Core-tier only — confirmed live via a dedicated `control_pursuit` smoke recipe (start → state-read → clear round-trip). |
| [Cinematic](cinematic) | `Cinematic` | A declarative cutscene timeline (cuts/dollies/orbits, spawns, AI orders, narration, fades, music) — always restores control, always ESC-skippable. |
| [Networking](net) | `Net` | Co-op data sync, native port of [ModNet](../modnet): auto-syncing shared tables, named messages, authority model. |
| [Contract Engine](contract) | `Contract` | The full save-safe ephemeral-mission engine, native port of the [Contract Framework](../contract-framework/): 16 objective types plus relations/support/AI-order/trigger subsystems. |
| [Meta / Override](override) | `Override` | Change engine logic without the tail-call crash — the crashing shape is made structurally impossible to write. |
| [Support & Call-ins](support) | `Support`, `Easy.Airstrike` | Combat call-ins (shell/artillery/airstrike/bombing run/gunship/reinforce) lifted out of `Ess.Contract` so they're callable anywhere, fire-and-forget. **Confirmed live in 0.3.0** — all 7 call-ins (including `Easy.Airstrike.at`) fired clean in-game; `reinforce` confirmed actually delivering units. |
| [Reactive Hooks & Hotkeys](reactive-hotkeys) | `On`, `Keys` | Intent-named reactive world hooks (death/area/health/hurt/vehicle/tick/labeled) and a multi-hotkey panel for one `OnKey` script. **Confirmed live in 0.3.0** — `Ess.Keys` fully confirmed; 7 of the original 8 `Ess.On` hooks confirmed live (`exitArea` not yet exercised). `Ess.On.labeled` added in **0.3.1**; its arm/disarm lifecycle is confirmed, its fire callback not yet exercised live (see the page for the precise distinction). **[`Ess.On.script`](reactive-hotkeys#essonscript--the-shipped-games-own-script-events) (0.5.0)** opens a channel Ess previously could not hear at all: the named events the shipped game's own Lua broadcasts (`"PDA Open"`, `"SupportUsed"`, the Satellite events…). `src/32_on.lua` lists **31 exact strings**, each checked against a real `Event.Post` call site in the decompiled scripts. |
| [Objectives & Quests](objectives) | `Objective`, `Quest`, `Easy.Objective`, `Easy.Quest` | The middle tier between a bare `Ess.Hud.objective` line and a whole `Ess.Contract` — single goals and multi-step chains with reload-safe `id`-based construction. **Confirmed live** — per the CHANGELOG's 0.3.0 verification entry, `Ess.Objective`/`Ess.Quest`/the `Easy.Objective.reach`/`.destroy`/`.clear`/`.survive` bundles are live-verified in-game. |
| [Debug & Dev Tools](dev-tools) | `Easy.Debug`, `Easy.Console.play` | A live on-screen debug overlay (position, reticle target, health, nearby counts) and an in-game "run any Easy call and cycle its params" playground. **Confirmed live** — per the CHANGELOG's 0.3.0 verification entry, `Easy.Debug.overlay()` renders and `Easy.Console.play()`'s drill-in/run-live/param-cycling all work in-game. |
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

The framework ships **50 recipes** — short "how do I X?" scripts that are each a living doc *and* a
self-verifying smoke test. `python tools/smoke.py` reloads the current build into the running game, runs
every recipe, and reports `PASS`/`FAIL` per recipe, so a change that breaks a public helper turns a recipe
red before release.

There are also **16 larger, bind-to-a-key demos** in `samples/demos/` (renamed from `samples/OnKey/` in
**0.3.2**) — including the in-game MissionForge mission-authoring tool and `StarterMod`, a copy-me template
covering the three patterns every OnKey mod needs (guard/state/action). **As of 0.3.2, none of these ship
pre-installed or pre-bound** — earlier releases auto-deployed and pre-bound all of them across F1-F12 in
the release zip, which silently claimed every F-key before a new modder had bound their own first mod (the
exact key the framework's own `GETTING_STARTED.md` tutorial suggests). Copy whichever demo you want into
your own `scripts/OnKey/` and bind it yourself (e.g. `MissionForge.lua=F7` under `[OnKey]` in
`lua_loader.ini`) — each file's header comment says what it does and suggests a key. See
[`samples/README.md`](https://github.com/loganw234/mercs2-lua-essentials/tree/master/samples#interactive-scripts-samplesdemos)
for the full one-line-per-demo catalog.

## Where it lives

- **Repo:** [`github.com/loganw234/mercs2-lua-essentials`](https://github.com/loganw234/mercs2-lua-essentials)
  — source under `src/` (one file per namespace, merged into `dist/Ess.lua` by `build/merge.py`), the
  capability reference, and the samples.
- **Releases:** each version tag ships a ready-to-extract zip (the framework, the wad, the demos, the
  recipes) on the [Releases page](https://github.com/loganw234/mercs2-lua-essentials/releases). Start with
  the latest.

## Verification status

Everything above is built and live-tested against the running game, most with exact before/after value
confirmations. Three honest limits:

- **Co-op peer-to-peer delivery** (`Ess.Net`) — a faithful port of confirmed-working co-op code, but full
  two-machine delivery hasn't been re-verified solo (needs a second machine).
- **`Ess.Input.hijackController`** — its known bug is fixed, but it hasn't been driven with real controller
  input at an open PDA.
- **The four 0.5.0 screen namespaces** (`Ess.Pda`, `Ess.Minimap`, `Ess.Gps`, `Ess.Shop`) were confirmed on
  screen on 2026-07-26 with recorded measurements, but unlike the rest of the framework **no recipe in
  `samples/recipes/` exercises them**, so `tools/smoke.py` cannot catch a regression there. See
  [Player Screens & Map Surfaces → Status](screens#status).

## See also

- [Frameworks](../frameworks) — where Ess used to be listed. It now sits at the top level, as the starting
  point for a new mod rather than one library among several; that section keeps the example gamemode and the
  guide to writing your own library.
- [UI Kit](../uilib/), [ModNet](../modnet), [Contract Framework](../contract-framework/) — the standalone
  predecessors, kept as historical reference.
- [WaveDefense](../wave-defense) — the worked example that glues the pieces together; the one framework file Ess
  doesn't absorb.
- [Building ForgeMenu](../deep-dives/forge-menu) and [Custom Contracts, a Save-Safe Approach](../deep-dives/custom-contract)
  — the deep dives whose reasoning `Ess.UI` and `Ess.Contract` are built on.
