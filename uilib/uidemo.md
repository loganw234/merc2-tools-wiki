---
title: "uidemo.lua"
parent: UI Kit Scripts
nav_order: 3
---

# uidemo.lua

The kit's own showcase/smoke test for every widget **other than** [`UI.Menu`](menu) — see
[menudemo.lua](menudemo) for that one. Doubles as copy-paste reference code: a drill-down
[`UI.List`](list) driven directly (no `UI.Menu` builder), a [`UI.Panel`](panel-bar-toast) used as an event
log, a [`UI.Bar`](panel-bar-toast), [`UI.Toast`](panel-bar-toast)s, and both
[`UI.Confirm`/`UI.Input`](confirm-and-input).

## Setup

1. [`uilib.lua`](../uilib/) in `scripts/OnLoad/` → `[OnLoad] uilib.lua=5`.
2. This file in `scripts/OnKey/` → `[OnKey] uidemo.lua=delete`.
3. Press **Delete** to open; press again to hide/show the whole demo without rebuilding it.

## What it demonstrates

- **A drill-down built directly on `UI.List`**, without `UI.Menu`'s tree/builder abstraction — three plain
  item arrays (`ROOT`, `SUB`, `BIG`) and a `goto_menu(items, crumb)` helper that just re-points the same
  list at whichever array is current. See [UI.List's own recipe](list#recipe-driving-a-drill-down-menu-directly-without-uimenu)
  for the extracted pattern.
- **A 30-row scrolling stress test** ("Scrolling stress test", with a header inserted mid-list at row 11) —
  the easiest way to see the scrollbar thumb, the header-skipping cursor, and the eased body-resize
  animation all at once, without needing 30 real menu actions to build one.
- **`UI.Panel` as a rolling event log** — every action taken anywhere in the demo calls a `log(s)` helper
  that pushes a line and drops the oldest past 8, rewriting the whole panel each time. See
  [Panel/Bar/Toast's own recipe](panel-bar-toast#recipe-a-panel-as-a-rolling-event-log).
- **`UI.Bar`** bumped by a fixed increment each press ("Bump the bar"), wrapping back to 0 past 100%.
- **`UI.Confirm` used two different ways**: once as a plain yes/no question ("Ask a question"), and once
  guarding a dismissive action — pressing Back at the menu's root pops a confirm ("Close the demo?") instead
  of closing immediately. See
  [Confirm/Input's own recipe](confirm-and-input#recipe-guarding-a-dismissive-action).
- **`UI.Input`** ("Type something") — a typed prompt whose result gets pushed to both a toast and the event
  log.

## The full script

```lua
local KEYVAL = "delete"          -- key that runs this script (first 10 lines)

_G.UIDEMO = _G.UIDEMO or {}
local D = _G.UIDEMO

local ok, err = pcall(function()

    if not (_G.UI and UI.List) then
        Loader.Printf("[uidemo] uilib.lua has not run yet -- press its key first")
        return
    end

    -- ---- event log helper (a Panel used as a rolling log) -----------
    local function log(s)
        if not D.log then return end
        D.lines = D.lines or {}
        D.lines[#D.lines + 1] = tostring(s)
        while #D.lines > 8 do table.remove(D.lines, 1) end
        for i = 0, 7 do
            D.log:line(i, D.lines[i + 1] or "")
        end
    end

    -- ---- menus -------------------------------------------------------
    local ROOT = {
        { header = "WIDGETS" },
        { label = "Pop a toast",           act = "toast" },
        { label = "Bump the bar",          act = "bar" },
        { label = "Ask a question",        act = "ask" },
        { label = "Type something",        act = "type" },
        { header = "LISTS" },
        { label = "Open a submenu",        act = "sub" },
        { label = "Scrolling stress test", act = "big" },
    }
    local SUB = {
        { header = "SUBMENU" },
        { label = "Toast from down here", act = "toast" },
        { label = "Back to the top",      act = "back" },
    }
    local BIG = { { header = "MANY ROWS (watch the scrollbar + resize)" } }
    for i = 1, 30 do
        if i == 11 then BIG[#BIG + 1] = { header = "A HEADER MID-LIST" } end
        BIG[#BIG + 1] = { label = "Row " .. i .. " -- pick me", act = "toast" }
    end

    local function goto_menu(items, crumb)
        D.at = crumb
        D.list:items(items)
        D.list:crumb(crumb)
    end

    -- ---- action dispatch ---------------------------------------------
    local function on_choose(it)
        if it.act == "toast" then
            UI.Toast("Toast! You picked: " .. it.label)
            log("toast: " .. it.label)
        elseif it.act == "bar" then
            D.val = (D.val or 0) + 0.25
            if D.val > 1 then D.val = 0 end
            D.bar:set(D.val)
            D.bar:label("DEMO BAR  " .. math.floor(D.val * 100) .. "%")
            log("bar -> " .. math.floor(D.val * 100) .. "%")
        elseif it.act == "ask" then
            UI.Confirm{
                text = "Is this library useful?",
                onResult = function(yes)
                    UI.Toast(yes and "Glad to hear it!" or "Harsh, but noted.")
                    log("confirm -> " .. tostring(yes))
                end,
            }
        elseif it.act == "type" then
            UI.Input{
                prompt = "SAY SOMETHING -- ENTER SUBMIT   ESC CANCEL",
                onSubmit = function(text)
                    UI.Toast("You typed: " .. text)
                    log("input: " .. text)
                end,
                onCancel = function() log("input cancelled") end,
            }
        elseif it.act == "sub" then
            goto_menu(SUB, "DEMO > SUBMENU")
            log("entered submenu")
        elseif it.act == "big" then
            goto_menu(BIG, "DEMO > STRESS TEST")
            log("entered stress test")
        elseif it.act == "back" then
            goto_menu(ROOT, "DEMO")
        end
    end

    local function on_back()
        if D.at ~= "DEMO" then
            goto_menu(ROOT, "DEMO")
            log("back to root")
        else
            UI.Confirm{
                text = "Close the demo?",
                onResult = function(yes)
                    if yes then
                        D.shown = false
                        D.list:hide(); D.log:hide(); D.bar:hide()
                        Loader.Printf("[uidemo] hidden -- " .. KEYVAL .. " to reopen")
                    end
                end,
            }
        end
    end

    -- ---- build once, toggle on re-press ------------------------------
    if not D.list then
        D.log = UI.Panel{ x = 380, y = 60, title = "EVENT LOG", lines = 0 }
        D.bar = UI.Bar{ x = 380, y = 300, label = "DEMO BAR  0%", value = 0 }
        D.val = 0
        D.list = UI.List{
            x = 40, y = 60,
            title = "UI DEMO",
            crumb = "DEMO",
            hint  = "UP/DOWN SELECT   ENTER PICK   LEFT BACK",
            items = ROOT,
            focus = true,
            onChoose = on_choose,
            onBack   = on_back,
        }
        D.at = "DEMO"
        D.shown = true
        log("demo built")
        Loader.Printf("[uidemo] built -- " .. KEYVAL .. " toggles it")
    else
        -- rebind callbacks so edits to this file apply on re-run
        D.list.onChoose = on_choose
        D.list.onBack   = on_back
        D.shown = not D.shown
        if D.shown then
            D.list:show():focus()
            D.log:show()
            D.bar:show()
        else
            D.list:hide()
            D.log:hide()
            D.bar:hide()
        end
        Loader.Printf("[uidemo] " .. (D.shown and "shown" or "hidden"))
    end

end)
if not ok then Loader.Printf("[uidemo] ERROR: " .. tostring(err)) end
```

## See also

- [UI.List](list) — the widget this script drives directly, without `UI.Menu`.
- [UI.Panel / UI.Bar / UI.Toast](panel-bar-toast) — the log/bar/toast recipes pulled from this script.
- [UI.Confirm / UI.Input](confirm-and-input) — including the confirm-before-close guard pattern.
- [menudemo.lua](menudemo) — the sibling script covering `UI.Menu` specifically.
