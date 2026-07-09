---
title: "6. Don't Let One Bad Line Kill Your Script"
parent: Tutorials
nav_order: 6
---

# Tutorial 6: Don't Let One Bad Line Kill Your Script

> Built from the confirmed `pcall` pattern already documented in
> [Snippets](../snippets#protect-a-risky-call-with-pcall) and used in nearly every real script on this
> wiki — this page isolates it as its own lesson instead of a footnote inside a bigger example.

[Tutorial 5](why-import) ended with a real error in your log file. What it didn't show you: when a Lua
script hits an error like that, **everything after that line in the same run stops executing.** If that
bad line was in the middle of a longer script, everything below it silently never happens — no crash, no
obvious warning on screen, just... nothing, and you'd have no idea why.

## See the problem for yourself

Create `scripts/OnKey/pcall_safety.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

Loader.Printf("[pcall_safety] about to do something risky")
MrxTutorialManager.ShowMessage("test")  -- no import() -- this WILL fail, on purpose
Loader.Printf("[pcall_safety] this line should never print")
```

Load into a level, press **Insert**, and check your log:

```
[pcall_safety] about to do something risky
attempt to index global 'MrxTutorialManager' (a nil value)
```

The second `Loader.Printf` — "this line should never print" — really didn't. One bad call took the rest
of the script down with it.

## The fix: `pcall`

```lua
local KEYVAL = "insert"

Loader.Printf("[pcall_safety] about to do something risky")

local bOk, sError = pcall(function()
  MrxTutorialManager.ShowMessage("test")  -- still no import() -- still fails
end)

if not bOk then
  Loader.Printf("[pcall_safety] that failed, but here's why: " .. tostring(sError))
end

Loader.Printf("[pcall_safety] this line DOES print now")
```

Press **Insert** again:

```
[pcall_safety] about to do something risky
[pcall_safety] that failed, but here's why: ...attempt to index global 'MrxTutorialManager' (a nil value)
[pcall_safety] this line DOES print now
```

> **[Image placeholder — `../img/pcallcaughterror.png`]** Screenshot of `lua_loader_printf.log` showing
> all three `[pcall_safety] ...` lines present together, including the caught-error line, with the final
> "this line DOES print now" line visible at the bottom — proving the script kept running.

## What's actually happening

`pcall(f)` calls `f` for you, but instead of letting an error inside `f` kill the rest of your script, it
**catches** the error and hands it back to you as a value. It always returns at least one thing: a boolean
— `true` if `f` ran with no error, `false` if it didn't. When it's `false`, there's exactly one more value
after it: the error message. That's why the pattern is always `local bOk, sError = pcall(...)` — never just
`pcall(...)` with the result thrown away, because `bOk` is the only thing that tells you which case you're
actually in.

This matters most in exactly the situation above: a script with more than one thing to do, where one risky
call (a `uGuid` that might not exist anymore, a module you might have mistyped) shouldn't be allowed to
take out everything else the script was also going to do.

## Try it yourself

- Delete the `pcall` wrapper and confirm the failure comes back — this proves to yourself that `pcall` was
  actually doing something, not just extra ceremony.
- Try `pcall` around a call that *doesn't* fail (like `Player.GetCash()`) — confirm `bOk` comes back `true`
  and the second value is the actual cash number, not an error message.
- [Your First Menu](../first-menu#three-pieces-combined) wraps game-changing calls like
  `Object.SetInfiniteAmmo` in `pcall` without the `function() ... end` wrapper —
  `pcall(Object.SetInfiniteAmmo, uChar, true)` instead. Try that shorter form here: it works the same way
  when the risky thing is a single direct function call rather than several lines together.

## Where this comes from

- [Snippets: Protect a risky call with pcall](../snippets#protect-a-risky-call-with-pcall) — the full
  confirmed writeup, including the shorter no-wrapper form.
- [Your First Menu](../first-menu#three-pieces-combined) — `pcall` used in a real, complete script.

**Next:** [Tutorial 7: Remembering Things: A Press Counter](press-counter) — every script so far forgets
everything the instant it finishes running. Time to fix that.
