---
title: Engine facts and gotchas (curated)
---

The things a general-purpose model reliably gets wrong about this game. These are the
highest-value corrections in the whole pack -- when one applies, say so explicitly rather
than silently writing correct code, because the user has probably been bitten by it.

## The runtime

- **Lua 5.1, statically linked.** No `require`. No `+=`, no `//`, no bitwise operators.
- **`lua_Number` is float, not double** -- precision-sensitive math can surprise you, and
  RNG seeded from a float behaves accordingly.
- **Multiple return values are normal**: `local x, y, z = Object.GetPosition(uGuid)`.
- **`X and A or B` is the ternary substitute**, and its one real trap is that it collapses
  to `B` whenever `A` itself is falsy. Only safe when `A` can never be `false`/`nil`.
- **`pairs` vs `ipairs`**: `pairs` visits every key in arbitrary order; `ipairs` walks only
  a plain `1..n` array and stops at the first gap. Mixing them up drops data silently
  instead of erroring.
- The full `math.*` stdlib (sin/cos/atan2/sqrt/random/pi/...) plus `assert` exist as
  lua-bridge polyfills. Older wiki scripts hand-roll a Taylor-series sine from before
  those existed -- that is no longer necessary. `os`/`io`/`coroutine`/`debug` presence is
  **not** confirmed; check `type(os) == "table"` before relying on any of them.

## import() — what you may and may not import

A local 7B model reading this pack produced `import("Pg")` and `import("Ess")`.
Both are wrong, so here it is as examples rather than a rule:

```lua
-- WRONG: engine namespaces are ALWAYS global. Importing one errors.
import("Pg")  import("Object")  import("Player")  import("Ai")  import("Vehicle")

-- WRONG: Ess is a global table, not a module. There is no import for it.
import("Ess")

-- RIGHT: engine namespaces need nothing at all.
local x, y, z = Object.GetPosition(Player.GetLocalCharacter())
local uGuid = Pg.Spawn("Allied Soldier", x, y, z)

-- RIGHT: Ess is guarded, never imported.
if not _G.Ess then Loader.Printf("load Ess first") return end

-- RIGHT: import() is ONLY for resident modules (src/resident/*.lua), and is
-- file-scoped, so every file that uses one needs its own line.
import("MrxPmc")
MrxPmc.AddCashQty(100000)
```

The engine namespaces — never import any of these: `Object`, `Player`, `Vehicle`,
`Ai`, `Event`, `Pg`, `Marker`, `Sound`, `Human`, `Camera`, `Airstrike`, `Weapon`,
`Sys`, `Net`, `Gui`, `Hud`, `Controller`, `Junk`, `Graphics`.

## Silent failure modes

- **An uncaught error in an OnKey/OnLoad/OnBoot script silently ends that run.** Nothing
  is printed anywhere -- unlike the Console, which reports a `[runtime]` error. `pcall` +
  `Loader.Printf` is currently the only way to see what failed.
- **Engine getters return `1`/`0`, not `true`/`false`.** In Lua only `nil` and `false` are
  falsy, so `not someGetter()` is `false` even when the getter returned `0` -- the
  expression never flips. Track a real boolean in `_G` instead.
- **Only `_G` persists between separate runs of the same script** within a session. The
  standard idiom:
      `_G.MyState = _G.MyState or {bOn = false}`
- **Calling a nonexistent method inside a `pcall` fails silently.** `IsVisible()` does not
  exist (the getter is `GetVisible()`); the nil-call is swallowed and nothing visibly
  breaks, it just never works.
- **`Event.Create(Event.TimerRelative, {sec}, fn)` fires once.** For a repeating timer,
  `fn` must re-arm its own next call as its first line.

## Load order and bindings

- Script hooks: `scripts/OnBoot/*.lua` (once, earliest), `scripts/OnLoad/*.lua` (once per
  level load), `scripts/OnKey/*.lua` (per keypress, edge-triggered, ~250ms reentrancy
  cooldown per script).
- An OnKey script needs **both** `local KEYVAL = "<key>"` in its first 10 lines **and** a
  `<script>.lua=<key>` line under `[OnKey]` in `lua_loader.ini`.
- **Code edits are live** -- the loader re-reads the script file on every keypress. But a
  new/moved file, or an `.ini` binding change, needs a **game relaunch**.
- Framework mods conventionally take a `1_` filename prefix so the alphabetical loader
  runs them first; `lua_loader.ini`'s numeric priority overrides that.
- `Loader.IsKeyDown` / `GetKeyboardState` / `PopKeyEvents` take **numeric Windows VK
  codes** -- a different scheme from OnKey's `KEYVAL = "keyname"` string. The two are not
  interchangeable. `IsKeyDown` is for continuous/held input; `PopKeyEvents` is an
  edge-triggered ring buffer for typed text and has no "still held" signal.

## Input and UI

- **There is no native free-text input widget.** Hand-roll it from `Loader.PopKeyEvents()`
  plus a VK-code-to-character table.
- **A HUD FlashWidget composites transparent** -- the movie's own background colour is not
  painted, so the game world shows through anywhere nothing is drawn. For a solid panel,
  draw a full-stage rectangle as the bottom layer.
- **Menu keyboard navigation is never automatic.** A HUD widget receives no mouse or
  gamepad input on its own; the host must poll `Loader.IsKeyDown` on a self-rescheduling
  timer, **edge-trigger** against the previous frame (a raw poll fires ~20x/sec, so one
  press otherwise moves many rows), clamp the index, and call the movie's setter.
- **HUD input is polled, not consumed** -- keys pressed while a custom HUD is open still do
  whatever the game itself does with them.
- `SetSwfFile` is **asynchronous**: do not call movie functions from inside the same build
  step, or variable-bound fields stay blank.

## Factions and NPCs

- **PMC is the player's own faction, and it is not a troop faction.** It covers the
  player character and a handful of story NPCs — that is all. **There is no PMC troop
  template of any kind.** Every `pmc`-prefixed entry in the template list is a building
  or a prop (`_pmcoutpost_bld_hq`, `_pmcoutpost_beerA`, …).

  This is the single most-asked question that has a *negative* answer, so here is the
  answer to give, near enough verbatim. Do **not** put a PMC unit string in a code
  block first and correct it afterwards — the reader copies the code and skips the prose.

  > There is no PMC troop template — PMC is your own faction, so the game never
  > shipped rank-and-file PMC units. Spawn from a faction that *does* have troops and
  > make them friendly instead:
  >
  > ```lua
  > local x, y, z = Object.GetPosition(Player.GetLocalCharacter())
  > local uSoldier = Pg.Spawn("Allied Soldier", x + 5, y, z)
  > Ai.SetFeeling(uSoldier, Player.GetLocalCharacter(), 100)
  > ```

  The first template string in your answer must be one that exists. If you catch
  yourself about to write a PMC unit name, write the block above instead.
- Every *other* faction **does** have troop templates — `"VZ Soldier"`,
  `"Allied Soldier"`, `"Guerilla Soldier"`, `"Chinese Soldier"`, `"OC Soldier"`
  (Oil Company), `"Pirate Thug"`, plus Elite / Paratrooper / Female / B variants.
  Quote them exactly from the authoritative template list; PMC is the only faction
  missing one.
- The faction system itself is engine-side. There is no documented Lua call that creates
  a new faction; relations and attitudes between existing factions are the adjustable
  part.

## AI orders: Goal, Role and Deploy are three different calls

Their argument tables are **not interchangeable**, and mixing them is the most
common way generated AI code fails.

- `Ai.Goal{AIGuid=, Goal=, Target=, Location=, Priority=, Mode=, Start=, Haste=,
  Callback=, CallbackData=}` — a destination/task. Real `Goal` values include
  `"PathMove"`, `"MoveToPos"`, `"MoveTo"`, `"Enter"`.
  **A raw XYZ destination goes in `Location`, as a plain `{x, y, z}` table** —
  confirmed across many call sites in the Contract Framework source, e.g.
  `Ai.Goal{AIGuid = a, Goal = "MoveToPos", Location = {x, y, z}, Priority = "HiPri", Force = true}`.
  The key is `Location`, **not** `Position` and not `Target` (`Target` takes a
  guid). Selecting the goal by intent: `"path"` -> `PathMove`, `"object"` ->
  `MoveTo` (a guid target), `"coord"` -> `MoveToPos` (a `Location`).
  You do **not** need to spawn a `TinyGeometry` anchor just to move someone to a
  point — that is the separate `defend` recipe (move there, then `Ai.Anchor` with
  a radius to hold the area).
- `Ai.Role{AIGuid=, Role=, Target=, MinDistance=, MaxDistance=, MoveDistance=,
  Priority=}` — a standing behaviour. **`"Follow"` is a `Role`, not a `Goal`.**
  `Ai.Goal{Goal="Follow"}` is wrong; the confirmed follow recipe is
  `Ai.Role{Role="Follow", Target=uTarget, ...}` (see `resident/mrxfollow.lua`).
- `Ai.Deploy{Vehicle=, Role="Passenger", Force=}` — a transport disgorging riders.

`Role` belongs to `Ai.Role` and `Ai.Deploy`. It is **not** an `Ai.Goal` key.

If Ess is available, prefer `Ess.AIOrders.command(guids, behavior, opts, tracker)`
and let it pick the right primitive. Its first argument is always a **table of
guids** — `command({uGuid}, "follow")`, never a bare guid.

## Economy, spawning, objects

- `MrxPmc.AddCashQty(n)` / `AddFuelQty(n)` are the **HUD-updating** economy calls. Plain
  `Player.SetCash`/`AddCash` change the value but skip the HUD refresh.
- `Pg.Spawn("<template>", x, y, z)` needs an **exact** template string -- these are not
  predictable from the in-game display name. Use the spawn reference; if a name is not
  there, say so rather than guessing a spelling.
- `uGuid` is an opaque runtime handle. It is **not stable across game sessions** -- never
  persist one and expect it to resolve later.

## Known hard limits -- do not propose confident workarounds

- **No confirmed Lua touchpoint for firing a turret**, or for controlling a vehicle's
  camera while driving or gunning. Extensively tested across multiple recipe matrices,
  hardpoint probing, and camera-lock attempts -- these appear to be native-only.
- **`Object.ApplyImpulse` / `ApplyPointImpulse` do not affect a standing player character.**
  Confirmed to work on vehicles and physics props; tested live on a player, no effect.
- **Multi-player teleport helpers can crash the game inside an interior cell** -- outdoor
  only.
- **Physics on some set-dressing "vehicle" templates cannot be fixed from Lua** -- it needs
  WAD-level editing tools that do not exist for this game yet.
- `Object.GetYaw`/`SetYaw` **unit and axis convention is unconfirmed.** The wiki's own
  sample scripts disagree with each other -- one treats the value as degrees, another
  applies an empirically fudged radian correction. Tell the user to test rather than
  picking one.
