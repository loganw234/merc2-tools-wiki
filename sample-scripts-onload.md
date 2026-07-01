---
title: OnLoad Scripts
parent: Sample Scripts
grand_parent: Recipes
nav_order: 2
---

# OnLoad Scripts

Complete `.lua` files meant to be dropped into `scripts/OnLoad/` — see [Getting Started](getting-started)
for what makes `OnLoad` different from `OnBoot`/`OnKey` if you haven't read that yet.

<details class="script-entry" markdown="1">
<summary><strong>WardrobeUnlocker.lua</strong> — Unlocks every character's outfit for selection from any character's own wardrobe menu.</summary>

Normally the HQ wardrobe only offers a character's own small, curated outfit list, further limited to
however many the game has currently unlocked for them. This merges every character's outfits into
whichever character you're currently playing, and removes that unlock cap — full breakdown of how and
why this works, including the wrong turns along the way, in
[Case Study: Overriding a Function](case-study-function-override).

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

</details>
