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
<summary><strong>WardrobeUnlocker.lua</strong> — Unlocks every character's outfit, plus 40 named NPC/character skins, for every hero's own wardrobe menu.</summary>

Normally the HQ wardrobe only offers a character's own small, curated outfit list, further limited to
however many the game has currently unlocked for them. This merges every hero's outfits together, adds a
curated roster of named NPC/character skins on top (PMC & allies, Venezuela, Allied Nations, China,
Guerrillas, Pirates, Universal Petroleum, civilian/misc), and gives the full combined list to **every**
hero, not just whichever one happens to be active — full breakdown of how and why the underlying
technique works, including the wrong turns along the way, in
[Deep Dive: Overriding a Function](deep-dives/function-override).

```lua
import("WifPmcInterior")

-- =========================== CONFIG ===========================
-- PRESET: set to a model code to automatically wear it on load, e.g.
--   local PRESET = "pmc_hum_obama"
-- Leave "" (blank) for no preset -- you keep your normal look and just pick
-- skins from the wardrobe menu.
local PRESET = ""

-- Verified-working NPC/character skins added to the wardrobe menu, on top of the
-- game's own Chris/Jennifer/Mattias outfits (which get merged in below).
-- Format: { "Menu Label", "model_code" }.  Add/remove freely.
local SKINS = {
  -- PMC & allies
  { "Fiona",                     "pmc_hum_fiona" },
  { "Eva",                       "pmc_hum_eva" },
  { "Diablo",                    "pmc_hum_diablo" },
  { "Hoang",                     "pmc_hum_hoang" },
  { "Stealth",                   "pmc_hum_stealth" },
  { "PMC Mechanic",              "pmc_hum_mechanic" },
  { "Blanco (PMC)",              "pmc_hum_blanco" },
  { "Helicopter Pilot",          "pmc_hum_helipilot" },
  { "Prop Pilot",                "pmc_hum_proppilot" },
  -- Venezuela
  { "Solano",                    "vz_hum_solano" },
  { "Carmona",                   "vz_hum_carmona" },
  { "Blanco (VZ)",               "vz_hum_blanco" },
  { "VZ Captain",                "vz_hum_captain" },
  { "VZ Deathsquad",             "vz_hum_deathsquad_a" },
  { "VZ Elite",                  "vz_hum_soldierelite_a" },
  -- Allied Nations
  { "Allied Boss",               "al_hum_boss" },
  { "Allied Officer",            "al_hum_officer_a" },
  { "Allied Pilot",              "al_hum_pilot" },
  { "Allied Recruit 1",          "al_hum_starter01" },
  { "Allied Recruit 2",          "al_hum_starter02" },
  -- China
  { "Chinese Boss",              "ch_hum_boss" },
  { "Chinese Prisoner",          "ch_hum_prisoner" },
  -- Guerrillas
  { "Guerilla Boss",             "gr_hum_boss" },
  { "Guerilla Boss (Disguise)",  "gr_hum_boss_fake" },
  { "Guerilla Advisor",          "gr_hum_advisor" },
  { "Guerilla Elite",            "gr_hum_elite" },
  -- Pirates
  { "Pirate Boss",               "pr_hum_boss" },
  { "Pirate Worker",             "pr_hum_worker" },
  -- Universal Petroleum
  { "UP Boss",                   "oc_hum_boss" },
  { "UP Executive",              "oc_hum_executive" },
  { "UP Board Member",           "oc_hum_boardmember" },
  { "UP Mercenary",              "oc_hum_mercenary_a" },
  { "UP Pilot",                  "oc_hum_pilot" },
  { "Fireman",                   "oc_hum_fireman" },
  -- Civilian / misc
  { "Doctor",                    "civ_hum_doctorfemale" },
  { "Police Officer",            "police_hum_officer_b" },
  { "Beach Girl A",              "civ_hum_beachfemale_a" },
  { "Beach Girl B",              "civ_hum_beachfemale_b" },
  { "Beach Girl C",              "civ_hum_beachfemale_c" },
  { "Beach Girl D",              "civ_hum_beachfemale_d" },
}
-- ==============================================================

-- Build the merged wardrobe once per load (guarded so a re-run in the same
-- session can't stack duplicate entries).
if WifPmcInterior and WifPmcInterior._tOutfits and not WifPmcInterior._wardrobePlus then
  WifPmcInterior._wardrobePlus = true

  -- 1) collect the game's own outfits (every hero) so any character can pick them
  local tAll = {}
  for _, tList in pairs(WifPmcInterior._tOutfits) do
    for _, tOutfit in ipairs(tList) do
      table.insert(tAll, tOutfit)
    end
  end
  -- 2) append our verified NPC skins (plain label = shown as-is in the menu)
  for _, s in ipairs(SKINS) do
    table.insert(tAll, { Name = s[1], Model = s[2], PlayerVisibleName = s[1] })
  end
  -- 3) give every hero the full merged list
  for sHero in pairs(WifPmcInterior._tOutfits) do
    WifPmcInterior._tOutfits[sHero] = tAll
  end
  -- 4) stop the availability gate from clipping the list back down
  WifPmcInterior.GetAvailableCostumes = function()
    return table.getn(tAll)
  end

  Hud.EventFanfare:Commence({ sType = "outfit", vText = "Wardrobe Unlocked!" })
end

-- Optional preset: wear a chosen skin on load (retries until the character exists).
if PRESET ~= "" then
  local tries = 0
  local function applyPreset()
    local uChar = Player.GetPrimaryCharacter()
    if uChar then
      pcall(Player.SetOutfit, uChar, PRESET)
    elseif tries < 20 then
      tries = tries + 1
      Event.Create(Event.TimerRelative, { 0.5 }, applyPreset)
    end
  end
  applyPreset()
end
```

**Confirmed working by live testing** (the merge-and-override mechanism itself, unchanged from the
original version this was built on). Reapplies every level load (that's why it belongs in `OnLoad`, not
`OnBoot`), guarded by `_wardrobePlus` so a mid-session re-run can't stack duplicate entries; the unlocked
wardrobe persists through loading screens within a session but not through a full game restart, since
nothing here touches save data. `sType = "outfit"` is a confirmed entry in `EventFanfare`'s own texture
table — see
[Hud: EventFanfare sType catalog](namespaces/hud#eventfanfare-stype-catalog-and-the-custom-toast-trick)
for the full list of valid styles.

![The merged, auto-paginated wardrobe menu in-game — "Select an outfit: (Page 1/2)", listing Next page, Default, Tactical, Sleeveless, Catsuit, Chicken, Default, Metal, and Cancel, with the currently-worn chicken-suit character model visible behind the dialog.](img/funcoverride.png)

*This screenshot predates the expanded NPC roster above — at 40 extra entries plus every hero's own
outfits merged together, the real current menu runs well past the 2 pages shown here.*

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
