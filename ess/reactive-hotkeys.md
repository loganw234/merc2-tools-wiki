---
title: "Reactive Hooks & Hotkeys"
parent: Essentials (Ess)
nav_order: 15
---

# Reactive Hooks & Hotkeys

## Overview

Two namespaces for the other half of scripting a mod — not making something happen, but responding to what
the world (or the player's keyboard) does:

- **`Ess.On`** — intent-named reactive hooks (`death`, `enterArea`, `healthBelow`, `playerHurt`, …) so a mod
  can react to the world without wiring a raw `Event.*` call or standing up a whole `Ess.Contract`. Every
  hook returns a `stop()` function.
- **`Ess.Keys`** — lets one script own a whole panel of hotkeys. `lua_loader.ini`'s `[OnKey]` binds exactly
  one key to one script; `Ess.Keys` is how that single script then dispatches several keys to several
  actions internally.

Both shipped new in 0.3.0's additive batch (`CHANGELOG.md`), and both were carried through that release's
live-verification pass. `CHANGELOG.md`'s `[0.3.0]` entry — a dated, versioned first-party record, not a
captured log/transcript — reports the results feature-by-feature:

- **`Ess.Keys`** (`vk`/`on`/`isBound`/`off`) — confirmed live, no qualifiers.
- **`Ess.On`** — *"7 of its 8 hooks fired live: `death`, `enterArea`, `insideArea`, `healthBelow`, `tick`,
  `vehicle` (enter + exit), `playerHurt`."* **`exitArea` was explicitly not exercised** in that pass — it
  alone is called out by name as the exception, and stays **written and internally consistent, not yet
  confirmed via live testing** (the status the whole batch carried before 0.3.0) until it gets its own pass.

The other 7 `Ess.On` hooks, and all of `Ess.Keys`, have moved past that status as of 0.3.0.

**`Ess.On.labeled` is a later addition, not covered by the "7 of 8" accounting above.** It shipped afterward,
in **v0.3.1**'s "bindings-pass harvest" (2026-07-22, `CHANGELOG.md`'s `[0.3.1]` entry) — a ninth hook with its
own, narrower verification status; see its row in the table below and the note underneath it.

**`Ess.On.script` is later still, and is a different *kind* of hook.** It shipped in **0.5.0**'s engine-native
sweep — a tenth entry that neither polls nor watches an engine signal, but listens for the named events the
shipped game's own scripts broadcast. No `Ess.*` function reached that channel before 0.5.0 (the raw
`Event.ScriptEvent` registration was always available by hand); it gets
[its own section](#essonscript--the-shipped-games-own-script-events) below, with its own verification status.

## Ess.On — reactive world hooks

Source: `src/32_on.lua`. Built entirely on already-confirmed pieces — `Event.ObjectDeath`,
`Ess.Object.pos`/`health`, `Ess.Player`, `Ess.Loop`, `Ess.Object.pollVehicleChange`, `Ess.Math.within2D`,
(for the 0.3.1-added `labeled` hook) `ObjectFilter` + `Event.ObjectProximity`, and (for the 0.5.0-added
`script` hook) `Event.ScriptEvent` — `Ess.On` just wraps them under an intent-named hook instead of you
wiring the primitive yourself. **Every hook returns a `stop()`** you call to cancel it. 7 of the (now) 10
hooks below are confirmed live as of 0.3.0 — see [Overview](#overview) for the one exception from that pass
(`exitArea`); the ninth, `labeled`, arrived later in 0.3.1 with its own status (see its row and the note
below the table), and the tenth, `script`, later still in 0.5.0
([its own section](#essonscript--the-shipped-games-own-script-events) covers it).

| Function | Signature | Fires | Notes |
|---|---|---|---|
| `Ess.On.death(guid, fn)` | `death(guid, fn) -> stop()` | Once | A real `Event.ObjectDeath` hook (`Ess.Event.on(Event.ObjectDeath, {guid}, fn)`) — not a poll. `fn()` takes no arguments. If `guid` is falsy, returns a no-op `stop()` immediately instead of erroring. |
| `Ess.On.enterArea(x,y,z,r, fn [,i])` | `enterArea(...) -> stop()` | Once | Polls every **0.25s**. The moment player `i` (default `0`) comes within horizontal radius `r` of `(x,z)` (`Ess.Math.within2D`, so `y` isn't part of the distance check), calls `fn(px, y, pz)` — note the `y` passed back is the **`y` you armed it with**, not a measured height — then stops itself. |
| `Ess.On.exitArea(x,y,z,r, fn [,i])` | `exitArea(...) -> stop()` | Once | Polls every **0.25s**. Only counts as "leaving" after the player has actually been inside the radius first (an internal `been` flag) — arming this while already outside the area does *not* fire on the next tick. Fires `fn(px, y, pz)` once, then stops. |
| `Ess.On.insideArea(x,y,z,r, fn [,i])` | `insideArea(...) -> stop()` | Every tick | Polls every **0.25s**; calls `fn(px, y, pz)` on **every** tick the player is inside the radius (a live "zone" callback), and simply does nothing on ticks they're outside. Never auto-stops — call the returned `stop()` yourself when the zone should stop watching. |
| `Ess.On.healthBelow(guid, pct, fn)` | `healthBelow(guid, pct, fn) -> stop()` | Once | Polls every **0.4s**. **The baseline is not max health** — it's whatever `Ess.Object.health(guid)` first reads back as soon as the hook arms (captured once as `base` on the first tick that returns a positive value). Fires `fn(hp)` the first time `hp <= base * (pct/100)` (`pct` defaults to `50`), then stops. Arm this against an already-damaged target and "50% health" means 50% of its health *at arm time*, not 50% of its true max — a real, easy-to-miss gotcha, not a documentation nicety. |
| `Ess.On.playerHurt(fn [,i])` | `playerHurt(fn [,i]) -> stop()` | Repeats | Polls every **0.2s** against player `i`'s (default `0`) character health. Calls `fn(newHp, lost)` any tick health is lower than the *previous* tick's reading — `lost` is the delta. Keeps running (and keeps updating its internal `last` reading) until you call `stop()`. |
| `Ess.On.vehicle(fn [,i])` | `vehicle(fn [,i]) -> stop()` | Repeats | A thin pass-through: resolves player `i`'s character via `Ess.Player.character(i or 0)`, then returns `Ess.Object.pollVehicleChange(char, fn)` directly — that call's own `stop()` is what you get back. If there's no character, returns a no-op `stop()` instead. See [Vehicle-entry watch](identity-query#essvehicle) for `pollVehicleChange`'s own default poll interval (0.5s) and the `(uVehicleOrNil, uPrevVehicleOrNil)` signature `fn` receives. |
| `Ess.On.tick(interval, fn)` | `tick(interval, fn) -> stop()` | Repeats | Just a named, reload-safe `Ess.Loop.start(id, interval or 1, fn)` under an auto-generated id (`"Ess.On.tick:<n>"`) — every call gets its **own** id, so multiple `Ess.On.tick` hooks never collide with each other or with `Ess.Loop` ids you manage yourself elsewhere. `fn()` runs every `interval` seconds (default `1`); its return value is ignored — the loop always keeps going until `stop()`. |
| `Ess.On.labeled(label, r, fn [,i])` | `labeled(label, r, fn [,i]) -> stop()` | Once per object | **New in 0.3.1.** Wraps the confirmed `ObjectFilter` + `Event.ObjectProximity` discovery idiom (see [ObjectFilter](../namespaces/objectfilter)): arms a filter on world label `label` (`ObjectFilter.Create` + `SetFilter`), then a persistent `Event.ObjectProximity` calls `fn(uGuid)` once for each matching object as it streams within radius `r` (default `300`) of player `i`'s (default `0`) character — immediately excluding that guid from the filter (`AddObject(filter, uGuid, true)`) so it can never re-fire; the exclusion **is** the dedupe, not a separate seen-set. Returns a no-op `stop()` immediately if `label` isn't a non-empty string, player `i` has no character, or `ObjectFilter.Create` itself fails. Promoted from the `CollectibleFinder` sample's inline version (see [Debug & Dev Tools](dev-tools#other-new-onkey-demos-built-on-these-pieces)), which stays as the hand-written worked example. |
| `Ess.On.script(name, fn)` | `script(name, fn) -> stop()` | Repeats | **New in 0.5.0**, and the only hook here that neither polls nor watches an engine signal: it listens for a **named script event the shipped game itself posts** (`Event.Post("PDA Open", {uPlayer = ...})` and 30 more). `fn(tPayload)` receives the posted table, and keeps receiving it — this is an `Event.CreatePersistent(Event.ScriptEvent, ...)` registration, so it fires on every post until `stop()`. A name the game never posts isn't an error; it just never fires. See [its own section](#essonscript--the-shipped-games-own-script-events) for the argument-order trap, the guard rails, and the table of real names. |

Every callback in the table above is `pcall`-guarded internally (`pcall(fn, ...)`), so one throwing handler
can't kill the poll loop it's attached to.

**`On.labeled`'s own verification is narrower than the rest of the table above, and worth stating precisely.**
Like the rest of 0.3.1, it was verified offline first (`checkpure` 10/10, `test_bundles` all green) before the
release's full in-game pass on the 2026-07-22 build — the same pass that ran the 42/42-recipe smoke suite. But
`On.labeled` wasn't one of those 42 recipes: it was exercised as a **targeted live probe** instead, and that
probe armed and stopped it cleanly (its `stop()` teardown works end-to-end) — no labeled object happened to be
inside radius at the test spot, so the `fn(uGuid)` fire callback itself was not observed actually firing in
that pass. That's a real, specific gap, not a reason to doubt the technique in general: the exact same
`ObjectFilter` + `Event.ObjectProximity` idiom this hook wraps is already live-proven by the existing
`CollectibleFinder` sample (which marks and clears `SpareParts` pickups with it as the player approaches). So
the underlying discovery idiom is live-confirmed — only this specific wrapper's own fire path is still
waiting on its own in-game trigger.

### Honest limits (from the source header, not omitted)

`Ess.On`'s own header comment is upfront about what this engine simply does not give you:

> there is no clean "the PLAYER got a kill" or "who shot me" event on this bridge, so those aren't here —
> `Ess.On.playerHurt` polls the player's own health dropping (the feasible version of "I took damage"), and
> `Ess.On.death` watches a KNOWN object you already have a guid for.

In practice that means: `Ess.On.death` can only ever tell you about a death you already knew to watch (you
must already hold its `guid`) — there's no "notify me about any death" hook, because no such event exists to
hook. And there's no attacker-identification event either, which is why `playerHurt` reports *that* health
dropped and by how much, not who caused it.

## Ess.On.script — the shipped game's own script events

**New in 0.5.0** (`CHANGELOG.md`'s `[0.5.0]` entry, the engine-native sweep). Source: `src/32_on.lua:186`,
`function Ess.On.script(sName, fn)`, returning a `stop()` like every other hook on this page.

Everything else here watches the world from the outside: `enterArea` polls a position, `playerHurt` polls a
health value, `death` registers for the engine's `Event.ObjectDeath` signal. `Ess.On.script` does none of
that. It
listens for the **named script events the shipped game's own Lua broadcasts** — `resident/mrxguipda.lua:125`
really does call `Event.Post("PDA Open", {uPlayer = ...})` every time the player opens the PDA, and the
satellite, support-menu, transit, munitions and medevac systems all announce themselves the same way.
**Before 0.5.0, Ess could not hear a single one of them** — no `Ess.*` function reached this channel. The
raw idiom was always available to a mod that wrote it by hand (`Event.CreatePersistent(Event.ScriptEvent,
{name, validationFn}, cb, {})` — the shipped game does exactly that at `resident/alarm.lua:64` for
`"mpPlayerJoin"`), and the [Event](../namespaces/event) page documents it. What 0.5.0 adds is the wrapper,
the argument-order measurement below, and a checked list of names worth listening for.

The registration it makes, from the source (the real call is wrapped — `Ess.Safe.quiet(Event.CreatePersistent,
...)` — which is what the guard-rail note below is about):

```lua
Event.CreatePersistent(Event.ScriptEvent,
    { sName, function() return true end },
    function(tPayload) pcall(fn, tPayload) end, {})
```

- **Persistent, so it repeats.** Unlike `Ess.On.death` (which goes through `Ess.Event.on` → `Event.Create`),
  this registers with `Event.CreatePersistent` and keeps firing on every post until `stop()` calls
  `Event.Delete`. `stop()` nils its own handle right after deleting (`if ev then Event.Delete(ev); ev = nil
  end`), so calling it twice is harmless — the second call sees `nil` and does nothing.
- **The second filter slot is a validation function**, required by `Event.ScriptEvent` — it decides which
  posts you care about. Ess passes an accept-everything `function() return true end`, matching what the
  game's simplest call sites do. The game's *careful* call sites use it as a filter: `vz/oilcon020.lua:147`
  listens for `"PDA Open"` with `return Player.GetLocalPlayer() == tData.uPlayer`, i.e. "only when *this*
  player opened it". `Ess.On.script` gives you no way to supply your own — do that filtering inside `fn`.
- **Not registered with `Ess.Event` or `Ess.Track`.** The handle never enters Ess's event registry, so the
  returned `stop()` is the only teardown. Hand it to a tracker (`tracker:add(stop)`) if you want it swept
  with everything else — see [Tracking & Cleanup](tracking).
- **Guard rails, and the one they don't cover.** A `sName` that isn't a non-empty string, or an `fn` that
  isn't a function, is rejected via `Ess.Safe.reject` (which only prints under `Ess.DEBUG`) and returns a
  no-op `stop()` — the hook is *not* armed. But the `Event.CreatePersistent` check only catches a **thrown**
  error: if that call returns nothing without erroring, the guard passes, the stored handle is `nil`, and you
  get a `stop()` that silently does nothing. `Ess.On.labeled` has the identical exposure on *its*
  `Event.CreatePersistent` (`if oke then ev = e end`) — the explicit handle check it does have is on
  `ObjectFilter.Create`, not on the event registration — so this is a shared pattern, not a `script`-only
  slip.
- **A name the game never posts is not an error.** Registration succeeds and the hook simply never fires —
  the quietest possible failure, and the reason to copy names out of the table below rather than type them.

Minimal shape (illustrative; the `uPlayer` field is source-confirmed at the call site cited above):

```lua
local stopPda = Ess.On.script("PDA Open", function(t)
    Ess.Log("PDA opened by " .. tostring(t and t.uPlayer))
end)
-- later, when you're done listening:
stopPda()
```

**Verification status, stated precisely.** The *mechanism* is confirmed live: the delivery order was measured
in-game on **2026-07-26** with a purpose-built probe event (see the next section). Two *names* are confirmed
live through this exact hook — `Ess.Gps` arms `"GPS Beacon Set"` and `"GPS Beacon Cleared"` via
`Ess.On.script` at load, and `src/57_gps.lua` reports them firing **four in a row across two set/clear
cycles, in order, with the right coordinates**. The other 29 names in the table below are **confirmed from
the decompiled source only** — each has a real `Event.Post` call site (cited), but none has been observed
firing through `Ess.On.script` in a live pass.

### The callback argument — where the payload actually lands

`Event.CreatePersistent`'s **callback data comes first and the posted table arrives after it.** Getting that
backwards is a silent nil-index, not an error. Measured in-game on **2026-07-26** with a probe event: a
callback data of `"CALLBACKDATA"` landed in **argument 1**, and the posted `{marker = "PAYLOAD"}` in
**argument 2** (recorded in the comment above the function in `src/32_on.lua`).

`Ess.On.script` sidesteps this by passing an **empty** callback-data table, which puts the posted payload in
argument 1 — so `fn(tPayload)` reads the way you'd expect.

The game's own code shows what the confusing version looks like, and it is worth reading before you write a
raw `Event.ScriptEvent` registration by hand. `vz/oilcon020.lua:194` registers `BeaconUsed` for
`"GPS Beacon Set"` with callback data `{self, tBeaconData}` — and `tBeaconData` there is an **undeclared
global**, so it is `nil` and the array is really just `{self}`. The posted payload therefore lands in the
second slot, which `function BeaconUsed(self, tBeaconData)` (line 207) names `tBeaconData` and reads `.nX` /
`.nY` off. It works entirely by accident of that nil.

This also settles a question [the `Event` page](../namespaces/event#the-4-core-functions) currently records as
open — whether `Event.ScriptEvent` listeners receive `Event.Post`ed names. **They do**, measured live, and
`Ess.Gps` has run on that fact since 0.5.0.

### The event names the game posts

`src/32_on.lua`'s header lists **31 exact strings** — spaces and capitals included, because these are literal
names and a typo just buys you silence. (`CHANGELOG.md`'s `[0.5.0]` entry rounds the same list to "~28"; the
source list is the one to trust, and it is the one below.) Every name here was checked against a real
`Event.Post` call site in the decompiled base-game scripts, and the call site is cited so you can read what it
actually sends.

**The payload shapes below are from the decompiled source, not from a live capture** — they are what the
posting call site passes, which is the best available evidence for every row except the two GPS events (see
the note under the table).

| Event name | What the call site posts | Posted by |
|---|---|---|
| `"GPS Beacon Set"` | `{nX = ..., nY = ...}` — the field named `nY` holds a **Z** coordinate | `resident/mrxguipda.lua:780` |
| `"GPS Beacon Cleared"` | The same two fields at the call site — but measured live as carrying no coordinates; see the note under this table | `resident/mrxguipda.lua:789` |
| `"PDA Open"` | `{uPlayer = ...}` | `resident/mrxguipda.lua:125`, and `:35` on the net path |
| `"PDA Close"` | `{uPlayer = ...}` at `:170`; an **empty** `{}` on the net path at `:39` | `resident/mrxguipda.lua:170`, `:39` |
| `"Support Menu Open"` | `{uPlayer = ...}` | `resident/mrxguihudsupportmenu.lua:259`, `:1740` |
| `"Support Menu Close"` | `{uPlayer = ...}` | `resident/mrxguihudsupportmenu.lua:327` |
| `"SupportUsed"` | The support module object itself (`Event.Post("SupportUsed", self)`) — not a plain data table | `resident/mrxsupport.lua:215` |
| `"Satellite Targetting Start"` | `{uPlayer = ...}` | `resident/mrxguisatellite.lua:47` |
| `"Satellite Targetting Success"` | `{uPlayer = ...}` | `resident/mrxguisatellite.lua:600` |
| `"Satellite Targetting Cancelled"` | `{uPlayer = ...}` | `resident/mrxguisatellite.lua:61` |
| `"Satellite Minigame Start"` | `{uPlayer = ...}` | `resident/mrxguisatellite.lua:522` |
| `"Satellite Minigame Sector Hit"` | `{uPlayer = ...}` | `resident/mrxguisatellite.lua:639` |
| `"Satellite Minigame Sector Miss"` | `{uPlayer = ...}` | `resident/mrxguisatellite.lua:657` |
| `"Transit Interface Open"` | `{uPlayer = ...}` | `resident/mrxguipda.lua:819` |
| `"Transit Interface Success"` | `{uPlayer = ...}` | `resident/mrxguipda.lua:905` |
| `"transitStart"` | `{uHeli}` | `resident/mrxsupporttransit.lua:339` |
| `"transitEnd"` | `{uHeli}` | `resident/mrxsupporttransit.lua:398` |
| `"MunitionsPickup"` | `{vStock, uGuid}` on the support-pickup path — but the fuel and cash paths post the literal strings `{"Fuel", uGuid}` (`:572`) and `{"Cash", uGuid}` (`:576`), so slot 1 is not always the same kind of value | `resident/munitions.lua:560`, `:572`, `:576`, `resident/laptop.lua:112` |
| `"NoMunitions"` | `{}` — nothing at all | `resident/munitions.lua:424` |
| `"UntagMunitions"` | `{uGuid}` | `resident/munitions.lua:386` |
| `"mpPlayerJoin"` | `{uPlayerGuid, uCharacterGuid}` | `resident/mrxplayer.lua:210` |
| `"mpPlayerLeft"` | `{uPlayerGuid, uCharacterGuid}` | `resident/mrxplayer.lua:300` |
| `"InFocus"` | `{uTarget = ..., uViewer = ..., bSniper = ...}` — `bSniper` is `false` from the binoculars, `true` from the sniper scope | `resident/mrxguibinoculars.lua:206`, `resident/mrxguisniperscope.lua:195` |
| `"Airstrike"` | `{sStage = "DesignationComplete", sType = "None"}` — both call sites post exactly these values | `resident/mrxsupport.lua:423`, `resident/mrxsupportdesignator.lua:329` |
| `"RecruitAvailable"` | `{sRecruit}` | `resident/mrxsupportmanager.lua:265` |
| `"HeroReported"` | `{sFactionTemplate, uGuid}` (array, faction template first) | `resident/mrxfactionmanager.lua:1236` |
| `"MedevacComplete"` | `Player.GetAllPlayers()` — a plain array of player guids, not a keyed table | `resident/mrxplayer.lua:517` |
| `"SurvivalMode"` | `{uGuid}` | `resident/hero.lua:222` |
| `"SurvivalCooldownEnded"` | `{uGuid}` | `resident/hero.lua:240` |
| `"parkingLotStart"` | Two different shapes across four call sites: three positional guids (entrance, parking-lot point, heli point), or a bare `{false}` | Guids: `resident/mrxhq.lua:743`, `vz/wifpmcinterior.lua:2110`. `{false}`: `vz/wifpmcinterior.lua:2102`, `vz/xQ!L.lua:845` |
| `"oilrigDestroyed"` | `{uiGuid}` | `resident/oilrig.lua:62` |

**Two notes to carry into your handler.** `"GPS Beacon Set"`'s payload field named `nY` holds a **Z**
coordinate (`nX = tEvent.PosX, nY = tEvent.PosZ` at the call site) — `Ess.Gps.onSet` untangles that and hands
its `fn` a plain `(x, z)`. And although `"GPS Beacon Cleared"` is posted with the same two fields, Ess's live
run measured them as **nil** (`src/57_gps.lua`: the clear payload "carries no coordinates at all"), which is
why `Ess.Gps.onClear`'s `fn` takes no arguments. Where the decompiled source and a live measurement disagree,
the measurement wins.

**This list is a curated starting point, not the closed set.** A sweep of literal `Event.Post("...")` call
sites across the decompiled base-game scripts finds **41** distinct names — the 31 above plus
`"ActionHijackStart"` / `"ActionHijackFinish"` / `"ActionHijackComplete"`, `"Ammo low"` / `"Ammo not low"`,
`"Attitude"`, `"Busted"`, `"CashAdded"`, `"ClientKill"` and `"CollateralDamage"`. Even 41 undercounts:
`resident/mrxbunkerbuster.lua:91` posts `"Nuked"` by handing `Event.Post` *itself* to a timer as the callback
(`Event.Create(Event.TimerRelative, {2}, Event.Post, {"Nuked", ...})`), which no grep for `Event.Post("`
will catch. And `vz/pmccon004.lua:316` and `:323` *listen* for `"SolanoHijackComplete"` /
`"SolanoHijackFailed"` with no matching post anywhere in the decompile, so some posts evidently originate
outside the script layer. **Inferred, not tested:** the hook has no per-name logic, so any posted name should
work — but only the two GPS names have actually been observed firing through `Ess.On.script`.

## Ess.Keys — multi-hotkey panel

Source: `src/25_keys.lua`. `lua_loader.ini`'s `[OnKey]` loader binds one key to one script, but a mod is
usually a *toolkit* of several hotkeys. `Ess.Keys` drains the same edge-triggered key buffer
[`Ess.Input`](timing-input#essinput) exposes, on one shared, self-arming `Ess.Loop` (id `"Ess.Keys"`,
interval **0.05s**), and dispatches to whichever registered key just went down — so a single script can own a
whole panel of actions instead of one. Confirmed live as of 0.3.0 (`vk`/`on`/`isBound`/`off` all named in that
release's verification pass — see [Overview](#overview)).

| Function | Signature | Notes |
|---|---|---|
| `Ess.Keys.on(key, fn)` | `on(key, fn)` | `key` is a Windows VK number (e.g. `0x74`) **or** a name string resolved via `Ess.Keys.vk` — `"F1"`..`"F12"`, `"a"`..`"z"`, `"0"`..`"9"`, and named keys (`space`, `enter`, `escape`/`esc`, `tab`, `backspace`, `up`/`down`/`left`/`right`, `shift`, `ctrl`, `insert`, `delete`, `home`, `end`, `pageup`, `pagedown`). Names are case-insensitive. `fn(bShift)` receives whether Shift was held (from `Ess.Input`'s down-snapshot, VK `0x10`) at the moment the key edge fired. Registering starts the shared loop if it isn't already running. Logs and does nothing if `key` doesn't resolve or `fn` isn't a function. |
| `Ess.Keys.off(key)` | `off(key)` | Unbinds that one key; no-op if it wasn't bound or doesn't resolve. |
| `Ess.Keys.clear()` | `clear()` | Drops every binding at once (`Ess.Keys._map = {}`). |
| `Ess.Keys.isBound(key) -> bool` | `isBound(key) -> bool` | |
| `Ess.Keys.vk(name) -> number \| nil` | `vk(name) -> number \| nil` | Resolves a name to its Windows VK code via the same lookup table `on`/`off`/`isBound` use internally. A raw number passed in is returned unchanged. |

Dispatch is **edge-triggered**: it drains `Ess.Input.poll().pressed` (the ring buffer of keys that went
up→down since the last drain), so a held key fires its bound action exactly **once**, not once per tick.
The shared loop is self-idling — its tick function returns `false` (stopping the loop) the instant
`Ess.Keys._map` is empty, and any subsequent `Ess.Keys.on` call re-arms it.

**Fresh every level load.** `Ess.Keys._map` is reset unconditionally at the top of `25_keys.lua`, so a world
reload invalidates the shared loop and drops every binding a prior session left. This is *not* the same as
an `[OnKey]` re-run: pressing an already-bound `OnKey` script's key again does **not** re-run its `OnLoad`
file, so a consumer script's own `Ess.Keys` bindings persist fine between its own repeated keypresses — only
an actual level/world reload clears them.

**Caveat — shared input buffer (paraphrasing the source comment):** `Ess.Keys` reads the exact same
edge-triggered key buffer a focused [`Ess.UI.Menu`](ui#essuimenu) widget reads. Running `Ess.Keys` and a
focused `Ess.UI.Menu` on the same keys at the same time means they'll contend for the same edges — use one
or the other, or make sure they bind distinct keys.

### Real recipe: `hotkey_toolkit.lua`

From `samples/recipes/hotkey_toolkit.lua`, quoted directly (not paraphrased):

```lua
Ess.Keys.on("F6", function() Ess.Easy.Spawn.explosion() end)                         -- F6 = a boom in front
Ess.Keys.on("F7", function() Ess.Easy.Vehicle.summon("UH1 Transport") end)           -- F7 = summon a heli
Ess.Keys.on("F8", function(shift)                                                    -- F8 = clear heat, Shift+F8 = chaos
    if shift then Ess.Easy.World.hellscape() else Ess.Easy.World.clearWanted() end
end)
```

Three keys, three actions, one script: F6 drops an explosion in front of you, F7 summons a UH1 Transport and
seats you in it, and F8 clears your wanted heat — or, held with Shift, triggers `Ess.Easy.World.hellscape()`
instead. The recipe's own smoke check just confirms all three ended up bound
(`Ess.Keys.isBound("F6") and Ess.Keys.isBound("F7") and Ess.Keys.isBound("F8")`) — actually pressing the keys
in-game is a manual follow-up, per the recipe's own logged instruction ("now press F6 / F7 / F8").

## See also

- [Ess.Easy](easy) — the one-liner catalog `hotkey_toolkit.lua` binds its keys to (`Spawn.explosion`,
  `Vehicle.summon`, `World.hellscape`/`clearWanted`).
- [Tracking & Cleanup](tracking) — `Ess.Track`/`Ess.Event` share the same "one registry, no leaks" design
  philosophy `Ess.On` and `Ess.Keys` lean on (a single shared `Ess.Loop`/buffer instead of a hand-rolled poll
  per script).
- [Ess.UI](ui) — read this before combining `Ess.Keys` with a focused `Ess.UI.Menu`; they contend for the
  same input buffer, per the caveat above.
- [Timing & Input](timing-input) — `Ess.Loop` (the heartbeat both namespaces are built on) and `Ess.Input`
  (the edge/held-key polling primitive `Ess.Keys` and `Ess.On.playerHurt`-style polling ultimately read).
- [Identity & World Query](identity-query) — `Ess.Object.pollVehicleChange`, the call `Ess.On.vehicle` wraps
  directly.
- [Event](../namespaces/event) — `Event.ScriptEvent`, `Event.CreatePersistent` and `Event.Post`, the raw
  primitives `Ess.On.script` sits on. Read it if you want to register one by hand; note the page's own
  "delivery mechanism not confirmed" caveat on `Event.Post` predates the 2026-07-26 live measurement recorded
  [above](#the-callback-argument--where-the-payload-actually-lands).
- [ObjectFilter](../namespaces/objectfilter) — the native engine namespace `Ess.On.labeled` wraps
  (`Create`/`SetFilter`/`AddObject`), including the corpus-cross-reference + live-probe provenance behind
  those signatures.
- [Debug & Dev Tools](dev-tools#other-new-onkey-demos-built-on-these-pieces) — the `CollectibleFinder` sample
  `Ess.On.labeled` was promoted from, which stays as the hand-written worked example.
