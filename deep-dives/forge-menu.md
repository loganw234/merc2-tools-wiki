---
title: "Building ForgeMenu — a Reusable Nested-Menu Library"
parent: Deep Dives
nav_order: 13
---

# Deep Dive: Building ForgeMenu — a Reusable Nested-Menu Library

> **Status: new, built on already-confirmed pieces.** The `forge.gfx` movie and the `FlashWidget`-renders-
> and-drives rendering approach are the exact confirmed-live mechanics from [ForgeCam](forgecam) and
> [MissionForge](mission-forge) — this library is a direct, deliberate generalization of MissionForge's own
> render loop (the code says so directly: `render` is "a generic version of MissionForge.refresh"). The
> library itself hasn't accumulated its own separate live-test history yet, but one specific fix baked into
> it (the `WARMUP` re-render workaround below) reads like a real bug that was actually hit and fixed, not a
> defensive guess.

[Building Nested Menus with MrxMultiPageMenu](nested-menus) covers the only way to nest menus using the
game's *native* menu system — and it's real work: no built-in submenu concept, every level hand-written as
its own `Reset`/`AddOption`/`Display` call, menu-builder functions deliberately declared as bare globals to
dodge a declaration-order hazard. ForgeMenu is the answer to "what if nesting didn't require any of that?"
— a small library that reuses the `forge.gfx` Scaleform movie [ForgeCam](forgecam) and
[MissionForge](mission-forge) already prove works, and turns building a nested menu into declaring a plain
tree of categories and entries. No widget code, no navigation-stack bookkeeping, no bare-global gotcha to
know about at all.

## The whole API, up front

```lua
local menu = ForgeMenu.new("MY MENU", { key = "F11" })   -- title shown at the top; key = your toggle key (label only)

menu:entry("Do a thing", function(ctx) ... end)           -- an action leaf

menu:category("Group", function(c)                        -- a sub-menu; c is another menu you add to
    c:entry("Nested action", function(ctx) ... end)
    c:category("Even deeper", function(cc) ... end)        -- categories nest as far as you like
end)

menu:toggle()                                              -- open if closed / close if open (call in OnKey)
```

That's the entire building-block set: `:entry` and `:category`. No separate "Back" option to wire up
anywhere — `:category` gives you a real nested tree, and back-navigation is built into the library once,
not re-derived by every menu author the way [the MrxMultiPageMenu pattern](nested-menus) requires.

### The `ctx` every action receives

| field / call | what it is |
|---|---|
| `ctx.x, ctx.y, ctx.z` | your character's position, read fresh at the moment the action runs |
| `ctx.yaw` | your character's facing, in degrees |
| `ctx.char`, `ctx.player` | the local character / player guids |
| `ctx:spawn(template [, dist])` | spawns `template` at your feet, or `dist` metres ahead (using the same forward-vector convention as MissionForge); returns the guid |
| `ctx:hint("text")` | flashes a message on the menu's bottom line, auto-clearing after ~3s |
| `ctx:print("text")` | writes a line to `lua_loader_printf.log`, prefixed `"ForgeMenu: "` |
| `ctx:close()` | closes the menu from inside an action |

### Live ON/OFF labels

A label isn't limited to a plain string — pass a **function that returns one**, and it's re-evaluated on
every render, which is what a toggle needs:

```lua
_G.MyMenuState = _G.MyMenuState or {}
local S = _G.MyMenuState
menu:entry(function() return S.god and "God: ON" or "God: OFF" end, function(ctx)
    S.god = not S.god
    pcall(Object.SetInvincible, ctx.char, S.god and true or false, "MyMenu")
end)
```

The `_G`-guarded state table is the exact same idiom [Your First Menu](../first-menu#three-pieces-combined)
establishes for a single flat menu — ForgeMenu doesn't change how you persist state across presses, it
only changes how you build the menu structure around it.

## Why the world doesn't pause

This is the detail that separates ForgeMenu from everything upstream of it in this wiki's menu lineage, and
it's worth being explicit about rather than assuming it follows from ForgeCam. The freecam's entire
input-hijack trick exists to solve one specific problem: **continuous analog stick input has no native Lua
touchpoint**, and the only way to get it is to hijack the PDA widget's `"ControllerInput"` event — which,
as a side effect neither MissionForge nor ForgeCam ever needed but had to live with, **pauses the world**.
[MissionForge's own deep dive](mission-forge) inherits that pause because it inherits the PDA hijack for
its camera.

A menu doesn't need continuous analog input at all — just discrete "move selection" / "choose" / "back"
events, which is exactly what [`Loader.PopKeyEvents`](../lua-bridge-api/loader) already provides on its
own, no PDA involved. So `ForgeMenu.lua` never opens the PDA, never touches `MrxState`, and never pauses
anything — it just puts a `FlashWidget` on the HUD and drives it from a plain, unpaused
`Event.TimerRelative` heartbeat:

```lua
tick = function(rt, dt)
    rt.now = (rt.now or 0) + dt
    local ev = Loader.PopKeyEvents()
    if ev and ev ~= "" then
        for i = 1, #ev do dispatchKey(rt, string.byte(ev, i)) end
    end
    ...
end
```

The practical consequence is the first gotcha worth knowing: **the game keeps running while the menu is
open.** Arrow keys and Enter still do whatever they normally do in gameplay at the same time they're
driving your menu, since nothing has suppressed them. Fine for a menu you open standing still; if it
matters, `ForgeMenu.new`'s `opts.keys` lets you remap navigation off the arrow keys entirely.

## How it works

### The render loop is MissionForge's, generalized

The module comment says it outright: `render` is "a generic version of MissionForge.refresh." Where
MissionForge's own render function was written against one specific, hardcoded catalog tree, ForgeMenu's
version walks whatever tree the *caller* built with `:entry`/`:category` — same `SetRow`/`SetCrumb`/
`SetHint`/`SetSelected`/`SetScroll`/`SetPanel` calls into the movie, same breadcrumb-joining, same
scroll-thumb math, same eased panel-height animation — just parameterized over an arbitrary tree instead of
one fixed catalog. The layout constants at the top of the file (`VISIBLE = 12`, `ROW_PITCH = 26`,
`TRACK_Y`/`TRACK_H`/`PANEL_H`) are called out in the source as having to **match the `forge.gfx` author
values exactly** — this library doesn't re-author the movie, it drives the identical one MissionForge does.

### One menu at a time, by design

Like `MrxMultiPageMenu` (see [its own module page](../resident/mrxmultipagemenu)), only one ForgeMenu can
be visually open at once — `openMenu` explicitly closes whatever else is open first:

```lua
if FM._openId and FM._openId ~= menu.id then
    local other = FM._rt[FM._openId]
    if other and other.active then closeMenu(other) end
end
```

Unlike `MrxMultiPageMenu`, this isn't a side effect of shared module state you have to reason about — it's
one explicit guard, because every ForgeMenu-based menu shares the same one on-screen slot (there's only one
`forge.gfx` widget instance in play). Multiple *menu trees* can coexist fine (each gets its own runtime
table keyed by `id`); what can't coexist is two of them being visibly open at the same instant.

### The generation counter, reused from ForgeCam's own lesson

`rt.gen` is incremented every time a menu opens, and the heartbeat loop checks it on every tick
(`if not rt.active or rt.gen ~= gen then return end`) before rescheduling itself. This is the same
"kill the old loop, don't let two ever run at once" pattern the freecam/ForgeCam lineage already had to
solve for its own re-arming timers — closing a menu (or opening a different one, which force-closes this
one) invalidates the generation, and the next tick of the *old* heartbeat sees the mismatch and simply
doesn't reschedule itself again, instead of piling up a second heartbeat alongside a new one.

### A real, specific bug already fixed: `WARMUP`

```lua
local WARMUP = 8   -- force a re-render for the first N ticks after opening (defeats the async
                   -- SetSwfFile load dropping the very first render)
```

This is the one line in the file that reads like a documented war story rather than defensive-by-default
coding: `SetSwfFile` loading a Scaleform movie is asynchronous, so a render issued immediately after
`buildWidget` can be dropped on the floor if the movie hasn't actually finished loading yet — the menu
would open with a briefly blank or stale first frame. The fix is a deliberately crude one: keep
re-rendering unconditionally for the first 8 ticks (0.4s at the 0.05s tick rate) after every open, so
whichever tick actually lands after the movie's ready gets through. Cheap, doesn't need to know exactly
when the load finishes, and self-corrects to normal (only-render-on-change) behavior after the window
closes.

## Recipes

**A spawn menu:**

```lua
local menu = ForgeMenu.new("SPAWNER", { key = "F11" })
menu:category("Vehicles", function(c)
    c:entry("Tank", function(ctx) ctx:spawn("M1A2 (Full)", 8) end)
    c:entry("Heli", function(ctx) ctx:spawn("AH1Z (Full)", 12) end)
end)
menu:toggle()
```

**A cheat menu:**

```lua
local menu = ForgeMenu.new("CHEATS", { key = "F11" })
menu:entry("Heal", function(ctx) pcall(Object.SetHealth, ctx.char, 100) end)
menu:entry("Kill Nearby", function(ctx) --[[ your own logic ]] end)
menu:toggle()
```

## Gotchas

- **The world stays unpaused** — see [above](#why-the-world-doesn-t-pause). Pick a toggle key that isn't one
  of your navigation keys (arrows/Enter/Backspace by default), since those keep doing their normal in-game
  thing while the menu is up.
- **Give distinct menus distinct titles**, or pass an explicit `{ id = "..." }` — the `id` is what keys a
  menu's saved runtime state (`FM._rt[id]`) across separate `ForgeMenu.new` calls in the same session; two
  menus that happen to share a title/id would share state.
- **Only one menu is visibly open at a time**, by design — see [above](#one-menu-at-a-time-by-design).
- **Entry actions run inside a `pcall`.** A bug in your function surfaces as `ERROR (see log)` on the hint
  line plus a `Loader.Printf` line, rather than breaking the menu outright — check
  `lua_loader_printf.log` first if an entry seems to silently do nothing.
- **Depends only on `forge.gfx` already being in the WAD** (shared with ForgeCam/MissionForge) — no
  `ContractFramework` or any other dependency.

## The current scripts

**`ForgeMenu.lua`** (the library — `scripts/OnLoad/`, needs a low `lua_loader.ini` number so it loads
before any menu that uses it, e.g. `ForgeMenu.lua=5`):

```lua
-- =====================================================================
-- ForgeMenu  -  a tiny, beginner-friendly library for building your OWN in-game
--              pop-up menus on top of the shipped forge.gfx movie.
--
-- WHY THIS EXISTS
--   MissionForge / ForgeCam drive a nice scrolling menu movie ("forge.gfx"). This file lifts ALL of
--   that plumbing - the Flash widget, the breadcrumb + scrollbar + panel animation, the keyboard
--   heartbeat, the navigation stack - out into a library so you can make a menu in ~10 lines and
--   NEVER touch any of it. You declare categories + entries; an entry runs a plain Lua function.
--
-- DEPENDENCIES: none. This does not require ContractFramework or anything else - just the forge.gfx
--   movie, which is already injected in the wad (shared with ForgeCam / MissionForge).
-- =====================================================================

import("MrxGuiBase")
import("MrxGuiManager")

_G.ForgeMenu = _G.ForgeMenu or {}
local FM = _G.ForgeMenu
FM._rt = FM._rt or {}     -- persistent runtime state, one table per menu id (survives the OnKey re-run)

-- ---------------------------------------------------------------------
-- Layout constants - these MUST match the forge.gfx author values (same as ForgeCam / MissionForge).
-- ---------------------------------------------------------------------
local VISIBLE   = 12       -- rows the movie shows at once
local ROW_PITCH = 26
local TRACK_Y   = 88
local TRACK_H   = 316
local PANEL_H   = 324
local LOC_X, LOC_Y, LOC_W, LOC_H = 40, 80, 380, 420

local TICK      = 0.05     -- heartbeat interval (s)
local HINT_HOLD = 3.0      -- how long a ctx:hint message stays before the hint reverts
local WARMUP    = 8        -- force a re-render for the first N ticks after opening (defeats the async
                           -- SetSwfFile load dropping the very first render)

-- Default navigation keys (Windows VK codes). Override per-menu via ForgeMenu.new(title,{keys={...}}).
local DEFAULT_KEYS = { up = 0x26, down = 0x28, open = 0x27, enter = 0x0D, back = 0x25, back2 = 0x08 }

-- Forward declarations (so the functions below can reference each other in any order).
local render, move, back, activate, dispatchKey, tick, startTick, closeMenu, openMenu

-- ---------------------------------------------------------------------
-- Small helpers
-- ---------------------------------------------------------------------
local function clamp(v, lo, hi) if v < lo then return lo elseif v > hi then return hi else return v end end

-- Talk to the movie. Every visible change goes through one of the forge.gfx callbacks.
local function callGfx(rt, fn, args)
    if rt.w then pcall(function() rt.w:CallActionScriptCallback(fn, args or {}) end) end
end

-- Where is the player standing / facing right now? (used to fill ctx and for ctx:spawn)
local function pose()
    local char   = Player.GetLocalCharacter()
    local player = Player.GetLocalPlayer()
    if not char then return nil, nil, nil, 0, nil, player end
    local ok, px, py, pz = pcall(Object.GetPosition, char)
    if not ok or not px then return nil, nil, nil, 0, char, player end
    local yaw = 0
    local oky, yv = pcall(Object.GetYaw, char); if oky and yv then yaw = yv end
    return px, py, pz, yaw, char, player
end

-- A label may be a plain string OR a function returning one (for live ON/OFF text).
local function resolveLabel(node)
    local l = node.label
    if type(l) == "function" then local ok, v = pcall(l); l = ok and v or "?" end
    return tostring(l or "?")
end
local function rowText(node)
    local l = resolveLabel(node)
    if node.children then return l .. "  >" end   -- categories get a chevron
    return l
end

-- Build the forge.gfx widget once and keep it (toggled with SetVisible), just like MissionForge.
local function buildWidget(rt)
    if rt.w then return end
    local player = Player.GetLocalPlayer()
    local w = MrxGuiBase.FlashWidget:new()
    pcall(function() w:SetOwner(player) end)
    w:SetLocation(LOC_X, LOC_Y, LOC_W, LOC_H)
    w:SetSwfFile("forge.gfx", nil, nil)
    MrxGuiBase.AddWidget(w)
    pcall(function() w:SetVisible(true) end)
    pcall(function() MrxGuiManager.AddWidgetToHud(player, w) end)
    rt.w = w
end

-- Flash a transient message on the hint line (reverts after HINT_HOLD seconds).
local function showHint(rt, msg)
    rt.hintMsg    = tostring(msg)
    rt.hintExpiry = (rt.now or 0) + HINT_HOLD
    render(rt)
end

-- The context object handed to every entry's action function.
local function makeCtx(rt)
    local px, py, pz, yaw, char, player = pose()
    local ctx = { x = px, y = py, z = pz, yaw = yaw or 0, char = char, player = player }
    function ctx:hint(msg)  showHint(rt, msg) end
    function ctx:print(msg) Loader.Printf("ForgeMenu: " .. tostring(msg)) end
    function ctx:close()    closeMenu(rt) end
    -- Spawn `template` at your feet, or `dist` metres in front of you. Sets facing to yours. Returns guid.
    function ctx:spawn(template, dist)
        if not px then self:hint("NO PLAYER POSITION"); return nil end
        local sx, sz = px, pz
        if dist and dist ~= 0 then
            local yr = math.rad(yaw or 0)
            sx = px - math.sin(yr) * dist     -- "forward" in the game's yaw convention (matches MissionForge)
            sz = pz + math.cos(yr) * dist
        end
        local ok, u = pcall(Pg.Spawn, template, sx, py, sz)
        if ok and u then pcall(Object.SetYaw, u, yaw or 0); return u end
        self:hint("SPAWN FAILED: " .. tostring(template))
        Loader.Printf("ForgeMenu: spawn failed '" .. tostring(template) .. "'")
        return nil
    end
    return ctx
end

-- ---------------------------------------------------------------------
-- Rendering  (draw the current menu level into the movie - generic version of MissionForge.refresh)
-- ---------------------------------------------------------------------
render = function(rt, instant)
    if not rt.stack then return end
    local lv   = rt.stack[#rt.stack]
    local list = lv.node.children
    local n    = #list
    if lv.sel > n - 1 then lv.sel = n - 1 end
    if lv.sel < 0 then lv.sel = 0 end
    if lv.off > lv.sel then lv.off = lv.sel end
    if lv.sel > lv.off + VISIBLE - 1 then lv.off = lv.sel - VISIBLE + 1 end
    if lv.off < 0 then lv.off = 0 end

    for i = 0, VISIBLE - 1 do
        local it = list[lv.off + i + 1]
        callGfx(rt, "SetRow", { i, it and rowText(it) or "" })
    end

    -- breadcrumb: TITLE > category > subcategory ...
    local crumb = resolveLabel(rt.stack[1].node)
    for i = 2, #rt.stack do crumb = crumb .. " > " .. resolveLabel(rt.stack[i].node) end
    callGfx(rt, "SetCrumb", { crumb })

    -- hint line (transient message wins; otherwise a context-aware control hint).
    -- NB: O / L / K / J are the forge.gfx glyph tokens for up / down / right / left (same as MissionForge).
    local hint
    if rt.hintMsg and rt.now < rt.hintExpiry then
        hint = rt.hintMsg
    else
        hint = "O/L MOVE"
        local it = list[lv.sel + 1]
        if it then
            if it.children then hint = hint .. "   K OPEN" else hint = hint .. "   K RUN" end
        end
        if #rt.stack > 1 then hint = hint .. "   J BACK" end
        if rt.closeKey then hint = hint .. "   " .. tostring(rt.closeKey) .. " CLOSE" end
    end
    callGfx(rt, "SetHint", { hint })

    if n == 0 then callGfx(rt, "SetSelected", { -1 }) else callGfx(rt, "SetSelected", { lv.sel - lv.off }) end

    if n > VISIBLE then
        local th = TRACK_H * VISIBLE / n
        if th < 18 then th = 18 end
        local ty = TRACK_Y + (TRACK_H - th) * lv.off / (n - VISIBLE)
        callGfx(rt, "SetScroll", { math.floor(ty), math.floor(th) })
    else
        callGfx(rt, "SetScroll", { 0, 0 })
    end

    local shown = n
    if shown > VISIBLE then shown = VISIBLE end
    if shown < 1 then shown = 1 end
    rt.panelTgt = 100 * (shown * ROW_PITCH + 12) / PANEL_H
    if instant then rt.panelCur = rt.panelTgt; callGfx(rt, "SetPanel", { rt.panelCur }) end
end

-- ---------------------------------------------------------------------
-- Navigation
-- ---------------------------------------------------------------------
move = function(rt, d)
    local lv = rt.stack[#rt.stack]
    local n = #lv.node.children
    if n == 0 then return end
    local s = clamp(lv.sel + d, 0, n - 1)
    if s ~= lv.sel then lv.sel = s; render(rt) end
end

back = function(rt)
    if #rt.stack > 1 then rt.stack[#rt.stack] = nil; render(rt) end
end

activate = function(rt)
    local lv = rt.stack[#rt.stack]
    local it = lv.node.children[lv.sel + 1]
    if not it then return end
    if it.children then
        rt.stack[#rt.stack + 1] = { node = it, sel = 0, off = 0 }
        render(rt)
    elseif it.action then
        local ctx = makeCtx(rt)
        local ok, err = pcall(it.action, ctx)
        if not ok then
            Loader.Printf("ForgeMenu: '" .. resolveLabel(it) .. "' error -> " .. tostring(err))
            showHint(rt, "ERROR (see log)")
        end
        if rt.active then render(rt) end   -- refresh so dynamic ON/OFF labels update at once
    end
end

dispatchKey = function(rt, b)
    local k = rt.keys
    if     b == k.up   then move(rt, -1)
    elseif b == k.down then move(rt, 1)
    elseif b == k.open or b == k.enter then activate(rt)
    elseif b == k.back or b == k.back2 then back(rt)
    end
end

-- ---------------------------------------------------------------------
-- Heartbeat: drain keys, run warm-up renders, expire transient hints, ease the panel.
-- ---------------------------------------------------------------------
local function easePanel(rt)
    if rt.panelCur and rt.panelTgt then
        local d = rt.panelTgt - rt.panelCur
        if d > 0.5 or d < -0.5 then rt.panelCur = rt.panelCur + d * 0.35; callGfx(rt, "SetPanel", { rt.panelCur })
        elseif rt.panelCur ~= rt.panelTgt then rt.panelCur = rt.panelTgt; callGfx(rt, "SetPanel", { rt.panelCur }) end
    end
end

tick = function(rt, dt)
    rt.now = (rt.now or 0) + dt
    local ev = Loader.PopKeyEvents()
    if ev and ev ~= "" then
        for i = 1, #ev do dispatchKey(rt, string.byte(ev, i)) end
    end
    if rt.warmup and rt.warmup > 0 then rt.warmup = rt.warmup - 1; render(rt) end
    if rt.hintMsg and rt.now >= rt.hintExpiry then rt.hintMsg = nil; render(rt) end
    easePanel(rt)
end

startTick = function(rt, gen)
    local function loop()
        if not rt.active or rt.gen ~= gen then return end   -- generation guard: dies when toggled off
        local dt = TICK
        if rt.stamp then
            local e = Sys.TimeStampGetElapsed(rt.stamp)
            if e and e > 0 then dt = e end
            Sys.TimeStampMark(rt.stamp)
        end
        if dt > 0.25 then dt = 0.25 end
        local ok, err = pcall(tick, rt, dt)
        if not ok then Loader.Printf("ForgeMenu: tick error -> " .. tostring(err)) end
        Event.Create(Event.TimerRelative, { TICK }, loop)
    end
    Event.Create(Event.TimerRelative, { TICK }, loop)
end

-- ---------------------------------------------------------------------
-- Open / close lifecycle
-- ---------------------------------------------------------------------
closeMenu = function(rt)
    rt.active = false
    rt.gen = (rt.gen or 0) + 1          -- invalidate the running heartbeat
    if rt.w then pcall(function() rt.w:SetVisible(false) end) end
    if FM._openId == rt.id then FM._openId = nil end
    Loader.Printf("ForgeMenu: '" .. tostring(rt.id) .. "' closed")
end

openMenu = function(menu)
    local rt = menu._rt
    if not (Player.GetLocalPlayer() and Player.GetLocalCharacter()) then
        Loader.Printf("ForgeMenu: no local player yet - can't open '" .. tostring(menu.id) .. "'")
        return
    end
    -- only one ForgeMenu open at a time (they share the same on-screen slot)
    if FM._openId and FM._openId ~= menu.id then
        local other = FM._rt[FM._openId]
        if other and other.active then closeMenu(other) end
    end
    rt.active   = true
    rt.now      = 0
    rt.root     = menu.root                                    -- snapshot THIS run's tree + action closures
    rt.stack    = { { node = menu.root, sel = 0, off = 0 } }
    rt.keys     = menu.keys
    rt.closeKey = menu.closeKey
    rt.panelCur, rt.panelTgt = 100, 100
    rt.hintMsg  = nil
    rt.warmup   = WARMUP
    pcall(Loader.ClearKeyEvents)                               -- swallow the toggle keypress itself
    buildWidget(rt)
    pcall(function() rt.w:SetVisible(true) end)
    render(rt, true)
    rt.gen   = (rt.gen or 0) + 1
    rt.stamp = Sys.RealTimeStamp()
    startTick(rt, rt.gen)
    FM._openId = menu.id
    Loader.Printf("ForgeMenu: '" .. tostring(menu.id) .. "' open")
end

-- ---------------------------------------------------------------------
-- Builder  (what :entry / :category add to). A category returns another Builder you keep building on.
-- ---------------------------------------------------------------------
local Builder = {}
Builder.__index = Builder

function Builder:entry(label, action)
    if type(action) ~= "function" then
        Loader.Printf("ForgeMenu: entry '" .. tostring(label) .. "' needs a function as its 2nd argument")
        action = function() end
    end
    self._children[#self._children + 1] = { label = label, action = action }
    return self
end

function Builder:category(label, buildFn)
    local node = { label = label, children = {} }
    self._children[#self._children + 1] = node
    local child = setmetatable({ _children = node.children }, Builder)
    if type(buildFn) == "function" then buildFn(child) end   -- optional: build children inline
    return child                                             -- ...or keep the returned object and add to it later
end

-- ---------------------------------------------------------------------
-- Menu  (a root Builder + open/close lifecycle). Returned by ForgeMenu.new.
-- ---------------------------------------------------------------------
local Menu = setmetatable({}, { __index = Builder })        -- Menu also has :entry / :category (via Builder)
Menu.__index = Menu

function Menu:toggle() if self._rt.active then closeMenu(self._rt) else openMenu(self) end return self end
function Menu:open()   if not self._rt.active then openMenu(self) end return self end
function Menu:close()  if self._rt.active then closeMenu(self._rt) end return self end
function Menu:isOpen() return self._rt.active == true end

-- ForgeMenu.new(title [, opts])
--   title : string shown as the breadcrumb root.
--   opts  : optional table -  { id = "unique-id",   -- defaults to the title; give distinct menus distinct ids
--                               key = "F8",          -- your toggle key, shown in the hint (display only)
--                               keys = { up=.., down=.., open=.., enter=.., back=.., back2=.. } }  -- VK overrides
--           (passing a string instead of a table is treated as the id.)
function FM.new(title, opts)
    if type(opts) == "string" then opts = { id = opts } end
    opts = opts or {}
    local id   = opts.id or title or "menu"
    local root = { label = title or "MENU", children = {} }
    FM._rt[id] = FM._rt[id] or { id = id }
    local menu = setmetatable({
        root      = root,
        _children = root.children,      -- so Builder:entry / :category add to the root
        id        = id,
        _rt       = FM._rt[id],
        keys      = opts.keys or DEFAULT_KEYS,
        closeKey  = opts.key,
    }, Menu)
    return menu
end

-- This OnLoad file re-runs on every world (re)load, by which point any FlashWidget from a previous
-- world has been torn down. Forget stale widget handles and force every menu closed, so the next toggle
-- rebuilds cleanly and no orphaned heartbeat survives a load.
for _, rt in pairs(FM._rt) do
    rt.active = false
    rt.gen = (rt.gen or 0) + 1
    rt.w = nil
end
FM._openId = nil

Loader.Printf("ForgeMenu: library ready (ForgeMenu.new / :category / :entry / :toggle)")
```

**`ExampleMenu.lua`** (the copy-me demo — `scripts/OnKey/`, bound to F11):

```lua
local KEYVAL = "f11"   -- must be in the first 10 lines (your toggle key; also add "ExampleMenu.lua=f11" under [OnKey])

if not _G.ForgeMenu then
    Loader.Printf("ExampleMenu: ForgeMenu library not loaded - put ForgeMenu.lua in scripts/OnLoad/ and add it to [OnLoad] in lua_loader.ini")
    return
end

local menu = ForgeMenu.new("EXAMPLE MENU", { key = KEYVAL:upper() })

-- --- top-level actions -------------------------------------------------
menu:entry("Heal Me", function(ctx)
    if ctx.char then pcall(Object.SetHealth, ctx.char, 100) end
    ctx:hint("HEALED")
end)

menu:entry("Face North", function(ctx)
    if ctx.char then pcall(Object.SetYaw, ctx.char, 0) end
    ctx:hint("FACING NORTH")
end)

-- --- a category of spawn buttons --------------------------------------
menu:category("Spawn Vehicles", function(c)
    c:entry("Diplomat Tank",   function(ctx) ctx:spawn("M1A2 (Full)", 8);  ctx:hint("TANK SPAWNED") end)
    c:entry("Ambassador Heli", function(ctx) ctx:spawn("AH1Z (Full)", 12); ctx:hint("HELI SPAWNED") end)
    c:entry("Softtop HMMWV",   function(ctx) ctx:spawn("HMMWV (Softtop) (Full)", 8); ctx:hint("HMMWV SPAWNED") end)
end)

-- --- a category with a NESTED subcategory ------------------------------
menu:category("Spawn Enemies", function(c)
    c:category("Guerilla", function(g)
        g:entry("Soldier",     function(ctx) ctx:spawn("Guerilla Soldier", 6);          ctx:hint("PLACED") end)
        g:entry("Heavy (RPG)", function(ctx) ctx:spawn("Guerilla Heavy (RPG)", 6);       ctx:hint("PLACED") end)
        g:entry("Boss",        function(ctx) ctx:spawn("Guerilla Boss", 6);              ctx:hint("PLACED") end)
    end)
    c:category("Chinese", function(g)
        g:entry("Soldier",     function(ctx) ctx:spawn("Chinese Soldier", 6);            ctx:hint("PLACED") end)
        g:entry("Sniper",      function(ctx) ctx:spawn("Chinese Sniper", 6);             ctx:hint("PLACED") end)
    end)
end)

-- --- a live ON/OFF toggle (label is a function, so it redraws each time) -----
_G.ExampleMenuState = _G.ExampleMenuState or {}   -- keep the flag in _G so it survives the OnKey re-run
local S = _G.ExampleMenuState
menu:entry(function() return S.god and "God Mode: ON" or "God Mode: OFF" end, function(ctx)
    S.god = not S.god
    if ctx.char then pcall(Object.SetInvincible, ctx.char, S.god and true or false, "ExampleMenu") end
    ctx:hint(S.god and "INVINCIBLE" or "MORTAL AGAIN")
end)

-- --- close button ------------------------------------------------------
menu:entry("Close Menu", function(ctx) ctx:close() end)

-- Flip the menu open/closed. (This file re-runs every time you press F8, so this line does the toggle.)
menu:toggle()
```

## General lessons

1. **A rendering pattern extracted from one specific tool becomes a library by parameterizing over the one
   thing that was hardcoded.** MissionForge's `refresh` only ever had to draw one catalog tree; ForgeMenu is
   that same function taught to walk *any* tree, plus a builder API for constructing one declaratively.
   Nothing about the Scaleform side changed at all.
2. **Not every input problem needs the PDA-pause trick.** The freecam lineage needed it because continuous
   analog input has no other Lua touchpoint. A menu's input — discrete moves and selections — was already
   fully served by `Loader.PopKeyEvents`, so ForgeMenu simply never pays the "world pauses" cost the tools
   built on the PDA hijack all inherit.
3. **A generation counter is a reusable answer to "how do I safely kill a self-rescheduling timer."**
   Same shape here as in the freecam/ForgeCam lineage: bump a counter on stop, have the loop check it before
   rescheduling itself, and a stale loop quietly stops instead of piling up alongside a new one.
4. **A single crude constant can be the right fix for an async-load race.** `WARMUP`'s "just re-render
   unconditionally for the first few ticks" doesn't need to know exactly when `SetSwfFile` finishes loading
   — it just needs to keep trying long enough that one of those ticks lands after it does.

## See also

- [Building Nested Menus with MrxMultiPageMenu](nested-menus) — the harder, DIY way to nest menus using the
  *native* dialog-box system instead of `forge.gfx`; still the right tool if you specifically want the
  native look-and-feel rather than the Scaleform one.
- [Building a Real Freecam](freecam) — the PDA-hijack trick and the "why not just poll" reasoning ForgeMenu
  deliberately avoids needing.
- [Building ForgeCam](forgecam) / [MissionForge](mission-forge) — where `forge.gfx` and the render/heartbeat
  pattern this library generalizes originally came from.
- [Your First Menu](../first-menu) — the `_G`-guarded persistent-state idiom used for live ON/OFF labels.
- [lua-bridge API: Loader](../lua-bridge-api/loader) — `PopKeyEvents`, the input primitive this whole
  library is built on.
- **[UI Kit](../uilib/)** — this exact input/heartbeat/warm-up engine, generalized further into a full
  nine-widget toolkit (lists, panels, progress bars, toasts, modal dialogs, a chat log, a two-pane board) —
  reach for it over ForgeMenu directly if you need more than just a menu.
