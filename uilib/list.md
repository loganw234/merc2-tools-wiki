---
title: "UI.List"
parent: UI Kit
nav_order: 2
---

# UI.List

The raw scrolling list underneath both [`UI.Menu`](menu) and [`UI.Board`](chat-and-board) — reach for it
directly when you want list-of-things-with-a-callback behavior without the tree/drill-down semantics
`UI.Menu` adds on top.

```lua
local list = UI.List{
    x = 40, y = 60, title = "PICK ONE",
    items = {
        { header = "SECTION A" },
        { label = "First",  any = 1 },
        { label = "Second", any = 2 },
    },
    onChoose = function(item, i, list) Loader.Printf("picked " .. tostring(item.any)) end,
    onBack   = function(list) list:hide() end,
}
```

## `UI.List(opts)`

`opts`: `x`/`y` (default `40, 60`), `w`/`h` (default `320, 360`), `title`, `crumb`, `hint`, `items` (initial
item list — see below), `empty` (text shown when `items` is empty, default `"EMPTY"`), `focus` (pass `true`
to focus it immediately on creation), plus the three callbacks below.

## Items

`items(t)` takes a flat array where each entry is either a **header** (`{ header = "TEXT" }`, or
`{ header = true, label = "TEXT" }` — non-selectable, the cursor skips over it entirely) or a **row**
(`{ label = "Shown text", ...anything }` — any extra fields on the table are yours; they come back
unmodified through the callbacks). 10 rows are visible at once; more than that scrolls, with the scrollbar
thumb's position and height computed directly from `#items`/visible-count/current-offset.

```lua
list:items({
    { header = "AVAILABLE" },
    { label = "Oil Refinery Raid", missionId = "oil_01" },
    { label = "Convoy Ambush",     missionId = "convoy_02" },
})
```

## Callbacks

| callback | fires when |
|---|---|
| `onSelect(item, i, list)` | The cursor moves to a new row (every Up/Down that lands on a different selectable row). |
| `onChoose(item, i, list)` | Enter or Right is pressed on a selectable row. |
| `onBack(list)` | Left or Esc is pressed. |

None of these are required — a `UI.List` with none of them just displays and takes no action on selection,
useful as a pure read-only view.

## Reading/setting selection

`:selected()` returns `item, i` for whatever's currently highlighted. `:select(i)` moves the cursor there
programmatically (a no-op if `i` isn't selectable, e.g. it's a header) — useful for restoring a selection
after rebuilding `items()` with fresh data.

## Auto-resize

The body height eases toward `100 * (PITCH * shown_rows + 12) / BODY` every time `:items()` (or `:paint()`
internally) runs, where `shown_rows` is clamped to however many rows actually fit (`min(#items, 10)`, floor
1). A 2-item list and a 10-item list end up genuinely different heights on screen, animated between states
rather than snapping — the same eased-resize idea [`UI.Panel`](panel-bar-toast) and
[ForgeMenu](../deep-dives/forge-menu)'s own panel use.

## Chainable display calls

`:title(s)` `:crumb(s)` `:hint(s)` each update the movie immediately and return `self`, so they compose:

```lua
list:title("SPAWNER"):hint("UP/DOWN MOVE   ENTER PICK"):items(myRows)
```

## Recipe: driving a drill-down menu directly, without `UI.Menu`

[`UI.Menu`](menu) is one owned `UI.List` plus a builder API — but you can drive the same list-swapping
technique yourself when you want more control over the transitions than `:entry`/`:category` gives you.
[`uidemo.lua`](uidemo) (the kit's own showcase script) does exactly this: three plain item arrays and one helper that
just re-points the same list at whichever one is current —

```lua
local ROOT = {
    { header = "WIDGETS" },
    { label = "Pop a toast",    act = "toast" },
    { label = "Open a submenu", act = "sub" },
}
local SUB = {
    { header = "SUBMENU" },
    { label = "Back to the top", act = "back" },
}

local function goto_menu(items, crumb)
    D.at = crumb
    D.list:items(items)
    D.list:crumb(crumb)
end

local function on_choose(it)
    if it.act == "toast" then UI.Toast("You picked: " .. it.label)
    elseif it.act == "sub" then goto_menu(SUB, "DEMO > SUBMENU")
    elseif it.act == "back" then goto_menu(ROOT, "DEMO") end
end

local function on_back()
    if D.at ~= "DEMO" then goto_menu(ROOT, "DEMO") else D.list:hide() end
end
```

Each row just carries a plain tag (`act`) your own `onChoose` switches on — there's no tree structure at
all, just whichever flat array `:items()` was last given. Going "back" from a submenu is the identical idea
[the native-menu nesting technique](../deep-dives/nested-menus) uses: rebuild (here, just re-point to) the
parent's own item list, tracked in a plain `D.at` string rather than a stack, since `uidemo.lua` only ever
needs one level of "back" at a time.

This is also the easiest way to stress-test scrolling/auto-resize while building your own widget: a 30-row
array with a header inserted mid-list is enough to see the scrollbar thumb, the header-skipping cursor
behavior, and the eased body-resize animation all at once, without needing 30 real menu actions to test.

## See also

- [UI.Menu](menu) — a tree-navigation wrapper built entirely on one owned `UI.List`.
- [UI.Board](chat-and-board) — a two-pane view using the identical selection/scrolling logic against a
  different movie (`contracts.gfx`), for when you need a details pane alongside the list.
