---
title: "4. Two Clocks, Side by Side"
parent: Tutorials
nav_order: 4
---

# Tutorial 4: Two Clocks, Side by Side

> Built from the `OnLoad`/`OnKey` model already documented in
> [Getting Started](../getting-started#2-the-script-loader-for-anything-that-should-run-automatically) —
> this page's only new contribution is running both side by side so the difference is something you *see*
> instead of just read about.

Every tutorial so far has used `scripts/OnKey/` — a script that runs once, whenever you press its key.
There's a second folder, `scripts/OnLoad/`, for scripts that run **automatically**, once, every time a
level finishes loading. Same engine, same Lua, genuinely different trigger.

## The code

You already have `scripts/OnKey/hello_log.lua` from [Tutorial 1](hello-log). Leave it exactly as it is.
Now create `scripts/OnLoad/hello_onload.lua` next to it:

```lua
Loader.Printf("[hello_onload] a level just finished loading!")
```

Notice what's *missing* compared to every `OnKey` script so far: no `local KEYVAL = ...` line. `OnLoad`
scripts don't bind to a key at all — there's nothing to bind.

## Watching the difference

1. Open `lua_loader_printf.log` and note how many lines are in it right now (or clear it, if you'd rather
   start from empty).
2. Load into a level (or reload the current one). Check the log — a
   `[hello_onload] a level just finished loading!` line appeared **on its own**, without you pressing
   anything.
3. Now press **Insert** a few times (still bound from [Tutorial 1](hello-log)'s `hello_log.lua`). Each
   press adds one more `[hello_log] the key was pressed!` line.
4. Load into a *different* level (or the same one again). Watch what happens to each script: `hello_onload`
   fires again, automatically, exactly once. `hello_log` does **not** — it only ever fires when you
   actually press the key, no matter how many times you load a level.

> **[Image placeholder — `../img/twoclocksonload.png`]** Screenshot of `lua_loader_printf.log` showing a
> `[hello_onload] ...` line appearing once immediately after a level load, followed by several
> `[hello_log] ...` lines appearing only after separate, later keypresses — illustrating that one fired on
> its own and the other only fired on demand.

## What's actually happening

Two independent triggers, running the exact same kind of Lua underneath:

- **`OnLoad`** fires once per level load, at the point the game itself considers a level "ready" (control
  has returned to the player). Good for anything that should happen automatically, every time you play —
  HUD tweaks, spawning something, setting up a system that should just always be running.
- **`OnKey`** fires only when its bound key is pressed, however many times you press it, whenever you press
  it. Good for anything on-demand — debug toggles, cheats, "do this right now" actions.

If you're ever unsure which one a script belongs in, ask: "should this happen automatically every time I
play, or only when I explicitly ask for it?" [Tutorial 8](timers) and [Tutorial 9](reacting-to-events)
both use `OnLoad` for exactly this reason — they set something up once that should then keep running or
keep watching on its own, which wouldn't make sense to re-trigger by hand.

## Try it yourself

- Add a second, different message to `hello_onload.lua` and reload the level — confirm both lines appear,
  in order, from one load.
- Move `hello_onload.lua`'s content into a brand new `scripts/OnKey/` file instead (with a `KEYVAL` line
  added) — confirm it now behaves like `hello_log.lua` instead: silent until pressed, not automatic.
- Guess, then check: if you load into a level, then load into a *second* level without closing the game,
  does an `OnLoad` script from the first level's load also print again for the second load? (It should —
  `OnLoad` scripts aren't tied to a specific level, they run on *every* level-load event.)

## Where this comes from

- [Getting Started: The script loader](../getting-started#2-the-script-loader-for-anything-that-should-run-automatically)
  — the full, precise trigger conditions for both folders.
- [Your First Mod: Step 2](../first-mod#step-2-make-it-automatic-with-onload) — `OnLoad` introduced in more
  depth, including when you'd reach for the third option, `OnBoot`, instead.

**Next:** [Tutorial 5: Why `import()`?](why-import) — you've already used it once (Tutorial 2) and skipped
it twice (Tutorial 3). Time to find out why.
