---
title: "Building MissionForge — a Contract Authoring Tool"
parent: Deep Dives
nav_order: 14
---

# Deep Dive: Building MissionForge — a Contract Authoring Tool

> **Status: new, in development.** Two concrete, documented fixes are baked directly into the shipped
> script's own comments — a stray-table-hole export bug and a keyboard-polling rewrite that cut bridge
> calls per tick from 14 to 2 — which is real evidence of iteration against the running game, not just
> a design written once and left alone. The full round-trip (Forge → web tool → deployed contract →
> played to completion) hasn't been independently re-confirmed end to end in this writeup.

MissionForge (`scripts/OnKey/MissionForge.lua`) is the in-game half of the
[Contract Framework](../contract-framework/)'s authoring pipeline — walk around, drop objectives and
units, export a paste-ready dump for [the web tool](../contract-framework/web-tool) to finish. It shares
its GFx menu and input-handling lineage directly with [ForgeCam](forgecam), but almost everything about
*how* it places things is a deliberate departure from that earlier tool — because the two are solving
genuinely different problems.

## Why not just reuse ForgeCam's approach wholesale

ForgeCam's whole design centers on one fact: the only way to get continuous controller input is to hijack
the PDA widget, and opening the PDA **pauses the world**. That's fine for a free-flying camera authoring
tool — you want the world to hold still while you compose a shot or a placement. It's a much worse fit for
a mission-authoring tool that needs the player's *own character* to walk around a normal, unpaused level,
place things at believable distances apart, and get a feel for how a firefight will actually read.

MissionForge's own header states the model plainly: **"Runs in the LIVE, UNPAUSED world. You just WALK your
merc around; the drop point is ALWAYS the character's feet."** No camera hijack, no PDA, no pause — just
walking, with a menu overlay and a ring-shaped cursor anchored directly to the player's own character (so
it tracks position for free, no per-tick repositioning cost at all).

## The bigger departure: no live preview, at all

[ForgeCam](forgecam)'s central discovery was that `Object.SetPosition` won't move a spawned human — its
ghost preview had to work around that by re-spawning the preview object every time it needed to move,
throttled to avoid churn. MissionForge sidesteps the entire problem a different way: **it never spawns a
live preview to move in the first place.**

Every placement drops an **inert marker**, not the real thing:

- Infantry → a faction-colored "Supply Drop (...)" crate.
- Vehicles → the **empty** variant of the chosen vehicle (crew suffixes like `" (Full)"`/`" (Driver)"`
  stripped from the template name).
- Props → the prop itself (already inert, nothing to strip).
- Objectives / support call-ins / triggers / AI orders → a `TinyGeometry` anchor plus a ground ring and
  the same radar/PDA/world marking [Support Effects & Triggers](../contract-framework/support-effects-and-triggers)
  documents for the real framework.

The export still carries the **real** template string (`"HMMWV (Softtop) (Full)"`, not the empty
placeholder that was actually spawned) — the placeholder only exists so the world isn't full of live,
active AI wandering around and shooting at things while you're trying to compose a mission around them.
This is a smaller, cheaper, and fundamentally simpler answer to "how do I preview a placement" than
ForgeCam's re-spawn-to-simulate-movement trick — it works *because* MissionForge never needed the preview
to move at all, only to mark a spot.

## Squads: one placement, a whole formation

Beyond single units, MissionForge builds a **SQUADS** branch per faction from two tables: a per-faction
`role → template` map (`off`, `rifle`, `mg`, `at`, `elite`, `boss`, `tank`, `apc`, `truck`, `heli`, ...) and
13 squad archetypes (`Fire Team`, `Rifle Squad`, `Armor Platoon`, up to a 24-unit `Battle Group`), each just
a list of `{role, count}` pairs. Dropping a squad places every unit in a grid formation at your feet,
rotated to match your facing, all sharing one squad id — so a single **Backspace** undoes the *entire*
squad in one step, not one unit at a time.

## Bugs found and fixed along the way

- **A trailing-nil hole could silently truncate exports.** `RemoveLast`/`RemoveNearest` used to pop
  entries directly out of the placements array; a pop that left a hole made `#F.items` (and therefore
  `ipairs` over it) unreliable — anything placed after the hole would vanish from the export without any
  error. The fix, `compact()`, rebuilds the array as a genuinely dense sequence via `pairs()` before every
  undo/remove/export, which also recovers anything that was already stranded past an earlier hole:
  ```lua
  local function compact()
      local keys = {}
      for k in pairs(F.items) do if type(k) == "number" then keys[#keys + 1] = k end end
      table.sort(keys)
      local out = {}
      for _, k in ipairs(keys) do out[#out + 1] = F.items[k] end
      F.items = out
  end
  ```
- **Per-key polling was a real, measured framerate hit.** The comments record the fix directly: keyboard
  input dropped from 14 lua-bridge calls per tick down to 2 — one `Loader.PopKeyEvents()` ring-buffer drain
  for discrete presses (menu nav, place, undo, export — each fires exactly once per press, in order,
  focus-gated) plus a single `Loader.GetKeyboardState()` snapshot for the two *held* keys (objective radius
  `,`/`.`). This is the same "drain the ring, don't poll every key" idiom [ForgeCam](forgecam) and
  [the Contract Board](../contract-framework/contract-board) both converged on independently.
- **The heartbeat tick rate itself was tuned down.** `TICK` is explicitly commented as "PERF TEST: halved
  from 0.05/20Hz" — the self-rescheduling `Event.TimerRelative` heartbeat that drains input and eases the
  panel now runs at ~10Hz instead of ~20Hz, with no loss of responsiveness noticed, since the actual input
  drain (`PopKeyEvents`) doesn't miss anything regardless of how often it's called — it's a ring buffer, not
  a poll.

## The heartbeat: simpler than ForgeCam's, because the world isn't paused

Since MissionForge never pauses anything, its self-rescheduling `Event.TimerRelative` loop doesn't need
[ForgeCam](forgecam)'s wall-clock-vs-simulation-time distinction at all — `Sys.RealTimeStamp` is still used
for the actual elapsed-time measurement (clamped to 0.25s max, in case of a stall), but there's no PDA
pause to work around, so the loop is a plain generation-guarded self-rearm:

```lua
local function startTick(gen)
    local function loop()
        if not F.active or F.gen ~= gen then return end
        local dt = TICK
        if F.stamp then
            local e = Sys.TimeStampGetElapsed(F.stamp)
            if e and e > 0 then dt = e end
            Sys.TimeStampMark(F.stamp)
        end
        if dt > 0.25 then dt = 0.25 end
        local ok, err = pcall(Update, dt)
        if not ok then Loader.Printf("MissionForge: ERROR -> " .. tostring(err)) end
        Event.Create(Event.TimerRelative, { TICK }, loop)
    end
    Event.Create(Event.TimerRelative, { TICK }, loop)
end
```

The `F.gen` generation counter is what lets toggling MissionForge off (or back on) cleanly kill the old
chain — each `loop()` call checks it still matches the generation that started it, so a stale chain from
before a toggle just quietly stops rescheduling itself instead of needing an explicit cancel/handle-tracking
scheme.

## The export

Pressing **End** dumps one evaluable Lua table to `lua_loader_printf.log`:

```lua
MISSIONFORGE_EXPORT = {
  name = "forge_<t>", anchor = { x=, y=, z= },
  spawns = { { x=, y=, z=, yaw= }, ... },   -- optional player teleport point(s); co-op = 1 per hero
  units = { { faction=, kind=, spawn=, placeholder=, x=, y=, z=, yaw=, group= }, ... },
  objectives = { { type=, x=, y=, z=, radius=, yaw=, group= }, ... },
  support = { { effect=, x=, y=, z=, radius=, group= }, ... },     -- artillery/flyby/heli/reinforce zones
  triggers = { { x=, y=, z=, radius=, group= }, ... },             -- generic trigger zones
  orders = { { behavior=, x=, y=, z=, radius=, group= }, ... },    -- AI orders (move/patrol/defend/attack/hold/face)
}
```

This is deliberately a much flatter, more mechanical shape than a real `Contract.Register` definition —
positions, templates, and group tags only. No trigger conditions, no relations, no reward, no text. That's
by design: **[the web tool](../contract-framework/web-tool) fills in everything that isn't a physical
placement** — owner factions, ordnance choices, trigger modes, relations, and every piece of narrative
text. `group` tags are the one piece of structure MissionForge does carry over: units, objectives, support,
triggers, and orders placed while the same group letter (cycled with **T**) is active all arrive
pre-associated, so the web tool's auto-wiring (a trigger fires the support/order sharing its group) has
something real to connect on import rather than starting from nothing.

## Controls reference

See [MissionForge](../contract-framework/mission-forge) in the Contract Framework section for the full
day-to-day controls table, catalog structure, and export workflow.

## Open questions

- **The full round-trip hasn't been independently re-walked here.** Forge → export → web tool import →
  generated Lua → deployed contract → played to actual completion is a long chain; this writeup verified
  each *piece* against source, not a single unbroken live session through all of them.
- **Co-op behavior is untested.** The export format explicitly supports one spawn point per hero
  (`spawns = { ... }`), but multi-player authoring/playtesting isn't confirmed here.
- **Whether the squad-formation grid ever collides with terrain/geometry** on uneven ground isn't
  addressed in the source — it's a flat local grid rotated to facing, with no ground-height sampling
  beyond the player's own `y` at drop time.

## See also

- [ForgeCam](forgecam) — the camera/input/menu lineage this tool shares, and the paused-world constraints
  it deliberately does *not* inherit.
- [Contract Framework](../contract-framework/) — the section index for the whole system MissionForge feeds
  into.
- [MissionForge (reference)](../contract-framework/mission-forge) — controls, catalog, and workflow for
  day-to-day use.
- [The Web Tool](../contract-framework/web-tool) — what happens to a `MISSIONFORGE_EXPORT` dump next.
