---
title: Snippets
parent: Recipes
nav_order: 1
layout: verified_page
verified: true
verified_note: every snippet live-tested (cash/fuel via MrxPmc pattern, infinite ammo, position, marker blip, timer event)
---

# Snippets

Small, copy-pasteable one- or few-liners for common tasks. Run any of these from `lua_console.py` first
to see them work, then move them into an `OnLoad`/`OnKey` script once you know what you want. If you
haven't read [Your First Mod](first-mod) yet, that's where `OnLoad`/`OnKey`/`KEYVAL` are explained — this
page assumes you already know where a snippet like this would go.

Looking for a complete, ready-to-drop-in script instead of a building block? See
[Sample Scripts](sample-scripts).

Every snippet below is a real call pattern pulled from the game's own scripts, not guessed — but "real
call pattern" isn't the same as "tested by a human in-game." Check the banner at the top of this page.
Headings below stay expanded/collapsed independently — click one to open it.

## Print debug info

<details class="script-entry" markdown="1">
<summary>One line to confirm your script is running and inspect a value.</summary>

The simplest possible thing — confirms your script is running and lets you inspect a value:

```lua
Loader.Printf("[mymod] cash = " .. Player.GetCash())
```

</details>

## Read / give cash

<details class="script-entry" markdown="1">
<summary>Read the player's cash, or add to it, via MrxPmc.</summary>

`MrxPmc` is a `resident/` module, not an engine namespace, so it isn't automatically visible from a
console chunk or `OnLoad`/`OnKey` script — `import()` it yourself first (confirmed by live testing: skip
this and you get `attempt to index global 'MrxPmc' (a nil value)`). See the
[Glossary](glossary#importname) if that's surprising.

```lua
import("MrxPmc")
local nCurrent = MrxPmc.GetCashQty()
MrxPmc.AddCashQty(10000)              -- relative: add 10,000
-- MrxPmc.AddCashQty(nCurrent * -1)   -- zero it out, if you ever need to
```

Confirmed by live testing: the lower-level `Player.SetCash(...)`/`Player.AddCash(...)` also genuinely
change the balance, but skip the HUD refresh `MrxPmc.AddCashQty` triggers — the on-screen number won't
visibly update even though the value changed. Use `MrxPmc.AddCashQty`/`AddFuelQty`, not the raw
`Player.*` setters, if you want what's displayed to actually update.

</details>

## Read / give fuel

<details class="script-entry" markdown="1">
<summary>Read the player's fuel, or add to it, raising the capacity first if needed.</summary>

Fuel has both a current quantity and a capacity — raising the quantity past the capacity does nothing
until you raise the capacity too. Same `import()` requirement as cash above:

```lua
import("MrxPmc")
local nFuel = MrxPmc.GetFuelQty()
local nCap  = MrxPmc.GetFuelCapacity()
MrxPmc.SetFuelCapacity(9999, true)    -- raise the cap first
MrxPmc.AddFuelQty(5000)               -- then add fuel
```

</details>

## Toggle infinite ammo

<details class="script-entry" markdown="1">
<summary>Turn infinite reserve ammo on or off for a character.</summary>

```lua
Object.SetInfiniteAmmo(Player.GetPrimaryCharacter(), true)   -- on
-- Object.SetInfiniteAmmo(Player.GetPrimaryCharacter(), false) -- off
```

**Confirmed working by live testing** — with one nuance: this doesn't mean "never reload." The magazine
you're currently firing still empties normally and still needs a reload; what's infinite is your reserve
ammo count, which stays maxed instead of depleting. Grenades behave the same way (infinite reserve, but
you still throw them one at a time). If you want the mag itself to never empty, this call alone isn't
enough — that'd need a different/additional call, not yet identified.

If you're in co-op and want to affect the second player too, there's a matching
`Player.GetSecondaryCharacter()`.

</details>

## Get your current position

<details class="script-entry" markdown="1">
<summary>Read the player's current world coordinates.</summary>

Useful for debugging, or as a building block for anything that needs to know where the player is:

```lua
local x, y, z = Object.GetPosition(Player.GetLocalCharacter())
Loader.Printf(string.format("[mymod] pos = %.1f, %.1f, %.1f", x, y, z))
```

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

`Object.GetPosition` returns **three separate values at once**, not one table/object bundling them
together — that's why the call site is `local x, y, z = Object.GetPosition(...)` instead of something
like `local pos = Object.GetPosition(...); pos.x`. This is completely ordinary in Lua (functions can
return as many values as they want, comma-separated) and you'll see it constantly throughout this wiki —
`Object.GetYaw`, `Vehicle.GetSeatParams`, `pcall` (see below) all do the same thing. If you only care
about the first value or two, it's fine to only capture that many: `local x, y = Object.GetPosition(...)`
silently drops `z` rather than erroring.

</details>

**Confirmed working by live testing** — returns real, sane coordinates matching the player's actual
in-world position.

</details>

## Put a marker/blip on an object

<details class="script-entry" markdown="1">
<summary>Add a minimap/radar blip to any object.</summary>

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

**Confirmed working by live testing** — tested with `uGuid = Player.GetLocalCharacter()` (blip on your
own character). The blip does render, but at ground level under the object — on a character, it can be
visually obscured by nearby geometry unless you jump or look from above. Don't assume "no icon visible"
means it failed; check the minimap itself (blips render there even when the in-world icon is hidden by
geometry) before concluding the call didn't work.

</details>

## React to an event instead of polling

<details class="script-entry" markdown="1">
<summary>Fire a callback once, later, instead of checking a condition every frame.</summary>

The engine event pattern used throughout `resident/` — fire a callback once, later, instead of checking
a condition every frame:

```lua
Event.Create(Event.TimerRelative, {2}, function()
  Loader.Printf("[mymod] two seconds later")
end, {})
```

**Confirmed working by live testing** — fires exactly once, at the correct delay. Tested at 2s, 5s, and
20s, all reliable.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

That `function() ... end` sitting *inside* the `Event.Create(...)` call, with no name of its own, is
called an **anonymous function** — a function defined right where it's used instead of with
`function Foo() ... end` somewhere else. `Event.Create` takes it as an argument and calls it later,
once the timer fires, exactly like `MrxMultiPageMenu.AddOption("Add cash", function(nCash) ... end, ...)`
does elsewhere in this wiki. This is an extremely common pattern in this codebase: "here's some code to
run later, when X happens" — the callback function *is* the "later."

You'll also see `local KEYVAL = "insert"` and `local nCurrent = ...` elsewhere on this page.
`local` limits where a name is visible — leave it off and the name becomes global (visible from
anywhere), which is almost never what you want for a throwaway variable inside one script. See
[Your First Mod](first-mod) and the [Resident Modules](resident/) landing page for more on this.

</details>

For a real per-object hook (the pattern every world-object script uses to defer setup until the object
is actually live), see the `OnActivate` / `Awake` explanation on the
[Resident Modules](resident/) landing page.

</details>

## Protect a risky call with pcall

<details class="script-entry" markdown="1">
<summary>Catch a runtime error instead of letting it silently stop the rest of your script.</summary>

You'll see almost every game-API call in this wiki's sample scripts (`DestroyerTool.lua`,
`MasterCheatMenu.lua`, `CommonSpawnMenu.lua`, and more) wrapped in `pcall`, especially anything touching a
`uGuid` that might not actually exist anymore (a despawned vehicle, a character who's since left):

```lua
local bSuccess, result = pcall(Object.SetInvincible, Player.GetLocalCharacter(), true, "mymod")
if not bSuccess then
  Loader.Printf("[mymod] SetInvincible failed: " .. tostring(result))
end
```

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

Normally, a runtime error (calling a function with the wrong arguments, indexing something that turned
out to be `nil`, etc.) stops the *entire* script right where it happened — nothing after that line in the
same run gets a chance to execute. `pcall(f, arg1, arg2, ...)` calls `f(arg1, arg2, ...)` for you, but
catches any error instead of letting it propagate, and always returns at least one value: a boolean,
`true` if the call finished without error. If that boolean is `true`, every other value `pcall` returns
after it is whatever `f` itself returned (following the [multiple-return-values](#get-your-current-position)
idea above). If it's `false`, there's exactly one more return value — the error message — and nothing
past that point inside `f` ran. That's why the pattern is always `local bOk, result = pcall(...)`, never
just `pcall(...)` on its own with the result thrown away: `bOk` is what tells you which case you're in.

This matters most in `OnKey`/`OnLoad` scripts specifically because one error can end that entire script's
run early — wrapping the risky part in `pcall` means a stale `uGuid` failing one call doesn't also skip
every *other* thing the rest of the script was about to do.

</details>

**A narrower, argument-free version — `pcall(f)`** — is also common when you don't need to pass anything
through, just guard against `f` itself not existing or throwing:

```lua
pcall(function()
  SomeOptionalThing.MightNotExist()
end)
```

</details>

## Dump any table's contents to the log

<details class="script-entry" markdown="1">
<summary>Print a table's full contents to the log for inspection.</summary>

Useful any time you want to know what's actually inside a data table (`tSupportData`, `_tFactions`,
whatever) instead of guessing from source — some tables (like `MrxSupportData.tSupportData`) start empty
in source and only get populated at runtime, so reading the file doesn't tell you the final shape.

Drop this as `scripts/OnBoot/dump_helper.lua` so `DumpTable` stays callable for the rest of the session:

```lua
function DumpTable(t, sName, nMaxDepth, nDepth, tSeen)
  nDepth = nDepth or 0
  nMaxDepth = nMaxDepth or 3
  tSeen = tSeen or {}
  local sIndent = string.rep("  ", nDepth)
  if type(t) ~= "table" then
    Loader.Printf(sIndent .. tostring(sName) .. " = " .. tostring(t) .. " (" .. type(t) .. ")")
    return
  end
  if tSeen[t] then
    Loader.Printf(sIndent .. tostring(sName) .. " = <already dumped, cyclic/shared reference>")
    return
  end
  tSeen[t] = true
  if nDepth > nMaxDepth then
    Loader.Printf(sIndent .. tostring(sName) .. " = <table, max depth reached>")
    return
  end
  Loader.Printf(sIndent .. tostring(sName) .. " = {")
  local tKeys = {}
  for k in pairs(t) do table.insert(tKeys, k) end
  table.sort(tKeys, function(a, b) return tostring(a) < tostring(b) end)
  for _, k in ipairs(tKeys) do
    local v = t[k]
    if type(v) == "table" then
      DumpTable(v, tostring(k), nMaxDepth, nDepth + 1, tSeen)
    elseif type(v) == "function" then
      Loader.Printf(sIndent .. "  " .. tostring(k) .. " = <function>")
    else
      Loader.Printf(sIndent .. "  " .. tostring(k) .. " = " .. tostring(v) .. " (" .. type(v) .. ")")
    end
  end
  Loader.Printf(sIndent .. "}")
end
```

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

This snippet uses both of Lua's two table-iteration loops on purpose, back to back, which is a good place
to see the difference between them:

- **`for k in pairs(t) do ... end`** (line with `table.insert(tKeys, k)`) visits **every** key in the
  table, in no particular/guaranteed order — string keys, number keys, whatever's actually there. That's
  exactly what you want here, since a data table like `MrxSupportData.tSupportData` is keyed by name
  (`"nuke"`, `"moab"`, ...), not by position.
- **`for _, k in ipairs(tKeys) do ... end`** only works on a plain numbered array (keys `1, 2, 3, ...`
  with no gaps) and visits them **in that exact order**, stopping at the first missing number. `tKeys` is
  built as exactly that kind of array (via `table.insert`), so `ipairs` is what gives this snippet
  alphabetically-sorted, repeatable output — using `pairs` a second time here would print the same
  entries, but in whatever arbitrary order the table happens to store them in internally, differently
  from one run to the next.

Mixing these up is one of the most common early Lua mistakes: `ipairs` over a table that isn't a plain
sequential array silently stops after the first gap instead of erroring, which can look like "half my
data disappeared" when really it never was a plain array to begin with.

</details>

Then, from the console:

```lua
import("MrxSupportData")
DumpTable(MrxSupportData.tSupportData, "MrxSupportData.tSupportData", 2)
```

**Confirmed working by live testing** — an early version of this is exactly how the
[support item catalog](resident/mrxsupportdata#support-item-catalog) was first explored. Fully recursive
dumps get verbose fast (one real table produced ~3000 log lines) — for building a clean reference table,
skip `DumpTable` and write a narrower one-line-per-entry loop instead, printing only the specific fields
you care about:

```lua
local tKeys = {}
for k in pairs(MrxSupportData.tSupportData) do table.insert(tKeys, k) end
table.sort(tKeys)
for _, k in ipairs(tKeys) do
  local d = MrxSupportData.tSupportData[k]
  Loader.Printf(string.format("%s | %s | cash=%s | fuel=%s | max=%s | type=%s",
    k, tostring(d.sName), tostring(d.nCashCost), tostring(d.nFuelCost), tostring(d.nMaxStock), tostring(d.sType)))
end
```

That's the actual script the support catalog was built from — one line per item instead of ~20.

</details>

## Dump every engine namespace at once

<details class="script-entry" markdown="1">
<summary>One-shot dump of every global namespace/module — prints roughly 12,000 log lines.</summary>

The single-table dumper above is great for one table you already know the name of. Sometimes you want a
complete inventory of *everything* reachable at global scope in one pass — every engine namespace
(`Player`, `Object`, `Vehicle`, `Event`, ...), every already-loaded `resident/` module, all in one log:

```lua
local tTopKeys = {}
for k in pairs(_G) do table.insert(tTopKeys, k) end
table.sort(tTopKeys, function(a, b) return tostring(a) < tostring(b) end)

local tSeen = {}

for _, sKey in ipairs(tTopKeys) do
  local v = _G[sKey]
  if type(v) == "table" and not tSeen[v] then
    tSeen[v] = true
    local tSubKeys = {}
    for k2 in pairs(v) do table.insert(tSubKeys, k2) end
    table.sort(tSubKeys, function(a, b) return tostring(a) < tostring(b) end)
    Loader.Printf("=== " .. sKey .. " (" .. #tSubKeys .. " entries) ===")
    for _, k2 in ipairs(tSubKeys) do
      Loader.Printf(sKey .. "." .. tostring(k2) .. " = " .. tostring(v[k2]))
    end
  else
    Loader.Printf("=== " .. sKey .. " (" .. type(v) .. ") ===")
  end
end
Loader.Printf("=== DUMP COMPLETE ===")
```

**Confirmed working by live testing** — but be aware of what you're triggering before you run it:

- **This prints upwards of 12,000 log lines in one go.** Every global table's direct members get their
  own `Loader.Printf` call, and there are dozens of tables (`Player` alone is 100+ entries; `Net`, `Sound`,
  `Object`, and `Pg` are all similarly large).
- **The game will hang for a bit while this runs.** All those log writes happening back-to-back visibly
  freezes the game for a few moments before control returns — this is expected, not a crash. Don't panic
  and don't spam re-run it while it's still working.
- This is one level deep only (each global's *direct* members) — it won't recurse into nested tables, so
  it stays a manageable size instead of exploding into an unbounded recursive dump.
- Useful as a one-time "get everything" snapshot to save off and grep through later, rather than something
  you'd run repeatedly. Save the resulting log somewhere stable (it'll get overwritten/rotated eventually)
  if you want to keep it around for reference.

</details>

## Show a custom HUD message (with icon and sound)

<details class="script-entry" markdown="1">
<summary>Reuse the tutorial-hint popup widget for your own custom message.</summary>

The little tutorial-hint popup the game shows for things like "you're swimming" or "you're low on fuel"
turns out to be a completely generic, reusable primitive — nothing about it is specific to tutorials:

```lua
import("MrxTutorialManager")
MrxTutorialManager.ShowMessage("Hello from my mod!")
```

**Confirmed working by live testing** — shows your exact text in that same popup widget, complete with
the usual notification sound cue:

![The tutorial-hint HUD popup showing custom text "Hello from my mod!" with the default book icon, rendered over an outdoor HQ balcony scene.](img/showtutorialmessage.png)

**There's no auto-hide timer** — the message stays up until something explicitly clears it:

```lua
MrxTutorialManager.HideMessage()
```

**Confirmed working** — clears it immediately.

Two more arguments exist on both functions — `ShowMessage(sMessage, bDontNetSync, sIdentifierName)` /
`HideMessage(bDontNetSync, sIdentifierName)`:

- **`sIdentifierName`** — an arbitrary string tag. **Confirmed working by live testing**: if you show a
  message tagged `"test1"`, a `HideMessage` call with a *different* (or missing) identifier won't clear
  it — only a matching identifier does. Useful if more than one script might want to show a message
  around the same time and you don't want them clearing each other's.
  ```lua
  MrxTutorialManager.ShowMessage("Message A", false, "test1")
  MrxTutorialManager.HideMessage(false, "wrong_id")  -- does NOT clear it
  MrxTutorialManager.HideMessage(false, "test1")     -- clears it
  ```
- **`bDontNetSync`** — per source, when this is `false`/omitted and you're the server/host, the message
  also broadcasts to your co-op partner via a network event; `true` keeps it local-only. **Not tested**
  — confirming the actual network behavior needs a second player, the same limitation as the
  [co-op tether snippet idea](sample-scripts-onload). The single-player behavior (shown above) doesn't
  depend on this argument either way.

One more thing worth knowing about the icon: the built-in tutorials (swimming, low fuel, etc.) each show
a specific icon — a d-pad, a joystick, a running figure — but that icon isn't a parameter to
`ShowMessage` at all. Checking one of those tutorials' source directly, its message is just a
**localization string key** (e.g. `"[Tutorial.Swimming]"`), not raw text — the icon is baked into
whatever that key resolves to in the string table, which this wiki doesn't have access to. Our plain-text
test rendered a generic book icon instead, which is presumably the default when no icon tag is present.
There's no known way to choose a different icon for a custom message.

</details>

## Show a clean, centered toast notification

<details class="script-entry" markdown="1">
<summary>A plain-text, icon-free popup using the engine's own EventFanfare system.</summary>

A different, simpler-looking popup than the tutorial-hint one above — no icon, no gold header, just
plain text centered on screen, using the engine's own `EventFanfare` system (see
[Hud: EventFanfare sType catalog and the custom toast trick](namespaces/hud#eventfanfare-stype-catalog-and-the-custom-toast-trick)
for the full story of how this was found):

```lua
import("MrxGuiHudMessage")

MrxGuiHudMessage._tEventTextures.custom = "this_texture_does_not_exist"
Hud.EventFanfare:Commence({sType = "custom", vText = "Whatever message I want!"})
```

**Confirmed working by live testing** — the `import`/table-write only needs to happen once (an `OnLoad`
or `OnBoot` script is a good place for it); after that, any later script can just call
`Hud.EventFanfare:Commence({sType = "custom", vText = "..."})` on its own. Multiple calls queue up and
play one after another automatically rather than overlapping — the same fanfare queue every built-in
fanfare variant shares.

![The clean, icon-free EventFanfare toast notification showing only the plain text "Whatever message I want!" centered on screen over an indoor scene with a yellow chicken-costume character in the foreground.](img/eventfanfaretext.png)

One nuance confirmed while testing this: reusing the exact name of a texture that's already loaded (e.g.
`"unlockables_newstockpileitem"`) makes a real icon *and* a gold header appear — but the header text shown
is that texture's own built-in title, not anything customizable from here. Stick to a made-up name that
doesn't match any real texture if you want the clean, text-only look.

![The same EventFanfare call but with a real, existing texture name reused instead — a gold "NEW STOCKPILE ITEM" header and a gold crate/box icon appear alongside the custom message text, with the header text coming from the reused texture's own built-in title rather than anything set by the script.](img/eventfanfare.png)

</details>

## A dangerous vehicle speed boost (irreversible once started)

<details class="script-entry" markdown="1">
<summary>A joke script that permanently shoves your current vehicle forward — no off switch.</summary>

A silly one — repeatedly shoves whatever vehicle you're currently riding in forward with a physics
impulse, scaled to the vehicle's own mass:

```lua
function StartSpeedBoost()
  UpdateSpeedBoost()
end

function UpdateSpeedBoost()
  local uPlayerChar = Player.GetLocalCharacter()
  if uPlayerChar then
    local uVehicle = Vehicle.GetFromRider(uPlayerChar)
    if uVehicle and Object.IsAlive(uVehicle) then
      -- Optional: only apply boost if the player is pressing the gas/moving
      local currentSpeed = Object.GetVelocity(uVehicle)
      if currentSpeed > 1.0 then
        -- Apply a forward impulse (adjust the Z component to change the push force)
        local myMass = Object.GetMass(uVehicle) or 1000
        Object.ApplyImpulse(uVehicle, 0, 0, 30 * myMass, true)
      end
    end
  end
  -- Reschedule this update function to run every 200ms (0.2 seconds)
  Event.Create(Event.TimerRelative, {0.2}, UpdateSpeedBoost)
end

StartSpeedBoost()
```

**Warning: you cannot turn this off.** `UpdateSpeedBoost` reschedules itself via `Event.TimerRelative`
forever, with no active/inactive flag checked anywhere — unlike the toggleable `OnKey` scripts elsewhere
in this wiki, there's no second button press that cancels it. Once it's running, it keeps shoving
whatever vehicle you're in every 0.2 seconds for the rest of the session. Running this a second time
doesn't reset or replace the first loop either — it just adds a *second*, independent boost loop stacking
on top of the first, making things worse, not better. Short of reloading the level (or the whole game),
the only way out is getting the vehicle destroyed or getting out of it entirely — and even then, the loop
keeps running in the background, ready to grab the next vehicle you enter.

Treat this as a joke/stress-test snippet, not something to actually drive with.

</details>

## Gating the speed boost behind a held key

<details class="script-entry" markdown="1">
<summary>The same boost, but only while a key (Shift) is actually held.</summary>

The [`Loader.IsKeyDown(vk)`](lua-bridge-api/loader) function (a lua-bridge addition, not part of the game
itself — see the [lua-bridge API](lua-bridge-api/) section) turns the joke above into something actually
controllable: one line makes the boost only apply while a key is physically held down, rather than
running unconditionally forever.

```lua
function StartSpeedBoost()
  UpdateSpeedBoost()
end

function UpdateSpeedBoost()
  local uPlayerChar = Player.GetLocalCharacter()
  if uPlayerChar then
    local uVehicle = Vehicle.GetFromRider(uPlayerChar)
    if uVehicle and Object.IsAlive(uVehicle) then
      local VK_SHIFT = 0x10
      if Loader.IsKeyDown(VK_SHIFT) then
        local currentSpeed = Object.GetVelocity(uVehicle)
        if currentSpeed > 1.0 then
          local myMass = Object.GetMass(uVehicle) or 1000
          Object.ApplyImpulse(uVehicle, 0, 0, 30 * myMass, true)
        end
      end
    end
  end
  Event.Create(Event.TimerRelative, {0.2}, UpdateSpeedBoost)
end

StartSpeedBoost()
```

Only one line changed — `if Loader.IsKeyDown(VK_SHIFT) then` around the impulse. The background loop
still reschedules itself forever exactly like the unrestricted version above (same caveat: running this
twice stacks a second independent loop, not a replacement), but its *effect* is now fully in your control —
release Shift and the pushing stops immediately, because the impulse simply doesn't get applied on ticks
where the key isn't held.

</details>

## A "while key is held" loop template

<details class="script-entry" markdown="1">
<summary>A bare template for code that runs every tick while a key is held down.</summary>

The same `Loader.IsKeyDown` + self-rescheduling `Event.TimerRelative` combination above is a genuinely
useful general-purpose building block on its own, worth having as a bare template: "run my code repeatedly,
for as long as a key stays held" — distinct from `OnKey`, which only fires once per press, not
continuously while held.

```lua
local VK_SPACE = 0x20  -- pick any virtual-key code you want to watch

function CheckHeldKeyLoop()
  if Loader.IsKeyDown(VK_SPACE) then
    -- Put your code here! This runs repeatedly, on every tick, for as long as
    -- the key stays held down -- not just once on the initial press.
    Loader.Printf("[mymod] space is currently held")
  end

  Event.Create(Event.TimerRelative, {0.2}, CheckHeldKeyLoop)
end

CheckHeldKeyLoop()
```

A few things worth understanding about the timing here, since it's easy to get wrong assumptions about:

- **`{0.2}` is how often this loop re-checks the key** — 5 times a second. Lower it (e.g. `{0.05}`) for
  snappier response, at the cost of more log spam and slightly more CPU use; raise it (e.g. `{0.5}`) if
  you don't need fast response and want things quieter. There's nothing special about `0.2` — it's a
  reasonable default, not a required value.
- **This is deliberately coarser than lua-bridge's own input polling** — `OnKey` itself polls at 30Hz, and
  `Loader.PopKeyEvents()` (see [lua-bridge API: Loader](lua-bridge-api/loader)) samples at ~60Hz
  specifically for cases that can't afford to miss a keystroke, like typed text. A plain
  `Event.TimerRelative` loop like this is the right tool when "check a few times a second" is good enough
  — true for most simple "while held, do X" effects — not when you need frame-tight timing.
  `Loader.IsKeyDown` itself is instantaneous (a single, cheap call) — the `0.2` interval is entirely about
  how often *you* choose to ask, not any limitation of the function being called.
- **One real caveat carried over from the [freecam deep dive](deep-dives/freecam)**: `Event.TimerRelative`
  is gated on the game's own simulation time, so a loop built this way stops rescheduling entirely if the
  world gets paused for any reason. Not a problem for most normal gameplay use, but worth knowing if an
  effect built this way mysteriously seems to "freeze."
- **Pick any key you want** — `VK_SPACE` (`0x20`) is just the example here. Swap in any Windows
  virtual-key code; see [Your First Mod](first-mod)'s link to Microsoft's own reference for the full list.

</details>

## Trigger the "Dance" easter egg animation

<details class="script-entry" markdown="1">
<summary>Play the "technoviking" dance animation used by the (apparently disabled) Dance radio prop.</summary>

`resident/danceradio.lua` defines a "Dance" radio prop meant to let a nearby character bust out a dance
move on use — but its real `OnActivate` is a no-op stub in the shipped game; only an old, unused
`OnActivateOld` actually wires up the context action and loads the asset. Looks like disabled/cut content.
The animation itself is still directly reachable, though:

```lua
local uChar = Player.GetLocalCharacter()
Pg.LoadAsset("player_mattias_bare_technoviking", "animation")
Human.PlayRawAnimation(uChar, "player_mattias_bare_technoviking", false, false, 0, false)
```

**Confirmed working by live testing**, bound to a `local KEYVAL = "pageup"` `OnKey` script. The animation
name is hardcoded to Mattias in the original source regardless of who plays it — the base game's own
(disabled) code calls it the same unconditional way — so it's untested whether it looks right played on
Chris or Jennifer specifically.

</details>

## Remove map boundaries

<details class="script-entry" markdown="1">
<summary>Lift every out-of-bounds restriction, for every connected player at once.</summary>

Certain areas are gated behind invisible boundary volumes attached to each player (see
[Player](namespaces/player) — the `AddBoundary`/`RemoveBoundary`/`RemoveAllBoundary`/`IsBoundaryDeath`
family; whether crossing one warns, forces a turn-back, or kills outright depends on how that specific
boundary was set up). This clears every boundary currently active on every connected player, co-op safe:

```lua
for _, p in ipairs(Player.GetAllPlayers()) do
    Player.RemoveAllBoundary(p)
end
```

This only clears what's active *right now* — it doesn't disable the boundary system itself, so the game's
own scripts can still add a new boundary later (e.g. on a mission or area transition).

</details>

## Custom ordnance & nuke drop system

<style>
.nuclear-drop { background: #14120a; border: 2px solid #ffcc00; border-radius: 8px; overflow: hidden; }
.nuclear-drop > summary { background: #000; color: #ffd400; font-weight: 700; padding: 0.65em 1em;
  cursor: pointer; border-bottom: 2px solid #ffcc00; list-style: none; }
.nuclear-drop > summary::-webkit-details-marker { display: none; }
.nuclear-drop > summary:before { content: "\2622  "; }
.nuclear-drop > *:not(summary) { padding: 0 1.1em; }
.nuclear-drop > *:first-of-type { padding-top: 0.9em; }
.nuclear-drop > *:last-child { padding-bottom: 0.9em; }
</style>

<details class="script-entry nuclear-drop" markdown="1">
<summary>A tunable multi-ordnance dropper — shells, bombs, and nukes — contributed by @Badga666 (Discord).</summary>

Shared by community member **@Badga666** on the project's Discord, describing their own tuning work on a
custom ordnance-dropping system built on `Ess`. This wiki hasn't independently re-tested it — treat the
specific ranges/values below as their own reported tuning experience, not wiki-confirmed fact, the same way
any other community contribution is flagged per [Contributing](CONTRIBUTING).

**How it's built**, in the contributor's own words:
- Replaced `ctx:hint` with `Ess.Easy.Toast` and wrapped engine calls in `Ess.Safe.call` to catch silent
  ordnance failures instead of failing invisibly.
- `"impact"`-triggered raw spawns reportedly ignore terrain, so arming switched to `"distance"` — detonating
  reliably after the projectile travels a set number of world units instead.
- Reverse-engineered `mrxfuelairbomb.lua` and `mrxbunkerbuster.lua` to replicate the official callback
  chains — `Ess.Loop` schedules fuel-cloud ignition, submunition scattering, and delayed shockwaves to land
  when the projectile would naturally detonate.
- Spawn height (`height`) is decoupled from detonation height (`fxAlt`): explosions lock to `py + fxAlt`
  (player Y plus an offset) for a ground-hugging blast regardless of spawn altitude or terrain slope.
- Nukes run through their own `dropNukes()`, keeping the same distance-arming and particle timing separate
  from the shared, tunable spawner every other ordnance type routes through.

All ordnance except nukes routes through one function:

```lua
dropOrdnance(ctx, name, radius, height, triggerType, triggerVal, velocity, fxType, fxAlt)
```

| Parameter | What it does | How to tweak | Reported range |
|---|---|---|---|
| `name` | Internal projectile template string | Match your build's ordnance names | `"Gunship Shell"`, `"Artillery Shell"`, `"Fuel Air Bomb Projectile"`, etc. |
| `radius` | Horizontal distance from player to drop zone | Lower = closer blasts, higher = safer distance | `30`–`120` |
| `height` | Spawn altitude above player Y | Higher = longer drop time (raise `triggerVal` to match) | `30`–`100` |
| `triggerType` | Arming method | `"distance"` (most reliable), `"timer"` (seconds), `"impact"` (reportedly often buggy) | `"distance"` |
| `triggerVal` | Arming threshold | Units traveled (`"distance"`) or seconds airborne (`"timer"`) before detonation | `40`–`120` |
| `velocity` | Downward drop speed (negative = falling) | Lower number = faster dive; keep proportional to `height` | `-80` to `-110` |
| `fxType` | FX routing tag | `"IMPACT"`, `"FAB"`, or `"CLUSTER"` — match the ordnance type | — |
| `fxAlt` | Detonation altitude above player Y | Lower = ground-hugging, higher = airburst | `2`–`8` |

Nukes use a separate function, `dropNukes(ctx, ringMode)`, tuned via locals inside it:

| Parameter | Default | Effect |
|---|---|---|
| `radius` | `120` | Ring diameter from player |
| `height` | `60` | Spawn altitude above player |
| `burstDist` | `100` | Travel distance before arming/detonation |

**The math behind it**, per the contributor:
- Detonation timing: `detTime = triggerVal / math.abs(velocity)` — e.g. `triggerVal = 80`, `velocity = -90`
  gives roughly a 0.89s delay before FX fire.
- FX altitude: `detY = py + fxAlt` — with `fxAlt = 2`, explosions lock to exactly 2 units above your feet.
- Ring distribution uses the engine's `x = sin(yaw), z = cos(yaw)` convention (see
  [Ess.Math](ess/core#essmath) for the same convention documented elsewhere on this wiki) —
  `Ess.Math.pointAhead()` handles the rotation, no manual yaw offset needed.

**Tuning tips, from the contributor's own notes:**
1. Explosions too high or low? Adjust only `fxAlt` — leave `height` alone unless you also want to change
   drop travel time.
2. Projectile detonating before it reaches the ground? Raise `triggerVal` by `10`–`20`.
3. Fuel-air-bomb cloud not forming? Raise `height` to `80`–`100` and `fxAlt` to `6`–`8` — FABs reportedly
   need altitude to disperse before ignition.
4. Cluster submunitions clumping together? Raise `triggerVal` to give the engine more frames to process the
   scatter logic.
5. FX out of sync with the blast? Adjust the `detTime` divisor, or add a `+0.2` buffer to the
   `Ess.Loop.start()` delay.
6. Testing a new ordnance type? Start from `"distance"` triggering, `velocity = -90`, `fxAlt = 3`, then tune
   from there.

</details>

## Ready for something more involved?

Everything above reads or writes a value. [Deep Dive: Overriding a Function](deep-dives/function-override)
walks through the next step up — replacing a piece of the game's own logic — end to end, including the
wrong turns along the way. The result of that case study is also available as a ready-to-use script under
[OnLoad Scripts](sample-scripts-onload).

## Something not here?

If you worked out a useful snippet that isn't listed, it's worth adding — this page is meant to grow.
