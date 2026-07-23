---
title: "Debug & Dev Tools"
parent: Essentials (Ess)
nav_order: 17
---

# Debug & Dev Tools

## Overview

Two mod-author-facing tools from the same 0.3.0 batch, both pure composition of already-confirmed `Ess`
pieces — no new engine calls introduced by either: a live on-screen dev overlay (`Ess.Easy.Debug`, from
`src/97_easy_debug.lua`) and an interactive in-game function runner (`Ess.Easy.Console.play`, the new half of
`src/96_console.lua`). Per the CHANGELOG's dated 0.3.0 verification entry, both are now **confirmed live**
in-game — built from confirmed calls, offline-verified first, and since run and observed in the actual game;
each section below states exactly what was checked and how.

## Ess.Easy.Debug

`Ess.Easy.Debug.overlay(opts) -> panel | nil` toggles a live dev panel that follows you around, showing the
handful of things you'd otherwise be reaching for `Loader.Printf` one at a time to check: your exact
position, what you're aiming at, your vehicle/health state, and what's nearby.

```lua
Ess.Easy.Debug.overlay(opts)   -- opts (all optional):
                                --   x, y        screen position (default 20, 40)
                                --   interval    refresh seconds (default 0.2)
                                --   radius      nearby-scan radius (default 40)
                                --   i           player index (default 0)
Ess.Easy.Debug.hide()          -- force it off
Ess.Easy.Debug.isOn() -> bool
```

Calling `overlay()` a second time while it's on tears it down (stops the refresh loop, destroys the panel)
and returns `nil` — a real toggle, not just "show." The underlying widget is a plain [`Ess.UI.Panel`](ui#essuipanel);
the source also honors an undocumented `opts.w` (panel width, default 360) alongside the ones listed in its
own header comment. Session state (`on`/`panel`) is kept in a file-local table that survives an `OnKey`
re-run (so the toggle stays a toggle across repeated presses of whatever key calls it) but resets on a world
reload, same reload-safety reasoning as `Ess.Loop`'s own registry.

The panel repaints four lines every `interval` seconds, each sourced from an already-shipped `Ess` call:

| Line | Example | Built from |
|---|---|---|
| Position | `pos: (120.4, 5.0, -88.2)  yaw 45` | `Ess.Player.pose(i)` |
| Aim | `aim: Veyron  VZ  d=12.3` (or `aim: (nothing)`) | `Ess.Player.targetUnderReticle(i)` + `Ess.Name` + `Ess.Probe.getFaction` + `Ess.Object.distance` |
| Vehicle + health + mem | `on foot   health: 85 / 100   mem 128` (or `vehicle: <name>`) | `Ess.Player.inVehicle(i)` + `Ess.Object.health` (plus a direct `Object.GetMaxHealth` read) + [`Sys.MemUsage`](../namespaces/sys) (new in 0.3.1, wrapped) |
| Nearby | `near(40): 6 hum  2 veh` | `Ess.Probe.nearby(x, y, z, radius, "humans"/"vehicles")`, called once per kind |

**As of 0.3.1 (the 2026-07-22 "bindings-pass harvest"), that vehicle/health line also appends an engine `mem`
figure.** `Ess.Easy.Debug.overlay` now wraps the native [`Sys.MemUsage`](../namespaces/sys) call and tacks its
raw, unlabeled number onto the end of the line (`memLine()` in the source). The absolute value isn't the
point — **the practical use is watching that number climb while your script runs**, a live memory-leak smell
test you get for free just by leaving the overlay open through a play session. `Sys.MemUsage` itself is a
native engine call documented on [Sys](../namespaces/sys), not an `Ess`-authored function. Per `CHANGELOG.md`'s
`[0.3.1]` entry, this release's offline test pass caught and fixed a real `Sys`-indexing guard bug in this
exact mem line before it ever shipped (the source now checks `Sys and Sys.MemUsage` before calling it, so a
missing `Sys` global — e.g. running under the offline test harness — returns an empty string instead of
throwing); the figure then rendered correctly during the release's live in-game pass.

**Deliberately shows no "FPS" number.** The overlay refreshes on a fixed-interval `Ess.Loop` — a timer, not
a per-render-frame hook — so any framerate it computed would be the *tick* rate, not the real framerate. The
source's own comment is blunt about why this was left out: it would be "a confidently-wrong number," and the
overlay only ever shows things the engine can actually report.

**The nearby line is throttled and cached.** It's the one expensive part of the refresh — two native
`FastCollect` passes over the radius, one per `Ess.Probe.nearby` kind — so it's gated behind an
`Ess.Time.cooldown(1)` ready-check (~once a second) and the last result is cached; the cheap pos/aim/health
lines still repaint on the full `interval`. This gate is a **post-release hardening fix**, not part of the
original design: the CHANGELOG's Hardening section records that the nearby scan used to run on *every* fast
tick until an offline pre-release audit added the cache, on the reasoning that "a dev overlay should stay
light enough not to perturb what you're measuring."

**Status:** line-building and the on/off toggle were execute-verified offline first. Per the CHANGELOG's
dated 0.3.0 verification entry, the panel itself is now **confirmed to render on-screen in-game** — the one
gap this page previously flagged for `Debug` ("construction verified, rendering not yet tested") is closed.
The `mem` figure folded into that same line in 0.3.1 (above) carries its own separate confirmation from that
later release's dated verification entry.

## Ess.Easy.Console.play

`Ess.Easy.Console` already existed before this addition, as a read-only in-game reference:
`Ess.Easy.Console.open()` browses the whole `Ess.Easy.*` (+ a few standout Core) catalog grouped by
namespace, built on `Ess.UI.Board`, with `Ess.Easy.Console.search()` filtering it via a `Ess.TextConsole`
prompt. `.play()` is the new piece — an interactive **playground**: instead of just reading a usage line, it
drills into a curated demo catalog via [`Ess.UI.Menu`](ui#essuimenu), lets you actually **run** a function
live, and cycle its parameters in-game to see exactly what each one does, on demand.

The catalog is a plain array table, `DEMOS`, each entry shaped like:

```lua
{ group = "Spawn", name = "Explosion", desc = "A big boom in front of you (real, damaging).",
  params = { { key = "type", values = { "Explosion (Grenade)", "Explosion (C4)", "Explosion (MOAB)", "fx_Explosion_Huge" } } },
  run = function(a) Ess.Easy.Spawn.explosion(a.type) end },
```

- `group` — one of seven topics, in the order they appear in `DEMOS`: **Spawn, World, Player, Support, Goals,
  Dev, Juice**.
- `desc` — a one-line description, shown as a header above a parameterized demo's sub-menu.
- `params` — optional; an array of `{ key, values }` pairs, each a confirmed preset list to cycle through.
  Omitted entirely for demos that take no arguments.
- `run(a)` — the real call, receiving a table `a` keyed by each param's `key`, holding whichever value is
  currently selected.

A rough tour of what's in each group today:

| Group | Demos |
|---|---|
| Spawn | Explosion (grenade/C4/MOAB/huge-fx cycle), Summon a vehicle (UH1 Transport/AH1Z (Full)/Veyron), Weapon pickup (RPG/Sniper Rifle/Minigun/Grenade Launcher/Shotgun/C4), Supply crate (Light MG/Blueprints/Treasure), Enemy squad (count 1/3/5/8) |
| World | Clear wanted level, Remove map walls, Hellscape, Reset atmosphere — all no-param, one-shot |
| Player | Grappling hook, All rewards, Give cash (10k/100k/1M), Change skin (`pmc_hum_fiona`/`vz_hum_solano`) |
| Support | Airstrike my target, Artillery ahead (~35u out, 6 shells) |
| Goals | Reach objective ahead (~30u), Survive timer (10/20/30s), Mini mission (a 2-step `Ess.Quest`: reach then survive 15s) |
| Dev | Toggle debug overlay — literally `Ess.Easy.Debug.overlay()`, the feature covered above |
| Juice | Slow motion (0.2/0.35/0.5 for 3s), Camera shake, Speed boost, Dance, Victory fanfare |

`Ess.Easy.Console.play()` builds one `Ess.UI.Menu`, one `menu:category()` per `group`. Inside a group, a demo
*with* `params` becomes its own nested category: a header showing `desc`, a `">> Run it"` entry that reads
whatever value each param is currently cycled to and calls `run(a)`, and one entry per param whose label
reads `"<key>: <current value>   (pick to cycle)"` — picking it just advances that param's index (wrapping
around) and the menu re-renders the label with the new value, the same dynamic-label trick `Ess.UI.Menu`'s
own `:switch` uses elsewhere. A demo with no `params` is a flat entry that runs the instant you pick it.
Every run goes through a small `pcall` wrapper: success toasts `"Ran: <name>"`, failure toasts
`"error (see log)"` and logs the real error via `Ess.Log`. Calling `.play()` a second time while it's already
open closes the menu instead of reopening it (the same toggle idiom as `Debug.overlay`).

`.play()` is reachable two ways: the pinned `"[ Playground -- run functions live ]"` row at the top of
`Ess.Easy.Console.open()`'s board, or the new **`Playground`** `OnKey` demo, bound to **F3** by default
(confirmed in `samples/OnKey/Playground.lua`, which sets `KEYVAL = "f3"` and just calls
`Ess.Easy.Console.play()` to toggle it).

**Status:** construction, param-cycling, and run-dispatch were execute-verified offline first. Per the
CHANGELOG's dated 0.3.0 verification entry, the on-screen behavior is now **confirmed live**: the drill-in
navigation, running a demo live, and the param-cycling all work in-game — the rendering gap this page
previously flagged for `.play()` is closed too.

## Other new OnKey demos built on these pieces

The same 0.3.0 batch ships five complete `OnKey` demo scripts that *compose* `Ess.Mark`/`Ess.On`/
`Ess.Object` (and the rest of the framework) into something playable, without introducing any new `Ess` API
of their own — one line each, not a deep dive. Per the CHANGELOG's own **"Still unverified"** callout, all
five still need to be deployed to `scripts/OnKey/` with `lua_loader.ini` bindings and a keypress each before
any of them has had an in-game pass — nothing below is upgraded to confirmed-live by association with the
rest of this page:

- **VehicleInspector** (F6) — a WAILA-for-vehicles poll: watches for the nil→guid transition on "what
  vehicle is the player in" to catch the moment you board, dumps the vehicle's full detail set to the log,
  and keeps a live HUD panel open (health-refreshing) while you're aboard.
- **WaveSurvival** (F11) — an escalating horde mode: waves of `Ess.Easy.Spawn.enemies` rush you,
  `Ess.On.death` tracks kills reliably per-guid, clearing a wave heals you (plus a crate every 3rd wave), and
  G calls in a danger-close airstrike on a cooldown.
- **BossFight** (F12) — a mini-boss encounter with a live `Ess.UI.Bar` health bar that regenerates through
  phase 1, enrages (adds + a camera shake) at 50% via `Ess.On.healthBelow`, and pays out cash on
  `Ess.On.death`.
- **EncounterDirector** (F1) — a weighted-random encounter roller (`Ess.RNG:pick`) that drops an ambush, a
  cash bounty, a guarded supply crate, an artillery dodge, or a `Ess.Quest`-driven checkpoint time trial
  around you on each press.
- **CreatorToolkit** (F8) — a hub-of-tools menu (object inspector, an AI-cap meter, a nearby scanner, this
  same `Ess.Easy.Debug.overlay` folded in — superseding an earlier standalone `DebugOverlay` demo, persistent
  teleport bookmarks, a prop placer, a dev panel, photo mode, a camera-path cinematic recorder); its own
  header comment calls it a **first-pass draft** that still needs an in-game pass (no WASD freecam yet — you
  author by positioning your character — and photo mode only hides player markers, since there's no native
  full-HUD-hide call). Stated plainly per its own header, not upgraded here.
Two more samples sit alongside them in the same folder but are **not** part of this 0.3.0 batch —
neither appears in the CHANGELOG, both still use the old generic `KEYVAL = "free"` pick-a-key convention
instead of the new batch's dedicated F-keys, and `TrailerHitch`'s own header already declares itself
confirmed live (a live-test status that predates, and is unrelated to, everything else on this page):

- **CollectibleFinder** (unbound — pick a free key) — an `Ess` reimplementation of a community
  proximity-marker script: marks `SpareParts` collectible boxes via `Ess.Mark` as you approach and auto-clears
  each marker on pickup via `Ess.On.death`.
- **TrailerHitch** (unbound — pick a free key) — spawns a truck + trailer and rigidly welds them via
  `Object.Attach`/`Object.SetTransformToObject` at the hitch hardpoint; confirmed live that the trailer tracks
  the truck's movement (a rigid weld, not a real tow joint — no swing/pivot).

## See also

- [Tracking & Cleanup](tracking) — `Ess.Track`, the similar "toggle a live thing on/off and clean it up
  again" pattern the overlay's own teardown follows.
- [Timing & Input](timing-input) — `Ess.Keys`, for building your own hotkey-driven dev tools the way
  `Playground`/`VehicleInspector`/the rest of this batch bind theirs.
- [Identity & World Query](identity-query) — `Ess.Probe`, what the debug overlay's nearby-scan is built
  directly on top of.
- [Ess.UI](ui) — `Ess.UI.Panel` and `Ess.UI.Menu`, the two widgets both tools here are built from.
- [Ess.Easy](easy) — the full beginner-tier one-liner catalog `Ess.Easy.Console.open()` browses and
  `.play()` runs live.
- [Essentials (Ess)](index) — the framework index this page belongs to.
