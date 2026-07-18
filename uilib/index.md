---
title: UI Kit
parent: Deprecated Frameworks
nav_order: 2
has_children: true
has_toc: false
---

# UI Kit

> **Deprecated — superseded by [Essentials (Ess)](../ess/).** `uilib.lua` is absorbed there as native
> `Ess.UI` — the same nine widgets, the same backward-compatible menu builder — shipped in one drop-in
> `1_Ess.lua`. This page stays as historical reference for the standalone predecessor; new mods should
> build on Ess.

> **Status: new, already iterated once.** Not a first draft — the header comment documents a full v1→v2
> rewrite ("v1 drove input with an always-on 33Hz `IsKeyDown` poll + focus model that misbehaved in-game")
> plus two further point-fixes for real bugs (a `SetLocation` corner-coords mistake that made toasts and
> dialogs render as "a giant smear," and a `UI.Menu` toggle that used to leak state). Treat the code as
> current and reasoned-through; it hasn't yet accumulated the kind of extended live-test history this
> wiki's "confirmed working" banners are reserved for.

`uilib.lua` (`_G.UI`) is a reusable widget kit — nine different HUD elements sharing one input/rendering
engine, so a modder building custom UI never has to solve the "widget, input, drawing, lifecycle" problem
from scratch the way [ForgeMenu](../deep-dives/forge-menu) and the
[Contract Board](../contract-framework/contract-board) each did independently. It's the direct successor to
both: the header comment says outright that its input handling, heartbeat, and warm-up repaint are built on
"the exact plumbing that made ForgeMenu rock-solid," and `UI.Board` reuses `contracts.gfx`, the identical
Scaleform movie the Contract Board drives.

## The nine widgets

| Widget | What it is |
|---|---|
| [`UI.Menu`](menu) | A ForgeMenu-style declarative drill-down: `:entry`/`:category`/`:header`/`:switch`, nests as deep as you like. |
| [`UI.List`](list) | The raw scrolling list every other multi-row widget here is built on — 10 visible rows, section headers, a scrollbar, auto-resize. |
| [`UI.Panel`](panel-bar-toast) | A title bar plus up to 8 lines, body auto-resizing to fit. |
| [`UI.Bar`](panel-bar-toast) | A label plus a progress bar. |
| [`UI.Toast`](panel-bar-toast) | A transient notification, 3 stacked slots, auto-hiding. |
| [`UI.Confirm`](confirm-and-input) | A modal yes/no dialog. |
| [`UI.Input`](confirm-and-input) | A one-shot typed prompt. |
| [`UI.Chat`](chat-and-board) | A scrolling message log with an optional typed input line. |
| [`UI.Board`](chat-and-board) | A two-pane list-plus-details view — the same shape (and the same `contracts.gfx` movie) as the [Contract Board](../contract-framework/contract-board). |

Every widget shares four calls: `:show()` `:hide()` `:focus()` `:blur()` `:destroy()` — chainable, and
identical regardless of which widget you're holding.

## Why one shared engine instead of nine separate ones

The four hard parts of any custom Scaleform widget — reading input, keeping exactly one thing focused,
running a heartbeat only while something's actually alive, and papering over the movie's async load — are
solved **once**, centrally, and every widget just plugs into it:

- **Input.** `Loader.PopKeyEvents()` (edge-triggered) drives navigation; `Loader.GetKeyboardState()` is
  read once per event batch just to check the Shift bit for typed text. See
  [lua-bridge API: Loader](../lua-bridge-api/loader) for both.
- **Focus.** Exactly one widget hears keys at a time (`UI.Focus`/`UI.Focused()`) — switching focus
  swallows any buffered keystrokes first, so whatever opened the newly-focused widget doesn't leak in as
  its first input.
- **The heartbeat idles itself.** A single `Event.TimerRelative` loop, shared by every widget, only keeps
  rescheduling while `needsTick()` is true (something focused, something mid-resize-animation, a toast
  still counting down) — with nothing active, it stops rescheduling entirely rather than ticking forever
  in the background. A generation counter (the same pattern [ForgeMenu](../deep-dives/forge-menu) already
  established) guarantees an old loop can't keep running alongside a freshly-restarted one.
- **Warm-up repaints.** `SetSwfFile` loads a movie asynchronously, so the very first paint issued right
  after creating a widget can be dropped before the movie's ready. Every widget re-sends its state
  unconditionally for `WARMUP = 8` ticks after showing, the same fix `ForgeMenu` already needed for the
  identical reason.

Read [UI.Menu](menu) or [UI.List](list) for exactly how these pieces click together in one concrete widget.

## Deploy

1. Copy `uilib.lua` to `scripts/OnLoad/` and register it with a low number so it loads before anything that
   uses it:
   ```ini
   [OnLoad]
   uilib.lua=5
   ```
2. The six `ui_*.gfx` movies (`ui_list`, `ui_panel`, `ui_bar`, `ui_toast`, `ui_confirm`, `ui_input`) plus
   `chat.gfx`/`contracts.gfx` for the two richer widgets need to already be injected in the WAD.
3. Guard any script that uses `UI` the same way every ForgeMenu-based script guards `_G.ForgeMenu`:
   ```lua
   if not (_G.UI and UI.Menu) then Loader.Printf("load uilib first"); return end
   ```

**Scripts:** see [UI Kit Scripts](scripts) for complete, ready-to-drop-in scripts built on this kit — the
two showcase scripts (split by which widgets each covers) plus [coopchat.lua](coopchat), a full co-op text
chat and the current implementation of [A Basic Co-op Text Chat](../deep-dives/coop-chat).

**Full source:** see [uilib.lua](source) for the library's complete, current source, reproduced in full.

**Pick a toggle key that isn't a navigation key** (arrows/Enter/Esc/Backspace by default) — those drive
whichever widget currently has focus while it's open, the same caution [ForgeMenu](../deep-dives/forge-menu)
calls out for the same reason.

## See also

- [Building ForgeMenu](../deep-dives/forge-menu) — the library this one's input/heartbeat/warm-up plumbing
  is directly lifted from, and the "why the world doesn't pause" reasoning that applies here too (no PDA
  hijack — a menu, or any of these widgets, only ever needs discrete key events).
- [Building Nested Menus with MrxMultiPageMenu](../deep-dives/nested-menus) — the native-dialog-box way to
  nest menus, if you specifically want that look over a custom Scaleform one.
- [A Basic Co-op Text Chat](../deep-dives/coop-chat) — [coopchat.lua](coopchat) is the current, improved
  implementation of this deep dive's problem, built on `UI.Chat`.
- [Contract Framework: The Contract Board](../contract-framework/contract-board) — `UI.Board` reuses its
  exact movie (`contracts.gfx`); see that page for the movie's own callback surface.
- [WaveDefense](../wave-defense) — a full gamemode whose entire HUD and setup menu is built on `UI.Panel`,
  `UI.Bar`, and a hand-rolled "cycler" convenience over `UI.Menu`.
