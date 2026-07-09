---
title: "8. Making Time Pass on Its Own"
parent: Tutorials
nav_order: 8
---

# Tutorial 8: Making Time Pass on Its Own

> Built from `Event.Create(Event.TimerRelative, ...)`, **confirmed working by live testing** (reliable at
> 2s, 5s, and 20s delays — see [Snippets](../snippets#react-to-an-event-instead-of-polling)), extended
> here to repeat using the same self-rescheduling shape already used elsewhere on this wiki (e.g. the
> [Custom UI](../deep-dives/custom-ui) keyboard-poll loop).

Every tutorial so far has needed you to do something — press a key, load a level. This one sets up
something once and then lets it keep happening **by itself**, on a timer, with nobody pressing anything.

This is an `OnLoad` script — you want this set up automatically once per level, not re-armed every time you
press a key (see [Tutorial 4](two-clocks) if that distinction isn't solid yet).

## The code

Create `scripts/OnLoad/timers.lua`:

```lua
_G.TutorialTimerCount = 0

local function Tick()
  _G.TutorialTimerCount = _G.TutorialTimerCount + 1
  Loader.Printf("[timers] tick #" .. _G.TutorialTimerCount)
  Event.Create(Event.TimerRelative, {5}, Tick, {})
end

Tick()
```

Load into a level and leave it alone. Don't press anything. Check `lua_loader_printf.log` every so often:

```
[timers] tick #1
[timers] tick #2
[timers] tick #3
```

A new line appears roughly every 5 seconds, forever, without you doing anything at all.

> **[Image placeholder — `../img/timerticklog.png`]** Screenshot of `lua_loader_printf.log` showing at
> least 4-5 `[timers] tick #N` lines, ideally with visible timestamps (if your log viewer shows file
> modification times) far enough apart to make clear these appeared on their own over real elapsed time,
> not from repeated keypresses.

## What's actually happening

`Event.Create(Event.TimerRelative, {5}, Tick, {})` means "call `Tick` once, 5 seconds from now." On its
own, that would only fire once — exactly like [Snippets](../snippets#react-to-an-event-instead-of-polling)
demonstrates. The trick that makes it repeat is inside `Tick` itself: the **last thing `Tick` does is
schedule another call to `Tick`**, 5 seconds later, every time it runs. Each firing re-arms the next one —
a self-rescheduling loop, not a built-in "repeat every N seconds" feature (there isn't one; you build it out
of the one-shot version).

The `_G.TutorialTimerCount` line is exactly [Tutorial 7](press-counter)'s counter pattern, doing the same
job: `Tick` runs as a completely fresh call each time (it has no memory of its own between firings, same as
any function), so the running count has to live in `_G`, not as a `local` inside `Tick`.

## Try it yourself

- Change `{5}` to `{1}` for a faster tick, or `{15}` for a slower one — confirm the interval actually
  changes.
- Make it stop after 5 ticks: add `if _G.TutorialTimerCount >= 5 then return end` as the very first line
  inside `Tick`, before it reschedules itself.
- Store the handle `Event.Create(...)` returns (`local uHandle = Event.Create(...)`) and look up
  [`Event.Delete`](../namespaces/event#the-4-core-functions) — see if you can wire up an `OnKey` script that
  stops the timer on demand, using the handle from the last time it scheduled itself.
- Reload the level entirely — confirm the tick count starts back over at 1, since `_G` doesn't survive
  past the game session the way a file would.

## Where this comes from

- [Snippets: React to an event instead of polling](../snippets#react-to-an-event-instead-of-polling) — the
  confirmed one-shot version this tutorial builds on.
- [Event namespace](../namespaces/event) — the full reference, including `Event.Delete` for cancelling a
  scheduled call.

**Next:** [Tutorial 9: Reacting Instead of Waiting](reacting-to-events) — this timer fires because *you*
scheduled it. The next tutorial reacts to something the *game* decides, on its own.
