---
title: "Building ForgeCam — a Forge-Mode Placement Tool"
parent: Deep Dives
nav_order: 11
---

# Deep Dive: Building ForgeCam — a Forge-Mode Placement Tool

> **Status: confirmed working live.** A Halo-Forge-style world editor: fly a detached camera with the
> controller, pick a spawn template from a scrolling Scaleform menu with the keyboard, drop it at a live
> ghost cursor, delete or clear, and export every placement as a paste-ready data table. Built directly on
> top of the [Freecam deep dive](freecam) and the [Custom UI pipeline](custom-ui), and along the way it
> settled a question that sat in the gap between them — **yes, a HUD `FlashWidget` renders and takes
> `CallActionScriptCallback` while the PDA has the world paused** — plus turned up a real engine limitation
> (`Object.SetPosition` won't move a spawned AI human) and a performance model for the one callback that
> ticks under pause.

## The goal

The [freecam](freecam) gave us a detached flying camera driven by real analog input. ForgeCam turns that
camera into an **authoring tool**: an in-world editor where you fly around, choose from hundreds of spawn
templates, stamp them into the world with a controllable yaw and distance, remove mistakes, and dump the
result as coordinates a runtime spawn director can replay. Think Halo's Forge, running live inside
Mercenaries 2, feeding a data file.

Three problems the freecam never had to solve fall out of that:

1. **A menu with hundreds of options.** The native `MrxMultiPageMenu` paginates, but the spawn catalog is
   ~6,600 templates — that's hundreds of pages. This needs a real scrolling UI, which means a custom
   Scaleform movie ([custom-ui](custom-ui)).
2. **Keyboard *and* controller, at the same time, under a paused world.** The camera wants smooth analog
   flight; the menu wants discrete key nav. And the freecam's core trick pauses the game.
3. **Moving and previewing spawned objects** — which is where a genuinely surprising engine limitation
   showed up.

## The constraint everything else bends around: one heartbeat

Recall the freecam's central discovery: the only way to read continuous controller input in this engine is
to hijack the live PDA widget's `"ControllerInput"` event, and **opening the PDA pauses the world**. That
pause is the whole ballgame here, because of a second freecam finding:

**`Event.TimerRelative` does not fire while the world is paused** — it's gated on simulation time, which is
frozen (see [Event](../namespaces/event)). That single fact invalidates the *documented* way to drive a
custom GFx menu. The [custom-ui](custom-ui) stress test polls the keyboard on a self-rescheduling
`Event.Create(Event.TimerRelative, {0.05}, poll)` — and that timer is dead the moment the PDA opens.

So ForgeCam has exactly **one clock**: the `"ControllerInput"` callback itself. Camera flight, keyboard
polling, menu navigation, drop/remove, the panel-resize easing — all of it has to run from inside that one
function, because nothing else ticks. This is the rule the whole script is organized around.

## The performance wall (and how the callback actually behaves)

The naive version — do all the work inside the callback — was unusable: **stick input made the framerate
crater, and the camera became wildly oversensitive.** When the sticks were untouched it was perfectly
smooth. That split is the entire diagnosis:

- The `"ControllerInput"` callback **fires in a burst while a stick is deflected** — many times per
  rendered frame, one per input delta — and only a trickle when idle. (The freecam's stale-axis decay
  already implied this: the callback keeps firing after you release, which is how the decay-to-zero runs.)
- Every one of those burst calls was doing real work: two `Camera`/`Object` position writes, trig, and
  (in an early version) a dozen `Loader.IsKeyDown` boundary calls. At hundreds of calls per frame, that
  saturates the frame.
- And because movement used a **wall-clock `dt`** (`Sys.RealTimeStamp` — the one clock that keeps ticking
  while paused; see [Sys](../namespaces/sys)), the lag fed back into sensitivity: a stalled frame meant a
  big `dt`, which meant a big movement step, which *looked* like a hair-trigger stick. Lag and
  oversensitivity were the same bug.

The fix has three parts, and the order they run in matters:

**1. Capture cheaply every call; gate the expensive work on the real-time clock.** Most burst callbacks
now do nothing but copy the analog axes into a table and check the clock. The heavy work — movement, the
keyboard drain, the menu easing — runs at most once per `MOVE_TICK` seconds, no matter how fast the
callback bursts. The time-gate is what actually caps the cost.

```lua
local function OnPdaControllerInput(oSelf, tInput)
  if not F.active then return end
  -- capture axes (pure Lua, every call - cheap)
  if tInput.LeftAnalogX ~= nil then F.leftX = tInput.LeftAnalogX; F.leftXSeen = true end
  -- ...LeftAnalogY / RightAnalogX / RightAnalogY the same...

  -- discrete controller buttons: handled IMMEDIATELY (see part 2)
  local bp = tInput.ButtonPress
  if bp then
    if bp == BTN_FLY_UP then F.dpadUpHeld = true
    elseif bp == BTN_FLY_DOWN then F.dpadDownHeld = true
    else pcall(HandleButton, bp) end
  end
  -- ...ButtonReleased clears the fly-hold flags...

  -- everything expensive is time-gated on the wall clock (survives the pause)
  if not F.stamp then F.stamp = Sys.RealTimeStamp(); return end
  local dt = Sys.TimeStampGetElapsed(F.stamp)
  if dt and dt >= MOVE_TICK then
    Sys.TimeStampMark(F.stamp)
    pcall(Update, dt)          -- ApplyMovement + keyboard + panel easing
  end
end
```

**2. Handle discrete controller buttons immediately, outside the gate.** D-pad menu navigation has to feel
instant, and button events are rare (one per press) and cheap. If they were queued and drained only on the
gated tick, a press with the stick idle might not be processed until the next stick movement. So buttons
run the moment their event arrives; only the *continuous* work is throttled.

**3. Drain the keyboard once per tick with `Loader.PopKeyEvents()`, not N× `IsKeyDown`.** One ring-buffer
read replaces a dozen per-key boundary calls (the buffer is filled by lua-bridge's own background thread,
so nothing is missed between ticks; see [Loader](../lua-bridge-api/loader)).

Two tunables fell out of this, both at the top of the file:

- `MOVE_TICK` — minimum seconds between camera updates. This is the smoothness knob **and** the cost cap.
- `CB_STRIDE` — process the gated work only every Nth callback, a cheap early-out that further trims the
  clock reads during a burst.

The first pass set these conservatively (`MOVE_TICK = 0.033`, ~30 Hz) purely to kill the lag — which it
did, but left the camera visibly steppy. Once the framerate was confirmed solid, the last change was
simply to spend the headroom: `MOVE_TICK = 0.016` (~60 Hz) and `CB_STRIDE = 1`. The time-gate still caps
the expensive work regardless of how hard the controller bursts, so the smoothness came back with no
return of the lag. **The gate is the throttle; the refresh rate is just a number you dial against your
headroom.**

## The menu renders under the pause (the open question, answered)

This one sat squarely in the gap between two dives: [custom-ui](custom-ui) only ever exercised its widget
in normal, un-paused play, and [freecam](freecam) paused the world but never put a GFx menu on top of it.
So: does a HUD `FlashWidget` actually render and respond while the world is paused and the PDA is hidden?

**It works.** Live-confirmed: with the PDA open (world paused), the PDA widget hidden, and cinematic mode
active, a separate `MrxGuiBase.FlashWidget` loaded with a custom `.gfx` **renders on the HUD and executes
`CallActionScriptCallback` normally.** The AVM1 in the movie runs on demand when Lua calls into it — it
isn't gated by the simulation pause the way `TimerRelative` is. That's the fact that makes a real Forge
menu possible at all, and it's reusable for any paused-world custom UI.

The menu itself follows the [custom-ui](custom-ui) division of labor exactly: the `.gfx` is a dumb view
(12 row slots, a breadcrumb, a highlight bar, a scrollbar thumb) authored in gfxforge-web and injected with
gfx_tool. **All the logic lives in Lua** — the catalog, the nav stack, scrolling, selection — and is pushed
into the movie with `CallActionScriptCallback("SetRow"/"SetSelected"/"SetCrumb"/"SetScroll"/...)`, driven
from the one heartbeat. Because the catalog is pure Lua data, adding factions or units never touches the
movie:

```lua
local function L(s) return { label = s, id = s } end   -- leaf: label == spawn template
local CATALOG = {
  { label = "GUERILLA", children = {
    { label = "INFANTRY", children = {
      L("Guerilla Heavy (RPG)"), L("Guerilla Soldier"), L("Guerilla Officer"), --[[ ...dozens... ]]
    } },
    { label = "VEHICLES", children = { L("M151 (MG) (GR)") } },
  } },
  -- ...ALLIED / CHINA / OC / PIRATE / VZ, each a faction -> category -> leaves...
  { label = "EXPORT PLACEMENTS", action = "export" },
}
```

`SORT_ITEMS` alphabetizes within a category, which — because every template name starts with its faction
and role — naturally clusters the types (`… Heavy (…)`, `… Soldier …`, `… Worker …`) without any manual
grouping.

## Input: letters, because the open PDA eats the arrows

The keyboard side hit a conflict the standalone custom-ui menu never did: **while the PDA is open, the game
itself claims the arrow keys** (they drive the PDA's own d-pad navigation), and almost certainly Enter and
Space as well. Any key the PDA wants is unreliable for us. So ForgeCam's keyboard map is **letters only** —
`O`/`L` to move the highlight, `K` to open a category or drop a leaf, `J` to go back, `P` to drop, and so
on. They're remappable constants, but the rule is "avoid anything the PDA navigates with."

Controller buttons come through the same `"ControllerInput"` event as `tInput.ButtonPress` / `ButtonReleased`
numeric IDs — the d-pad is `1`–`4`, the face buttons `5`–`8`. Using them for menu nav has a nice property:
they're the *same* input vocabulary the PDA navigates with, so they reliably fire the callback (which,
remember, is our only heartbeat).

## `Object.SetPosition` moves props and vehicles — but not spawned humans

The brush preview was supposed to be simple: spawn the selected template as a "ghost" and move it with the
cursor every frame, the same way the freecam moves its look-at anchor prop with `Object.SetPosition`. It
half-worked in a very telling way: the ghost appeared, but it was **stuck** — it wouldn't follow the
cursor — and it only showed up *after* the first drop.

Two findings behind that:

- **The camera anchor (a prop) follows `SetPosition` fine; a spawned AI *human* does not.** Same call, same
  coordinates, same frame — the soldier just stays where it spawned. The [Object](../namespaces/object)
  page already lists `SetPosition`'s behaviour on non-vehicles (and its mystery 4th argument) as
  unconfirmed; this is a concrete data point for it. Spawn-*position* always works (that's how everything
  is placed); it's *re*-positioning a human that silently no-ops.
- The "only after a drop" half was a plain init bug — the cursor coordinate wasn't computed until the first
  movement tick, so the first preview spawned at the world origin. Seeding the cursor position on activate
  fixes it.

The fix for the human problem is to **make the ghost follow by re-spawning it.** Each tick, try
`SetPosition` (which smoothly moves vehicles and props), then check the object's *actual* position against
the cursor — if it's still far off, it's a human that ignored the move, so re-spawn it there. Throttled, so
it doesn't churn:

```lua
-- in ApplyMovement: try to move it (works for vehicles/props; humans ignore this)
if F.uPreview then
  pcall(Object.SetPosition, F.uPreview, F.ax, F.ay, F.az)
  pcall(Object.SetYaw, F.uPreview, F.dropYaw)
end

-- in Update: if it DIDN'T actually move to the cursor, re-spawn it there (throttled)
if F.uPreview and F.brush then
  local bOk, px, py, pz = pcall(Object.GetPosition, F.uPreview)
  if bOk and px then
    local dx, dy, dz = F.ax - px, F.ay - py, F.az - pz
    if (dx*dx + dy*dy + dz*dz) > PREVIEW_STEP2 and (F.now - (F.pvT or 0)) > PREVIEW_MIN_DT then
      SpawnPreview()          -- remove + Pg.Spawn at the cursor
    end
  end
end
```

The visible tradeoff: an infantry ghost **hops** to the cursor in steps (each re-spawn) rather than
gliding, while vehicles and props glide smoothly via `SetPosition`. For an authoring tool that's fine — you
aim, the ghost settles where the drop will land, you stamp it.

## The brush → preview → drop → export loop

Everything ties together into one model:

- Highlighting a **leaf** in the menu sets it as the active **brush** and spawns/updates the ghost preview.
- **Drop** commits the current ghost as a placed object, records its real position (via `GetPosition`, so
  the recorded coordinate matches what you see), and spawns a fresh ghost so you can keep stamping.
- **Remove** deletes the nearest placed object to the cursor — but only ever a guid ForgeCam itself
  spawned, tracked in a table, so it can never nuke real level content.
- **Export** walks the placement list and prints a paste-ready table to `lua_loader_printf.log` — the exact
  shape a runtime spawn director consumes (an anchor centroid plus per-unit `{ template, x, y, z, yaw }`):

```lua
Loader.Printf(string.format("{ sId = \"forge_%d\", tAnchor = { %.2f, %.2f, %.2f }, tComposition = {",
  math.floor(F.now), cx, cy, cz))
for _, e in ipairs(F.tPlaced) do
  Loader.Printf(string.format("    { s=%q, x=%.2f, y=%.2f, z=%.2f, yaw=%.2f },", e.s, e.x, e.y, e.z, e.yaw))
end
Loader.Printf("} },")
```

Because the world is paused during authoring, placed units hold still while you compose — and if you exit
Forge without clearing them, they come alive when the world un-pauses, so the same tool doubles as a live
preview of the encounter you just built.

## Controls

| Input | Action |
|---|---|
| **F6** | toggle Forge (open the PDA first — same requirement as the freecam) |
| Left stick / Right stick | fly camera / look + aim the cursor |
| D-pad up-down | fly the camera up / down |
| **O / L** | move the menu highlight up / down (highlighting a leaf sets the brush) |
| **K** | open a category / run an action / drop the highlighted leaf |
| **J** | menu back (up a level) |
| **P** (or Space) | drop the active brush at the cursor |
| **N** | remove the nearest Forge-placed object |
| **Q / E** | spin the drop yaw · **Z / X** cursor nearer / farther |
| **B** | export placements to the log · **M** clear all Forge objects |
| D-pad / face buttons | mirror the menu nav + drop/remove on the controller |

## Known limitations

- **Paused-world only.** Everything here inherits the freecam's constraint: continuous controller input
  requires the PDA open, which pauses the world. That's a *feature* for authoring (placed units hold
  still), but it's not a live-gameplay editor.
- **Infantry previews hop, they don't glide** — the `SetPosition`-vs-human limitation above. Vehicles and
  props follow smoothly.
- **The re-spawn preview churns objects** while you fly with an infantry brush selected (a `Pg.Spawn` +
  `Remove` every ~0.1 s). Throttled and fine in practice, but it's real work; the throttle constants are
  tunable if it ever hitches.
- **Catalog IDs must be exact `Pg.Spawn` template strings.** A typo drops nothing and prints
  `DROP FAILED` — which is also the cheapest way to validate a name.
- **The 4th argument to `Camera.SetPosition` / `Object.SetPosition` is still unconfirmed** (see
  [Camera](../namespaces/camera) / [Object](../namespaces/object)); ForgeCam relies on the interpolation
  the freecam's setup already established rather than probing it further.

## Why this matters beyond ForgeCam

- **A HUD `FlashWidget` works under the PDA pause.** This is the reusable headline: any tool that wants a
  real custom UI *while* using the freecam's paused-world input trick can now assume the GFx menu will
  render and drive. It closes the loop between [Custom UI](custom-ui) and [Freecam](freecam).
- **The paused-world heartbeat pattern.** When `TimerRelative` is dead, the `"ControllerInput"` callback is
  your only tick — and it bursts. Capture cheaply every call, time-gate the expensive work on
  `Sys.RealTimeStamp`, handle discrete buttons immediately, and drain the keyboard with `PopKeyEvents`.
  That's a transferable recipe for anything realtime under pause.
- **`Object.SetPosition` doesn't move spawned humans.** A concrete, confirmed limitation to design around —
  move a human by re-spawning it, not by repositioning it.
- **The open PDA claims the arrow keys.** If you're layering a keyboard UI over the freecam trick, reach
  for letter keys.

## Cross-references

- [Building a Real Freecam](freecam) — the input hijack, the paused world, the look-at-anchor camera this
  is built on.
- [Custom UI — Authoring Scaleform Movies](custom-ui) — the gfxforge / gfx_tool pipeline behind the menu,
  and the `CallActionScriptCallback` bridge.
- [Event](../namespaces/event) — why `TimerRelative` is dead under pause.
- [Object](../namespaces/object) / [Camera](../namespaces/camera) — `SetPosition` / `SetYaw` and their
  unconfirmed flags.
- [Loader](../lua-bridge-api/loader) — `PopKeyEvents` / `IsKeyDown` for the keyboard side.
- [Getting Started](../getting-started) — the `OnKey` script model and `Loader.Printf` this deploys through.
