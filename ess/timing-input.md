---
title: Timing & Input
parent: Essentials (Ess)
nav_order: 3
---

# Timing & Input

## Overview

Four small namespaces that share one job: give a mod a correct, engine-safe way to measure time and read
keyboard input, instead of every script hand-rolling the same fragile pattern.

- **`Ess.Time`** — wall-clock timing (elapsed-time stamps and an auto-advancing per-frame clock) that
  survives world-pause, plus time-scale for slow-motion.
- **`Ess.Loop`** — the one shared self-rescheduling heartbeat. Every repeating "do this every N seconds"
  loop anywhere else in Ess is built on this.
- **`Ess.Input`** — the one correct keyboard-polling shape on this engine (an edge-triggered press buffer
  plus a held-key snapshot), a VK-to-character table, and a niche controller-hijack trick.
- **`Ess.TextConsole`** — a REPL-style typed-input console built on `Ess.Input` and `Ess.Loop`, no `.gfx`
  asset required.

## Ess.Time

`Ess.Time` wraps the engine's `Sys.*TimeStamp` idiom. There are two different flavors of "how much time
passed," and picking the right one matters:

- **An explicit stamp** (`stamp`/`elapsed`/`mark`, and `cooldown` built on top of them) — `elapsed()` reads
  the true value and never advances on its own, so checking a cooldown is idempotent; only `mark()` resets
  it. Use this for "has N seconds passed since X," timers, cooldowns.
- **An auto-advancing clock** (`Ess.Time.clock`) — `:delta()` returns "seconds since my own last `:delta()`
  call," clamped so a pause/hitch can't blow up downstream math. This is the shape a per-frame heartbeat
  wants for its `dt`.

Both read the real-world clock, so both keep advancing through a world-pause (a PDA/menu) — unlike
`Event.TimerRelative`'s own delay, which is sim-gated and freezes under pause.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Time.stamp()` | `stamp() -> uStamp` | `Sys.RealTimeStamp`, pcall-guarded. Real-world clock — keeps advancing through pause/slow-mo. |
| `Ess.Time.mainStamp()` | `mainStamp() -> uStamp` | `Sys.MainTimeStamp`. Pausable/scaled clock — tracks `Ess.Time.scale()` and game pause. Use this instead of `stamp()` for a gameplay cooldown that should freeze with the game. |
| `Ess.Time.mark(uStamp)` | `mark(uStamp)` | Re-marks an *existing* stamp handle in place (`Sys.TimeStampMark`) — every confirmed call site re-marks a stamp previously produced by `stamp()`/`mainStamp()` rather than creating a new one each time. |
| `Ess.Time.elapsed(uStamp)` / `Ess.Time.since(uStamp)` | `elapsed(uStamp) -> n \| 0` | Seconds since the stamp was marked (`Sys.TimeStampGetElapsed`). `since` is a plain alias — same function, reads better at some call sites. |
| `Ess.Time.clock(maxDelta)` | `clock(maxDelta) -> clock` | Returns an object with `:delta()`, an auto-advancing per-frame timer. `maxDelta` defaults to `0.25` seconds. |
| `Ess.Time.cooldown(seconds)` | `cooldown(seconds) -> ready` | Returns a `ready()` function: `true` (and re-marks) at most once per `seconds` window, `false` otherwise without re-marking, so a retry doesn't push the window back. The *first* call is always ready — nothing is on cooldown yet. |
| `Ess.Time.scale(n)` | `scale(n)` | `Sys.SetTimeScale(n)` — confirmed idiom for slow-motion, e.g. `Ess.Time.scale(0.2)` for a 5x slowdown. |
| `Ess.Time.restoreScale()` | `restoreScale()` | Just `scale(1)` under a clearer name for "undo the slow-mo." |
| `Ess.Time.format(nSeconds, bUseTenths)` | `format(nSeconds, bUseTenths) -> s \| nil` | `Junk.FormatTime` — formats a raw seconds value (e.g. from `elapsed()`) into a HUD-ready display string. |

`Clock:delta()` clamps any single reading to `maxDelta` (default `0.25`) and re-marks its own stamp on every
call — so a long hitch or pause can't produce one huge `dt` spike downstream.

### `Ess.Time.cooldown` example

```lua
local ready = Ess.Time.cooldown(3)   -- a 3-second cooldown

if ready() then
    -- fires immediately the first time, then at most once per 3s after that
end
```

### The Easy tier: `Ess.Easy.Time.slowmo`

`Ess.Time` carries one bit of `Ess.Easy` surface, defined inline in the same file: `Ess.Easy.Time.slowmo(n,
seconds)` applies `Ess.Time.scale(n)` immediately (default `n = 0.2`) and schedules a single
`Ess.Time.restoreScale()` via `Ess.Loop` after `seconds` of *real* time (default `2`) — using
`Ess.Time.stamp()`, not `mainStamp()`, so the restore timer isn't itself slowed down by the scale it just
applied. This is the confirmed real recipe (`samples/recipes/slow_motion.lua`):

```lua
Ess.Easy.Time.slowmo(0.3, 2)   -- 30% speed for 2 seconds, then back to normal on its own
```

For manual start/stop control instead of an auto-restore, use `Ess.Time.scale(n)` /
`Ess.Time.restoreScale()` directly. See [Ess.Easy](easy) for the full one-liner catalog.

## Ess.Loop

The one shared self-rescheduling heartbeat primitive. Every "run this every N seconds" loop elsewhere in
Ess — and, per the source header, at least five independent hand-rolled reimplementations across this
project's history (uilib's `ensureTick`, contracts.lua's `poll()`, WaveDefense's main loop, ForgeMenu,
MissionForge) — is this one implementation instead.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Loop.start(id, interval, tickFn)` | `start(id, interval, tickFn)` | Registers (or **replaces**) a self-rescheduling loop under `id`. `tickFn()` runs every `interval` seconds (default `1`); return `true`/truthy to keep going, `false`/`nil` to auto-stop. |
| `Ess.Loop.stop(id)` | `stop(id)` | Cancels a running loop early. Its next scheduled tick sees it's gone and quietly does not reschedule — no error. |
| `Ess.Loop.isRunning(id)` | `isRunning(id) -> bool` | Whether a loop is currently registered under `id`. |

Calling `start()` again with the **same `id`** immediately supersedes any previous loop registered under
that id, via an internal generation counter — this is what makes it safe to call `Ess.Loop.start`
unconditionally from the top of a re-run `OnKey` script without leaking a duplicate loop on every keypress.
A tick that errors is caught (`pcall`), logged via `Ess.Log`, and treated as `keepGoing = false`, so one
bad tick stops that loop instead of spamming errors forever.

The registry resets on every `OnLoad` re-run (world reload) — that's intentional, since a reload already
invalidates every scheduled `Event.TimerRelative` the engine was tracking.

Real confirmed usage (`samples/recipes/do_it_later.lua`), a heartbeat that ticks three times then stops
itself by returning `false`:

```lua
local ticks = 0
Ess.Loop.start("recipe_do_it_later", 0.3, function()
    ticks = ticks + 1
    if ticks >= 3 then
        Ess.Log("heartbeat ran " .. ticks .. " times, stopping")
        return false
    end
    return true
end)
```

(That same recipe also uses `Ess.Easy.Triggers.after(seconds, fn)` for a one-shot delayed call — a
different namespace, covered on [Encounter Toolkit](encounter-toolkit), not part of `Ess.Loop` itself.)

`Ess.TextConsole` below is itself just an `Ess.Loop` consumer — its typing loop is registered under the id
`"Ess.TextConsole"`.

## Ess.Input

The one correct keyboard-polling shape on this engine, plus a VK-to-character table and a controller-input
trick.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Input.poll()` | `poll() -> { pressed = {vk, ...}, down = fn(vk) -> bool }` | Call **once per tick**. `pressed` drains `Loader.PopKeyEvents()` (an edge-triggered ring buffer — each byte is a VK that went up→down since the last drain). `down(vk)` reads `Loader.GetKeyboardState()` (a 256-byte snapshot) for "is this held right now." |
| `Ess.Input.held(vk)` | `held(vk) -> bool` | Is `vk` down at this instant, from the keyboard-state snapshot **only** — does not touch the edge buffer. Use this instead of `poll().down(vk)` when something else is already draining `poll()`'s edges (e.g. a "hold Shift to boost" loop running alongside a menu that owns the discrete-press buffer). |
| `Ess.Input.clear()` | `clear()` | Discards every buffered key event (`Loader.ClearKeyEvents`, pcall-guarded). The canonical use: a script activated *by* a keypress drains the buffer once on activate so its own trigger key doesn't immediately fire an action on the first tick. |
| `Ess.Input.VkToChar(vk, bShift)` | `VkToChar(vk, bShift) -> sChar \| nil` | US keyboard layout: A-Z, 0-9, space, and common punctuation, with shifted variants. Ported byte-for-byte from uilib's `CHAR` table. |
| `Ess.Input.usingController()` | `usingController() -> bool` | `Gui.ControllerInUse()`, guarded (returns `false` if the function doesn't exist) and normalized (`b == true or b == 1`, since this engine's getters sometimes return `1`/`0` instead of a real boolean — a naive `if b then` would treat `0` as truthy). For branching HUD hint text ("Press A" vs "Press E"). |
| `Ess.Input.hijackController(onInput)` | `hijackController(onInput) -> release()` | ⚠ Unverified in this build — see caveat below. Always call the returned `release()` when done. |

**NEVER call a per-key `Loader.IsKeyDown` in a loop.** Every framerate bug this project has hit in a custom
menu/console/HUD came from exactly that mistake, independently, more than once — `poll()`/`held()` are the
fix made structural.

### `hijackController` caveat

Source-flagged as **unverified**: synthesized from a wiki deep-dive survey rather than a direct primary-source
read. The documented technique is real and reasoned-through, not invented — there is no per-frame Event on
this engine at all (`Event.TimerRelative` is sim-gated and freezes under world-pause), so while a PDA-style
pause is up, the only callback that still ticks is `ControllerInput`, and only on actual controller
activity (an idle stick sends nothing at all, not a final zero — decay stale axes yourself if that matters).
`hijackController` hides the PDA widget and installs your handler on its `ControllerInput` event to ride
that. **Caveat:** while hijacked, the PDA underneath still claims arrows/Enter/Esc — a keyboard UI layered
on top must use letter keys, not arrows, while it's active. This has not been driven with real controller
input at an open PDA — treat it as reasoned-through, not confirmed.

## Ess.TextConsole

A standalone REPL-style typed-input console, built on `Ess.Input.VkToChar` and `Ess.Loop`. Unlike
`Ess.UI.Input` (a one-shot modal prompt that auto-closes on submit and needs the `ui_input.gfx` movie — see
[Ess.UI](ui)), `Ess.TextConsole` stays open across multiple Enter presses and needs no `.gfx` asset at all —
just a plain `MrxGui.TextWidget`. Good fit for a standalone `OnKey` script (a cheat/spawn menu) that wants
one quick text field without pulling in the whole UI kit.

| Function | Signature | Notes |
|---|---|---|
| `Ess.TextConsole.open(opts)` | `open{ prompt=, text=, max=, lockPlayer=, onSubmit=fn(text), onCancel=fn(), onChange=fn(text) }` | Opens the console. `prompt` defaults to `"> "`, `text` (a starting buffer) defaults to `""`, `max` defaults to `200` characters. `lockPlayer` defaults to `true` — disables player movement/actions (`Player.SetInputEnabled`) while typing; pass `lockPlayer = false` for an overlay that should keep gameplay running underneath (e.g. a chat box). |
| `Ess.TextConsole.close()` | `close()` | Safe to call even if not open. |
| `Ess.TextConsole.isOpen()` | `isOpen() -> bool` | |

Behavior, straight from the tick loop:

- **Enter** submits: `onSubmit(text)` fires, the buffer resets to `""`, and the console **stays open** for
  another line (REPL-style, not one-shot).
- **Escape** cancels: `onCancel()` fires and the console closes.
- **Backspace** trims one character.
- Any other mapped key appends via `Ess.Input.VkToChar(vk, bShift)`, up to `max` characters. `onChange(text)`
  fires whenever the buffer changes (including on submit-reset and backspace).

Internally, `open()` drains the input buffer (`Loader.ClearKeyEvents`) before starting so the keypress that
triggered the console doesn't leak in as its first character, then starts a `0.01`s `Ess.Loop` under the id
`"Ess.TextConsole"`. `close()` stops that loop and restores player input if `lockPlayer` was set.

## See also

- [Essentials (Ess)](index) — the framework index.
- [Tracking & Cleanup](tracking) — `Ess.Track`/`Ess.Event`, the pattern for tearing down anything a script
  registers, including loops and events started from here.
- [Ess.Easy](easy) — the full one-liner catalog, including `Ess.Easy.Time.slowmo` and `Ess.Easy.Triggers`.
- [Ess.UI](ui) — the widget kit `Ess.TextConsole` deliberately stays lighter than; shares the same
  `PopKeyEvents`/`GetKeyboardState` input plumbing described above.
