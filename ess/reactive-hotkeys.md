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

## Ess.On — reactive world hooks

Source: `src/32_on.lua`. Built entirely on already-confirmed pieces — `Event.ObjectDeath`,
`Ess.Object.pos`/`health`, `Ess.Player`, `Ess.Loop`, `Ess.Object.pollVehicleChange`, `Ess.Math.within2D`, and
(for the 0.3.1-added `labeled` hook) `ObjectFilter` + `Event.ObjectProximity` — `Ess.On` just wraps them under
an intent-named hook instead of you wiring the primitive yourself. **Every hook returns a `stop()`** you call
to cancel it. 7 of the (now) 9 hooks below are confirmed live as of 0.3.0 — see [Overview](#overview) for the
one exception from that pass (`exitArea`); the ninth, `labeled`, arrived later in 0.3.1 with its own status
(see its row and the note below the table).

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
- [ObjectFilter](../namespaces/objectfilter) — the native engine namespace `Ess.On.labeled` wraps
  (`Create`/`SetFilter`/`AddObject`), including the corpus-cross-reference + live-probe provenance behind
  those signatures.
- [Debug & Dev Tools](dev-tools#other-new-onkey-demos-built-on-these-pieces) — the `CollectibleFinder` sample
  `Ess.On.labeled` was promoted from, which stays as the hand-written worked example.
