---
title: Building a Real Freecam
parent: Deep Dives
nav_order: 1
---

# Deep Dive: Building a Real Freecam

## The goal

A detached, fully controllable flying camera — the kind of thing most games with a dev/spectator mode
ship — driven by a real controller's analog sticks and d-pad, not scripted paths or keyboard taps.

This turned out to require solving a much harder problem first: **this game's Lua layer has no
documented way to read continuous controller input at all.** Everything that looked like it might work
turned out to be something else. The eventual solution is a genuine engine feature (a general-purpose
widget input event), just not one anybody would think to look for from a modding angle — it's hidden
inside the PDA's own menu-navigation code.

## The dead ends (worth knowing about even though they didn't work)

### `Event.Button` — real, but only 4 fixed actions

[`Event.Button`](../namespaces/event#input--player-events) is a real, live-testable event — but grepping
every `Event.Create(Event.Button, ...)` call site in the whole decompiled corpus turns up exactly 4
button-name strings, ever: `"lbutton"`, `"rtrigger"`, `"cancel"`, `"selection"`. These are semantic
action names tied to specific tutorial/HUD features, not a general input map. No directional/stick names
exist anywhere in this system.

### `Event.Minigame` — a QTE evaluator, not a poll

[`Event.Minigame`](../namespaces/event#input--player-events) does accept real `Controller.*` constants
(the numeric IDs behind d-pad/stick-tilt directions), which looked promising. Live testing showed why it
still doesn't work for this: `"hold"` mode doesn't report sustained hold duration or live stick position
— it accumulates discrete motion/wiggle pulses toward a completion threshold, the same mechanic the
retail hijack QTE's `"alternate"` (mash-between-two-directions) mode uses. Holding a stick steady in one
direction produces nothing; wiggling it produces a `"success"`/`"failed"` outcome, once, then the
listener needs re-arming. No continuous state anywhere in it.

### Bare widgets — no dispatch without being genuinely active

`MrxGuiBase.Widget:new({})` can create a raw, unattached widget with a real `SetEventHandler` method.
Hooking `"ControllerInput"` on one and just leaving it sitting in memory produces nothing — zero events,
whether or not any menu is open. Widget existence alone isn't enough; something about being a genuinely
active/focused UI element is required, which a bare `Widget:new()` never becomes on its own.

## The breakthrough: hijacking the PDA's own input

Every GUI widget in this engine — confirmed by reading `_HandleInputForFlashWidget` in
`shell/mrxguibase.lua` and the PDA's own `_HandleInput` in `resident/mrxguipda.lua` — can receive a
`"ControllerInput"` event carrying a genuinely continuous, real-time input table:

```lua
tInput = {
  LeftAnalogX = 0.5,  LeftAnalogY = -0.13,   -- real floats, only present when non-idle
  RightAnalogX = 0.3, RightAnalogY = 0.05,
  ButtonPress = 1,     -- a Joystick.BUTTON_* numeric ID, present only on the frame a button goes down
  ButtonReleased = 1,  -- present only on the frame it comes back up
}
```

The PDA already has a live, working widget instance permanently sitting in memory (created once at game
start, just hidden until opened) — it doesn't need to be spawned. Every widget in the game is tracked in
a genuinely public table: `resident/mrxguibase.lua:311` declares `WidgetIdIndex = {}` **without** the
`local` keyword, so it's reachable as `MrxGuiBase.WidgetIdIndex` after `import("MrxGuiBase")`. Scanning
that table (comparing a dump taken with the PDA closed against one with it open — every entry was
identical except the four widgets literally named `"PDA"`, `"PDA Subtitle Buffer"`, and two unnamed
children) finds the live PDA widget directly, by name, with zero need to reverse-engineer its internal
`Open()` flow.

From there, the technique is:

1. Find the widget named `"PDA"` in `WidgetIdIndex`.
2. Overwrite its `"ControllerInput"` handler with your own function — `SetEventHandler` just replaces
   whatever was registered before, and (confirmed live) reopening the real PDA afterward restores normal
   menu behavior with no lingering breakage.
3. Hide it: `SetVisible(false)` on the `"PDA"` and `"PDA Subtitle Buffer"` widgets is sufficient — the
   two unnamed children hide along with them, no need to target them separately.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

Step 2 works because a widget's event handler is just a table field that happens to hold a function —
`SetEventHandler("ControllerInput", myFunction)` really just does something like
`self.EventHandlers.ControllerInput = myFunction` under the hood. There's nothing special "wiring" it to
the PDA's own original logic permanently; overwriting that field is exactly as valid as overwriting a
number or a string field would be, because in Lua a function is a first-class value like any other. This
is the same fact that makes the [function-override deep dive](function-override) work — reassigning a
name changes what gets called *the next time* something looks that name up, no matter who set it
originally or who's setting it now.

</details>

4. The game world visibly pauses while the PDA is open (confirmed: same as normal PDA behavior, not
   something this technique causes). The 3D view itself returns to normal (not stuck on any PDA-specific
   camera) once hidden.
5. Closing/reopening the real PDA afterward works exactly as before — this is fully reversible.

## The bugs that showed up building an actual camera on top of this

Getting real input flowing was the hard part, but four more issues had to be found and fixed before a
usable camera came out the other end — each one is a real, confirmed property of this engine, not a
guess:

**`Event.TimerRelative` doesn't fire while the world is paused.** The obvious way to drive a per-frame
update loop — `Freecam.Tick()` rescheduling itself via `Event.Create(Event.TimerRelative, ...)` — only
ever fired once and then went silent, because that timer is gated on *simulation* time, which is exactly
what's frozen while the PDA has the world paused. Fix: drive movement directly from inside the
`"ControllerInput"` callback itself (which keeps firing fine — it's UI input, not gameplay simulation),
using [`Sys.RealTimeStamp()`/`Sys.TimeStampGetElapsed()`](../namespaces/sys#time--clock) for real,
wall-clock delta time instead.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

The callback passed to `Event.Create`/`SetEventHandler` in this script is a **closure** — a function that
was defined *inside* another block of code and can still see (and change) the local variables around it
even after that outer code has finished running. `OnPdaControllerInput` and `ApplyMovement` both reach
into `Freecam` — a `local` declared once, near the top of the file — every single time the engine calls
them, potentially thousands of calls later. Nothing has to be passed back in as an argument to make that
work; the function just remembers where `Freecam` lives, the same way it would remember any other local
variable from its surrounding scope. See [Snippets: React to an event instead of polling](../snippets#react-to-an-event-instead-of-polling)
for a simpler first look at this same idea — a callback function is just "code to run later" that still
has access to whatever was around it when it was written.

</details>

**Analog axes go stale instead of reporting zero.** The engine only sends `LeftAnalogX`/etc. fields when
a value is actively changing — once a stick returns to center (or you simply stop moving it), the field
stops appearing in `tInput` entirely rather than one final event reporting `0`. Naively only updating a
tracked value "when present" means it freezes at its last nonzero reading forever, producing runaway
drift that continues after you've let go. Fix: track a last-updated timestamp per axis and force it back
to `0` if it hasn't been refreshed in ~150ms.

**`Object.SetPosition` doesn't visually propagate under plain world-pause, but does once
`Player.SetCinematicMode` is active.** A spawned prop's position can be set every tick and nothing moves
on screen — until `Player.SetCinematicMode(uPlayer, true, true)` is also engaged, at which point the
exact same calls start working immediately. `Camera.SetPosition` is unaffected either way (it works
under plain pause). This suggests object/physics-simulation updates and camera-rendering updates are
gated by two different systems, and cinematic mode re-enables the former.

**`Camera.SetPosition` itself needs an active `Camera.SetLookAt` binding to actually commit.** A bare
`Camera.Hold(uCamera, true, false)` plus `SetPosition`, with no `SetLookAt` ever called, silently does
nothing — not even a hardcoded, oversized test teleport moves the camera. The moment a `SetLookAt` target
exists (even a static one, never repositioned), `SetPosition` starts working immediately. The practical
approach that came out of this: spawn a small prop (`Pg.Spawn("Verification Camera", ...)` — the same
placeholder template `resident/mrxtaskobjectiveverify.lua` uses for its own scripted camera shots),
`SetLookAt` the camera to it once, and use the prop as a "where am I pointing" pointer from then on.

**Movement direction and look direction must be computed from the same angle, or they desync.** An
earlier version moved the camera along fixed world axes while a separate mechanism handled "look,"
which meant "forward" stopped meaning forward the moment you turned. The fix (and the final design):
the right stick rotates a yaw/pitch angle; the look-at prop is placed out in front of the camera along
that angle every tick (`Object.SetPosition` on the prop, which is Lua's only avenue to real camera
rotation here — direct `Camera.SetYaw`/`SetPitch` calls kept getting overridden by the game's own
chase-cam logic no matter what `Hold` flags were tried); and the left stick's forward/strafe vectors are
computed from that exact same angle, so they can never drift out of sync.

## The final script

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

Every line below starting `Freecam.X = Freecam.X or default` is doing the same small trick, and it's
worth understanding why before reading the rest: **`OnKey` scripts re-run their entire file from scratch
on every keypress.** Any plain `local` declared in the file is gone the instant the script finishes and
gets rebuilt fresh next time — which is exactly wrong for something like `Freecam.active` or `Freecam.camX`,
which need to *survive* between the "turn on" press and the "turn off" press, and between every single
input event in between. `_G` (the global table) is the one thing that genuinely persists across separate
runs of an `OnKey`/`OnLoad` script within the same play session, so `_G.RealFreecam = _G.RealFreecam or {}`
means "reuse the existing table if one's already there from last time, otherwise start a fresh one" — and
then each `Freecam.field = Freecam.field or default` fills in any field that doesn't exist yet, without
clobbering one that's already mid-flight. This exact pattern is also the fix for a real bug hit while
building this: an earlier version used one big table literal (`_G.RealFreecam = _G.RealFreecam or { ...all
fields at once... }`), and once a new field got added to that literal mid-session, `_G.RealFreecam`
already existed from an older run and the `or` short-circuited — so the new field was just missing,
producing an `attempt to perform arithmetic on a nil value` error until the whole table was reset by hand.
Setting each field individually, the way the script below does, means adding one later never breaks an
already-running session.

</details>

```lua
local KEYVAL = "f4"

_G.RealFreecam = _G.RealFreecam or {}
local Freecam = _G.RealFreecam
Freecam.active = Freecam.active or false
Freecam.camX = Freecam.camX or 0
Freecam.camY = Freecam.camY or 0
Freecam.camZ = Freecam.camZ or 0
Freecam.camYaw = Freecam.camYaw or 0
Freecam.camPitch = Freecam.camPitch or 0
Freecam.moveSpeed = Freecam.moveSpeed or 60
Freecam.lookSpeed = Freecam.lookSpeed or 2
Freecam.vertSpeed = Freecam.vertSpeed or 60
Freecam.lookDistance = Freecam.lookDistance or 10
Freecam.deadzone = Freecam.deadzone or 0.15
Freecam.leftX = Freecam.leftX or 0
Freecam.leftY = Freecam.leftY or 0
Freecam.rightX = Freecam.rightX or 0
Freecam.rightY = Freecam.rightY or 0
Freecam.dpadUpHeld = Freecam.dpadUpHeld or false
Freecam.dpadDownHeld = Freecam.dpadDownHeld or false
Freecam.now = Freecam.now or 0
Freecam.leftXAt = Freecam.leftXAt or 0
Freecam.leftYAt = Freecam.leftYAt or 0
Freecam.rightXAt = Freecam.rightXAt or 0
Freecam.rightYAt = Freecam.rightYAt or 0

local PI = 3.14159265

local function normalizeAngle(x)
  local twoPi = 2 * PI
  x = x % twoPi
  if x > PI then x = x - twoPi elseif x < -PI then x = x + twoPi end
  return x
end

-- math.sin/math.cos don't exist in this Lua build -- Taylor-series fallbacks.
local function customSin(x)
  x = normalizeAngle(x)
  local x2 = x * x
  return x * (1 - x2 * (0.16666666666667 - x2 * (0.00833333333333 - x2 * 0.000198412698)))
end

local function customCos(x)
  x = normalizeAngle(x)
  local x2 = x * x
  return 1 - x2 * (0.5 - x2 * (0.04166666666667 - x2 * (0.00138888888889 - x2 * 0.000024801587)))
end

local function ApplyDeadzone(n)
  if math.abs(n) < Freecam.deadzone then return 0 end
  return n
end

local function ApplyMovement(dt)
  local uCamera = Player.GetCamera(Player.GetLocalPlayer())
  if not uCamera then return end

  local nLX = ApplyDeadzone(Freecam.leftX)
  local nLY = ApplyDeadzone(Freecam.leftY)
  local nRX = ApplyDeadzone(Freecam.rightX)
  local nRY = ApplyDeadzone(Freecam.rightY)

  -- Right stick: rotate the look direction (yaw/pitch), clamp pitch so it
  -- can't flip past straight up/down.
  Freecam.camYaw = Freecam.camYaw + nRX * Freecam.lookSpeed * dt
  Freecam.camPitch = Freecam.camPitch + nRY * Freecam.lookSpeed * dt
  if Freecam.camPitch > 1.4 then Freecam.camPitch = 1.4 end
  if Freecam.camPitch < -1.4 then Freecam.camPitch = -1.4 end

  local fCos = customCos(Freecam.camYaw)
  local fSin = customSin(Freecam.camYaw)

  -- Left stick: move camera forward/strafe, relative to current yaw -- same
  -- angle driving the look direction, so they can't desync.
  Freecam.camX = Freecam.camX + (nLY * fCos - nLX * fSin) * Freecam.moveSpeed * dt
  Freecam.camZ = Freecam.camZ + (nLY * fSin + nLX * fCos) * Freecam.moveSpeed * dt

  -- D-pad: pure vertical flight.
  if Freecam.dpadUpHeld then Freecam.camY = Freecam.camY + Freecam.vertSpeed * dt end
  if Freecam.dpadDownHeld then Freecam.camY = Freecam.camY - Freecam.vertSpeed * dt end

  -- Anchor: placed out in front along the current yaw/pitch -- this is what
  -- actually "points" the camera via SetLookAt.
  if Freecam.uAnchor then
    local fPitchCos = customCos(Freecam.camPitch)
    local ax = Freecam.camX + Freecam.lookDistance * fPitchCos * fCos
    local az = Freecam.camZ + Freecam.lookDistance * fPitchCos * fSin
    local ay = Freecam.camY + Freecam.lookDistance * customSin(Freecam.camPitch)
    Object.SetPosition(Freecam.uAnchor, ax, ay, az)
  end

  Camera.SetPosition(uCamera, Freecam.camX, Freecam.camY, Freecam.camZ, true)
end

local function OnPdaControllerInput(oSelf, tInput)
  local bOk, sErr = pcall(function()
    if not Freecam.lastStamp then
      Freecam.lastStamp = Sys.RealTimeStamp()
      return
    end
    local dt = Sys.TimeStampGetElapsed(Freecam.lastStamp)
    Sys.TimeStampMark(Freecam.lastStamp)
    if not dt then return end

    Freecam.now = Freecam.now + dt

    if tInput.LeftAnalogX ~= nil then Freecam.leftX = tInput.LeftAnalogX; Freecam.leftXAt = Freecam.now end
    if tInput.LeftAnalogY ~= nil then Freecam.leftY = tInput.LeftAnalogY; Freecam.leftYAt = Freecam.now end
    if tInput.RightAnalogX ~= nil then Freecam.rightX = tInput.RightAnalogX; Freecam.rightXAt = Freecam.now end
    if tInput.RightAnalogY ~= nil then Freecam.rightY = tInput.RightAnalogY; Freecam.rightYAt = Freecam.now end
    if tInput.ButtonPress == 1 then Freecam.dpadUpHeld = true end   -- Joystick.BUTTON_PAD1_U
    if tInput.ButtonPress == 2 then Freecam.dpadDownHeld = true end -- Joystick.BUTTON_PAD1_D
    if tInput.ButtonReleased == 1 then Freecam.dpadUpHeld = false end
    if tInput.ButtonReleased == 2 then Freecam.dpadDownHeld = false end

    -- Stale-axis decay: the engine stops sending a field once it's idle
    -- rather than reporting a final 0, so force it back to centered after
    -- ~150ms of silence.
    local nStaleAfter = 0.15
    if Freecam.now - Freecam.leftXAt > nStaleAfter then Freecam.leftX = 0 end
    if Freecam.now - Freecam.leftYAt > nStaleAfter then Freecam.leftY = 0 end
    if Freecam.now - Freecam.rightXAt > nStaleAfter then Freecam.rightX = 0 end
    if Freecam.now - Freecam.rightYAt > nStaleAfter then Freecam.rightY = 0 end

    ApplyMovement(dt)
  end)
  if not bOk then
    Loader.Printf("REALFREECAM: ERROR -> " .. tostring(sErr))
  end
end

local function FindPdaWidget()
  import("MrxGuiBase")
  for k, oWidget in pairs(MrxGuiBase.WidgetIdIndex) do
    local bOk, sName = pcall(function() return oWidget:GetName() end)
    if bOk and sName == "PDA" then return oWidget end
  end
  return nil
end

local function SetPdaVisible(bVisible)
  import("MrxGuiBase")
  for k, oWidget in pairs(MrxGuiBase.WidgetIdIndex) do
    local bOk, sName = pcall(function() return oWidget:GetName() end)
    if bOk and (sName == "PDA" or sName == "PDA Subtitle Buffer") then
      pcall(function() oWidget:SetVisible(bVisible) end)
    end
  end
end

local uPlayer = Player.GetLocalPlayer()
local uCamera = Player.GetCamera(uPlayer)
local uChar = Player.GetLocalCharacter()

if uPlayer and uCamera and uChar then
  Freecam.active = not Freecam.active

  if Freecam.active then
    Loader.Printf("REALFREECAM: activating -- open the PDA now if it isn't already open")

    local oPdaWidget = FindPdaWidget()
    if not oPdaWidget then
      Loader.Printf("REALFREECAM: could not find PDA widget -- is it open?")
      Freecam.active = false
    else
      oPdaWidget:SetEventHandler("ControllerInput", OnPdaControllerInput)
      SetPdaVisible(false)

      local px, py, pz = Object.GetPosition(uChar)
      Freecam.camX, Freecam.camY, Freecam.camZ = px, py + 2, pz
      Freecam.camYaw, Freecam.camPitch = 0, 0
      Freecam.leftX, Freecam.leftY, Freecam.rightX, Freecam.rightY = 0, 0, 0, 0
      Freecam.dpadUpHeld, Freecam.dpadDownHeld = false, false
      Freecam.lastStamp = nil
      Freecam.now, Freecam.leftXAt, Freecam.leftYAt, Freecam.rightXAt, Freecam.rightYAt = 0, 0, 0, 0, 0

      Freecam.uAnchor = Pg.Spawn("Verification Camera", px, py + 2, pz + Freecam.lookDistance)

      Player.SetCinematicMode(uPlayer, true, true)
      Object.SetVisible(uChar, false)
      Object.SetInvincible(uChar, true, "Freecam")

      Camera.Blend(uCamera, 0)
      Camera.SetLookAt(uCamera, Freecam.uAnchor)
      Camera.Hold(uCamera, true, false)
    end
  else
    Loader.Printf("REALFREECAM: deactivating")
    Camera.Hold(uCamera, false, false)
    Object.SetVisible(uChar, true)
    Object.SetInvincible(uChar, false, "Freecam")
    Player.SetCinematicMode(uPlayer, false)
    SetPdaVisible(true)
    if Freecam.uAnchor then
      Object.Remove(Freecam.uAnchor)
      Freecam.uAnchor = nil
    end
  end
end
```

**Confirmed working by live testing** — both sticks and the d-pad function correctly: left stick moves
the camera forward/strafe relative to current facing, right stick rotates look direction cleanly with no
desync, d-pad flies straight up/down.

## Controls

| Input | Effect |
|---|---|
| `f4` | Toggle freecam on/off (PDA must be open to activate) |
| Left stick | Move forward/back/strafe, relative to current facing |
| Right stick | Look (yaw/pitch) |
| D-pad up/down | Fly up/down |

## Known limitations

- **Requires the PDA to be open, and freezes the game world while active.** This is a paused-world
  flycam (inspection, screenshots, cinematic camera paths), not a live-gameplay spectator camera —
  nothing else in the world moves or updates while it's on. Whether the pause can be separated from the
  input stream (so the world keeps running while flying around) hasn't been investigated.
- **Controller-only.** Everything here comes through the `"ControllerInput"` widget event; mouse-look
  was investigated separately and found to have no equivalent — see the note on `Camera.Hold`'s rotation
  flag in [Vehicle](../namespaces/vehicle) and [Camera](../namespaces/camera) for the related dead end
  where a detached camera's rotation stayed locked no matter how `Hold`'s flags were combined.
- **The player character is hidden and invincible while active**, not actually removed from the world —
  restored automatically on deactivate.
- **`moveSpeed`/`vertSpeed`/`lookSpeed`/`deadzone` are tunable constants** in the script, not confirmed
  "correct" values from any source — adjust to taste.

## Why this matters beyond freecam

The core technique — finding a permanently-alive widget via `MrxGuiBase.WidgetIdIndex`, hijacking its
`"ControllerInput"` handler, and hiding it — isn't freecam-specific. It's the only known way to get real
continuous analog/digital input into a Lua script in this engine at all. Anything that needs to react to
held-down input, analog magnitude, or genuine per-frame controller state (rather than one-shot press
events) can reuse this same pattern.
