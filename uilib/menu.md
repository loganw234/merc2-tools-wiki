---
title: "UI.Menu"
parent: UI Kit
nav_order: 1
---

# UI.Menu

`UI.Menu` is [ForgeMenu](../deep-dives/forge-menu)'s declarative `:entry`/`:category` API, reimplemented on
top of [`UI.List`](list) instead of the `forge.gfx` movie. If you've already read the ForgeMenu deep dive,
the shape is deliberately identical:

```lua
local menu = UI.Menu{ title = "MY MENU", key = "F8" }

menu:entry("Do a thing", function(ctx) ctx:hint("done") end)

menu:category("Spawns", function(c)
    c:entry("Tank", function(ctx) ctx:spawn("M1A2 (Full)", 8) end)
    c:category("Enemies", function(cc) cc:entry(...) end)   -- nests as far as you like
end)

menu:toggle()   -- put this at the very end of your OnKey file
```

## `UI.Menu(opts)`

`opts` (or a bare string, treated as `title`): `title` (shown at the top), `id` (defaults to `title` — give
distinct menus distinct ids so their runtime state doesn't collide), `key` (your toggle key, display only),
`x`/`y` (top-left corner, defaults `40, 60`), `onClose` (called when the menu closes, however that happens).

## Building the tree

| Call | Adds |
|---|---|
| `menu:entry(label, action)` | A leaf. `action` is `function(ctx) ... end`, called when chosen. |
| `menu:category(label, buildFn)` | A submenu. `buildFn` receives a new builder (`c`) to add children to; also returned, so you can build inline *or* keep the returned object and add to it later. |
| `menu:header(text)` | A non-selectable section divider — the cursor skips over it. |
| `menu:switch(label, get, set)` | A ready-made ON/OFF toggle: renders `"<label>: ON"`/`"<label>: OFF"` from `get()`, and calls `set(newBool, ctx)` when picked. Saves writing the dynamic-label boilerplate yourself. |

`label` can be a plain string, or a function returning one — re-evaluated on every paint, which is exactly
what `:switch` uses internally and what you'd reach for directly if you needed a live label `:switch` alone
doesn't cover:

```lua
_G.MyState = _G.MyState or {}
local S = _G.MyState
menu:entry(function() return S.god and "God: ON" or "God: OFF" end, function(ctx)
    S.god = not S.god
end)
```

This is the same `switch`-equivalent hand-rolled directly — `:switch` exists so you don't have to write it
out every time.

**A dynamic label re-renders the instant it's picked, cursor position preserved.** Choosing any entry
re-paints the current menu level afterward — necessary for `:switch`/dynamic-label entries specifically,
since without it the label would keep showing its *old* text until you happened to navigate away and back.
Re-painting means re-calling `UI.List:items()`, which on its own would reset the selection to the top of
the list; `Menu:_choose` works around that by remembering the selected row first and restoring it after:

```lua
if self._rt.open then
    local list = self._rt.list
    local keep = list and list._sel          -- keep the cursor where it is (a re-items resets it to the top)
    self:_paint()
    if list and keep then list:select(keep) end
end
```

## The `ctx` every action receives

Beyond the [ForgeMenu](../deep-dives/forge-menu#the-whole-api-up-front)-equivalent fields
(`ctx.x/y/z/yaw`, `ctx.char`/`ctx.player`, `ctx:spawn`, `ctx:close`), `UI.Menu`'s `ctx` adds two composition
helpers that pop one of the kit's other modal widgets directly from inside a menu action:

| call | does |
|---|---|
| `ctx:hint(msg)` / `ctx:toast(msg)` | Both pop a [`UI.Toast`](panel-bar-toast) — `:toast` is just a more explicit alias. |
| `ctx:print(msg)` | Writes to `lua_loader_printf.log`, prefixed `"[uilib] "`. |
| `ctx:close()` | Closes the menu. |
| `ctx:confirm(text, onYes, onNo)` | Pops a [`UI.Confirm`](confirm-and-input) and routes the result to whichever callback matches. |
| `ctx:ask(prompt, onSubmit, onCancel)` | Pops a [`UI.Input`](confirm-and-input) typed prompt. |
| `ctx:spawn(template [, dist])` | Spawns at your feet or `dist` metres ahead; returns the guid. |

<a id="ctxspawn-rejects-a-blank-template-before-it-ever-reaches-the-engine"></a>
**`ctx:spawn` rejects a blank template before it ever reaches the engine.** `Pg.Spawn("")` is a **hard
native crash** (an empty template name resolves to a null asset in the engine's own C++), and `pcall`
**cannot catch it** — `pcall` only catches Lua-level errors, and a native crash never raises one. If your
own code can ever hand `ctx:spawn` an unset or empty template (a dynamically-resolved value from another
system, a menu built before its data finished loading, ...), that used to be an unrecoverable crash to
desktop. It's now guarded up front:

```lua
if type(template) ~= "string" or template:match("^%s*$") then
    self:hint("NO TEMPLATE SET"); return nil
end
```

A blank/whitespace-only `template` now just shows a hint and returns `nil`, the same as any other failed
spawn — never a crash. Worth remembering for **any** direct `Pg.Spawn` call, not just through `ctx:spawn` —
`pcall` is not a safety net against this one specific failure mode.

```lua
menu:category("Dialogs", function(c)
    c:entry("Ask a question", function(ctx)
        ctx:confirm("Is this useful?", function() ctx:toast("Glad to hear it!") end)
    end)
end)
```

This is the one thing `UI.Menu` can do that plain [ForgeMenu](../deep-dives/forge-menu) can't — a menu
action opening a *different kind* of widget (a confirm dialog, a typed prompt, even a full
[`UI.Board`](chat-and-board)) mid-flow, because every widget in the kit shares the same focus/heartbeat
engine instead of each being its own island.

## How it's built: a thin tree wrapper over `UI.List`

Where ForgeMenu talks directly to the `forge.gfx` movie's row/crumb/hint/scroll callbacks, `UI.Menu`
delegates all of that to one owned [`UI.List`](list) instance and just translates tree navigation into list
operations:

```lua
function Menu:_paint()
    local lvl = self._stack[#self._stack]
    local rows = {}
    for _, node in ipairs(lvl.children) do
        if node.header then rows[#rows + 1] = { header = node.header }
        elseif node.children then rows[#rows + 1] = { label = resolveLabel(node) .. "  >", _node = node }
        else rows[#rows + 1] = { label = resolveLabel(node), _node = node } end
    end
    self._rt.list:items(rows)
    ...
end
```

`:_choose` (wired to the list's `onChoose`) either pushes a new stack frame (entering a category) or runs
the leaf's `action` inside a `pcall`; `:_back` (wired to `onBack`) pops the stack, or closes the menu
entirely if already at the root. The whole nested-menu problem collapses to "translate a tree walk into
`UI.List:items()` calls" — none of the actual widget/input/lifecycle code is duplicated.

## One menu visible at a time

Same rule as [ForgeMenu](../deep-dives/forge-menu#one-menu-at-a-time-by-design): opening a `UI.Menu` closes
whichever other one is currently open (`S.openId` tracks which). Runtime state persists per `id` across the
OnKey re-run (`menu_rt(id)`), so `:toggle()` genuinely toggles and the underlying list widget is reused
rather than rebuilt and leaked on every press — the source comment calls this out directly as a fix over an
earlier version that didn't have it ("v2.2: UI.Menu ForgeMenu parity — persistent per-id state = real
toggle, no leak").

## The demo scripts

The kit ships **two** showcase scripts, split by what each covers — neither is a leftover or superseded by
the other. Full scripts, each on its own page, under [UI Kit Scripts](scripts):

- **[`menudemo.lua`](menudemo)** (`scripts/OnKey/`, bound to F3) — `UI.Menu` itself, end to end: nested
  categories (`Spawn Vehicles`, `Spawn Enemies > Guerilla/Chinese`), `ctx:spawn`, the `:switch` live ON/OFF
  toggle (`"God Mode"`), and — under a `"Rich Widgets"` category — composing with `UI.Confirm`/`UI.Input`
  via `ctx:confirm`/`ctx:ask`, plus dedicated entries that open a full [`UI.Board`](chat-and-board) and a
  [`UI.Chat`](chat-and-board) log directly from a menu action.
- **[`uidemo.lua`](uidemo)** (`scripts/OnKey/`, bound to Delete; see [UI.List](list) for the recipe pulled
  from it) — everything *other* than `UI.Menu`: a hand-driven drill-down built directly on
  [`UI.List`](list) (including a 30-row scrolling stress test), [`UI.Panel`](panel-bar-toast) used as a
  rolling event log, [`UI.Bar`](panel-bar-toast), and both [`UI.Confirm`/`UI.Input`](confirm-and-input)
  (including a confirm-before-close guard on its own back button).

Between the two, every one of the kit's nine widgets has a real, current demo behind it. A third script,
[`coopchat.lua`](coopchat), goes beyond demoing `UI.Chat` into real use — a full co-op text chat.

## See also

- [Building ForgeMenu](../deep-dives/forge-menu) — the original declarative menu API this one mirrors, and
  the full story behind the input/heartbeat/warm-up plumbing both share.
- [UI.List](list) — the widget `UI.Menu` is built on.
- [UI.Confirm / UI.Input](confirm-and-input) — what `ctx:confirm`/`ctx:ask` actually open.
- [Building Nested Menus with MrxMultiPageMenu](../deep-dives/nested-menus) — the native-dialog-box
  alternative, if you want that look instead of a custom Scaleform one.
