---
title: Canonical code patterns (curated)
---

Copy the shape, not necessarily the values. Every snippet here follows the rules above
(Lua 5.1, `Loader.Printf`, `pcall` on fallible calls, file-scoped `import`).

## Minimal OnKey script

```lua
local KEYVAL = "insert"  -- MUST be in the first 10 lines; also needs an
                         -- `myscript.lua=insert` line in lua_loader.ini [OnKey]
Loader.Printf("hello from OnKey")
```

## State that survives re-execution

Each keypress re-runs the file from scratch, so plain locals reset. `_G` is the only thing
that persists within a session.

```lua
_G.MyMod = _G.MyMod or { bOn = false, nCount = 0 }
local S = _G.MyMod

S.bOn = not S.bOn
Loader.Printf("toggled -> " .. tostring(S.bOn))
```

## Safe engine call

One bad `uGuid` should never kill the rest of the script.

```lua
local uChar = Player.GetLocalCharacter()
local bOk, sErr = pcall(Object.SetInvincible, uChar, true, "mymod")
if not bOk then
  Loader.Printf("SetInvincible failed: " .. tostring(sErr))
end
```

## Where am I / put something in front of me

```lua
local uChar = Player.GetLocalCharacter()
local x, y, z = Object.GetPosition(uChar)
Loader.Printf(string.format("pos %.1f %.1f %.1f", x, y, z))

local uGuid = Pg.Spawn("Veyron", x + 5, y, z)   -- exact template string required
```

## Repeating timer

`Event.TimerRelative` fires once -- re-arm as the first line of the callback.

```lua
local function tick()
  Event.Create(Event.TimerRelative, {0.05}, tick)   -- re-arm FIRST
  -- per-tick work here
end
tick()
```

## Edge-triggered key polling

A raw poll fires ~20x/sec, so without edge-triggering one press registers many times.

```lua
_G.KeyWatch = _G.KeyWatch or { bPrevDown = false }
local S = _G.KeyWatch

local function poll()
  Event.Create(Event.TimerRelative, {0.05}, poll)
  local bDown = Loader.IsKeyDown(0x28)          -- VK_DOWN, a numeric VK code
  if bDown and not S.bPrevDown then
    Loader.Printf("down pressed")               -- fires once per physical press
  end
  S.bPrevDown = bDown
end
poll()
```

## Persistence across game restarts

Flat namespace shared by every script -- prefix your keys.

```lua
local nProgress = Loader.LoadVar("MyMod_progress") or 0
Loader.SaveVar("MyMod_progress", nProgress + 1)
```

## Economy with a HUD refresh

```lua
import("MrxPmc")            -- file-scoped: every file needs its own import
MrxPmc.AddCashQty(100000)   -- updates the HUD; Player.AddCash does not
```

## A paginating menu (native)

```lua
import("MrxMultiPageMenu")
MrxMultiPageMenu.Reset()
MrxMultiPageMenu.AddOption("Say hello", function() Loader.Printf("hi!") end)
MrxMultiPageMenu.AddOption("Close", nil, nil, true, true)  -- nil callback is only
                                                           -- safe on the cancel button
MrxMultiPageMenu.Display("Test Menu:")
```

## A menu (Ess -- preferred for new work)

```lua
if not _G.Ess then Loader.Printf("load Ess first") return end

local menu = Ess.UI.Menu{ title = "MY MENU", key = "F8" }
menu:entry("Do a thing", function(ctx) ctx:hint("done") end)
menu:category("Group", function(c)
  c:entry("Nested", function(ctx) ctx:hint("nested") end)
end)
menu:toggle()   -- last line of the OnKey file
```

## Overriding existing game logic

Resolves at call time, not definition time -- this changes behaviour for every future
call from anywhere, including from inside the original module's own functions.

```lua
import("SomeModule")
SomeModule.SomeFunction = function(...)
  -- replacement body
end
```

Ess offers a guarded version of this (`Ess.Override`) that avoids the tail-call crash;
prefer it when Ess is loaded.
