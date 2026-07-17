---
title: Ess.UI
parent: Essentials (Ess)
nav_order: 6
---

# Ess.UI

## Overview

This page covers `Ess.Gfx` (the raw FlashWidget primitives), `Ess.ScrollLog`, and `Ess.UI` — the native
`Ess` port of **[UI Kit](../uilib/)** (`uilib.lua`'s `_G.UI`), absorbed as a full source port rather than an
alias to an external `uilib.lua` deployment. Same nine widgets, same shared input/focus/heartbeat engine,
same declarative `UI.Menu` builder — `Ess.UI.VERSION` is `"1.0"`, labelled in the source itself as "Ess's
port of uilib v2.2." Where the port is a faithful, line-for-line carry-over this page says so and links back
to [UI Kit](../uilib/) for the full design reasoning instead of re-deriving it; where the native port
genuinely behaves differently, it's called out explicitly, widget by widget, and summarized below.

Fits into [the three tiers](index#the-three-tiers) like this: `Ess.Gfx` **is** the Raw tier for widget
work — the primitives every one of `uilib.lua`, `contracts.lua`, ForgeCam, and ForgeMenu used to hand-roll
separately around `MrxGuiBase.FlashWidget`. `Ess.UI` is the Core tier — already fairly friendly, so most UI
work doesn't need an Easy tier at all. The thin `Ess.Easy` slice on top covers only the handful of
single-call cases that don't need a widget object (see [below](#ess-easy-ui-helpers)).

**Deploy:** the `.gfx` movies every `Ess.UI` widget needs ship in `data/vz-patch.wad`, part of the normal
[Ess install](index#install) — nothing extra to inject beyond what installing `Ess` already requires.

## The nine widgets

| Widget | What it is |
|---|---|
| [`Ess.UI.Menu`](#ess-ui-menu) | A ForgeMenu-style declarative drill-down: `:entry`/`:category`/`:header`/`:switch`, nests as deep as you like. |
| [`Ess.UI.List`](#ess-ui-list) | The raw scrolling list every other multi-row widget here is built on — 10 visible rows, section headers, a scrollbar, auto-resize. |
| [`Ess.UI.Panel`](#ess-ui-panel) | A title bar plus up to 8 lines, body auto-resizing to fit. |
| [`Ess.UI.Bar`](#ess-ui-bar) | A label plus a progress bar. |
| [`Ess.UI.Toast`](#ess-ui-toast) | A transient notification, 3 stacked slots, auto-hiding. |
| [`Ess.UI.Confirm`](#ess-ui-confirm) | A modal yes/no dialog. |
| [`Ess.UI.Input`](#ess-ui-input) | A one-shot typed prompt. |
| [`Ess.UI.Chat`](#ess-ui-chat) | A scrolling message log with an optional typed input line. |
| [`Ess.UI.Board`](#ess-ui-board) | A two-pane list-plus-details view, driving `contracts.gfx` — the same widget [`Ess.Contract`](contract)'s own board UI (contract selection, intermission shops) is built on. |

Every widget shares `:show()` `:hide()` `:focus()` `:blur()` `:destroy()` — chainable, identical regardless
of which widget you're holding. Exactly one widget hears keys at a time (`Ess.UI.Focus(w)`/
`Ess.UI.Focused()`), the heartbeat idles itself when nothing needs it, and every widget re-sends its state
for `Ess.UI._WARMUP` (8) ticks after showing to survive the movie's async load. All of that plumbing is the
same design [UI Kit](../uilib/#why-one-shared-engine-instead-of-nine-separate-ones) documents in depth —
rebuilt here on `Ess.Gfx`/`Ess.Loop`/`Ess.Input`/`Ess.Time.clock`/`Ess.Player.pose` instead of `uilib.lua`'s
own private copies of the same mechanisms, not a hand-copy of them. `Ess.UI.wrap(s, width)`, `Ess.UI.comma(n)`,
`Ess.UI.fmt_time(sec)`, and the remappable `Ess.UI.KEYS` table (`up`/`down`/`left`/`right`/`enter`/`esc`,
same VK defaults) all carry over unchanged.

## Where the native port genuinely differs

Confirmed by reading both source trees side by side (`uilib.lua`'s full text is reproduced on
[uilib.lua](../uilib/source); `Ess.UI` lives in `src/42_ui_engine.lua` through `src/49_ui_menu.lua` plus
`src/54_ui_chat.lua`/`src/55_ui_board.lua`). Most of the kit is a byte-for-byte logic carry-over — `Menu`,
`Confirm`, `Panel`, and `Bar` are identical apart from swapped globals (`UI`→`Ess.UI`, `Loader.Printf`→
`Ess.Log`). A few pieces are not:

- **Held Up/Down now auto-repeats.** The shared heartbeat (`src/42_ui_engine.lua`) added a held-key
  auto-repeat for the scroll axis: after `Ess.UI.REPEAT_DELAY` (0.35s) of holding Up or Down, it re-fires
  `_keyvk` every `Ess.UI.REPEAT_RATE` (0.06s) until released, like an OS text-cursor repeat. Only Up/Down
  repeat — Enter/Esc/Left/Right stay single-shot on purpose, so a stuck key can't machine-gun a "pick"/"back"
  action. `uilib.lua` had no such repeat at all: every move required a fresh discrete key-down edge from
  `Loader.PopKeyEvents()`. This applies to *whatever widget currently has focus and defines `_keyvk`* — List,
  Menu, and Board's scrolling all get it; so, incidentally, does Confirm's Left/Right/Up/Down toggle, since
  Confirm's own `_keyvk` treats all four the same way.
- **`Ess.UI.List` (and therefore `Ess.UI.Menu`, built on it) now wraps at the ends.** Pressing Down on the
  last selectable row jumps to the first; Up on the first jumps to the last (headers are skipped correctly
  either way). `uilib.lua`'s list simply stopped — `nearest()` returned `nil` past either end and the
  keypress did nothing. See [`Ess.UI.List`](#ess-ui-list) below for the exact source line.
- **`Ess.UI.Board` was *not* given the same fix.** Its own copy of the up/down nav logic (`src/55_ui_board.lua`)
  is otherwise a near-exact copy of List's, but it still stops at the ends — no wraparound. That makes List/
  Menu and Board behave differently from each other inside `Ess.UI` itself, which `uilib.lua` never did
  (neither widget wrapped there).
- **`Ess.UI.Chat` gained an opt-in `autoHide` option** (`opts.autoHide = seconds`) with no equivalent in
  `uilib.lua`'s `UI.Chat` at all. See [`Ess.UI.Chat`](#ess-ui-chat).
- **`Ess.UI.Toast`'s default footprint shrank and moved.** `uilib.lua` hardcoded a 320×44 toast with a 50px
  vertical gap between stacked slots. `Ess.UI` makes all of that configurable (`Ess.UI.TOAST_W/H/GAP/X/Y`)
  but ships smaller defaults: 160×22 with a 25px gap. See [`Ess.UI.Toast`](#ess-ui-toast) for what stayed the
  same (the text-wrap width) despite the box shrinking.
- **Widget visibility at construction is genuinely ambiguous — flagging this for a live check rather than
  guessing.** `uilib.lua`'s private `make_widget` unconditionally called `wg:SetVisible(true)` as its last
  step, so every widget was visible in the engine's own terms the instant it was built. `Ess.Gfx.widget`
  (the constructor every `Ess.UI` widget now calls) does **not** call `SetVisible` at all — it returns
  `{ raw = wg, shown = false }` and leaves the native visibility flag exactly as `FlashWidget:new()` set it.
  `Ess.UI.Confirm`, `Ess.UI.Input`, and `Ess.UI.Toast` all compensate by calling `:show()` (or
  `Ess.Gfx.setVisible(..., true)` directly, for Toast) explicitly in their own constructors — those three
  are unaffected. **`Ess.UI.List`, `Panel`, `Bar`, `Chat`, and `Board` do not call `:show()` in their
  constructors**, exactly matching `uilib.lua`'s own code shape (which didn't need to, since `make_widget`
  already showed it). Built through [`Ess.UI.Menu`](#ess-ui-menu) — which explicitly calls
  `rt.list:show():focus()` in `:open()` — this never surfaces. Built directly (the exact pattern
  [UI Kit's own `UI.List`/`UI.Panel` recipes](../uilib/list) use, with no `:show()` call at all), whether the
  widget actually renders depends on `FlashWidget:new()`'s own default visibility, which isn't confirmed from
  source alone. Worth a quick live check before relying on a bare `Ess.UI.List{...}`/`Ess.UI.Panel{...}` to
  appear without an explicit `:show()`.

Everything else below — `Menu`'s builder and `ctx:` surface, `Confirm`'s default-to-NO safety rule, `Input`'s
US-layout typing, `Panel`/`Bar`'s auto-resize, `Board`'s two-pane shape — carries over unchanged; see
[UI Kit](../uilib/) for why each of those works the way it does.

## Ess.Gfx

The Raw tier: the FlashWidget boilerplate every one of `uilib.lua`, `contracts.lua`, ForgeCam, and ForgeMenu
used to hand-roll independently. `Ess.UI`'s own widgets are all built on this — but so can yours, for a
custom movie the kit doesn't cover. `samples/OnKey/MissionForge.lua` does exactly that: it drives `forge.gfx`
directly through `Ess.Gfx.widget`/`.call`/`.setVisible`, entirely outside `Ess.UI`.

| Function | Signature | Notes |
|---|---|---|
| `widget` | `Ess.Gfx.widget(file, x, y, w, h) -> widget \| nil` | Builds, positions, and adds a `FlashWidget` from a deployed `.gfx` asset. Returns `{ raw = <FlashWidget>, shown = false }`, or `nil` (logged) if construction fails. Does the corner-coordinate `SetLocation` math (`x, y, x+w, y+h`) once, centrally — the same bug [UI Kit](../uilib/panel-bar-toast#the-real-bug-behind-all-three-setlocation-takes-corners-not-a-size) documents (`SetLocation` wants absolute corners, not a width/height offset) is structurally impossible to get wrong again once every widget goes through this one constructor. Does **not** call `SetVisible` — see the [visibility caveat above](#where-the-native-port-genuinely-differs). |
| `call` | `Ess.Gfx.call(widget, fn, args) -> ok` | `pcall`-wrapped `CallActionScriptCallback(fn, args)`. `args` defaults to `{}`. |
| `onEvent` | `Ess.Gfx.onEvent(widget, name, cb) -> ok` | `pcall`-wrapped `SetFlashEventHandler`. The native shape needs a mandatory `(_, v)` two-arg callback plus a mandatory trailing `{}` third argument to the call itself — both easy to get subtly wrong by hand. This hides both; your `cb` just receives `v`. |
| `setVisible` | `Ess.Gfx.setVisible(widget, bool)` | Works around a confirmed real bug: the getter is `GetVisible()` (not `IsVisible()`, which silently nil-calls), and it returns `1`/`0` — `not 0` is `false` in Lua, so a naive `SetVisible(not w:GetVisible())` toggle never flips. This never reads the getter back; it tracks its own `widget.shown` boolean. |
| `warmupRerender` | `Ess.Gfx.warmupRerender(rt, ticks = 8)` | Re-runs a zero-arg repaint thunk `rt` every 0.05s for `ticks` ticks, so at least one repaint lands after `SetSwfFile`'s async movie load actually finishes. The same `WARMUP = 8` idea baked into `Ess.UI`'s own engine (`Ess.UI._WARMUP`), exposed standalone for custom widgets built directly on `Ess.Gfx`. |
| `menuNav` | `Ess.Gfx.menuNav(widget, keys) -> stop()` | Polls `Ess.Input` for up/down/enter (default VK_UP/VK_DOWN/VK_RETURN, matching `Ess.UI.KEYS` if remapped) and forwards `Move`/`Choose` calls into a movie's own compiled AS2 menu logic — a HUD `FlashWidget` gets no native input of its own. Built on `Ess.Input.poll` (edge-triggered), not a raw per-key `IsKeyDown` loop. Returns a `stop()` function. |

## Ess.UI.Menu

```lua
local menu = Ess.UI.Menu{ title = "MY MENU", key = "F8" }

menu:entry("Do a thing", function(ctx) ctx:hint("done") end)

menu:category("Spawns", function(c)
    c:entry("Tank", function(ctx) ctx:spawn("M1A2 (Full)", 8) end)
end)

menu:toggle()   -- put this at the very end of your OnKey file
```

**`Ess.UI.Menu(opts)`** (or a bare string, treated as `title`): `title`, `id` (defaults to `title`), `key`
(toggle key, display only), `x`/`y` (default `40, 60`), `onClose`.

| Call | Adds / does |
|---|---|
| `:entry(label, action)` | A leaf. `action` is `function(ctx) ... end`. |
| `:category(label, buildFn)` | A submenu; `buildFn` receives a child builder, nests freely, also returned. |
| `:header(text)` | A non-selectable section divider. |
| `:switch(label, get, set)` | A ready-made ON/OFF toggle entry: renders `"<label>: ON/OFF"` from `get()`, calls `set(newBool, ctx)` when picked. |
| `:toggle()` / `:open()` / `:close()` / `:isOpen()` | Lifecycle. |

`ctx` (passed to every action): `x`/`y`/`z`/`yaw`, `char`/`player` (from `Ess.Player.pose(0)`, the promoted
form of `uilib.lua`'s private `pose()` — see [Core Primitives](core)/[Identity & World Query](identity-query)),
plus `:hint(msg)`/`:toast(msg)` (pop an `Ess.UI.Toast`), `:print(msg)` (via `Ess.Log`), `:close()`,
`:confirm(text, onYes, onNo)`, `:ask(prompt, onSubmit, onCancel)`, and `:spawn(template, dist?)`.

**Byte-for-byte port**, confirmed by direct diff against `uilib.lua`'s `UI.Menu` (`src/49_ui_menu.lua` vs.
[uilib.lua's source](../uilib/source)): identical tree-builder, identical `_choose`/`_back`/`open`/`close`
logic, identical dynamic-label re-paint-and-restore-cursor behavior, identical one-menu-open-at-a-time rule
via `S.openId`, identical persistent-per-`id` runtime state so `:toggle()` really toggles without leaking a
list. `ctx:spawn`'s blank-template crash guard (`Pg.Spawn("")` is a native crash `pcall` can't catch) carries
over unchanged too. `FEATURE_SHEET.md` calls this out directly: "`Ess.UI.Menu`'s builder/`ctx:` surface is
byte-for-byte backward compatible with `uilib`'s own — live-tested against the real `ExampleMenu.lua` shape."

The one behavioral change is inherited, not local to this file: because `Menu` is one owned
[`Ess.UI.List`](#ess-ui-list), it picks up List's new wraparound cursor for free (Down past the last entry
jumps to the top). See [UI.Menu](../uilib/menu) for the full design writeup — the tree-to-list translation,
the "why this is the one thing `UI.Menu` can do that plain ForgeMenu can't" composition story, and the
`ctx:spawn` crash-guard history.

## Ess.UI.List

```lua
local list = Ess.UI.List{
    x = 40, y = 60, title = "PICK ONE",
    items = { { header = "SECTION A" }, { label = "First", any = 1 } },
    onChoose = function(item, i, list) Ess.Log("picked " .. tostring(item.any)) end,
    onBack   = function(list) list:hide() end,
}
```

**`Ess.UI.List(opts)`**: `x`/`y` (default `40, 60`), `w`/`h` (default `320, 360`), `title`, `crumb`, `hint`,
`items`, `empty` (default `"EMPTY"`), `focus`, plus `onSelect`/`onChoose`/`onBack`.

| Call | Signature | Notes |
|---|---|---|
| `:items(t)` | `items(t) -> self` | Flat array of headers (`{header="TEXT"}`) and rows (`{label=..., ...}`). 10 rows visible; more scrolls. |
| `:selected()` | `selected() -> item, i` | |
| `:select(i)` | `select(i) -> self` | No-op if `i` isn't selectable. |
| `:paint()` | `paint() -> self` | Re-sends rows/scrollbar/size to the movie; called internally by `:items()`. |
| `:title(s)` / `:crumb(s)` / `:hint(s)` | `-> self` | Update the movie immediately, chainable. |

Callbacks: `onSelect(item, i, list)` on every cursor move, `onChoose(item, i, list)` on Enter/Right,
`onBack(list)` on Left/Esc. Body auto-resize (eases toward `100*(24*shown_rows+12)/296`) is unchanged from
`uilib.lua`.

**Confirmed difference: the cursor now wraps.** `src/43_ui_list.lua`'s `_keyvk`:

```lua
local t = nearest(o._sel + d, d)
-- rolled off an end -> wrap around to the other end
if not t then t = (d == 1) and nearest(1, 1) or nearest(#o._items, -1) end
```

Down past the last selectable row jumps to the first; Up past the first jumps to the last (headers are
skipped correctly in both directions). `uilib.lua`'s `UI.List` had no such fallback — `nearest()` returning
`nil` at either end just left the keypress a no-op. Since [`Ess.UI.Menu`](#ess-ui-menu) is one owned
`Ess.UI.List`, every drill-down menu wraps too, which `uilib.lua`'s `UI.Menu` never did.
[`Ess.UI.Board`](#ess-ui-board)'s separate copy of this same nav logic was **not** updated the same way — see
[Where the native port genuinely differs](#where-the-native-port-genuinely-differs).

Also carries the [construction-time visibility caveat](#where-the-native-port-genuinely-differs): no
`:show()` call happens inside the constructor, unlike `uilib.lua`'s `make_widget`, which showed every widget
unconditionally. See [UI.List](../uilib/list) for the full drill-down-without-`UI.Menu` recipe and the
scrollbar/auto-resize math.

## Ess.UI.Panel

```lua
local p = Ess.UI.Panel{ x = 20, y = 120, title = "STATUS" }
p:line(0, "Health: 100")
```

**`Ess.UI.Panel(opts)`**: `x`/`y` (default `20, 120`), `w`/`h` (default `300, 200`), `title`, `lines`
(pre-sized slot count, default `0`).

| Call | Notes |
|---|---|
| `:title(s)` | Sets the header. |
| `:line(i, s)` | Sets line `i` (0-indexed, 0–7). A non-empty line past the current `:fit()` count auto-grows it. |
| `:fit(n)` | Explicitly sets visible line count (clamped 0–8), eases the body height toward it. |
| `:clear()` | Blanks all 8 lines, fits back to 0. |

No behavioral difference found — `src/44_ui_panel.lua`'s logic (including the `panel_px(n) = 40 + 18*n`
sizing formula) is identical to `uilib.lua`'s `UI.Panel`. Same [construction-time visibility
caveat](#where-the-native-port-genuinely-differs) as List/Bar/Chat/Board. See [UI.Panel](../uilib/panel-bar-toast)
for the rolling-event-log recipe.

## Ess.UI.Bar

```lua
local b = Ess.UI.Bar{ x = 20, y = 330, label = "Loading" }
b:set(0.4)
```

**`Ess.UI.Bar(opts)`**: `x`/`y` (default `20, 330`), `w`/`h` (default `300, 36`), `label`, `value` (initial
`0..1`, default `0`).

| Call | Notes |
|---|---|
| `:set(v)` | Clamps `0..1`, sends as a whole-number percent. |
| `:label(s)` | Updates the text. |

No behavioral difference found — identical logic to `uilib.lua`'s `UI.Bar`. See
[UI.Bar](../uilib/panel-bar-toast) for context.

## Ess.UI.Toast

```lua
Ess.UI.Toast("Wardrobe Unlocked!")
Ess.UI.Toast("Something urgent", { ttl = 8 })
```

A function, not a constructor — finds a free slot (or steals the soonest-expiring one once all
`Ess.UI.TOAST_SLOTS` are busy, default `3`), wraps the text, shows it, and starts its countdown. Returns the
underlying toast object (`:dismiss()` clears it early), but most calls are fire-and-forget.

**Confirmed difference: the default toast box shrank and moved.**

| Constant | `uilib.lua` (hardcoded) | `Ess.UI` (overridable global) |
|---|---|---|
| Box size | 320×44 | `Ess.UI.TOAST_W` = 160 × `Ess.UI.TOAST_H` = 22 |
| Slot gap | 50px | `Ess.UI.TOAST_GAP` = 25px |
| X (right-aligned) | `640 - 320 - 8` = 312 | `Ess.UI.TOAST_X` = `640 - TOAST_W - 8` = 472 |
| Y | 150 | `Ess.UI.TOAST_Y` = 150 (unchanged) |

The text-wrap width passed to `Ess.UI.wrap(text, 46)` is **unchanged** — still 46 characters per line, the
same value `uilib.lua` used for its larger 320-wide box. All four constants above are ordinary overridable
`Ess.UI.*` globals if the smaller default doesn't fit your `ui_toast.gfx` skin. Everything else — the
steal-the-soonest-expiring-slot logic, the `Ess.UI.TOAST_TTL` (default 4s) countdown, `:dismiss()` — is
unchanged. See [UI.Toast](../uilib/panel-bar-toast#ui-toast-a-transient-notification) for the stacking
behavior.

## Ess.UI.Confirm

```lua
Ess.UI.Confirm{
    text = "Delete this save slot?",
    onResult = function(yes) if yes then DoDelete() end end,
}
```

**`Ess.UI.Confirm(opts)`**: `text`, `title` (default `"CONFIRM"`), `yes`/`no` (default `"YES"`/`"NO"`),
`onResult` — called exactly once with a plain boolean. A **singleton**: calling it again while one's open
reconfigures and re-shows the same widget.

Left/Right/Up/Down flip the highlighted choice, Enter commits, **Esc always resolves `false`** regardless of
what's highlighted, and the highlight **defaults to NO**. Remembers whatever was focused before it and
restores that focus once resolved.

**Byte-for-byte port** — `src/47_ui_confirm.lua` is identical logic to `uilib.lua`'s `UI.Confirm`, only the
globals swapped. Unlike List/Panel/Bar/Chat/Board, `Confirm` explicitly calls `:show()`/`:focus()` in its own
constructor, so it's unaffected by the [construction-time visibility
caveat](#where-the-native-port-genuinely-differs). One inherited change worth knowing: since Left/Right/
Up/Down are all treated identically by Confirm's `_keyvk`, the engine's new [held-key
auto-repeat](#where-the-native-port-genuinely-differs) means holding any of the four now keeps flipping the
highlighted choice every `Ess.UI.REPEAT_RATE` seconds — `uilib.lua` required a fresh key-down edge per flip.
See [UI.Confirm](../uilib/confirm-and-input) for the "escape never accidentally confirms" reasoning.

## Ess.UI.Input

```lua
Ess.UI.Input{
    prompt = "ENTER A NAME",
    onSubmit = function(text) Ess.Log("got: " .. text) end,
    onCancel = function() Ess.Log("cancelled") end,
}
```

**`Ess.UI.Input(opts)`**: `prompt` (default `"INPUT -- ENTER SUBMIT   ESC CANCEL"`), `text` (default `""`),
`max` (default `120`), `onSubmit(text)`, `onCancel()`. A **singleton**, same as `Confirm`.

Enter submits, Esc cancels and discards, Backspace deletes one character. Long entries truncate from the
front past ~40 characters (`"..." .. tail`). Same focus-save/restore as `Confirm`; explicitly calls
`:show()`/`:focus()` in its own constructor, so also unaffected by the visibility caveat.

**Logic is byte-for-byte identical to `uilib.lua`'s `UI.Input`.** The one implementation change: character
typing goes through the now-shared `Ess.Input.VkToChar(vk, shift)` instead of `uilib.lua`'s own private
`CHAR` table — per `src/48_ui_input.lua`'s header comment and [Timing & Input](timing-input#ess-input), it's
the same table, "ported byte-for-byte from uilib's `CHAR` table," still US-layout-only (edit `Ess.Input`'s
`PUNCT` for other layouts). See [UI.Input](../uilib/confirm-and-input#typed-character-mapping) for the full
VK-mapping table.

## Ess.UI.Chat

```lua
local ch = Ess.UI.Chat{ title = "RADIO", x = 640 - 360 - 8, y = 8 }
ch:push("Misha: slick menu, boss.")
ch:prompt(function(text) Ess.Log("you said: " .. text) end)
```

**`Ess.UI.Chat(opts)`**: `x`/`y` (default `20, 400`), `w`/`h` (default `360, 132`), `title`, `max`
(scrollback cap, default `60`), `onSubmit`, and the new **`autoHide`** (see below). Drives `chat.gfx`.

| Call | Notes |
|---|---|
| `:push(text)` | Word-wraps (52 chars, `Ess.UI.wrap`) and appends; trims oldest past `max`. Only the last 5 lines show at once; body auto-resizes to fit. |
| `:prompt([onSubmit])` | Enters typed-input mode; Enter pushes the text and fires `onSubmit`, Esc cancels. |
| `:title(s)` / `:clear()` | |

**Confirmed new feature, no `uilib.lua` equivalent: `opts.autoHide = seconds`.** Auto-hides the window that
many seconds after the last `:push()`. Per `src/54_ui_chat.lua` and the shared heartbeat's `o._hideIn`
handling in `src/42_ui_engine.lua`: the countdown is **frozen while the widget holds input focus** (it never
fades out mid-type) and re-arms — resurfacing the window if it had faded — on every new `:push()`. Omit it
for the old always-visible behavior. Confirmed real usage, `samples/OnKey/CoopChat.lua`:

```lua
C.ui = Ess.UI.Chat{ x = 20, y = 330, w = 384, title = "CO-OP CHAT", onSubmit = onSubmit, autoHide = 10 }
```

The underlying `_hideIn`/`_autoHide` mechanism in the shared heartbeat is generic to any widget in `S.live`,
but `Ess.UI.Chat` is the only constructor that currently exposes it as an option. Everything else — the
5-line visible window, the `CHAR`-table-driven prompt (now `Ess.Input.VkToChar`, same swap as `Ess.UI.Input`)
— is unchanged. Also has the [construction-time visibility caveat](#where-the-native-port-genuinely-differs).
**Not related to** the [Co-op Text Chat](../deep-dives/coop-chat) deep dive's `MrxGuiTextBuffer`-based
network chat — see [UI.Chat](../uilib/chat-and-board#ui-chat-a-scrolling-log-with-an-optional-typed-line)
for that distinction.

## Ess.UI.Board

```lua
local b = Ess.UI.Board{
    title = "CONTRACTS", hint = "UP/DOWN BROWSE   ESC CLOSE", focus = true,
    items = { { header = "AVAILABLE" }, { label = "Oil Refinery Raid", k = 1 } },
    onSelect = function(it, i, board)
        if it.k == 1 then
            board:detail{ category = "DESTRUCTION", rewards = { "$8,000" },
                objectives = { "Destroy 4 storage tanks" }, progress = 0, progressText = "NOT STARTED" }
        end
    end,
    onChoose = function(it, i, board) Ess.UI.Toast("Accepted: " .. it.label) end,
    onBack   = function(board) board:hide() end,
}
```

**`Ess.UI.Board(opts)`**: same shape as [`Ess.UI.List`](#ess-ui-list) (`x`/`y`/`w`/`h`, `title`, `hint`,
`items`, `empty`, `focus`) plus `detail` (initial payload). Drives `contracts.gfx` — and per
`src/55_ui_board.lua`'s own header comment, [`Ess.Contract`](contract)'s own board UI (the contract
selection screen, intermission shops, etc) is **built on this widget directly**, not a separate hand-rolled
UI reusing the same movie file.

| Call | Notes |
|---|---|
| `:items(t)` / `:selected()` / `:select(i)` / `:title(s)` / `:hint(s)` | Identical to `Ess.UI.List`. `:items()` also fires `onSelect` immediately, so the detail pane is populated the instant the board opens. |
| `:detail(d)` | `{ category=, rewards={} (up to 4), objectives={} (up to 8), progress=0..1, progressText= }`. |

**Confirmed *not* to have received `Ess.UI.List`'s wraparound fix.** `src/55_ui_board.lua`'s `_keyvk` up/down
handling is otherwise a close copy of List's selection/scrolling logic (same `nearest()`/`selectable()`
shape, same scrollbar-thumb math against its own `TRK_Y`/`TRK_H` constants) but keeps the old stop-at-the-end
behavior — `local t = nearest(o._sel + d, d); if t and t ~= o._sel then ...` with no wrap fallback. This
matches `uilib.lua`'s `UI.Board` exactly (neither version ever wrapped there); it's only a difference
*within* `Ess.UI` itself, between Board and List/Menu. Everything else — the two-pane shape, the `SetCat`/
`SetReward`/`SetObj`/`SetBar`/`SetProg` calls in `:detail()` — is byte-for-byte identical to `uilib.lua`'s
`UI.Board`. Has the [construction-time visibility caveat](#where-the-native-port-genuinely-differs) too. See
[UI.Board](../uilib/chat-and-board) for the full shape and the `menudemo.lua` three-item usage pattern.

## Ess.ScrollLog

A scrolling on-screen text buffer via the one confirmed bug-free construction path for
`MrxGuiTextBuffer` — unrelated to the `Ess.UI` engine above (no shared focus/heartbeat, no `:show()`/`:hide()`/
`:focus()`/`:blur()`/`:destroy()` common surface).

```lua
local log = Ess.ScrollLog.new("MyLog", 20, 150, 340, 220)
log:add("Something happened")
```

| Function | Signature | Notes |
|---|---|---|
| `new` | `Ess.ScrollLog.new(name, x, y, w, h) -> scrollLog \| nil` | `name` is a reuse key: calling again with the same name returns the **same instance**, so two callers can't collide on one overlapping box. `x`/`y`/`w`/`h` default `20, 150, 340, 220`. |
| `:add` | `add(msg, duration = 1)` | Shows the box and queues `msg`. `duration` defaults to a deliberately short 1s. |
| `:setVisible` | `setVisible(bool)` | |
| `:clearAll` | `clearAll()` | |

**Confirmed shipped engine bug this works around:** the documented constructor,
`MrxGuiTextBuffer.InstantiateTextBuffer`, references a global `oWidget` that doesn't exist anywhere in its
own scope — calling it throws and crashes the caller. Patching it from outside doesn't work either (the
patched copy can't resolve the module's own private internal calls). The confirmed-working path instead
calls the never-broken `HandleInstantiationEventForTextBuffer(oWidget, tEvent)` directly on a hand-built
widget named exactly `"MessageBox"` (the string that flips on the translucent chat-box backdrop). This ~30-line
workaround was previously duplicated near-verbatim between two other hand-rolled implementations; now it's
one library.

**Confirmed real bug this also fixes:** `duration × message count` is real queued wall-clock time — each
message occupies the box for its own duration before the next can show. `:add`'s 1s default (shorter than
the native `AddMessage`'s own longer default) exists specifically so a bulk dump can't silently queue up
tens of minutes of messages the way an earlier, unguarded version once did.

## Ess.Easy UI helpers

The thin `Ess.Easy` slice over `Ess.UI` — single-call cases that don't need a widget object. Full depth,
including `Ess.Easy.Console`, lives on the [Ess.Easy](easy) page; this is just the pointer:

| Call | Does |
|---|---|
| `Ess.Easy.Toast(msg)` | `Ess.UI.Toast(tostring(msg))`. |
| `Ess.Easy.Confirm(text, onYes, onNo)` | Positional-callback wrapper over `Ess.UI.Confirm`; `onNo` optional. |
| `Ess.Easy.Menu(title, entries)` | Opens immediately, one **flat** level — no `:category` nesting or `:switch`. `entries` accepts an ordered `{ {label, fn}, ... }` array or a `{ [label] = fn }` map. Use `Ess.UI.Menu` directly for the full nested builder. |
| `Ess.Easy.Console.open()` | Browses the whole `Ess.Easy.*` surface in-game, searchable — built on [`Ess.UI.Board`](#ess-ui-board) for the list+detail view and `Ess.TextConsole` for the search box. |

See [Ess.Easy](easy) for the complete one-liner catalog.

## See also

- [Essentials (Ess)](index) — the framework index this page belongs to.
- [UI Kit](../uilib/) — the standalone predecessor `Ess.UI` is a native port of; the design reasoning behind
  the shared engine (input/focus/heartbeat/warm-up) lives there, not repeated here.
- [Ess.Easy](easy) — the full beginner-tier one-liner catalog, including `Ess.Easy.Console`'s complete
  registry.
- [Timing & Input](timing-input) — `Ess.Input`/`Ess.Loop`/`Ess.Time.clock`, the primitives `Ess.UI`'s engine
  is built on; `Ess.TextConsole`, the `.gfx`-free alternative to `Ess.UI.Input`.
- [Contract Engine](contract) — `Ess.Contract`'s own board UI (contract selection, intermission shops) is
  built directly on `Ess.UI.Board`, not a second independent driver of the same movie.
