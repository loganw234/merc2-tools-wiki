---
title: "7. Remembering Things: A Press Counter"
parent: Tutorials
nav_order: 7
---

# Tutorial 7: Remembering Things: A Press Counter

> Built from the `_G` persistence pattern already confirmed in
> [Your First Menu](../first-menu#three-pieces-combined) — stripped down to just the state, with the menu
> removed, so the idea stands on its own before you add anything else to it.

Every `OnKey` script you've written so far re-runs its **entire file from scratch** on every press. Any
plain `local` variable is created fresh and thrown away the instant the script finishes — there's no
memory between presses unless you deliberately build some. This tutorial builds the smallest possible
piece of memory: a number that goes up by one each time you press a key.

## The problem, first

Create `scripts/OnKey/press_counter_broken.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

local nCount = 0
nCount = nCount + 1
Loader.Printf("[press_counter] count is now: " .. nCount)
```

Press **Insert** several times and check the log. Every single line says `count is now: 1` — `nCount`
starts over at `0` on every press, because `local` variables don't survive past the end of the script
that created them.

## The fix: `_G`

`_G` is the one table that's genuinely shared and kept alive across separate script runs. Create
`scripts/OnKey/press_counter.lua`:

```lua
local KEYVAL = "insert"

_G.TutorialPressCount = (_G.TutorialPressCount or 0) + 1
Loader.Printf("[press_counter] count is now: " .. _G.TutorialPressCount)
```

Press **Insert** several times:

```
[press_counter] count is now: 1
[press_counter] count is now: 2
[press_counter] count is now: 3
```

> **[Image placeholder — `../img/presscounterlog.png`]** Screenshot of `lua_loader_printf.log` showing at
> least 4-5 consecutive `[press_counter] count is now: N` lines with N genuinely incrementing each time,
> demonstrating the count surviving across separate keypresses.

## What's actually happening

`_G.TutorialPressCount or 0` reads as "whatever's already stored in `_G.TutorialPressCount`, or `0` if
there's nothing there yet." The very first press, nothing's there yet (`_G.TutorialPressCount` is `nil`,
which is falsy), so it becomes `0 + 1 = 1`. Every press after that, the value really is sitting in `_G`
from last time, so it becomes *that* value `+ 1`. The `or` is doing all the work here — without it,
`_G.TutorialPressCount + 1` would error the very first time, since you can't add `1` to `nil`.

This is the same idea [Your First Menu](../first-menu#three-pieces-combined) uses for remembering whether
a toggle is on or off — a whole table instead of one number, but the exact same
`_G.Something = _G.Something or {...}` shape.

## Try it yourself

- Add a *second* counter (`_G.TutorialOtherCount`) in the same script, incrementing independently — confirm
  both survive and update correctly together.
- Add a **reset**: put `_G.TutorialPressCount = 0` at the top of the script, temporarily, run it once, then
  remove that line again. (This is a real technique — a one-time reset line you add, run, then delete.)
- Make it count *down* instead of up, starting from 10, and print `"self-destructing in N"` — stop it from
  going below 0 with an `if` check.
- [Tutorial 8](timers) reuses this exact `_G` pattern to count timer ticks instead of keypresses — see if
  you can predict what that code will look like before you get there.

## Where this comes from

- [Your First Menu: Three pieces, combined](../first-menu#three-pieces-combined) — the same pattern,
  immediately put to use in a real two-toggle menu.

**Next:** [Tutorial 8: Making Time Pass on Its Own](timers) — everything so far has needed a keypress. Time
to make something happen without you touching anything.
