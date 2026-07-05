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
[Deep Dive: Overriding a Function](deep-dives/function-override).

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

<details class="script-entry" markdown="1">
<summary><strong>HijackAutoSuccess.lua</strong> — Makes every hijack QTE succeed automatically, with no button presses needed.</summary>

The hijack minigame (`MrxActionHijack`) is entered through one function, `OnMinigameStart`, which sets up
the real input-tracking `Event.Minigame` listener and (for tap/alternate steps) a simulated-opponent timer
that "presses buttons" against the player on its own schedule. Overriding just this one function — same
technique as [Deep Dive: Overriding a Function](deep-dives/function-override) — skips creating either of
those, forces success immediately, and lets the hijacker's already-scheduled struggle animation play out
normally and complete on its own:

```lua
import("MrxActionHijack")
import("MrxGuiHudActionHijack")

MrxActionHijack.OnMinigameStart = function(self)
  local tStep = self[self.nCurrent]
  tStep._buttonPressed = true
  tStep.bSuccess = true
  pcall(MrxGuiHudActionHijack.HideButton, self._hijackerPlayer)
  pcall(Sound.CueSound, 0, "ui_HUD_Minigame_Press_Button")

  -- Multi-round "reactive loop" steps normally finish from inside HandleTapMinigame's own round-scoring
  -- logic, which this override never runs -- so those need to be pushed to completion directly instead.
  if tStep.nReactiveLoop ~= nil and not tStep.bMinigameDone then
    tStep.bMinigameDone = true
    MrxActionHijack.DeleteAllEvents(self)
    MrxActionHijack.DoSuccessAnimation(self)
  end
end
```

**Confirmed working by live testing** — animations play out cleanly with no button presses needed, exactly
as expected: the ordinary (non-reactive-loop) `press`/`hold`/`tap`/`alternate` steps look completely
normal, since the character still plays out their usual struggle animation at its usual pace — the only
difference is that no real input is required (or possible) during it, because `bSuccess` was already
forced `true` before the QTE prompt would have appeared.

</details>

<details class="script-entry" markdown="1">
<summary><strong>CoopTetherRange.lua</strong> — Widens (or removes) how far apart co-op players can wander before getting pulled back together. <strong>Unverified — needs a real co-op session to confirm.</strong></summary>

The co-op "stay together" mechanic — the boundary that kicks in when the second player wanders too far
from the host — is driven by two module-level values, a minimum and a maximum distance, and rebuilding
them is done by re-running the same setup function the game itself uses:

```lua
import("MrxCoop")

MrxCoop.SetupTether(5, 500)  -- (min, max) -- units and real default values unconfirmed, pick numbers to taste
```

**Everything about the mechanism itself is confirmed from source** — `SetupTether(aTetherMin, aTetherMax)`
is a real function, and exceeding the max distance is what actually flips
`Player.SetOutBoundary(secondaryPlayer, true)` for the trailing player. **What's not confirmed:** the
real default `(min, max)` values — there are no calls to `SetupTether()` anywhere in the decompiled
corpus, meaning either the real defaults come from native code, or from one of the handful of files that
failed to decompile — so this script's `(5, 500)` is a placeholder, not a documented default, and the
whole thing hasn't been tested in an actual two-player session yet.

One thing worth knowing if you experiment with this yourself: just reassigning
`MrxCoop.iTetherMax` directly, without calling `SetupTether()` again, won't do anything — the proximity
watchers that actually enforce the distance are created once via `Event.Create(..., iTetherMax, ...)`,
which bakes in whatever value it had *at that moment*. Only a fresh `SetupTether()` call tears down the
old watchers and rebuilds them against the new numbers.

</details>
