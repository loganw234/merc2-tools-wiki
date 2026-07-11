---
title: "UI.Confirm / UI.Input"
parent: UI Kit
nav_order: 4
---

# UI.Confirm / UI.Input

The kit's two **modal** widgets — both grab focus, both hand control back via a callback, and both are
**singletons**: calling `UI.Confirm{}` or `UI.Input{}` again while one is already open reconfigures and
re-shows the same underlying widget rather than creating a second one. One confirm dialog and one input
prompt can exist at a time, each reused across every call site in your scripts.

## `UI.Confirm` — modal yes/no

```lua
UI.Confirm{
    text = "Delete this save slot?",
    onResult = function(yes) if yes then DoDelete() end end,
}
```

`opts`: `text` (wrapped automatically), `title` (default `"CONFIRM"`), `yes`/`no` (button labels, default
`"YES"`/`"NO"`), `onResult` — called exactly once with a plain boolean.

**Left/Right/Up/Down all just flip the highlighted choice** (there are only two), Enter commits whichever
is highlighted, and **Esc always resolves `false`** regardless of what's highlighted — a deliberate
"escape never accidentally confirms" safety rule, not a bug. The highlight **defaults to NO** (`o._pick =
1`), so a reflexive Enter-mash on an unfamiliar dialog defaults to the safe answer.

Before showing itself, `UI.Confirm` remembers whatever widget was focused before it (`o._prev = S.focus`)
and restores that focus once resolved — so popping a confirm from inside, say, a
[`UI.Menu`](menu) action via `ctx:confirm(...)` hands control back to that same menu afterward, rather than
leaving nothing focused.

### Recipe: guarding a dismissive action

`uidemo.lua`'s own `onBack` handler uses `UI.Confirm` to guard against an accidental close, rather than
just hiding on the first Back press at the root:

```lua
local function on_back()
    if D.at ~= "DEMO" then
        goto_menu(ROOT, "DEMO")           -- not at the root yet: just go up one level, no confirmation needed
    else
        UI.Confirm{
            text = "Close the demo?",
            onResult = function(yes) if yes then D.list:hide() end end,
        }
    end
end
```

The pattern generalizes to anything you don't want a stray extra Backspace/Esc to dismiss outright — only
ask when the action is actually about to do something hard to undo (here, leaving the root level), not on
every intermediate step.

## `UI.Input` — one-shot typed prompt

```lua
UI.Input{
    prompt = "ENTER A NAME",
    onSubmit = function(text) Loader.Printf("got: " .. text) end,
    onCancel = function() Loader.Printf("cancelled") end,
}
```

`opts`: `prompt` (default `"INPUT -- ENTER SUBMIT   ESC CANCEL"`), `text` (pre-filled starting value,
default `""`), `max` (character cap, default `120`), `onSubmit(text)`, `onCancel()`.

Enter calls `onSubmit` with whatever's been typed; Esc calls `onCancel` and discards it; Backspace deletes
one character. The visible line truncates from the front once typed text exceeds ~40 characters
(`"..." .. tail`), so a long entry stays readable without the whole widget growing. Same focus-save/restore
behavior as `UI.Confirm`.

### Typed character mapping

Both `UI.Input` and [`UI.Chat`](chat-and-board)'s prompt mode share one `CHAR` table mapping Windows VK
codes to `{ n = normal, s = shifted }` character pairs — letters, digits (with the correct shifted
punctuation, e.g. `2`→`@`), space, and the standard US-layout punctuation keys (comma, period, slash,
hyphen, equals, semicolon, quote, brackets, backslash, backtick). **This is a US keyboard layout**, hardcoded
— the module comment flags it directly (`edit PUNCT for other layouts`) rather than pretending it's locale
generic. Only the Shift state is read (via one `GetKeyboardState()` call per input batch); Ctrl/Alt
combinations aren't handled.

## See also

- [UI.Menu](menu) — `ctx:confirm`/`ctx:ask` are exactly these two widgets, reachable from inside a menu
  action without leaving the menu's own focus chain broken.
- [UI Kit overview](index) — the shared focus system (`UI.Focus`/`UI.Focused()`) both widgets' save/restore
  behavior is built on.
