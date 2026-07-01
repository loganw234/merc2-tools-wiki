---
title: "Case Study: Overriding a Function"
nav_order: 5
---

# Case Study: Safely Overriding a Function

Everything in [Recipes](recipes) either reads a value or writes one field. This page is different — it
walks through **replacing a piece of the game's own logic** with your own, end to end: what the original
code does, three approaches that turned out to be wrong (and why), the one that actually worked,
confirmed in-game, and the general lesson underneath all of it.

The example: the HQ wardrobe normally only lets a character wear outfits from their own small, curated
list. The goal — make every outfit, for every character, available from any character's wardrobe menu,
**without hand-copying model names into a new table** — if a mod later adds a new outfit to the game's
own data, this approach should pick it up automatically, with no code changes.

## The starting point: three real tables/functions, three different rules

Three pieces of `vz/wifpmcinterior.lua` matter here, and they don't all behave the same way:

- **`_tOutfits`** — a hero-keyed table (`chris` / `jennifer` / `mattias`), each holding that hero's own
  short list of `{Name, Model, PlayerVisibleName}` entries. Declared **without** `local` — genuinely
  global, reachable from outside the file via `import("WifPmcInterior")`.
- **`GetAvailableCostumes()`** — also **not** `local`. Returns how many of the current hero's outfits are
  currently unlocked. This is the gate that limits the wardrobe menu to only a few entries early in the
  game.
- **`_SelectOutfit(uGuid)`** — the function that actually builds and shows the wardrobe menu. Also not
  `local`, but far riskier to touch than the first two (see below).

Two functions downstream matter too, called once the player picks something:

```lua
function _ChangeOutfit(uGuid, iIndex, fCallback, tCallbackArgs)
  if uGuid == Player.GetPrimaryCharacter() then
    _WardrobeOpen = false
  end
  MrxState.Enter(MrxState.STATE_WAITFORGAME, _CompleteChangeOutfit, {uGuid, iIndex, fCallback, tCallbackArgs})
end

function _CompleteChangeOutfit(uGuid, iIndex, fCallback, tCallbackArgs)
  local sHero = MrxUtil.GetCharacterIdentity(uGuid)
  local tOutfits = _tOutfits[sHero]
  local sModelName = tOutfits[iIndex].Model
  Player.SetProfileCostume(iIndex - 1)
  Player.SetOutfit(uGuid, sModelName)
  -- ...network sync, preening VO, state-machine exit...
end
```

The detail that ends up mattering most: `_CompleteChangeOutfit` takes a **numeric index**, not an outfit
table, and re-reads `_tOutfits[sHero]` **fresh, by index, every time it runs** — it never caches a copy
anywhere. Whatever is sitting in `_tOutfits[sHero]` *at the moment the player picks something* is what
gets applied.

## Three wrong turns first

### Wrong turn 1: "just walk `MrxPlayer._tCharacterMap`"

The original idea was to read `mrxplayer.lua`'s full character/model registry (`_tCharacterMap`) instead
of `_tOutfits`, since it's larger and includes NPC/unlockable models. Checking source first: that table
is declared `local _tCharacterMap = {...}`. A genuine Lua `local` is invisible outside the file it's
declared in, **no matter what** — `import()` only exposes a module's non-`local` top-level names, and
this isn't one. There's no way to read this table from outside at all; `mrxplayer.lua` only exposes two
narrow functions against it (`GetTemplateAndModelName`, a single-entry lookup, and `SetCharacterMap`, a
wholesale replace). Neither gives you the live, iterable table the plan needed. Dead end — but a useful
one, since it's the clearest possible example of what `local` actually means in this module system: not
"harder to reach," but genuinely unreachable.

`_tOutfits` in `wifpmcinterior.lua`, found while looking for the actual wardrobe code (which turns out to
live there, not in `mrxhq.lua`), had no such problem — declared without `local`, so it *is* reachable.

### Wrong turn 2: replace `_SelectOutfit` entirely

Next attempt: fully rewrite `_SelectOutfit` to skip the availability gate and build the menu directly.
This actually got as far as being proposed as workable code — but it was wrong in a way that would have
caused real bugs: it called `_ChangeOutfit(uGuid, tOutfit)`, passing an outfit **table**, when the real
function expects a numeric **index**. It also quietly dropped the original's co-op branch
(`Net.IsServer() and uGuid == Player.GetSecondaryCharacter()`, which routes the second player's own
client to build its own menu instead of having the server do it) and the "fewer than 2 outfits unlocked"
tutorial-dialog special case. None of that was intentional — it was simply lost by reimplementing instead
of reading closely enough first. This is the general risk of overriding a function: **you inherit all of
its responsibilities**, not just the one line you wanted to change, and every one you don't reproduce is
a silent regression, not an error.

### Wrong turn 3: hijack the shared menu builder

Pagination in the wardrobe menu comes from `MrxMultiPageMenu`, and the next idea was to intercept
`MrxMultiPageMenu.AddOption`/`Display` directly to inject extra entries at that layer. Reading
`mrxmultipagemenu.lua` fully closed this off for two reasons. First, it made the idea unnecessary:
pagination is already fully automatic (`_knMaxOptionsPerPage = 8`, with "Next page"/"Previous page"
entries generated for you) — there was never a pagination problem to solve. Second, it made the idea
actively bad: `MrxMultiPageMenu` is shared by many systems (`MrxCheatBootstrap`'s own menus use the exact
same module). Wrapping it globally would affect every menu built anywhere in the game, with no clean way
to tell "this call is from the wardrobe" apart from "this call is from the cheat menu."

## What actually worked

Once `_ChangeOutfit`'s real signature (index into `_tOutfits[sHero]`, re-read live every call) was
understood, the fix collapsed to two small, additive changes — no rewriting `_SelectOutfit` or anything
downstream of it at all:

```lua
import("WifPmcInterior")
import("MrxUtil")

local sHero = MrxUtil.GetCharacterIdentity(Player.GetPrimaryCharacter())

-- 1. Merge every hero's outfits into the current hero's own bucket (walks the LIVE table --
--    if a mod adds a new hero or a new outfit to _tOutfits later, this picks it up automatically,
--    since this loop reads the table fresh each time it runs, not a hardcoded copy)
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
wardrobe menu (all three heroes' outfits merged into one list, auto-paginated at 8 entries per page),
built entirely by the game's own unmodified `_SelectOutfit`/`_ChangeOutfit`/`_CompleteChangeOutfit` —
network sync, the `MrxState` transition, and preening VO all still run exactly as they did before, because
none of that code was touched:

![The merged, auto-paginated wardrobe menu in-game — "Select an outfit: (Page 1/2)", listing Next page, Default, Tactical, Sleeveless, Catsuit, Chicken, Default, Metal, and Cancel, with the currently-worn chicken-suit character model visible behind the dialog.](img/funcoverride.png)

## Why it works

Two mechanisms from earlier in this wiki are doing all the real work here:

- **Tables are references, not copies.** `WifPmcInterior._tOutfits[sHero] = tMerged` doesn't create a
  parallel "modded" table alongside the original — it *is* the same table `_ChangeOutfit`/
  `_CompleteChangeOutfit` read from, because there's only ever one `_tOutfits` table in memory, and every
  piece of code (yours or the game's) that says `_tOutfits` is pointing at that same object.
- **Global name lookups happen at call time, not at definition time.** `_SelectOutfit` calls the bare
  name `GetAvailableCostumes()`, which Lua resolves through the file's own environment table *at the
  moment it's called* — not once, when the file was first loaded. Reassigning
  `WifPmcInterior.GetAvailableCostumes` from outside changes what that lookup finds on the *next* call,
  even though the reassignment happened from a completely different script. This was the one genuinely
  untested assumption going into this — confirmed correct by the result.

## Known limitations

- **Doesn't survive a full game restart.** The outfit choice does persist through loading screens within
  a session (this override reapplies via `OnLoad`, so it's re-established every level load), but nothing
  here writes to save data — it's purely live, in-memory state, same as everything else in this wiki.
  Not a bug, just worth knowing going in.
- **Index `2` in the merged list is silently unavailable** through the normal menu — the original
  `_SelectOutfit` loop always excludes position 2 unless a cheat code was entered (`Net.HasPlayerUnlockedCode()`),
  and that logic wasn't touched. Whatever outfit happens to land at index 2 after merging (`pairs()`
  iteration order over `_tOutfits` isn't guaranteed stable) just won't show up.
- **Untested: true multiplayer, non-host client.** `_SelectOutfit` calls `Player.GetAvailableCostumes()`
  (a different, native engine function) on the client path and the local `GetAvailableCostumes()` only on
  the server/host path. This override only touches the local one — a non-host client in a real multiplayer
  session would likely still see the original, gated list. Untested; flagging honestly rather than
  guessing.

## The general pattern

If you want to apply this same technique to a different piece of game logic:

1. **Find the actual gate/data**, not just the function that visibly does the thing. Here, the real
   obstacle wasn't the menu-building function at all — it was one small accessor (`GetAvailableCostumes`)
   two calls away.
2. **Prefer merging into existing live tables over replacing functions.** Every function downstream of
   `_tOutfits` kept working, unmodified, because they all re-read it fresh. Full-function replacement
   should be a last resort, not a first attempt — see wrong turn 2.
3. **Read every function you're *not* changing just as carefully as the one you are.** The co-op branch
   and the tutorial-dialog special case in `_SelectOutfit` were never touched precisely because they were
   read and understood well enough to know they didn't need to be.
