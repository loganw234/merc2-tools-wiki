---
title: "UI.Panel / UI.Bar / UI.Toast"
parent: UI Kit
nav_order: 3
---

# UI.Panel / UI.Bar / UI.Toast

The three simplest widgets in the kit — no navigation, no focus needed for most uses, just display.

## `UI.Panel` — a title bar plus up to 8 lines

```lua
local p = UI.Panel{ x = 20, y = 120, title = "STATUS" }
p:line(0, "Health: 100")
p:line(1, "Fuel: 80%")
```

`opts`: `x`/`y` (default `20, 120`), `w`/`h` (default `300, 200`), `title`, `lines` (how many of the 8 slots
to start pre-sized for, default `0`).

- `:title(s)` sets the header.
- `:line(i, s)` sets line `i` (0-indexed, 0–7). Setting a non-empty line past the panel's current `:fit()`
  count auto-grows it — `:line(3, "text")` on a panel only fit for 2 lines silently calls `:fit(4)` first,
  so you don't have to track the count yourself as you add lines.
- `:fit(n)` explicitly sets how many of the 8 lines are visible (clamped 0–8) and eases the body height
  toward it, same auto-resize idea as [`UI.List`](list).
- `:clear()` blanks all 8 lines and fits back down to 0.

## `UI.Bar` — a label plus a progress bar

```lua
local b = UI.Bar{ x = 20, y = 330, label = "Loading" }
b:set(0.4)          -- 40%
b:label("Almost there")
```

`opts`: `x`/`y` (default `20, 330`), `w`/`h` (default `300, 36`), `label`, `value` (initial `0..1`, default
`0`). `:set(v)` clamps to `0..1` and sends the bar as a whole-number percent; `:label(s)` updates the text.

## `UI.Toast` — a transient notification

```lua
UI.Toast("Wardrobe Unlocked!")
UI.Toast("Something urgent", { ttl = 8 })   -- override the default hold time
```

Unlike the other widgets, `UI.Toast` is a **function**, not a constructor you keep a handle to for long —
call it, it finds a free slot (or steals the soonest-expiring one if all `UI.TOAST_SLOTS` are busy,
default `3`), wraps the text to fit, shows it, and starts its countdown. It does return the underlying
toast object (with a `:dismiss()` if you need to clear it early), but most calls are fire-and-forget.

Toasts stack top-to-bottom in a fixed screen region — `UI.TOAST_X`/`UI.TOAST_Y` (right-aligned by default,
`640 - 320 - 8` from the left in the kit's fixed 640×480 virtual canvas) — and each auto-hides after
`UI.TOAST_TTL` seconds (default `4`) unless overridden per-call via `opts.ttl`.

## The real bug behind all three: `SetLocation` takes corners, not a size

Every widget constructor in the kit calls a shared `make_widget(file, x, y, w, h)` helper, and its one
load-bearing comment documents a bug that shipped and was found live:

```lua
-- SetLocation takes CORNER coords (x1, y1, x2, y2), NOT (x, y, width, height).
-- Passing w/h as the corners makes any widget whose w<x or h<y collapse into an
-- inverted rect and render as a giant smear (that was the "broken toasts" bug).
wg:SetLocation(x, y, x + w, y + h)
```

`MrxGuiBase.FlashWidget:SetLocation` wants the second point as an absolute screen coordinate, not a
width/height offset — call it with `(x, y, w, h)` directly (the natural reading of "position and size") and
any widget whose height/width is smaller than its x/y position inverts into a nonsensical rectangle. This
is specifically why every widget constructor in `uilib.lua` computes `x + w, y + h` itself rather than
trusting a caller (or a future edit) to remember the conversion — the fix is centralized in the one place
that builds every widget, not repeated at each call site.

## See also

- [UI Kit overview](index) — the shared heartbeat/focus/warm-up engine every widget here, including these
  three, is built on.
- [UI.List](list) — the widget to reach for once you need selectable rows, not just display.
