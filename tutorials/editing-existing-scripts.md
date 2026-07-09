---
title: "11. Editing an Existing Script"
parent: Tutorials
nav_order: 11
---

# Tutorial 11: Editing an Existing Script

> Built around `CommonSpawnMenu.lua`, a real, substantial script already **confirmed working by live
> testing** on [Sample Scripts: OnKey](../sample-scripts-onkey) — nothing new is introduced here; this
> page is entirely about finding your way around code you didn't write.

Every tutorial so far has you writing a small script from scratch, alone, understanding every line of it.
Real modding is usually the opposite: you find something that already works — someone else's script, or a
sample from this wiki — and you change *one thing* about it without needing to understand *everything*
about it. That's a different skill, and it's the one this last tutorial is about.

## Get the script

If you don't already have it, grab **`CommonSpawnMenu.lua`** from
[Sample Scripts: OnKey](../sample-scripts-onkey) and drop it into `scripts/OnKey/`. Load into a level and
press **F5** — a menu titled "Common Spawn" opens, listing a handful of vehicles plus "Custom Name..." and
"Cancel". Picking one spawns it right in front of you.

This script is genuinely long — free-text keyboard input, a scrolling on-screen console, polling loops —
far more than anything you've written in this ladder. **You don't need to understand any of that.** The
one thing you're looking for is much smaller.

## Find the part that's actually data

Open the file and search for `tSpawnMenuOptions` (use your editor's find/Ctrl+F — don't read top to
bottom). You'll land on this:

```lua
local tSpawnMenuOptions = {
  {label = "Veyron (Sports Car)", action = "spawn", template = "Veyron"},
  {label = "ZTZ98 (Tank)", action = "spawn", template = "ZTZ98"},
  {label = "UH1 Transport (Helicopter)", action = "spawn", template = "UH1 Transport (PMC)"},
  {label = "Ambulance", action = "spawn", template = "Ambulance"},
  {label = "El Grande (Truck)", action = "spawn", template = "El Grande"},
  {label = "M35 Cargo Truck", action = "spawn", template = "M35 (Cargo) (VZ)"},
  {label = "Grenade Explosion", action = "spawn", template = "Explosion (Grenade)"},
  {label = "Custom Name...", action = "custom"},
  {label = "Cancel", action = "cancel"},
}
```

This is exactly what it looks like: a plain list, one entry per menu row. `label` is what you see in the
menu; `template` is the exact string handed to `Pg.Spawn`. Everything else in this 600-line file —
building the menu, reading your selection, the whole free-text console — is **logic** that *uses* this
list. You don't need to touch, or understand, any of that to change what's *in* the list.

Most scripts worth editing are shaped like this: a clearly delimited block of **data** (a table like this
one, usually near the top and usually commented) and **logic** below it that acts on that data. Finding
the data half and leaving the logic half alone is, by far, the safest kind of edit there is.

## Make one small, additive change

Copy the exact shape of an existing line, change the two strings, and add it — **above** `"Custom
Name..."` and `"Cancel"`, so it lands with the other spawn options instead of after them:

```lua
local tSpawnMenuOptions = {
  {label = "Veyron (Sports Car)", action = "spawn", template = "Veyron"},
  {label = "ZTZ98 (Tank)", action = "spawn", template = "ZTZ98"},
  {label = "UH1 Transport (Helicopter)", action = "spawn", template = "UH1 Transport (PMC)"},
  {label = "Ambulance", action = "spawn", template = "Ambulance"},
  {label = "El Grande (Truck)", action = "spawn", template = "El Grande"},
  {label = "M35 Cargo Truck", action = "spawn", template = "M35 (Cargo) (VZ)"},
  {label = "Grenade Explosion", action = "spawn", template = "Explosion (Grenade)"},
  {label = "My Own Entry", action = "spawn", template = "PutARealTemplateHere"},
  {label = "Custom Name...", action = "custom"},
  {label = "Cancel", action = "cancel"},
}
```

For a real `template` value, see [Spawn Reference: Drivable Vehicles](../spawn-reference/drivable-vehicles)
— every name there is confirmed spawnable. Save the file, press **F5**, and confirm "My Own Entry" shows
up in the menu, in the position you put it. Pick it.

> **[Image placeholder — `../img/editingscriptmenu.png`]** Screenshot of the in-game "Common Spawn" menu
> showing the new "My Own Entry" option listed among the original entries (Veyron, ZTZ98, UH1 Transport,
> etc.), positioned above "Custom Name..." and "Cancel".

## Reading what happened, using tools you already have

The menu itself tells you whether the spawn worked — a "Spawned: ..." or "Failed: ..." toast appears
either way (that's [Tutorial 2](hello-screen)'s on-screen-message idea, already built into this script).
If it says "Failed," open `lua_loader_printf.log` (from [Tutorial 1](hello-log)) — nothing generates
there for this specific script's `pcall` failures beyond the toast, so a "Failed" toast with no matching
menu-side clue almost always means the `template` string is wrong: a typo, or a name that isn't actually
spawnable this way.

Look at how the spawn itself happens, a bit further down in the same file:

```lua
function DoSpawn(sTemplateName)
  local uChar = Player.GetLocalCharacter()
  local x, y, z = Object.GetPosition(uChar)

  local bOk, uSpawned = pcall(Pg.Spawn, sTemplateName, x, y + nSpawnHeightOffset, z)
  return bOk and uSpawned
end
```

Every piece of this should look familiar: `Player.GetLocalCharacter()` and `Object.GetPosition(...)` are
[Tutorial 3](reading-state); wrapping a risky call in `pcall` and checking the boolean is
[Tutorial 6](pcall-safety). You've already learned everything this function does — you just hadn't yet
seen it inside a script someone else wrote for a real purpose.

## If something breaks

Table syntax is picky — a missing comma between two entries, or quotes that don't match, breaks the
*entire file*, not just your new line. If pressing F5 does nothing at all — not even the original menu you
had working a minute ago — that's the most common cause. Compare your new line, character by character,
against the ones directly above and below it. If you get stuck, delete your line and confirm the original
menu comes back; that isolates the problem to the line you added rather than anything else.

## Try it yourself

- Add a second entry, this time picking a template from
  [Spawn Reference: All Vehicles](../spawn-reference/all-vehicles) instead.
- Deliberately break it — delete a comma between two entries — and see what pressing F5 does with the
  syntax broken. Then fix it and confirm the menu comes back.
- Deliberately misspell a `template` string on purpose and confirm you get a "Failed: ..." toast instead of
  a working spawn, without anything else in the menu breaking.
- Try removing one of the *original* entries entirely (not just adding one) — confirm the menu shrinks by
  exactly one row and every other entry still works.

## Where this comes from

- [Sample Scripts: OnKey — CommonSpawnMenu.lua](../sample-scripts-onkey) — the full script, confirmed
  working end to end, including the free-text console this tutorial never touches.
- [Spawn Reference: Drivable Vehicles](../spawn-reference/drivable-vehicles) /
  [All Vehicles](../spawn-reference/all-vehicles) — confirmed template names to add.

## You've reached the end of the ladder

Between these eleven pages you've now used every basic building block this wiki's other sections assume
you already have: logging, on-screen feedback, reading state, the `OnLoad`/`OnKey` split, `import()`,
`pcall`, `_G` state, timers, event hooks, looking things up by name, and — this last one — safely changing
code you didn't write yourself. From here:

- [Your First Menu](../first-menu) combines several of these into one real, complete script.
- [Recipes](../recipes) is the grab-bag of small, ready-to-use pieces — you now know where each of them
  would actually go.
- [Sample Scripts](../sample-scripts) has several more complete scripts shaped exactly like this
  tutorial's — worth a look now that "a big file" isn't intimidating on its own.
- [Resident Modules](../resident/) is the full reference for everything you can call once "the basics"
  aren't the hard part anymore.
- [Deep Dives](../deep-dives/) is where this wiki's harder, multi-day investigations live, wrong turns
  included — worth reading once you want to build something bigger than a script.
