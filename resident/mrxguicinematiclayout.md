---
title: MrxGuiCinematicLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, cinematic]
verified: true
verified_note: 'deeper pass: documented the 7-widget tree (names/coords/fonts, the two GuiInitialization bindings into mrxguicinematic), noted AddedWidgetList global; confirmed no Event.* calls and ReInit is the only function'
---

# MrxGuiCinematicLayout

*Module: mrxguicinematiclayout.lua*

## Overview
`MrxGuiCinematicLayout` is the **data-only layout companion** to [MrxGuiCinematic](mrxguicinematic): it declares the widget tree for the full-screen cinematic overlay (the black background, the movie/still-image surface, the caption text, and the subtitle/supersubtitle bands) as a plain Lua table, then loads them into the GUI. All actual behavior lives in `mrxguicinematic.lua`; this file just wires two of those functions to widget initialization.

## Inheritance
- Inherits from: `none` — data/layout module
- Imports: `MrxGuiCinematic`, `MrxGuiBase` (guarded by `if import then` so the table can also be loaded by an offline tool where `import` is absent — in that case `MrxGuiCinematic` is stubbed to `{}`)

## Instance pattern
Stateless. The only state is two **module-level globals**: `LocalWidgetList` (the static layout definition) and `AddedWidgetList` (the live widget handles created by the last `ReInit`). Note `AddedWidgetList` is a global, not a local — `ReInit` reads it before assigning it, so it relies on a prior loader having created it.

## The widget tree (`LocalWidgetList`)
One root widget, `"Cinematic Placeholder"` (640×480, center-anchored), with six children in this order — the indices matter because `mrxguicinematic.lua` grabs children by number (`tChildren[1]`, `[5]`, `[6]`, …):

1. **placeholder black bg** — full-screen black `image` (fade backdrop).
2. **placeholder image** — the still-picture `image` surface (`Show` sets its texture; `ShowMovie` hides it and plays a movie in its place).
3. **placeholder text** — caption `text`, font `english_18`, bottom-anchored.
4. **continue** — the "[confirm]" prompt `text` (localized token `[confirm] [0x46f1bb15]`).
5. **Movie subtitle** — bottom subtitle band; binds `GuiInitialization → MrxGuiCinematic._InitializeSubtitleBuffer`.
6. **Movie supersubtitle** — top subtitle band (used for `bSuper` lines).

The root's `EventHandlers.GuiInitialization` is bound to `MrxGuiCinematic._HandleInitializationEvent`, which is what turns this static tree into the working overlay (adds the `MovieWidget`, aliases `Show`/`Hide`/`ShowMovie` onto the widget, sets up animation points). Fonts are `english_18` throughout; changing coordinates here moves the corresponding element on screen.

## Functions
### `ReInit()`
The only function in the file. Removes every widget currently in `AddedWidgetList` (via `MrxGuiBase.RemoveWidget`), resets that table, then re-loads each entry of `LocalWidgetList` with `MrxGuiBase.LoadAndAddWidgetFromLayoutFileData(...)`, repopulating `AddedWidgetList`. Call it to hot-reload the cinematic layout after editing `LocalWidgetList`.

## Events
No `Event.Create`/`Event.*` engine-event references appear in this file. The `LocalWidgetList` table wires two widgets' `EventHandlers.GuiInitialization` key directly to functions from the imported `MrxGuiCinematic` module (`MrxGuiCinematic._HandleInitializationEvent` on the root widget, `MrxGuiCinematic._InitializeSubtitleBuffer` on the "Movie subtitle" child) — these are Scaleform/widget-level event handler names (dispatched by the GUI system when a widget initializes), not `Event.*` engine constants, and the handler functions themselves live in `mrxguicinematic.lua`, not this file.

## Notes for modders
- **Child order is load-bearing.** `mrxguicinematic.lua` addresses children by numeric index (subtitle is child 5, supersubtitle child 6, movie surface is added at runtime). Reordering or inserting entries in `LocalWidgetList[1].Children` will silently rewire the wrong widgets.
- **This is where you move/resize the caption and subtitle bands** — edit the `x1/y1/x2/y2` and anchors on the relevant child, then `ReInit()`. Behavior (timing, fades) is not here; that's [MrxGuiCinematic](mrxguicinematic).
- **`EventHandlers` values are function references, `EventHandlerNames` are the string names** the GUI system stores; both must be kept in sync if you rebind a handler.
- The visible strings (`"Cinematic placeholder text."`, the `[confirm] [0x46f1bb15]` token) are placeholders/localization tokens, not final on-screen copy.