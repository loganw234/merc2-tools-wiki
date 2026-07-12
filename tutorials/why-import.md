---
title: "5. Why import()?"
parent: Tutorials
nav_order: 5
---

# Tutorial 5: Why `import()`?

> Built from the confirmed, live-tested explanation already in the
> [Glossary](../glossary#importname) — this page's contribution is walking through the failure case
> yourself instead of just reading about it.

In [Tutorial 2](hello-screen), `MrxTutorialManager` needed an `import("MrxTutorialManager")` line before
you could call it. In [Tutorial 3](reading-state), `Player` and `Object` needed nothing at all. That
inconsistency isn't an accident, and it isn't optional to understand — get it wrong in a real script and
the failure won't be obvious.

## Reproduce the error on purpose

Create `scripts/OnKey/why_import.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

MrxTutorialManager.ShowMessage("This should fail!")
```

Notice: no `import("MrxTutorialManager")` line. Load into a level and press **Insert**. Nothing shows up on
screen — no popup, no crash you can see. Open `lua_loader_printf.log` anyway (the log file writes error
messages too, not just your own `Loader.Printf` calls):

```
attempt to index global 'MrxTutorialManager' (a nil value)
```

> **[Image placeholder — `../img/importerror.png`]** Screenshot of `lua_loader_printf.log` showing the
> `attempt to index global 'MrxTutorialManager' (a nil value)` error line, in context with a few normal
> `Loader.Printf` lines from earlier tutorials above it for comparison.

That error is Lua telling you, plainly: `MrxTutorialManager` doesn't exist as far as this script is
concerned — it's `nil`, and you can't call `.ShowMessage` on `nil`.

## The fix

```lua
local KEYVAL = "insert"

import("MrxTutorialManager")
MrxTutorialManager.ShowMessage("This should work now!")
```

Press **Insert** again. The popup appears, exactly like [Tutorial 2](hello-screen).

## What's actually happening

This game's Lua code comes in two flavors that look identical to call but behave very differently:

- **Engine namespaces** — `Player`, `Object`, `Event`, `Pg`, and others. These are built into the engine
  itself and are **always** globally available, from any script, with zero setup. This is why
  [Tutorial 3](reading-state)'s `Player.GetCash()` and `Object.GetPosition(...)` just worked.
- **Resident modules** — `MrxTutorialManager`, `MrxPmc`, and roughly 226 others. These are `.lua` files
  the game itself loads (you can browse them under [Resident Modules](../resident/)), and by default
  they're only visible *inside their own file*. `import("Name")` is what pulls one into *your* script's
  environment so you can call it too. Skip it, and the name is simply `nil` where you are — which is
  exactly the error above.

There's no way to tell which is which just by how a call *looks* — `Player.GetCash()` and
`MrxTutorialManager.ShowMessage(...)` are syntactically identical. When in doubt, check the
[Resident Modules](../resident/) index: if it's listed there, it needs `import()`.

## Try it yourself

- Try importing a name that doesn't exist at all — `import("NotARealModule")` — and see what happens
  versus forgetting the import line entirely. Are the two errors the same, or different?
- Remove the `import("MrxTutorialManager")` line again, but this time wrap the call in
  `pcall(function() MrxTutorialManager.ShowMessage("test") end)`. Does the error still show up in your log?
  ([Tutorial 6](pcall-safety) is entirely about what `pcall` changes here and why.)
- Check the [Resident Modules](../resident/) index for `MrxPmc` (used back in
  [Your First Mod](../first-mod#step-3-trigger-it-on-demand-with-onkey)) — confirm for yourself that it's
  listed there as a module, which is exactly why that tutorial's script also needed its own
  `import("MrxPmc")` line.

## Where this comes from

- [Glossary: `import("Name")`](../glossary#importname) — the full explanation, including the one exception
  (functions a module explicitly publishes to `_G` don't need importing).
- [Glossary: engine namespace](../glossary#engine-namespace) — the other half of the distinction.
- [Resident Modules](../resident/) — the landing page explaining the module system in full, and the index
  of every module that needs `import()`.

**Next:** [Tutorial 6: Don't Let One Bad Line Kill Your Script](pcall-safety) — that error you just caused
didn't crash the game, but it silently stopped your script cold. Here's how to stop that from happening.
