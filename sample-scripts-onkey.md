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

