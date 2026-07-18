---
title: "1. Hello, Log"
parent: Tutorials
nav_order: 1
---

# Tutorial 1: Hello, Log

> Built from a single call already used throughout this wiki (`Loader.Printf`) — the only thing new here
> is slowing down to look at just this one piece by itself, as a true first step.

Before anything else — a menu, a spawned vehicle, a whole gamemode — you need to know your own code
actually ran at all. The smallest possible way to check that is to print one line somewhere you can go
look at it.

## The code

Create `scripts/OnKey/hello_log.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

Loader.Printf("[hello_log] the key was pressed!")
```

Load into a level, then press **Insert**.

## Where the line actually went

Nothing appeared on your screen — that's expected. `Loader.Printf` writes to a plain text file next to
your game's `.exe`, called `lua_loader_printf.log`, not to the screen. Open that file in any text editor
after pressing the key. You should see your line at the very bottom:

```
[hello_log] the key was pressed!
```

> **[Image placeholder — `../img/hellologfile.png`]** Screenshot of `lua_loader_printf.log` open in a
> plain text editor (e.g. Notepad), with the file path visible in the title bar, showing
> `[hello_log] the key was pressed!` as the most recent line at the bottom of the file.

Press **Insert** a few more times, then reopen the file — a new line appears each time. This file only
ever contains things a script *explicitly* asked to print — nothing from the base game leaks into it,
unlike the engine's own shared debug log. That's why every tutorial from here on uses it: it's your own,
private, always-available window into "what is my script actually doing right now."

## What's actually happening

`Loader.Printf(message)` is a global function — available in every script, no setup line needed — that
takes one string and appends it as a new line in that log file. That's the whole mechanism. The
`"[hello_log] "` prefix isn't required by anything; it's a convention used throughout this wiki so that
when several scripts are all writing to the same file, you can tell at a glance which script wrote which
line. Get in the habit now — by [Tutorial 4](two-clocks) you'll have two scripts logging at once.

## Try it yourself

- Change the message text and press Insert again — confirm the new text shows up, not the old one, and
  that the old line is still there above it.
- Add a second `Loader.Printf(...)` line to the same script, with different text — confirm both lines
  appear, in order, after just one keypress.
- Try `Loader.Printf(42)` — a number instead of a string in quotes. Does it work, or does it complain? If
  it complains, try `Loader.Printf(tostring(42))` instead and compare.
- Pick a different key (change `"insert"` to `"home"`, `"end"`, or another key name) and confirm it still
  works. This is the same `KEYVAL` line every `OnKey` script in this wiki uses.

## Where this comes from

- [Getting Started: `Loader.Printf`](../getting-started#loader-printf-debug-output-that-doesn-t-get-lost) —
  why this exists instead of the engine's own `Debug.Printf`.
- [Glossary: `Loader.Printf`](../glossary#loaderprintf) / [`KEYVAL`](../glossary#keyval)

**Next:** [Tutorial 2: Hello, Screen](hello-screen) — the same idea, but somewhere you don't have to
alt-tab out of the game to see it.
