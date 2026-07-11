---
title: "menudemo.lua"
parent: UI Kit Scripts
nav_order: 2
---

# menudemo.lua

The showcase script for [`UI.Menu`](menu) — nested categories, spawning, a live ON/OFF toggle, and
composing with every other widget in the kit from inside a menu action.

## Setup

1. [`uilib.lua`](../uilib/) in `scripts/OnLoad/` → `[OnLoad] uilib.lua=5`.
2. This file in `scripts/OnKey/` → `[OnKey] menudemo.lua=f3`.
3. In game, press **F3** to open/close. Up/Down move, Enter/Right pick, Left/Esc back.

## What it demonstrates

- **Flat actions** — "Pop a toast", "Heal me": the simplest possible `menu:entry`.
- **A category of spawn buttons** — "Spawn Vehicles", using `ctx:spawn(template, dist)` to drop a vehicle
  a set distance ahead of the player.
- **A nested subcategory** — "Spawn Enemies" contains "Guerilla" and "Chinese", each its own
  `menu:category` two levels deep, demonstrating that `:category` nests as far as you build it.
- **Composing with other widgets mid-action** — "Dialogs" → "Ask a question" pops a
  [`UI.Confirm`](confirm-and-input) via `ctx:confirm`; "Type something" pops a
  [`UI.Input`](confirm-and-input) via `ctx:ask`. Both hand control back to the menu once resolved.
- **The two richer movies from inside a menu action** — "Rich Widgets" → "Contract Board" closes the menu
  and opens a full [`UI.Board`](chat-and-board) (three items, three different `:detail{}` payloads picked
  by an `it.k` tag); "Chat Log" lazily creates and reuses a [`UI.Chat`](chat-and-board) in the corner.
- **A live ON/OFF toggle via `:switch`** — "God Mode" reads/writes `D.god` and calls
  `Object.SetInvincible`, with the label re-rendering `"God Mode: ON"`/`"God Mode: OFF"` automatically.

## The full script

```lua
local KEYVAL = "f3"   -- toggle key (first 10 lines); also add "menudemo.lua=f3" under [OnKey]

-- =====================================================================
--  menudemo.lua -- the ForgeMenu-style UI.Menu, showcased end to end.
--
--  Shows: nested categories, ctx:spawn, a live ON/OFF toggle (function
--  label), and how a menu entry composes with the kit's other widgets
--  (UI.Confirm, UI.Input, UI.Toast).
--
--  SETUP
--    1) uilib.lua in scripts/OnLoad/  ->  [OnLoad] uilib.lua=5
--    2) this file in scripts/OnKey/   ->  [OnKey]  menudemo.lua=f3
--    3) in game, press F3 to open/close. Up/Down move, Enter/Right pick,
--       Left/Esc back.
--
--  This whole file is just DATA + little functions - the library does the
--  widget, input, drawing, and lifecycle.
-- =====================================================================

if not (_G.UI and UI.Menu) then
    Loader.Printf("menudemo: load uilib.lua first ([OnLoad] uilib.lua=5)")
    return
end

_G.MENUDEMO = _G.MENUDEMO or {}     -- keep flags in _G so they survive the OnKey re-run
local D = _G.MENUDEMO

local menu = UI.Menu{ title = "UI KIT DEMO", key = KEYVAL:upper() }

-- --- top-level actions -------------------------------------------------
menu:entry("Pop a toast", function(ctx)
    ctx:hint("Hello from the menu!")
end)

menu:entry("Heal me", function(ctx)
    if ctx.char then pcall(Object.SetHealth, ctx.char, 100) end
    ctx:hint("HEALED")
end)

-- --- spawn buttons (ctx:spawn drops at / ahead of your feet) -----------
menu:category("Spawn Vehicles", function(c)
    c:entry("Diplomat Tank",   function(ctx) ctx:spawn("M1A2 (Full)", 8);            ctx:hint("TANK") end)
    c:entry("Ambassador Heli", function(ctx) ctx:spawn("AH1Z (Full)", 12);           ctx:hint("HELI") end)
    c:entry("Softtop HMMWV",   function(ctx) ctx:spawn("HMMWV (Softtop) (Full)", 8);  ctx:hint("HMMWV") end)
end)

-- --- a NESTED subcategory ---------------------------------------------
menu:category("Spawn Enemies", function(c)
    c:category("Guerilla", function(g)
        g:entry("Soldier",     function(ctx) ctx:spawn("Guerilla Soldier", 6);    ctx:hint("PLACED") end)
        g:entry("Heavy (RPG)", function(ctx) ctx:spawn("Guerilla Heavy (RPG)", 6); ctx:hint("PLACED") end)
    end)
    c:category("Chinese", function(g)
        g:entry("Soldier", function(ctx) ctx:spawn("Chinese Soldier", 6); ctx:hint("PLACED") end)
        g:entry("Sniper",  function(ctx) ctx:spawn("Chinese Sniper", 6);  ctx:hint("PLACED") end)
    end)
end)

-- --- composing with other widgets, via the ctx shortcuts --------------
menu:category("Dialogs", function(c)
    c:entry("Ask a question", function(ctx)
        ctx:confirm("Is this UI kit useful?",
            function() ctx:toast("Glad to hear it!") end,      -- onYes
            function() ctx:toast("Harsh, but noted.") end)     -- onNo
    end)
    c:entry("Type something", function(ctx)
        ctx:ask("SAY SOMETHING -- ENTER SUBMIT   ESC CANCEL",
            function(text) ctx:toast("You typed: " .. text) end)
    end)
end)

-- --- the two richer movies: UI.Board (contracts.gfx) + UI.Chat (chat.gfx) ----
menu:category("Rich Widgets", function(c)
    c:entry("Contract Board", function(ctx)
        ctx:close()                 -- hand the screen (and keys) to the board
        UI.Board{
            title = "CONTRACTS", hint = "UP/DOWN BROWSE   ESC CLOSE", focus = true,
            items = {
                { header = "AVAILABLE" },
                { label = "Oil Refinery Raid", k = 1 },
                { label = "Convoy Ambush",     k = 2 },
                { header = "SIDE JOBS" },
                { label = "Find the HVT",       k = 3 },
            },
            onSelect = function(it, i, board)
                if it.k == 1 then board:detail{ category = "DESTRUCTION", rewards = { "$8,000", "Fuel +300" },
                    objectives = { "Destroy 4 storage tanks", "Stay undetected" }, progress = 0, progressText = "NOT STARTED" }
                elseif it.k == 2 then board:detail{ category = "INTERCEPT", rewards = { "$5,000" },
                    objectives = { "Stop the convoy", "Recover the cargo" }, progress = 0, progressText = "NOT STARTED" }
                elseif it.k == 3 then board:detail{ category = "RECON", rewards = { "$3,000", "Intel" },
                    objectives = { "Locate the HVT", "Verify identity", "Extract" }, progress = 0, progressText = "NOT STARTED" }
                else board:detail{} end
            end,
            onChoose = function(it, i, board) UI.Toast("Accepted: " .. it.label) end,
            onBack   = function(board) board:hide() end,   -- Esc closes; press F3 to reopen the menu
        }
    end)
    c:entry("Chat Log", function(ctx)
        local ch = D.chat
        if not ch then ch = UI.Chat{ title = "RADIO", x = 640 - 360 - 8, y = 8 }; D.chat = ch end   -- top-right corner
        ch:show():push("Misha: slick menu, boss.")
        ctx:hint("pushed a radio line")
    end)
end)

-- --- a live ON/OFF toggle, via the :switch helper (auto ON/OFF label) --
menu:switch("God Mode", function() return D.god end, function(on, ctx)
    D.god = on
    if ctx.char then pcall(Object.SetInvincible, ctx.char, on and true or false, "menudemo") end
    ctx:hint(on and "INVINCIBLE" or "MORTAL AGAIN")
end)

menu:entry("Close", function(ctx) ctx:close() end)

-- Flip open/closed. This file re-runs each time you press F3, so this toggles it.
menu:toggle()
```

## See also

- [UI.Menu](menu) — the widget this script showcases.
- [UI.Confirm / UI.Input](confirm-and-input) / [UI.Chat / UI.Board](chat-and-board) — the widgets it
  composes with via `ctx:confirm`/`ctx:ask` and direct calls.
- [uidemo.lua](uidemo) — the sibling script covering every widget *other* than `UI.Menu`.
