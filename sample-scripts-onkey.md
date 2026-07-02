---
title: OnKey Scripts
parent: Sample Scripts
grand_parent: Recipes
nav_order: 3
---

# OnKey Scripts

Complete `.lua` files meant to be dropped into `scripts/OnKey/` — see [Getting Started](getting-started)
for how `OnKey` binding/`KEYVAL` works if you haven't read that yet.

<details class="script-entry" markdown="1">
<summary><strong>OpenCheatMenu.lua</strong> — Opens the game's own dev cheat menu with a single hotkey press.</summary>

The whole entry point of [`MrxCheatBootstrap`](resident/mrxcheatbootstrap) is one call,
`_G.Cheat.DisplayOptions()` — this just wires it to a hotkey instead of typing it into the console every
time.

```lua
local KEYVAL = "f2"  -- must be in the first 10 lines -- pick any key you like, see the note below

_G.Cheat.DisplayOptions()
```

**Confirmed working** — this reuses the exact `_G.Cheat.DisplayOptions()` call already live-tested on the
[`MrxCheatBootstrap`](resident/mrxcheatbootstrap) page; wiring it to `OnKey` doesn't change its behavior,
just when it fires.

![The in-game cheat menu opened via the hotkey — "Welcome to the Cheat Menu." with options Add cash, Add fuel, Add support, Modify attitude, Unlock all landing zones, Dispense all rewards, and Close this menu, with the player character standing in the HQ courtyard behind the dialog.](img/cheatmenu.png)

Picking a different key: `KEYVAL` (or the matching entry in `lua_loader.ini`'s `[OnKey]` section) needs a
recognized key name — see [Your First Mod](first-mod) for the mechanics of how `KEYVAL` gets picked up.
For the full list of valid Windows virtual-key names/codes to choose from, see Microsoft's own reference:
[Virtual-Key Codes](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes) (this is
the same link the loader's own auto-generated `lua_loader.ini` points you to).

</details>

<details class="script-entry" markdown="1">
<summary><strong>ConsoleCheatsMenu.lua</strong> — A custom menu recreating the classic console-release D-pad cheat codes (fill fuel, give all airstrikes/supplies/vehicles, infinite ammo, invincibility, unlock costumes/grapple) as a single hotkey menu. <strong>Partially unverified — see below.</strong></summary>

The original D-pad button-sequence cheat codes from the console releases aren't implemented in Lua
anywhere in this corpus — they're native/engine code, unreachable from here. Rather than trying to
recreate D-pad sequence detection from scratch, this just puts the same *effects* behind a
[`MrxMultiPageMenu`](resident/mrxmultipagemenu)-based menu, the same UI pattern
[`MrxCheatBootstrap`](resident/mrxcheatbootstrap) itself uses, triggered by a hotkey instead of a button
sequence.

```lua
local KEYVAL = "f3"  -- must be in the first 10 lines

import("MrxMultiPageMenu")
import("MrxPmc")
import("MrxSupportData")

local function GiveAllOfType(sType, nQty, sExcludeKey)
  for sKey, tData in pairs(MrxSupportData.tSupportData) do
    if tData.sType == sType and sKey ~= sExcludeKey then
      MrxPmc.AddSupportQty(sKey, nQty)
    end
  end
end

local function GiveAllVehicles()
  for sKey, tData in pairs(MrxSupportData.tSupportData) do
    if tData.sType ~= "Supply" and tData.sType ~= "Airstrike" then
      MrxPmc.AddSupportQty(sKey, 25)
    end
  end
end

local function FillFuel()
  MrxPmc.AddFuelQty(MrxPmc.GetFuelCapacity() - MrxPmc.GetFuelQty())
end

local function UnlockAllCostumes()
  import("WifPmcInterior")
  import("MrxUtil")
  local sHero = MrxUtil.GetCharacterIdentity(Player.GetPrimaryCharacter())
  local tMerged = {}
  for sOtherHero, tList in pairs(WifPmcInterior._tOutfits) do
    for _, tOutfit in ipairs(tList) do
      table.insert(tMerged, tOutfit)
    end
  end
  WifPmcInterior._tOutfits[sHero] = tMerged
  WifPmcInterior.GetAvailableCostumes = function()
    return table.getn(WifPmcInterior._tOutfits[sHero])
  end
end

MrxMultiPageMenu.Reset()
MrxMultiPageMenu.AddOption("Fill Fuel", FillFuel)
MrxMultiPageMenu.AddOption("Give All Airstrikes (except nuke)", GiveAllOfType, {"Airstrike", 1, "nuke"})
MrxMultiPageMenu.AddOption("Give All Supplies", GiveAllOfType, {"Supply", 1})
MrxMultiPageMenu.AddOption("Give All Vehicles (25 each)", GiveAllVehicles)
MrxMultiPageMenu.AddOption("Give Nuke (25)", MrxPmc.AddSupportQty, {"nuke", 25})
MrxMultiPageMenu.AddOption("Infinite Ammo", Object.SetInfiniteAmmo, {Player.GetPrimaryCharacter(), true})
MrxMultiPageMenu.AddOption("Invincibility", Object.SetInvincible, {Player.GetPrimaryCharacter(), true, "ConsoleCheatsMenu"})
MrxMultiPageMenu.AddOption("Unlock All Costumes", UnlockAllCostumes)
MrxMultiPageMenu.AddOption("Unlock Grappling Hook", MrxPmc.AddEquipment, {"GrapplingHook"})
MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
MrxMultiPageMenu.Display("Console Cheats:")
```

**What's confirmed vs. not**, being specific rather than blanket-labeling the whole thing:

- **Confirmed working** (reused directly from already-tested pages): `MrxPmc.AddSupportQty` (give
  all airstrikes/supplies/vehicles/nuke), `MrxPmc.AddFuelQty`/`GetFuelQty`/`GetFuelCapacity` (fill fuel),
  `Object.SetInfiniteAmmo`, and the wardrobe-merge logic (unlock all costumes) — see
  [`MrxCheatBootstrap`](resident/mrxcheatbootstrap) and `WardrobeUnlocker.lua` above.
- **Not yet individually tested**: `Object.SetInvincible(uGuid, bInvincible, sReason)` and
  `MrxPmc.AddEquipment(sName)` are both real, confirmed-to-exist functions (verified against source,
  including that `"GrapplingHook"` is the correct equipment key in `WifEquipmentData._tEquipment`), but
  neither call has actually been fired and observed in-game yet.
- **Not yet tested as a whole**: looping over `tSupportData` and calling `AddSupportQty` many times in a
  row (rather than once, as already confirmed) hasn't been observed end-to-end — should work, since it's
  the same confirmed call in a loop, but "should" isn't "confirmed."
- **Known simplification**: the original codes note "executable by either player, only affects the
  player who executed it." This version always targets `Player.GetPrimaryCharacter()` — resolving "the
  player who pressed this specific hotkey" in split-screen/co-op hasn't been figured out yet.

</details>

