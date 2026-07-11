---
title: "Contract.Register & Lifecycle"
parent: Contract Framework
nav_order: 1
---

# Contract.Register & Lifecycle

> **Status: new, in development.** Read directly from `ContractFramework.lua` (read in full). Behavior
> described here is what the code currently does, not yet independently confirmed by extended live play.

## Why this exists instead of the native contract system

The game's own mission system (`WifMissionData` + `MrxTask`) is the same system the
[Adding a Custom Contract](../deep-dives/custom-contract) deep dive fought with — it serializes task nodes
**into the save file** and drives missions through `dynamic_import` + `mrxbriefing` + the `MrxState` load
gate. Hook into it and you risk corrupting a save in a way that's very hard to diagnose or undo.

`ContractFramework.lua` sidesteps all of that: a contract is a **plain, ephemeral runtime object**, built
only from primitives that were always safe to call from Lua — `Pg.Spawn`, `Event.*`, `Object.*`,
`MrxPmc`. Nothing here is written to the save. The tradeoff is explicit: an active contract does **not**
survive a save/reload. It's simply re-offered (via the [Contract Board](contract-board)) the next time a
level loads. For an ephemeral, replayable side-mission system, that's a fair trade for never touching the
save file at all.

## The whole modder-facing surface

```lua
Contract.Register{
  id       = "my_contract",      -- unique string, required
  title    = "My Contract",
  category = "CUSTOM",           -- groups contracts on the board
  briefing = "One or two sentences shown on the board.",
  reward   = { cash = 50000, fuel = 20 },     -- also: support = {id=n,...}, equipment = {id,...}
  start    = { x = 0, y = 0, z = 0, yaw = 0 }, -- teleports the player here on accept (optional)
  objectives = {
    Contract.Destroy{ desc = "Destroy 3 cars" },
    Contract.Reach{ desc = "Reach the drop-off", radius = 12 },
  },
  onComplete = function() end,   -- optional
  onFail     = function() end,   -- optional
}
```

That covers the common case. The full set of `def` fields a contract can use:

| Field | Purpose |
|---|---|
| `id`, `title`, `briefing`, `category` | Identity and board display. `id` is the only required field. |
| `reward` | `{ cash=, fuel=, support={id=qty,...}, equipment={id,...} }` — paid out via `MrxPmc` on completion. |
| `start` | `{x,y,z,yaw}` (or a **list** of them, one per co-op hero) — teleports the player(s) there via `MrxUtil.TeleportHeroesToLocations` before objectives begin. Omit to start wherever the player already is. |
| `objectives` | An array built from the [objective builders](objectives) — see that page for all 15 types. |
| `mode` | `"sequential"` (default) or `"parallel"` — see [Objectives Reference](objectives). |
| `timeLimit` | Overall seconds before the whole contract auto-fails. |
| `fail` | Background conditions built from `Contract.Protect{...}` / `Contract.StayInArea{...}` — see [Objectives Reference](objectives). |
| `relations`, `units`, `waypoints` | See [Units, AI Orders & Relations](units-ai-and-relations). |
| `support`, `triggers` | See [Support Effects & Triggers](support-effects-and-triggers). |
| `intro` | An opening radio line (via the HUD objective tray) played right as the contract begins. |
| `fanfareType`, `fanfare` | Customize the native completion sting — see [Support Effects & Triggers](support-effects-and-triggers#fanfare) for the valid `fanfareType` values. |
| `onComplete`, `onFail` | Plain Lua callbacks, called once, after reward payout / cleanup. |
| `fResolve` | `function(def)` — runs once, at accept time, to fill in coordinates that can't be known until the player accepts (e.g. relative to wherever they're currently standing). Real modder contracts authored with absolute coordinates from the [MissionForge](mission-forge) creator don't need this — it exists for the built-in demo contract below. |
| `onBegin` | `function(inst)` — an escape hatch for a bespoke gamemode built *on top of* a contract. See [Handing off to a bespoke gamemode](#handing-off-to-a-bespoke-gamemode) below. |
| `hideTracker` | `true` to suppress both the native HUD objective-tray line and the [Contract Board](contract-board)'s own floating tracker panel — for a gamemode that draws its own HUD entirely. See the same section below. |

## `Contract.Accept(idOrDef)`

Starts a contract, by id (looked up in the registry) or by passing a definition table directly (what the
[Contract Board](contract-board) does).

- **Co-op gating:** skipped entirely if `Net.IsMultiplayer() and Net.IsClient()` — only the host runs
  contracts. `Net.IsClient()` can read `true` in single-player too, which would silently no-op every
  accept if gated on that alone; gating on `IsMultiplayer` as well avoids that.
- Any already-active contract is aborted first (`C.Abort()`), and `C.finished` is cleared so
  [`Contract.Status()`](#contractstatus) reflects the new contract, not the previous one's result.
- If `def.fResolve` is set, it runs now, before anything else.
- If `def.start` is set, `MrxUtil.TeleportHeroesToLocations` moves the player(s) there, and the rest of
  acceptance runs in that call's completion callback — so objectives never start spawning underneath a
  player who hasn't teleported yet.
- Setup order matters: `def.intro`'s radio line plays, then relations
  ([Units, AI Orders & Relations](units-ai-and-relations)) and background support/triggers
  ([Support Effects & Triggers](support-effects-and-triggers)) are each wrapped in their own `pcall` —
  deliberately, so a bad relation or a misconfigured support entry can't prevent the actual objective list
  from starting. Errors there are logged, not swallowed silently.
- Finally the objective list runs via the same runner [Objectives Reference](objectives) describes,
  finishing the contract (win or lose) through `C._finish`.

## Handing off to a bespoke gamemode

A contract doesn't have to be *just* a mission — `def.onBegin` lets it be the launcher for something much
larger, and [WaveDefense](../wave-defense) is the fullest worked example of this. `onBegin(inst)` fires
inside `Accept`'s `begin()`, after the player has been teleported and relations/support/triggers are set
up, but **before** the objective list starts running:

```lua
if def.onBegin then local obOk, obE = pcall(def.onBegin, inst); if not obOk then Loader.Printf("Contract: onBegin error -> " .. tostring(obE)) end end
C._runList(inst, def.objectives or {}, def.mode, function(ok) C._finish(inst, ok) end, ...)
```

Wrapped in its own `pcall`, same as every other optional setup step — a bad `onBegin` can never prevent the
objective runner from starting. The pattern this enables: give the contract a single, effectively-never-
completing placeholder objective (WaveDefense uses `Contract.Survive{ time = 3600 }`), do all the *real*
game logic in `onBegin` and your own heartbeat, and call `Contract._finish(inst, bWin)` **yourself**,
directly, whenever your own logic decides the run is actually over. `ContractFramework.lua` still owns
accept/teleport/relations/reward-payout/fanfare/cleanup — your gamemode owns everything about what
"winning" even means.

**`def.hideTracker = true`** pairs with this: it suppresses the native HUD objective-tray line (the
`hudLine(1, ...)` calls throughout every objective handler go silent while a `hideTracker` contract is
active) *and*, independently, tells the [Contract Board](contract-board) not to spawn its own floating
tracker panel for this contract. Between the two, a `hideTracker` contract gets a completely clean screen —
no native or board-drawn UI competing with whatever HUD your own gamemode draws (via
[UI Kit](../uilib/), for instance).

## `Contract.Status()`

A read-only snapshot of the live contract, in exactly the shape the [Contract Board](contract-board) reads:

```lua
{ finished = nil | "complete" | "failed",
  progress = 0.0 .. 1.0,     -- fraction of top-level objectives done
  timeLeft = seconds,        -- only present if def.timeLimit was set
  objectives = { { done = true|false }, ... } }  -- parallels def.objectives
```

Returns `nil` if nothing is active and nothing has just finished. Once a contract finishes, `Status()`
keeps returning its final result (`finished = "complete"|"failed"`) until the next `Accept` clears it —
this is what lets the board show a completion/failure screen instead of just going blank.

## `Contract.Abort()`

Force-ends the active contract as a failure (`C._finish(inst, false)`) if one is running; a no-op
otherwise. The board's own confirm-before-cancel flow calls this.

## The built-in demo contract

`ContractFramework.lua` registers one contract itself, `demo_convoy`, so the board isn't empty on a fresh
install:

```lua
C.Register({
    id = "demo_convoy", title = "Demo: Wreck the Convoy", category = "DEMO",
    briefing = "Three cars, then reach the drop.",
    reward = { cash = 50000, fuel = 100 },
    objectives = {
        C.Destroy({ desc = "Destroy 3 cars" }),
        C.Reach({ desc = "Reach the drop-off", radius = 12 }),
    },
    -- fResolve runs at accept time to fill in dynamic coords (here, relative to the player). Real
    -- modder contracts use absolute coords from the creator and don't need this.
    fResolve = function(def)
        local uc = Player.GetLocalCharacter(); if not uc then return end
        local x, y, z = Object.GetPosition(uc)
        def.objectives[1].tSpawns = { { "Veyron", x + 8, y, z + 3, 0 }, { "Veyron", x + 10, y, z, 0 }, { "Veyron", x + 8, y, z - 3, 0 } }
        def.objectives[2].tZone   = { x = x + 40, y = y, z = z, r = 12 }
    end,
})
```

This is the one case in the whole framework where coordinates are computed at accept time instead of
authored up front — because a demo contract has to work from *wherever* the player happens to be standing,
not a fixed location. A real contract built from [MissionForge](mission-forge) captures absolute world
coordinates directly, so `fResolve` is rarely needed outside cases like this.

## Deploying a contract file

Every contract file is expected to guard against the framework not being loaded yet:

```lua
if not _G.Contract then
    Loader.Printf("MyContracts: Contract framework not loaded - give ContractFramework.lua a LOWER [OnLoad] number")
    return
end
```

This is why load order matters (see the [section index](index#load-order)): `_G.Contract` only exists once
`ContractFramework.lua` itself has run.
