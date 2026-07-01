---
title: Recipes
nav_order: 4
layout: verified_page
verified: false
---

# Recipes

Small, copy-pasteable snippets for common tasks. Run any of these from `lua_console.py` first to see
them work, then move them into an `OnLoad`/`OnKey` script once you know what you want. If you haven't
read [Your First Mod](first-mod) yet, that's where `OnLoad`/`OnKey`/`KEYVAL` are explained — this page
assumes you already know where a snippet like this would go.

Every snippet below is a real call pattern pulled from the game's own scripts, not guessed — but "real
call pattern" isn't the same as "tested by a human in-game." Check the banner at the top of this page.

## Print debug info

The simplest possible thing — confirms your script is running and lets you inspect a value:

```lua
Loader.Printf("[mymod] cash = " .. Player.GetCash())
```

## Read / give cash

```lua
local nCurrent = MrxPmc.GetCashQty()
MrxPmc.AddCashQty(10000)              -- relative: add 10,000
-- MrxPmc.AddCashQty(nCurrent * -1)   -- zero it out, if you ever need to
```

## Read / give fuel

Fuel has both a current quantity and a capacity — raising the quantity past the capacity does nothing
until you raise the capacity too:

```lua
local nFuel = MrxPmc.GetFuelQty()
local nCap  = MrxPmc.GetFuelCapacity()
MrxPmc.SetFuelCapacity(9999, true)    -- raise the cap first
MrxPmc.AddFuelQty(5000)               -- then add fuel
```

## Toggle infinite ammo

```lua
Object.SetInfiniteAmmo(Player.GetPrimaryCharacter(), true)   -- on
-- Object.SetInfiniteAmmo(Player.GetPrimaryCharacter(), false) -- off
```

If you're in co-op and want to affect the second player too, there's a matching
`Player.GetSecondaryCharacter()`.

## Get your current position

Useful for debugging, or as a building block for anything that needs to know where the player is:

```lua
local x, y, z = Object.GetPosition(Player.GetLocalCharacter())
Loader.Printf(string.format("[mymod] pos = %.1f, %.1f, %.1f", x, y, z))
```

## Put a marker/blip on an object

This is the same pattern the game's own radar-objective modules (`crate`, `blippable`) use to put a
minimap/off-screen blip on a world object:

```lua
Marker.AddBlip(uGuid, "temp_radar_icon_airplane", 48, 255, 255, 255, 255, 0.5, 16, 20)
```

`uGuid` is the target object's handle and `"temp_radar_icon_airplane"` is a texture name (swap for
whatever icon you want, assuming it exists as a loaded asset). The trailing numeric arguments are copied
verbatim from working game code (size/color/alpha/scale-ish values) — their exact individual meaning
hasn't been independently confirmed argument-by-argument, so treat this as "known to work with these
values" rather than a fully documented signature. If you need a different visual result, adjust one
argument at a time and observe.

## React to an event instead of polling

The engine event pattern used throughout `resident/` — fire a callback once, later, instead of checking
a condition every frame:

```lua
Event.Create(Event.TimerRelative, {2}, function()
  Loader.Printf("[mymod] two seconds later")
end, {})
```

For a real per-object hook (the pattern every world-object script uses to defer setup until the object
is actually live), see the `OnActivate` / `Awake` explanation on the
[Resident Modules](resident/) landing page.

## Something not here?

If you worked out a useful snippet that isn't listed, it's worth adding — this page is meant to grow.
