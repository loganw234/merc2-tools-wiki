---
title: "Overriding a Function"
parent: Deep Dives
nav_order: 2
---

# Deep Dive: Safely Overriding a Function

Everything in [Snippets](../snippets) either reads a value or writes one field. This page is different — it
walks through **replacing a piece of the game's own logic** with your own, end to end: what the original
approach was, three attempts that turned out to be wrong (and why), the one that actually worked,
confirmed in-game, and the general lesson underneath all of it. Just want the finished result as a
drop-in file? It's on [OnLoad Scripts](../sample-scripts-onload) as `WardrobeUnlocker.lua`.

The example: the HQ wardrobe normally only lets a character wear outfits from their own small, curated
list. The goal — make every outfit, for every character, available from any character's wardrobe menu,
**without hand-copying model names into a new table** — if the game's own data later gains a new outfit,
this approach should pick it up automatically, with no code changes.

## The starting point: three pieces, three different rules

The wardrobe lives behind `import("WifPmcInterior")`. Three things there matter, and they don't all
behave the same way:

- **`_tOutfits`** — a hero-keyed table (`chris` / `jennifer` / `mattias`), each holding that hero's own
  short list of `{Name, Model, PlayerVisibleName}` entries. Genuinely reachable from outside via
  `import("WifPmcInterior")`.
- **`GetAvailableCostumes()`** — also reachable the same way. Returns how many of the current hero's
  outfits are currently unlocked. This turns out to be the actual gate limiting the wardrobe menu to only
  a few entries early in the game. It's a tiny function, just a fallback default over one internal counter:

  ```lua
  function GetAvailableCostumes()
    return _nAvailableCostumes or 1
  end
  ```
- **`_SelectOutfit(uGuid)`** — the function that builds and shows the wardrobe menu itself. Reachable too,
  but far riskier to touch than the first two (see below).

Two more functions matter, both triggered once the player picks something from that menu: one arms a
state-machine transition, and the other is where the actual costume swap happens. The detail that ends up
mattering most, found by reading that second function closely: it takes a **numeric index**, not an
outfit table, and resolves the outfit list **fresh, by that index, every single time it runs** — never a
cached copy:

```lua
local sHero = MrxUtil.GetCharacterIdentity(uGuid)
local tOutfits = _tOutfits[sHero]
local sModelName = tOutfits[iIndex].Model
```

Whatever is sitting in `_tOutfits[sHero]` *at the moment the player picks something* is what gets
applied — not whatever was there when the file first loaded.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

Lua is a **dynamically typed language** — a variable, table field, or function doesn't have a fixed type
locked in ahead of time; it's just whatever value was assigned to it most recently. If a function reads a
table field, it gets whatever's there *right now*, not whatever was there when the game first started.
That single fact is the reason everything on this page works at all: nothing has to be "unlocked" or
"declared modifiable" in advance. If you can reach a name, you can reassign it, and every later read of
that same name sees your new value — because as far as Lua is concerned, there was never an "original"
value that's somehow more official than yours. Whatever was said last is what's true now.

</details>

## Three wrong turns first

### Wrong turn 1: look for a bigger table in `MrxPlayer`

The first idea was to read `MrxPlayer`'s full character/model registry instead of `_tOutfits`, since it's
larger and includes NPC/unlockable models too. Checking first, rather than assuming: that table turned
out to be declared as a genuine Lua `local`. A real `local` is invisible outside the file it's declared
in, **no matter what** — `import()` only exposes a module's non-`local` top-level names, and this wasn't
one. There was no way to read it from outside at all; `MrxPlayer` only exposes two narrow functions
against it (one does a single-entry lookup, the other wholesale-replaces the entire table). Neither gives
you the live, iterable table the plan needed. Dead end — but a useful one, since it's the clearest
possible example of what `local` actually means in this module system: not "harder to reach," but
genuinely unreachable, full stop.

`_tOutfits`, found while looking for the actual wardrobe code (which turns out to live in
`WifPmcInterior`, not in the HQ-management module the search started with), had no such problem — it's
reachable.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

This is worth sitting with, because it cuts against the "dynamic language, everything's flexible" point
above: `local` is the one real exception. It doesn't make a name *harder* to reach from outside its own
file — it makes it **impossible**, by design. Lua enforces this at the language level, not as a
convention. If a name matters to your plan, checking whether it's declared `local` before building
anything around it saves real time.

</details>

### Wrong turn 2: replace the whole menu function

Next attempt: fully rewrite `_SelectOutfit` to skip the availability gate and build the menu directly.
This got as far as looking like workable code — but it had a real bug: it called the costume-change
function with an outfit **table**, when — as established above — that function actually expects a
numeric **index**. It also quietly dropped two things the original handled: a co-op branch (routing the
second player's own client to build its own menu instead of having the host do it for them), and a
"fewer than 2 outfits unlocked" tutorial-dialog special case. None of that was intentional — it was simply
lost by reimplementing instead of reading closely enough first. This is the general risk of overriding a
function: **you inherit all of its responsibilities**, not just the one line you wanted to change, and
every responsibility you don't reproduce becomes a silent regression, not an error you'd notice right
away.

### Wrong turn 3: hijack the shared menu builder

Pagination in the wardrobe menu comes from the game's shared multi-page-menu module, and the next idea
was to intercept its option-adding/display functions directly, to inject extra entries at that layer.
Reading that module fully closed this off for two reasons. First, it made the idea unnecessary:
pagination turned out to already be fully automatic (a fixed number of options per page, with
"Next page"/"Previous page" entries generated for you) — there was never a pagination problem to solve.
Second, it made the idea actively bad: that menu module is shared by many systems across the game — the
in-game cheat menu builds its own menus through the exact same one. Wrapping it globally would affect
every menu built anywhere in the game, with no clean way to tell "this call is from the wardrobe" apart
from "this call is from somewhere else entirely."

## What actually worked

Once the costume-change function's real signature (index into the live outfit table, re-read fresh every
call) was understood, the fix collapsed to two small, additive changes — no rewriting the menu function or
anything downstream of it at all:

```lua
import("WifPmcInterior")
import("MrxUtil")

local sHero = MrxUtil.GetCharacterIdentity(Player.GetPrimaryCharacter())

-- 1. Merge every hero's outfits into the current hero's own bucket (walks the LIVE table --
--    if the game's own data gains a new hero or a new outfit later, this picks it up
--    automatically, since this loop reads the table fresh each time it runs, not a hardcoded copy)
local tMerged = {}
for sOtherHero, tList in pairs(WifPmcInterior._tOutfits) do
  for _, tOutfit in ipairs(tList) do
    table.insert(tMerged, tOutfit)
  end
end
WifPmcInterior._tOutfits[sHero] = tMerged

-- 2. Stop the availability gate from clipping the merged list back down to a handful of entries
WifPmcInterior.GetAvailableCostumes = function()
  return table.getn(WifPmcInterior._tOutfits[sHero])
end
```

**Confirmed working by live testing**, dropped into `scripts/OnLoad/`. The result: a full two-page
wardrobe menu (all three heroes' outfits merged into one list, auto-paginated for you), built entirely by
the game's own unmodified menu/costume-change logic — network sync, the state-machine transition, and the
character voice-line that plays on a costume change all still run exactly as they did before, because
none of that code was touched:

![The merged, auto-paginated wardrobe menu in-game — "Select an outfit: (Page 1/2)", listing Next page, Default, Tactical, Sleeveless, Catsuit, Chicken, Default, Metal, and Cancel, with the currently-worn chicken-suit character model visible behind the dialog.](../img/funcoverride.png)

## Why it works

Two mechanisms from earlier in this wiki are doing all the real work here:

- **Tables are references, not copies.** `WifPmcInterior._tOutfits[sHero] = tMerged` doesn't create a
  parallel "modded" table alongside the original — it *is* the same table the game's own
  costume-change logic reads from, because there's only ever one `_tOutfits` table in memory, and every
  piece of code (yours or the game's) that touches it is pointing at that same object.
- **Global name lookups happen at call time, not at definition time** — the dynamic-typing point from
  above, applied specifically to function calls. The wardrobe-menu function calls the bare name
  `GetAvailableCostumes()`, which Lua resolves through the file's own environment table *at the moment
  it's called* — not once, when the file first loaded. Reassigning `WifPmcInterior.GetAvailableCostumes`
  from outside changes what that lookup finds on the *next* call, even though the reassignment happened
  from a completely different script. This was the one genuinely untested assumption going into this —
  confirmed correct by the result.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

If you're used to languages where functions are compiled once and fixed in place, this is the part that
feels like magic and isn't. In Lua, a "function call" like `GetAvailableCostumes()` is really just "look
up this name, right now, in the current environment, and call whatever's there." There's no special
binding that locks it to one specific piece of code forever — it's exactly as changeable as any other
table field, because under the hood, that's all it is: a table field that happens to hold a function
instead of a number or a string.

</details>

## Known limitations

- **Doesn't survive a full game restart.** The outfit choice does persist through loading screens within
  a session (this override reapplies via `OnLoad`, so it's re-established every level load), but nothing
  here writes to save data — it's purely live, in-memory state, same as everything else in this wiki.
  Not a bug, just worth knowing going in.
- **One merged entry is silently unavailable** through the normal menu — the original menu-building logic
  always excludes one specific position unless a cheat code was entered, and that logic wasn't touched.
  Exactly which outfit lands there after merging isn't guaranteed stable, since Lua doesn't guarantee
  iteration order over this kind of table.
- **Untested: true multiplayer, non-host client.** The wardrobe-menu function calls a different,
  native/engine-level availability check on the client path than the one this override replaces (which
  only applies on the host/server path). A non-host client in a real multiplayer session would likely
  still see the original, gated list. Untested; flagging honestly rather than guessing.

## The general pattern

If you want to apply this same technique to a different piece of game logic:

1. **Find the actual gate/data**, not just the function that visibly does the thing. Here, the real
   obstacle wasn't the menu-building function at all — it was one small accessor two calls away.
2. **Prefer merging into existing live tables over replacing functions.** Every function downstream of
   the outfit table kept working, unmodified, because they all re-read it fresh. Full-function replacement
   should be a last resort, not a first attempt — see wrong turn 2.
3. **Read every function you're *not* changing just as carefully as the one you are.** The co-op branch
   and the tutorial-dialog special case were never touched precisely because they were read and understood
   well enough to know they didn't need to be.
