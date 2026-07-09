---
title: "9. Reacting Instead of Waiting"
parent: Tutorials
nav_order: 9
---

# Tutorial 9: Reacting Instead of Waiting

> Built from `Event.ObjectHealthLessThan`, **confirmed** by a real decompiled call site
> (`vz/chicon001.lua:75`, cited on the [Event namespace](../namespaces/event) page) — combined here with
> Tutorials 1 and 2's `Loader.Printf`/`ShowMessage` as a capstone that pulls the whole ladder together.

[Tutorial 8](timers) made something happen on a schedule *you* chose. This tutorial reacts to something
the **game itself** decides — you register your interest once, and the engine calls you back exactly when
it happens, whenever that turns out to be.

Like Tutorial 8, this is an `OnLoad` script — you're registering this once per level, not re-registering it
on every keypress (which would stack up duplicate listeners, one per press).

## The code

Create `scripts/OnLoad/reacting_to_events.lua`:

```lua
local uChar = Player.GetLocalCharacter()
local nHalfHealth = Object.GetHealth(uChar) / 2

Event.Create(Event.ObjectHealthLessThan, {uChar, nHalfHealth}, function()
  Loader.Printf("[reacting_to_events] health dropped below half!")

  import("MrxTutorialManager")
  MrxTutorialManager.ShowMessage("Ouch! Below half health!")
end, {})
```

Load into a level, then go take some damage on purpose (let an enemy hit you, jump off something tall,
whatever's safe to try). The moment your health crosses below half of whatever it was when the level
loaded, the message appears on screen and the log line appears — with nobody polling, nobody checking a
condition every frame.

> **[Image placeholder — `../img/reactinghealthmessage.png`]** Screenshot of the in-game tutorial-hint
> popup showing "Ouch! Below half health!" appearing during or just after a combat moment, with the
> player's on-screen health indicator visibly reduced.

## What's actually happening

`Event.Create(eventType, {filterArgs}, callback, {callbackArgs})` is the same shape you already used in
[Tutorial 8](timers) with `Event.TimerRelative` — only the event type and its filter arguments change.
`Event.ObjectHealthLessThan` takes `{guid, healthValue}`: watch this specific `uGuid`, and call me back the
moment its health drops below this specific number. The engine is doing the checking, continuously, as
part of its own simulation — your script just waits to be told.

This is a genuinely different shape from everything before it in this ladder: [Tutorial 8](timers) is
"do this, then wait, then do it again" (you drive the schedule). This is "tell the engine what you care
about, then do nothing until it tells you" (the engine drives the schedule). Both are described more fully,
side by side with several other event types, on the [Event namespace](../namespaces/event) page.

## Try it yourself

- Change `nHalfHealth` to `Object.GetHealth(uChar) - 1` — trigger it with the tiniest possible scratch of
  damage, to confirm the threshold really is just a number comparison.
- Look up [`Event.ObjectDeath`](../namespaces/event#gameplay--object-events) on the Event namespace page —
  it takes just `{guid}`. Try registering for your own character's death instead of a health threshold.
  (Careful: you'll need to actually die to see it fire.)
- This event only fires **once** per registration — health dropping below half a second time within the
  same level load won't trigger it again, because nothing re-registered it. Confirm this for yourself, then
  look at how [Tutorial 8](timers)'s `Tick` function re-arms itself, and think about whether the same
  self-rescheduling idea could make this one fire every time health crosses the threshold, not just the
  first time.

## Where this comes from

- [Event namespace](../namespaces/event) — the full catalog of event types, including
  `ObjectHealthLessThan`'s confirmed call site and dozens of others worth knowing exist.

**Next:** [Tutorial 10: Finding Something in the World by Name](finding-by-name) — the last stop on this
ladder: asking the world what's actually in it.
