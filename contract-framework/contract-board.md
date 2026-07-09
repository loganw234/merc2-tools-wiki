---
title: The Contract Board
parent: Contract Framework
nav_order: 6
---

# The Contract Board

> **Status: new, in development.** Read directly from `contracts.lua` (read in full). Behavior described
> here is what the code currently does, not yet independently confirmed by extended live play.

`contracts.lua` is the entire player-facing side of the framework: a category-grouped mission list, a
details/rewards/objectives panel, and HUD tracker widgets that stay up while a contract is running. It owns
**only** the UI — registering, running, and paying out contracts is
[`ContractFramework.lua`](register-and-lifecycle)'s job.

## The four-function adapter — the only thing wired together

The board never touches the engine directly. It calls exactly four functions, each of which tries a couple
of likely names first so a draft framework can often "just work" without any changes to the board itself:

| Function | Contract:  | Purpose |
|---|---|---|
| `API.list()` | `Contract.All()` | Array of registered contract definitions. Returns `nil` to fall into demo mode. |
| `API.accept(c)` | `Contract.Accept(c.id)` | Start contract `c`. Returns `true` on success. |
| `API.cancel(c)` | `Contract.Abort()` | Abort the running contract. |
| `API.status()` | `Contract.Status()` | Live state: `{% raw %}{ finished=, progress=, timeLeft=, objectives={ {done=}, ... } }{% endraw %}`. |

This is exactly the [`Contract.Register & Lifecycle`](register-and-lifecycle) surface — `Contract.All` is
literally aliased to `Contract.List` for this reason (`C.All = C.List`, with a comment noting it's "the GFx
board's preferred detection name").

## Demo mode

If `API.list()` comes back `nil` (no framework loaded, or `Contract.All` doesn't exist yet), the board
switches to **demo mode**: three built-in fake contracts, and `API.status()` simulates one objective
completing roughly every 4 seconds. This means the entire UI — browsing, categories, accepting, the
tracker widgets, the completion flow — can be built and tested standalone, before `ContractFramework.lua`
is even wired up.

## Browse → accept → active → confirm

The board is a small state machine (`S.mode`):

- **`"browse"`** — the two-pane list: categories (auto-detected from whatever's registered, alpha-sorted)
  on the left, details for the current selection on the right. Accepting requires **two** Enter presses in
  a row (`S.armed`) — a deliberate guard against a stray double-tap starting the wrong contract.
- **`"active"`** — while a contract is running, reopening the board shows only the active contract with a
  cancel option, instead of the full list.
- **`"confirm"`** — pressing cancel doesn't cancel immediately; it drops into a confirm step first
  (Enter confirms, Left keeps the contract running).

## Reusable HUD widgets: `Contract.UI.Panel` / `Contract.UI.Bar`

Two chainable widget constructors, defined at file scope so they exist even before the board's own hotkey
is ever pressed:

```lua
local panel = Contract.UI.Panel{ x = 12, y = 24, title = "Convoy Protection" }
panel:line(0, "[ ] Reach the checkpoint"):line(1, "[x] Board the escort vehicle")

local bar = Contract.UI.Bar{ x = 20, y = 330, label = "Progress" }
bar:set(0.6)   -- 0..1
```

`Panel` gives you `:title(s)` / `:line(i, s)` (8 lines, `i` = 0..7) / `:clear()` / `:show()` / `:hide()` /
`:destroy()`; `Bar` gives you `:set(v)` (0..1) / `:label(s)` / `:show()` / `:hide()` / `:destroy()`. Both
are thin wrappers over a `MrxGuiBase.FlashWidget` (`cpanel.gfx` / `cbar.gfx`) — modders never touch
Scaleform directly.

## The tracker

While a contract is active, a `Contract.UI.Panel` tracker stays up **even with the board closed** — one
line per objective, `[x]`/`[ ]` checkboxes, the title showing `done/total` and time remaining. It's built
and torn down by the board itself (`tracker_up`/`tracker_update`/`tracker_destroy`), driven by polling
`API.status()` roughly 5 times a second.

## Finishing in sync with the native fanfare

`ContractFramework.lua`'s own completion path calls `C.onFinish(result)` the instant a contract ends — the
board wires exactly this hook:

```lua
if _G.Contract then _G.Contract.onFinish = finish_teardown end
```

This tears the tracker down **instantly, with no lingering message of its own** — the native completion
fanfare ([Support Effects & Triggers: Fanfare](support-effects-and-triggers#fanfare)) is the intended
completion cue, so the board deliberately doesn't show a second, competing one. `status_tick`'s own
`finished` check calls the same teardown as a fallback, for cases (like demo mode) where there's no real
framework to call the hook at all.

## Performance: the same input pattern as MissionForge

The board's own comments call this out explicitly as a measured fix, not a guess: per-key
`Loader.IsKeyDown` polling for every nav key was "the framerate hit with the board open." The fix is the
same idiom [MissionForge](mission-forge) and [ForgeCam](../deep-dives/forgecam) both converged on
independently — one `Loader.PopKeyEvents()` ring-buffer drain per tick for discrete presses (Up/Down/Left/
Right/Enter), plus a single `Loader.GetKeyboardState()` snapshot for Up/Down's hold-to-repeat behavior.

## A documented async-loading bug

`SetSwfFile` (the call that loads a `.gfx` movie into a `FlashWidget`) is asynchronous. The board's own
comments record a real bug this caused: calling `refresh()` immediately after `build()` fired before the
movie had actually finished loading, and the call was silently dropped — the symptom was a board that
"needs an input before it populates." The fix is to re-push `refresh()` again shortly after
(`Event.Create(Event.TimerRelative, {0.15}, ...)` and again at `0.40`), so the board populates correctly
even if the first attempt was too early.

## Deploying

```
scripts/OnKey/contracts.lua
```

`KEYVAL` (`"f5"`) auto-binds — no `lua_loader.ini` entry needed. Requires `contracts.gfx`, `cpanel.gfx`,
and `cbar.gfx` alongside it (the Scaleform movies, built via the same
[gfxforge / gfx_tool pipeline](../deep-dives/custom-ui) as every other custom UI on this wiki).

## See also

- [Contract.Register & Lifecycle](register-and-lifecycle) — `Contract.All`/`Accept`/`Abort`/`Status`, the
  other side of the four-function adapter.
- [Custom UI — Authoring Scaleform Movies](../deep-dives/custom-ui) — the `.gfx` authoring pipeline behind
  `contracts.gfx`/`cpanel.gfx`/`cbar.gfx`.
- [MissionForge](mission-forge) / [ForgeCam](../deep-dives/forgecam) — the same ring-buffer input pattern,
  arrived at independently in two other tools.
