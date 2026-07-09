---
title: "10. Finding Something in the World by Name"
parent: Tutorials
nav_order: 10
---

# Tutorial 10: Finding Something in the World by Name

> Built from `Pg.GetGuidByName`, a call already used and confirmed elsewhere on this wiki (cited as a real
> call site on the [Event namespace](../namespaces/event) page's `ObjectProximity` entry) — wrapped in the
> `pcall` pattern from [Tutorial 6](pcall-safety) as its intended real-world use, not just an exercise.

Every tutorial so far has worked with things the game handed you directly — your own character, your own
cash. The world is full of *other* things too, and most of them have names. This tutorial looks one up.

## The code

Create `scripts/OnKey/finding_by_name.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

local sTargetName = "PutANameHere"  -- see below for where to get a real one

local bOk, uFound = pcall(Pg.GetGuidByName, sTargetName)

if bOk and uFound then
  local x, y, z = Object.GetPosition(uFound)
  Loader.Printf("[finding_by_name] found '" .. sTargetName .. "' at " .. x .. ", " .. y .. ", " .. z)
else
  Loader.Printf("[finding_by_name] '" .. sTargetName .. "' was not found")
end
```

## Finding a real name to try

`"PutANameHere"` is a placeholder — it won't exist, and that's fine as your very first test (see what a
miss looks like below). For a real hit, you need an actual object name from the game.
[Spawn Reference: Names Resolved by Name](../spawn-reference/getguidbyname) is built exactly for this — a
searchable table of every name real decompiled scripts have ever passed to `Pg.GetGuidByName`, with a
filter box. A handful are marked **template** (also spawnable via `Pg.Spawn`); most are marked
**level-instance** — a placed object that only resolves while its specific mission/layer is actually
loaded, so a miss there doesn't necessarily mean the name is wrong, just that you're not in the right
place for it right now.

Pick any name from that table, drop it in as `sTargetName`, load into a level, and press **Insert**.

## Reading both outcomes

With a name that exists:

```
[finding_by_name] found 'SomeRealName' at 1234.5, 67.8, -910.2
```

With `"PutANameHere"` (or any name that doesn't exist):

```
[finding_by_name] 'PutANameHere' was not found
```

> **[Image placeholder — `../img/findingbynamelog.png`]** Screenshot of `lua_loader_printf.log` showing
> both outcomes together — one `found '...' at x, y, z` line from a real name, and one
> `'...' was not found` line from a made-up name — so both the hit and the miss are visible side by side.

Neither case is an error, a crash, or a red banner in your log — both are completely ordinary results.
That's exactly why this tutorial reaches for [Tutorial 6](pcall-safety)'s `pcall` pattern: looking something
up by name is the textbook case of "this might just not be there," not a real failure.

## What's actually happening

`Pg.GetGuidByName(sName)` searches the currently loaded world for an object with that name and hands back
its `uGuid` if found. Wrapping it in `pcall` and then checking `bOk and uFound` (not just `uFound` on its
own) covers both ways this can come back empty-handed: a clean "didn't find it," or an actual error
depending on what's loaded right now. Once you have a real `uGuid`, it behaves exactly like every other one
you've used in this ladder — [Tutorial 3](reading-state)'s `Object.GetPosition(uChar)` and this tutorial's
`Object.GetPosition(uFound)` are the same call, on two different kinds of thing.

## Try it yourself

- Try a name you're confident is wrong on purpose (a typo of a real one) — confirm you get the "not found"
  branch, not a crash.
- Combine this with [Tutorial 2](hello-screen): call `MrxTutorialManager.ShowMessage(...)` with the found
  coordinates instead of only logging them.
- Combine this with [Tutorial 9](reacting-to-events): once you've found a real object's `uGuid`, try
  registering `Event.Create(Event.ObjectDeath, {uFound}, ...)` against it, in an `OnLoad` script instead of
  `OnKey`.

## Where this comes from

- [Spawn Reference: Names Resolved by Name](../spawn-reference/getguidbyname) — the full searchable table
  of confirmed names to test with.
- [Event: `ObjectProximity`](../namespaces/event#gameplay--object-events) — a real, confirmed call site
  using `Pg.GetGuidByName` in context.

**Next:** [Tutorial 11: Editing an Existing Script](editing-existing-scripts) — every tutorial so far had
you write something from scratch. The last one hands you a real, much bigger script someone else wrote,
and asks you to change just one thing about it.
