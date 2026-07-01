---
title: Sample Scripts
parent: Recipes
nav_order: 2
---

# Sample Scripts

Complete, ready-to-drop-in `.lua` files — as opposed to [Snippets](snippets), which are small building
blocks meant to be copied into something you're already writing. Organized by which `scripts/` folder
each one belongs in (see [Getting Started](getting-started) if `OnBoot`/`OnLoad`/`OnKey` isn't familiar
yet).

This page is meant to grow with community contributions — if you've built something reusable, this is
where it goes.

## OnBoot

No submissions yet — if you've built one, this is a good place for it.

## OnLoad

### `WardrobeUnlocker.lua`

Unlocks the HQ wardrobe fully: every character's outfit becomes selectable from any character's own
wardrobe menu, instead of being limited to that character's small default list and however many the game
has currently unlocked for them.

```lua
import("WifPmcInterior")
import("MrxUtil")

local sHero = MrxUtil.GetCharacterIdentity(Player.GetPrimaryCharacter())

-- Merge every hero's outfits into the current hero's own bucket (walks the LIVE table --
-- if the game's own data gains a new hero or a new outfit later, this picks it up
-- automatically, since this loop reads the table fresh each time it runs)
local tMerged = {}
for sOtherHero, tList in pairs(WifPmcInterior._tOutfits) do
  for _, tOutfit in ipairs(tList) do
    table.insert(tMerged, tOutfit)
  end
end
WifPmcInterior._tOutfits[sHero] = tMerged

-- Stop the availability gate from clipping the merged list back down to a handful of entries
WifPmcInterior.GetAvailableCostumes = function()
  return table.getn(WifPmcInterior._tOutfits[sHero])
end
```

**Confirmed working by live testing.** Reapplies every level load (that's why it belongs in `OnLoad`, not
`OnBoot`), so the unlocked wardrobe persists through loading screens within a session — it does not
persist through a full game restart, since nothing here touches save data.

![The merged, auto-paginated wardrobe menu in-game — "Select an outfit: (Page 1/2)", listing Next page, Default, Tactical, Sleeveless, Catsuit, Chicken, Default, Metal, and Cancel, with the currently-worn chicken-suit character model visible behind the dialog.](img/funcoverride.png)

Full breakdown of how and why this works, including the wrong turns along the way, in
[Case Study: Overriding a Function](case-study-function-override).

## OnKey

No submissions yet — if you've built one, this is a good place for it.
