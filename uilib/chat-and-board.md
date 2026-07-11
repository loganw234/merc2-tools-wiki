---
title: "UI.Chat / UI.Board"
parent: UI Kit
nav_order: 5
---

# UI.Chat / UI.Board

The two widgets in the kit that drive a **richer, purpose-built movie** rather than one of the six generic
`ui_*.gfx` files — each wraps a Scaleform movie authored for a specific, larger job.

## `UI.Board` — a two-pane list-plus-details view

```lua
local b = UI.Board{
    title = "CONTRACTS", hint = "UP/DOWN BROWSE   ESC CLOSE", focus = true,
    items = {
        { header = "AVAILABLE" },
        { label = "Oil Refinery Raid", k = 1 },
    },
    onSelect = function(it, i, board)
        if it.k == 1 then
            board:detail{ category = "DESTRUCTION", rewards = { "$8,000", "Fuel +300" },
                objectives = { "Destroy 4 storage tanks", "Stay undetected" },
                progress = 0, progressText = "NOT STARTED" }
        end
    end,
    onChoose = function(it, i, board) UI.Toast("Accepted: " .. it.label) end,
    onBack   = function(board) board:hide() end,
}
```

`UI.Board` drives **`contracts.gfx`** — the identical movie the
[Contract Framework's Contract Board](../contract-framework/contract-board) uses. It shares that movie's
two-pane shape (a category-grouped list on the left, a details panel on the right: category line, up to 4
reward lines, up to 8 objective lines, a progress bar plus progress text) and its own selection/scrolling
logic is a near-exact copy of [`UI.List`](list)'s — same header/row split, same scrollbar-thumb math, same
`nearest()` skip-headers-when-navigating behavior — just paired with the extra `:detail()` call the richer
movie's details pane needs.

`opts` matches [`UI.List`](list)'s shape (`x`/`y`/`w`/`h`, `title`, `hint`, `items`, `empty`, `focus`) plus
`detail` (an initial details payload). Beyond `:items()`/`:selected()`/`:select()`/`:title()`/`:hint()`
(identical to `UI.List`), the one new call is:

```lua
board:detail{
    category    = "OIL FIELD",
    rewards     = { "$5000", "Fuel +200" },       -- up to 4 shown
    objectives  = { "Destroy 3 tanks", "Reach the LZ" },   -- up to 8 shown
    progress    = 0.4,           -- 0..1
    progressText = "2/5",
}
```

Unlike `UI.List`, **`onSelect` fires on every cursor move**, not just as a hook you might ignore — it's the
expected place to call `:detail()` with that row's own data, which is exactly the pattern the demo script
uses (see `menudemo.lua`'s "Contract Board" entry — three items, three different `:detail{}` payloads
picked by an `it.k` tag on each row).

## `UI.Chat` — a scrolling log with an optional typed line

```lua
local ch = UI.Chat{ title = "RADIO", x = 640 - 360 - 8, y = 8 }
ch:push("Misha: slick menu, boss.")
ch:prompt(function(text) Loader.Printf("you said: " .. text) end)
```

Drives `chat.gfx`. `opts`: `x`/`y` (default `20, 400`), `w`/`h` (default `360, 132`), `title`, `max`
(scrollback cap, default `60`), `onSubmit`.

- `:push(text)` word-wraps and appends to the log (`UI.wrap`, same wrapping utility `UI.Toast` uses),
  trimming the oldest lines past `max`. Only the last 5 lines are ever visible at once; the body
  auto-resizes to however many of those 5 slots are actually filled.
- `:prompt([onSubmit])` enters typed-input mode — same `CHAR`-table-driven typing as
  [`UI.Input`](confirm-and-input), Enter pushes the typed text as a new log line **and** fires `onSubmit`
  with it, Esc cancels without pushing anything.
- `:title(s)` / `:clear()`.

`UI.Chat` isn't the same mechanism as the [Co-op Text Chat](../deep-dives/coop-chat) deep dive's approach
(that one is built on `MrxGuiTextBuffer`, worked around a real engine crash, and syncs across a live
network connection) — it's a separate, purpose-authored movie with its own scrolling-log implementation.
Whether the two are meant to solve the same problem or different ones (a synced multiplayer chat vs. a
local flavor-text radio log) isn't stated in the source; treat them as two independent tools until that's
confirmed one way or the other.

## See also

- [Contract Framework: The Contract Board](../contract-framework/contract-board) — the original
  `contracts.gfx` caller; `UI.Board` is a second, independent driver for the identical movie.
- [UI.List](list) — `UI.Board`'s selection/scrolling logic is copied from here, extended with `:detail()`.
- [Co-op Text Chat](../deep-dives/coop-chat) — a different, `MrxGuiTextBuffer`-based chat mechanism; not
  confirmed to be related to `UI.Chat`.
