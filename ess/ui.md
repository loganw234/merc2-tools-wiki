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
port of uilib v2.2."

**As of Ess 0.5.0 the kit no longer draws the way `uilib.lua` did.** Every widget is now a clip inside
**one** Scaleform movie (`ess_ui.gfx`) that builds its own chrome at runtime from a table of plain numbers
(`Ess.UI.Theme`), instead of eight per-widget movies with their layouts baked into the artwork. The public
API is unchanged — every call below behaves as it did — but the fixed capacities that came with the old
movies are gone, and there are two new surfaces (`Ess.UI.Theme`, `Ess.UI.setScale`) that did not exist
before. See [The runtime rewrite](#the-runtime-rewrite).

Fits into [the three tiers](index#the-three-tiers) like this: `Ess.Gfx` **is** the Raw tier for widget
work — the primitives every one of `uilib.lua`, `contracts.lua`, ForgeCam, and ForgeMenu used to hand-roll
separately around `MrxGuiBase.FlashWidget`. `Ess.UI` is the Core tier — already fairly friendly, so most UI
work doesn't need an Easy tier at all. The thin `Ess.Easy` slice on top covers only the handful of
single-call cases that don't need a widget object (see [below](#esseasy-ui-helpers)).

**Deploy:** the `.gfx` movies `Ess.UI` needs ship in `data/vz-patch.wad`, part of the normal
[Ess install](index#install) — nothing extra to inject beyond what installing `Ess` already requires.
**Except on 0.5.1, where that wad was broken — read the next section before anything else.**

## Install warning for the UI wad

**Ess 0.5.1's shipped `data/vz-patch.wad` did not contain `ess_ui.gfx` at all. On a clean 0.5.1 install
the entire UI kit does nothing — every menu, panel, toast, board and chat, plus `Ess.UI.Theme` and
`Ess.UI.setScale`. Fixed in 0.5.2. If you are on 0.5.1, installing 0.5.2 is not optional.**

| Ess version | State of the UI kit |
|---|---|
| 0.4.2 and earlier | Fine — pre-rewrite, eight per-widget movies, all present in the wad. |
| **0.5.0** | Fine on a *dev* install with the movie hand-injected; the released wad was already stale. |
| **0.5.1** | **Broken.** No `ess_ui` asset in the wad. Nothing draws. |
| **0.5.2+** | Fixed. The wad carries 12 assets and the build gate enforces it. |

The worst part is that it fails **silently**. Confirmed from source: `Ess.Gfx.widget` constructs the host
`FlashWidget` successfully whether or not the named asset resolves, so `rtEnsure`'s own
`"is ess_ui.gfx injected?"` branch never fires, nothing errors, nothing reaches
`lua_loader_printf.log`, and the 3-second load-timeout fallback (see
[The runtime rewrite](#the-runtime-rewrite)) cheerfully flushes the queued draw calls into a movie that
isn't there. There is **no fallback** to the old per-widget movies — `Ess.UI._rtcall` just returns `false`.
A 0.5.1 user's symptom is "my menu key does nothing," with a clean log.

**Why it shipped:** the wad had been committed once, *before* the UI kit was rewritten, and never
regenerated — `ess_ui.gfx` is authored in a separate repo (`gfxforge-web`), so a rebuild there touched
nothing in the Ess tree. `build/package.py` only checked `wad.exists()`, which a stale wad passes
perfectly. It did not reproduce in development because the dev install had the movie injected by hand.

### The bare-stem trap

Per `docs/UI_WAD.md`, the underlying trap is worth knowing for anyone injecting their own movie:

> **Assets are registered under their bare stem, but loaded with the extension.** `Ess.UI.FILES` says
> `"ess_ui.gfx"` and `SetSwfFile` takes `"ess_ui.gfx"` — but the wad's `ASET` table holds
> `pandemic_hash_m2("ess_ui")`, with the extension stripped before hashing.

So injecting a movie under its full filename registers a name the engine will never look up, and it fails
**exactly as silently as the missing-asset bug did**: the widget host constructs, nothing errors, nothing
logs, the UI simply never appears. `mercs2-gfx-tool`'s `--name` argument takes the bare stem:

```bash
gfx_tool new --wad "<game>/data/vz.wad" --name ess_ui --movie ess_ui.gfx \
             --merge data/vz-patch.wad --out /tmp/vz-patch-new.wad
```

### The build gate that stops it recurring

0.5.2 added `check_wad()` to `build/package.py`. It parses the wad's **FFCS `ASET` table** directly
(chunk table at `0x0C`, five `(tag, value, meta)` triples; `ASET` entries are 16 bytes with the hash
first) and fails the build if any movie named in `Ess.UI.FILES` is absent. The names are read out of
`Ess.UI.FILES` itself rather than listed in `package.py`, so adding a movie to the kit extends the gate
automatically instead of quietly opting out of it. **Verified in both directions** per the release commit:
the gate rejects the wad that actually shipped in 0.5.1 and accepts the repaired one.

The wad went from 11 assets to 12: the 11 pre-rewrite assets were present the whole time and are
unchanged; `ess_ui` was added alongside them. Two footnotes for anyone who goes looking:

- The release commit calls the pre-rewrite 11 "per-widget movies". Only **eight** of them are. Reading
  the shipped `data/vz-patch.wad`'s chunk table gives 12 `ASET` entries; hashing candidate stems against
  it identifies ten — the eight per-widget UI movies, `ess_ui`, and `forge` (the movie the MissionForge
  demo drives directly through `Ess.Gfx`). The other two can't be named from the wad alone, which stores
  hashes and hash-named block paths.
- `docs/UI_WAD.md`'s prose says "the other ten" — an off-by-one in the doc; the wad and the release
  commit both say 11 + `ess_ui`.

## The runtime rewrite

`Ess.UI` 0.5.0 replaced eight per-widget movies with **one**: `ess_ui.gfx`, whose AS2 payload is a UI
toolkit that draws every widget from theme parameters. Each `Ess.UI` widget becomes a container clip
*inside* that movie, addressed by a string id, so N widgets cost one movie load instead of N. Navigation
is still driven by the Lua heartbeat's key polling — deliberately, so the change is only about **who
draws**.

`Ess.UI.FILES` still lists all nine names, because a third-party script may reference
`Ess.UI.FILES.panel`. Only `runtime` is loaded by anything:

```lua
Ess.UI.FILES = {
    runtime = "ess_ui.gfx",                                     -- the only one Ess loads
    list  = "ui_list.gfx",  panel   = "ui_panel.gfx",  bar   = "ui_bar.gfx",     -- inert
    toast = "ui_toast.gfx", confirm = "ui_confirm.gfx", input = "ui_input.gfx",  -- inert
    chat  = "chat.gfx",     board   = "contracts.gfx",                           -- inert
}
```

The eight inert `.gfx` files are still deployed, so anyone driving them directly through
[`Ess.Gfx`](#essgfx) still can.

### The hard caps are gone

This is the part most likely to change what you can write. Every one of the old ceilings existed because
rows and fields were **pre-baked into the movie's artwork**; the runtime creates them on demand, so they
simply aren't ceilings any more.

| Widget | Old cap | Why it existed | Now |
|---|---|---|---|
| [`Panel`](#essuipanel) | 8 lines | `ui_panel.gfx` hand-listed `p_line0`…`p_line7` | No cap. `:line(20, s)` works; `:fit(n)` clamps only at 0. |
| [`Toast`](#essuitoast) | 3 stacked | `ui_toast.gfx` was a single-toast movie instantiated three times | `Ess.UI.TOAST_SLOTS` is a **tunable, not a ceiling** — raising it just works. Still defaults to 3. |
| [`Chat`](#essuichat) | 5 visible lines | `chat.gfx` had five message fields | `opts.lines`, default 5, any size. |
| [`Confirm`](#essuiconfirm) | 2 message lines | two message fields | Wrapped at 44 columns, bounded at 8 lines as a *sanity* bound (`MAX_LINES`), not a format limit. |
| [`Board`](#essuiboard) | 4 rewards, 8 objectives | `contracts.gfx`'s field count | No cap on either. |
| [`List`](#essuilist) | fixed 10 visible rows | `VIS = 10` tied to `ui_list.gfx` | `opts.rows`, default 10. Still **windowed on purpose** — O(visible), not O(total), which matters when a real menu in the wild has 831 entries. |

`Ess.UI.Toast` also stopped pre-wrapping its text in Lua: the movie's text field wraps natively, so a long
toast wraps instead of being cut to the two lines the old movie had fields for. `Ess.UI.wrap` is still
exported and still used by `Confirm` and `Chat` (there, keeping the wrap in Lua is what keeps the dialog's
width predictable regardless of message length).

### Async load is handled, not worked around

`SetSwfFile` is asynchronous — it returns before the movie exists, so early calls silently drop.
`uilib.lua`'s answer, carried into early `Ess.UI`, was `_WARMUP = 8`: re-send every widget's whole state
eight times on a 0.05s heartbeat and hope one lands. `Ess.Gfx.widget` now passes `SetSwfFile`'s
**load-completion callback**, which the engine has always had and this code was passing `nil` for. Calls
made before the movie loads are **queued and flushed in order** — nothing is dropped and nothing is sent
twice.

Confirmed live per the rewrite commit: the callback does fire on this engine, logging
`UI runtime ready (load callback)`.

Because the callback was unverified when the code was written, there is still a belt-and-braces
`RT_LOAD_TIMEOUT` of **3.0 seconds**: if the callback hasn't fired by then, the queue is flushed anyway
and the log says `UI runtime ready (timeout fallback -- load callback did not fire)`. A UI that appears
slightly late is recoverable; one that never appears is not.

Two consequences:

- **`Ess.UI._WARMUP` no longer applies to any `Ess.UI` widget.** It's still defined (`8`), and
  `Ess.UI._attachCommon` still consumes it — but confirmed by grep, nothing calls `_attachCommon` any
  more. Every widget goes through `Ess.UI._attachRuntimeCommon` instead, whose `_repaint` is an empty
  function with the comment "Nothing to warm up any more." [`Ess.Gfx.warmupRerender`](#essgfx) stays for
  custom widgets you build yourself.
- **Panels are write-through.** The Lua-side line cache existed only to re-send state during warm-up; the
  queue makes it unnecessary, so it's gone.

### Movie → Lua events must be registered up front

A confirmed gotcha recorded in `src/42_ui_engine.lua`, worth knowing if you build on `Ess.Gfx` yourself:
**every event name the movie can send has to be registered before the movie loads.** Registering a new
name on an already-loaded widget does not bind — `Metrics` (registered in `rtEnsure`) delivered fine while
`Diag` and `ScreenInfo`, registered later from a test, silently never arrived. This matches how the
game's own code does it: `resident/mrxgui.lua` registers all its `SetFlashEventHandler`s inside the
`SetSwfFile` load callback.

The engine registers four up front: `essuiMetrics` (the reply to `:measure()`), `essui` (diagnostics),
`essuiScreen` (canvas-edge report), and `essuiRow` (opt-in mouse row clicks).

### Ask the movie, don't recompute the layout

Because the movie owns the layout — panel height depends on the theme's `rowHeight`/`titleHeight`/
`padding` and on how many lines are populated — any Lua-side copy of that arithmetic is a second source of
truth waiting to drift. Duplicating it is what previously drew a bar through the middle of a tall panel.
So `List`, `Panel`, `Bar` and `Chat` all expose:

| Call | Signature | Notes |
|---|---|---|
| `:measure(cb)` | `measure(cb) -> self` | **Asynchronous.** `cb(w, h, all)` fires when the movie replies through the `essuiMetrics` channel; `all` also carries `x`, `y`, `rows` and `kind`. |

## Ess.UI.Theme

New in Ess 0.5.0. The entire look of the kit as **34 plain values** (counted from `DEFAULTS` in
`src/41_ui_theme.lua`; the changelog's "~36" is a round number, the table has 34). Nothing is baked into
the movie, so restyling is assigning numbers — no Flash tools, no re-export, no wad rebuild.

```lua
Ess.UI.Theme.preset("cyan")            -- a whole look at once
Ess.UI.Theme.accent     = 0x59D0FF     -- or one value at a time
Ess.UI.Theme.panelAlpha = 80
Ess.UI.Theme.rowHeight  = 22
Ess.UI.Theme.apply()                   -- push + redraw anything already on screen
```

Setting values **before any widget exists needs no `apply()`** — the first widget picks them up, because
the engine pushes the whole theme itself as part of its ready handshake (before the queued draw calls
flush, so the first draw is never in the wrong style and then visibly restyled). `apply()` exists for
changing the look while the UI is live, which is what makes it pleasant to tune from a console.

| Call | Notes |
|---|---|
| `Ess.UI.Theme.preset(name)` | Applies a named preset. **Clears every previous override first**, so two looks can never blend. An unknown name is *reported* via `Ess.Log` and leaves the current theme alone — a typo'd preset would otherwise look exactly like "theming doesn't work". |
| `Ess.UI.Theme.get(k)` | The **effective** value: your override if set, else the default. Reading `Ess.UI.Theme[k]` directly gives `nil` for anything you haven't personally set, since the defaults live behind the table. |
| `Ess.UI.Theme.apply()` | Re-push all keys and redraw what's on screen. Pushes **all** keys, not just changed ones, so the movie can never be half-way between two themes. |
| `Ess.UI.Theme.reset()` | Drop every override, back to stock. Same result as `preset("classic")`. |
| `Ess.UI.Theme.DEFAULTS` | The stock table. `DEFAULTS` mirrors `ess_ui.gfx`'s own `ThemeDefaults()` exactly, so adopting the runtime changed nothing visually until someone asked. |
| `Ess.UI.Theme.PRESETS` | The preset table — writable, see the worked example below. |

**A key set to `nil` falls back to its default rather than drawing nothing**, so a typo degrades to "stock
look" instead of an invisible panel.

**Reserved names.** `apply`, `reset`, `preset`, `get` and `_push` are functions on this table and
`DEFAULTS`/`PRESETS` are sub-tables, so none of those seven can be used as a theme key. Harmless today —
none appears in `DEFAULTS`, so none is ever pushed to the movie — but `Ess.UI.Theme.get("preset")` hands
back a function rather than a value.

### The seven presets

Confirmed from `src/41_ui_theme.lua`'s `PRESETS` table, not from the changelog's summary:

| Preset | What it is |
|---|---|
| `classic` | The stock look — and **deliberately an empty table**: every key falls through to its default. That's the point. It means the defaults *are* a theme rather than something privileged, and it's always the way back. |
| `cyan` | Seven keys: an ice-blue accent (`0x59D0FF`), matching selection, `radius = 8`, `rowHeight = 22`. |
| `slate` | Desaturated grey-blue, `radius = 2`, higher `panelAlpha` (96). |
| `amber` | Warm gold accent (`0xFFC448`), header text tinted to match. |
| `neon` | Magenta/teal, `borderWidth = 2`, `radius = 0`. Labelled in source as "deliberately loud, for showing the range rather than for daily use". |
| `mono` | Pure black/white, `panelAlpha = 100`, `rowHeight = 22`, larger type. Labelled "high contrast, chunky rows — also a legibility option, not only a look". |
| `dusk` | Soft violet, low contrast, `radius = 10`. |

### The 34 values

Colours are `0xRRGGBB`. **Metrics are in CANVAS units, not pixels** — see
[`Ess.UI.setScale` and the canvas](#essuisetscale-and-the-canvas).

| Group | Keys (default) |
|---|---|
| Accent | `accent` (`0xE88C18`), `accentText` (`0x191919`) |
| Panel | `panelFill` (`0x181A1F`), `panelAlpha` (`92`), `panelBorder` (`0x2A2E37`), `borderWidth` (`1`) |
| Rows | `rowFill` (`0x1E2127`), `rowFillAlt` (`0x22252C`), `rowHover` (`0x2E333C`), `rowSelected` (`0x59D0FF`), `rowSelectedText` (`0x10151A`) |
| Text | `textPrimary` (`0xE1E5EC`), `textDim` (`0x969CA8`), `textAccent` (`0x78D2FF`), `textHeader` (`0xE1E5EC`) |
| Bar | `barFill` (`0x5AD078`), `barTrack` (`0x282C34`) |
| Shared palette | `warn` (`0xFFC448`), `danger` (`0xE05252`) |
| Metrics | `radius` (`4`), `rowHeight` (`18`), `titleHeight` (`26`), `padding` (`8`), `scrollbarWidth` (`4`), `crumbHeight` (`14`), `hintHeight` (`14`) |
| Type | `font` (`"_normal_Font"`), `sizeTitle` (`13`), `sizeBody` (`11`), `sizeSmall` (`10`) |
| Feel | `easing` (`0.35`), `hoverEnabled` (`0`) |
| Gradient | `gradientHeader` (`0`), `gradientAngle` (`1.5707963`) |

Two of those need their own note:

- **`warn` and `danger` are not drawn by any chrome.** They're a shared palette for *your* code to
  reference via `Ess.UI.Theme.get("danger")`, so a mod's own colours track the active theme instead of
  hardcoding their own.
- **`gradientHeader`/`gradientAngle` are known non-functional.** The source flags them: `beginGradientFill`
  renders flat in this GFx build at every rotation tested, even with the mandatory matrix argument. They
  are kept so nothing breaks if that's ever fixed; **setting them does nothing today.**

### Worked example

`samples/recipes/theme_the_ui.lua` (shipped in the release zip under `Ess-samples/recipes/`) is both the
recipe and a smoke test. The parts worth copying:

```lua
local T = Ess.UI.Theme

-- A preset is just a table of overrides. `cyan` in full -- seven keys, nothing else:
--     cyan = { accent = 0x59D0FF, accentText = 0x10151A, textAccent = 0x9BE4FF,
--              rowSelected = 0x59D0FF, rowSelectedText = 0x10151A,
--              radius = 8, rowHeight = 22 }
-- Anything it doesn't mention keeps the default.

T.preset("cyan")
T.get("accent")             --> 0x59D0FF, from the preset

-- Tweaking on top: assign, then apply().
T.panelAlpha = 80
T.rowHeight  = 24
T.apply()
T.get("panelAlpha")         --> 80
rawget(T, "barFill")        --> nil: never set, still draws the default

-- Your own preset behaves exactly like a built-in.
T.PRESETS.recipe_demo = {
    accent = 0x2ED573, accentText = 0x06210F,
    rowSelected = 0x2ED573, rowSelectedText = 0x06210F,
    textAccent = 0x8CF0B4, radius = 6,
}
T.preset("recipe_demo")

T.preset("no_such_preset_exists")   -- reported via Ess.Log; current theme survives untouched

T.reset()                   -- back to stock
```

**One trap the source itself documents and the code then contradicts:** `Ess.UI.Theme.apply()`'s comment
says it is safe to call when no UI exists because "there is nothing to do and nothing to queue." It *is*
safe, but reading the code, the not-yet-loaded branch still calls `Ess.UI._rtcall("ThemeApply", {})`, and
`_rtcall` runs `rtEnsure()` — which constructs the fullscreen runtime widget and starts loading
`ess_ui.gfx`. So a bare `Ess.UI.Theme.apply()` in an `OnLoad` script **does** spin the kit up before any
widget is wanted. This is precisely the side effect [`Ess.UI.setScale`](#essuisetscale-and-the-canvas) was
fixed to avoid; `apply()` was not given the same treatment. Set your theme keys and *don't* call `apply()`
at load time — the first widget pushes them for you.

## Ess.UI.setScale and the canvas

Three different coordinate spaces are in play here, and the release fixed a bug caused by conflating two
of them. Worth getting straight before tuning anything.

| Name | What it is | Value |
|---|---|---|
| **MrxGui widget space** | The engine's fixed virtual screen. Resolution-independent — the same numbers land in the same relative place at 1080p, 1440p or 4K. | 480 tall, `480 × aspect` wide: **853 on 16:9**, 640 on 4:3. |
| **The stage** | `ess_ui.gfx`'s own stage, fixed at build time. | `Ess.UI.STAGE_W` = **853**, `Ess.UI.STAGE_H` = **480**. |
| **The canvas** | What your layout code should use: the stage divided by the global scale. | `Ess.UI.CANVAS_W`/`CANVAS_H` — **1137 × 640** at the default scale of 75. |

Do **not** read `MrxGuiBase.nScreenWidth`/`nScreenHeight` for any of this. They report 640×480 with scale
1 regardless of the real display, because `g_nGuiScreenWidthTemp` was `nil` when that module loaded —
they're defaults, not measurements. `Graphics.GetScreenRatio()` returns a **category string**
(`"WIDESCREEN"` / otherwise), not a number, so only those two cases can be told apart; 16:10 is treated as
16:9, the same approximation the game itself makes.

| Function | Signature | Notes |
|---|---|---|
| `setScale` | `Ess.UI.setScale(pct) -> pct, CANVAS_W, CANVAS_H` | Sets the global scale and re-derives the canvas. Clamped **25–200**; a non-number becomes 100. Takes effect immediately, safe to call repeatedly while tuning. |
| `isWide` | `Ess.UI.isWide() -> bool` | True when `Graphics.GetScreenRatio()` reports widescreen. |
| `widgetRect` | `Ess.UI.widgetRect() -> w, h` | The host widget's rectangle in widget space. `853, 480` on widescreen (1:1 with the stage); `640, 360` on 4:3, so the 16:9 stage is **letterboxed** rather than squeezed. |
| `canvasW` | `Ess.UI.canvasW() -> n` | `Ess.UI.CANVAS_W`. |
| `screen` | `Ess.UI.screen() -> w, h, ratio` | Canvas width/height plus the game's own category string, not a number. |
| `anchor` | `Ess.UI.anchor(a) -> x, y, w, h` | Resolves an edge-relative box against the **measured** canvas. |

`Ess.UI.anchor` accepts `left`/`right`/`top`/`bottom` (inset from that edge), `cx`/`cy` (centre on that
axis), `w` (default `100`) and `h` (default `24`):

```lua
local x, y, w, h = Ess.UI.anchor{ right = 8, top = 8, w = 160, h = 22 }      -- 8 in from the top-right
local x, y, w, h = Ess.UI.anchor{ cx = true, bottom = 40, w = 300, h = 80 }  -- centred, 40 up from the bottom
```

The point of the indirection: "8 in from the right edge" resolves against the real canvas width, whereas
`x = 640 - 160 - 8` written at a call site bakes in the 4:3 assumption. `Ess.UI.TOAST_X` used to be
exactly that, and put toasts ~213 units left of the real edge on every widescreen display.

### What the scale actually does

Scaling the whole kit uniformly is what "make it smaller" means — shrinking only the theme's font sizes
would leave text rattling around inside boxes that stayed the same size, which reads as broken rather than
smaller. So `setScale` moves chrome, text, spacing and positions together.

Scaling **down** *enlarges* the usable canvas: at 75 the same widget rect holds `853 / 0.75` = 1137 units
across, so there is **more** room to lay out in, not less. Which means the effect depends on how a widget
is positioned:

- **Fixed coordinates** (`x = 40, w = 300` — how nearly every mod in the wild is written) shrink and grow
  with the scale, as you'd expect.
- **Coordinates derived from `CANVAS_W`** keep filling the screen at any scale, because the canvas grows
  as the scale shrinks. There, lowering the scale makes text and chrome *finer* against same-sized boxes
  rather than making anything smaller.

That distinction is not academic — per the commit that added the scale, a value approved against one
layout stopped meaning the same thing once a demo was re-spaced to fill the wider canvas, because the
columns grew with it.

### Two fixes worth knowing about

**`setScale` no longer builds the whole UI as a side effect of setting a number.** It used to call into
the movie unconditionally, and `_rtcall` runs `rtEnsure`, which constructs and shows the fullscreen
runtime widget and loads `ess_ui.gfx`. So a bare `Ess.UI.setScale(80)` in an `OnLoad` script spun the
entire kit up before any widget was wanted, purely to store a number. It now only reaches for the movie if
one already exists — the scale is stored either way, and the ready handshake pushes it. (`Ess.UI.Theme.apply()`
still has this behaviour; see [above](#essuitheme).)

**The widget rect was counting the scale twice.** `widgetRect()` used to return `CANVAS_W`/`CANVAS_H`,
which are themselves scale-derived (`STAGE_W * 100 / SCALE`) — so the rect was inflated by `1/s` *and* the
movie's content was then scaled by `s`. The two didn't cancel, because only one of them affects where a
coordinate lands on screen.

> **Consequence, with the numbers from the fix commit:** a 520-unit panel covered **61% of the display
> instead of the 520/1895 = 27%** its coordinates imply. That is why the kit read "massive" at scale 100
> and only looked sane around 10 — a user turning the scale down was compensating for a squared factor,
> not setting a density.

The rect and the scale do different jobs: the rect maps the movie's **stage** onto widget space, the scale
shrinks content **inside** the stage. Working the contract through — content at scale `s`, in a rect of
`R` widget units with stage `S` mapped onto it, lands at `x · s · (R/S)`; for `x = CANVAS_W` to be the
right-hand screen edge with `CANVAS_W = S/s`, that has to equal a widescreen display's 853 units, so
`(S/s) · s · (R/S) = R ⟹ R = 853`. The scale cancels out entirely and the rect is simply the stage size.
The 4:3 branch was already right (a fixed 640, not a derived one), so only the widescreen path was
affected.

**Live-verified**, per that commit: on a clean boot at scale 45, the rect reports 853×480, four edge
markers land on the real edges and centre, and a panel built exactly `CANVAS_W/4` wide at `CANVAS_W/4`
across spans precisely the second quarter of the display — left edge at 25%, right edge at the halfway
point.

### The default scale changed

`Ess.UI.SCALE` defaults to **75** (confirmed in `src/42_ui_engine.lua`). It was 45 while `widgetRect()`
was double-counting; with the geometry corrected, 45 and then 55 both read too small **once the small text
was the thing being judged** rather than a demo grid. Menus are mostly body text at `sizeBody`, so that's
the case to tune against — chrome and headers look fine at densities where rows are already hard to read.

Two related notes:

- Widening the stage from 640 to 853 means **the kit renders ~25% smaller than it did pre-0.5.0** at the
  same coordinates, since 853 units now span the width 640 used to. Existing coordinates stay valid; if it
  reads small, that's a theme change (`sizeBody`/`sizeTitle`/`rowHeight`), not a layout one.
- Measured on a 1440p 16:9 display: **2.354 px per widget unit**, so 640 units really is 75.4% of the
  display width — which is exactly why the pre-fix widget, built 640×480, left the entire UI living in the
  left three-quarters of the screen.

## The nine widgets

| Widget | What it is |
|---|---|
| [`Ess.UI.Menu`](#essuimenu) | A ForgeMenu-style declarative drill-down: `:entry`/`:category`/`:header`/`:switch`, nests as deep as you like. |
| [`Ess.UI.List`](#essuilist) | The raw scrolling list every other multi-row widget here is built on — a configurable row window, section headers, a scrollbar, auto-resize. |
| [`Ess.UI.Panel`](#essuipanel) | A title bar plus body lines, body auto-resizing to fit. No line cap. |
| [`Ess.UI.Bar`](#essuibar) | A label plus a progress bar. |
| [`Ess.UI.Toast`](#essuitoast) | A transient notification, stacked slots, auto-hiding. |
| [`Ess.UI.Confirm`](#essuiconfirm) | A modal yes/no dialog. |
| [`Ess.UI.Input`](#essuiinput) | A one-shot typed prompt. |
| [`Ess.UI.Chat`](#essuichat) | A scrolling message log with an optional typed input line. |
| [`Ess.UI.Board`](#essuiboard) | A two-pane list-plus-details view — since 0.5.0 a **composition** of List + Panel + Bar, not its own movie. |

Every widget shares `:show()` `:hide()` `:focus()` `:blur()` `:destroy()` — chainable, identical regardless
of which widget you're holding. Exactly one widget hears keys at a time (`Ess.UI.Focus(w)`/
`Ess.UI.Focused()`), and the heartbeat idles itself when nothing needs it. All of that plumbing is the
same design [UI Kit](../uilib/#why-one-shared-engine-instead-of-nine-separate-ones) documents in depth —
rebuilt here on `Ess.Gfx`/`Ess.Loop`/`Ess.Input`/`Ess.Time.clock`/`Ess.Player.pose` instead of `uilib.lua`'s
own private copies of the same mechanisms. `Ess.UI.wrap(s, width)` (default width 46), `Ess.UI.comma(n)`,
`Ess.UI.fmt_time(sec)`, and the remappable `Ess.UI.KEYS` table (`up`/`down`/`left`/`right`/`enter`/`esc`,
same VK defaults) all carry over unchanged.

The one piece of that plumbing that **did** change is the warm-up: per-widget repaint warm-up is gone, and
so is the "widget state is re-sent 8 times after `:show()`" behaviour. See
[Async load is handled, not worked around](#the-runtime-rewrite).

`Ess.UI` lives in `src/41_ui_theme.lua` and `src/42_ui_engine.lua` through `src/49_ui_menu.lua`, plus
`src/54_ui_chat.lua`/`src/55_ui_board.lua`.

## Where the native port genuinely differs

This section compares `Ess.UI` against its `uilib.lua` ancestor (whose full text is reproduced on
[uilib.lua](../uilib/source)). Since 0.5.0 the rendering path is no longer comparable at all — every
difference in [The runtime rewrite](#the-runtime-rewrite) is also a difference from `uilib.lua`. What
follows is the **logic** differences, which are what a script written against `uilib.lua` will actually
notice.

`Menu` and `Confirm` remain byte-for-byte logic carry-overs apart from swapped globals (`UI`→`Ess.UI`,
`Loader.Printf`→`Ess.Log`) and the retargeted draw calls. The rest:

- **Held Up/Down now auto-repeats.** The shared heartbeat (`src/42_ui_engine.lua`) added a held-key
  auto-repeat for the scroll axis: after `Ess.UI.REPEAT_DELAY` (0.35s) of holding Up or Down, it re-fires
  `_keyvk` every `Ess.UI.REPEAT_RATE` (0.06s) until released, like an OS text-cursor repeat. Only Up/Down
  repeat — Enter/Esc/Left/Right stay single-shot on purpose, so a stuck key can't machine-gun a "pick"/"back"
  action. `uilib.lua` had no such repeat at all: every move required a fresh discrete key-down edge from
  `Loader.PopKeyEvents()`. This applies to *whatever widget currently has focus and defines `_keyvk`* — List,
  Menu, and Board's scrolling all get it; so, incidentally, does Confirm's Left/Right/Up/Down toggle, since
  Confirm's own `_keyvk` treats all four the same way.
- **`Ess.UI.List` wraps at the ends** — and **as of 0.5.0 so does `Ess.UI.Board`.** Pressing Down on the
  last selectable row jumps to the first; Up on the first jumps to the last (headers are skipped correctly
  either way). `uilib.lua`'s list simply stopped. Board used to carry its own near-copy of List's nav
  logic *without* the wrap, which made List/Menu and Board behave differently from each other inside
  `Ess.UI` itself; rebuilding Board as a composition over a real `Ess.UI.List` deleted that copy, so the
  inconsistency is gone. **This corrects what earlier revisions of this page said about Board.**
- **`Ess.UI.Chat` gained an opt-in `autoHide` option** (`opts.autoHide = seconds`) with no equivalent in
  `uilib.lua`'s `UI.Chat` at all. See [`Ess.UI.Chat`](#essuichat).
- **`Ess.UI.Toast`'s default footprint and position both moved**, and the defaults were retuned again for
  the wider canvas in 0.5.0. See [`Ess.UI.Toast`](#essuitoast) for the current numbers.
- **Construction-time visibility is a much smaller question than it was.** `uilib.lua`'s private
  `make_widget` unconditionally called `wg:SetVisible(true)` as its last step. Earlier `Ess.UI` built one
  `FlashWidget` per widget through `Ess.Gfx.widget`, which does **not** call `SetVisible` — so whether a
  bare `Ess.UI.List{...}` rendered without an explicit `:show()` was genuinely unclear. That's now down to
  one object: `rtEnsure` builds the single shared host widget and **explicitly** calls
  `Ess.Gfx.setVisible(gfx, true)` on it. Individual widgets are clips inside that movie, and
  `_attachRuntimeCommon` sets `o._shown = true` at construction — Lua's own model is that a freshly-built
  widget is shown, and `:hide()` is what makes it otherwise. Whether the *clip* draws before an explicit
  `:show()` is decided by `ess_ui.gfx`, which is authored in a separate repo and can't be read from the Ess
  source tree, so this page won't claim it either way. In practice `Menu` calls `rt.list:show():focus()`,
  `Confirm`/`Input` call `:show()` in their own constructors, and `Toast` sends `Show` explicitly, so the
  question only arises for a bare `List`/`Panel`/`Bar`/`Chat`/`Board`. Adding `:show()` costs nothing.

Everything else below — `Menu`'s builder and `ctx:` surface, `Confirm`'s default-to-NO safety rule, `Input`'s
US-layout typing, `Panel`/`Bar`'s auto-resize, `Board`'s two-pane shape — carries over unchanged; see
[UI Kit](../uilib/) for why each of those works the way it does.

## Ess.Gfx

The Raw tier: the FlashWidget boilerplate every one of `uilib.lua`, `contracts.lua`, ForgeCam, and ForgeMenu
used to hand-roll independently. `Ess.UI`'s own shared runtime host is built on this — but so can yours, for a
custom movie the kit doesn't cover. `samples/demos/MissionForge.lua` does exactly that: it drives `forge.gfx`
directly through `Ess.Gfx.widget`/`.call`/`.setVisible`, entirely outside `Ess.UI`.

| Function | Signature | Notes |
|---|---|---|
| `widget` | `Ess.Gfx.widget(file, x, y, w, h, onLoad?) -> widget \| nil` | Builds, positions, and adds a `FlashWidget` from a deployed `.gfx` asset. Returns `{ raw = <FlashWidget>, shown = false }`, or `nil` (logged) if construction fails. Does the corner-coordinate `SetLocation` math (`x, y, x+w, y+h`) once, centrally — the same bug [UI Kit](../uilib/panel-bar-toast#the-real-bug-behind-all-three-setlocation-takes-corners-not-a-size) documents (`SetLocation` wants absolute corners, not a width/height offset) is structurally impossible to get wrong again once every widget goes through this one constructor. Does **not** call `SetVisible`. **Note: it constructs successfully whether or not `file` resolves to a real asset** — which is what made the [0.5.1 wad bug](#install-warning-for-the-ui-wad) silent. |
| `call` | `Ess.Gfx.call(widget, fn, args) -> ok` | `pcall`-wrapped `CallActionScriptCallback(fn, args)`. `args` defaults to `{}`. |
| `onEvent` | `Ess.Gfx.onEvent(widget, name, cb) -> ok` | `pcall`-wrapped `SetFlashEventHandler`. The native shape needs a mandatory `(_, v)` two-arg callback plus a mandatory trailing `{}` third argument to the call itself — both easy to get subtly wrong by hand. This hides both; your `cb` just receives `v`. Register **every** name before the movie loads — see [above](#the-runtime-rewrite). |
| `setVisible` | `Ess.Gfx.setVisible(widget, bool)` | Works around a confirmed real bug: the getter is `GetVisible()` (not `IsVisible()`, which silently nil-calls), and it returns `1`/`0` — `not 0` is `false` in Lua, so a naive `SetVisible(not w:GetVisible())` toggle never flips. This never reads the getter back; it tracks its own `widget.shown` boolean. |
| `warmupRerender` | `Ess.Gfx.warmupRerender(rt, ticks = 8)` | Re-runs a zero-arg repaint thunk `rt` every 0.05s for `ticks` ticks, so at least one repaint lands after `SetSwfFile`'s async movie load actually finishes. **Superseded by `onLoad` for new code** — that fires exactly once, when the movie is actually ready, instead of re-sending state a fixed number of times and hoping. Kept for callers that predate it, and as a fallback for the case where a callback never fires. |
| `menuNav` | `Ess.Gfx.menuNav(widget, keys) -> stop()` | Polls `Ess.Input` for up/down/enter (default VK_UP/VK_DOWN/VK_RETURN, matching `Ess.UI.KEYS` if remapped) and forwards `Move`/`Choose` calls into a movie's own compiled AS2 menu logic — a HUD `FlashWidget` gets no native input of its own. Built on `Ess.Input.poll` (edge-triggered), not a raw per-key `IsKeyDown` loop. Returns a `stop()` function. |

**The `onLoad` parameter** is new in 0.5.0 and is the whole basis of the runtime rewrite's load handling.
`SetSwfFile`'s 2nd and 3rd parameters are a load-completion callback and its argument table — the engine's
own answer to the async-load problem, which this code previously passed `nil` for. The game itself uses
it (`resident/mrxgui.lua`: `_oFadeFlash:SetSwfFile("loadingscreen_standalone", _CompleteFadeFlashLoad, {0})`)
and registers its event handlers inside that callback. `Ess.Gfx.widget` passes `{}` as the argument table,
so your `onLoad` receives no arguments; it's `pcall`-wrapped and errors are logged.

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
`:confirm(text, onYes, onNo)`, `:ask(prompt, onSubmit, onCancel)`, and `:spawn(template, dist?, opts?)` —
`opts.useView = true` places it along the view yaw instead of the body yaw (see [Core
Primitives](core#essmath)/[Identity & World Query](identity-query#essplayer)); blank-template crash guard
unchanged.

**Byte-for-byte port**, confirmed by direct diff against `uilib.lua`'s `UI.Menu` (`src/49_ui_menu.lua` vs.
[uilib.lua's source](../uilib/source)): identical tree-builder, identical `_choose`/`_back`/`open`/`close`
logic, identical dynamic-label re-paint-and-restore-cursor behavior, identical one-menu-open-at-a-time rule
via `S.openId`, identical persistent-per-`id` runtime state so `:toggle()` really toggles without leaking a
list. `ctx:spawn`'s blank-template crash guard (`Pg.Spawn("")` is a native crash `pcall` can't catch) carries
over unchanged too.

**`src/49_ui_menu.lua` is genuinely untouched by the 0.5.0 rewrite** — confirmed by `git log`, its last
change predates it. Menu came along for free because it owns one [`Ess.UI.List`](#essuilist) and never
talked to a movie itself. It therefore inherits what List gained: the runtime draw path, the theme, the
scale, and the wraparound cursor. (Not `opts.rows`, though — `Ess.UI.Menu` exposes no `rows` option and
builds its list without one, so a menu always gets List's default 10-row window.)

See [UI.Menu](../uilib/menu) for the full design writeup — the tree-to-list translation, the "why this is
the one thing `UI.Menu` can do that plain ForgeMenu can't" composition story, and the `ctx:spawn`
crash-guard history.

## Ess.UI.List

```lua
local list = Ess.UI.List{
    x = 40, y = 60, w = 320, rows = 12, title = "PICK ONE",
    items = { { header = "SECTION A" }, { label = "First", any = 1 } },
    onChoose = function(item, i, list) Ess.Log("picked " .. tostring(item.any)) end,
    onBack   = function(list) list:hide() end,
}
```

**`Ess.UI.List(opts)`**: `x`/`y` (default `40, 60`), `w` (default `320`), **`rows`** (visible row window,
default `10`, clamped to at least 1), `title`, `crumb`, `hint`, `items`, `empty`, `focus`, plus
`onSelect`/`onChoose`/`onBack`.

**`opts.h` is no longer read.** The movie derives the body height from the theme's metrics and the row
count, so height is a consequence of `rows`, not an input. Passing `h` is silently ignored.

| Call | Signature | Notes |
|---|---|---|
| `:items(t)` | `items(t) -> self` | Flat array of headers (`{ header = "TEXT" }`) and rows (`{ label = ..., ... }`). |
| `:selected()` | `selected() -> item, i` | |
| `:select(i)` | `select(i) -> self` | No-op if `i` isn't selectable. |
| `:paint()` | `paint() -> self` | Re-sends rows/selection/scroll offsets to the movie; called internally by `:items()`. |
| `:title(s)` / `:crumb(s)` / `:hint(s)` | `-> self` | Update the movie immediately, chainable. |
| `:measure(cb)` | `measure(cb) -> self` | Async; `cb(w, h, all)`. See [above](#the-runtime-rewrite). |

Callbacks: `onSelect(item, i, list)` on every cursor move, `onChoose(item, i, list)` on Enter/Right,
`onBack(list)` on Left/Esc.

**The cursor wraps.** `src/43_ui_list.lua`'s `_keyvk`:

```lua
local t = nearest(o._sel + d, d)
-- rolled off an end -> wrap around to the other end
if not t then t = (d == 1) and nearest(1, 1) or nearest(#o._items, -1) end
```

Down past the last selectable row jumps to the first; Up past the first jumps to the last (headers are
skipped correctly in both directions). `uilib.lua`'s `UI.List` had no such fallback. Since
[`Ess.UI.Menu`](#essuimenu) is one owned `Ess.UI.List` and [`Ess.UI.Board`](#essuiboard) is now built on one
too, every drill-down menu and every board wraps.

**Windowed on purpose.** The list shows `rows` rows at a time and indexes into the item table with an
offset, rather than creating a clip per item — O(visible) rather than O(total), which matters because a
real user menu in the wild has 831 entries. The rewrite also deleted the pixel constants
(`TOP`/`PITCH`/`TRH`/`BODY`) that tied the scrollbar and resize maths to `ui_list.gfx`'s exact artwork:
the movie now derives both from the theme's own metrics, so restyling `rowHeight` no longer silently
desynchronises the scrollbar. `:paint()` sends **data offsets, not pixels** (`RowsScroll(id, off, total, vis)`)
and the movie works out the thumb.

`opts.empty` sets the text drawn when there are no items. There is no Lua-side default any more — with
`empty` unset, whatever `ess_ui.gfx` draws for an empty list is what you get.

See [UI.List](../uilib/list) for the full drill-down-without-`UI.Menu` recipe.

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
| `:line(i, s)` | Sets line `i` (0-indexed). **No upper bound** — `:line(20, s)` works. A non-empty line past the current `:fit()` count auto-grows it. Negative `i` is a no-op. |
| `:fit(n)` | Sets the visible line count. **Clamps only at 0**, no ceiling. |
| `:clear()` | Blanks every line, fits back to 0. |
| `:measure(cb)` | Async; `cb(w, h, all)` with the panel's real laid-out box. |

Three changes in 0.5.0 — the first two confirmed from `src/44_ui_panel.lua`, the third from the commit
that made it (the header band is drawn by `ess_ui.gfx`, so no Lua file can show it):

- **The 8-line cap is gone.** `ui_panel.gfx` hand-listed eight text fields (`p_line0`…`p_line7`), so
  `:line(8, s)` and beyond silently did nothing and `:fit(n)` clamped at 8. Behaviour for `i <= 7` is
  identical.
- **Panels are write-through.** The Lua-side line cache only existed to re-send state during warm-up, and
  the call queue makes that unnecessary.
- **A title-less panel draws no header band.** Previously the header was always drawn, so every widget
  built on Panel without a title carried a big empty accent bar. The change is threaded through the
  movie's `RowTopFor` so the body rows and the auto-fit height follow it. This is what dropped a
  [toast](#essuitoast) from ~56 units tall to ~30 — and it fixes any other title-less panel for free.

Also gone: the `panel_px(n) = 40 + 18*n` sizing formula this page used to document. The movie owns the
layout now and derives it from the theme, which is exactly why `:measure()` exists — duplicating that
arithmetic in Lua is what previously drew a bar through the middle of a tall panel.

See [UI.Panel](../uilib/panel-bar-toast) for the rolling-event-log recipe.

## Ess.UI.Bar

```lua
local b = Ess.UI.Bar{ x = 20, y = 330, label = "Loading" }
b:set(0.4)
```

**`Ess.UI.Bar(opts)`**: `x`/`y` (default `20, 330`), `w`/`h` (default `300, 36`), `label`, `value` (initial
`0..1`, default `0`).

| Call | Notes |
|---|---|
| `:set(v)` | Clamps `0..1`. |
| `:label(s)` | Updates the text. |
| `:measure(cb)` | Async; `cb(w, h, all)`. |

Retargeted onto the runtime with the API, argument names and default position/size all unchanged, so
existing call sites land identically. The bar's fill and track colours come from the theme
(`barFill`/`barTrack`). Note `o._pct` — which this object has always exposed to anything poking at it
directly — is still `0..100`; the movie takes the `0..1` form. See [UI.Bar](../uilib/panel-bar-toast) for
context.

## Ess.UI.Toast

```lua
Ess.UI.Toast("Wardrobe Unlocked!")
Ess.UI.Toast("Something urgent", { ttl = 8 })
```

A function, not a constructor — finds a free slot (or steals the soonest-expiring one once all
`Ess.UI.TOAST_SLOTS` are busy), shows it, and starts its countdown. Returns the underlying toast object
(`:dismiss()` clears it early), but most calls are fire-and-forget. Each slot is a runtime *panel* —
`src/46_ui_toast.lua` drives the same movie-side calls [`Ess.UI.Panel`](#essuipanel) does rather than
constructing an `Ess.UI.Panel` object — and it is deliberately **title-less**, which since 0.5.0 means no
header band at all.

**The tunables, as they stand in `src/42_ui_engine.lua`.** These are ordinary overridable `Ess.UI.*`
globals; the values changed twice — once in the uilib port, once when the canvas widened to 853 — so the
numbers below are the current ones, not the changelog's:

| Constant | `uilib.lua` (hardcoded) | `Ess.UI` today |
|---|---|---|
| Box width | 320 | `Ess.UI.TOAST_W` = **190** |
| Box height | 44 | `Ess.UI.TOAST_H` = **22** |
| Slot pitch | 50 | `Ess.UI.TOAST_GAP` = **34** |
| X | `640 - 320 - 8` = 312 | `Ess.UI.TOAST_X` is **deliberately unset** — see below |
| Y | 150 | `Ess.UI.TOAST_Y` = 150 (unchanged) |
| Slots | 3, a hard ceiling | `Ess.UI.TOAST_SLOTS` = 3, a **tunable** |
| Lifetime | 4s | `Ess.UI.TOAST_TTL` = 4 |

**`TOAST_X` is unset on purpose.** The usable width depends on `Graphics.GetScreenRatio()`, which may not
be answerable at `OnLoad` time, so `Ess.UI.Toast` resolves it lazily against the real canvas each time it
builds a slot: `Ess.UI.TOAST_X or (Ess.UI.canvasW() - Ess.UI.TOAST_W - 8)`. At the default scale of 75
that puts the left edge at `1137 - 190 - 8` = 939. Setting `Ess.UI.TOAST_X` explicitly still overrides.
The old hardcoded `640 - TOAST_W - 8` is precisely the bug [`Ess.UI.anchor`](#essuisetscale-and-the-canvas)
exists to prevent — it put toasts ~213 units left of the real edge on every widescreen display.

`TOAST_GAP` is the **pitch** between stacked slots, not the empty space between them: a title-less toast
is ~30 units tall, so 34 leaves a small visual gap without the stack drifting far down the screen.

**Text is no longer pre-wrapped in Lua.** The movie's text field wraps natively, so a long toast wraps
properly instead of being cut to the two lines the old movie had fields for. `Ess.UI.wrap` is still
exported for your own use — it just isn't called here any more.

Everything else — the steal-the-soonest-expiring-slot rule, the countdown (run by the shared heartbeat),
`:dismiss()` — is unchanged. See
[UI.Toast](../uilib/panel-bar-toast#uitoast--a-transient-notification) for the stacking behavior.

## Ess.UI.Confirm

```lua
Ess.UI.Confirm{
    text = "Delete this save slot?",
    onResult = function(yes) if yes then DoDelete() end end,
}
```

**`Ess.UI.Confirm(opts)`**: `text`, `title` (default `"CONFIRM"`), `yes`/`no` (default `"YES"`/`"NO"`),
`onResult` — called exactly once with a plain boolean. Also accepts `x`/`y` (default `180, 200`); the box
is a fixed 300×110 in canvas units. A **singleton**: calling it again while one's open reconfigures and
re-shows the same widget.

**Caveat on `x`/`y`:** they're read inside the `if not o then` construction branch, so only the *first*
`Ess.UI.Confirm` call of a world positions the dialog — every later call reuses the same clip at the same
place and silently ignores them. (The singleton is cleared on world reload, so the next world's first call
gets its say again.)

Left/Right/Up/Down flip the highlighted choice, Enter commits, **Esc always resolves `false`** regardless of
what's highlighted, and the highlight **defaults to NO**. Remembers whatever was focused before it and
restores that focus once resolved.

**Byte-for-byte logic port** — `src/47_ui_confirm.lua` matches `uilib.lua`'s `UI.Confirm`, only the globals
and the draw calls swapped. Two things to know:

- **The message is no longer clipped to two lines.** `ui_confirm.gfx` had exactly two message fields, so
  anything longer was silently cut. The wrap is still done in Lua (`Ess.UI.wrap` at 44 columns) rather than
  letting the field wrap natively, so the dialog's width stays predictable regardless of message length,
  and there is a `MAX_LINES` of 8 — labelled in source as "a sanity bound, not a format limit: a dialog
  taller than this is a panel."
- Since Left/Right/Up/Down are all treated identically by Confirm's `_keyvk`, the engine's [held-key
  auto-repeat](#where-the-native-port-genuinely-differs) means holding **Up or Down** keeps flipping the
  highlighted choice every `Ess.UI.REPEAT_RATE` seconds — `uilib.lua` required a fresh key-down edge per
  flip. Held Left/Right do *not* repeat: the heartbeat only auto-repeats the scroll axis
  (`Ess.UI.KEYS.up`/`.down`), whatever the focused widget does with the other keys.

`Confirm` explicitly calls `:show()`/`:focus()` in its own constructor. See
[UI.Confirm](../uilib/confirm-and-input) for the "escape never accidentally confirms" reasoning.

## Ess.UI.Input

```lua
Ess.UI.Input{
    prompt = "ENTER A NAME",
    onSubmit = function(text) Ess.Log("got: " .. text) end,
    onCancel = function() Ess.Log("cancelled") end,
}
```

**`Ess.UI.Input(opts)`**: `prompt` (default `"INPUT -- ENTER SUBMIT   ESC CANCEL"`), `text` (default `""`),
`max` (default `120`), `onSubmit(text)`, `onCancel()`. Also accepts `x`/`y` (default `160, 260`); the box is
a fixed 340×56 in canvas units. A **singleton**, same as `Confirm` — including the same caveat that `x`/`y`
are only honoured by the first call of a world, since they're read in the construction branch.

Enter submits, Esc cancels and discards, Backspace deletes one character. Long entries truncate from the
front past 40 characters (`ECHO_COLS`, rendered as `"..." .. tail`). Same focus-save/restore as `Confirm`;
explicitly calls `:show()`/`:focus()` in its own constructor.

The echo line is drawn through the runtime's `Foot` call rather than a body line — the primary text colour
along the bottom, which is where `ui_input.gfx` put it. The caret blink is still driven by the heartbeat
(it checks `_isInput` and calls `_echo`), because it's input state rather than decoration.

**Logic is byte-for-byte identical to `uilib.lua`'s `UI.Input`.** The one implementation change: character
typing goes through the now-shared `Ess.Input.VkToChar(vk, shift)` instead of `uilib.lua`'s own private
`CHAR` table — per `src/48_ui_input.lua`'s header comment and [Timing & Input](timing-input#essinput), it's
the same table, "ported byte-for-byte from uilib's `CHAR` table," still US-layout-only (edit `Ess.Input`'s
`PUNCT` for other layouts). See [UI.Input](../uilib/confirm-and-input#typed-character-mapping) for the full
VK-mapping table.

## Ess.UI.Chat

```lua
local ch = Ess.UI.Chat{ title = "RADIO", x = 20, y = 330, w = 384, lines = 8 }
ch:push("Misha: slick menu, boss.")
ch:prompt(function(text) Ess.Log("you said: " .. text) end)
```

**`Ess.UI.Chat(opts)`**: `x`/`y` (default `20, 400`), `w`/`h` (default `360, 132`), `title`, **`lines`**
(visible window, default `5`, at least 1), `max` (stored scrollback cap, default `60`), `onSubmit`, and
`autoHide` (see below).

| Call | Notes |
|---|---|
| `:push(text)` | Word-wraps (52 chars, `Ess.UI.wrap`) and appends; trims oldest past `max`. The last `lines` lines show; body auto-resizes to fit. |
| `:prompt([onSubmit])` | Enters typed-input mode; Enter pushes the text and fires `onSubmit`, Esc cancels. Typed text is capped at 200 characters, echoed tail-anchored past 44. |
| `:title(s)` / `:clear()` | |
| `:measure(cb)` | Async; `cb(w, h, all)`. |

**The 5-line window is now `opts.lines`.** It was hard-wired to 5 only because `chat.gfx` had five message
fields; it can be any size now. `opts.max` still bounds the stored backlog separately, as before.

**`opts.autoHide = seconds`** — a confirmed new feature with no `uilib.lua` equivalent. Auto-hides the
window that many seconds after the last `:push()`. Per `src/54_ui_chat.lua` and the shared heartbeat's
`o._hideIn` handling in `src/42_ui_engine.lua`: the countdown is **frozen while the widget holds input
focus** (it never fades out mid-type) and re-arms — resurfacing the window if it had faded — on every new
`:push()`. Omit it for the old always-visible behavior. Confirmed real usage,
`samples/demos/CoopChat.lua`:

```lua
C.ui = Ess.UI.Chat{ x = 20, y = 330, w = 384, title = "CO-OP CHAT", onSubmit = onSubmit, autoHide = 10 }
```

The underlying `_hideIn`/`_autoHide` mechanism in the shared heartbeat is generic to any widget in `S.live`,
but `Ess.UI.Chat` is the only constructor that currently exposes it as an option. **Not related to** the
[Co-op Text Chat](../deep-dives/coop-chat) deep dive's `MrxGuiTextBuffer`-based network chat — see
[UI.Chat](../uilib/chat-and-board#uichat--a-scrolling-log-with-an-optional-typed-line) for that distinction.

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

**`Ess.UI.Board(opts)`**: `x`/`y` (default `60, 60`), `w`/`h` (default `660, 420`), `rows` (default `12`),
`title`, `hint`, `items`, `focus`, plus `onSelect`/`onChoose`/`onBack`.

| Call | Notes |
|---|---|
| `:items(t)` / `:selected()` / `:select(i)` / `:title(s)` / `:hint(s)` / `:paint()` | Forwarded straight to the owned list. |
| `:detail(d)` | `{ title=, category=, rewards={}, objectives={}, progress=0..1, progressText= }`. **No caps** on `rewards` or `objectives` any more. |

### Rebuilt as a composition

This is the biggest structural change in the kit. **`Ess.UI.Board` is now literally an
[`Ess.UI.List`](#essuilist) beside an [`Ess.UI.Panel`](#essuipanel) with an [`Ess.UI.Bar`](#essuibar) under
it** — three existing widgets on the shared runtime, rather than a fourth bespoke movie. It no longer
drives `contracts.gfx` at all.

The left pane takes `math.floor(w * 0.42)` of the width, then a 10-unit gap, then the detail pane. The
list is deliberately **not** focused itself: the Board owns focus and forwards every key to it
(`o:_keyvk(vk, shift)` → `o._list:_keyvk(vk, shift)`), so exactly one object sits in the engine's focus
slot, preserving the kit's one-focus rule.

What that bought, per the commit — *"a feature gained by removing code"*:

- It deleted Board's private copy of List's windowing logic (`selectable`/`nearest`, the offset maths, the
  scrollbar arithmetic — all duplicated with slightly different constants).
- It therefore **inherits List's wraparound cursor**, which its own copy never had. Earlier revisions of
  this page documented Board as the one widget without it; that is no longer true.
- Fixes and features landing in `Ess.UI.List` now reach Board automatically.

`:detail(d)` lays the right pane out as a flat run of lines — category, blank, `REWARDS` + indented
entries, blank, `OBJECTIVES` + indented entries — into the owned Panel, then sets the Bar from `progress`
and uses `progressText` as the Bar's **label**. `d.title` retitles the detail panel (it defaults to
`"DETAILS"`).

**Three option names quietly stopped being read** when Board became a composition — confirmed by reading
`src/55_ui_board.lua`'s constructor, which forwards only `x`/`y`/`w`/`rows`/`title`/`hint` and the three
callbacks to its list:

| Option | Status |
|---|---|
| `empty` | Not forwarded to the owned list. Set it on a list you build yourself if you need it. |
| `crumb` | Not forwarded either. |
| `detail` (initial payload) | Not read at construction. Nor does `:items()` fire `onSelect` — `Ess.UI.List`'s `onSelect` only fires on a cursor *move* — so a freshly-opened board shows an empty detail pane until the user presses a key. Call `:detail(d)` yourself right after `:items(...)` if you want it populated on open. |

Also worth knowing: `h` only positions the progress bar (`y + h - 44`). The list and detail panel size
themselves from `rows` and the theme, so a Board's real height is not exactly `h`.

Per `src/55_ui_board.lua`'s own header comment, [`Ess.Contract`](contract)'s board UI is built on this
widget. (Heads-up for anyone reading the source: `src/96_console.lua`'s header comment still describes
Board as "reusing the `contracts.gfx` movie" — that comment is stale, the movie is no longer involved.)
See [UI.Board](../uilib/chat-and-board) for the original two-pane design and the `menudemo.lua` usage
pattern.

## Ess.ScrollLog

A scrolling on-screen text buffer via the one confirmed bug-free construction path for
`MrxGuiTextBuffer` — unrelated to the `Ess.UI` engine above (no shared focus/heartbeat, no `:show()`/`:hide()`/
`:focus()`/`:blur()`/`:destroy()` common surface, and no dependency on `ess_ui.gfx`, so it is the one part
of this page that still worked on a 0.5.1 install).

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
| `Ess.Easy.Console.open()` | Browses the whole `Ess.Easy.*` surface in-game, searchable — built on [`Ess.UI.Board`](#essuiboard) for the list+detail view and `Ess.TextConsole` for the search box. |

See [Ess.Easy](easy) for the complete one-liner catalog.

## See also

- [Essentials (Ess)](index) — the framework index this page belongs to.
- [UI Kit](../uilib/) — the standalone predecessor `Ess.UI` is a native port of; the design reasoning behind
  the shared engine (input/focus/heartbeat) lives there, not repeated here. Note the rendering path
  described on that page is the pre-0.5.0 one.
- [Ess.Easy](easy) — the full beginner-tier one-liner catalog, including `Ess.Easy.Console`'s complete
  registry.
- [Timing & Input](timing-input) — `Ess.Input`/`Ess.Loop`/`Ess.Time.clock`, the primitives `Ess.UI`'s engine
  is built on; `Ess.TextConsole`, the `.gfx`-free alternative to `Ess.UI.Input`.
- [Contract Engine](contract) — `Ess.Contract`'s own board UI is built directly on `Ess.UI.Board`.
